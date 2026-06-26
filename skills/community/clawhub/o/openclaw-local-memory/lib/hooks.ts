/**
 * Advanced Brain-Like Memory Hooks
 * 
 * Features:
 * - Significance detection (what's worth remembering)
 * - Entity extraction
 * - Periodic summarization
 * - Profile building
 * - Smart context pruning
 * - Multi-tier memory (exchange → summary → profile)
 */

import type { LocalMemoryStore } from "./store.js";

interface LocalMemoryConfig {
  autoRecall?: boolean;
  autoCapture?: boolean;
  maxRecallResults?: number;
  similarityThreshold?: number;
  debug?: boolean;
  
  // Smart capture - be MORE AGGRESSIVE to save context
  captureInterval?: number;           // Capture every N turns (default: 8, higher = less capture)
  summariseThreshold?: number;        // Token threshold to trigger summary (default: 60000, LOWER = more often)
  captureSignificantOnly?: boolean;  // Only capture significant content (default: true)
  pruneAfterCapture?: boolean;        // Clear captured context from session (default: true)
  minSignificanceScore?: number;      // Min score to be worth capturing (default: 0.5, HIGHER = stricter)
  
  // Profile settings
  profileFrequency?: number;         // Inject profile every N turns (default: 15, higher = less often)
  includeProfileOnFirstTurn?: boolean;
  
  // Context management - BE AGGRESSIVE
  maxContextAge?: number;             // Max context age in ms before forcing prune
  memoryRefreshThreshold?: number;    // Refresh memory injection after N turns
  maxMemoryInjections?: number;      // Max memories to inject per recall (default: 5)
  contextBudget?: number;            // Max chars of memory context to inject (default: 2000)
}

type LogFn = (level: "info" | "warn" | "debug", msg: string, data?: Record<string, unknown>) => void;

// ─── Significance Detection ───────────────────────────────────────────────────

interface SignificanceResult {
  score: number;           // 0-1
  reasons: string[];        // Why it's significant
  category?: string;       // Detected category
  shouldCapture: boolean;
}

const SIGNIFICANCE_PATTERNS = [
  // Decisions and commitments
  { pattern: /\b(entschieden|beschlossen|geplant|wird|werden|machen|setup|konfiguriert|installiert|aktiviert|configured|decided|will use|going with|chose|selected)\b/i, weight: 0.3, reason: "decision" },
  
  // User identity and facts
  { pattern: /\b(ich bin|mein|unser|unser Unternehmen|Name|Email|Konto|team|firma|unternehmen|company|I am|my name|we are)\b/i, weight: 0.25, reason: "identity" },
  
  // Preferences
  { pattern: /\b(bevorzug|präferiert|immer|nie|niemals|nur|like|love|hate|prefer|want|need|never|always)\b/i, weight: 0.25, reason: "preference" },
  
  // Credentials and security
  { pattern: /\b(api[_-]?key|password|secret|token|credential|auth|login|zugang)\b/i, weight: 0.2, reason: "credential" },
  
  // Skills and capabilities
  { pattern: /\b(können|fähig|skill|ability|experienced|proficient|know how|can do|capable)\b/i, weight: 0.2, reason: "skill" },
  
  // Projects and ongoing work
  { pattern: /\b(projekt|project|build|deploy|setup|implement|develop|create|machen)\b/i, weight: 0.15, reason: "project" },
  
  // Errors and problems (worth remembering for context)
  { pattern: /\b(error|bug|issue|problem|fehler|kaputt|nicht|broken|failed|nicht funktioniert)\b/i, weight: 0.1, reason: "problem" },
  
  // Important events
  { pattern: /\b(heute|gestern|morgen|letzte woche|diese woche|gerade eben|soeben)\b/i, weight: 0.1, reason: "temporal" },
  
  // Goals and targets
  { pattern: /\b(ziel|goal|target|milestone|deadline|erfolg|success|fertig|complete)\b/i, weight: 0.15, reason: "goal" },
  
  // Money/business
  { pattern: /\b(geld|cost|price|preis|budget|euro|€|revenue|umsatz|deal|pipeline)\b/i, weight: 0.15, reason: "business" },
];

