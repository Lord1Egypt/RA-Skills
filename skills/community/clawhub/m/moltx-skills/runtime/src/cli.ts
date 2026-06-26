import { coreTools } from "./tools/core.js";
import { apiTools } from "./tools/api.js";
import { hashTools } from "./tools/hash.js";
import { predictionTools } from "./tools/prediction.js";
import { councilTools } from "./tools/council.js";
import { eventTools } from "./tools/events.js";
import { agentSyncTools } from "./tools/agent-sync.js";
import { agentQueryTools } from "./tools/agent-query.js";
import { walletTools } from "./tools/wallet.js";
import { siweTools } from "./tools/siwe.js";
import { identityTools } from "./tools/identity.js";

type ToolHandler = (args: unknown) => Promise<string>;

const toolRegistry: Record<string, ToolHandler> = {
  ...apiTools,
  ...coreTools,
  ...hashTools,
  ...predictionTools,
  ...councilTools,
  ...eventTools,
  ...agentSyncTools,
  ...agentQueryTools,
  ...walletTools,
  ...siweTools,
  ...identityTools,
};

function printAndExit(message: string, code: number): never {
  process.stdout.write(message.endsWith("\n") ? message : `${message}\n`);
  process.exit(code);
}

function parseJsonPayload(argv: string[]): unknown {
  const jsonFlagIndex = argv.indexOf("--json");
  if (jsonFlagIndex === -1 || jsonFlagIndex === argv.length - 1) {
    throw new Error('missing --json \'<payload>\'');
  }

  return JSON.parse(argv[jsonFlagIndex + 1]);
}

async function main(): Promise<void> {
  const [, , command, ...rest] = process.argv;

  if (command === "list") {
    printAndExit(Object.keys(toolRegistry).sort().join("\n"), 0);
  }

  if (command === "call") {
    const toolName = rest[0];
    if (!toolName) {
      printAndExit('{"error":"missing tool name"}', 1);
    }

    const tool = toolRegistry[toolName];
    if (!tool) {
      printAndExit(`{"error":"unknown tool: ${toolName}"}`, 1);
    }

    try {
      const payload = parseJsonPayload(rest.slice(1));
      printAndExit(await tool(payload), 0);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "unknown runtime error";
      printAndExit(JSON.stringify({ error: message }), 1);
    }
  }

  printAndExit('{"error":"usage: list | call <tool_name> --json \'<payload>\'"}', 1);
}

await main();
