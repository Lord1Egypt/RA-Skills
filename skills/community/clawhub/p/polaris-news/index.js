/**
 * Polaris News — OpenClaw Skill
 *
 * Verified news intelligence from The Polaris Report.
 * 160+ sources, 18 verticals, bias scored, confidence rated.
 */

const API_BASE =
  process.env.POLARIS_API_URL || "https://api.thepolarisreport.com";
const SITE_URL = "https://thepolarisreport.com";

const CATEGORIES = [
  "tech", "policy", "markets", "global", "science", "health",
  "startups", "ai_ml", "cybersecurity", "climate", "defense",
  "realestate", "biotech", "crypto", "politics", "energy", "space", "sports",
];

// ── Helpers ──────────────────────────────────────────────────────────────────

async function apiFetch(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

function confidenceBar(score) {
  const pct = Math.round((score || 0) * 100);
  return `${pct}%`;
}

function briefLink(id) {
  return `${SITE_URL}/brief/${id}`;
}

function footer() {
  return `\n—\nPowered by The Polaris Report\n${SITE_URL}`;
}

// ── /news [category] [limit] ─────────────────────────────────────────────────

async function handleNews(args) {
  let category = null;
  let limit = 5;

  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);
  for (const tok of tokens) {
    if (CATEGORIES.includes(tok.toLowerCase())) {
      category = tok.toLowerCase();
    } else if (/^\d+$/.test(tok)) {
      limit = Math.min(parseInt(tok, 10), 20);
    }
  }

  const params = new URLSearchParams({ limit: String(limit) });
  if (category) params.set("category", category);

  const data = await apiFetch(`/api/v1/agent-feed?${params}`);
  const briefs = data.briefs || [];

  if (briefs.length === 0) {
    return `No briefs found${category ? ` for "${category}"` : ""}. Try a different category.${footer()}`;
  }

  const header = category
    ? `Latest ${category.toUpperCase()} Intelligence`
    : "Latest Intelligence Briefs";

  const lines = [`${header}\n`];

  for (const b of briefs) {
    lines.push(
      `▸ ${b.headline}`,
      `  ${b.category.toUpperCase()} · Confidence ${confidenceBar(b.confidence)} · Bias ${(b.bias || 0).toFixed(2)}`,
      `  ${b.summary}`,
      `  ${briefLink(b.id)}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /brief [topic] ───────────────────────────────────────────────────────────

async function handleBrief(args) {
  const topic = (args || "").trim();
  if (!topic) {
    return "Usage: /brief [topic]\nExample: /brief impact of AI on healthcare";
  }

  const res = await fetch(`${API_BASE}/api/v1/generate/brief`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  });

  if (!res.ok) {
    if (res.status === 429) {
      return "Rate limit reached. Free tier allows 3 brief generations per day.\nUpgrade at https://thepolarisreport.com/pricing";
    }
    throw new Error(`API error ${res.status}`);
  }

  const data = await res.json();
  const b = data.brief;

  const lines = [
    `${b.headline}`,
    `${"─".repeat(40)}`,
    `${b.category.toUpperCase()} · Confidence ${confidenceBar(b.provenance?.confidence_score)} · Bias ${(b.provenance?.bias_score || 0).toFixed(2)}`,
    "",
    b.body,
  ];

  if (b.counter_argument) {
    lines.push("", "Counter-Argument:", b.counter_argument);
  }

  if (data.brief_url) {
    lines.push("", `Read more: ${SITE_URL}${data.brief_url}`);
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /search [query] ──────────────────────────────────────────────────────────

async function handleSearch(args) {
  const query = (args || "").trim();
  if (!query || query.length < 2) {
    return "Usage: /search [query]\nExample: /search semiconductor export controls";
  }

  const params = new URLSearchParams({ q: query, limit: "5" });
  const data = await apiFetch(`/api/v1/search?${params}`);
  const briefs = data.briefs || [];

  if (briefs.length === 0) {
    return `No results for "${query}". Try different keywords.${footer()}`;
  }

  const lines = [`Search: "${query}" — ${data.total} result${data.total !== 1 ? "s" : ""}\n`];

  for (const b of briefs) {
    lines.push(
      `▸ ${b.headline}`,
      `  ${b.category.toUpperCase()} · Confidence ${confidenceBar(b.confidence)} · Bias ${(b.bias || 0).toFixed(2)}`,
      `  ${b.summary}`,
      `  ${briefLink(b.id)}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /trending ────────────────────────────────────────────────────────────────

async function handleTrending() {
  const data = await apiFetch("/api/v1/popular?limit=5");
  const briefs = data.briefs || [];

  if (briefs.length === 0) {
    return `No trending briefs right now. Check back soon.${footer()}`;
  }

  const lines = ["Trending Now\n"];

  for (const b of briefs) {
    const id = b.brief_id || b.id;
    const summary = b.deck || b.summary || "";
    lines.push(
      `▸ ${b.headline}`,
      `  ${b.category.toUpperCase()} · ${b.views_24h || 0} views today · Confidence ${confidenceBar(b.confidence)}`,
      `  ${summary}`,
      `  ${briefLink(id)}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── Skill Entry Point ────────────────────────────────────────────────────────

module.exports = {
  name: "polaris-news",

  commands: {
    news: {
      description: "Get the latest verified news briefs",
      execute: async (args) => {
        try {
          return await handleNews(args);
        } catch (err) {
          return `Error fetching news: ${err.message}`;
        }
      },
    },

    brief: {
      description: "Generate an intelligence brief on any topic",
      execute: async (args) => {
        try {
          return await handleBrief(args);
        } catch (err) {
          return `Error generating brief: ${err.message}`;
        }
      },
    },

    search: {
      description: "Search verified news",
      execute: async (args) => {
        try {
          return await handleSearch(args);
        } catch (err) {
          return `Error searching: ${err.message}`;
        }
      },
    },

    trending: {
      description: "See what's trending right now",
      execute: async () => {
        try {
          return await handleTrending();
        } catch (err) {
          return `Error fetching trending: ${err.message}`;
        }
      },
    },
  },
};
