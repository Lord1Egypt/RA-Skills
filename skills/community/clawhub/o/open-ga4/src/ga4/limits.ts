import { assertDimensionsAllowed, type AccessPolicy } from "../privacy/policy.js";
import { Ga4Error } from "./errors.js";

/**
 * Request limits and the metric renames, enforced before a socket is opened.
 *
 * Failing locally matters more than it looks: Google counts client errors
 * against a budget of 10,000 per 15 minutes per project-and-property pair, and
 * exhausting it blocks that pair entirely. A request we know is invalid must
 * never be sent.
 */

export const LIMITS = {
  /** Google's documented per-request ceilings. */
  MAX_DIMENSIONS: 9,
  MAX_METRICS: 10,
  MAX_DATE_RANGES: 4,
  MAX_MINUTE_RANGES: 2,
  ROW_LIMIT_MAX: 250_000,
  ROW_LIMIT_DEFAULT: 10_000,
  MINUTES_AGO_MAX: 29,

  /** Our own, tighter ceilings, so a report stays readable and cheap in tokens. */
  DEFAULT_ROWS: 25,
  MAX_ROWS: 1_000,
} as const;

/**
 * Names Google retired, mapped to their replacements.
 *
 * Models were trained on years of documentation using the old names, so
 * `conversions` is what they reach for. Rewriting silently is kinder than a
 * 400, and the rewrite is reported in the result so nobody is misled about
 * which metric was actually read.
 */
export const RENAMED_FIELDS: Readonly<Record<string, string>> = {
  conversions: "keyEvents",
  sessionConversionRate: "sessionKeyEventRate",
  userConversionRate: "userKeyEventRate",
  purchaserConversionRate: "purchaserRate",
  firstTimePurchaserConversionRate: "firstTimePurchaserRate",
  advertiserAdCostPerConversion: "advertiserAdCostPerKeyEvent",
  isConversionEvent: "isKeyEvent",
  pageViews: "screenPageViews",
  pageviews: "screenPageViews",
  users: "totalUsers",
  uniqueUsers: "totalUsers",
};

export type FieldRewrite = { from: string; to: string };

/** Apply the rename table, reporting what changed. */
export function applyRenames(names: readonly string[]): {
  names: string[];
  rewrites: FieldRewrite[];
} {
  const rewrites: FieldRewrite[] = [];
  const mapped = names.map((name) => {
    const replacement = RENAMED_FIELDS[name];
    if (replacement && replacement !== name) {
      rewrites.push({ from: name, to: replacement });
      return replacement;
    }
    return name;
  });
  return { names: mapped, rewrites };
}

/**
 * A request the client can already tell Google would reject: too many
 * dimensions, an empty request, a filter value that will not parse, and so on.
 *
 * Extends Ga4Error, rather than a plain Error, so it carries the same exit
 * code as every other bad-input failure: `code` is fixed at INVALID_REQUEST,
 * which exitCodeFor already maps to exit 2. Before this, a plain Error here
 * fell through diagnose()'s generic "UNEXPECTED" bucket and read as a refusal
 * from Google that was never asked for; nothing here ever reaches a network
 * call. `reason` keeps the specific check that failed (EMPTY_REQUEST,
 * TOO_MANY_DIMENSIONS, BAD_FILTER_VALUE, ...) for anyone who wants more detail
 * than "invalid request"; it does not affect the exit code.
 */
export class Ga4RequestError extends Ga4Error {
  constructor(
    readonly reason: string,
    message: string,
  ) {
    super(
      "INVALID_REQUEST",
      message,
      "This was caught locally, before any request reached Google. Fix the value named above and try again.",
    );
    this.name = "Ga4RequestError";
  }
}

export type ReportShape = {
  dimensions: readonly string[];
  metrics: readonly string[];
  dateRangeCount?: number;
  limit?: number;
};

