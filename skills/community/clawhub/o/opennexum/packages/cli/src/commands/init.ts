import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import readline from "node:readline";
import type { Command } from "commander";
import { detectAvailableCli, detectGitRemote } from "../lib/detect.js";

// ─── AGENTS.md callback protocol block ────────────────────────────────────────

const CALLBACK_BLOCK_START = "<!-- nexum:callback:start -->";
const CALLBACK_BLOCK_END = "<!-- nexum:callback:end -->";
const DEFAULT_AGENT_GUIDE = `# AGENTS.md

## 核心规范
- 使用 Conventional Commits。
- 保持 commit 原子化；一个 commit 只做一件完整的事。
- 直接 push 到 main/master，快速迭代，出问题直接 revert。
`;
const CALLBACK_PROTOCOL_BLOCK = `${CALLBACK_BLOCK_START}
## Nexum 回调协议（必须遵守）

每完成一个 nexum 任务后，必须执行以下命令（在 git commit + push 之后）：

\`\`\`bash
nexum callback <taskId> --project <projectDir> \\
  --model <使用的模型名> \\
  --input-tokens <input token 数量> \\
  --output-tokens <output token 数量>
\`\`\`

示例：
\`\`\`bash
nexum callback INFRA-001 --project /path/to/project \\
  --model claude-sonnet-4-6 \\
  --input-tokens 12345 \\
  --output-tokens 2048
\`\`\`

注意事项：
- token 数量从本次对话的实际消耗中读取，无法确认时填 0
- 模型名填当前使用的模型（如 claude-sonnet-4-6、gpt-5.4 等）
- 此步骤会触发评估流程和编排通知，不可跳过
${CALLBACK_BLOCK_END}
`;

// ─── Helpers ──────────────────────────────────────────────────────────────────

async function fileExists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function writeIfNotExists(filePath: string, content: string): Promise<boolean> {
  if (await fileExists(filePath)) {
    return false;
  }
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, content, "utf8");
  return true;
}

async function ensureGitkeep(dirPath: string): Promise<boolean> {
  const gitkeepPath = path.join(dirPath, ".gitkeep");
  if (await fileExists(gitkeepPath)) {
    return false;
  }
  await mkdir(dirPath, { recursive: true });
  await writeFile(gitkeepPath, "", "utf8");
  return true;
}

async function upsertCallbackProtocol(
  projectDir: string
): Promise<{ result: "created" | "updated" | "unchanged"; targetFile: string }> {
  const agentsPath = path.join(projectDir, "AGENTS.md");
  const claudePath = path.join(projectDir, "CLAUDE.md");
  const hasAgents = await fileExists(agentsPath);
  const hasClaude = await fileExists(claudePath);

  const blockPattern = new RegExp(
    `${CALLBACK_BLOCK_START}[\\s\\S]*?${CALLBACK_BLOCK_END}\\n?`,
    "g"
  );

  if (!hasAgents && !hasClaude) {
    await writeFile(
      agentsPath,
      `${DEFAULT_AGENT_GUIDE}\n${CALLBACK_PROTOCOL_BLOCK}\n`,
      "utf8"
    );
    return { result: "created", targetFile: agentsPath };
  }

  const sourcePath = hasAgents ? agentsPath : claudePath;
  const current = await readFile(sourcePath, "utf8");
  const withoutExistingBlock = current.replace(blockPattern, "").trimEnd();
  const next = `${withoutExistingBlock ? `${withoutExistingBlock}\n\n` : ""}${CALLBACK_PROTOCOL_BLOCK}\n`;

  if (hasAgents && next === current) {
    return { result: "unchanged", targetFile: agentsPath };
  }

  await writeFile(agentsPath, next, "utf8");
  return { result: hasAgents ? "updated" : "created", targetFile: agentsPath };
}

// ─── Interactive wizard ────────────────────────────────────────────────────────

function createAsk(rl: readline.Interface) {
  return (question: string): Promise<string> =>
    new Promise((resolve) => rl.question(question, resolve));
}

