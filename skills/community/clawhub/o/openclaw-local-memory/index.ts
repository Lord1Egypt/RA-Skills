import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { LocalMemoryStore } from "./lib/store.js";
import { buildCaptureHandler, buildRecallHandler } from "./lib/hooks.js";
import { 
  registerSearchTool, 
  registerStoreTool, 
  registerForgetTool, 
  registerWipeTool, 
  registerListTool,
  registerProfileTool,
  registerStatsTool,
  registerRecentTool,
} from "./lib/tools.js";

// ─── Config Schema ───────────────────────────────────────────────────────────

const ConfigSchema = {
  type: "object",
  additionalProperties: false,
  properties: {
    containerTag: { type: "string", default: "openclaw_local_memory" },
    autoRecall: { type: "boolean", default: true },
    autoCapture: { type: "boolean", default: true },
    maxRecallResults: { type: "number", default: 5 }, // REDUCED from 10
    similarityThreshold: { type: "number", default: 0.35 }, // SLIGHTLY HIGHER
    debug: { type: "boolean", default: false },
    
    // Smart capture - CONSERVATIVE to save context
    captureInterval: { type: "number", default: 8 }, // INCREASED (less frequent)
    summariseThreshold: { type: "number", default: 60000 }, // REDUCED (more frequent consolidation)
    captureSignificantOnly: { type: "boolean", default: true },
    pruneAfterCapture: { type: "boolean", default: true },
    minSignificanceScore: { type: "number", default: 0.5 }, // INCREASED (stricter)
    
    // Profile settings - CONSERVATIVE  
    profileFrequency: { type: "number", default: 15 }, // INCREASED (less frequent)
    includeProfileOnFirstTurn: { type: "boolean", default: true },
    
    // Memory management
    maxMemories: { type: "number", default: 500 },
    pruneOlderThanDays: { type: "number", default: 30 },
    decayRate: { type: "number", default: 0.05 },
    chunkThreshold: { type: "number", default: 2000 },
    chunkSize: { type: "number", default: 800 }, // REDUCED (smaller chunks)
    maxChunks: { type: "number", default: 3 }, // REDUCED
    
    // Context limiting
    maxMemoryInjections: { type: "number", default: 3 }, // MAX 3 per recall
    contextBudget: { type: "number", default: 2000 }, // MAX 2000 chars
    
    // Scoring weights
    importanceWeight: { type: "number", default: 0.25 }, // SLIGHTLY LOWER
    recencyWeight: { type: "number", default: 0.25 }, // SLIGHTLY LOWER
    relevanceWeight: { type: "number", default: 0.5 }, // HIGHER (relevance matters more)
  },
};

type LocalMemoryConfig = {
  containerTag?: string;
  autoRecall?: boolean;
  autoCapture?: boolean;
  maxRecallResults?: number;
  similarityThreshold?: number;
  debug?: boolean;
  captureInterval?: number;
  summariseThreshold?: number;
  captureSignificantOnly?: boolean;
  pruneAfterCapture?: boolean;
  minSignificanceScore?: number;
  profileFrequency?: number;
  includeProfileOnFirstTurn?: boolean;
  maxMemories?: number;
  pruneOlderThanDays?: number;
  decayRate?: number;
  chunkThreshold?: number;
  chunkSize?: number;
  maxChunks?: number;
  maxMemoryInjections?: number;
  contextBudget?: number;
  importanceWeight?: number;
  recencyWeight?: number;
  relevanceWeight?: number;
};

// ─── Plugin ──────────────────────────────────────────────────────────────────

