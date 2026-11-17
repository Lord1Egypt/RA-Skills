const NEXT_ACTIONS = Object.freeze({
  COUNT_MISMATCH: "Re-export or provide the exact expected count from a trusted snapshot, then retry.",
  SCOPE_MISSING: "Capture each source scope explicitly and ensure every record or manifest names its scope.",
  MANIFEST_INVALID: "Regenerate the export manifest and verify its format, counts, and referenced files.",
  APPROVAL_INVALID: "Run the dry-run again and use the newly issued approval for this exact action and run.",
  OUTPUT_CONFLICT: "Choose a new empty output path and repeat the dry-run before applying.",
  SYMBOLIC_LINK: "Use explicit regular input files and a non-symbolic-link output path.",
  AUDIT_INCOMPLETE: "Increase --max-comparisons until the approximate audit is complete, or omit the strict flag.",
  PREFLIGHT_FAILED: "Correct every reported preflight problem, then repeat the dry-run.",
  NODE_VERSION_UNSUPPORTED: "Install Node.js 22 or newer and rerun the command.",
  USAGE_ERROR: "Check --help, correct the command arguments, and retry.",
  INTERNAL_ERROR: "Retry only after reviewing the error details; report a reproducible case if it persists.",
});

export class MigratorError extends Error {
  constructor(code, message, { nextAction = null, details = null, cause = undefined } = {}) {
    super(String(message), { cause });
    this.name = "MigratorError";
    this.code = String(code);
    this.next_action = nextAction || NEXT_ACTIONS[this.code] || NEXT_ACTIONS.INTERNAL_ERROR;
    this.details = details;
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      next_action: this.next_action,
      details: this.details,
    };
  }
}

export function migratorError(code, message, options = {}) {
  return new MigratorError(code, message, options);
}

export function asMigratorError(error) {
  if (error instanceof MigratorError) return error;
  const message = error instanceof Error ? error.message : String(error);
  const lower = message.toLowerCase();
  let code = "INTERNAL_ERROR";
  if (error instanceof Error && error.code === "EEXIST") code = "OUTPUT_CONFLICT";
  else if (lower.includes("count does not match") || lower.includes("expected total")) code = "COUNT_MISMATCH";
  else if (lower.includes("missing scope") || lower.includes("missing agentid")) code = "SCOPE_MISSING";
  else if (lower.includes("manifest") || lower.includes("unknown memory-lancedb-pro")
    || lower.includes("invalid official")) code = "MANIFEST_INVALID";
  else if (lower.includes("approval")) code = "APPROVAL_INVALID";
  else if (lower.includes("symbolic link")) code = "SYMBOLIC_LINK";
  else if (lower.includes("overwrite") || lower.includes("already exist")
    || lower.includes("output appeared") || lower.includes("output ancestor changed")) {
    code = "OUTPUT_CONFLICT";
  } else if (lower.includes("usage:") || lower.includes("required") || lower.includes("unknown adapter")
    || lower.includes("unexpected argument") || lower.includes("must be")
    || lower.includes("invalid --")) code = "USAGE_ERROR";
  return new MigratorError(code, message, {
    details: error instanceof Error && error.code ? { system_code: error.code } : null,
    cause: error instanceof Error ? error : undefined,
  });
}

export function formatMigratorError(error, { json = false } = {}) {
  const normalized = asMigratorError(error);
  if (json) return `${JSON.stringify(normalized)}\n`;
  return `error [${normalized.code}]: ${normalized.message}\nnext action: ${normalized.next_action}\n`;
}
