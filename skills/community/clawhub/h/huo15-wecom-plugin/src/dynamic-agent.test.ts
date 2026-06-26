import os from "node:os";
import path from "node:path";

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import {
  ensureDynamicAgentListed,
  generateAgentId,
  getDynamicAgentConfig,
  resetEnsuredCache,
  shouldUseDynamicAgent,
} from "./dynamic-agent.js";

describe("getDynamicAgentConfig v2.9.2 seed defaults", () => {
  it("seedFromMainWorkspace defaults to true", () => {
    expect(getDynamicAgentConfig({} as never).seedFromMainWorkspace).toBe(true);
  });

  it("seedFiles defaults to [IDENTITY, SOUL, USER, AGENTS]", () => {
    expect(getDynamicAgentConfig({} as never).seedFiles).toEqual([
      "IDENTITY.md",
      "SOUL.md",
      "USER.md",
      "AGENTS.md",
    ]);
  });

  it("mainWorkspacePath inherits from agents.defaults.workspace", () => {
    const cfg = { agents: { defaults: { workspace: "/Users/test/.openclaw/workspace" } } };
    expect(getDynamicAgentConfig(cfg as never).mainWorkspacePath).toBe("/Users/test/.openclaw/workspace");
  });

  it("explicit mainWorkspacePath overrides agents.defaults.workspace", () => {
    const cfg = {
      agents: { defaults: { workspace: "/wrong" } },
      channels: { wecom: { dynamicAgents: { mainWorkspacePath: "/explicit" } } },
    };
    expect(getDynamicAgentConfig(cfg as never).mainWorkspacePath).toBe("/explicit");
  });
});

describe("getDynamicAgentConfig defaults (v2.9.0)", () => {
  it("enabled defaults to true (was false in v2.8.x)", () => {
    expect(getDynamicAgentConfig({} as never).enabled).toBe(true);
  });

  it("workspaceTemplate defaults to ~/.openclaw/workspace-{agentId}", () => {
    expect(getDynamicAgentConfig({} as never).workspaceTemplate).toBe("~/.openclaw/workspace-{agentId}");
  });

  it("agentDirTemplate defaults to ~/.openclaw/agents/{agentId}/agent", () => {
    expect(getDynamicAgentConfig({} as never).agentDirTemplate).toBe("~/.openclaw/agents/{agentId}/agent");
  });

  it("maxAgents defaults to 100", () => {
    expect(getDynamicAgentConfig({} as never).maxAgents).toBe(100);
  });

  it("user override wins", () => {
    const cfg = {
      channels: {
        wecom: {
          dynamicAgents: {
            enabled: false,
            workspaceTemplate: "~/custom/{agentId}",
            agentDirTemplate: "~/custom/agents/{agentId}",
            maxAgents: 5,
          },
        },
      },
    };
    expect(getDynamicAgentConfig(cfg as never)).toMatchObject({
      enabled: false,
      workspaceTemplate: "~/custom/{agentId}",
      agentDirTemplate: "~/custom/agents/{agentId}",
      maxAgents: 5,
    });
  });
});

describe("shouldUseDynamicAgent gate", () => {
  it("returns true for any non-admin sender by default (v2.9.0)", () => {
    expect(shouldUseDynamicAgent({ chatType: "group", senderId: "alice", config: {} as never })).toBe(true);
    expect(shouldUseDynamicAgent({ chatType: "dm", senderId: "alice", config: {} as never })).toBe(true);
  });

  it("explicit disabled returns false", () => {
    const cfg = { channels: { wecom: { dynamicAgents: { enabled: false } } } };
    expect(shouldUseDynamicAgent({ chatType: "group", senderId: "alice", config: cfg as never })).toBe(false);
  });

  it("admin senders bypass dynamic routing (route to main)", () => {
    const cfg = { channels: { wecom: { dynamicAgents: { enabled: true, adminUsers: ["ZhaoBo"] } } } };
    expect(shouldUseDynamicAgent({ chatType: "group", senderId: "ZhaoBo", config: cfg as never })).toBe(false);
    expect(shouldUseDynamicAgent({ chatType: "group", senderId: "Other", config: cfg as never })).toBe(true);
  });
});