function assessSignificance(content: string): SignificanceResult {
  const reasons: string[] = [];
  let totalWeight = 0;
  let matchedPatterns = 0;
  
  const lower = content.toLowerCase();
  
  for (const { pattern, weight, reason } of SIGNIFICANCE_PATTERNS) {
    if (pattern.test(lower)) {
      matchedPatterns++;
      totalWeight += weight;
      if (!reasons.includes(reason)) {
        reasons.push(reason);
      }
    }
  }
  
  // Length bonus (medium length is best - too short = not enough context, too long = probably rambling)
  const len = content.length;
  let lengthBonus = 0;
  if (len >= 50 && len < 500) lengthBonus = 0.1;
  else if (len >= 500 && len < 2000) lengthBonus = 0.15;
  else if (len >= 2000 && len < 5000) lengthBonus = 0.1;
  else if (len >= 5000) lengthBonus = 0;
  else if (len < 30) lengthBonus = -0.2;
  
  // Question penalty (questions are less worth capturing)
  if (/^\s*(\?|warum|wie|was|wo\b)/i.test(lower.trim())) {
    lengthBonus -= 0.1;
  }
  
  // URL/file path bonus (technical content is valuable)
  if (/\.(com|de|net|org|io|ts|js|md|json|py|sh)\b/.test(content)) {
    lengthBonus += 0.1;
  }
  
  // Greeting penalty
  if (/^hi|^hey|^hallo|^moin|^servus/i.test(lower.trim())) {
    lengthBonus -= 0.3;
  }
  
  const score = Math.max(0, Math.min(1, totalWeight + lengthBonus));
  
  return {
    score,
    reasons,
    category: reasons[0] || "other",
    shouldCapture: score >= 0.4 || matchedPatterns >= 2,
  };
}

// ─── Context Window Management ────────────────────────────────────────────────

interface ContextWindow {
  turnCount: number;
  lastCaptureAt: number;
  lastProfileAt: number;
  accumulatedContent: string[];
  tokenEstimate: number;
}

const contextWindows = new Map<string, ContextWindow>();

function getOrCreateWindow(sessionKey: string): ContextWindow {
  if (!contextWindows.has(sessionKey)) {
    contextWindows.set(sessionKey, {
      turnCount: 0,
      lastCaptureAt: Date.now(),
      lastProfileAt: 0,
      accumulatedContent: [],
      tokenEstimate: 0,
    });
  }
  return contextWindows.get(sessionKey)!;
}

function shouldCaptureNow(window: ContextWindow, cfg: LocalMemoryConfig): boolean {
  const interval = cfg.captureInterval ?? 5;
  const turnsSinceCapture = window.turnCount - Math.floor(window.lastCaptureAt / 1000);
  
  // Capture every N turns
  if (interval > 0 && window.turnCount % interval === 0) {
    return true;
  }
  
  // Capture if context is getting long
  if (window.tokenEstimate > (cfg.summariseThreshold ?? 100000)) {
    return true;
  }
  
  return false;
}

// ─── Capture Handler ─────────────────────────────────────────────────────────

