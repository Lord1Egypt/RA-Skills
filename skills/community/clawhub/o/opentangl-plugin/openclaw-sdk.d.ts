/**
 * Minimal type stubs for the OpenClaw Plugin SDK.
 * The real types are provided by the `openclaw` package at runtime.
 * These stubs exist so the plugin can be authored and type-checked
 * without a full OpenClaw installation.
 */

declare module "openclaw/plugin-sdk/plugin-entry" {
  import type { TSchema } from "@sinclair/typebox";

  export interface ToolResult {
    content: Array<{ type: "text"; text: string }>;
    isError?: boolean;
  }

  export interface ToolDefinition<P extends TSchema = TSchema> {
    name: string;
    description: string;
    parameters: P;
    execute(
      id: string,
      params: Record<string, unknown>
    ): Promise<ToolResult>;
  }

  export interface ToolOptions {
    optional?: boolean;
  }

  export interface OpenClawPluginApi {
    id: string;
    name: string;
    version?: string;
    description?: string;
    pluginConfig: Record<string, unknown>;
    registerTool<P extends TSchema>(
      tool: ToolDefinition<P>,
      opts?: ToolOptions
    ): void;
  }

  export interface PluginEntryConfig {
    id: string;
    name: string;
    description?: string;
    register(api: OpenClawPluginApi): void;
  }

  export function definePluginEntry(config: PluginEntryConfig): unknown;
}
