import type { Check, CheckId } from "../tools/discovery.js";

/**
 * `doctor --json`'s machine-readable state.
 *
 * The markdown checklist runDiagnose renders is right for a person reading a
 * terminal: it lists everything that is wrong. It is wrong for an agent
 * guiding somebody through setup, because the useful question at that point
 * is not "what is wrong" but "what do I do next". This module answers the
 * second question, and answers it with exactly one step: a person handed
 * five simultaneous problems does nothing, a person handed one does it.
 */

export type BlockedOn =
  | "ok"
  | "no_credentials"
  | "bad_credentials"
  | "clock_skew"
  | "data_api_disabled"
  | "admin_api_disabled"
  | "no_property_grant"
  | "no_property_selected"
  | "wrong_property"
  | "quota"
  | "unknown";

export const BLOCKED_ON_VALUES: readonly BlockedOn[] = [
  "ok",
  "no_credentials",
  "bad_credentials",
  "clock_skew",
  "data_api_disabled",
  "admin_api_disabled",
  "no_property_grant",
  "no_property_selected",
  "wrong_property",
  "quota",
  "unknown",
];

export type SetupState = {
  ok: boolean;
  blocked_on: BlockedOn;
  /** The service-account address currently in use, when one is known. */
  principal?: string;
  next?: { where: string; action: string; paste?: string; role?: string };
  url?: string;
  properties?: Array<{ id: string; name: string }>;
  /**
   * Failing checks that are not blocking anything, so they never become
   * `blocked_on` and never make `ok` false. Today that is exactly one: the
   * privacy-settings check, which fails when redaction has been turned off.
   *
   * It needs a channel of its own precisely because it is not blocking. Before
   * this field, redaction being off was visible only in the markdown checklist
   * a person reads; the JSON an agent reads said `ok: true` and named nothing,
   * so the agent could not tell a user their reports were unredacted. Omitted
   * entirely when there is nothing to warn about, so the common shape stays as
   * small as it was.
   */
  warnings?: string[];
};

type Next = NonNullable<SetupState["next"]>;
type Mapped = { blocked_on: Exclude<BlockedOn, "ok">; next: Next; url?: string };

/**
 * The console link for the two API-enablement states. Both live on
 * console.cloud.google.com, already on the egress and text-only allowlists
 * in src/privacy/surface.test.ts (the same host errors.ts already links to
 * for the equivalent SERVICE_DISABLED error).
 */
function enableApiUrl(service: string): string {
  return `https://console.cloud.google.com/apis/library/${service}`;
}

/**
 * Maps a Ga4Error code to a blocking state, in the order a person would need
 * to fix them. Every code SETUP_CODES (src/cli/exit.ts) plus QUOTA_EXHAUSTED
 * has an exact bucket here; that is deliberately the same nine-code set,
 * because those are the only codes this taxonomy exists to describe.
 *
 * Anything else reaching here (a bare 5xx, an invalid request, a genuinely
 * unexpected error) is not a setup problem this taxonomy recognizes, and it
 * is not safe to guess one: reporting it as quota exhaustion sends someone to
 * wait out a limit that was never hit. It gets its own "unknown" bucket
 * instead, whose action is to relay the underlying message rather than to
 * name a cause this code cannot support.
 */