interface WizardAnswers {
  projectName: string;
  stack: string;
  gitRemote: string;
  gitBranch: string;
  notifyTarget: string;
  watchEnabled: boolean;
  watchIntervalMin: number;
  watchTimeoutMin: number;
}

type InitAgentConfig = {
  cli: string;
  model?: string;
  reasoning?: string;
  execution: {
    runtime: string;
    agentId: string;
  };
};

async function runWizard(projectDir: string, useDefaults: boolean): Promise<WizardAnswers> {
  const defaultProjectName = path.basename(projectDir);

  if (useDefaults) {
    return {
      projectName: defaultProjectName,
      stack: "",
      gitRemote: "origin",
      gitBranch: "main",
      notifyTarget: "",
      watchEnabled: false,
      watchIntervalMin: 5,
      watchTimeoutMin: 60,
    };
  }

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const ask = createAsk(rl);

  try {
    // Step 1: project name
    const projectNameInput = (await ask(`项目名 (默认: ${defaultProjectName}): `)).trim();
    const projectName = projectNameInput || defaultProjectName;

    // Step 2: stack description
    const stack = (await ask("技术栈描述 (默认: 留空): ")).trim();

    // Step 3: git remote
    const gitRemoteInput = (await ask("Git remote 名称 (默认: origin, 输入 - 跳过 push): ")).trim();
    // Empty input → default to 'origin'; enter a single space or '-' to opt out of push
    const gitRemote = gitRemoteInput === "" ? "origin" : (gitRemoteInput === "-" ? "" : gitRemoteInput);

    if (gitRemote) {
      process.stdout.write(`  正在检测 ${gitRemote} 连通性...`);
      const reachable = await detectGitRemote(projectDir, gitRemote);
      if (reachable) {
        process.stdout.write(" ✓\n");
      } else {
        process.stdout.write(" ✗ (无法连通，仍将写入配置，请确认 remote 是否正确)\n");
      }
    }

    // Step 4: git branch
    const gitBranchInput = (await ask("Git branch (默认: main): ")).trim();
    const gitBranch = gitBranchInput || "main";

    // Step 5: notify target
    const notifyTarget = (await ask("OpenClaw notify target (默认: 留空): ")).trim();

    // Step 6: watch
    const watchInput = (await ask("是否启用 watch 模式？(默认: n) [y/n]: ")).trim().toLowerCase();
    const watchEnabled = watchInput === "y" || watchInput === "yes";

    let watchIntervalMin = 5;
    let watchTimeoutMin = 60;

    if (watchEnabled) {
      const intervalInput = (await ask("Watch 检查间隔（分钟，默认: 5）: ")).trim();
      watchIntervalMin = parseInt(intervalInput, 10) || 5;

      const timeoutInput = (await ask("Watch 超时时间（分钟，默认: 60）: ")).trim();
      watchTimeoutMin = parseInt(timeoutInput, 10) || 60;
    }

    return {
      projectName,
      stack,
      gitRemote,
      gitBranch,
      notifyTarget,
      watchEnabled,
      watchIntervalMin,
      watchTimeoutMin,
    };
  } finally {
    rl.close();
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────

export async function runInit(projectDir: string, yes: boolean): Promise<void> {
  const isTTY = !!(process.stdin.isTTY && process.stdout.isTTY);
  const useDefaults = yes || !isTTY;

  // Detect available CLIs
  process.stdout.write("检测可用 CLI...");
  const cliAvail = await detectAvailableCli();
  const parts: string[] = [];
  if (cliAvail.claude) parts.push("claude ✓");
  else parts.push("claude ✗ (未检测到)");
  if (cliAvail.codex) parts.push("codex ✓");
  else parts.push("codex ✗ (未检测到)");
  console.log(` ${parts.join(", ")}`);

  if (!cliAvail.claude && !cliAvail.codex) {
    console.warn(
      "警告：未检测到任何可用的 AI CLI（claude / codex），初始化继续但任务无法派发。"
    );
  }

  // Interactive wizard (or defaults)
  const answers = await runWizard(projectDir, useDefaults);

  const agents: Record<string, InitAgentConfig> = {
    "codex-gen-01": buildInitAgent("codex", "gpt-5.4", "high"),
    "codex-gen-02": buildInitAgent("codex", "gpt-5.4", "high"),
    "codex-gen-03": buildInitAgent("codex", "gpt-5.4", "high"),
    "codex-frontend-01": buildInitAgent("codex", "gpt-5.4", "medium"),
    "codex-eval-01": buildInitAgent("codex", "gpt-5.4", "high"),
    "codex-e2e-01": buildInitAgent("codex", "gpt-5.4", "medium"),
    "claude-gen-01": buildInitAgent("claude", "sonnet-4-6"),
    "claude-gen-02": buildInitAgent("claude", "sonnet-4-6"),
    "claude-eval-01": buildInitAgent("claude", "sonnet-4-6"),
    "claude-plan-01": buildInitAgent("claude", "opus-4-6"),
  };

  // Build full config
  const config: Record<string, unknown> = {
    project: {
      name: answers.projectName,
      ...(answers.stack ? { stack: answers.stack } : {}),
    },
    git: {
      remote: answers.gitRemote,
      branch: answers.gitBranch,
    },
    notify: {
      ...(answers.notifyTarget ? { target: answers.notifyTarget } : {}),
    },
    watch: {
      enabled: answers.watchEnabled,
      ...(answers.watchEnabled
        ? {
            intervalMin: answers.watchIntervalMin,
            timeoutMin: answers.watchTimeoutMin,
          }
        : {}),
    },
    webhook: {
      agentId: "orchestrator",
    },
    agents,
  };

  // Write files
  const nexumDir = path.join(projectDir, "nexum");
  const activeTasksPath = path.join(nexumDir, "active-tasks.json");
  const configPath = path.join(nexumDir, "config.json");
  const contractsDir = path.join(projectDir, "docs", "nexum", "contracts");
  const evalDir = path.join(nexumDir, "runtime", "eval");
  const fieldReportsDir = path.join(nexumDir, "runtime", "field-reports");

  const created: string[] = [];

  if (await writeIfNotExists(activeTasksPath, JSON.stringify({ tasks: [] }, null, 2) + "\n")) {
    created.push(activeTasksPath);
  }

  await mkdir(nexumDir, { recursive: true });
  await writeFile(configPath, JSON.stringify(config, null, 2) + "\n", "utf8");
  created.push(configPath);

  if (await ensureGitkeep(contractsDir)) {
    created.push(path.join(contractsDir, ".gitkeep"));
  }

  if (await ensureGitkeep(evalDir)) {
    created.push(path.join(evalDir, ".gitkeep"));
  }

  if (await ensureGitkeep(fieldReportsDir)) {
    created.push(path.join(fieldReportsDir, ".gitkeep"));
  }

  const { result: callbackResult, targetFile: callbackTarget } =
    await upsertCallbackProtocol(projectDir);
  if (callbackResult === "created" || callbackResult === "updated") {
    created.push(callbackTarget);
  }

  console.log("\nnexum 初始化完成：");
  for (const file of created) {
    console.log(`  写入 ${path.relative(projectDir, file)}`);
  }
}

function buildInitAgent(cli: "codex" | "claude", model: string, reasoning?: string): InitAgentConfig {
  return {
    cli,
    model,
    ...(reasoning ? { reasoning } : {}),
    execution: {
      runtime: "acp",
      agentId: cli,
    },
  };
}

export function registerInit(program: Command): void {
  program
    .command("init")
    .description("Initialize nexum project structure (interactive wizard)")
    .option("--project <dir>", "Project directory", process.cwd())
    .option("--yes", "Skip interactive prompts, use all defaults")
    .action(async (options: { project: string; yes?: boolean }) => {
      try {
        await runInit(options.project, options.yes ?? false);
      } catch (err) {
        console.error("init failed:", err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });
}
