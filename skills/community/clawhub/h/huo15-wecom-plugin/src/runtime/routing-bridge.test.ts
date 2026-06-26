import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { resolveRuntimeRoute } from "./routing-bridge.js";
import { ensureDynamicAgentListed } from "../dynamic-agent.js";
import type { UnifiedInboundEvent } from "../types/index.js";

vi.mock("../dynamic-agent.js", async () => {
  const actual = await vi.importActual<typeof import("../dynamic-agent.js")>(
    "../dynamic-agent.js",
  );
  return {
    ...actual,
    ensureDynamicAgentListed: vi.fn().mockResolvedValue(undefined),
  };
});

describe("resolveRuntimeRoute", () => {
  beforeEach(() => {
    vi.mocked(ensureDynamicAgentListed).mockClear();
  });

  it("overrides WS runtime routes with dynamic agent routing for direct chats", () => {
    const baseRoute = {
      agentId: "main",
      channel: "wecom",
      accountId: "acct-ws",
      sessionKey: "agent:main",
      mainSessionKey: "agent:main:main",
      lastRoutePolicy: "session" as const,
      matchedBy: "default" as const,
    };
    const resolveAgentRoute = vi.fn().mockReturnValue({ ...baseRoute });
    const core = {
      channel: {
        routing: {
          resolveAgentRoute,
        },
      },
    } as unknown as PluginRuntime;
    const cfg = {
      channels: {
        wecom: {
          dynamicAgents: {
            enabled: true,
          },
        },
      },
    } as OpenClawConfig;
    const event = {
      accountId: "acct-ws",
      conversation: {
        accountId: "acct-ws",
        peerKind: "direct",
        peerId: "HiDaoMax",
        senderId: "HiDaoMax",
      },
    } as UnifiedInboundEvent;

    const route = resolveRuntimeRoute({ core, cfg, event });

    expect(resolveAgentRoute).toHaveBeenCalledOnce();
    expect(route.agentId).toBe("wecom-acct-ws-dm-hidaomax");
    expect(route.sessionKey).toBe(
      "agent:wecom-acct-ws-dm-hidaomax:wecom:acct-ws:dm:HiDaoMax",
    );
    expect(vi.mocked(ensureDynamicAgentListed)).toHaveBeenCalledWith({
      agentId: "wecom-acct-ws-dm-hidaomax",
      chatType: "dm",
      peerId: "HiDaoMax",
      accountId: "acct-ws",
      runtime: core,
    });
  });

  it("keeps the resolved core route when dynamic agent routing is disabled for the sender", () => {
    const baseRoute = {
      agentId: "main",
      channel: "wecom",
      accountId: "acct-ws",
      sessionKey: "agent:main",
      mainSessionKey: "agent:main:main",
      lastRoutePolicy: "session" as const,
      matchedBy: "binding.account" as const,
    };
    const core = {
      channel: {
        routing: {
          resolveAgentRoute: vi.fn().mockReturnValue({ ...baseRoute }),
        },
      },
    } as unknown as PluginRuntime;
    const cfg = {
      channels: {
        wecom: {
          dynamicAgents: {
            enabled: true,
            adminUsers: ["HiDaoMax"],
          },
        },
      },
    } as OpenClawConfig;
    const event = {
      accountId: "acct-ws",
      conversation: {
        accountId: "acct-ws",
        peerKind: "direct",
        peerId: "HiDaoMax",
        senderId: "HiDaoMax",
      },
    } as UnifiedInboundEvent;

    const route = resolveRuntimeRoute({ core, cfg, event });

    expect(route).toEqual(baseRoute);
    expect(vi.mocked(ensureDynamicAgentListed)).not.toHaveBeenCalled();
  });
});
