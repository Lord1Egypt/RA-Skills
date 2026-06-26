import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
import type { PluginRuntime } from "./runtime-api.js";

const { setRuntime: setZulipRuntime, getRuntime: getZulipRuntime } =
  createPluginRuntimeStore<PluginRuntime>("Zulip runtime not initialized");
export { getZulipRuntime, setZulipRuntime };
export function clearZulipRuntime() {
  setZulipRuntime(undefined as unknown as PluginRuntime);
}
