'use strict';

const WEBHOOK_URL = 'https://hook.notilens.com/webhook/{token}/send';
const USER_AGENT = 'notilens-clawhub/0.2.0';

// ── Internals ─────────────────────────────────────────────────────────────────

function getCredentials() {
  const token = process.env.NOTILENS_TOKEN;
  const secret = process.env.NOTILENS_SECRET;
  if (!token || !secret) {
    throw new Error(
      'NOTILENS_TOKEN and NOTILENS_SECRET environment variables are required. ' +
      'Get them from your topic settings at https://www.notilens.com.'
    );
  }
  return { token, secret };
}

async function _deliver(payload) {
  const { token, secret } = getCredentials();
  const url = WEBHOOK_URL.replace('{token}', token);

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-NOTILENS-KEY': secret,
      'User-Agent': USER_AGENT,
    },
    body: JSON.stringify({ ts: Date.now() / 1000, ...payload }),
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(
      `NotiLens delivery failed: HTTP ${res.status} — ${data.message || data.error || 'unknown error'}`
    );
  }

  return data;
}

function _meta(obj) {
  return Object.keys(obj).length ? { meta: obj } : {};
}

// ── Helper ────────────────────────────────────────────────────────────────────

/**
 * Generate a unique run ID to correlate all events from the same task execution.
 * Format: run_{unix_ms}_{random_hex4}
 * Include this in meta.run_id on every event for a given run.
 */
function genRunId() {
  const hex = Math.floor(Math.random() * 0xffff).toString(16).padStart(4, '0');
  return `run_${Date.now()}_${hex}`;
}

// ── Notify ────────────────────────────────────────────────────────────────────

/**
 * Send a notification. Title is auto-generated from name + event.
 *
 * @param {string} name      - Source name (app, script, agent, etc.)
 * @param {string} event     - Event name, e.g. "order.placed" or "disk.space.full"
 * @param {string} message   - Notification body text
 * @param {object} [options] - type, image_url, open_url, download_url, tags, meta
 */
async function notify(name, event, message, options = {}) {
  if (!event)   throw new Error('event is required');
  if (!message) throw new Error('message is required');
  const { type = 'info', ...rest } = options;
  return _deliver({
    event,
    title: `${name} | ${event}`,
    message,
    type,
    agent: name,  // kept as "agent" for backend compatibility
    ...rest,
  });
}

/**
 * Track any custom event. Title is auto-generated from name + event.
 * Use this for domain-specific events like "order.placed", "deploy.started", etc.
 *
 * @param {string} name
 * @param {string} event     - Any event string, e.g. "order.placed"
 * @param {string} message   - Notification body
 * @param {string} [type]    - "info" | "success" | "warning" | "urgent" (default: "info")
 * @param {object} [meta]    - Optional key-value pairs
 */
async function track(name, event, message, type = 'info', meta = {}) {
  if (!event)   throw new Error('event is required');
  if (!message) throw new Error('message is required');
  return _deliver({
    event,
    title: `${name} | ${event}`,
    message,
    type,
    agent: name,  // kept as "agent" for backend compatibility
    ..._meta(meta),
  });
}

// ── Task lifecycle ─────────────────────────────────────────────────────────────

/**
 * Fire task.queued — task is queued before a worker picks it up.
 */
async function taskQueued(name, taskId, message = '', meta = {}) {
  return _deliver({
    event: 'task.queued',
    title: `${name} | ${taskId} | task.queued`,
    message: message || `${name} | ${taskId} queued`,
    type: 'info',
    agent: name,
    task_id: taskId,
    ..._meta(meta),
  });
}

/**
 * Fire task.started — begins executing a task.
 * @param {object} [meta] - run_id, queue_ms, etc.
 */
async function taskStarted(name, taskId, message = '', meta = {}) {
  return _deliver({
    event: 'task.started',
    title: `${name} | ${taskId} | task.started`,
    message: message || `${name} | ${taskId} started`,
    type: 'info',
    agent: name,
    task_id: taskId,
    ..._meta(meta),
  });
}

/**
 * Fire task.progress — meaningful checkpoint during a long task.
 * @param {object} [meta] - rows_done, percent, tokens_used, etc.
 */
async function taskProgress(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.progress');
  return _deliver({
    event: 'task.progress',
    title: `${name} | ${taskId} | task.progress`,
    message,
    type: 'info',
    agent: name,
    task_id: taskId,
    ..._meta(meta),
  });
}

