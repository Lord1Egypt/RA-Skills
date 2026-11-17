import { getActiveMemorySearchManager } from "openclaw/plugin-sdk/memory-host-search";
import { registerCacheRecall, PLUGIN_ID } from "./adapter.mjs";

export default {
  id: PLUGIN_ID,
  name: "Hui-Yi Native Memory Guard",
  register(api) { registerCacheRecall(api, { getManager: getActiveMemorySearchManager }); },
};
