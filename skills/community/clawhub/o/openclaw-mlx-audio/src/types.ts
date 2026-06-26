/**
 * OpenClaw Plugin Type Definitions
 */

export interface OpenClawPlugin {
  name: string;
  version: string;
  init?: (config: any) => Promise<void>;
  tools?: Record<string, PluginTool>;
  commands?: Record<string, PluginCommand>;
  [key: string]: any;
}

export interface PluginTool {
  description: string;
  parameters: {
    type: string;
    properties: Record<string, any>;
    required?: string[];
  };
  execute: (params: any) => Promise<any>;
}

export interface PluginCommand {
  description: string;
  execute: (subcommand: string, args: string[]) => Promise<string>;
}
