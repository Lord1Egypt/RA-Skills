// OpenClaw Moltbook Plugin v0.2
// Direct API integration - no Ollama dependency
// Added: moltbook_goto_submolt, improved error handling with time negotiation

const MOLTBOOK_API = "https://www.moltbook.com/api/v1";
const MOLTBOOK_WEB = "https://www.moltbook.com";
const DEFAULT_TIMEOUT = 15000;

// Load credentials from ~/.config/moltbook/credentials.json
async function loadCredentials(): Promise<{ api_key: string; agent_name: string } | null> {
  try {
    const fs = await import("fs");
    const path = await import("path");
    const os = await import("os");

    const credPath = path.join(os.homedir(), ".config", "moltbook", "credentials.json");

    if (!fs.existsSync(credPath)) {
      return null;
    }

    const content = fs.readFileSync(credPath, "utf-8");
    return JSON.parse(content);
  } catch {
    return null;
  }
}

// Generic fetch with timeout
async function moltbookFetch(
  endpoint: string,
  options: RequestInit = {},
  timeoutMs: number = DEFAULT_TIMEOUT
): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const credentials = await loadCredentials();
    if (!credentials) {
      throw new Error("Moltbook credentials not found. Create ~/.config/moltbook/credentials.json with api_key and agent_name");
    }

    const response = await fetch(`${MOLTBOOK_API}${endpoint}`, {
      ...options,
      headers: {
        "Authorization": `Bearer ${credentials.api_key}`,
        "Content-Type": "application/json",
        ...options.headers,
      },
      signal: controller.signal,
    });

    return response;
  } finally {
    clearTimeout(timeout);
  }
}

// Check rate limit (2.5 min cooldown)
async function checkRateLimit(): Promise<{ allowed: boolean; waitSeconds?: number }> {
  try {
    const fs = await import("fs");
    const path = await import("path");
    const os = await import("os");

    const statePath = path.join(os.homedir(), ".openclaw", "moltbook-state.json");

    if (!fs.existsSync(statePath)) {
      return { allowed: true };
    }

    const state = JSON.parse(fs.readFileSync(statePath, "utf-8"));
    const lastPost = state.last_post_time || 0;
    const now = Date.now();
    const cooldown = 150000; // 2.5 minutes in ms

    if (now - lastPost < cooldown) {
      const waitSeconds = Math.ceil((cooldown - (now - lastPost)) / 1000);
      return { allowed: false, waitSeconds };
    }

    return { allowed: true };
  } catch {
    return { allowed: true };
  }
}

// Update rate limit state
async function updateLastPost(): Promise<void> {
  try {
    const fs = await import("fs");
    const path = await import("path");
    const os = await import("os");

    const stateDir = path.join(os.homedir(), ".openclaw");
    const statePath = path.join(stateDir, "moltbook-state.json");

    if (!fs.existsSync(stateDir)) {
      fs.mkdirSync(stateDir, { recursive: true });
    }

    let state: any = {};
    if (fs.existsSync(statePath)) {
      state = JSON.parse(fs.readFileSync(statePath, "utf-8"));
    }

    state.last_post_time = Date.now();
    fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
  } catch {
    // Ignore state update failures
  }
}

// =============================================================================
// TOOL IMPLEMENTATIONS
// =============================================================================

async function executeMoltbookPost(
  _toolCallId: string,
  params: { title?: string; content: string; submolt?: string },
  _signal?: AbortSignal
) {
  const { title = "", content, submolt = "general" } = params;

  // Check rate limit
  const rateCheck = await checkRateLimit();
  if (!rateCheck.allowed) {
    return {
      content: [{ type: "text" as const, text: `Rate limited. Wait ${rateCheck.waitSeconds} seconds before posting again.` }],
    };
  }

  const body = {
    submolt,
    title,
    content,
  };

  const response = await moltbookFetch("/posts", {
    method: "POST",
    body: JSON.stringify(body),
  });

  if (response.status === 429) {
    const data = await response.json().catch(() => ({})) as { message?: string; retry_after_seconds?: number };
    return {
      content: [{ type: "text" as const, text: `Rate limited: ${data.message || "Please wait before posting again"}. Retry after: ${data.retry_after_seconds || "unknown"} seconds.` }],
    };
  }

  if (!response.ok) {
    const error = await response.text();
    return {
      content: [{ type: "text" as const, text: `Moltbook post failed (${response.status}): ${error}` }],
    };
  }

  const data = await response.json() as { id?: string; post?: { id?: string } };
  await updateLastPost();

  const postId = data.id || data.post?.id;
  const postUrl = postId ? `https://www.moltbook.com/post/${postId}` : "unknown";

  return {
    content: [{ type: "text" as const, text: `Posted to moltbook (${submolt}): ${title || "(no title)"}\nURL: ${postUrl}` }],
  };
}

