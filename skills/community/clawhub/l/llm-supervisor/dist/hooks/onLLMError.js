"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.onLLMError = onLLMError;
const state_1 = require("../state");
async function onLLMError(ctx, event) {
    const cfg = ctx.config;
    const state = (0, state_1.getState)(ctx);
    // Only react if we're currently on cloud
    if (state.mode !== "cloud")
        return;
    // Detect rate limit / quota style errors
    const msg = (event.error?.message || "").toLowerCase();
    const isRateLimit = msg.includes("rate limit") ||
        msg.includes("quota") ||
        msg.includes("429");
    if (!isRateLimit)
        return;
    ctx.log.warn("[llm-supervisor] Cloud LLM rate limit detected");
    // Switch to local
    (0, state_1.setState)(ctx, {
        mode: "local",
        since: Date.now(),
        lastError: event.error?.message
    });
    // Notify users
    await ctx.notify.all(`⚠️ Cloud LLM rate limit detected.\n` +
        `Switched main agent to **local model (${cfg.localModel})**.\n` +
        `Chat is unaffected. Code actions will require confirmation.`);
    ctx.log.info("[llm-supervisor] Switched to local LLM");
}
