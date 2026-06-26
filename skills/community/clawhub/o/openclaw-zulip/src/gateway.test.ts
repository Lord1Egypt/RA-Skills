import { describe, it, expect, vi, afterEach, beforeEach } from "vitest";
import { startZulipGateway } from "./gateway.js";
import type { GatewayCallbacks } from "./gateway.js";

const TEST_CONFIG = {
  realm: "https://test.zulipchat.com",
  email: "bot@test.zulipchat.com",
  apiKey: "test-key",
};

function mockFetchResponse(data: unknown, status = 200) {
  return {
    status,
    headers: new Headers(),
    json: async () => data,
  } as Response;
}

describe("startZulipGateway", () => {
  let fetchSpy: ReturnType<typeof vi.spyOn>;

  beforeEach(() => {
    fetchSpy = vi.spyOn(globalThis, "fetch");
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("registers queue and dispatches message events", async () => {
    const messages: unknown[] = [];
    let connectedInfo: unknown;
    const ac = new AbortController();

    // registerQueue response
    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        queue_id: "q-1",
        last_event_id: -1,
        zulip_version: "10.0",
        zulip_feature_level: 300,
        idle_queue_timeout_secs: 600,
        max_message_length: 10000,
        max_topic_length: 60,
        max_file_upload_size_mib: 25,
      }),
    );

    // getEvents response with a message
    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        events: [
          {
            type: "message",
            id: 0,
            message: {
              id: 100,
              sender_id: 10,
              sender_email: "user@test.com",
              sender_full_name: "User",
              type: "stream",
              stream_id: 1,
              display_recipient: "general",
              subject: "test",
              content: "hello",
              timestamp: 1700000000,
            },
            flags: [],
          },
        ],
      }),
    );

    // Next getEvents — abort to stop the loop
    fetchSpy.mockImplementation(async () => {
      ac.abort();
      return mockFetchResponse({ result: "success", events: [] });
    });

    const callbacks: GatewayCallbacks = {
      onMessage: (event) => {
        messages.push(event);
      },
      onConnected: (info) => {
        connectedInfo = info;
      },
    };

    const handle = startZulipGateway(TEST_CONFIG, callbacks, {
      abortSignal: ac.signal,
    });

    // Wait for the loop to process
    await new Promise((r) => setTimeout(r, 100));
    await handle.stop();

    expect(connectedInfo).toEqual({ queueId: "q-1", zulipVersion: "10.0" });
    expect(messages).toHaveLength(1);
    expect((messages[0] as any).message.content).toBe("hello");
  });

  it("skips own messages when ownUserId is set", async () => {
    const messages: unknown[] = [];
    const ac = new AbortController();

    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        queue_id: "q-2",
        last_event_id: -1,
        zulip_version: "10.0",
        zulip_feature_level: 300,
        idle_queue_timeout_secs: 600,
        max_message_length: 10000,
        max_topic_length: 60,
        max_file_upload_size_mib: 25,
      }),
    );

    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        events: [
          {
            type: "message",
            id: 0,
            message: {
              id: 200,
              sender_id: 42, // own user
              sender_email: "bot@test.com",
              sender_full_name: "Bot",
              type: "stream",
              stream_id: 1,
              display_recipient: "general",
              subject: "test",
              content: "my own msg",
              timestamp: 1700000000,
            },
            flags: [],
          },
        ],
      }),
    );

    fetchSpy.mockImplementation(async () => {
      ac.abort();
      return mockFetchResponse({ result: "success", events: [] });
    });

    const handle = startZulipGateway(
      TEST_CONFIG,
      {
        onMessage: (e) => {
          messages.push(e);
        },
      },
      { ownUserId: 42, abortSignal: ac.signal },
    );

    await new Promise((r) => setTimeout(r, 100));
    await handle.stop();

    expect(messages).toHaveLength(0);
  });

  it("reconnects on BAD_EVENT_QUEUE_ID", async () => {
    const reconnects: boolean[] = [];
    const ac = new AbortController();

    // First registerQueue
    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        queue_id: "q-old",
        last_event_id: -1,
        zulip_version: "10.0",
        zulip_feature_level: 300,
        idle_queue_timeout_secs: 600,
        max_message_length: 10000,
        max_topic_length: 60,
        max_file_upload_size_mib: 25,
      }),
    );

    // getEvents returns BAD_EVENT_QUEUE_ID
    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse(
        { result: "error", msg: "Bad event queue id", code: "BAD_EVENT_QUEUE_ID" },
        400,
      ),
    );

    // Second registerQueue after reconnect
    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        queue_id: "q-new",
        last_event_id: -1,
        zulip_version: "10.0",
        zulip_feature_level: 300,
        idle_queue_timeout_secs: 600,
        max_message_length: 10000,
        max_topic_length: 60,
        max_file_upload_size_mib: 25,
      }),
    );

    // Abort after reconnect
    fetchSpy.mockImplementation(async () => {
      ac.abort();
      return mockFetchResponse({ result: "success", events: [] });
    });

    const handle = startZulipGateway(
      TEST_CONFIG,
      {
        onMessage: () => {},
        onReconnect: () => reconnects.push(true),
      },
      { abortSignal: ac.signal },
    );

    await new Promise((r) => setTimeout(r, 200));
    await handle.stop();

    expect(reconnects).toHaveLength(1);
  });

  it("dispatches onTopicRename for update_message with subject change", async () => {
    const renames: { streamId: number; oldTopic: string; newTopic: string }[] = [];
    const ac = new AbortController();

    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        queue_id: "q-3",
        last_event_id: -1,
        zulip_version: "10.0",
        zulip_feature_level: 300,
        idle_queue_timeout_secs: 600,
        max_message_length: 10000,
        max_topic_length: 60,
        max_file_upload_size_mib: 25,
      }),
    );

    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        events: [
          {
            type: "update_message",
            id: 0,
            message_id: 500,
            stream_id: 7,
            orig_subject: "🔴 login bug",
            subject: "🟡 login bug",
            propagate_mode: "change_all",
          },
        ],
      }),
    );

    fetchSpy.mockImplementation(async () => {
      ac.abort();
      return mockFetchResponse({ result: "success", events: [] });
    });

    const handle = startZulipGateway(
      TEST_CONFIG,
      {
        onMessage: () => {},
        onTopicRename: (streamId, oldTopic, newTopic) => {
          renames.push({ streamId, oldTopic, newTopic });
        },
      },
      { abortSignal: ac.signal },
    );

    await new Promise((r) => setTimeout(r, 100));
    await handle.stop();

    expect(renames).toHaveLength(1);
    expect(renames[0]).toEqual({
      streamId: 7,
      oldTopic: "🔴 login bug",
      newTopic: "🟡 login bug",
    });
  });

  it("ignores update_message when subject did not change", async () => {
    const renames: unknown[] = [];
    const ac = new AbortController();

    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        queue_id: "q-4",
        last_event_id: -1,
        zulip_version: "10.0",
        zulip_feature_level: 300,
        idle_queue_timeout_secs: 600,
        max_message_length: 10000,
        max_topic_length: 60,
        max_file_upload_size_mib: 25,
      }),
    );

    fetchSpy.mockResolvedValueOnce(
      mockFetchResponse({
        result: "success",
        events: [
          {
            type: "update_message",
            id: 0,
            message_id: 501,
            stream_id: 7,
            // content-only edit, no subject fields
          },
        ],
      }),
    );

    fetchSpy.mockImplementation(async () => {
      ac.abort();
      return mockFetchResponse({ result: "success", events: [] });
    });

    const handle = startZulipGateway(
      TEST_CONFIG,
      {
        onMessage: () => {},
        onTopicRename: () => {
          renames.push(true);
        },
      },
      { abortSignal: ac.signal },
    );

    await new Promise((r) => setTimeout(r, 100));
    await handle.stop();

    expect(renames).toHaveLength(0);
  });
});
