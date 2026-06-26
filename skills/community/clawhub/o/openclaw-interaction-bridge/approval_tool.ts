// approval_tool.ts - TaskFlow-based approval tool for OpenClaw Interaction Bridge
// Creates a managed TaskFlow that waits for user approval via snarling display

// Store pending approvals (request_id -> { flowId, createdAt })
interface PendingEntry {
  flowId: string;
  createdAt: number;
  sessionKey?: string;
}
const pendingApprovals = new Map<string, PendingEntry>();

// Store pending notifications (notification_id -> { flowId, createdAt, sessionKey })
interface PendingNotificationEntry {
  flowId: string;
  createdAt: number;
  sessionKey: string;
}
const pendingNotifications = new Map<string, PendingNotificationEntry>();

// Track if an approval is currently in progress (global lock)
// Now includes timestamp for staleness detection
let currentApprovalInProgress: string | null = null;
let currentApprovalStartedAt: number | null = null;

// Maximum time an approval lock is valid before it's considered stale (30 minutes)
const APPROVAL_LOCK_TIMEOUT_MS = 30 * 60 * 1000;

export interface RequestUserApprovalInput {
  action: string;
  message: string;
}

export interface ApprovalConfig {
  callbackUrl: string;
  approvalSecret: string;
  sessionKey: string;
}

// Plugin-side approval statistics
export const approvalStats = {
  requested: 0,
  approved: 0,
  rejected: 0,
  timedOut: 0,
  errored: 0,
};

// Plugin-side notification statistics
export const notificationStats = {
  sent: 0,
  revealed: 0,
  dismissed: 0,
  timedOut: 0,
  errored: 0,
};

/**
 * Check if the current approval lock is stale or orphaned, and clear it if so.
 * Returns true if the lock was cleared.
 */
function clearStaleLock(): boolean {
  if (!currentApprovalInProgress) return false;

  // Check 1: Is the lock entry missing from pendingApprovals? (orphaned)
  const entry = pendingApprovals.get(currentApprovalInProgress);
  if (!entry) {
    console.error(`[approval-tool] Clearing orphaned lock: ${currentApprovalInProgress} (no matching pending entry)`);
    currentApprovalInProgress = null;
    currentApprovalStartedAt = null;
    return true;
  }

  // Check 2: Has the lock been held too long? (stale/timeout)
  const elapsed = Date.now() - (currentApprovalStartedAt ?? entry.createdAt);
  if (elapsed > APPROVAL_LOCK_TIMEOUT_MS) {
    console.error(`[approval-tool] Clearing stale lock: ${currentApprovalInProgress} (held for ${Math.round(elapsed / 60000)}min, timeout=${APPROVAL_LOCK_TIMEOUT_MS / 60000}min)`);
    approvalStats.timedOut++;
    pendingApprovals.delete(currentApprovalInProgress);
    currentApprovalInProgress = null;
    currentApprovalStartedAt = null;
    return true;
  }

  return false;
}

/**
 * Force-clear the approval lock. Called by webhook handler after successful
 * flow resumption, or as a safety net.
 */
export function forceClearApprovalLock(requestId?: string): void {
  if (requestId && currentApprovalInProgress !== requestId) {
    // The lock belongs to a different request — only clear if stale
    clearStaleLock();
    return;
  }
  if (requestId) {
    pendingApprovals.delete(requestId);
  }
  currentApprovalInProgress = null;
  currentApprovalStartedAt = null;
}

/**
 * Request user approval using TaskFlow.
 * Creates a managed TaskFlow, sets it to waiting state, notifies snarling,
 * and POLLS until the user responds.
 *
 * If another approval is in progress, it checks for staleness before blocking.
 */
