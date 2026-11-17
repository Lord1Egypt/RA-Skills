
/* Shared UI Utilities — timeSince helper + TASKS state */
// NOTE: toast, renderMarkdown, sanitizeHtml, renderFullMarkdown,
//       loadOperationsStatus, refreshCurrentTab are defined in api.js (loaded first).
//       Do NOT redefine them here.

// ─── Time helpers (shared across tabs) ───────────────────────────────
function timeSince(ts) {
  // ts can be a Unix-ms number or ISO string
  const ms = typeof ts === 'number' ? ts : Date.parse(ts || '');
  const s = Math.floor((Date.now() - ms) / 1000);
  if (s < 60) return s + 's ago';
  if (s < 3600) return Math.floor(s / 60) + 'm ago';
  if (s < 86400) return Math.floor(s / 3600) + 'h ago';
  return Math.floor(s / 86400) + 'd ago';
}

// ═══ TASKS ═══