async function executeMoltbookCheckNotifications(_toolCallId: string) {
  try {
    const response = await moltbookFetch("/home");

    if (!response.ok) {
      return {
        content: [{ type: "text" as const, text: `Failed to check notifications: ${response.status}` }],
      };
    }

    const data = await response.json() as { karma?: number; notifications?: { unread_count?: number }; dms?: { unread_count?: number }; dm_requests?: unknown[] };

    const karma = data.karma || 0;
    const unreadNotifications = data.notifications?.unread_count || 0;
    const unreadDMs = data.dms?.unread_count || 0;
    const pendingRequests = data.dm_requests?.length || 0;

    let report = `Moltbook Status:\n- Karma: ${karma}\n- Unread notifications: ${unreadNotifications}\n- Unread DMs: ${unreadDMs}`;

    if (pendingRequests > 0) {
      report += `\n- Pending DM requests: ${pendingRequests}`;
    }

    return { content: [{ type: "text" as const, text: report }] };
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    return {
      content: [{ type: "text" as const, text: `Error checking moltbook: ${message}` }],
    };
  }
}

async function executeMoltbookBrowse(
  _toolCallId: string,
  params: { feed_type?: string; limit?: number; submolt?: string }
) {
  const { feed_type = "hot", limit = 10, submolt } = params;

  // Try API first
  let endpoint = `/feed?sort=${feed_type}&limit=${limit}`;
  if (submolt) {
    endpoint += `&submolt=${submolt}`;
  }

  try {
    const response = await moltbookFetch(endpoint);

    if (response.ok) {
      const data = await response.json() as { posts?: { title?: string; author?: { name?: string }; upvotes?: number; comment_count?: number; submolt?: { name?: string } }[] };
      const posts = data.posts || [];

      if (posts.length === 0) {
        return { content: [{ type: "text" as const, text: "No posts found." }] };
      }

      let report = `Moltbook Feed (${feed_type}):\n`;

      for (const post of posts.slice(0, limit)) {
        const title = post?.title || "(no title)";
        const author = post?.author?.name || "unknown";
        const upvotes = post?.upvotes || 0;
        const comments = post?.comment_count || 0;
        const submoltName = post?.submolt?.name || "general";

        report += `\n[${submoltName}] ${title}\n  by ${author} | ${upvotes}↑ ${comments}💬\n`;
      }

      return { content: [{ type: "text" as const, text: report }] };
    }

    // API failed - try web fallback if submolt specified
    if (submolt && (response.status === 500 || response.status === 404)) {
      return await browseWebFallback(submolt, limit);
    }

    return {
      content: [{ type: "text" as const, text: `Failed to browse feed: ${response.status}. Moltbook API may be overloaded or in maintenance. Options: retry now, wait 5-30 minutes, or check web view: ${MOLTBOOK_WEB}/m/${submolt || ""}` }],
    };

  } catch (err) {
    // Network/API error - try web fallback if submolt specified
    if (submolt) {
      return await browseWebFallback(submolt, limit);
    }

    const message = err instanceof Error ? err.message : String(err);
    return {
      content: [{ type: "text" as const, text: `Moltbook API unreachable: ${message}. This could be temporary overload or maintenance.` }],
    };
  }
}