export async function requestUserApproval(
  input: RequestUserApprovalInput,
  taskFlow: any,
  config: ApprovalConfig
): Promise<string> {
  const { action, message } = input;
  const { callbackUrl, approvalSecret, sessionKey } = config;

  // Check and clear stale/orphaned locks before deciding to block
  clearStaleLock();

  // Global lock: only one approval at a time (with stale detection)
  if (currentApprovalInProgress) {
    const entry = pendingApprovals.get(currentApprovalInProgress);
    // Should still exist since clearStaleLock didn't clear it
    return `⚠️ Approval request blocked — another approval is already in progress (ID: ${currentApprovalInProgress}, started ${entry ? Math.round((Date.now() - entry.createdAt) / 60000) + 'min ago' : 'recently'}). Respond to that one first.\n\nBlocked action: ${action}`;
  }

  const requestId = `approval-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

  if (!taskFlow) {
    throw new Error("TaskFlow API not available - cannot create approval flow");
  }

  // Create a managed TaskFlow for this approval request
  const created = await taskFlow.createManaged({
    controllerId: "openclaw-interaction-bridge/approval",
    goal: `Request approval for: ${action}`,
    currentStep: "awaiting_user_approval",
    stateJson: {
      requestId,
      action,
      message,
      approved: null,
      respondedAt: null,
    },
  });

  if (!created || !created.flowId) {
    const detail = created ? JSON.stringify(created) : "null result";
    throw new Error(`Failed to create approval TaskFlow: ${detail}`);
  }

  const flowId = created.flowId;
  const now = Date.now();

  // Store mapping and set global lock
  pendingApprovals.set(requestId, { flowId, createdAt: now });
  currentApprovalInProgress = requestId;
  currentApprovalStartedAt = now;

  // Set the flow to waiting state
  const waiting = await taskFlow.setWaiting({
    flowId,
    expectedRevision: created.revision,
    currentStep: "awaiting_user_approval",
    stateJson: {
      requestId,
      action,
      message,
      approved: null,
      respondedAt: null,
    },
    waitJson: {
      kind: "user_approval",
      channel: "snarling",
      requestId,
      action,
      message,
    },
  });

  if (!waiting || !waiting.applied) {
    // Clean up on failure
    pendingApprovals.delete(requestId);
    currentApprovalInProgress = null;
    currentApprovalStartedAt = null;
    const detail = waiting ? JSON.stringify(waiting) : "null result";
    throw new Error(`Failed to set approval flow to waiting: ${detail}`);
  }

  approvalStats.requested++;

  // Notify snarling display directly (port 5000) - no middleman
  // Include sessionKey so snarling can pass it back in the callback URL
  try {
    await fetch("http://localhost:5000/approval/alert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        request_id: requestId,
        message: `${action}: ${message}`,
        secret: approvalSecret,
        sessionKey,
        timeout_seconds: 7200,
      }),
    });
  } catch (_e) {
    console.error(`[approval-tool] Could not notify snarling: ${_e}`);
    approvalStats.errored++;
  }

  // Return immediately — the webhook callback will resume the TaskFlow and
  // enqueue a system event with the approval result. The agent sees the
  // result as a system message on its next turn (triggered by the wake).
  // Note: The tool must return immediately because blocking/polling causes
  // session context corruption ("missing tool result" errors).
  console.error(`[approval-tool] Approval request sent, waiting for callback (request: ${requestId})`);
  return `⏳ Waiting for approval via Snarling display.\n\nAction: ${action}\nDetails: ${message}\nRequest: ${requestId}`;
}

/**
 * Resume a waiting approval TaskFlow with the user's decision.
 * Called by the webhook handler when user presses A/B on snarling.
 * After resuming the flow, wakes the agent session so it can continue.
 */
export async function resumeApprovalFlow(
  requestId: string,
  approved: boolean,
  taskFlowApi: any,
  systemApi: { enqueueSystemEvent: (text: string, opts: { sessionKey: string }) => void; requestHeartbeatNow: (opts: any) => void; runHeartbeatOnce?: (opts: any) => Promise<any> },
  sessionKey: string
): Promise<{ success: boolean; message: string }> {
  const entry = pendingApprovals.get(requestId);

  if (!entry) {
    // No matching entry — but still try to clear the lock if it matches
    if (currentApprovalInProgress === requestId) {
      console.error(`[approval-tool] Clearing lock for missing entry: ${requestId}`);
      currentApprovalInProgress = null;
      currentApprovalStartedAt = null;
    }
    return { success: false, message: `No pending approval found for request: ${requestId}` };
  }

  const flowId = entry.flowId;

  try {
    // Get current flow state
    const getResult = await taskFlowApi.get(flowId);
    const flow = getResult?.flow ?? getResult;
    if (!flow || !flow.flowId) {
      pendingApprovals.delete(requestId);
      forceClearApprovalLock(requestId);
      return { success: false, message: `TaskFlow not found: ${flowId}` };
    }

    // Resume the flow with the approval decision
    const resumed = await taskFlowApi.resume({
      flowId,
      expectedRevision: flow.revision,
      status: "running",
      currentStep: "approval_responded",
      stateJson: {
        ...flow.stateJson,
        approved,
        respondedAt: Date.now(),
      },
    });

    if (!resumed || !resumed.applied) {
      // Resume failed — clean up the lock anyway since we got a response
      pendingApprovals.delete(requestId);
      forceClearApprovalLock(requestId);
      return { success: false, message: `Failed to resume flow: ${resumed?.reason || "unknown error"}` };
    }

    // Finish the flow
    const finished = await taskFlowApi.finish({
      flowId,
      expectedRevision: resumed.flow.revision,
      stateJson: {
        ...resumed.flow.stateJson,
        approved,
        respondedAt: Date.now(),
      },
    });

    if (!finished || !finished.applied) {
      // Flow was resumed but couldn't be finished — still a success
      // since the approval decision was recorded
      console.error(`[approval-tool] Warning: could not finish flow ${flowId}: ${finished?.reason || "unknown"}`);
    }

    // Enqueue system event so the agent sees the approval on its next turn
    // Wake is now handled by the callback handler AFTER the HTTP response is sent
    const approvalResult = approved ? "APPROVED" : "REJECTED";
    if (approved) { approvalStats.approved++; } else { approvalStats.rejected++; }
    try {
      systemApi.enqueueSystemEvent(
        `User approval response: ${approvalResult}. ${approved ? "Proceeding with the action." : "Action cancelled by user."} (request: ${requestId})`,
        { sessionKey }
      );
    } catch (wakeErr) {
      console.error(`[approval-tool] Warning: failed to enqueue system event: ${wakeErr}`);
    }

    return { success: true, message: `Approval ${approved ? "APPROVED" : "REJECTED"} for ${requestId}` };
  } finally {
    // ALWAYS clean up, regardless of success or failure in individual steps
    pendingApprovals.delete(requestId);
    forceClearApprovalLock(requestId);
  }
}

/**
 * Get the flowId for a pending approval request.
 */
export function getPendingApprovalFlowId(requestId: string): string | undefined {
  return pendingApprovals.get(requestId)?.flowId;
}

/**
 * Send a notification with feedback tracking using TaskFlow.
 * Creates a managed TaskFlow, sets it to waiting state, notifies snarling,
 * and returns immediately. The webhook callback will resume the flow later.
 */
export async function sendNotificationWithFeedback(
  input: { message: string; priority?: string; duration?: number },
  taskFlow: any,
  config: ApprovalConfig
): Promise<string> {
  const { message, priority = "normal", duration = 0 } = input;  // 0 = no timeout, let snarling decide based on priority
  const { callbackUrl, approvalSecret, sessionKey } = config;

  const notificationId = `notify-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

  if (!taskFlow) {
    throw new Error("TaskFlow API not available - cannot create notification flow");
  }

  // Create a managed TaskFlow for this notification
  const truncatedMessage = message.length > 50 ? message.substring(0, 50) + "..." : message;
  const created = await taskFlow.createManaged({
    controllerId: "openclaw-interaction-bridge/notification",
    goal: `Notification feedback: ${truncatedMessage}`,
    currentStep: "awaiting_user_interaction",
    stateJson: {
      notificationId,
      message,
      priority,
      revealed: null,
      dismissed: null,
      timeToRevealSec: null,
      timedOut: null,
    },
  });

  if (!created || !created.flowId) {
    const detail = created ? JSON.stringify(created) : "null result";
    throw new Error(`Failed to create notification TaskFlow: ${detail}`);
  }

  const flowId = created.flowId;
  const now = Date.now();

  // Store mapping
  pendingNotifications.set(notificationId, { flowId, createdAt: now, sessionKey });

  // Set the flow to waiting state
  const waiting = await taskFlow.setWaiting({
    flowId,
    expectedRevision: created.revision,
    currentStep: "awaiting_user_interaction",
    stateJson: {
      notificationId,
      message,
      priority,
      revealed: null,
      dismissed: null,
      timeToRevealSec: null,
      timedOut: null,
    },
    waitJson: {
      kind: "notification_feedback",
      channel: "snarling",
      notificationId,
      message,
      priority,
    },
  });

  if (!waiting || !waiting.applied) {
    // Clean up on failure
    pendingNotifications.delete(notificationId);
    const detail = waiting ? JSON.stringify(waiting) : "null result";
    throw new Error(`Failed to set notification flow to waiting: ${detail}`);
  }

  notificationStats.sent++;

  // Notify snarling display directly (port 5000)
  try {
    await fetch("http://localhost:5000/approval/alert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type: "notification",
        notification_id: notificationId,
        message,
        priority,
        duration,
        secret: approvalSecret,
        callback_url: callbackUrl,
        sessionKey,
      }),
    });
  } catch (_e) {
    console.error(`[notification-tool] Could not notify snarling: ${_e}`);
    notificationStats.errored++;
  }

  // Return immediately — the webhook callback will resume the TaskFlow and
  // enqueue a system event with the notification feedback result.
  console.error(`[notification-tool] Notification sent, waiting for feedback (id: ${notificationId})`);
  return `⏳ Notification sent, awaiting feedback.\n\nMessage: ${message}\nPriority: ${priority}\nID: ${notificationId}`;
}

