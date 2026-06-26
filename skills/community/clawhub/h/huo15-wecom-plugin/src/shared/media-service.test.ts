import { beforeEach, describe, expect, it, vi } from "vitest";
import { WecomMediaService } from "./media-service.js";

describe("WecomMediaService", () => {
  const fetchRemoteMedia = vi.fn();
  const saveMediaBuffer = vi.fn();

  beforeEach(() => {
    fetchRemoteMedia.mockReset();
    saveMediaBuffer.mockReset();
  });

  it("passes configured wecom mediaMaxMb to remote attachment fetches and saves", async () => {
    const service = new WecomMediaService(
      {
        channel: {
          media: {
            fetchRemoteMedia,
            saveMediaBuffer,
          },
        },
      } as never,
      {
        channels: {
          wecom: {
            mediaMaxMb: 24,
          },
        },
      } as never,
    );

    fetchRemoteMedia.mockResolvedValue({
      buffer: Buffer.from("file"),
      contentType: "application/pdf",
      fileName: "sample.pdf",
    });
    saveMediaBuffer.mockResolvedValue({
      path: "/tmp/sample.pdf",
    });

    const event = {
      accountId: "default",
      attachments: [{ remoteUrl: "https://example.com/sample.pdf" }],
    } as never;

    const attachment = await service.normalizeFirstAttachment(event);

    expect(fetchRemoteMedia).toHaveBeenCalledWith({
      url: "https://example.com/sample.pdf",
      maxBytes: 24 * 1024 * 1024,
    });

    await service.saveInboundAttachment(event, attachment!);

    expect(saveMediaBuffer).toHaveBeenCalledWith(
      expect.any(Buffer),
      "application/pdf",
      "inbound",
      24 * 1024 * 1024,
      "sample.pdf",
    );
  });

  it("prefers account-specific mediaMaxMb for inbound saves", async () => {
    const service = new WecomMediaService(
      {
        channel: {
          media: {
            fetchRemoteMedia,
            saveMediaBuffer,
          },
        },
      } as never,
      {
        channels: {
          wecom: {
            mediaMaxMb: 24,
            accounts: {
              ops: {
                mediaMaxMb: 36,
              },
            },
          },
        },
      } as never,
    );

    saveMediaBuffer.mockResolvedValue({
      path: "/tmp/account-specific.pdf",
    });

    await service.saveInboundAttachment(
      {
        accountId: "ops",
      } as never,
      {
        buffer: Buffer.from("file"),
        contentType: "application/pdf",
        filename: "ops.pdf",
      },
    );

    expect(saveMediaBuffer).toHaveBeenCalledWith(
      expect.any(Buffer),
      "application/pdf",
      "inbound",
      36 * 1024 * 1024,
      "ops.pdf",
    );
  });
});
