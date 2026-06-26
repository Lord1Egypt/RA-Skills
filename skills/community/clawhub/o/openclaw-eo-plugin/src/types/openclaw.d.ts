declare module 'openclaw' {
  export interface ToolDefinition {
    name: string;
    description?: string;
    inputSchema?: {
      type: string;
      properties?: Record<string, any>;
    };
    handler: Function;
  }
  export interface HookDefinition {
    id: string;
    name: string;
    event: string;
    handler: Function;
  }
  export interface PluginApi {
    registerTool(tool: ToolDefinition): void;
    registerHook(hook: HookDefinition): void;
    getContext(): any;
  }
  export type HookHandler = any;
}

declare module 'openclaw/plugins' {
  export const PluginApi: any;
}

declare module '@openclaw/shared' {
  export const shared: any;
}
