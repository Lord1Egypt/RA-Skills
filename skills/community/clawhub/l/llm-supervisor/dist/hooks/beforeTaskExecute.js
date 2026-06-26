"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.beforeTaskExecute = beforeTaskExecute;
const state_1 = require("../state");
const CODE_INTENTS = [
    "create_file",
    "edit_file",
    "write_code",
    "refactor",
    "generate_code",
    "scaffold",
    "modify_repository",
    "apply_patch"
];
async function beforeTaskExecute(ctx, event) {
    const state = (0, state_1.getState)(ctx);
    // Only guard when in local mode
    if (state.mode !== "local")
        return;
    // Only guard code-related tasks
    const intent = event.task?.intent;
    if (!intent || !CODE_INTENTS.includes(intent))
        return;
    const confirmationPhrase = ctx.config.confirmationPhrase;
    // Check if user has explicitly confirmed
    const lastUserMessage = event.context?.lastUserMessage || "";
    const confirmed = lastUserMessage
        .toUpperCase()
        .includes(confirmationPhrase);
    if (confirmed) {
        ctx.log.info("[llm-supervisor] Local code execution confirmed by user");
        return;
    }
    // Block execution
    event.block(`⚠️ You are currently running on a **local LLM** due to cloud rate limits.\n` +
        `This may affect code quality.\n\n` +
        `If you want to proceed anyway, reply:\n` +
        `**${confirmationPhrase}**`);
    ctx.log.warn("[llm-supervisor] Blocked code task awaiting confirmation");
}
