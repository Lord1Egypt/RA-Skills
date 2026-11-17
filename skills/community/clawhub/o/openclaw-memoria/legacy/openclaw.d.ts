// Type stub for OpenClaw plugin SDK (provided at runtime by the gateway)
declare module "openclaw/plugin-sdk/core" {
  export interface OpenClawPluginApi {
    logger: {
      info?: (...args: any[]) => void;
      warn?: (...args: any[]) => void;
      debug?: (...args: any[]) => void;
      error?: (...args: any[]) => void;
    };
    pluginConfig: Record<string, any>;
    config: Record<string, any>;
    workspace: { path: string };
    on: (event: string, handler: (...args: any[]) => any) => void;
    modifyPrompt: (callback: (ctx: any) => any) => void;
  }
}