// Web fallback for browsing specific submolt
async function browseWebFallback(submolt: string, limit: number): Promise<{ content: any[] }> {
  try {
    const response = await fetch(`${MOLTBOOK_WEB}/m/${submolt}`, {
      headers: { "Accept": "text/html" },
    });

    if (!response.ok) {
      if (response.status === 404) {
        return { content: [{ type: "text" as const, text: `m/${submolt} not found (via web check).` }] };
      }
      return { content: [{ type: "text" as const, text: `API failed, web fallback failed (${response.status}). Moltbook may be temporarily unavailable.` }] };
    }

    const html = await response.text();

    // Extract posts from HTML (basic parsing)
    const posts: any[] = [];
    const titleMatches = html.match(/<h[1-6][^>]*>([^<]+)<\/h[1-6]>/gi) || [];
    const authorMatches = html.match(/Posted by u\/([^\s<]+)/gi) || [];

    // Simple extraction - look for post patterns
    const postRegex = /<article[^>]*>.*?<\/article>/gis;
    const articles = html.match(postRegex) || [];

    let report = `Moltbook /m/${submolt} (via web fallback):\n`;

    if (articles.length === 0 && titleMatches.length < 2) {
      // Check for "Submolt not found" message
      if (html.includes("Submolt not found") || html.includes("doesn't exist")) {
        return { content: [{ type: "text" as const, text: `m/${submolt} doesn't exist yet.\n\nCreate it via: ${MOLTBOOK_WEB}/m/${submolt}` }] };
      }
      return { content: [{ type: "text" as const, text: `m/${submolt} found but no posts visible, or parsing failed. View directly: ${MOLTBOOK_WEB}/m/${submolt}` }] };
    }

    // Extract up to limit posts
    let count = 0;
    for (const article of articles.slice(0, limit)) {
      const titleMatch = article.match(/<h[1-6][^>]*>([^<]+)<\/h[1-6]>/i);
      const authorMatch = article.match(/u\/([^\s<]+)/);
      const upvoteMatch = article.match(/(\d+)\s*↑/);

      if (titleMatch) {
        const title = titleMatch[1].trim();
        const author = authorMatch ? authorMatch[1] : "unknown";
        const upvotes = upvoteMatch ? upvoteMatch[1] : "0";

        report += `\n[${submolt}] ${title}\n  by ${author} | ${upvotes}↑\n`;
        count++;
      }
    }

    if (count === 0) {
      // Try to find any post-like content
      const anyTitles = html.match(/<h[1-3][^>]*>([^<]{10,200})<\/h[1-3]>/gi) || [];
      if (anyTitles.length > 0) {
        report += "\n(Posts found but details incomplete - parsing limited)\n";
        for (const t of anyTitles.slice(0, limit)) {
          const cleanTitle = t.replace(/<[^>]+>/g, "").trim();
          if (cleanTitle.length > 10) {
            report += `\n- ${cleanTitle.substring(0, 100)}...\n`;
          }
        }
      } else {
        report += "\n(No parseable posts found - submolt may be empty or requires login)\n";
      }
    }

    report += `\n\nView full submolt: ${MOLTBOOK_WEB}/m/${submolt}`;

    return { content: [{ type: "text" as const, text: report }] };

  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    return { content: [{ type: "text" as const, text: `Web fallback failed: ${message}. Moltbook may be temporarily unavailable.` }] };
  }
}

async function executeMoltbookReply(
  _toolCallId: string,
  params: { post_id: string; content: string }
) {
  const { post_id, content } = params;

  const response = await moltbookFetch(`/posts/${post_id}/comments`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });

  if (!response.ok) {
    const error = await response.text();
    return {
      content: [{ type: "text" as const, text: `Failed to reply (${response.status}): ${error}` }],
    };
  }

  return {
    content: [{ type: "text" as const, text: `Replied to post ${post_id}` }],
  };
}

async function executeMoltbookFindSubmolt(
  _toolCallId: string,
  params: { query?: string }
) {
  const { query = "" } = params;

  const response = await moltbookFetch("/explore/submolts");

  if (!response.ok) {
    return {
      content: [{ type: "text" as const, text: `Failed to list submolts: ${response.status}` }],
    };
  }

  const data = await response.json() as { submolts?: { name?: string; display_name?: string; description?: string }[] };
  const submolts = data.submolts || [];

  let report = "Available submolts:\n";

  for (const s of submolts.slice(0, 20)) {
    const name = s?.name || "unknown";
    const display = s?.display_name || name;
    const description = s?.description || "";

    if (!query || name.includes(query) || display.includes(query)) {
      report += `\n- ${name}: ${display}\n  ${description}`;
    }
  }

  if (query) {
    report += `\n\n(Filtered by: "${query}")`;
  }

  return { content: [{ type: "text" as const, text: report }] };
}