/** Reject a request Google would reject, with a message that says what to do. */
export function assertWithinLimits(shape: ReportShape): void {
  if (shape.dimensions.length === 0 && shape.metrics.length === 0) {
    throw new Ga4RequestError(
      "EMPTY_REQUEST",
      "A report needs at least one metric. Try the 'overview' preset for headline numbers.",
    );
  }
  if (shape.dimensions.length > LIMITS.MAX_DIMENSIONS) {
    throw new Ga4RequestError(
      "TOO_MANY_DIMENSIONS",
      `Google Analytics allows ${LIMITS.MAX_DIMENSIONS} dimensions per report; this asks for ` +
        `${shape.dimensions.length} (${shape.dimensions.join(", ")}). Split it into separate reports.`,
    );
  }
  if (shape.metrics.length > LIMITS.MAX_METRICS) {
    throw new Ga4RequestError(
      "TOO_MANY_METRICS",
      `Google Analytics allows ${LIMITS.MAX_METRICS} metrics per report; this asks for ` +
        `${shape.metrics.length} (${shape.metrics.join(", ")}). Split it into separate reports.`,
    );
  }
  if ((shape.dateRangeCount ?? 1) > LIMITS.MAX_DATE_RANGES) {
    throw new Ga4RequestError(
      "TOO_MANY_DATE_RANGES",
      `Google Analytics allows ${LIMITS.MAX_DATE_RANGES} date ranges per report; this asks for ` +
        `${shape.dateRangeCount}.`,
    );
  }
  if (shape.limit !== undefined) {
    if (!Number.isInteger(shape.limit) || shape.limit < 1) {
      throw new Ga4RequestError("BAD_LIMIT", `limit must be a whole number of rows; got ${shape.limit}.`);
    }
    if (shape.limit > LIMITS.MAX_ROWS) {
      throw new Ga4RequestError(
        "LIMIT_TOO_LARGE",
        `This skill returns at most ${LIMITS.MAX_ROWS} rows per report, to keep results readable ` +
          `and quota use low; ${shape.limit} were requested. Narrow the query, or page with offset.`,
      );
    }
  }
}

/**
 * Realtime accepts a small, fixed subset of fields. Rejecting locally turns an
 * opaque 400 into a sentence naming what realtime can actually do.
 */
export const REALTIME_DIMENSIONS: ReadonlySet<string> = new Set([
  "appVersion",
  "audienceId",
  "audienceName",
  "audienceResourceName",
  "city",
  "cityId",
  "country",
  "countryId",
  "deviceCategory",
  "eventName",
  "minutesAgo",
  "platform",
  "streamId",
  "streamName",
  "unifiedScreenName",
]);

export const REALTIME_METRICS: ReadonlySet<string> = new Set([
  "activeUsers",
  "eventCount",
  "keyEvents",
  "screenPageViews",
]);

/**
 * Realtime's own custom-dimension form, and the reason the privacy policy has to
 * run here too.
 *
 * `customUser:<name>` is the field a team reaches for when joining analytics
 * back to a person, so in practice it holds CRM ids, account ids and hashed
 * emails: precisely what src/privacy/policy.ts refuses by default. This pattern
 * *permits* it, because realtime does accept it and a local refusal claiming
 * otherwise would be wrong. Whether it may be asked for is a different question
 * from whether the API has it, and that one is the policy's.
 */
const REALTIME_CUSTOM_DIMENSION = /^customUser:[A-Za-z0-9_]+$/;

/**
 * Everything realtime refuses locally: fields it does not have, and fields it
 * has but that this skill will not ask for by default.
 *
 * The policy check is here rather than at the call site for the reason
 * buildFilters holds its own: the caller that skips it is the defect, and a
 * required argument is what stops one being written. runRealtime was that
 * caller. Nothing could exploit it, because `live` takes only a preset id and
 * every realtime preset's dimensions are constants, but the check was missing
 * from the one command that has a permissive `customUser:` rule of its own,
 * which is the worst place for it to be missing from.
 */
export function assertRealtimeFields(
  dimensions: readonly string[],
  metrics: readonly string[],
  policy: AccessPolicy,
  propertyIdentifying: ReadonlySet<string> = new Set(),
): void {
  assertDimensionsAllowed(dimensions, policy, propertyIdentifying);

  const badDimensions = dimensions.filter(
    (name) => !REALTIME_DIMENSIONS.has(name) && !REALTIME_CUSTOM_DIMENSION.test(name),
  );
  if (badDimensions.length > 0) {
    throw new Ga4RequestError(
      "REALTIME_DIMENSION_UNAVAILABLE",
      `Realtime reporting does not have ${badDimensions.join(", ")}. It has only: ` +
        `${[...REALTIME_DIMENSIONS].join(", ")} (plus customUser:<name>). ` +
        `There are no page, traffic-source, or browser dimensions in realtime at all. ` +
        `For those, run a normal report over a recent date range instead.`,
    );
  }
  const badMetrics = metrics.filter((name) => !REALTIME_METRICS.has(name));
  if (badMetrics.length > 0) {
    throw new Ga4RequestError(
      "REALTIME_METRIC_UNAVAILABLE",
      `Realtime reporting does not have ${badMetrics.join(", ")}. It has only: ` +
        `${[...REALTIME_METRICS].join(", ")}. There is no sessions metric in realtime. ` +
        `For those, run a normal report over a recent date range instead.`,
    );
  }
}
