// ~/.openclaw/extensions/openclaw-interaction-bridge/index.ts
// OpenClaw Interaction Bridge Plugin
// - Sends agent state updates directly to snarling (processing/speaking/idle)
// - Registers approval callback HTTP route for snarling button responses
// - Exposes /approval-callback and /approval/stats HTTP endpoints

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";
import { requestUserApproval, resumeApprovalFlow, resumeNotificationFlow, sendNotificationWithFeedback, forceClearApprovalLock, approvalStats, notificationStats } from "./approval_tool";

const SNARLING_URL = "http://localhost:5000/state";
const CALLBACK_BASE_URL = "http://localhost:18789";
const APPROVAL_SECRET = process.env.OPENCLAW_APPROVAL_SECRET || crypto.randomUUID();
let idleTimeout: ReturnType<typeof setTimeout> | null = null;
const IDLE_DELAY_MS = 10000; // 10 seconds of no activity = go idle
let lastState = ""; // Track last state sent to avoid duplicates

// Track if HTTP route is registered (only register once)
let routeRegistered = false;

// Map OpenClaw agent states to snarling states
function mapToSnarlingState(status: string): string {
  switch (status) {
    case "processing":
    case "speaking":
      return "processing";
    case "idle":
      return "sleeping";
    default:
      return "sleeping";
  }
}

async function updateState(status: string, sessionId: string) {
  try {
    // Map to snarling state
    const isCommunicating = status === "speaking";
    const stateToSend = isCommunicating ? "communicating" : mapToSnarlingState(status);

    // Only send if state changed (avoid flooding)
    if (stateToSend === lastState) {
      // State unchanged, just reset the idle timer
      if (idleTimeout) clearTimeout(idleTimeout);
      idleTimeout = setTimeout(() => {
        lastState = "";
        void fetch(SNARLING_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ state: "sleeping", timestamp: Date.now() })
        });
        idleTimeout = null;
      }, IDLE_DELAY_MS);
      return;
    }

    lastState = stateToSend;

    // Clear existing idle timer
    if (idleTimeout) clearTimeout(idleTimeout);
    idleTimeout = null;

    void fetch(SNARLING_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state: stateToSend, timestamp: Date.now() })
    });

    // Set idle timeout — after no new activity, go to sleeping
    if (status === "processing" || status === "speaking") {
      idleTimeout = setTimeout(() => {
        lastState = "";
        void fetch(SNARLING_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ state: "sleeping", timestamp: Date.now() })
        });
        idleTimeout = null;
      }, IDLE_DELAY_MS);
    }
  } catch (_e) {
    // Silent fail - snarling is optional
  }
}

