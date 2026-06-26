/**
 * Unit tests for ZulipClient.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { ZulipClient, ZulipApiRequestError } from "./client.js";

const TEST_CONFIG = {
  realm: "https://test.zulipchat.com",
  email: "bot@test.zulipchat.com",
  apiKey: "test-api-key-1234",
  timeout: 5000,
};

function mockFetchResponse(data: unknown, status = 200, headers?: Record<string, string>) {
  return {
    status,
    headers: new Headers(headers),
    json: async () => data,
  } as Response;
}

describe("ZulipClient", () => {
  let client: ZulipClient;
  let fetchSpy: ReturnType<typeof vi.spyOn>;

  beforeEach(() => {
    client = new ZulipClient(TEST_CONFIG);
    fetchSpy = vi.spyOn(globalThis, "fetch");
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("getServerSettings", () => {
    it("calls /api/v1/server_settings without auth", async () => {
      fetchSpy.mockResolvedValueOnce(
        mockFetchResponse({
          result: "success",
          zulip_version: "10.0",
          zulip_feature_level: 300,
          push_notifications_enabled: true,
          require_email_format_usernames: true,
          authentication_methods: { password: true },
        }),
      );

      const settings = await client.getServerSettings();
      expect(settings.zulip_version).toBe("10.0");
      expect(settings.zulip_feature_level).toBe(300);

      const [url] = fetchSpy.mock.calls[0]!;
      expect(url).toBe("https://test.zulipchat.com/api/v1/server_settings");
    });
  });

  describe("getOwnUser", () => {
    it("returns bot user info", async () => {
      fetchSpy.mockResolvedValueOnce(
        mockFetchResponse({
          result: "success",
          user_id: 42,
          email: "bot@test.zulipchat.com",
          full_name: "Test Bot",
          is_bot: true,
        }),
      );

      const user = await client.getOwnUser();
      expect(user.user_id).toBe(42);
      expect(user.is_bot).toBe(true);
    });
  });

  describe("sendMessage", () => {
    it("sends a channel message", async () => {
      fetchSpy.mockResolvedValueOnce(mockFetchResponse({ result: "success", id: 100 }));

      const result = await client.sendMessage({
        type: "stream",
        to: "general",
        topic: "greetings",
        content: "Hello!",
      });
      expect(result.id).toBe(100);

      const [url, init] = fetchSpy.mock.calls[0]!;
      expect(url).toBe("https://test.zulipchat.com/api/v1/messages");
      const body = (init as RequestInit).body as URLSearchParams;
      expect(body.get("type")).toBe("stream");
      expect(body.get("to")).toBe("general");
      expect(body.get("topic")).toBe("greetings");
    });

    it("sends a DM with user ID array", async () => {
      fetchSpy.mockResolvedValueOnce(mockFetchResponse({ result: "success", id: 101 }));

      await client.sendMessage({
        type: "direct",
        to: [10, 20],
        content: "Hi there",
      });

      const body = (fetchSpy.mock.calls[0]![1] as RequestInit).body as URLSearchParams;
      expect(body.get("to")).toBe("[10,20]");
    });
  });

  describe("registerQueue", () => {
    it("registers with event types", async () => {
      fetchSpy.mockResolvedValueOnce(
        mockFetchResponse({
          result: "success",
          queue_id: "q-123",
          last_event_id: -1,
          idle_queue_timeout_secs: 600,
          max_message_length: 10000,
          max_topic_length: 60,
          max_file_upload_size_mib: 25,
          zulip_version: "10.0",
          zulip_feature_level: 300,
        }),
      );

      const reg = await client.registerQueue({
        event_types: ["message", "heartbeat"],
        apply_markdown: true,
      });
      expect(reg.queue_id).toBe("q-123");
      expect(reg.last_event_id).toBe(-1);
    });
  });

  describe("getEvents", () => {
    it("long-polls for events", async () => {
      fetchSpy.mockResolvedValueOnce(
        mockFetchResponse({
          result: "success",
          events: [
            { type: "heartbeat", id: 0 },
            {
              type: "message",
              id: 1,
              message: {
                id: 500,
                sender_id: 10,
                sender_email: "user@test.com",
                sender_full_name: "User",
                type: "stream",
                stream_id: 1,
                display_recipient: "general",
                subject: "hello",
                content: "Hi!",
                timestamp: 1700000000,
              },
              flags: [],
            },
          ],
        }),
      );

      const res = await client.getEvents("q-123", -1);
      expect(res.events).toHaveLength(2);
      expect(res.events[0].type).toBe("heartbeat");
      expect(res.events[1].type).toBe("message");
    });
  });

  describe("error handling", () => {
    it("throws ZulipApiRequestError on API error", async () => {
      fetchSpy.mockResolvedValue(
        mockFetchResponse({ result: "error", msg: "Invalid API key", code: "UNAUTHORIZED" }, 401),
      );

      await expect(client.getOwnUser()).rejects.toThrow(ZulipApiRequestError);
      await expect(client.getOwnUser()).rejects.toThrow("Invalid API key");
    });

    it("retries on 429 rate limit", async () => {
      fetchSpy
        .mockResolvedValueOnce(
          mockFetchResponse({ result: "error", msg: "Rate limited" }, 429, { "Retry-After": "0" }),
        )
        .mockResolvedValueOnce(
          mockFetchResponse({
            result: "success",
            user_id: 42,
            email: "bot@test.com",
            full_name: "Bot",
            is_bot: true,
          }),
        );

      const user = await client.getOwnUser();
      expect(user.user_id).toBe(42);
      expect(fetchSpy).toHaveBeenCalledTimes(2); // initial 429 + retry inside rawFetch
    });
  });

  describe("deleteQueue", () => {
    it("deletes an event queue", async () => {
      fetchSpy.mockResolvedValueOnce(mockFetchResponse({ result: "success" }));

      await expect(client.deleteQueue("q-123")).resolves.toBeUndefined();
      const [url, init] = fetchSpy.mock.calls[0]!;
      expect(url).toBe("https://test.zulipchat.com/api/v1/events");
      expect((init as RequestInit).method).toBe("DELETE");
    });
  });
});
