import type {
  OpenClawPluginToolContext,
  OpenClawPluginToolFactory,
} from "openclaw/plugin-sdk/core";
import { resolveWecomSourceSnapshot } from "../../runtime/source-registry.js";
import { cleanSchemaForGemini } from "./schema.js";
import { clearWecomMcpCategoryCache, sendJsonRpc, type McpToolInfo } from "./transport.js";

type WecomMcpParams = {
  action: "list" | "call";
  category: string;
  method?: string;
  args?: string | Record<string, unknown>;
};

const BIZ_CACHE_CLEAR_ERROR_CODES = new Set([850002]);

function textResult<TDetails>(data: TDetails) {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }],
    details: data,
  };
}

function errorResult(error: unknown) {
  if (error && typeof error === "object" && "errcode" in error) {
    const errcode = Number((error as { errcode?: number }).errcode ?? 0);
    const errmsg = String((error as { errmsg?: string }).errmsg ?? `错误码: ${errcode}`);
    return textResult({ error: errmsg, errcode });
  }
  return textResult({
    error: error instanceof Error ? error.message : String(error),
  });
}

function parseArgs(args: string | Record<string, unknown> | undefined): Record<string, unknown> {
  if (!args) return {};
  if (typeof args === "object") return args;
  try {
    return JSON.parse(args) as Record<string, unknown>;
  } catch (error) {
    const detail = error instanceof SyntaxError ? error.message : String(error);
    throw new Error(`args 不是合法的 JSON: ${args} (${detail})`);
  }
}

function extractToolAccountId(ctx: OpenClawPluginToolContext): string | undefined {
  const explicit = String((ctx as { accountId?: string }).accountId ?? "").trim();
  if (explicit) return explicit;
  const agentAccountId = String(ctx.agentAccountId ?? "").trim();
  return agentAccountId || undefined;
}

async function handleList(accountId: string, category: string): Promise<unknown> {
  const result = (await sendJsonRpc(accountId, category, "tools/list")) as
    | { tools?: McpToolInfo[] }
    | undefined;
  const tools = result?.tools ?? [];
  return {
    accountId,
    category,
    count: tools.length,
    tools: tools.map((tool) => ({
      name: tool.name,
      description: tool.description ?? "",
      inputSchema: tool.inputSchema ? cleanSchemaForGemini(tool.inputSchema) : undefined,
    })),
  };
}

function checkBizErrorAndClearCache(result: unknown, accountId: string, category: string): void {
  if (!result || typeof result !== "object") return;
  const content = (result as { content?: Array<{ type: string; text?: string }> }).content;
  if (!Array.isArray(content)) return;
  for (const item of content) {
    if (item.type !== "text" || !item.text) continue;
    try {
      const parsed = JSON.parse(item.text) as { errcode?: number };
      if (typeof parsed.errcode === "number" && BIZ_CACHE_CLEAR_ERROR_CODES.has(parsed.errcode)) {
        clearWecomMcpCategoryCache(accountId, category);
        return;
      }
    } catch {
      // Ignore non-JSON content.
    }
  }
}

async function handleCall(
  accountId: string,
  category: string,
  method: string,
  args: Record<string, unknown>,
): Promise<unknown> {
  const result = await sendJsonRpc(accountId, category, "tools/call", {
    name: method,
    arguments: args,
  });
  checkBizErrorAndClearCache(result, accountId, category);
  return result;
}

export function createWeComMcpToolFactory(): OpenClawPluginToolFactory {
  return (toolContext: OpenClawPluginToolContext) => {
    if (toolContext.messageChannel !== "wecom") {
      return null;
    }
    const accountId = extractToolAccountId(toolContext);
    const source = resolveWecomSourceSnapshot({
      accountId,
      sessionKey: toolContext.sessionKey,
      sessionId: toolContext.sessionId,
    });
    if (!source || source.source !== "bot-ws") {
      return null;
    }

    return {
      name: "wecom_mcp",
      label: "WeCom MCP",
      description:
        "企业微信 Bot WS MCP 工具。仅在 WeCom Bot WS 会话中可用，用于列出和调用企业微信 MCP 能力。",
      parameters: {
        type: "object" as const,
        properties: {
          action: {
            type: "string",
            enum: ["list", "call"],
            description: "操作类型：list 或 call",
          },
          category: {
            type: "string",
            description: "MCP 品类，如 contact、todo、meeting、doc",
          },
          method: {
            type: "string",
            description: "action=call 时要调用的工具方法名",
          },
          args: {
            type: "string",
            description: "action=call 时传入的 JSON 字符串参数，默认 {}",
          },
        },
        required: ["action", "category"],
      },
      async execute(_toolCallId: string, rawParams: unknown) {
        try {
          const params = rawParams as WecomMcpParams;
          const effectiveAccountId = extractToolAccountId(toolContext);
          if (!effectiveAccountId) {
            throw new Error("当前会话缺少 WeCom accountId，无法调用 wecom_mcp。");
          }

          if (params.action === "list") {
            return textResult(await handleList(effectiveAccountId, params.category));
          }
          if (!params.method) {
            return textResult({ error: "action=call 时必须提供 method" });
          }
          return textResult(
            await handleCall(
              effectiveAccountId,
              params.category,
              params.method,
              parseArgs(params.args),
            ),
          );
        } catch (error) {
          return errorResult(error);
        }
      },
    };
  };
}
