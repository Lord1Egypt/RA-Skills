import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { buildWorkspaceSkillCommandSpecs, loadWorkspaceSkillEntries } from "../../src/agents/skills.js";
import { createTestPluginApi } from "../../test/helpers/extensions/plugin-api.js";
import { createPluginRuntimeMock } from "../../test/helpers/extensions/plugin-runtime-mock.js";
import type {
  AnyAgentTool,
  OpenClawPluginCommandDefinition,
  PluginHookHandlerMap,
} from "../../src/plugins/types.js";
import pluginEntry from "./index.js";
import {
  DEFAULT_TRANSCRIPT_PREFIX,
  flushTelemetryEvents,
  OBSERVABILITY_LAB_PLUGIN_ID,
  resetObservabilityLabRuntimeState,
  resolveTelemetryLogPath,
  type ObservabilityLabConfig,
} from "./src/observability.js";

const tempDirs: string[] = [];

function createPluginConfig(config: Partial<ObservabilityLabConfig> = {}) {
  return {
    plugins: {
      entries: {
        [OBSERVABILITY_LAB_PLUGIN_ID]: {
          enabled: true,
          config: {
            captureEnabled: false,
            rewriteEnabled: false,
            transcriptPrefix: DEFAULT_TRANSCRIPT_PREFIX,
            ...config,
          },
        },
      },
    },
  };
}

async function makeTempDir() {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "openclaw-observability-lab-"));
  tempDirs.push(dir);
  return dir;
}

async function copyPluginIntoWorkspace(workspaceDir: string) {
  const pluginDir = path.dirname(fileURLToPath(import.meta.url));
  const targetDir = path.join(workspaceDir, ".openclaw", "extensions", OBSERVABILITY_LAB_PLUGIN_ID);
  await fs.mkdir(path.dirname(targetDir), { recursive: true });
  await fs.cp(pluginDir, targetDir, { recursive: true });
}

function createHarness(config: ReturnType<typeof createPluginConfig>) {
  let currentConfig = config;
  const commands = new Map<string, OpenClawPluginCommandDefinition>();
  const hooks = new Map<keyof PluginHookHandlerMap, PluginHookHandlerMap[keyof PluginHookHandlerMap]>();
  const tools = new Map<string, AnyAgentTool>();

  const stateDir = path.join(os.tmpdir(), `openclaw-observability-lab-state-${Date.now()}-${Math.random()}`);
  tempDirs.push(stateDir);

  const runtime = createPluginRuntimeMock({
    config: {
      loadConfig: vi.fn(() => currentConfig),
      writeConfigFile: vi.fn(async (nextConfig) => {
        currentConfig = nextConfig as typeof currentConfig;
      }),
    },
    state: {
      resolveStateDir: vi.fn(() => stateDir),
    },
  });

  const api = createTestPluginApi({
    id: OBSERVABILITY_LAB_PLUGIN_ID,
    name: "Observability Lab",
    source: "workspace",
    config: currentConfig as never,
    runtime,
    registerCommand: (command) => {
      commands.set(command.name, command);
    },
    registerTool: (tool) => {
      if (typeof tool === "function") {
        throw new Error("test harness expects concrete tools only");
      }
      tools.set(tool.name, tool as AnyAgentTool);
    },
    on: (hookName, handler) => {
      hooks.set(hookName, handler);
    },
  });

  pluginEntry.register(api);

  return {
    commands,
    hooks,
    runtime,
    tools,
    getConfig: () => currentConfig,
    stateDir,
  };
}

afterEach(async () => {
  resetObservabilityLabRuntimeState();
  await Promise.all(
    tempDirs.splice(0, tempDirs.length).map((dir) => fs.rm(dir, { recursive: true, force: true })),
  );
});

