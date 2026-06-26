"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getState = getState;
exports.setState = setState;
exports.isCooldownOver = isCooldownOver;
const DEFAULT_STATE = {
    mode: "cloud",
    since: Date.now()
};
function getState(ctx) {
    return ctx.state.get("llm-supervisor:state") ?? DEFAULT_STATE;
}
function setState(ctx, state) {
    ctx.state.set("llm-supervisor:state", state);
}
function isCooldownOver(state, cooldownMinutes) {
    const elapsedMs = Date.now() - state.since;
    return elapsedMs > cooldownMinutes * 60 * 1000;
}