/**
 * Fire task.paused — task is pausing (rate limit, waiting on I/O, etc.).
 * @param {object} [meta] - pause_count, wait_reason, etc.
 */
async function taskPaused(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.paused');
  return _deliver({
    event: 'task.paused',
    title: `${name} | ${taskId} | task.paused`,
    message,
    type: 'warning',
    agent: name,
    task_id: taskId,
    ..._meta(meta),
  });
}

/**
 * Fire task.waiting — task is blocked on an external resource.
 * @param {object} [meta] - wait_count, wait_reason, etc.
 */
async function taskWaiting(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.waiting');
  return _deliver({
    event: 'task.waiting',
    title: `${name} | ${taskId} | task.waiting`,
    message,
    type: 'warning',
    agent: name,
    task_id: taskId,
    ..._meta(meta),
  });
}

/**
 * Fire task.resumed — task resumed after a pause or wait.
 * @param {object} [meta] - pause_ms, wait_ms, pause_count, wait_count
 */
async function taskResumed(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.resumed');
  return _deliver({
    event: 'task.resumed',
    title: `${name} | ${taskId} | task.resumed`,
    message,
    type: 'info',
    agent: name,
    task_id: taskId,
    ..._meta(meta),
  });
}

/**
 * Fire task.retry — task is being retried after a failure.
 * @param {number} retryCount - Current retry number (1-based)
 * @param {object} [meta]     - last_error, etc.
 */
async function taskRetry(name, taskId, retryCount, meta = {}) {
  return _deliver({
    event: 'task.retry',
    title: `${name} | ${taskId} | task.retry`,
    message: `${name} | ${taskId} retrying (attempt ${retryCount})`,
    type: 'warning',
    agent: name,
    task_id: taskId,
    meta: { retry_count: retryCount, ...meta },
  });
}

/**
 * Fire task.loop — agent detected it is repeating the same step.
 * @param {number} loopCount - How many times the step has repeated
 * @param {object} [meta]
 */
async function taskLoop(name, taskId, message, loopCount, meta = {}) {
  if (!message) throw new Error('message is required for task.loop');
  return _deliver({
    event: 'task.loop',
    title: `${name} | ${taskId} | task.loop`,
    message,
    type: 'warning',
    agent: name,
    task_id: taskId,
    is_actionable: true,
    meta: { loop_count: loopCount, ...meta },
  });
}

/**
 * Fire task.error — non-fatal error (task continues after this).
 * @param {object} [meta] - error_count, last_error, etc.
 */
async function taskError(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.error');
  return _deliver({
    event: 'task.error',
    title: `${name} | ${taskId} | task.error`,
    message,
    type: 'urgent',
    agent: name,
    task_id: taskId,
    is_actionable: true,
    ..._meta(meta),
  });
}

// ── Terminal states ────────────────────────────────────────────────────────────

/**
 * Fire task.completed — task finished successfully.
 * @param {object} [meta]               - total_duration_ms, active_ms, rows_processed, etc.
 * @param {string} [meta.download_url]  - Promoted to top-level field
 * @param {string} [meta.open_url]      - Promoted to top-level field
 */
async function taskCompleted(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.completed');
  const { download_url, open_url, ...restMeta } = meta;
  return _deliver({
    event: 'task.completed',
    title: `${name} | ${taskId} | task.completed`,
    message,
    type: 'success',
    agent: name,
    task_id: taskId,
    ...(download_url ? { download_url } : {}),
    ...(open_url     ? { open_url }     : {}),
    ..._meta(restMeta),
  });
}

/**
 * Fire task.failed — task failed and will not be retried.
 * @param {object} [meta]          - retry_count, error_count, last_error, total_duration_ms
 * @param {string} [meta.open_url] - Promoted to top-level field
 */
async function taskFailed(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.failed');
  const { open_url, ...restMeta } = meta;
  return _deliver({
    event: 'task.failed',
    title: `${name} | ${taskId} | task.failed`,
    message,
    type: 'urgent',
    agent: name,
    task_id: taskId,
    is_actionable: true,
    ...(open_url ? { open_url } : {}),
    ..._meta(restMeta),
  });
}

/**
 * Fire task.timeout — task exceeded its time limit.
 * @param {object} [meta] - total_duration_ms, time_limit_ms, etc.
 */
async function taskTimeout(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.timeout');
  return _deliver({
    event: 'task.timeout',
    title: `${name} | ${taskId} | task.timeout`,
    message,
    type: 'urgent',
    agent: name,
    task_id: taskId,
    is_actionable: true,
    ..._meta(meta),
  });
}

