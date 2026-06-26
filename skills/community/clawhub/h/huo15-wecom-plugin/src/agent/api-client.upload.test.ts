import { beforeEach, describe, expect, it, vi } from "vitest";
import type { ResolvedAgentAccount } from "../types/index.js";

const { wecomFetchMock, resolveProxyMock } = vi.hoisted(() => ({
  wecomFetchMock: vi.fn(),
  resolveProxyMock: vi.fn(() => undefined),
}));

vi.mock("../http.js", () => ({
  wecomFetch: wecomFetchMock,
  readResponseBodyAsBuffer: vi.fn(),
}));

vi.mock("../config/index.js", () => ({
  resolveWecomEgressProxyUrlFromNetwork: resolveProxyMock,
}));

import { uploadMedia } from "../transport/agent-api/core.js";

function createAgent(agentId: number): ResolvedAgentAccount {
  return {
    accountId: `acct-${agentId}`,
    configured: true,
    corpId: "corp",
    corpSecret: "secret",
    agentId,
    token: "token",
    encodingAESKey: "aes",
    config: {} as any,
  };
}

function jsonResponse(body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

describe("wecom agent uploadMedia", () => {
  beforeEach(() => {
    wecomFetchMock.mockReset();
    resolveProxyMock.mockReset();
    resolveProxyMock.mockReturnValue(undefined);
  });

  it("uses text/plain for .txt uploads", async () => {
    wecomFetchMock.mockResolvedValueOnce(jsonResponse({ access_token: "token-1", expires_in: 7200 }));
    wecomFetchMock.mockResolvedValueOnce(jsonResponse({ errcode: 0, errmsg: "ok", media_id: "m-1" }));

    const mediaId = await uploadMedia({
      agent: createAgent(10001),
      type: "file",
      buffer: Buffer.from("hello txt"),
      filename: "note.txt",
    });

    expect(mediaId).toBe("m-1");
    const [, init] = wecomFetchMock.mock.calls[1] as [string, RequestInit];
    const body = init.body as Buffer;
    const bodyText = body.toString("utf8");
    expect(bodyText).toContain('filename="note.txt"');
    expect(bodyText).toContain("Content-Type: text/plain");
  });

  it("uses docx mime and normalizes non-ascii filename", async () => {
    wecomFetchMock.mockResolvedValueOnce(jsonResponse({ access_token: "token-2", expires_in: 7200 }));
    wecomFetchMock.mockResolvedValueOnce(jsonResponse({ errcode: 0, errmsg: "ok", media_id: "m-2" }));

    const mediaId = await uploadMedia({
      agent: createAgent(10002),
      type: "file",
      buffer: Buffer.from("docx bytes"),
      filename: "需求文档.docx",
    });

    expect(mediaId).toBe("m-2");
    const [, init] = wecomFetchMock.mock.calls[1] as [string, RequestInit];
    const body = init.body as Buffer;
    const bodyText = body.toString("utf8");
    expect(bodyText).toContain('filename="file.docx"');
    expect(bodyText).toContain(
      "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    );
  });

  it("retries with octet-stream when preferred mime upload fails", async () => {
    wecomFetchMock.mockResolvedValueOnce(jsonResponse({ access_token: "token-3", expires_in: 7200 }));
    wecomFetchMock.mockResolvedValueOnce(jsonResponse({ errcode: 40005, errmsg: "invalid media type" }));
    wecomFetchMock.mockResolvedValueOnce(jsonResponse({ errcode: 0, errmsg: "ok", media_id: "m-3" }));

    const mediaId = await uploadMedia({
      agent: createAgent(10003),
      type: "file",
      buffer: Buffer.from("yaml bytes"),
      filename: "config.yaml",
    });

    expect(mediaId).toBe("m-3");
    expect(wecomFetchMock).toHaveBeenCalledTimes(3);

    const [, firstUploadInit] = wecomFetchMock.mock.calls[1] as [string, RequestInit];
    const [, retryUploadInit] = wecomFetchMock.mock.calls[2] as [string, RequestInit];
    const firstUploadBody = (firstUploadInit.body as Buffer).toString("utf8");
    const retryUploadBody = (retryUploadInit.body as Buffer).toString("utf8");
    expect(firstUploadBody).toContain("Content-Type: application/yaml");
    expect(retryUploadBody).toContain("Content-Type: application/octet-stream");
  });
});
