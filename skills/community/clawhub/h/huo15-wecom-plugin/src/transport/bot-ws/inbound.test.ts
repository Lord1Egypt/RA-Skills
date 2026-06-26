import { describe, expect, it } from "vitest";

import { mapBotWsFrameToInboundEvent } from "./inbound.js";
import type { ResolvedBotAccount } from "../../types/index.js";

function createBotAccount(): ResolvedBotAccount {
  return {
    accountId: "haidao",
    configured: true,
    primaryTransport: "ws",
    wsConfigured: true,
    webhookConfigured: false,
    config: {},
    ws: {
      botId: "bot-id",
      secret: "secret",
    },
    token: "",
    encodingAESKey: "",
    receiveId: "",
    botId: "bot-id",
    secret: "secret",
  };
}

describe("mapBotWsFrameToInboundEvent", () => {
  it("includes quote content in text events", () => {
    const event = mapBotWsFrameToInboundEvent({
      account: createBotAccount(),
      frame: {
        cmd: "aibot_msg_callback",
        headers: { req_id: "req-1" },
        body: {
          msgid: "msg-1",
          msgtype: "text",
          chattype: "group",
          chatid: "group-1",
          from: { userid: "user-1" },
          text: { content: "@daodao 这个线索价值" },
          quote: {
            msgtype: "text",
            text: { content: "原始引用内容" },
          },
        },
      },
    });

    expect(event.text).toBe("@daodao 这个线索价值\n\n> 原始引用内容");
  });

  it("extracts attachments from mixed events", () => {
    const event = mapBotWsFrameToInboundEvent({
      account: createBotAccount(),
      frame: {
        cmd: "aibot_msg_callback",
        headers: { req_id: "req-2" },
        body: {
          msgid: "msg-2",
          msgtype: "mixed",
          chattype: "group",
          chatid: "group-2",
          from: { userid: "user-2" },
          mixed: {
            msg_item: [
              {
                msgtype: "text",
                text: { content: "来看看这张图" },
              },
              {
                msgtype: "image",
                image: { url: "https://example.com/image.jpg", aeskey: "mock-aes-key" },
              },
              {
                msgtype: "file",
                file: { url: "https://example.com/doc.pdf", aeskey: "mock-file-key" },
              },
              {
                msgtype: "video",
                video: { url: "https://example.com/demo.mp4", aeskey: "mock-video-key" },
              },
            ],
          },
        },
      },
    });

    expect(event.attachments).toBeDefined();
    expect(event.attachments).toHaveLength(3);
    expect(event.attachments![0]).toEqual({
      name: "image",
      remoteUrl: "https://example.com/image.jpg",
      aesKey: "mock-aes-key",
    });
    expect(event.attachments![1]).toEqual({
      name: "file",
      remoteUrl: "https://example.com/doc.pdf",
      aesKey: "mock-file-key",
    });
    expect(event.attachments![2]).toEqual({
      name: "video",
      remoteUrl: "https://example.com/demo.mp4",
      aesKey: "mock-video-key",
    });
  });

  it("extracts attachment from quote file in text events", () => {
    const event = mapBotWsFrameToInboundEvent({
      account: createBotAccount(),
      frame: {
        cmd: "aibot_msg_callback",
        headers: { req_id: "req-3" },
        body: {
          msgid: "msg-3",
          msgtype: "text",
          chattype: "single",
          from: { userid: "user-3" },
          text: { content: "请读取这个引用文件" },
          quote: {
            msgtype: "file",
            file: { url: "https://example.com/quoted.pdf", aeskey: "quoted-file-key" },
          },
        },
      },
    });

    expect(event.inboundKind).toBe("text");
    expect(event.attachments).toEqual([
      {
        name: "file",
        remoteUrl: "https://example.com/quoted.pdf",
        aesKey: "quoted-file-key",
      },
    ]);
  });

  it("maps top-level video to video inbound kind and attachment", () => {
    const event = mapBotWsFrameToInboundEvent({
      account: createBotAccount(),
      frame: {
        cmd: "aibot_msg_callback",
        headers: { req_id: "req-4" },
        body: {
          msgid: "msg-4",
          msgtype: "video",
          chattype: "single",
          from: { userid: "user-4" },
          video: { url: "https://example.com/top-video.mp4", aeskey: "top-video-key" },
        },
      },
    });

    expect(event.inboundKind).toBe("video");
    expect(event.attachments).toEqual([
      {
        name: "video",
        remoteUrl: "https://example.com/top-video.mp4",
        aesKey: "top-video-key",
      },
    ]);
  });

  it("extracts attachment from quote image in text events", () => {
    const event = mapBotWsFrameToInboundEvent({
      account: createBotAccount(),
      frame: {
        cmd: "aibot_msg_callback",
        headers: { req_id: "req-5" },
        body: {
          msgid: "msg-5",
          msgtype: "text",
          chattype: "single",
          from: { userid: "user-5" },
          text: { content: "请看这张引用图片" },
          quote: {
            msgtype: "image",
            image: { url: "https://example.com/quoted.jpg", aeskey: "quoted-image-key" },
          },
        },
      },
    });

    expect(event.inboundKind).toBe("text");
    expect(event.attachments).toEqual([
      {
        name: "image",
        remoteUrl: "https://example.com/quoted.jpg",
        aesKey: "quoted-image-key",
      },
    ]);
  });

  it("extracts attachment from quote video in text events", () => {
    const event = mapBotWsFrameToInboundEvent({
      account: createBotAccount(),
      frame: {
        cmd: "aibot_msg_callback",
        headers: { req_id: "req-6" },
        body: {
          msgid: "msg-6",
          msgtype: "voice",
          chattype: "single",
          from: { userid: "user-6" },
          voice: { content: "语音转写内容" },
          quote: {
            msgtype: "video",
            video: { url: "https://example.com/quoted.mp4", aeskey: "quoted-video-key" },
          },
        },
      },
    });

    expect(event.inboundKind).toBe("voice");
    expect(event.attachments).toEqual([
      {
        name: "video",
        remoteUrl: "https://example.com/quoted.mp4",
        aesKey: "quoted-video-key",
      },
    ]);
  });

  it("prioritizes top-level media over quote media in WS events", () => {
    const event = mapBotWsFrameToInboundEvent({
      account: createBotAccount(),
      frame: {
        cmd: "aibot_msg_callback",
        headers: { req_id: "req-7" },
        body: {
          msgid: "msg-7",
          msgtype: "image",
          chattype: "group",
          chatid: "group-7",
          from: { userid: "user-7" },
          image: { url: "https://example.com/top.jpg", aeskey: "top-image-key" },
          quote: {
            msgtype: "file",
            file: { url: "https://example.com/quoted.pdf", aeskey: "quoted-file-key" },
          },
        },
      },
    });

    // Should only include top-level image, not quote file
    expect(event.inboundKind).toBe("image");
    expect(event.attachments).toEqual([
      {
        name: "image",
        remoteUrl: "https://example.com/top.jpg",
        aesKey: "top-image-key",
      },
    ]);
  });

  it("extracts all images from quote.mixed in text events", () => {
    const event = mapBotWsFrameToInboundEvent({
      account: createBotAccount(),
      frame: {
        cmd: "aibot_msg_callback",
        headers: { req_id: "req-8" },
        body: {
          msgid: "msg-8",
          msgtype: "text",
          chattype: "single",
          from: { userid: "user-8" },
          text: { content: "这个引用有图文内容" },
          quote: {
            msgtype: "mixed",
            mixed: {
              msg_item: [
                { msgtype: "text", text: { content: "一些文本" } },
                { msgtype: "image", image: { url: "https://example.com/mixed-img1.jpg", aeskey: "mixed-key-1" } },
                { msgtype: "image", image: { url: "https://example.com/mixed-img2.jpg", aeskey: "mixed-key-2" } },
              ],
            },
          },
        },
      },
    });

    expect(event.inboundKind).toBe("text");
    // v2.8.8 — quote.mixed 现在提取全部 image/file/video（之前只取首张以"和 webhook 对齐"）
    expect(event.attachments).toEqual([
      {
        name: "image",
        remoteUrl: "https://example.com/mixed-img1.jpg",
        aesKey: "mixed-key-1",
      },
      {
        name: "image",
        remoteUrl: "https://example.com/mixed-img2.jpg",
        aesKey: "mixed-key-2",
      },
    ]);
  });
});