describe("ensureDynamicAgentListed (v2.9.0 — writes workspace + agentDir + bindings)", () => {
  let writtenCfg: Record<string, unknown> | null = null;
  let mkdirCalls: string[] = [];

  function makeRuntime(initialCfg: Record<string, unknown>) {
    return {
      config: {
        loadConfig: () => initialCfg,
        writeConfigFile: vi.fn(async (cfg: unknown) => {
          writtenCfg = cfg as Record<string, unknown>;
        }),
      },
    };
  }

  beforeEach(() => {
    resetEnsuredCache();
    writtenCfg = null;
    mkdirCalls = [];
    vi.spyOn(os, "homedir").mockReturnValue("/Users/test");
    // Spy mkdir without breaking dynamic import (node:fs/promises is loaded inside ensureDynamicAgentListed)
    vi.doMock("node:fs/promises", () => ({
      mkdir: vi.fn(async (p: string) => {
        mkdirCalls.push(p);
      }),
    }));
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.doUnmock("node:fs/promises");
  });

  it("writes complete agent entry { id, workspace, agentDir } AND a route binding", async () => {
    const cfg: Record<string, unknown> = { agents: {}, bindings: [] };
    const runtime = makeRuntime(cfg);

    await ensureDynamicAgentListed({
      agentId: "wecom-default-group-chat123",
      chatType: "group",
      peerId: "chat123",
      accountId: "default",
      runtime,
    });

    expect(runtime.config.writeConfigFile).toHaveBeenCalledTimes(1);
    const list = (writtenCfg!.agents as { list: Array<Record<string, string>> }).list;
    // main is auto-inserted as first entry on first dynamic derive
    expect(list).toEqual(
      expect.arrayContaining([
        { id: "main" },
        {
          id: "wecom-default-group-chat123",
          workspace: path.join("/Users/test", ".openclaw", "workspace-wecom-default-group-chat123"),
          agentDir: path.join("/Users/test", ".openclaw", "agents", "wecom-default-group-chat123", "agent"),
        },
      ]),
    );
    expect(writtenCfg!.bindings).toEqual([
      {
        type: "route",
        agentId: "wecom-default-group-chat123",
        match: {
          channel: "wecom",
          accountId: "default",
          peer: { kind: "group", id: "chat123" },
        },
      },
    ]);
  });

  it("is idempotent — second call with same agentId does NOT writeConfigFile again", async () => {
    const cfg: Record<string, unknown> = { agents: {}, bindings: [] };
    const runtime = makeRuntime(cfg);

    await ensureDynamicAgentListed({
      agentId: "wecom-default-dm-alice",
      chatType: "dm",
      peerId: "alice",
      accountId: "default",
      runtime,
    });
    await ensureDynamicAgentListed({
      agentId: "wecom-default-dm-alice",
      chatType: "dm",
      peerId: "alice",
      accountId: "default",
      runtime,
    });

    expect(runtime.config.writeConfigFile).toHaveBeenCalledTimes(1);
  });

  it("migrates legacy entry { id } only → fills workspace + agentDir + binding", async () => {
    const cfg: Record<string, unknown> = {
      agents: {
        list: [
          { id: "main" },
          { id: "wecom-default-group-legacy" }, // 旧版本只有 id
        ],
      },
      bindings: [], // 旧版本忘了写 binding
    };
    const runtime = makeRuntime(cfg);

    await ensureDynamicAgentListed({
      agentId: "wecom-default-group-legacy",
      chatType: "group",
      peerId: "legacy",
      accountId: "default",
      runtime,
    });

    expect(runtime.config.writeConfigFile).toHaveBeenCalledTimes(1);
    const list = (writtenCfg!.agents as { list: Array<Record<string, string>> }).list;
    const migrated = list.find((e) => e.id === "wecom-default-group-legacy");
    expect(migrated).toMatchObject({
      workspace: expect.stringContaining("workspace-wecom-default-group-legacy"),
      agentDir: expect.stringContaining(path.join("agents", "wecom-default-group-legacy", "agent")),
    });
    expect(writtenCfg!.bindings).toEqual([
      expect.objectContaining({ agentId: "wecom-default-group-legacy" }),
    ]);
  });

  it("rejects new derive when maxAgents reached, keeps existing list intact", async () => {
    const existing = Array.from({ length: 3 }, (_, i) => ({
      id: `wecom-default-group-c${i}`,
      workspace: `/tmp/w${i}`,
      agentDir: `/tmp/a${i}`,
    }));
    const cfg: Record<string, unknown> = {
      agents: { list: [{ id: "main" }, ...existing] },
      bindings: [],
      channels: { wecom: { dynamicAgents: { maxAgents: 3 } } }, // limit = 3, existing already has 3
    };
    const runtime = makeRuntime(cfg);
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});

    await ensureDynamicAgentListed({
      agentId: "wecom-default-group-overflow",
      chatType: "group",
      peerId: "overflow",
      accountId: "default",
      runtime,
    });

    // 上限到了 → writeConfigFile 不应被调用
    expect(runtime.config.writeConfigFile).not.toHaveBeenCalled();
    expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining("maxAgents=3 reached"));
  });

  it("renders custom workspaceTemplate / agentDirTemplate with all template vars", async () => {
    const cfg: Record<string, unknown> = {
      agents: {},
      bindings: [],
      channels: {
        wecom: {
          dynamicAgents: {
            workspaceTemplate: "~/custom-ws/{accountId}/{chatType}/{peerId}-{agentId}",
            agentDirTemplate: "~/custom-ad/{userId}",
          },
        },
      },
    };
    const runtime = makeRuntime(cfg);

    await ensureDynamicAgentListed({
      agentId: "wecom-default-group-c1",
      chatType: "group",
      peerId: "c1",
      accountId: "default",
      runtime,
    });

    const list = (writtenCfg!.agents as { list: Array<Record<string, string>> }).list;
    const entry = list.find((e) => e.id === "wecom-default-group-c1")!;
    expect(entry.workspace).toBe(
      path.join("/Users/test", "custom-ws", "default", "group", "c1-wecom-default-group-c1"),
    );
    expect(entry.agentDir).toBe(path.join("/Users/test", "custom-ad", "c1"));
  });
});

describe("generateAgentId account scoping", () => {
  it("generates different ids for same peer across accounts", () => {
    const a = generateAgentId("dm", "zhangsan", "acct-a");
    const b = generateAgentId("dm", "zhangsan", "acct-b");
    expect(a).toBe("wecom-acct-a-dm-zhangsan");
    expect(b).toBe("wecom-acct-b-dm-zhangsan");
    expect(a).not.toBe(b);
  });

  it("falls back to default account scope when accountId is omitted", () => {
    expect(generateAgentId("group", "wr123456")).toBe("wecom-default-group-wr123456");
  });
});
