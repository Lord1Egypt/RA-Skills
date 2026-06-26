import { homedir } from "node:os";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { BotWsPushHandle } from "./app/index.js";
import { extractMediaDirectives } from "./outbound.js";

vi.mock("./transport/agent-api/core.js", () => ({
  sendText: vi.fn(),
  sendMedia: vi.fn(),
  uploadMedia: vi.fn(),
}));

describe("wecomOutbound", () => {
  const createBotWsHandle = (overrides: Partial<BotWsPushHandle> = {}): BotWsPushHandle => ({
    isConnected: () => true,
    sendMarkdown: vi.fn().mockResolvedValue(undefined),
    replyCommand: vi.fn().mockResolvedValue({ errcode: 0 }),
    sendMedia: vi.fn().mockResolvedValue({ ok: true, messageId: "ws-media-1" }),
    ...overrides,
  });

  beforeEach(async () => {
    const runtime = await import("./runtime.js");
    runtime.setWecomRuntime({
      channel: {
        text: {
          chunkText: (text: string) => [text],
        },
      },
    } as any);
  });

  afterEach(async () => {
    const runtime = await import("./runtime.js");
    const sourceRegistry = await import("./runtime/source-registry.js");
    runtime.unregisterBotWsPushHandle("default");
    runtime.unregisterBotWsPushHandle("acct-ws");
    runtime.unregisterActiveBotWsReplyHandle({
      accountId: "default",
      sessionKey: "agent:ops_bot:wecom:default:dm:zhangsan",
      peerKind: "direct",
      peerId: "zhangsan",
    });
    runtime.unregisterActiveBotWsReplyHandle({
      accountId: "acct-ws",
      sessionKey: "agent:ops_bot:wecom:acct-ws:dm:lisi",
      peerKind: "direct",
      peerId: "lisi",
    });
    sourceRegistry.clearWecomSourceAccount("default");
    sourceRegistry.clearWecomSourceAccount("acct-ws");
    vi.unstubAllGlobals();
  });

  it("does not crash when called with core outbound params", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    await expect(
      wecomOutbound.sendMedia({
        cfg: {},
        to: "wr-test-chat",
        text: "caption",
        mediaUrl: "https://example.com/media.png",
      } as any),
    ).rejects.toThrow(/requires Agent mode for account=default/i);
  });

  it("throws explicit error when outbound accountId does not exist", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          defaultAccount: "acct-a",
          accounts: {
            "acct-a": {
              enabled: true,
              agent: {
                corpId: "corp-a",
                corpSecret: "secret-a",
                agentId: 10001,
                token: "token-a",
                encodingAESKey: "aes-a",
              },
            },
          },
        },
      },
    };
    await expect(
      wecomOutbound.sendText({
        cfg,
        accountId: "acct-missing",
        to: "user:zhangsan",
        text: "hello",
      } as any),
    ).rejects.toThrow(/account "acct-missing" not found/i);
  });

  it("routes sendText to agent chatId/userid", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const api = await import("./transport/agent-api/core.js");
    const now = vi.spyOn(Date, "now").mockReturnValue(123);
    (api.sendText as any).mockResolvedValue(undefined);

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          agent: {
            corpId: "corp",
            corpSecret: "secret",
            agentId: 1000002,
            token: "token",
            encodingAESKey: "aes",
          },
        },
      },
    };

    // Chat ID (wr/wc) is intentionally NOT supported for Agent outbound.
    await expect(
      wecomOutbound.sendText({ cfg, to: "wr123", text: "hello" } as any),
    ).rejects.toThrow(/不支持向群 chatId 发送/);
    expect(api.sendText).not.toHaveBeenCalled();

    // Test: User ID (Default)
    const userResult = await wecomOutbound.sendText({
      cfg,
      to: "userid123",
      text: "hi",
    } as any);
    expect(api.sendText).toHaveBeenCalledWith(
      expect.objectContaining({
        chatId: undefined,
        toUser: "userid123",
        toParty: undefined,
        toTag: undefined,
        text: "hi",
      }),
    );
    expect(userResult.messageId).toBe("agent-123");

    (api.sendText as any).mockClear();

    // Test: User ID explicit
    await wecomOutbound.sendText({ cfg, to: "user:zhangsan", text: "hi" } as any);
    expect(api.sendText).toHaveBeenCalledWith(
      expect.objectContaining({ toUser: "zhangsan", toParty: undefined }),
    );

    (api.sendText as any).mockClear();

    // Test: Numeric targets default to User ID
    await wecomOutbound.sendText({ cfg, to: "1001", text: "hi party" } as any);
    expect(api.sendText).toHaveBeenCalledWith(
      expect.objectContaining({ toUser: "1001", toParty: undefined }),
    );

    (api.sendText as any).mockClear();

    // Test: Party ID Explicit
    await wecomOutbound.sendText({ cfg, to: "party:2002", text: "hi party 2" } as any);
    expect(api.sendText).toHaveBeenCalledWith(
      expect.objectContaining({ toUser: undefined, toParty: "2002" }),
    );

    (api.sendText as any).mockClear();

    // Test: Tag ID Explicit
    await wecomOutbound.sendText({ cfg, to: "tag:1", text: "hi tag" } as any);
    expect(api.sendText).toHaveBeenCalledWith(
      expect.objectContaining({ toUser: undefined, toTag: "1" }),
    );

    now.mockRestore();
  });

  it("suppresses /new ack for bot sessions but not agent sessions", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const api = await import("./transport/agent-api/core.js");
    const sourceRegistry = await import("./runtime/source-registry.js");
    const now = vi.spyOn(Date, "now").mockReturnValue(456);
    (api.sendText as any).mockResolvedValue(undefined);
    (api.sendText as any).mockClear();

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          agent: {
            corpId: "corp",
            corpSecret: "secret",
            agentId: 1000002,
            token: "token",
            encodingAESKey: "aes",
          },
        },
      },
    };

    const ack = "✅ New session started · model: openai-codex/gpt-5.2";

    // Bot 会话（wecom:...）应抑制，避免私信回执
    const r1 = await wecomOutbound.sendText({ cfg, to: "wecom:userid123", text: ack } as any);
    expect(api.sendText).not.toHaveBeenCalled();
    expect(r1.messageId).toBe("suppressed-456");

    (api.sendText as any).mockClear();

    sourceRegistry.registerWecomSourceSnapshot({
      accountId: "default",
      source: "agent-callback",
      sessionKey: "agent:ops_bot:wecom:default:dm:userid123",
      peerKind: "direct",
      peerId: "userid123",
    });

    // Agent 会话允许发送回执，即使 target 是普通 wecom:user:...
    await wecomOutbound.sendText({
      cfg,
      accountId: "default",
      sessionKey: "agent:ops_bot:wecom:default:dm:userid123",
      to: "wecom:user:userid123",
      text: ack,
    } as any);
    expect(api.sendText).toHaveBeenCalledWith(
      expect.objectContaining({
        toUser: "userid123",
        text: "✅ 已开启新会话（模型：openai-codex/gpt-5.2）",
      }),
    );

    now.mockRestore();
  });

  it("prefers Bot WS active push for text when ws is the active bot transport", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const api = await import("./transport/agent-api/core.js");
    const sendMarkdown = vi.fn().mockResolvedValue(undefined);
    const now = vi.spyOn(Date, "now").mockReturnValue(789);
    runtime.registerBotWsPushHandle(
      "acct-ws",
      createBotWsHandle({
        sendMarkdown,
      }),
    );
    (api.sendText as any).mockClear();

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          defaultAccount: "acct-ws",
          accounts: {
            "acct-ws": {
              enabled: true,
              bot: {
                primaryTransport: "ws",
                ws: {
                  botId: "bot-1",
                  secret: "secret-1",
                },
              },
              agent: {
                corpId: "corp-ws",
                corpSecret: "agent-secret",
                agentId: 10001,
                token: "token-ws",
                encodingAESKey: "aes-ws",
              },
            },
          },
        },
      },
    };

    const result = await wecomOutbound.sendText({
      cfg,
      accountId: "acct-ws",
      to: "user:lisi",
      text: "hello ws",
    } as any);

    expect(sendMarkdown).toHaveBeenCalledWith("lisi", "hello ws");
    expect(api.sendText).not.toHaveBeenCalled();
    expect(result.messageId).toBe("bot-ws-789");

    now.mockRestore();
  });

  it("keeps agent-source sessions on the Agent text path even when ws is primary", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const api = await import("./transport/agent-api/core.js");
    const sourceRegistry = await import("./runtime/source-registry.js");
    const sendMarkdown = vi.fn().mockResolvedValue(undefined);
    runtime.registerBotWsPushHandle(
      "acct-ws",
      createBotWsHandle({
        sendMarkdown,
      }),
    );
    sourceRegistry.registerWecomSourceSnapshot({
      accountId: "acct-ws",
      source: "agent-callback",
      sessionKey: "agent:ops_bot:wecom:acct-ws:dm:lisi",
    });
    (api.sendText as any).mockResolvedValue(undefined);
    (api.sendText as any).mockClear();

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          defaultAccount: "acct-ws",
          accounts: {
            "acct-ws": {
              enabled: true,
              bot: {
                primaryTransport: "ws",
                ws: {
                  botId: "bot-1",
                  secret: "secret-1",
                },
              },
              agent: {
                corpId: "corp-ws",
                corpSecret: "agent-secret",
                agentId: 10001,
                token: "token-ws",
                encodingAESKey: "aes-ws",
              },
            },
          },
        },
      },
    };

    await wecomOutbound.sendText({
      cfg,
      accountId: "acct-ws",
      sessionKey: "agent:ops_bot:wecom:acct-ws:dm:lisi",
      to: "user:lisi",
      text: "hello agent",
    } as any);

    expect(sendMarkdown).not.toHaveBeenCalled();
    expect(api.sendText).toHaveBeenCalledWith(
      expect.objectContaining({
        toUser: "lisi",
        text: "hello agent",
      }),
    );
  });

  it("keeps agent-source peer targets on the Agent text path without sessionKey", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const api = await import("./transport/agent-api/core.js");
    const sourceRegistry = await import("./runtime/source-registry.js");
    const sendMarkdown = vi.fn().mockResolvedValue(undefined);
    runtime.registerBotWsPushHandle(
      "acct-ws",
      createBotWsHandle({
        sendMarkdown,
      }),
    );
    sourceRegistry.registerWecomSourceSnapshot({
      accountId: "acct-ws",
      source: "agent-callback",
      peerKind: "direct",
      peerId: "lisi",
    });
    (api.sendText as any).mockResolvedValue(undefined);
    (api.sendText as any).mockClear();

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          defaultAccount: "acct-ws",
          accounts: {
            "acct-ws": {
              enabled: true,
              bot: {
                primaryTransport: "ws",
                ws: {
                  botId: "bot-1",
                  secret: "secret-1",
                },
              },
              agent: {
                corpId: "corp-ws",
                corpSecret: "agent-secret",
                agentId: 10001,
                token: "token-ws",
                encodingAESKey: "aes-ws",
              },
            },
          },
        },
      },
    };

    await wecomOutbound.sendText({
      cfg,
      accountId: "acct-ws",
      to: "user:lisi",
      text: "hello peer",
    } as any);

    expect(sendMarkdown).not.toHaveBeenCalled();
    expect(api.sendText).toHaveBeenCalledWith(
      expect.objectContaining({
        toUser: "lisi",
        text: "hello peer",
      }),
    );
  });

  it("does not silently fall back to Agent when Bot WS active push is configured but unavailable", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const api = await import("./transport/agent-api/core.js");
    (api.sendText as any).mockClear();

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          bot: {
            primaryTransport: "ws",
            ws: {
              botId: "bot-1",
              secret: "secret-1",
            },
          },
          agent: {
            corpId: "corp",
            corpSecret: "secret",
            agentId: 1000002,
            token: "token",
            encodingAESKey: "aes",
          },
        },
      },
    };

    await expect(
      wecomOutbound.sendText({
        cfg,
        to: "user:zhangsan",
        text: "hello",
      } as any),
    ).rejects.toThrow(/no live ws runtime is registered/i);
    expect(api.sendText).not.toHaveBeenCalled();
  });

  it("prefers Bot WS for outbound media when ws is the active bot transport", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const api = await import("./transport/agent-api/core.js");
    const sendMedia = vi.fn().mockResolvedValue({ ok: true, messageId: "ws-media-1" });
    runtime.registerBotWsPushHandle(
      "default",
      createBotWsHandle({
        sendMedia,
      }),
    );
    (api.uploadMedia as any).mockResolvedValue("media-1");
    (api.sendMedia as any).mockResolvedValue(undefined);
    (api.sendMedia as any).mockClear();

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          bot: {
            primaryTransport: "ws",
            ws: {
              botId: "bot-1",
              secret: "secret-1",
            },
          },
          agent: {
            corpId: "corp",
            corpSecret: "secret",
            agentId: 1000002,
            token: "token",
            encodingAESKey: "aes",
          },
        },
      },
    };

    await wecomOutbound.sendMedia({
      cfg,
      to: "user:zhangsan",
      text: "caption",
      mediaUrl: "https://example.com/media.png",
    } as any);

    expect(sendMedia).toHaveBeenCalledWith({
      chatId: "zhangsan",
      maxBytes: 80 * 1024 * 1024,
      mediaUrl: "https://example.com/media.png",
      mediaLocalRoots: expect.any(Array),
      text: "caption",
    });
    expect(api.sendMedia).not.toHaveBeenCalled();
  });

  it("marks the active bot-ws reply handle when same-session text is sent via active push", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const api = await import("./transport/agent-api/core.js");
    const sendMarkdown = vi.fn().mockResolvedValue(undefined);
    const markExternalActivity = vi.fn();
    runtime.registerBotWsPushHandle(
      "acct-ws",
      createBotWsHandle({
        sendMarkdown,
      }),
    );
    runtime.registerActiveBotWsReplyHandle({
      accountId: "acct-ws",
      sessionKey: "agent:ops_bot:wecom:acct-ws:dm:lisi",
      peerKind: "direct",
      peerId: "lisi",
      handle: {
        context: {
          transport: "bot-ws",
          accountId: "acct-ws",
          raw: { transport: "bot-ws", envelopeType: "ws", body: {} },
        },
        deliver: vi.fn(),
        markExternalActivity,
      } as any,
    });
    (api.sendText as any).mockClear();

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          defaultAccount: "acct-ws",
          accounts: {
            "acct-ws": {
              enabled: true,
              bot: {
                primaryTransport: "ws",
                ws: {
                  botId: "bot-1",
                  secret: "secret-1",
                },
              },
              agent: {
                corpId: "corp-ws",
                corpSecret: "agent-secret",
                agentId: 10001,
                token: "token-ws",
                encodingAESKey: "aes-ws",
              },
            },
          },
        },
      },
    };

    await wecomOutbound.sendText({
      cfg,
      accountId: "acct-ws",
      sessionKey: "agent:ops_bot:wecom:acct-ws:dm:lisi",
      to: "user:lisi",
      text: "hello ws",
    } as any);

    expect(sendMarkdown).toHaveBeenCalledWith("lisi", "hello ws");
    expect(markExternalActivity).toHaveBeenCalledTimes(1);
    expect(api.sendText).not.toHaveBeenCalled();
  });

  it("keeps agent-source sessions on the Agent media path even when ws is primary", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const api = await import("./transport/agent-api/core.js");
    const sourceRegistry = await import("./runtime/source-registry.js");
    const sendMedia = vi.fn().mockResolvedValue({ ok: true, messageId: "ws-media-1" });
    runtime.registerBotWsPushHandle(
      "default",
      createBotWsHandle({
        sendMedia,
      }),
    );
    sourceRegistry.registerWecomSourceSnapshot({
      accountId: "default",
      source: "agent-callback",
      sessionKey: "agent:ops_bot:wecom:default:dm:zhangsan",
    });
    (api.uploadMedia as any).mockResolvedValue("media-1");
    (api.sendMedia as any).mockResolvedValue(undefined);
    (api.sendMedia as any).mockClear();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        arrayBuffer: async () => new Uint8Array([1, 2, 3]).buffer,
        headers: new Headers({ "content-type": "image/png" }),
      }),
    );

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          bot: {
            primaryTransport: "ws",
            ws: {
              botId: "bot-1",
              secret: "secret-1",
            },
          },
          agent: {
            corpId: "corp",
            corpSecret: "secret",
            agentId: 1000002,
            token: "token",
            encodingAESKey: "aes",
          },
        },
      },
    };

    await wecomOutbound.sendMedia({
      cfg,
      sessionKey: "agent:ops_bot:wecom:default:dm:zhangsan",
      to: "user:zhangsan",
      text: "caption",
      mediaUrl: "https://example.com/media.png",
    } as any);

    expect(sendMedia).not.toHaveBeenCalled();
    expect(api.sendMedia).toHaveBeenCalledTimes(1);
  });

  it("marks the active bot-ws reply handle when same-session media is sent via active push", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const sendMedia = vi.fn().mockResolvedValue({ ok: true, messageId: "ws-media-1" });
    const markExternalActivity = vi.fn();
    runtime.registerBotWsPushHandle(
      "default",
      createBotWsHandle({
        sendMedia,
      }),
    );
    runtime.registerActiveBotWsReplyHandle({
      accountId: "default",
      sessionKey: "agent:ops_bot:wecom:default:dm:zhangsan",
      peerKind: "direct",
      peerId: "zhangsan",
      handle: {
        context: {
          transport: "bot-ws",
          accountId: "default",
          raw: { transport: "bot-ws", envelopeType: "ws", body: {} },
        },
        deliver: vi.fn(),
        markExternalActivity,
      } as any,
    });

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          bot: {
            primaryTransport: "ws",
            ws: {
              botId: "bot-1",
              secret: "secret-1",
            },
          },
          agent: {
            corpId: "corp",
            corpSecret: "secret",
            agentId: 1000002,
            token: "token",
            encodingAESKey: "aes",
          },
        },
      },
    };

    await wecomOutbound.sendMedia({
      cfg,
      sessionKey: "agent:ops_bot:wecom:default:dm:zhangsan",
      to: "user:zhangsan",
      text: "caption",
      mediaUrl: "https://example.com/media.png",
    } as any);

    expect(sendMedia).toHaveBeenCalledTimes(1);
    expect(markExternalActivity).toHaveBeenCalledTimes(1);
  });

  it("keeps agent-source peer targets on the Agent media path without sessionKey", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const api = await import("./transport/agent-api/core.js");
    const sourceRegistry = await import("./runtime/source-registry.js");
    const sendMedia = vi.fn().mockResolvedValue({ ok: true, messageId: "ws-media-1" });
    runtime.registerBotWsPushHandle(
      "default",
      createBotWsHandle({
        sendMedia,
      }),
    );
    sourceRegistry.registerWecomSourceSnapshot({
      accountId: "default",
      source: "agent-callback",
      peerKind: "direct",
      peerId: "zhangsan",
    });
    (api.uploadMedia as any).mockResolvedValue("media-1");
    (api.sendMedia as any).mockResolvedValue(undefined);
    (api.sendMedia as any).mockClear();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        arrayBuffer: async () => new Uint8Array([1, 2, 3]).buffer,
        headers: new Headers({ "content-type": "image/png" }),
      }),
    );

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          bot: {
            primaryTransport: "ws",
            ws: {
              botId: "bot-1",
              secret: "secret-1",
            },
          },
          agent: {
            corpId: "corp",
            corpSecret: "secret",
            agentId: 1000002,
            token: "token",
            encodingAESKey: "aes",
          },
        },
      },
    };

    await wecomOutbound.sendMedia({
      cfg,
      to: "user:zhangsan",
      text: "caption",
      mediaUrl: "https://example.com/media.png",
    } as any);

    expect(sendMedia).not.toHaveBeenCalled();
    expect(api.sendMedia).toHaveBeenCalledTimes(1);
  });

  it("merges configured media local roots into Bot WS sends", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const sendMedia = vi.fn().mockResolvedValue({ ok: true, messageId: "ws-media-merged" });
    runtime.registerBotWsPushHandle(
      "default",
      createBotWsHandle({
        sendMedia,
      }),
    );

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          bot: {
            primaryTransport: "ws",
            ws: {
              botId: "bot-1",
              secret: "secret-1",
            },
          },
          media: {
            localRoots: ["/tmp/downloads"],
          },
        },
      },
    };

    await wecomOutbound.sendMedia({
      cfg,
      to: "user:zhangsan",
      mediaUrl: "/tmp/workspace-agent/01.png",
      mediaLocalRoots: ["/tmp/workspace-agent"],
    } as any);

    expect(sendMedia).toHaveBeenCalledWith(
      expect.objectContaining({
        chatId: "zhangsan",
        mediaUrl: "/tmp/workspace-agent/01.png",
        mediaLocalRoots: expect.arrayContaining(["/tmp/workspace-agent", "/tmp/downloads"]),
        text: undefined,
      }),
    );
  });

  it("passes account-aware mediaMaxMb to Bot WS media sends", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const sendMedia = vi.fn().mockResolvedValue({ ok: true, messageId: "ws-media-limit" });
    runtime.registerBotWsPushHandle(
      "acct-ws",
      createBotWsHandle({
        sendMedia,
      }),
    );

    const cfg = {
      agents: {
        defaults: {
          mediaMaxMb: 12,
        },
      },
      channels: {
        wecom: {
          enabled: true,
          mediaMaxMb: 24,
          accounts: {
            "acct-ws": {
              enabled: true,
              mediaMaxMb: 36,
              bot: {
                primaryTransport: "ws",
                ws: {
                  botId: "bot-1",
                  secret: "secret-1",
                },
              },
            },
          },
        },
      },
    };

    await wecomOutbound.sendMedia({
      cfg,
      accountId: "acct-ws",
      to: "user:zhangsan",
      mediaUrl: "https://example.com/media.png",
    } as any);

    expect(sendMedia).toHaveBeenCalledWith(
      expect.objectContaining({
        chatId: "zhangsan",
        maxBytes: 36 * 1024 * 1024,
      }),
    );
  });

  it("does not fall back to Agent media when Bot WS conversation media delivery fails", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const api = await import("./transport/agent-api/core.js");
    const sendMedia = vi.fn().mockResolvedValue({ ok: false, error: "upload failed" });
    runtime.registerBotWsPushHandle(
      "default",
      createBotWsHandle({
        sendMedia,
      }),
    );
    (api.uploadMedia as any).mockResolvedValue("media-1");
    (api.sendMedia as any).mockResolvedValue(undefined);
    (api.sendMedia as any).mockClear();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        arrayBuffer: async () => new Uint8Array([1, 2, 3]).buffer,
        headers: new Headers({ "content-type": "image/png" }),
      }),
    );

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          bot: {
            primaryTransport: "ws",
            ws: {
              botId: "bot-1",
              secret: "secret-1",
            },
          },
          agent: {
            corpId: "corp",
            corpSecret: "secret",
            agentId: 1000002,
            token: "token",
            encodingAESKey: "aes",
          },
        },
      },
    };

    await expect(
      wecomOutbound.sendMedia({
        cfg,
        to: "user:zhangsan",
        text: "caption",
        mediaUrl: "https://example.com/media.png",
      } as any),
    ).rejects.toThrow(/Bot WS media delivery failed/i);

    expect(sendMedia).toHaveBeenCalledTimes(1);
    expect(api.sendMedia).not.toHaveBeenCalled();
  });

  it("keeps explicit agent targets on the Agent media path", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const runtime = await import("./runtime.js");
    const api = await import("./transport/agent-api/core.js");
    const sendMedia = vi.fn().mockResolvedValue({ ok: true, messageId: "ws-media-1" });
    runtime.registerBotWsPushHandle(
      "default",
      createBotWsHandle({
        sendMedia,
      }),
    );
    (api.uploadMedia as any).mockResolvedValue("media-1");
    (api.sendMedia as any).mockResolvedValue(undefined);
    (api.sendMedia as any).mockClear();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        arrayBuffer: async () => new Uint8Array([1, 2, 3]).buffer,
        headers: new Headers({ "content-type": "image/png" }),
      }),
    );

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          bot: {
            primaryTransport: "ws",
            ws: {
              botId: "bot-1",
              secret: "secret-1",
            },
          },
          agent: {
            corpId: "corp",
            corpSecret: "secret",
            agentId: 1000002,
            token: "token",
            encodingAESKey: "aes",
          },
        },
      },
    };

    await wecomOutbound.sendMedia({
      cfg,
      to: "wecom-agent:default:user:zhangsan",
      text: "caption",
      mediaUrl: "https://example.com/media.png",
    } as any);

    expect(sendMedia).not.toHaveBeenCalled();
    expect(api.sendMedia).toHaveBeenCalledTimes(1);
  });

  it("routes explicit upstream agent text targets to the upstream delivery path", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const api = await import("./transport/agent-api/core.js");
    const client = await import("./transport/agent-api/client.js");
    const upstreamSpy = vi.spyOn(client, "sendUpstreamAgentApiText").mockResolvedValue(undefined);
    (api.sendText as any).mockClear();

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          agent: {
            corpId: "corp-main",
            corpSecret: "secret-main",
            agentId: 1000002,
            token: "token-main",
            encodingAESKey: "aes-main",
            upstreamCorps: {
              partner: {
                corpId: "corp-up",
                agentId: 2000001,
              },
            },
          },
        },
      },
    };

    await wecomOutbound.sendText({
      cfg,
      to: "wecom-agent-upstream:default:corp-up:zhangsan",
      text: "hello upstream",
    } as any);

    expect(upstreamSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        toUser: "zhangsan",
        text: "hello upstream",
        upstreamAgent: expect.objectContaining({
          corpId: "corp-up",
          agentId: 2000001,
        }),
        primaryAgent: expect.objectContaining({
          corpId: "corp-main",
          agentId: 1000002,
        }),
      }),
    );
    expect(api.sendText).not.toHaveBeenCalled();

    upstreamSpy.mockRestore();
  });

  it("routes plain agent targets to upstream delivery when session source snapshot carries upstream corp", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const api = await import("./transport/agent-api/core.js");
    const client = await import("./transport/agent-api/client.js");
    const sourceRegistry = await import("./runtime/source-registry.js");
    const upstreamSpy = vi.spyOn(client, "sendUpstreamAgentApiText").mockResolvedValue(undefined);
    (api.sendText as any).mockClear();

    sourceRegistry.registerWecomSourceSnapshot({
      accountId: "default",
      source: "agent-callback",
      sessionKey: "agent:test-agent-blue:wecom:blue:direct:zhangsan",
      peerKind: "direct",
      peerId: "zhangsan",
      upstreamCorpId: "corp-up",
    });

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          agent: {
            corpId: "corp-main",
            corpSecret: "secret-main",
            agentId: 1000002,
            token: "token-main",
            encodingAESKey: "aes-main",
            upstreamCorps: {
              partner: {
                corpId: "corp-up",
                agentId: 2000001,
              },
            },
          },
        },
      },
    };

    await wecomOutbound.sendText({
      cfg,
      accountId: "default",
      sessionKey: "agent:test-agent-blue:wecom:blue:direct:zhangsan",
      to: "wecom-agent:default:user:zhangsan",
      text: "hello upstream by snapshot",
    } as any);

    expect(upstreamSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        toUser: "zhangsan",
        text: "hello upstream by snapshot",
        upstreamAgent: expect.objectContaining({
          corpId: "corp-up",
          agentId: 2000001,
        }),
      }),
    );
    expect(api.sendText).not.toHaveBeenCalled();

    upstreamSpy.mockRestore();
  });

  it("routes plain agent media targets to upstream delivery when peer context carries upstream corp", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const api = await import("./transport/agent-api/core.js");
    const client = await import("./transport/agent-api/client.js");
    const upstreamUpload = await import("./transport/agent-api/upstream-media-upload.js");
    const contextStore = await import("./context-store.js");
    const upstreamSendSpy = vi.spyOn(client, "sendUpstreamAgentApiMedia").mockResolvedValue(undefined);
    const upstreamUploadSpy = vi
      .spyOn(upstreamUpload, "uploadUpstreamAgentApiMedia")
      .mockResolvedValue("media-up-1");
    (api.sendMedia as any).mockClear();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        arrayBuffer: async () => new Uint8Array([1, 2, 3]).buffer,
        headers: new Headers({ "content-type": "text/markdown" }),
      }),
    );

    contextStore.setPeerContext("default", "zhangsan", {
      peerKind: "direct",
      upstreamCorpId: "corp-up",
    });

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          agent: {
            corpId: "corp-main",
            corpSecret: "secret-main",
            agentId: 1000002,
            token: "token-main",
            encodingAESKey: "aes-main",
            upstreamCorps: {
              partner: {
                corpId: "corp-up",
                agentId: 2000001,
              },
            },
          },
        },
      },
    };

    await wecomOutbound.sendMedia({
      cfg,
      accountId: "default",
      to: "wecom-agent:default:user:zhangsan",
      text: "caption",
      mediaUrl: "https://example.com/file.md",
    } as any);

    expect(upstreamUploadSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        upstreamAgent: expect.objectContaining({
          corpId: "corp-up",
          agentId: 2000001,
        }),
        filename: "file.md",
      }),
    );
    expect(upstreamSendSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        toUser: "zhangsan",
        mediaId: "media-up-1",
        mediaType: "file",
        upstreamAgent: expect.objectContaining({
          corpId: "corp-up",
          agentId: 2000001,
        }),
      }),
    );
    expect(api.sendMedia).not.toHaveBeenCalled();

    upstreamSendSpy.mockRestore();
    upstreamUploadSpy.mockRestore();
  });

  it("uses account-scoped agent config in matrix mode", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const api = await import("./transport/agent-api/core.js");
    (api.sendText as any).mockResolvedValue(undefined);
    (api.sendText as any).mockClear();

    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          defaultAccount: "acct-a",
          accounts: {
            "acct-a": {
              enabled: true,
              agent: {
                corpId: "corp-a",
                corpSecret: "secret-a",
                agentId: 10001,
                token: "token-a",
                encodingAESKey: "aes-a",
              },
            },
            "acct-b": {
              enabled: true,
              agent: {
                corpId: "corp-b",
                corpSecret: "secret-b",
                agentId: 10002,
                token: "token-b",
                encodingAESKey: "aes-b",
              },
            },
          },
        },
      },
    };

    await wecomOutbound.sendText({
      cfg,
      accountId: "acct-b",
      to: "user:lisi",
      text: "hello b",
    } as any);
    expect(api.sendText).toHaveBeenCalledWith(
      expect.objectContaining({
        toUser: "lisi",
        agent: expect.objectContaining({
          accountId: "acct-b",
          agentId: 10002,
          corpId: "corp-b",
        }),
      }),
    );
  });

  it("rejects outbound when target account has matrix conflict", async () => {
    const { wecomOutbound } = await import("./outbound.js");
    const cfg = {
      channels: {
        wecom: {
          enabled: true,
          defaultAccount: "acct-a",
          accounts: {
            "acct-a": {
              enabled: true,
              agent: {
                corpId: "corp-shared",
                corpSecret: "secret-a",
                agentId: 10001,
                token: "token-a",
                encodingAESKey: "aes-a",
              },
            },
            "acct-b": {
              enabled: true,
              agent: {
                corpId: "corp-shared",
                corpSecret: "secret-b",
                agentId: 10001,
                token: "token-b",
                encodingAESKey: "aes-b",
              },
            },
          },
        },
      },
    };

    await expect(
      wecomOutbound.sendText({
        cfg,
        accountId: "acct-b",
        to: "user:lisi",
        text: "hello",
      } as any),
    ).rejects.toThrow(/duplicate wecom agent identity/i);
  });
});