export function buildCaptureHandler(
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  const minSignificance = cfg.minSignificanceScore ?? 0.4;
  
  return {
    async registerUserMessage(
      userContent: string,
      sessionKey: string,
      turnIndex: number,
    ) {
      if (userContent.length < 20) return;
      if (userContent.startsWith("[") && userContent.includes("agent_end")) return;
      
      const window = getOrCreateWindow(sessionKey);
      window.turnCount++;
      
      // Accumulate for later summarization
      if (userContent.split(" ").length >= 4) {
        window.accumulatedContent.push(userContent);
      }
      
      // Check significance
      const sig = assessSignificance(userContent);
      
      log("debug", "user message registered", {
        turnCount: window.turnCount,
        sigScore: sig.score,
        sigReasons: sig.reasons,
        tokenEstimate: window.tokenEstimate,
      });
      
      // Trigger capture if significant
      if (sig.shouldCapture && sig.score >= minSignificance) {
        window.lastCaptureAt = Date.now();
      }
    },

    async handle(
      event: Record<string, unknown>,
      ctx: Record<string, unknown>,
      sessionKey?: string,
    ) {
      if (!sessionKey) return;

      try {
        const assistantContent = extractAssistantResponse(event);
        if (!assistantContent || assistantContent.length < 5) return;

        const window = getOrCreateWindow(sessionKey);
        const userContent = window.accumulatedContent.pop() ?? "";
        
        const combinedContent = `[User]: ${userContent.slice(0, 1500)}\n\n[Assistant]: ${assistantContent.slice(0, 1500)}`;
        
        // Assess significance
        const sig = assessSignificance(combinedContent);
        
        // Update token estimate
        window.tokenEstimate = estimateTokens(event);
        
        // Decide what to do
        const shouldPeriodicCapture = window.turnCount % (cfg.captureInterval ?? 5) === 0;
        const shouldSummarise = window.tokenEstimate > (cfg.summariseThreshold ?? 100000);
        const shouldPrune = cfg.pruneAfterCapture && (sig.shouldCapture || shouldPeriodicCapture);
        
        log("debug", "capture decision", {
          sigScore: sig.score,
          sigShouldCapture: sig.shouldCapture,
          periodic: shouldPeriodicCapture,
          summarise: shouldSummarise,
          prune: shouldPrune,
          tokenEstimate: window.tokenEstimate,
        });

        if (sig.shouldCapture && sig.score >= minSignificance) {
          const id = await store.add(combinedContent, {
            sessionKey,
            conversationId: sessionKey,
            turnIndex: window.turnCount,
            messageType: "exchange",
            source: "assistant",
            category: sig.category as any,
          });

          log("info", "captured significant exchange", {
            id: id.slice(0, 8),
            sigScore: sig.score,
            sigReasons: sig.reasons,
          });
        }

        if (shouldSummarise) {
          // Consolidate accumulated content
          await consolidateMemory(store, window, log);
          window.tokenEstimate = Math.floor(window.tokenEstimate * 0.3); // Reset after summary
        }
      } catch (err) {
        log("warn", "capture failed", { error: String(err) });
      }
    },
  };
}

// ─── Memory Consolidation ───────────────────────────────────────────────────

async function consolidateMemory(
  store: LocalMemoryStore,
  window: ContextWindow,
  log: LogFn,
): Promise<void> {
  if (window.accumulatedContent.length < 2) return;

  const summaryText = window.accumulatedContent
    .slice(-10) // Last 10 exchanges
    .join("\n---\n");

  const id = await store.add(summaryText, {
    conversationId: window.accumulatedContent.length > 5 ? "consolidated" : undefined,
    turnIndex: 0,
    messageType: "summary",
    source: "system",
    category: "context",
  });

  log("info", "consolidated memory", {
    id: id.slice(0, 8),
    exchanges: window.accumulatedContent.length,
  });

  window.accumulatedContent = [];
}

// ─── Recall Handler ──────────────────────────────────────────────────────────

export function buildRecallHandler(
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  const contextWindows = new Map<string, ContextWindow>();
  
  return async (event: Record<string, unknown>, ctx: Record<string, unknown>) => {
    try {
      const sessionKey = ctx.sessionKey as string | undefined;
      if (!sessionKey) return;

      const prompt = extractPrompt(event);
      if (!prompt || prompt.length < 5) return;

      // Get or create window
      let window = contextWindows.get(sessionKey);
      if (!window) {
        window = {
          turnCount: 0,
          lastCaptureAt: Date.now(),
          lastProfileAt: 0,
          accumulatedContent: [],
          tokenEstimate: estimateTokens(event),
        };
        contextWindows.set(sessionKey, window);
      }
      window.turnCount++;

      // AGGRESSIVE LIMITING: Fewer results, stricter threshold
      const limit = Math.min(cfg.maxRecallResults ?? 10, 5); // MAX 5 memories
      const threshold = (cfg.similarityThreshold ?? 0.3) + 0.1; // Stricter threshold
      const contextBudget = cfg.contextBudget ?? 2000; // Max chars to inject
      const maxInjections = cfg.maxMemoryInjections ?? 3; // Max memories to show
      
      // ─── Build context sections (STRICTLY LIMITED) ─────────────────────────────────
      const sections: string[] = [];
      
      // 1. Profile - ONLY if first turn or very rarely
      const profileFrequency = cfg.profileFrequency ?? 15;
      const includeProfile = cfg.includeProfileOnFirstTurn !== false && window.turnCount <= 1;
      
      if (includeProfile) {
        const profile = await store.buildProfile();
        // TRUNCATE profile heavily
        const profileSection = formatProfileSection(profile, 500); // Max 500 chars
        if (profileSection) {
          sections.push(profileSection);
          window.lastProfileAt = window.turnCount;
        }
      }

      // 2. Relevant memories - STRICTLY LIMITED
      const memories = await store.search(prompt, maxInjections, threshold);
      if (memories.length > 0) {
        sections.push(formatMemorySection(memories, contextBudget));
      }

      // 3. ONLY if context is very short (first 2 turns)
      if (window.turnCount <= 2) {
        const recent = await store.getRecent(2);
        if (recent.length > 0) {
          sections.push(formatRecentSection(recent, 800));
        }
      }

      if (sections.length === 0) return;

      // FINAL BUDGET CHECK: Don't exceed context budget
      let context = sections.join("\n\n");
      if (context.length > contextBudget) {
        context = context.slice(0, contextBudget) + "\n...[memory truncated to save context]";
      }

      // Inject into prependContext
      if (Array.isArray(event.prependContext)) {
        event.prependContext.push(context);
      }

      log("debug", "recalled context (slim)", {
        turnCount: window.turnCount,
        profileIncluded: includeProfile,
        memoriesFound: memories.length,
        contextLength: context.length,
        budget: contextBudget,
      });
    } catch (err) {
      log("warn", "recall failed", { error: String(err) });
    }
  };
}

