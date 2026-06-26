/**
 * Zulip gateway — event queue long-polling for real-time message reception.
 *
 * Lifecycle:
 * 1. POST /register → get queue_id + last_event_id
 * 2. Loop: GET /events (blocking) → yield message events
 * 3. On BAD_EVENT_QUEUE_ID → re-register
 * 4. On stopAccount → DELETE /events
 */

import { ZulipClient, ZulipApiRequestError } from "./client.js";
import type { ZulipClientConfig, MessageEvent, UpdateMessageEvent } from "./types.js";

export interface GatewayCallbacks {
  onMessage: (event: MessageEvent) => void | Promise<void>;
  onTopicRename?: (streamId: number, oldTopic: string, newTopic: string) => void | Promise<void>;
  onError?: (error: unknown) => void;
  onConnected?: (info: { queueId: string; zulipVersion: string }) => void;
  onReconnect?: () => void;
  log?: (message: string) => void;
}

export interface GatewayHandle {
  /** Stop the gateway loop and clean up the event queue. */
  stop(): Promise<void>;
}

/**
 * Start long-polling for Zulip events.
 *
 * Returns a handle with a `stop()` method.
 */
export function startZulipGateway(
  config: ZulipClientConfig,
  callbacks: GatewayCallbacks,
  opts?: { ownUserId?: number; abortSignal?: AbortSignal },
): GatewayHandle {
  const client = new ZulipClient(config);
  let running = true;
  let currentQueueId: string | undefined;

  const loop = (async () => {
    let consecutiveErrors = 0;

    while (running && !opts?.abortSignal?.aborted) {
      try {
        // Register event queue
        const reg = await client.registerQueue({
          event_types: ["message", "heartbeat", "update_message"],
          apply_markdown: true,
          all_public_streams: false,
        });
        currentQueueId = reg.queue_id;
        let lastEventId = reg.last_event_id;

        callbacks.onConnected?.({
          queueId: reg.queue_id,
          zulipVersion: reg.zulip_version,
        });

        // Reset backoff on successful connection
        consecutiveErrors = 0;

        // Poll loop
        while (running && !opts?.abortSignal?.aborted) {
          const events = await client.getEvents(reg.queue_id, lastEventId);

          for (const event of events.events) {
            if (event.id > lastEventId) {
              lastEventId = event.id;
            }

            if (event.type === "message") {
              const msgEvent = event;
              // Skip own messages
              if (opts?.ownUserId != null && msgEvent.message.sender_id === opts.ownUserId) {
                continue;
              }
              try {
                await callbacks.onMessage(msgEvent);
              } catch (err) {
                callbacks.onError?.(err);
              }
            }
            // heartbeat events just advance lastEventId

            if (event.type === "update_message") {
              const ume = event;
              if (
                ume.orig_subject != null &&
                ume.subject != null &&
                ume.orig_subject !== ume.subject &&
                ume.stream_id != null
              ) {
                try {
                  await callbacks.onTopicRename?.(ume.stream_id, ume.orig_subject, ume.subject);
                } catch (err) {
                  callbacks.onError?.(err);
                }
              }
            }
          }
        }
      } catch (err) {
        if (!running || opts?.abortSignal?.aborted) {
          break;
        }

        // Best-effort cleanup of stale queue before re-registering
        if (currentQueueId) {
          try {
            await client.deleteQueue(currentQueueId);
          } catch {
            // Ignore — queue may already be gone
          }
          currentQueueId = undefined;
        }

        if (err instanceof ZulipApiRequestError && err.code === "BAD_EVENT_QUEUE_ID") {
          callbacks.log?.("zulip: event queue expired, re-registering...");
          callbacks.onReconnect?.();
          continue;
        }

        // Exponential backoff with jitter (cap at 5 minutes)
        const isRateLimit =
          err instanceof ZulipApiRequestError &&
          String(err.message).includes("rate limit");
        const baseDelay = isRateLimit ? 30_000 : 5_000;
        const backoffDelay = Math.min(
          baseDelay * 2 ** consecutiveErrors,
          300_000,
        );
        const jitter = Math.random() * 5_000;
        const delay = backoffDelay + jitter;
        consecutiveErrors++;

        callbacks.onError?.(err);
        callbacks.log?.(
          `zulip: gateway error, retrying in ${Math.round(delay / 1000)}s (attempt ${consecutiveErrors}): ${String(err)}`,
        );
        await new Promise((r) => setTimeout(r, delay));
      }
    }
  })();

  return {
    async stop() {
      running = false;
      if (currentQueueId) {
        try {
          await client.deleteQueue(currentQueueId);
        } catch {
          // Best-effort cleanup
        }
        currentQueueId = undefined;
      }
      await loop.catch(() => {});
    },
  };
}