/**
 * Fire task.cancelled — task was cancelled before completion.
 * @param {object} [meta] - total_duration_ms, etc.
 */
async function taskCancelled(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.cancelled');
  return _deliver({
    event: 'task.cancelled',
    title: `${name} | ${taskId} | task.cancelled`,
    message,
    type: 'warning',
    agent: name,
    task_id: taskId,
    ..._meta(meta),
  });
}

/**
 * Fire task.stopped — task was stopped intentionally (not an error).
 * @param {object} [meta] - total_duration_ms, etc.
 */
async function taskStopped(name, taskId, message = '', meta = {}) {
  return _deliver({
    event: 'task.stopped',
    title: `${name} | ${taskId} | task.stopped`,
    message: message || `${name} | ${taskId} stopped`,
    type: 'info',
    agent: name,
    task_id: taskId,
    ..._meta(meta),
  });
}

/**
 * Fire task.terminated — task was forcibly terminated.
 * @param {object} [meta] - total_duration_ms, reason, etc.
 */
async function taskTerminated(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for task.terminated');
  return _deliver({
    event: 'task.terminated',
    title: `${name} | ${taskId} | task.terminated`,
    message,
    type: 'urgent',
    agent: name,
    task_id: taskId,
    is_actionable: true,
    ..._meta(meta),
  });
}

// ── Input ──────────────────────────────────────────────────────────────────────

/**
 * Fire input.required — needs a human decision to continue.
 * @param {string} [openUrl] - URL to open for the approval UI
 * @param {object} [meta]
 */
async function inputRequired(name, message, openUrl = '', meta = {}) {
  if (!message) throw new Error('message is required for input.required');
  return _deliver({
    event: 'input.required',
    title: `${name} | input required`,
    message,
    type: 'warning',
    agent: name,
    is_actionable: true,
    ...(openUrl ? { open_url: openUrl } : {}),
    ..._meta(meta),
  });
}

/**
 * Fire input.approved — human approved the request.
 */
async function inputApproved(name, message, meta = {}) {
  if (!message) throw new Error('message is required for input.approved');
  return _deliver({
    event: 'input.approved',
    title: `${name} | input approved`,
    message,
    type: 'success',
    agent: name,
    ..._meta(meta),
  });
}

/**
 * Fire input.rejected — human rejected the request.
 */
async function inputRejected(name, message, meta = {}) {
  if (!message) throw new Error('message is required for input.rejected');
  return _deliver({
    event: 'input.rejected',
    title: `${name} | input rejected`,
    message,
    type: 'warning',
    agent: name,
    is_actionable: true,
    ..._meta(meta),
  });
}

// ── Output ─────────────────────────────────────────────────────────────────────

/**
 * Fire output.generated — produced output (file, report, result, etc.).
 * @param {string} [meta.download_url] - Promoted to top-level field
 * @param {string} [meta.open_url]     - Promoted to top-level field
 * @param {string} [meta.image_url]    - Promoted to top-level field
 */
async function outputGenerated(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for output.generated');
  const { download_url, open_url, image_url, ...restMeta } = meta;
  return _deliver({
    event: 'output.generated',
    title: `${name} | ${taskId} | output.generated`,
    message,
    type: 'success',
    agent: name,
    task_id: taskId,
    ...(download_url ? { download_url } : {}),
    ...(open_url     ? { open_url }     : {}),
    ...(image_url    ? { image_url }    : {}),
    ..._meta(restMeta),
  });
}

/**
 * Fire output.failed — failed to produce expected output.
 * @param {object} [meta] - last_error, etc.
 */
async function outputFailed(name, taskId, message, meta = {}) {
  if (!message) throw new Error('message is required for output.failed');
  return _deliver({
    event: 'output.failed',
    title: `${name} | ${taskId} | output.failed`,
    message,
    type: 'urgent',
    agent: name,
    task_id: taskId,
    is_actionable: true,
    ..._meta(meta),
  });
}

// ── Exports ────────────────────────────────────────────────────────────────────

module.exports = {
  genRunId,
  notify,
  track,
  taskQueued,
  taskStarted,
  taskProgress,
  taskPaused,
  taskWaiting,
  taskResumed,
  taskRetry,
  taskLoop,
  taskError,
  taskCompleted,
  taskFailed,
  taskTimeout,
  taskCancelled,
  taskStopped,
  taskTerminated,
  inputRequired,
  inputApproved,
  inputRejected,
  outputGenerated,
  outputFailed,
};
