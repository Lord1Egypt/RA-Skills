import { DEFAULT_KEPT_QUERY_PARAMS, type RedactionOptions } from "./privacy/redact.js";
import { DEFAULT_ACCESS_POLICY, type AccessPolicy } from "./privacy/policy.js";
import { LIMITS } from "./ga4/limits.js";

/**
 * Settings, resolved from the environment.
 *
 * Everything here is read from the process environment and never from argv.
 * That is deliberate for the four privacy settings: a command-line flag can be
 * set by the model, and a page title is attacker-controlled text that reaches
 * the model. An environment variable is set by a person.
 */
export type ResolvedConfig = {
  defaultPropertyId?: string;
  defaultRowLimit: number;
  redaction: RedactionOptions;
  access: AccessPolicy;
  auditLogPath?: string;
};

/** True only for "1", "true", "yes" and "on", case-insensitively. */
function isTrue(value: string | undefined): boolean {
  if (value === undefined) return false;
  return ["1", "true", "yes", "on"].includes(value.trim().toLowerCase());
}

/** False only for "0", "false", "no" and "off". Anything else leaves the default. */
function isFalse(value: string | undefined): boolean {
  if (value === undefined) return false;
  return ["0", "false", "no", "off"].includes(value.trim().toLowerCase());
}

export function configFromEnv(
  env: NodeJS.ProcessEnv,
  onWarning?: (message: string) => void,
): ResolvedConfig {
  const allowlist: string[] = [];
  for (const raw of (env.GA4_PROPERTY_ALLOWLIST ?? "").split(",")) {
    const id = raw.trim();
    if (id === "") continue;
    if (!/^[0-9]+$/.test(id)) {
      onWarning?.(
        `Ignoring GA4_PROPERTY_ALLOWLIST entry ${JSON.stringify(id)}: a property id is the ` +
          "9 or 10 digit number from Admin > Property details, not the G-XXXXXXXXXX measurement id.",
      );
      continue;
    }
    allowlist.push(id);
  }

  return {
    defaultPropertyId: env.GA4_PROPERTY_ID?.trim() || undefined,
    defaultRowLimit: LIMITS.DEFAULT_ROWS,
    redaction: {
      enabled: !isFalse(env.GA4_REDACT),
      keepQueryParams: DEFAULT_KEPT_QUERY_PARAMS,
      extraPatterns: [],
    },
    access: {
      ...DEFAULT_ACCESS_POLICY,
      allowUserIdentifyingDimensions: isTrue(env.GA4_ALLOW_USER_DIMENSIONS),
      propertyAllowlist: allowlist,
    },
    auditLogPath: env.GA4_AUDIT_LOG?.trim() || undefined,
  };
}