/**
 * Resume a waiting notification TaskFlow with user feedback.
 * Called by the webhook handler when snarling reports user interaction.
 */
export async function resumeNotificationFlow(
  notificationId: string,
  feedback: { revealed: boolean | null; time_to_reveal_sec: number | null; dismissed: boolean | null; timed_out?: boolean },
  taskFlowApi: any,
  systemApi: { enqueueSystemEvent: (text: string, opts: { sessionKey: string }) => void; requestHeartbeatNow: (opts: any) => void; runHeartbeatOnce?: (opts: any) => Promise<any> },
  sessionKey: string
): Promise<{ success: boolean; message: string }> {
  const entry = pendingNotifications.get(notificationId);

  if (!entry) {
    return { success: false, message: `No pending notification found for id: ${notificationId}` };
  }

  const flowId = entry.flowId;

  try {
    // Get current flow state
    const getResult = await taskFlowApi.get(flowId);
    const flow = getResult?.flow ?? getResult;
    if (!flow || !flow.flowId) {
      pendingNotifications.delete(notificationId);
      return { success: false, message: `TaskFlow not found: ${flowId}` };
    }

    // Resume the flow with the notification feedback
    const resumed = await taskFlowApi.resume({
      flowId,
      expectedRevision: flow.revision,
      status: "running",
      currentStep: "notification_responded",
      stateJson: {
        ...flow.stateJson,
        revealed: feedback.revealed,
        timeToRevealSec: feedback.time_to_reveal_sec,
        dismissed: feedback.dismissed,
        timedOut: feedback.timed_out ?? false,
      },
    });

    if (!resumed || !resumed.applied) {
      pendingNotifications.delete(notificationId);
      return { success: false, message: `Failed to resume flow: ${resumed?.reason || "unknown error"}` };
    }

    // Finish the flow
    const finished = await taskFlowApi.finish({
      flowId,
      expectedRevision: resumed.flow.revision,
      stateJson: {
        ...resumed.flow.stateJson,
        revealed: feedback.revealed,
        timeToRevealSec: feedback.time_to_reveal_sec,
        dismissed: feedback.dismissed,
        timedOut: feedback.timed_out ?? false,
      },
    });

    if (!finished || !finished.applied) {
      console.error(`[notification-tool] Warning: could not finish flow ${flowId}: ${finished?.reason || "unknown"}`);
    }

    // Update stats
    if (feedback.timed_out) {
      notificationStats.timedOut++;
    } else if (feedback.revealed) {
      notificationStats.revealed++;
    } else if (feedback.dismissed) {
      notificationStats.dismissed++;
    }

    // Enqueue system event so the agent sees the feedback on its next turn
    const timedOutStr = feedback.timed_out ? ", timed_out=true" : "";
    try {
      systemApi.enqueueSystemEvent(
        `Notification feedback: revealed=${feedback.revealed}, time_to_reveal_sec=${feedback.time_to_reveal_sec}, dismissed=${feedback.dismissed}${timedOutStr} (id: ${notificationId})`,
        { sessionKey }
      );
    } catch (wakeErr) {
      console.error(`[notification-tool] Warning: failed to enqueue system event: ${wakeErr}`);
    }

    return { success: true, message: `Notification feedback received for ${notificationId}` };
  } finally {
    // ALWAYS clean up
    pendingNotifications.delete(notificationId);
  }
}