async function executeMoltbookGotoSubmolt(
  _toolCallId: string,
  params: { submolt: string }
) {
  const { submolt } = params;

  // Try API first
  try {
    const response = await moltbookFetch(`/submolts/${submolt}`, {}, 10000);

    if (response.ok) {
      const data = await response.json() as { post_count?: number; last_active_at?: string };
      const postCount = data.post_count || 0;
      const lastActive = data.last_active_at ? new Date(data.last_active_at).toLocaleDateString() : "unknown";
      const url = `${MOLTBOOK_WEB}/m/${submolt}`;

      return {
        content: [{ type: "text" as const, text: `m/${submolt} exists:\n- Posts: ${postCount}\n- Last active: ${lastActive}\n- URL: ${url}` }],
      };
    }

    if (response.status === 404) {
      // Not found via API - check web for confirmation
      const webResponse = await fetch(`${MOLTBOOK_WEB}/m/${submolt}`, { method: "HEAD" });

      if (webResponse.status === 404 || webResponse.status === 302) {
        return {
          content: [{ type: "text" as const, text: `m/${submolt} doesn't exist yet.\n\nThe API may support creating this submolt. Try via web interface first.` }],
        };
      }
    }

    // API error with status
    return {
      content: [{ type: "text" as const, text: `Moltbook API is not responding properly (status ${response.status}). This could be:\n- Rate limiting (wait before retry)\n- Temporary overload\n- Scheduled maintenance\n\nOptions:\n- Retry now\n- Wait and auto-retry\n- Use web view: ${MOLTBOOK_WEB}/m/${submolt}` }],
    };

  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);

    if (message.includes("credentials")) {
      return {
        content: [{ type: "text" as const, text: message }],
      };
    }

    // Network/API failure - offer time negotiation
    return {
      content: [{ type: "text" as const, text: `Moltbook API unreachable: ${message}\n\nThis could be:\n- Network issues\n- API temporarily down\n- Rate limiting\n\nOptions:\n- Retry now\n- Retry in 5 minutes\n- Retry in 30 minutes\n- Check web status: ${MOLTBOOK_WEB}/status (if available)` }],
    };
  }
}

// =============================================================================
// PLUGIN REGISTRATION
// =============================================================================

interface PluginApi {
  registerTool: (tool: any) => void;
}

const moltbookPlugin = {
  id: "openclaw-moltbook",
  name: "Moltbook",
  description: "Moltbook collaboration space integration with submolt navigation",
  register(api: PluginApi) {
    api.registerTool({
      name: "moltbook_post",
      label: "Moltbook Post",
      description: "Post content to moltbook collaboration space. Rate limited to once per 2.5 minutes.",
      parameters: {
        type: "object",
        properties: {
          title: { type: "string", description: "Post title (optional)" },
          content: { type: "string", description: "Post body content (required)" },
          submolt: { type: "string", description: "Target community (default: general)" },
        },
        required: ["content"],
      },
      execute: executeMoltbookPost,
    });

    api.registerTool({
      name: "moltbook_check_notifications",
      label: "Moltbook Check Notifications",
      description: "Check karma, unread notifications, DMs, and pending requests.",
      parameters: {
        type: "object",
        properties: {},
      },
      execute: executeMoltbookCheckNotifications,
    });

    api.registerTool({
      name: "moltbook_browse",
      label: "Moltbook Browse",
      description: "Browse moltbook feed for posts and engagement opportunities.",
      parameters: {
        type: "object",
        properties: {
          feed_type: { type: "string", description: "Feed type: hot, new (default: hot)" },
          limit: { type: "number", description: "Number of posts to fetch (default: 10)" },
          submolt: { type: "string", description: "Filter to specific submolt (optional)" },
        },
      },
      execute: executeMoltbookBrowse,
    });

    api.registerTool({
      name: "moltbook_reply",
      label: "Moltbook Reply",
      description: "Reply to an existing post.",
      parameters: {
        type: "object",
        properties: {
          post_id: { type: "string", description: "ID of post to reply to (required)" },
          content: { type: "string", description: "Reply content (required)" },
        },
        required: ["post_id", "content"],
      },
      execute: executeMoltbookReply,
    });

    api.registerTool({
      name: "moltbook_find_submolt",
      label: "Moltbook Find Submolt",
      description: "List available submolts (communities) for posting.",
      parameters: {
        type: "object",
        properties: {
          query: { type: "string", description: "Filter by keyword (optional)" },
        },
      },
      execute: executeMoltbookFindSubmolt,
    });

    api.registerTool({
      name: "moltbook_goto_submolt",
      label: "Moltbook Goto Submolt",
      description: "Check if a submolt exists and get its stats. Provides time negotiation on API failure.",
      parameters: {
        type: "object",
        properties: {
          submolt: { type: "string", description: "Submolt name to check (required)" },
        },
        required: ["submolt"],
      },
      execute: executeMoltbookGotoSubmolt,
    });
  },
};

export default moltbookPlugin;