// ── v2.8.19 — MEDIA: 字面量解析（修群里发 zip 失败事故）─────────────────────
describe("extractMediaDirectives", () => {
  it("returns empty when text is null/undefined/empty", () => {
    expect(extractMediaDirectives(null)).toEqual({ residualText: "", mediaPaths: [] });
    expect(extractMediaDirectives(undefined)).toEqual({ residualText: "", mediaPaths: [] });
    expect(extractMediaDirectives("")).toEqual({ residualText: "", mediaPaths: [] });
  });

  it("returns text unchanged when no MEDIA: directive", () => {
    const r = extractMediaDirectives("hello world\nfoo bar");
    expect(r).toEqual({ residualText: "hello world\nfoo bar", mediaPaths: [] });
  });

  it("extracts single absolute MEDIA: line and removes it from residualText", () => {
    const r = extractMediaDirectives("结果：\nMEDIA: /tmp/foo.zip\n请查收");
    expect(r.mediaPaths).toEqual(["/tmp/foo.zip"]);
    expect(r.residualText).toBe("结果：\n请查收");
  });

  it("expands ~/ to user home dir", () => {
    const r = extractMediaDirectives("MEDIA: ~/Downloads/report.pdf");
    expect(r.mediaPaths).toEqual([`${homedir()}/Downloads/report.pdf`]);
    expect(r.residualText).toBe("");
  });

  it("strips paired quotes around path", () => {
    const dq = extractMediaDirectives('MEDIA: "/tmp/has space.zip"');
    expect(dq.mediaPaths).toEqual(["/tmp/has space.zip"]);
    const sq = extractMediaDirectives("MEDIA: '/tmp/foo.pdf'");
    expect(sq.mediaPaths).toEqual(["/tmp/foo.pdf"]);
  });

  it("is case-insensitive on the MEDIA prefix", () => {
    expect(extractMediaDirectives("media: /tmp/a.png").mediaPaths).toEqual(["/tmp/a.png"]);
    expect(extractMediaDirectives("Media: /tmp/b.png").mediaPaths).toEqual(["/tmp/b.png"]);
    expect(extractMediaDirectives("MEDIA: /tmp/c.png").mediaPaths).toEqual(["/tmp/c.png"]);
  });

  it("collects multiple MEDIA: lines in order, preserves rest", () => {
    const txt = [
      "三个文件如下：",
      "MEDIA: /tmp/1.zip",
      "中间有说明",
      "MEDIA: ~/2.pdf",
      "MEDIA: /tmp/3.png",
      "末尾备注",
    ].join("\n");
    const r = extractMediaDirectives(txt);
    expect(r.mediaPaths).toEqual([
      "/tmp/1.zip",
      `${homedir()}/2.pdf`,
      "/tmp/3.png",
    ]);
    expect(r.residualText).toBe("三个文件如下：\n中间有说明\n末尾备注");
  });

  it("ignores MEDIA: when not on its own line (in-line text safe)", () => {
    // 'MEDIA:' 出现在普通文本中部不应被抽走，避免误伤
    const r = extractMediaDirectives("说明：参数 MEDIA: foo 是干啥的？");
    expect(r.mediaPaths).toEqual([]);
    expect(r.residualText).toBe("说明：参数 MEDIA: foo 是干啥的？");
  });

  it("tolerates leading/trailing spaces around the directive line", () => {
    const r = extractMediaDirectives("   MEDIA:   /tmp/a.png   ");
    expect(r.mediaPaths).toEqual(["/tmp/a.png"]);
  });

  it("skips empty path after MEDIA:", () => {
    const r = extractMediaDirectives("MEDIA:   \n正文");
    expect(r.mediaPaths).toEqual([]);
    // 空 MEDIA: 行也算被过滤掉
    expect(r.residualText).toBe("正文");
  });
});