export default definePluginEntry({
  id: "openclaw-interaction-bridge",
  name: "OpenClaw Interaction Bridge",
  description: "Bridge OpenClaw agent state directly to snarling display via HTTP API",
  register(api: any) {
    // State monitoring hooks - track when agent is processing or speaking
    api.on("before_tool_call", (event: any) => {
      const sessionKey = event.sessionKey || event.ctx?.sessionKey || "unknown";
      updateState("processing", sessionKey);
    });

    api.on("before_agent_reply", (event: any) => {
      const sessionKey = event.sessionKey || event.ctx?.sessionKey || "unknown";
      updateState("speaking", sessionKey);
    });

    api.on("agent_end", (event: any) => {
      // Agent finished its turn — go idle immediately
      lastState = "";
      void fetch(SNARLING_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: "sleeping", timestamp: Date.now() })
      });
      if (idleTimeout) { clearTimeout(idleTimeout); idleTimeout = null; }
    });

    // Register the approval tool using factory pattern
    // The factory function receives (ctx: OpenClawPluginToolContext) with sessionKey, sessionId, etc.
    // Plain tool objects do NOT receive ctx in execute — the 3rd arg is empty/undefined at runtime.
    api.registerTool((ctx: any) => {
      const sessionKey = ctx?.sessionKey;

      return {
        name: "request_user_approval",
        description: "Request user approval via snarling display. Creates a TaskFlow that waits for user response. Only one approval at a time.",
        parameters: Type.Object({
          action: Type.String({ description: "The action requiring approval (e.g., 'delete_file', 'send_email')" }),
          message: Type.String({ description: "Human-readable message explaining what needs approval" })
        }),
        async execute(_toolCallId: string, params: any) {
          const { action, message } = params;

          if (!sessionKey) {
            return {
              content: [{ type: "text", text: "Error: No sessionKey in tool context." }]
            };
          }

          // Get TaskFlow bound to this tool context
          let taskFlow: any = null;
          try {
            taskFlow = api.runtime?.taskFlow?.fromToolContext?.(ctx);
          } catch (e) {
            console.error(`[approval-tool] fromToolContext failed: ${e instanceof Error ? e.message : String(e)}, falling back to bindSession`);
          }

          if (!taskFlow) {
            const taskFlowApi = api.runtime?.taskFlow;
            if (taskFlowApi?.bindSession) {
              console.error(`[approval-tool] Using bindSession with sessionKey=${sessionKey}`);
              taskFlow = taskFlowApi.bindSession({
                sessionKey,
                requesterOrigin: "openclaw-interaction-bridge/approval-tool"
              });
            }
          }

          if (!taskFlow) {
            return {
              content: [{
                type: "text",
                text: "Error: TaskFlow not available. This tool requires an active agent session."
              }]
            };
          }

          const callbackUrl = `${CALLBACK_BASE_URL}/approval-callback`;

          try {
            const result = await requestUserApproval({ action, message }, taskFlow, { callbackUrl, approvalSecret: APPROVAL_SECRET, sessionKey });
            return {
              content: [{ type: "text", text: result }]
            };
          } catch (error) {
            return {
              content: [{
                type: "text",
                text: `Error requesting approval: ${error instanceof Error ? error.message : String(error)}`
              }]
            };
          }
        }
      };
    }, { optional: true });

    // Register send_notification tool — with feedback tracking via TaskFlow
    api.registerTool((ctx: any) => {
      const sessionKey = ctx?.sessionKey;

      return {
        name: "send_notification",
        description: "Send a notification to the snarling display. Fire-and-forget — does not wait for user response. Use for informational alerts, reminders, or status updates that don't require a decision.",
        parameters: Type.Object({
          message: Type.String({ description: "The notification message to display" }),
          priority: Type.Optional(Type.Union([Type.Literal("low"), Type.Literal("normal"), Type.Literal("high")], { description: "Priority level: low, normal (default), or high", default: "normal" })),
          duration: Type.Optional(Type.Number({ description: "Display duration in seconds (0 = use priority-based default: low=300s, others=no timeout)", default: 0 }))
        }),
        async execute(_toolCallId: string, params: any) {
          const { message, priority = "normal", duration = 0 } = params;

          // Try TaskFlow-based notification with feedback
          if (sessionKey) {
            let taskFlow: any = null;
            try {
              taskFlow = api.runtime?.taskFlow?.fromToolContext?.(ctx);
            } catch (e) {
              console.error(`[notification-tool] fromToolContext failed: ${e instanceof Error ? e.message : String(e)}, falling back to bindSession`);
            }

            if (!taskFlow) {
              const taskFlowApi = api.runtime?.taskFlow;
              if (taskFlowApi?.bindSession) {
                console.error(`[notification-tool] Using bindSession with sessionKey=${sessionKey}`);
                taskFlow = taskFlowApi.bindSession({
                  sessionKey,
                  requesterOrigin: "openclaw-interaction-bridge/notification-tool"
                });
              }
            }

            if (taskFlow) {
              const callbackUrl = `${CALLBACK_BASE_URL}/notification-callback`;
              try {
                const result = await sendNotificationWithFeedback({ message, priority, duration }, taskFlow, { callbackUrl, approvalSecret: APPROVAL_SECRET, sessionKey });
                return {
                  content: [{ type: "text", text: result }]
                };
              } catch (error) {
                // Fall through to fire-and-forget on TaskFlow error
                console.error(`[notification-tool] TaskFlow notification failed, falling back to fire-and-forget: ${error instanceof Error ? error.message : String(error)}`);
              }
            }
          }

          // Fallback: fire-and-forget notification (no feedback)
          try {
            const response = await fetch("http://localhost:5000/approval/alert", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                type: "notification",
                message,
                priority,
                duration,
                secret: APPROVAL_SECRET
              })
            });

            if (!response.ok) {
              return {
                content: [{ type: "text", text: `Notification sent but snarling returned HTTP ${response.status}` }]
              };
            }

            return {
              content: [{ type: "text", text: `Notification sent: "${message}" (priority: ${priority}, duration: ${duration}s)` }]
            };
          } catch (error) {
            return {
              content: [{ type: "text", text: `Failed to send notification: ${error instanceof Error ? error.message : String(error)}` }]
            };
          }
        }
      };
    }, { optional: true });

    // Register approval callback route (exact match)
    if (api.registerHttpRoute && !routeRegistered) {
      routeRegistered = true;

      api.registerHttpRoute({
        method: "POST",
        path: "/approval-callback",
        auth: "gateway",
        match: "exact",
        replaceExisting: true,
        handler: async (req: any, res: any) => {
          // Parse body from raw request first (needed for both stats and callback)
          let body: any = {};
          try {
            const chunks: Buffer[] = [];
            for await (const chunk of req) { chunks.push(typeof chunk === 'string' ? Buffer.from(chunk) : chunk); }
            const raw = Buffer.concat(chunks).toString();
            body = JSON.parse(raw);
          } catch (_e) {
            console.error(`[approval-callback] Failed to parse body: ${_e}`);
            res.statusCode = 400;
            res.end(JSON.stringify({ error: "Invalid JSON body" }));
            return true;
          }

          // Stats request: send {"action":"stats"} to /approval-callback
          if (body.action === 'stats') {
            res.statusCode = 200;
            res.end(JSON.stringify({ stats: approvalStats }));
            return true;
          }

          const { request_id, approved, secret } = body;

          if (!request_id) {
            res.statusCode = 400;
            res.end(JSON.stringify({ error: "Missing request_id" }));
            return true;
          }

          console.error(`[approval-callback] Received: request_id=${request_id}, approved=${approved}`);

          // Verify approval secret from request body
          const callbackSecret = secret;
          if (callbackSecret !== APPROVAL_SECRET) {
            console.error(`[approval-callback] Invalid secret for request ${request_id} (got='${callbackSecret}', expected='${APPROVAL_SECRET}')`);
            res.statusCode = 403;
            res.end(JSON.stringify({ error: "Invalid or missing approval secret" }));
            return true;
          }

          // Try sessionKey from body first (gateway strips query params), then URL params
          const bodySessionKey = body.sessionKey;
          const sessionKey = bodySessionKey || url.searchParams.get('sessionKey');
          if (!sessionKey) {
            res.statusCode = 400;
            res.end(JSON.stringify({ error: "Missing sessionKey parameter" }));
            return true;
          }
          console.error(`[approval-callback] Using sessionKey: ${sessionKey} (from body: ${!!bodySessionKey})`);

          // Bind TaskFlow to the main session for webhook context
          const taskFlowApi = api.runtime?.taskFlow;
          if (!taskFlowApi) {
            res.statusCode = 500;
            res.end(JSON.stringify({ error: "TaskFlow API not available", request_id }));
            return true;
          }

          const boundTaskFlow = taskFlowApi.bindSession({
            sessionKey,
            requesterOrigin: "snarling-webhook"
          });

          // Get system API for waking the agent session
          const systemApi = api.runtime?.system;
          if (!systemApi?.enqueueSystemEvent) {
            console.error(`[approval-callback] Warning: system API not available, agent may not wake up after approval`);
          }

          try {
            const result = await resumeApprovalFlow(
              request_id,
              approved === true,
              boundTaskFlow,
              // Pass minimal systemApi — just enqueueSystemEvent
              // Wake will happen AFTER HTTP response is sent
              { enqueueSystemEvent: systemApi?.enqueueSystemEvent?.bind(systemApi) ?? (() => {}), requestHeartbeatNow: () => {}, runHeartbeatOnce: undefined },
              sessionKey
            );

            // Safety net: always clear the lock after handling a callback
            forceClearApprovalLock(request_id);

            // Send HTTP response FIRST — must fully flush before attempting wake
            if (result.success) {
              res.statusCode = 200;
              res.end(JSON.stringify({ status: "success", request_id, approved, message: result.message }));
            } else {
              res.statusCode = 404;
              res.end(JSON.stringify({ error: result.message, request_id }));
            }

            // Schedule wake on NEXT event loop tick to ensure HTTP response is fully flushed
            // and the session lane is no longer considered "in-flight"
            setImmediate(() => {
              try {
                const wakeReason = "hook:approval";
                if (systemApi?.requestHeartbeatNow) {
                  systemApi.requestHeartbeatNow({
                    reason: wakeReason,
                    sessionKey,
                    coalesceMs: 100
                  });
                }
                if (systemApi?.runHeartbeatOnce) {
                  systemApi.runHeartbeatOnce({
                    sessionKey,
                    reason: wakeReason,
                    heartbeat: { target: "last" }
                  }).catch(() => {});
                }
                // Second wake attempt after a short delay
                setTimeout(() => {
                  try {
                    systemApi.requestHeartbeatNow?.({
                      reason: wakeReason,
                      sessionKey,
                      coalesceMs: 0
                    });
                  } catch (_e) {}
                }, 500);
              } catch (_wakeErr) {
                // Wake best-effort
              }
            });
          } catch (error) {
            console.error(`[approval-callback] Error: ${error}`);
            forceClearApprovalLock(request_id);
            res.statusCode = 500;
            res.end(JSON.stringify({ error: "Failed to resume TaskFlow", details: String(error), request_id }));
          }
          return true;
        }
      });

      console.error("[openclaw-interaction-bridge] Registered /approval-callback route (with ?stats=1 for tracker)");

      // Register notification callback route (exact match)
      api.registerHttpRoute({
        method: "POST",
        path: "/notification-callback",
        auth: "gateway",
        match: "exact",
        replaceExisting: true,
        handler: async (req: any, res: any) => {
          // Parse body from raw request
          let body: any = {};
          try {
            const chunks: Buffer[] = [];
            for await (const chunk of req) { chunks.push(typeof chunk === 'string' ? Buffer.from(chunk) : chunk); }
            const raw = Buffer.concat(chunks).toString();
            body = JSON.parse(raw);
          } catch (_e) {
            console.error(`[notification-callback] Failed to parse body: ${_e}`);
            res.statusCode = 400;
            res.end(JSON.stringify({ error: "Invalid JSON body" }));
            return true;
          }

          // Stats request
          if (body.action === 'stats') {
            res.statusCode = 200;
            res.end(JSON.stringify({ stats: notificationStats }));
            return true;
          }

          const { notification_id, revealed, time_to_reveal_sec, dismissed, timed_out, secret, sessionKey: bodySessionKey } = body;

          if (!notification_id) {
            res.statusCode = 400;
            res.end(JSON.stringify({ error: "Missing notification_id" }));
            return true;
          }

          console.error(`[notification-callback] Received: notification_id=${notification_id}, revealed=${revealed}, dismissed=${dismissed}`);

          // Verify secret
          if (secret !== APPROVAL_SECRET) {
            console.error(`[notification-callback] Invalid secret for notification ${notification_id}`);
            res.statusCode = 403;
            res.end(JSON.stringify({ error: "Invalid or missing approval secret" }));
            return true;
          }

          // sessionKey from body, or fall back to URL query params
          const url = new URL(req.url || '/', `http://localhost`);
          const sessionKey = bodySessionKey || url.searchParams.get('sessionKey');
          if (!sessionKey) {
            res.statusCode = 400;
            res.end(JSON.stringify({ error: "Missing sessionKey parameter" }));
            return true;
          }
          console.error(`[notification-callback] Using sessionKey: ${sessionKey} (from body: ${!!bodySessionKey})`);

          // Bind TaskFlow to the session
          const taskFlowApi = api.runtime?.taskFlow;
          if (!taskFlowApi) {
            res.statusCode = 500;
            res.end(JSON.stringify({ error: "TaskFlow API not available", notification_id }));
            return true;
          }

          const boundTaskFlow = taskFlowApi.bindSession({
            sessionKey,
            requesterOrigin: "snarling-webhook"
          });

          // Get system API for waking the agent session
          const systemApi = api.runtime?.system;
          if (!systemApi?.enqueueSystemEvent) {
            console.error(`[notification-callback] Warning: system API not available, agent may not wake up after notification feedback`);
          }

          try {
            const result = await resumeNotificationFlow(
              notification_id,
              { revealed: revealed ?? null, time_to_reveal_sec: time_to_reveal_sec ?? null, dismissed: dismissed ?? null, timed_out: timed_out ?? undefined },
              boundTaskFlow,
              { enqueueSystemEvent: systemApi?.enqueueSystemEvent?.bind(systemApi) ?? (() => {}), requestHeartbeatNow: () => {}, runHeartbeatOnce: undefined },
              sessionKey
            );

            // Send HTTP response FIRST
            if (result.success) {
              res.statusCode = 200;
              res.end(JSON.stringify({ status: "success", notification_id, message: result.message }));
            } else {
              res.statusCode = 404;
              res.end(JSON.stringify({ error: result.message, notification_id }));
            }

            // Schedule wake on NEXT event loop tick
            setImmediate(() => {
              try {
                const wakeReason = "hook:notification_feedback";
                if (systemApi?.requestHeartbeatNow) {
                  systemApi.requestHeartbeatNow({
                    reason: wakeReason,
                    sessionKey,
                    coalesceMs: 100
                  });
                }
                if (systemApi?.runHeartbeatOnce) {
                  systemApi.runHeartbeatOnce({
                    sessionKey,
                    reason: wakeReason,
                    heartbeat: { target: "last" }
                  }).catch(() => {});
                }
                // Second wake attempt after a short delay
                setTimeout(() => {
                  try {
                    systemApi.requestHeartbeatNow?.({
                      reason: wakeReason,
                      sessionKey,
                      coalesceMs: 0
                    });
                  } catch (_e) {}
                }, 500);
              } catch (_wakeErr) {
                // Wake best-effort
              }
            });
          } catch (error) {
            console.error(`[notification-callback] Error: ${error}`);
            res.statusCode = 500;
            res.end(JSON.stringify({ error: "Failed to resume notification TaskFlow", details: String(error), notification_id }));
          }
          return true;
        }
      });

      console.error("[openclaw-interaction-bridge] Registered /notification-callback route");
    }
  }
});