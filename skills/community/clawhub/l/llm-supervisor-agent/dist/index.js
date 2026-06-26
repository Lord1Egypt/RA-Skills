"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = register;
const onLLMError_1 = require("./hooks/onLLMError");
const onAgentStart_1 = require("./hooks/onAgentStart");
const beforeTaskExecute_1 = require("./hooks/beforeTaskExecute");
const llm_1 = require("./commands/llm");
function register(ctx) {
    // Hooks
    ctx.hooks.onLLMError(onLLMError_1.onLLMError);
    ctx.hooks.onAgentStart(onAgentStart_1.onAgentStart);
    ctx.hooks.beforeTaskExecute(beforeTaskExecute_1.beforeTaskExecute);
    // Commands
    ctx.commands.register("llm", llm_1.llmCommand);
    ctx.log.info("[llm-supervisor] Skill loaded");
}