function mapped(code: string, principal?: string, detail?: string, checkId?: CheckId): Mapped {
  switch (code) {
    case "CREDENTIALS_MISSING":
      return {
        blocked_on: "no_credentials",
        next: {
          where: "your environment",
          action:
            "Set GA4_CREDENTIALS to your service-account key's contents, or a path to it, " +
            "then run doctor again.",
        },
      };
    case "CREDENTIALS_REJECTED":
      return {
        blocked_on: "bad_credentials",
        next: {
          where: "Google Cloud",
          action:
            "The credential was rejected, which usually means the key was revoked or deleted. " +
            "Generate a new service-account key and update GA4_CREDENTIALS with it.",
        },
      };
    case "CLOCK_SKEW":
      return {
        blocked_on: "clock_skew",
        next: {
          where: "this machine",
          action:
            "Turn on automatic network time, then run doctor again. Date & Time > Set " +
            "automatically on macOS and Windows; on Linux the same setting, or " +
            "`timedatectl set-ntp true` from a terminal, which needs administrator rights " +
            "and is yours to run. Your Analytics account and credentials are fine.",
        },
      };
    case "DATA_API_DISABLED":
      return {
        blocked_on: "data_api_disabled",
        next: {
          where: "Google Cloud",
          action:
            "Enable the Google Analytics Data API for this project, wait about a minute, " +
            "then run doctor again.",
        },
        url: enableApiUrl("analyticsdata.googleapis.com"),
      };
    case "ADMIN_API_DISABLED":
      return {
        blocked_on: "admin_api_disabled",
        next: {
          where: "Google Cloud",
          action:
            "Enable the Google Analytics Admin API for this project, wait about a minute, " +
            "then run doctor again. Reports still need this only to list properties by name.",
        },
        url: enableApiUrl("analyticsadmin.googleapis.com"),
      };
    case "NO_PROPERTY_ACCESS":
      return {
        blocked_on: "no_property_grant",
        next: {
          where: "Google Analytics",
          action:
            "Open Admin, then Property access management, and add this address with the " +
            "Viewer role. This is done inside Google Analytics itself, not Google Cloud IAM.",
          paste: principal,
          role: "Viewer",
        },
        // analytics.google.com is on the reviewed, text-only host allowlist
        // in src/privacy/surface.test.ts (never fetched, only ever printed
        // for a person to open) and named in README.md's egress paragraph,
        // both updated alongside this change.
        url: "https://analytics.google.com/analytics/web/",
      };
    case "PROPERTY_NOT_FOUND":
      return {
        blocked_on: "wrong_property",
        next: {
          where: "your environment",
          action:
            "Run properties to see the numeric ids this credential can read, then correct " +
            "GA4_PROPERTY_ID (or --property). The number in the site tag (G-XXXXXXX) is a " +
            "measurement id, not a property id, and will not work here.",
        },
      };
    case "NO_PROPERTY":
      return {
        blocked_on: "no_property_selected",
        next: {
          where: "your environment",
          action:
            "Set GA4_PROPERTY_ID (or pass --property) to the numeric id of the property to use. " +
            "Run properties to list what this credential can read.",
        },
      };
    case "QUOTA_EXHAUSTED":
      return {
        blocked_on: "quota",
        next: {
          where: "Google Analytics",
          action:
            "Wait for quota to reset (daily quota resets at midnight US Pacific time; hourly " +
            "quota resets within the hour), then try again.",
        },
      };
    default: {
      // Which side of the wire this happened on is knowable from the check
      // rather than from the code: property selection is resolved entirely on
      // this machine (a property id that is not one, a property outside the
      // allowlist), and never reaches a socket. The same code can arrive from
      // the other side too, since Google's HTTP 400 is INVALID_REQUEST as
      // well, so keying on the code alone would attribute one of them wrongly.
      // Sending somebody to Google Analytics to fix an allowlist their own
      // environment enforces is the kind of wrong turn this file exists to
      // prevent.
      const decidedHere = checkId === "property_selection";
      const preamble = decidedHere
        ? "This skill refused the property itself, on this machine, and Google was never asked. " +
          "It is not one of the setup steps doctor knows how to fix"
        : "This is not one of the setup problems doctor recognizes, and the cause is not known";
      return {
        blocked_on: "unknown",
        next: {
          where: decidedHere ? "your environment" : "Google Analytics",
          action: detail
            ? `${preamble}: report the message rather than guessing a fix. Message: "${detail}"`
            : `${preamble}: report the underlying message rather than guessing a fix.`,
        },
      };
    }
  }
}

/**
 * Reduces the checks runDiagnose produced to the single step that would
 * unblock setup, in dependency order.
 *
 * Two checks never reach `mapped`, on purpose:
 *
 * - A check with no `code` at all (the privacy-settings check, which is not
 *   error-driven) is outside this taxonomy entirely: it is a standing
 *   posture, not a reason a report cannot run, so it is not treated as
 *   blocking. It is not silently dropped either: a failing one lands in
 *   `warnings`, because "your reports are unredacted" is something the agent
 *   has to be able to say, and `ok: true` with nothing beside it said the
 *   opposite.
 * - ADMIN_API_DISABLED is skipped when the "data_api_report" check
 *   specifically passed later: that is the one check that actually proves
 *   reports work. Matching on *any* later check passing is wrong: runDiagnose
 *   always appends a "privacy_settings" check after it, and that check
 *   passes on essentially every real run (redaction is on by default), which
 *   would satisfy an "any later pass" predicate whether or not reports ever
 *   ran at all. That would hide the one genuine blocking step and send
 *   someone in a loop: told to run `properties` to fix "no property
 *   selected", which fails with the same ADMIN_API_DISABLED. Matched on
 *   `id`, a stable identifier, rather than `label`, which is display text
 *   somebody will reword.
 */
export function setupStateFrom(checks: Check[], principal?: string): SetupState {
  const dataApiReportPassedLater = (fromIndex: number): boolean =>
    checks.slice(fromIndex + 1).some((check) => check.id === "data_api_report" && check.status === "pass");

  const warnings = checks
    .filter((check) => check.status === "fail" && check.code === undefined)
    .map((check) => (check.fix ? `${check.detail} ${check.fix}` : check.detail));
  const withWarnings = warnings.length > 0 ? { warnings } : {};

  for (let i = 0; i < checks.length; i += 1) {
    const check = checks[i]!;
    if (check.status !== "fail" || check.code === undefined) {
      continue;
    }
    if (check.code === "ADMIN_API_DISABLED" && dataApiReportPassedLater(i)) {
      continue;
    }
    const { blocked_on, next, url } = mapped(check.code, principal, check.detail, check.id);
    return {
      ok: false,
      blocked_on,
      ...(principal !== undefined ? { principal } : {}),
      next,
      ...(url !== undefined ? { url } : {}),
      ...withWarnings,
    };
  }

  return {
    ok: true,
    blocked_on: "ok",
    ...(principal !== undefined ? { principal } : {}),
    ...withWarnings,
  };
}
