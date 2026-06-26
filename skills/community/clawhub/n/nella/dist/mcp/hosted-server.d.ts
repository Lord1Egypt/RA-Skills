/**
 * Hosted MCP Server
 *
 * Exposes Nella's MCP tools over Streamable HTTP transport.
 * Authenticates via API keys stored in Supabase, rate limits via Redis,
 * and logs usage to the usage_events table.
 *
 * Usage:
 *   nella serve --port 3000
 *   NODE_ENV=production node packages/nella/dist/mcp/hosted-server.js
 *
 * Required env vars:
 *   SUPABASE_URL              - Supabase project URL
 *   SUPABASE_SERVICE_ROLE_KEY - Supabase service role key
 *   REDIS_URL                 - Redis connection string (rediss://... for TLS)
 *
 * Optional env vars:
 *   PORT                      - HTTP port (default: 3000)
 *   NELLA_LOG_LEVEL           - Log level (default: info)
 */
interface HostedServerOptions {
    port?: number;
    host?: string;
}
declare function startHostedServer(options?: HostedServerOptions): Promise<void>;

export { type HostedServerOptions, startHostedServer };
