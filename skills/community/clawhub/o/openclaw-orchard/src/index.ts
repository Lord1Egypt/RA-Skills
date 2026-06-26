import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import type { PluginApi } from "openclaw/plugin-sdk/plugin-entry";
import type Database from "better-sqlite3";
import { openDb, initSchema, resolveDbPath, seedSettings } from "./db/schema.js";
import { getConfig, getQueueInterval, isLogOnlyMode, mergeSettingsConfig } from "./config.js";
import { registerProjectTools } from "./tools/project-tools.js";
import { registerTaskTools } from "./tools/task-tools.js";
import { registerKbTools } from "./tools/kb-tools.js";
import { registerConfigSafetyTools } from "./tools/config-safety-tools.js";
import { registerRoutes, startStandaloneUiServer } from "./api/routes.js";
import { runQueueTick, setWakeCallback, seedRunningTasksFromDb } from "./queue/runner.js";
import { scheduleArchitect } from "./roles/architect.js";
import { scheduleReporter } from "./roles/reporter.js";
import type { OrchardConfig } from "./config.js";
import http from "http";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Singleton guard — prevent double-initialization
let initialized = false;
let db: Database.Database | null = null;

function getDb(): Database.Database {
  if (!db) throw new Error("OrchardOS database not initialized");
  return db;
}

export default definePluginEntry({
  id: "orchard",
  name: "OrchardOS",
  description: "Agentic project management for OpenClaw",
  register(api: PluginApi) {
    if (initialized) return;
    initialized = true;

    const cfg = getConfig((api.pluginConfig ?? {}) as Record<string, unknown>);
    const dbPath = resolveDbPath(cfg.dbPath);
    const uiServerEnabled = cfg.uiServer?.enabled !== false;
    const uiServerPort = cfg.uiServer?.port ?? 18790;
    const uiServerBindAddress = cfg.uiServer?.bindAddress ?? "127.0.0.1";
    const uiServerAllowUnsafeBind = cfg.uiServer?.allowUnsafeBind === true;
    api.logger.info(`[orchard] initializing, db: ${dbPath}`);
    if (cfg.debug?.enabled) {
      api.logger.warn(`[orchard] debug mode enabled (env overrides supported)`);
    }

    if (cfg.contextInjection?.enabled && !cfg.contextInjection.apiKey && !process.env.GEMINI_API_KEY) {
      api.logger.warn("[orchard] contextInjection is enabled but no apiKey is configured and GEMINI_API_KEY is not set; embeddings will be disabled");
    }

    db = openDb(dbPath);
    initSchema(db);
    seedSettings(db, cfg);

    // Register tools
    registerProjectTools(api, getDb);
    registerTaskTools(api, getDb, () => cfg);
    registerKbTools(api, getDb, () => cfg);
    registerConfigSafetyTools(api, getDb);

    // Register HTTP routes
    registerRoutes(api, getDb, () => cfg);

    let queueHandle: ReturnType<typeof setInterval> | null = null;
    let architectHandle: ReturnType<typeof setInterval> | null = null;
    let reporterHandle: ReturnType<typeof setInterval> | null = null;
    let uiServerHandle: http.Server | null = null;

    // Register queue runner service
    api.registerService({
      id: "orchard-queue-runner",
      async start() {
        const interval = getQueueInterval(cfg);
        api.logger.info(`[orchard] queue runner starting, interval: ${interval}ms`);

        const tick = async () => {
          try {
            // Merge DB settings over static config on every tick so runtime
            // changes (via UI settings) take effect without a gateway restart.
            const liveCfg = mergeSettingsConfig(cfg, getDb());
            await runQueueTick(getDb(), liveCfg, api.runtime, api.logger);
          } catch (tickErr: any) {
            api.logger.error(`[orchard] queue tick error: ${tickErr?.message}`);
          }
        };

        // Expose wake callback for routes + tools
        setWakeCallback(tick);

        // Start standalone UI server. It does not store or inject a server-side
        // gateway token; browsers supply their own bearer token to the local UI.
        const uiHtmlPath = path.resolve(__dirname, "../src/ui/dashboard.html");
        if (uiServerEnabled) {
          uiServerHandle = startStandaloneUiServer(uiHtmlPath, "http://127.0.0.1:18789", uiServerPort, uiServerBindAddress, uiServerAllowUnsafeBind, api.logger);
        }

        // Reconcile any sessions left running from a previous process
        await seedRunningTasksFromDb(getDb(), api.runtime, cfg, api.logger);

        // Initial tick on start
        await tick();

        queueHandle = setInterval(() => {
          void tick();
        }, interval);

        if (isLogOnlyMode(cfg)) {
          api.logger.warn(`[orchard] log-only mode active; periodic architect and reporter schedulers are disabled`);
        } else {
          // Schedule architect periodic wake
          architectHandle = scheduleArchitect(getDb, cfg, api.runtime, api.logger);

          // Schedule reporter
          reporterHandle = scheduleReporter(getDb, cfg, api.logger);
        }
      },
      async stop() {
        if (queueHandle !== null) { clearInterval(queueHandle); queueHandle = null; }
        if (architectHandle !== null) { clearInterval(architectHandle); architectHandle = null; }
        if (reporterHandle !== null) { clearInterval(reporterHandle); reporterHandle = null; }
        if (uiServerHandle !== null) {
          await new Promise((resolve) => uiServerHandle!.close(() => resolve(undefined)));
          uiServerHandle = null;
        }
        api.logger.info(`[orchard] queue runner stopped`);
      },
    });

    api.logger.info(`[orchard] registered tools, routes, and queue runner`);
  },
});
