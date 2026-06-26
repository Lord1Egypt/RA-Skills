"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.onAgentStart = onAgentStart;
const state_1 = require("../state");
async function onAgentStart(ctx, event) {
    const state = (0, state_1.getState)(ctx);
    if (state.mode === "cloud") {
        // Explicitly ensure cloud provider
        event.agent.setLLMProfile("anthropic:default");
        ctx.log.info("[llm-supervisor] Agent started in cloud mode");
        return;
    }
    // Local mode
    const localModel = ctx.config.localModel;
    event.agent.setLLMProfile({
        provider: "ollama",
        model: localModel,
        baseUrl: "http://127.0.0.1:11434"
    });
    ctx.log.info(`[llm-supervisor] Agent started in local mode (${localModel})`);
}
