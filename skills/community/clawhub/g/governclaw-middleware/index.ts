/**
 * GovernClaw Middleware Skill
 *
 * Provides governed wrappers for sensitive operations (HTTP, shell, file, browser).
 * All actions are validated against the GovernClaw policy engine before execution.
 */

import axios, { AxiosError } from "axios";

// GovernClaw service configuration
const GOVERNCLAW_BASE_URL = process.env.GOVERNCLAW_URL || "http://127.0.0.1:8000";
const GOVERNCLAW_GOVERN_URL = `${GOVERNCLAW_BASE_URL}/govern_action`;

/**
 * GovernClaw decision response
 */
interface GovernClawResponse {
  decision: "allow" | "block";
  reason: string;
  effective_payload?: Record<string, unknown>;
  audit_log: string[];
}

/**
 * GovernClaw request payload
 */
interface GovernClawRequest {
  parent_id: string;
  child_id: string;
  action_type: "http" | "file" | "shell" | "browser" | "node" | "integration";
  mode: "playground" | "governed" | "strict";
  description: string;
  payload: Record<string, unknown>;
  source: "agent" | "control" | "cron" | "node" | "webhook";
  channel?: string;
  skill: string;
  node_id?: string;
}

/**
 * Context passed by OpenClaw runtime
 */
interface OpenClawContext {
  sessionId?: string;
  agentId?: string;
  source?: string;
  channel?: string;
  nodeId?: string;
  tools: {
    http: {
      json: (params: {
        method: string;
        url: string;
        body?: unknown;
        headers?: Record<string, string>;
      }) => Promise<unknown>;
    };
  };
}

/**
 * Build the GovernClaw request payload from context and action details
 */
function buildGovernClawRequest(
  context: OpenClawContext,
  actionType: GovernClawRequest["action_type"],
  description: string,
  payload: Record<string, unknown>
): GovernClawRequest {
  return {
    parent_id: context.sessionId || "unknown-session",
    child_id: context.agentId || "unknown-agent",
    action_type: actionType,
    mode: "governed",
    description,
    payload,
    source: (context.source as GovernClawRequest["source"]) || "agent",
    channel: context.channel,
    skill: "governclaw-middleware",
    node_id: context.nodeId,
  };
}

/**
 * Query GovernClaw for policy decision
 */
async function queryGovernClaw(
  request: GovernClawRequest
): Promise<GovernClawResponse> {
  try {
    const response = await axios.post<GovernClawResponse>(
      GOVERNCLAW_GOVERN_URL,
      request,
      {
        headers: { "Content-Type": "application/json" },
        timeout: 10000, // 10 second timeout for policy decision
      }
    );
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      const message = error.response?.data?.detail || error.message;
      throw new Error(`GovernClaw request failed: ${message}`);
    }
    throw error;
  }
}

/**
 * Governed HTTP tool - validates HTTP requests against GovernClaw policies
 */
async function governedHttp(
  params: {
    method: "GET" | "POST" | "PUT" | "DELETE";
    url: string;
    body?: Record<string, unknown>;
    headers?: Record<string, string>;
  },
  context: OpenClawContext
): Promise<unknown> {
  const { method, url, body, headers } = params;

  // Build the governance request
  const governRequest = buildGovernClawRequest(
    context,
    "http",
    `OpenClaw HTTP ${method} to ${url}`,
    { url, method, body, headers }
  );

  // Query GovernClaw for policy decision
  const decision = await queryGovernClaw(governRequest);

  // If blocked, return block response without executing HTTP
  if (decision.decision !== "allow") {
    return {
      ok: false,
      blocked: true,
      reason: decision.reason,
      audit_log: decision.audit_log,
    };
  }

  // Policy allowed - execute the actual HTTP request
  // Use effective_payload if provided, otherwise use original params
  const effectivePayload = decision.effective_payload || { url, method, body, headers };

  try {
    const result = await context.tools.http.json({
      method: effectivePayload.method as string,
      url: effectivePayload.url as string,
      body: effectivePayload.body,
      headers: effectivePayload.headers as Record<string, string> | undefined,
    });

    return result;
  } catch (error) {
    // Pass through HTTP errors from the underlying tool
    if (error instanceof Error) {
      return {
        ok: false,
        error: error.message,
        blocked: false,
      };
    }
    throw error;
  }
}

/**
 * Export the skill's tools
 */
export const tools = {
  governedHttp: {
    description:
      "Makes HTTP requests through the GovernClaw policy engine. Use this instead of the raw HTTP tool when calling external APIs.",
    parameters: {
      type: "object",
      properties: {
        method: {
          type: "string",
          enum: ["GET", "POST", "PUT", "DELETE"],
          description: "HTTP method to use",
        },
        url: {
          type: "string",
          description: "Target URL for the request",
        },
        body: {
          type: "object",
          description: "Request body (for POST/PUT requests)",
        },
        headers: {
          type: "object",
          description: "Custom HTTP headers",
          additionalProperties: { type: "string" },
        },
      },
      required: ["method", "url"],
    },
    handler: governedHttp,
  },
};

// Default export for OpenClaw skill loader
export default { tools };
