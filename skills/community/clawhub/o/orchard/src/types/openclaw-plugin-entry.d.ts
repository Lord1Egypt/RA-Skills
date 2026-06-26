declare module "openclaw/plugin-sdk/plugin-entry" {
  export interface PluginApi {
    pluginConfig?: unknown;
    logger: {
      info(message: string): void;
      warn(message: string): void;
      error(message: string): void;
    };
    runtime: unknown;
    registerService(service: {
      id: string;
      start(): Promise<void> | void;
      stop(): Promise<void> | void;
    }): void;
    [key: string]: unknown;
  }

  export interface PluginEntry {
    id: string;
    name: string;
    description?: string;
    register(api: PluginApi): void | Promise<void>;
  }

  export function definePluginEntry(entry: PluginEntry): PluginEntry;
}