describe("observability-lab plugin", () => {
  it("ships a plugin-packaged skill that becomes a slash command", async () => {
    const workspaceDir = await makeTempDir();
    await copyPluginIntoWorkspace(workspaceDir);

    const config = createPluginConfig();
    const entries = loadWorkspaceSkillEntries(workspaceDir, {
      config,
      managedSkillsDir: path.join(workspaceDir, ".managed"),
      bundledSkillsDir: path.join(workspaceDir, ".bundled"),
    });
    const commands = buildWorkspaceSkillCommandSpecs(workspaceDir, {
      config,
      managedSkillsDir: path.join(workspaceDir, ".managed"),
      bundledSkillsDir: path.join(workspaceDir, ".bundled"),
    });

    expect(entries.map((entry) => entry.skill.name)).toContain("observe-demo");
    expect(commands).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          skillName: "observe-demo",
          name: "observe_demo",
        }),
      ]),
    );
  });

  it("registers multiple deterministic plugin slash commands", async () => {
    const harness = createHarness(createPluginConfig());

    expect(Array.from(harness.commands.keys()).toSorted()).toEqual([
      "observe",
      "observe_help",
      "observe_tail",
    ]);
    expect(Array.from(harness.tools.keys())).toEqual(["observe_demo_echo"]);

    const observe = harness.commands.get("observe");
    const help = harness.commands.get("observe_help");
    if (!observe || !help) {
      throw new Error("expected plugin commands to be registered");
    }

    const enableResult = await observe.handler({
      args: "on",
      channel: "discord",
      channelId: "discord",
      isAuthorizedSender: true,
      commandBody: "/observe on",
      config: harness.getConfig() as never,
      requestConversationBinding: vi.fn(),
      detachConversationBinding: vi.fn(),
      getCurrentConversationBinding: vi.fn(),
    });
    const helpResult = await help.handler({
      channel: "discord",
      channelId: "discord",
      isAuthorizedSender: true,
      commandBody: "/observe_help",
      config: harness.getConfig() as never,
      requestConversationBinding: vi.fn(),
      detachConversationBinding: vi.fn(),
      getCurrentConversationBinding: vi.fn(),
    });

    expect(enableResult).toEqual({ text: "【可观测实验室】 录制已开启。" });
    expect(helpResult).toEqual({
      text: [
        "【可观测实验室】 使用说明",
        "",
        "插件命令：",
        "/observe status",
        "/observe on",
        "/observe off",
        "/observe rewrite on",
        "/observe rewrite off",
        "/observe prefix [text]",
        "/observe_tail",
        "/observe_help",
        "",
        "技能命令：",
        "/observe_demo <text>",
        "/skill observe-demo <text>",
        "",
        "说明：",
        "- 遥测会先写入内存队列，再异步刷入本地 JSONL 文件",
        "- 只有当前会话命中本插件命令或 observe-demo 技能后，才会开始记录后续事件",
        "- 记录范围会持续到本次会话结束，不会自动影响下一次新会话",
        "- before_message_write 可以同步改写 assistant 转写文本，不会阻塞文件 I/O",
        "- /observe_demo 现在是真正的 skill；是否调用工具由 agent 按 skill 指令自己决定",
      ].join("\n"),
    });
    expect(harness.getConfig().plugins.entries[OBSERVABILITY_LAB_PLUGIN_ID]?.config).toEqual({
      captureEnabled: true,
      rewriteEnabled: false,
      transcriptPrefix: DEFAULT_TRANSCRIPT_PREFIX,
    });

    const demoTool = harness.tools.get("observe_demo_echo");
    if (!demoTool) {
      throw new Error("expected demo tool to be registered");
    }
    const toolResult = await demoTool.execute("tool-1", {
      command: "test",
      commandName: "observe_demo",
      skillName: "observe-demo",
    });
    expect(toolResult).toEqual({
      content: [
        {
          type: "text",
          text: [
            "【可观测实验室】 技能调用已确认",
            "- 插件：observability-lab",
            "- 技能：observe-demo",
            "- 命令：observe_demo",
            "- 输入：test",
          ].join("\n"),
        },
      ],
      details: {
        pluginId: "observability-lab",
        skillName: "observe-demo",
        commandName: "observe_demo",
        input: "test",
      },
    });
  });

  it("只在命中插件 skill 后记录当前会话的后续事件，并在会话结束后停止", async () => {
    const harness = createHarness(createPluginConfig({ captureEnabled: true }));

    const sessionStart = harness.hooks.get("session_start");
    const messageReceived = harness.hooks.get("message_received");
    const llmInput = harness.hooks.get("llm_input");
    const beforeToolCall = harness.hooks.get("before_tool_call");
    const afterToolCall = harness.hooks.get("after_tool_call");
    const beforeMessageWrite = harness.hooks.get("before_message_write");
    const sessionEnd = harness.hooks.get("session_end");
    if (
      !sessionStart ||
      !messageReceived ||
      !llmInput ||
      !beforeToolCall ||
      !afterToolCall ||
      !beforeMessageWrite ||
      !sessionEnd
    ) {
      throw new Error("expected all demo hooks to be registered");
    }

    await sessionStart(
      {
        sessionId: "session-1",
        sessionKey: "agent:main:discord:user:42",
      },
      {
        sessionId: "session-1",
        sessionKey: "agent:main:discord:user:42",
        agentId: "main",
      },
    );

    await messageReceived(
      {
        from: "discord:user:42",
        content: "/observe_demo test",
      },
      {
        channelId: "discord",
        accountId: "default",
        conversationId: "user:42",
      },
    );

    await beforeToolCall(
      {
        toolName: "observe_demo_echo",
        params: { command: "test" },
        runId: "run-1",
        toolCallId: "tool-1",
      },
      {
        toolName: "observe_demo_echo",
        runId: "run-1",
        toolCallId: "tool-1",
        sessionId: "session-1",
        sessionKey: "agent:main:discord:user:42",
        agentId: "main",
      },
    );

    await afterToolCall(
      {
        toolName: "observe_demo_echo",
        params: { command: "test" },
        runId: "run-1",
        toolCallId: "tool-1",
        result: { ok: true },
      },
      {
        toolName: "observe_demo_echo",
        runId: "run-1",
        toolCallId: "tool-1",
        sessionId: "session-1",
        sessionKey: "agent:main:discord:user:42",
        agentId: "main",
      },
    );

    await messageReceived(
      {
        from: "discord:user:42",
        content: "hello after activation",
      },
      {
        channelId: "discord",
        accountId: "default",
        conversationId: "user:42",
      },
    );

    await llmInput(
      {
        runId: "run-2",
        sessionId: "session-1",
        provider: "openai",
        model: "gpt-5.4",
        prompt: "hello after activation",
        historyMessages: [],
        imagesCount: 0,
      },
      {
        sessionId: "session-1",
        sessionKey: "agent:main:discord:user:42",
        agentId: "main",
      },
    );

    const beforeWriteResult = await beforeMessageWrite(
      {
        message: {
          role: "assistant",
          content: "【可观测实验室】 技能调用已确认",
        },
        sessionKey: "agent:main:discord:user:42",
        agentId: "main",
      },
      {
        sessionKey: "agent:main:discord:user:42",
        agentId: "main",
      },
    );

    await sessionEnd(
      {
        sessionId: "session-1",
        sessionKey: "agent:main:discord:user:42",
        messageCount: 3,
      },
      {
        sessionId: "session-1",
        sessionKey: "agent:main:discord:user:42",
        agentId: "main",
      },
    );

    expect(beforeWriteResult).toEqual({});

    await flushTelemetryEvents({ stateDir: harness.stateDir });
    const telemetryPath = resolveTelemetryLogPath(harness.stateDir);
    const telemetryLines = (await fs.readFile(telemetryPath, "utf8"))
      .trim()
      .split("\n")
      .map((line) => JSON.parse(line) as { type: string });

    expect(telemetryLines.map((line) => line.type)).toEqual([
      "before_tool_call",
      "after_tool_call",
      "message_received",
      "llm_input",
      "before_message_write",
      "session_end",
    ]);

    const tailCommand = harness.commands.get("observe_tail");
    if (!tailCommand) {
      throw new Error("expected observe_tail command");
    }
    const tailResult = await tailCommand.handler({
      channel: "discord",
      channelId: "discord",
      isAuthorizedSender: true,
      commandBody: "/observe_tail",
      config: harness.getConfig() as never,
      requestConversationBinding: vi.fn(),
      detachConversationBinding: vi.fn(),
      getCurrentConversationBinding: vi.fn(),
    });

    expect(tailResult).toEqual({
      text: [
        "【可观测实验室】 最近遥测：",
        "1. after_tool_call",
        "2. message_received",
        "3. llm_input",
        "4. before_message_write",
        "5. session_end",
      ].join("\n"),
    });
  });

  it("在当前会话被激活后，before_message_write 才会改写 assistant 文本", async () => {
    const harness = createHarness(
      createPluginConfig({
        captureEnabled: true,
        rewriteEnabled: true,
        transcriptPrefix: "[audit] ",
      }),
    );

    const observe = harness.commands.get("observe");
    const beforeMessageWrite = harness.hooks.get("before_message_write");
    if (!observe || !beforeMessageWrite) {
      throw new Error("expected observe command and before_message_write hook");
    }

    const rewriteStatus = await observe.handler({
      args: "rewrite status",
      channel: "discord",
      channelId: "discord",
      isAuthorizedSender: true,
      commandBody: "/observe rewrite status",
      config: harness.getConfig() as never,
      requestConversationBinding: vi.fn(),
      detachConversationBinding: vi.fn(),
      getCurrentConversationBinding: vi.fn(),
    });

    expect(rewriteStatus).toEqual({
      text: "【可观测实验室】 改写当前为开启（前缀：[audit] ）。",
    });

    const activationWriteResult = beforeMessageWrite(
      {
        message: {
          role: "assistant",
          content: "【可观测实验室】 状态",
        },
        sessionKey: "agent:main:webchat",
        agentId: "main",
      },
      {
        sessionKey: "agent:main:webchat",
        agentId: "main",
      },
    );

    expect(activationWriteResult).toEqual({
      message: {
        role: "assistant",
        content: "[audit] 【可观测实验室】 状态",
      },
    });

    const beforeWriteResult = beforeMessageWrite(
      {
        message: {
          role: "assistant",
          content: [
            { type: "thinking", thinking: "plan" },
            { type: "text", text: "ready" },
          ],
        },
        sessionKey: "agent:main:webchat",
        agentId: "main",
      },
      {
        sessionKey: "agent:main:webchat",
        agentId: "main",
      },
    );

    expect(beforeWriteResult).toEqual({
      message: {
        role: "assistant",
        content: [
          { type: "thinking", thinking: "plan" },
          { type: "text", text: "[audit] ready" },
        ],
      },
    });

    await flushTelemetryEvents({ stateDir: harness.stateDir });
    const telemetryPath = resolveTelemetryLogPath(harness.stateDir);
    const telemetryLines = (await fs.readFile(telemetryPath, "utf8"))
      .trim()
      .split("\n")
      .map((line) => JSON.parse(line) as { type: string; event: { message?: { role?: string } } });

    expect(telemetryLines).toEqual([
      expect.objectContaining({
        type: "before_message_write",
        event: expect.objectContaining({
          message: expect.objectContaining({ role: "assistant" }),
        }),
      }),
      expect.objectContaining({
        type: "before_message_write",
        event: expect.objectContaining({
          message: expect.objectContaining({ role: "assistant" }),
        }),
      }),
    ]);
  });

  it("会在 session_end 后清掉激活态，不影响下一次新会话", async () => {
    const harness = createHarness(createPluginConfig({ captureEnabled: true }));

    const beforeToolCall = harness.hooks.get("before_tool_call");
    const llmOutput = harness.hooks.get("llm_output");
    const sessionEnd = harness.hooks.get("session_end");
    const sessionStart = harness.hooks.get("session_start");
    if (!beforeToolCall || !llmOutput || !sessionEnd || !sessionStart) {
      throw new Error("expected lifecycle hooks to be registered");
    }

    await beforeToolCall(
      {
        toolName: "observe_demo_echo",
        params: { command: "test" },
        runId: "run-1",
        toolCallId: "tool-1",
      },
      {
        toolName: "observe_demo_echo",
        runId: "run-1",
        toolCallId: "tool-1",
        sessionId: "session-1",
        sessionKey: "agent:main:webchat",
        agentId: "main",
      },
    );

    await sessionEnd(
      {
        sessionId: "session-1",
        sessionKey: "agent:main:webchat",
        messageCount: 1,
      },
      {
        sessionId: "session-1",
        sessionKey: "agent:main:webchat",
        agentId: "main",
      },
    );

    await sessionStart(
      {
        sessionId: "session-2",
        sessionKey: "agent:main:webchat",
      },
      {
        sessionId: "session-2",
        sessionKey: "agent:main:webchat",
        agentId: "main",
      },
    );

    await llmOutput(
      {
        runId: "run-2",
        sessionId: "session-2",
        provider: "openai",
        model: "gpt-5.4",
        assistantTexts: ["should not be captured"],
        lastAssistant: {
          role: "assistant",
          content: [{ type: "text", text: "should not be captured" }],
        },
        usage: { input: 1, output: 1, total: 2 },
      },
      {
        sessionId: "session-2",
        sessionKey: "agent:main:webchat",
        agentId: "main",
      },
    );

    await flushTelemetryEvents({ stateDir: harness.stateDir });
    const telemetryPath = resolveTelemetryLogPath(harness.stateDir);
    const telemetryLines = (await fs.readFile(telemetryPath, "utf8"))
      .trim()
      .split("\n")
      .map((line) => JSON.parse(line) as { type: string });

    expect(telemetryLines.map((line) => line.type)).toEqual(["before_tool_call", "session_end"]);
  });
});
