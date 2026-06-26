import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import os from "node:os";
const execFileAsync = promisify(execFile);
const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPT = join(__dirname, "tracker_core.py");
const STATE_FILE = process.env.PACKAGE_TRACKER_STATE_FILE ||
    join(os.homedir(), ".openclaw", "workspace", "package-tracker-state.json");
const WEBHOOK_BASE_PATH = "/webhooks/package-tracker"; // token will be embedded in path
function webhookPath(config) {
    const token = (config.webhook?.token || "").trim();
    // Avoid query strings: some HTTP route runtimes do not expose the query reliably.
    // Use a path segment instead.
    return token ? `${WEBHOOK_BASE_PATH}/${encodeURIComponent(token)}` : WEBHOOK_BASE_PATH;
}
// ── Helper: call Python core ──────────────────────────────────────────────────
async function callCore(config, command, args) {
    const cal = config.calendar ?? {};
    const sched = config.schedule ?? {};
    const k100 = config.kuaidi100;
    const webhook = config.webhook ?? {};
    const env = {
        ...process.env,
        KUAIDI100_CUSTOMER: k100.customer,
        KUAIDI100_KEY: k100.key,
        KUAIDI100_SUB_ENDPOINT: "https://poll.kuaidi100.com/poll",
        KUAIDI100_SALT: (webhook.salt || webhook.token || "").trim(),
        KUAIDI100_SIGNATURE_MODE: (webhook.signatureMode || "soft").trim(),
        GCAL_CLIENT_ID: cal.client_id ?? "",
        GCAL_CLIENT_SECRET: cal.client_secret ?? "",
        GCAL_REFRESH_TOKEN: cal.refresh_token ?? "",
        GCAL_CALENDAR_ID: cal.calendar_id ?? "primary",
        OFF_WORK_TIME: sched.off_work_time ?? "18:30",
        REMINDER_MINUTES_BEFORE: String(sched.reminder_minutes_before ?? 30),
        TIMEZONE_NAME: sched.timezone ?? "Asia/Shanghai",
        TRACKER_STATE_FILE: STATE_FILE,
    };
    const { stdout } = await execFileAsync("python3", [SCRIPT, command, JSON.stringify(args)], {
        env, timeout: 30_000,
    });
    try {
        return JSON.parse(stdout);
    }
    catch {
        return { raw: stdout };
    }
}
function formatResult(result) {
    return JSON.stringify(result, null, 2);
}
// ── Read body from IncomingMessage ────────────────────────────────────────────
function readBody(req) {
    return new Promise((resolve, reject) => {
        let data = "";
        req.on("data", (chunk) => { data += chunk.toString(); });
        req.on("end", () => resolve(data));
        req.on("error", reject);
    });
}
function respondKuaidi100Ok(res, message = "成功") {
    // Kuaidi100 expects a JSON response body to mark callback as successful.
    // See doc snippet: {"result":true,"returnCode":"200","message":"成功"}
    res.statusCode = 200;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ result: true, returnCode: "200", message }));
}
const rateBuckets = new Map();
function rateLimitOk(ip, limitPerMinute) {
    if (!limitPerMinute || limitPerMinute <= 0)
        return true;
    const now = Date.now();
    const windowMs = 60_000;
    const key = ip || "unknown";
    const b = rateBuckets.get(key);
    if (!b || now - b.windowStartMs >= windowMs) {
        rateBuckets.set(key, { windowStartMs: now, count: 1 });
        return true;
    }
    b.count += 1;
    return b.count <= limitPerMinute;
}
// ── Plugin entry ──────────────────────────────────────────────────────────────
export default definePluginEntry({
    id: "package-tracker",
    name: "Package Tracker",
    description: "Track Chinese domestic packages via Kuaidi100 push API and auto-add delivery reminders to Google Calendar.",
    register(api) {
        const cfg = () => {
            // Prefer plugin-scoped config from `plugins.entries.<id>.config`.
            // NOTE: `api.config` is the full OpenClaw config; we need `api.pluginConfig` here.
            const c = api.pluginConfig;
            if (c)
                return c;
            // Fallback: env (useful for local dev)
            return {
                kuaidi100: {
                    customer: process.env.KUAIDI100_CUSTOMER ?? "",
                    key: process.env.KUAIDI100_KEY ?? "",
                },
                calendar: {
                    client_id: process.env.GCAL_CLIENT_ID,
                    client_secret: process.env.GCAL_CLIENT_SECRET,
                    refresh_token: process.env.GCAL_REFRESH_TOKEN,
                    calendar_id: process.env.GCAL_CALENDAR_ID ?? "primary",
                },
                schedule: {
                    off_work_time: process.env.OFF_WORK_TIME ?? "18:30",
                    reminder_minutes_before: Number(process.env.REMINDER_MINUTES_BEFORE ?? "30"),
                },
                webhook: {
                    baseUrl: process.env.PACKAGE_TRACKER_WEBHOOK_BASE_URL ?? "",
                    token: process.env.PACKAGE_TRACKER_WEBHOOK_TOKEN ?? "",
                },
            };
        };
        // ── Webhook HTTP route ─────────────────────────────────────────────────
        // Kuaidi100 POSTs status updates here whenever the package moves.
        api.registerHttpRoute({
            path: webhookPath(cfg()),
            auth: "plugin",
            match: "exact",
            replaceExisting: true,
            handler: async (req, res) => {
                // Only handle POST
                if ((req.method || "GET").toUpperCase() !== "POST") {
                    res.statusCode = 404;
                    res.end("Not Found");
                    return true;
                }
                // Local rate limit (best-effort). Avoids log spam / CPU burn if tunnel URL leaks.
                // For Cloudflare Tunnel, remoteAddress is often 127.0.0.1, so this is mainly a coarse limiter.
                const ip = req.socket?.remoteAddress || "";
                const limit = cfg().webhook?.rateLimitPerMinute ?? 60;
                if (!rateLimitOk(ip, limit)) {
                    // Even on rate limit, respond in Kuaidi100-expected JSON format.
                    // This reduces retries and keeps their dashboard from marking as failed.
                    respondKuaidi100Ok(res, "rate limited");
                    return true;
                }
                try {
                    const body = await readBody(req);
                    const result = await callCore(cfg(), "handle_push", { push_body: body });
                    respondKuaidi100Ok(res, "成功");
                    if (result?.today_delivery) {
                        console.log(`[package-tracker] 📦 Today delivery detected: ${result.number} — calendar synced`);
                    }
                    return true;
                }
                catch {
                    // Still respond ok so kuaidi100 won't hammer retries
                    respondKuaidi100Ok(res, "ok");
                    return true;
                }
            },
        });
        // ── Tool: add_tracking_number ──────────────────────────────────────────
        api.registerTool({
            name: "add_tracking_number",
            description: "Subscribe to push tracking updates for a package number via Kuaidi100. " +
                "Costs 1 API quota. Kuaidi100 will push the initial status plus all future " +
                "updates automatically. Use when user says: 给我加个快递单号, 帮我追踪这个包裹, " +
                "快递单号是 XXX. Accepts optional carrier code (com) and a note (e.g. item name).",
            parameters: Type.Object({
                number: Type.String({ description: "Tracking number" }),
                com: Type.Optional(Type.String({
                    description: "Carrier code e.g. shunfeng/zhongtong/auto (default: auto — Kuaidi100 auto-detects)"
                })),
                note: Type.Optional(Type.String({ description: "Optional note, e.g. 黑色毛衣" })),
            }),
            async execute(_id, params) {
                const baseUrl = (cfg().webhook?.baseUrl || "").replace(/\/$/, "");
                const callbackUrl = baseUrl ? `${baseUrl}${webhookPath(cfg())}` : "";
                const result = await callCore(cfg(), "add_tracking", {
                    number: params.number,
                    com: params.com ?? "auto",
                    note: params.note ?? "",
                    webhook_url: callbackUrl,
                });
                return { content: [{ type: "text", text: formatResult(result) }] };
            },
        });
        // ── Tool: list_packages ────────────────────────────────────────────────
        api.registerTool({
            name: "list_packages",
            description: "List all tracked packages with latest status from local cache (no API quota used). " +
                "Status is updated automatically when Kuaidi100 pushes new tracking events. " +
                "Use when user asks: 我有哪些快递, 今天有快递吗, 显示全部包裹, 快递状态.",
            parameters: Type.Object({}),
            async execute(_id, _params) {
                const result = await callCore(cfg(), "list_packages", {});
                return { content: [{ type: "text", text: formatResult(result) }] };
            },
        });
        // ── Tool: sync_to_calendar ─────────────────────────────────────────────
        api.registerTool({
            name: "sync_to_calendar",
            description: "Manually trigger Google Calendar sync for today's expected deliveries. " +
                "This runs automatically on each Kuaidi100 push, but can be called manually too. " +
                "Idempotent — safe to call multiple times. " +
                "Use when user says: 帮我加到日历, 提醒我下班取快递, 加个提醒.",
            parameters: Type.Object({}),
            async execute(_id, _params) {
                const result = await callCore(cfg(), "sync_calendar", {});
                return { content: [{ type: "text", text: formatResult(result) }] };
            },
        });
        // ── Tool: remove_tracking_number ───────────────────────────────────────
        api.registerTool({
            name: "remove_tracking_number",
            description: "Remove a tracking number from the watch list. " +
                "Use when user says: 删除这个快递, 取消追踪 XXX.",
            parameters: Type.Object({
                number: Type.String({ description: "Tracking number to remove" }),
            }),
            async execute(_id, params) {
                const result = await callCore(cfg(), "remove_tracking", { number: params.number });
                return { content: [{ type: "text", text: formatResult(result) }] };
            },
        });
    },
});
