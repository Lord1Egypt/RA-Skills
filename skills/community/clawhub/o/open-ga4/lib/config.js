import { DEFAULT_KEPT_QUERY_PARAMS } from "./privacy/redact.js";
import { DEFAULT_ACCESS_POLICY } from "./privacy/policy.js";
import { LIMITS } from "./ga4/limits.js";
/** True only for "1", "true", "yes" and "on", case-insensitively. */
function isTrue(value) {
    if (value === undefined)
        return false;
    return ["1", "true", "yes", "on"].includes(value.trim().toLowerCase());
}
/** False only for "0", "false", "no" and "off". Anything else leaves the default. */
function isFalse(value) {
    if (value === undefined)
        return false;
    return ["0", "false", "no", "off"].includes(value.trim().toLowerCase());
}
export function configFromEnv(env, onWarning) {
    const allowlist = [];
    for (const raw of (env.GA4_PROPERTY_ALLOWLIST ?? "").split(",")) {
        const id = raw.trim();
        if (id === "")
            continue;
        if (!/^[0-9]+$/.test(id)) {
            onWarning?.(`Ignoring GA4_PROPERTY_ALLOWLIST entry ${JSON.stringify(id)}: a property id is the ` +
                "9 or 10 digit number from Admin > Property details, not the G-XXXXXXXXXX measurement id.");
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
