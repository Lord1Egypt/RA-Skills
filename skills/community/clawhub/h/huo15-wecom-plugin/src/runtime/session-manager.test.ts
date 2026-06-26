import { beforeEach, describe, expect, it, vi } from "vitest";
import { prepareInboundSession } from "./session-manager.js";

const {
  resolveRuntimeRoute,
  getPeerContextToken,
  registerWecomSourceSnapshot,
} = vi.hoisted(() => ({
  resolveRuntimeRoute: vi.fn(),
  getPeerContextToken: vi.fn(),
  registerWecomSourceSnapshot: vi.fn(),
}));

vi.mock("./routing-bridge.js", () => ({
  resolveRuntimeRoute,
}));

vi.mock("../context-store.js", () => ({
  getPeerContextToken,
}));

vi.mock("./source-registry.js", () => ({
  registerWecomSourceSnapshot,
}));

function createCore() {
  const finalizeInboundContext = vi.fn((ctx) => ctx);
  const recordInboundSession = vi.fn(async () => {});

  return {
    core: {
      channel: {
        session: {
          resolveStorePath: vi.fn(() => "/tmp/wecom-session-store"),
          readSessionUpdatedAt: vi.fn(() => 1234567890),
          recordInboundSession,
        },
        reply: {
          resolveEnvelopeFormatOptions: vi.fn(() => ({ envelope: "default" })),
          formatAgentEnvelope: vi.fn(() => "formatted-body"),
          finalizeInboundContext,
        },
      },
    } as any,
    finalizeInboundContext,
    recordInboundSession,
  };
}

function createMediaService() {
  return {
    normalizeFirstAttachment: vi.fn(async () => undefined),
    saveInboundAttachment: vi.fn(async () => undefined),
  } as any;
}

describe("prepareInboundSession", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    resolveRuntimeRoute.mockReturnValue({
      sessionKey: "agent:ops_bot:wecom:direct:hidaomax",
      agentId: "ops_bot",
      accountId: "default",
    });
  });

  it("marks bot-ws turns as the current wecom surface", async () => {
    getPeerContextToken.mockReturnValue("ctx-bot");
    const { core, finalizeInboundContext, recordInboundSession } = createCore();

    const result = await prepareInboundSession({
      core,
      cfg: {} as any,
      event: {
        accountId: "default",
        transport: "bot-ws",
        messageId: "msg-bot-1",
        conversation: {
          peerKind: "direct",
          peerId: "HiDaoMax",
          senderId: "HiDaoMax",
        },
        senderName: "HiDaoMax",
        text: "hello",
      } as any,
      mediaService: createMediaService(),
    });

    expect(finalizeInboundContext).toHaveBeenCalledWith(
      expect.objectContaining({
        Provider: "wecom",
        Surface: "wecom",
        OriginatingChannel: "wecom",
        OriginatingTo: "wecom:context:ctx-bot",
        To: "wecom:user:HiDaoMax",
      }),
    );
    expect(recordInboundSession).toHaveBeenCalledTimes(1);
    expect(result.ctx.Provider).toBe("wecom");
    expect(result.ctx.Surface).toBe("wecom");
  });

  it("keeps agent-callback turns on provider-only context", async () => {
    getPeerContextToken.mockReturnValue(undefined);
    const { core, finalizeInboundContext } = createCore();

    const result = await prepareInboundSession({
      core,
      cfg: {} as any,
      event: {
        accountId: "default",
        transport: "agent-callback",
        messageId: "msg-agent-1",
        conversation: {
          peerKind: "direct",
          peerId: "HiDaoMax",
          senderId: "HiDaoMax",
        },
        senderName: "HiDaoMax",
        text: "hello",
      } as any,
      mediaService: createMediaService(),
    });

    expect(finalizeInboundContext).toHaveBeenCalledWith(
      expect.objectContaining({
        Provider: "wecom",
        OriginatingChannel: "wecom",
        OriginatingTo: "wecom:user:HiDaoMax",
      }),
    );
    expect(result.ctx.Provider).toBe("wecom");
    expect(result.ctx).not.toHaveProperty("Surface");
  });

  it("registers SessionId for source lookups after context finalization", async () => {
    getPeerContextToken.mockReturnValue(undefined);
    const { core } = createCore();
    core.channel.reply.finalizeInboundContext = vi.fn((ctx) => ({
      ...ctx,
      SessionId: "sess-agent-1",
    }));

    await prepareInboundSession({
      core,
      cfg: {} as any,
      event: {
        accountId: "default",
        transport: "agent-callback",
        messageId: "msg-agent-2",
        conversation: {
          peerKind: "direct",
          peerId: "HiDaoMax",
          senderId: "HiDaoMax",
        },
        senderName: "HiDaoMax",
        text: "hello",
      } as any,
      mediaService: createMediaService(),
    });

    expect(registerWecomSourceSnapshot).toHaveBeenLastCalledWith(
      expect.objectContaining({
        accountId: "default",
        source: "agent-callback",
        messageId: "msg-agent-2",
        sessionKey: "agent:ops_bot:wecom:direct:hidaomax",
        sessionId: "sess-agent-1",
        peerKind: "direct",
        peerId: "HiDaoMax",
      }),
    );
  });
});