// ─── Memory Pruning ─────────────────────────────────────────────────────────

/**
 * Signal that context can be pruned after significant memory capture
 */
export function shouldPruneContext(
  ctx: Record<string, unknown>,
  sessionKey: string,
): boolean {
  const window = (ctx as any).__memoryWindow as ContextWindow | undefined;
  if (!window) return false;
  
  // Prune if we just captured something significant
  const timeSinceCapture = Date.now() - window.lastCaptureAt;
  return timeSinceCapture < 60000; // Within last minute
}

// ─── Formatting Helpers ───────────────────────────────────────────────────────

function formatRelativeTime(isoTimestamp: string): string {
  try {
    const dt = new Date(isoTimestamp);
    const now = new Date();
    const seconds = (now.getTime() - dt.getTime()) / 1000;
    const minutes = seconds / 60;
    const hours = seconds / 3600;
    const days = seconds / 86400;

    if (minutes < 1) return "just now";
    if (minutes < 60) return `${Math.floor(minutes)}m ago`;
    if (hours < 24) return `${Math.floor(hours)}h ago`;
    if (days < 7) return `${Math.floor(days)}d ago`;

    const month = dt.toLocaleString("en", { month: "short" });
    if (dt.getFullYear() === now.getFullYear()) {
      return `${dt.getDate()} ${month}`;
    }
    return `${dt.getDate()} ${month}, ${dt.getFullYear()}`;
  } catch {
    return "";
  }
}

function formatAge(createdAt: string): string {
  const days = (Date.now() - new Date(createdAt).getTime()) / (24 * 60 * 60 * 1000);
  if (days < 1) return "today";
  if (days < 7) return `${Math.floor(days)}d ago`;
  if (days < 30) return `${Math.floor(days / 7)}w ago`;
  return `${Math.floor(days / 30)}mo ago`;
}

function formatProfileSection(
  profile: Awaited<ReturnType<LocalMemoryStore["buildProfile"]>>,
  charBudget: number = 800,
): string {
  const sections: string[] = [];
  
  if (profile.entities.length > 0) {
    sections.push(`## 👤 Entities\n${profile.entities.slice(0, 5).join(", ")}`);
  }
  
  if (profile.preferences.length > 0) {
    sections.push(`## ❤️ Prefs\n${profile.preferences.slice(0, 3).map(p => p.slice(0, 60)).join("; ")}`);
  }
  
  if (profile.static.length > 0) {
    sections.push(`## 📝 Facts\n${profile.static.slice(0, 3).map(f => f.slice(0, 80)).join(" | ")}`);
  }
  
  if (profile.dynamic.length > 0) {
    sections.push(`## 🔄 Recent\n${profile.dynamic.slice(0, 2).map(d => d.slice(0, 60)).join(" | ")}`);
  }
  
  if (sections.length === 0) return "";
  
  // Respect budget
  let result = `<memory-profile>\n${sections.join("\n\n")}\n</memory-profile>`;
  if (result.length > charBudget) {
    result = result.slice(0, charBudget) + "...";
  }
  return result;
}

