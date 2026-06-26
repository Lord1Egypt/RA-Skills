// Keep the bundled runtime entry narrow so generic runtime activation does not
// import the broad Zulip API barrel just to install runtime state.
export { setZulipRuntime } from "./src/runtime.js";
