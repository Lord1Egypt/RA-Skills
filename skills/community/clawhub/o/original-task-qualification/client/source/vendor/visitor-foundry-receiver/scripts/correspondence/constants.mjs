export const CONTRACT_VERSION = "1";

export const MAX_TITLE_CHARS = 120;
export const MAX_SUMMARY_CHARS = 2000;
export const MAX_EVENT_TEXT_CHARS = 8000;
export const MAX_URL_CHARS = 2048;
export const MAX_LABEL_CHARS = 200;
export const MAX_BODY_BYTES = 32 * 1024;
export const DEFAULT_EVENT_LIMIT = 25;
export const MIN_EVENT_LIMIT = 1;
export const MAX_EVENT_LIMIT = 100;
/** GET /events page size used by the workbench. Distinct from the retained window. */
export const PAGE_EVENT_LIMIT = DEFAULT_EVENT_LIMIT;
/** Client-retained ordered event window. Distinct from the request page size. */
export const WINDOW_EVENT_LIMIT = MAX_EVENT_LIMIT;
export const MAX_CHECKPOINT_CHARS = 16 * 1024;

export const EVENT_KINDS = Object.freeze([
  "request",
  "reply",
  "artifact",
  "correction",
  "needs_human",
  "resolved",
  "reopened",
]);

export const GRANT_ROLES = Object.freeze(["reader", "writer"]);
export const PROJECT_STATUSES = Object.freeze(["open", "needs_human", "resolved"]);
export const NEXT_ACTION_KINDS = Object.freeze(["reply", "human_review"]);

export const PROJECT_CREATE_FIELDS = Object.freeze(["title", "summary"]);
export const GRANT_CREATE_FIELDS = Object.freeze(["role", "expiresAt"]);
export const EVENT_POST_FIELDS = Object.freeze(["kind", "text", "artifact", "expectedVersion"]);
export const ARTIFACT_FIELDS = Object.freeze(["url", "label"]);

export const CHECKPOINT_SCHEMA = "neomorphic.correspondence.checkpoint.v1";
export const CORRESPONDENCE_RECORD_BUNDLE_SCHEMA = "neomorphic.correspondence.record-bundle.v1";