function formatMemorySection(
  memories: Awaited<ReturnType<LocalMemoryStore["search"]>>,
  contextBudget: number = 2000,
): string {
  if (memories.length === 0) return "";
  
  // STRICT LIMITING: Cap at 3 most important memories to save context
  const limited = memories.slice(0, 3);
  
  const lines = limited.map((r) => {
    const cat = r.metadata?.category ?? "other";
    const age = formatAge(r.metadata?.createdAt ?? "");
    const score = Math.round(r.score * 100);
    // TRUNCATE HEAVILY to save context - max 150 chars per memory
    let content = r.content;
    if (content.length > 150) {
      content = content.slice(0, 150) + "...";
    }
    return `[${cat}·${score}%·${age}] ${content}`;
  });

  const joined = lines.join("\n");
  // Respect budget
  const truncated = joined.length > contextBudget ? joined.slice(0, contextBudget) + "..." : joined;

  return `<memory-recall>\n## 🧠 Memories (${limited.length}/${memories.length})\n${truncated}\n</memory-recall>`;
}

function formatRecentSection(
  memories: Awaited<ReturnType<LocalMemoryStore["getRecent"]>>,
  contextBudget: number = 1500,
): string {
  if (memories.length === 0) return "";
  
  // STRICT: Only 2 recent memories max
  const limited = memories.slice(0, 2);
  
  const lines = limited.map((m) => {
    const cat = m.metadata.category;
    const age = formatAge(m.metadata.createdAt);
    // TRUNCATE to 120 chars
    let content = m.content;
    if (content.length > 120) {
      content = content.slice(0, 120) + "...";
    }
    return `[${cat}·${age}] ${content}`;
  });

  const joined = lines.join("\n");
  const truncated = joined.length > contextBudget ? joined.slice(0, contextBudget) + "..." : joined;

  return `<memory-recent>\n## 🕐 Recent (${limited.length})\n${truncated}\n</memory-recent>`;
}

// ─── Token Estimation ────────────────────────────────────────────────────────

function estimateTokens(event: Record<string, unknown>): number {
  let total = 0;
  
  if (typeof event.prompt === "string") {
    total += event.prompt.length;
  }
  
  if (Array.isArray(event.messages)) {
    for (const msg of event.messages as Record<string, unknown>[]) {
      const content = msg.content;
      if (typeof content === "string") {
        total += content.length;
      } else if (Array.isArray(content)) {
        for (const c of content) {
          if (typeof c === "string") total += c.length;
          else if (typeof c === "object" && c !== null) total += (c as Record<string, unknown>).text?.length ?? 0;
        }
      }
    }
  }
  
  return Math.floor(total / 4); // Rough German/English average
}

// ─── Message Extraction ──────────────────────────────────────────────────────

function extractMessages(event: Record<string, unknown>): (string | Record<string, unknown>)[] {
  if (Array.isArray(event.messages)) {
    return event.messages as (string | Record<string, unknown>)[];
  }
  if (Array.isArray(event.content)) {
    return event.content as (string | Record<string, unknown>)[];
  }
  return [];
}

function extractPrompt(event: Record<string, unknown>): string {
  if (typeof event.prompt === "string") return event.prompt;
  if (typeof event.messages === "string") return event.messages;

  if (Array.isArray(event.messages)) {
    for (const msg of event.messages as Record<string, unknown>[]) {
      if (msg.role === "user") {
        const content = msg.content;
        if (typeof content === "string") return content;
        if (Array.isArray(content)) {
          return content.map((c) => (typeof c === "string" ? c : (c as Record<string, unknown>).text ?? "")).join(" ");
        }
      }
    }
  }
  return "";
}

function extractAssistantResponse(event: Record<string, unknown>): string {
  const messages = extractMessages(event);
  
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i];
    if (typeof msg === "object" && msg !== null && (msg as Record<string, unknown>).role === "assistant") {
      const content = (msg as Record<string, unknown>).content;
      if (typeof content === "string") return content;
      if (Array.isArray(content)) {
        return content.map((c) => (typeof c === "string" ? c : (c as Record<string, unknown>).text ?? "")).join(" ");
      }
    }
  }
  return "";
}
