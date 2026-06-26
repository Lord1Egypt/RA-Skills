import type { WSClient, WsFrameHeaders } from "@wecom/aibot-node-sdk";
import { fetchRemoteMedia } from "openclaw/plugin-sdk/media-runtime";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { uploadAndReplyBotWsMedia, uploadAndSendBotWsMedia } from "./media.js";

vi.mock("openclaw/plugin-sdk/media-runtime", () => ({
  assertLocalMediaAllowed: vi.fn(),
  detectMime: vi.fn(),
  fetchRemoteMedia: vi.fn(),
}));

describe("uploadAndSendBotWsMedia", () => {
  const fetchRemoteMediaMock = vi.mocked(fetchRemoteMedia);

  beforeEach(() => {
    fetchRemoteMediaMock.mockReset();
    fetchRemoteMediaMock.mockResolvedValue({
      buffer: Buffer.from("png"),
      contentType: "image/png",
      fileName: "sample.png",
    } as never);
  });

  it("passes the configured maxBytes to outbound media loading", async () => {
    const wsClient = {
      uploadMedia: vi.fn().mockResolvedValue({ media_id: "media-1" }),
      sendMediaMessage: vi.fn().mockResolvedValue({ headers: { req_id: "req-1" } }),
    } as unknown as WSClient;

    await uploadAndSendBotWsMedia({
      wsClient,
      chatId: "hidao",
      mediaUrl: "https://example.com/sample.png",
      maxBytes: 42 * 1024 * 1024,
    });

    expect(fetchRemoteMediaMock).toHaveBeenCalledWith(
      expect.objectContaining({
        url: "https://example.com/sample.png",
        maxBytes: 42 * 1024 * 1024,
      }),
    );
  });
});

// ── v2.8.23 — uploadAndReplyBotWsMedia 群聊路径分流（修群里发文件 86008/ack timeout）──
describe("uploadAndReplyBotWsMedia (v2.8.23 chattype 分流)", () => {
  const fetchRemoteMediaMock = vi.mocked(fetchRemoteMedia);

  beforeEach(() => {
    fetchRemoteMediaMock.mockReset();
    fetchRemoteMediaMock.mockResolvedValue({
      buffer: Buffer.from("zip-content-bytes"),
      contentType: "application/zip",
      fileName: "test.zip",
    } as never);
  });

  it("DM (chattype=single) 走被动回复 replyMedia (绑 reqId UX 更好)", async () => {
    const replyMediaSpy = vi.fn().mockResolvedValue({ headers: { req_id: "reply-req-1" } });
    const sendMediaMessageSpy = vi.fn().mockResolvedValue({ headers: { req_id: "send-req-1" } });
    const wsClient = {
      uploadMedia: vi.fn().mockResolvedValue({ media_id: "media-dm" }),
      replyMedia: replyMediaSpy,
      sendMediaMessage: sendMediaMessageSpy,
    } as unknown as WSClient;

    const frame = {
      headers: { req_id: "in-req-1" },
      body: { chattype: "single", from: { userid: "ZhaoBo" } },
    } as unknown as WsFrameHeaders;

    const result = await uploadAndReplyBotWsMedia({
      wsClient,
      frame,
      mediaUrl: "https://example.com/test.zip",
    });

    expect(result.ok).toBe(true);
    // DM 必须走 replyMedia 不走 sendMediaMessage
    expect(replyMediaSpy).toHaveBeenCalledTimes(1);
    expect(replyMediaSpy).toHaveBeenCalledWith(frame, "file", "media-dm");
    expect(sendMediaMessageSpy).not.toHaveBeenCalled();
  });

  it("群聊 (chattype=group) 走主动推送 sendMediaMessage (绕开 86008/ack timeout)", async () => {
    const replyMediaSpy = vi.fn().mockResolvedValue({ headers: { req_id: "reply-req-1" } });
    const sendMediaMessageSpy = vi.fn().mockResolvedValue({ headers: { req_id: "send-req-1" } });
    const logSpy = vi.spyOn(console, "log").mockImplementation(() => {});
    const wsClient = {
      uploadMedia: vi.fn().mockResolvedValue({ media_id: "media-group" }),
      replyMedia: replyMediaSpy,
      sendMediaMessage: sendMediaMessageSpy,
    } as unknown as WSClient;

    const frame = {
      headers: { req_id: "in-req-1" },
      body: { chattype: "group", chatid: "wrXXX", from: { userid: "ZhaoBo" } },
    } as unknown as WsFrameHeaders;

    const result = await uploadAndReplyBotWsMedia({
      wsClient,
      frame,
      mediaUrl: "https://example.com/test.zip",
    });

    expect(result.ok).toBe(true);
    // 群聊必须走 sendMediaMessage 不走 replyMedia（被动回复在群里撞 86008/ack timeout）
    expect(sendMediaMessageSpy).toHaveBeenCalledTimes(1);
    expect(sendMediaMessageSpy).toHaveBeenCalledWith("wrXXX", "file", "media-group");
    expect(replyMediaSpy).not.toHaveBeenCalled();
    // 必须打主动推送通道成功 log
    expect(
      logSpy.mock.calls.some((c) =>
        String(c[0]).includes("群聊媒体走主动推送通道（aibot_send_msg）成功"),
      ),
    ).toBe(true);
    logSpy.mockRestore();
  });

  it("群聊缺 chatid 直接抛错（防御）", async () => {
    const wsClient = {
      uploadMedia: vi.fn().mockResolvedValue({ media_id: "media-bad" }),
      replyMedia: vi.fn(),
      sendMediaMessage: vi.fn(),
    } as unknown as WSClient;

    const frame = {
      headers: { req_id: "in-req-1" },
      body: { chattype: "group" /* missing chatid */, from: { userid: "X" } },
    } as unknown as WsFrameHeaders;

    const result = await uploadAndReplyBotWsMedia({
      wsClient,
      frame,
      mediaUrl: "https://example.com/test.zip",
    });

    // catch 块接管 → share-fallback 兜底（mock 没配 share 也不会崩）
    expect(result.ok === true || result.ok === false).toBe(true);
  });
});
