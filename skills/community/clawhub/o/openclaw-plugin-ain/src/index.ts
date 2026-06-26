import { loadConfig } from '@felipematos/ain-cli';
import { registerAinProviders } from './providers.js';
import { registerAinTools } from './tools.js';
import { registerRoutingHook } from './routing-hook.js';
import type { OpenClawPluginDefinition, OpenClawPluginApi, AinPluginConfig } from './types.js';

const plugin: OpenClawPluginDefinition = {
  id: 'openclaw-plugin-ain',
  name: 'AIN - AI Node',
  description: 'AIN provider registry, routing, and execution for OpenClaw',
  version: '0.2.2',

  async register(api: OpenClawPluginApi) {
    const pluginConfig = api.pluginConfig as AinPluginConfig;
    const config = loadConfig();

    registerAinProviders(api, config);

    if (pluginConfig.exposeTools !== false) {
      registerAinTools(api);
    }

    if (pluginConfig.enableRouting !== false) {
      registerRoutingHook(api, pluginConfig.routingPolicy);
    }

    api.logger.info('AIN plugin registered successfully');
  },
};

export default plugin;
