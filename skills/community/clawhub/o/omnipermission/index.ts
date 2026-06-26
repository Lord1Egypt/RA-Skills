import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { emptyPluginConfigSchema } from "openclaw/plugin-sdk";
import { registerOmniCli } from "./src/cli.ts";
import { registerOmniHooks } from "./src/hooks.ts";

const omniPermissionPlugin = {
  id: "omnipermission",
  name: "OmniPermission Plugin",
  configSchema: emptyPluginConfigSchema(),

  register(api: OpenClawPluginApi) {
    api.logger.info("[omnipermission] 🛰️ Plugin Loaded.");

    // Initialize modular components
    registerOmniCli(api);
    registerOmniHooks(api);
  },
};

export default omniPermissionPlugin;