export default definePluginEntry({
  id: "openclaw-local-memory",
  name: "Local Memory",
  description: "Brain-like local memory for OpenClaw — stores, searches, and injects memories with importance scoring, entity extraction, and automatic consolidation.",
  kind: "memory",
  configSchema: ConfigSchema,

  register(api) {
    const raw = api.pluginConfig;
    const cfg: LocalMemoryConfig = raw && typeof raw === "object" && !Array.isArray(raw)
      ? (raw as Record<string, unknown>)
      : {};

    const log = (level: "info" | "warn" | "debug", msg: string, data?: Record<string, unknown>) => {
      if (cfg.debug || level !== "debug") {
        api.logger[level === "info" ? "info" : level === "warn" ? "warn" : "info"](
          `[local-memory] ${msg}`,
          data ?? {}
        );
      }
    };

    // ── Init store ──────────────────────────────────────────────────────────
    const store = new LocalMemoryStore({
      containerTag: cfg.containerTag ?? "openclaw_local_memory",
      debug: cfg.debug ?? false,
      maxMemories: cfg.maxMemories ?? 500,
      pruneOlderThanDays: cfg.pruneOlderThanDays ?? 30,
      decayRate: cfg.decayRate ?? 0.05,
      chunkThreshold: cfg.chunkThreshold ?? 2000,
      chunkSize: cfg.chunkSize ?? 1000,
      maxChunks: cfg.maxChunks ?? 5,
      importanceWeight: cfg.importanceWeight ?? 0.3,
      recencyWeight: cfg.recencyWeight ?? 0.3,
      relevanceWeight: cfg.relevanceWeight ?? 0.4,
    });

    log("info", "initialized", {
      container: store.containerTag,
      backend: "tfidf-v2",
      features: [
        "significance_detection",
        "entity_extraction", 
        "importance_scoring",
        "time_decay",
        "semantic_chunking",
        "profile_building",
        "context_pruning",
      ],
    });

    // ── Register Tools ────────────────────────────────────────────────────────
    registerSearchTool(api, store, cfg, log);
    registerStoreTool(api, store, cfg, log);
    registerForgetTool(api, store, cfg, log);
    registerWipeTool(api, store, log);
    registerListTool(api, store, cfg, log);
    registerProfileTool(api, store, log);
    registerStatsTool(api, store, log);
    registerRecentTool(api, store, log);

    // ── Memory Prompt Section ─────────────────────────────────────────────────
    api.registerMemoryPromptSection(({ agentId, sessionKey }) => {
      return ""; // Filled by recall handler
    });

    // ── Hooks ────────────────────────────────────────────────────────────────
    const captureHandler = buildCaptureHandler(store, cfg, log);
    const recallHandler = cfg.autoRecall ? buildRecallHandler(store, cfg, log) : null;

    api.on("before_agent_start", (event: Record<string, unknown>, ctx: Record<string, unknown>) => {
      const sessionKey = ctx.sessionKey as string | undefined;
      
      if (sessionKey) {
        const userPrompt = extractUserPrompt(event);
        if (userPrompt) {
          captureHandler.registerUserMessage(userPrompt, sessionKey, 0);
        }
      }
      
      if (recallHandler) {
        return recallHandler(event, ctx);
      }
    });

    if (cfg.autoCapture) {
      api.on("agent_end", (event: Record<string, unknown>, ctx: Record<string, unknown>) => {
        const sessionKey = ctx.sessionKey as string | undefined;
        return captureHandler.handle(event, ctx, sessionKey);
      });
    }

    // ── Service ─────────────────────────────────────────────────────────────
    api.registerService({
      id: "openclaw-local-memory",
      start: () => {
        log("info", "🧠 Local Memory started");
        log("info", `   Container: ${cfg.containerTag ?? "openclaw_local_memory"}`);
        log("info", `   Auto-capture: ${cfg.autoCapture ?? true}`);
        log("info", `   Auto-recall: ${cfg.autoRecall ?? true}`);
      },
      stop: () => { 
        log("info", "service stopped");
      },
    });
  },
});

// ─── Helpers ─────────────────────────────────────────────────────────────────

function extractUserPrompt(event: Record<string, unknown>): string {
  if (typeof event.prompt === "string") return event.prompt;
  if (Array.isArray(event.messages)) {
    for (const msg of event.messages as Record<string, unknown>[]) {
      if (msg.role === "user") {
        const content = msg.content;
        if (typeof content === "string") return content;
        if (Array.isArray(content)) {
          return content
            .map((c) => (typeof c === "string" ? c : (c as Record<string, unknown>).text ?? ""))
            .join(" ");
        }
      }
    }
  }
  return "";
}
