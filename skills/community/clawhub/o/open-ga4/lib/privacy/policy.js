import { Ga4Error } from "../ga4/errors.js";
/**
 * What the agent is allowed to ask for.
 *
 * Redaction (see `redact.ts`) cleans values on the way out. This module is the
 * other half: it refuses certain *questions* outright, before a request is
 * spent, and it resolves the property identifier that users get wrong more
 * often than anything else in GA4.
 */
/**
 * Dimensions that link a row to a specific identified person. Blocked unless
 * explicitly allowed.
 *
 * The list is deliberately short. The alternative design (prompting for
 * approval on every URL-bearing dimension) was rejected: `pagePath` is in the
 * single most common question anyone asks ("what are my top pages?"), and a
 * tool that interrupts the most common question is a tool people stop using.
 * Value redaction runs unconditionally on every row of every report instead,
 * which is where the actual leaked identifiers live.
 */
const USER_IDENTIFYING_EXACT = new Set(["userId", "signedInWithUserId"]);
/**
 * User-scoped custom dimensions: the field teams reach for when they want to
 * join analytics back to a person, so in practice these hold CRM ids, account
 * ids and hashed emails.
 */
const USER_IDENTIFYING_PREFIXES = ["customUser:"];
/**
 * Dimensions whose values are visitor-authored, URL-derived, or hand-written
 * by marketers. Not blocked (they are the useful ones), but they are why
 * redaction is on by default and why results are marked as untrusted network
 * content: a stranger can put text in any of them by visiting a URL.
 *
 * **This list is not exhaustive, and nothing depends on it being.** Read that
 * before adding a check that assumes otherwise. Redaction runs on every value of
 * every dimension column, and the untrusted-content framing is attached to every
 * row of every report, both regardless of class (see src/ga4/format.ts), so a
 * dimension missing from here is protected exactly as much as one listed. What
 * the class is for is documentation and the `fields` listing: it records which
 * dimensions are *known* to carry text a stranger wrote, so nobody has to
 * rediscover it.
 *
 * Enumerating the full set is not achievable. `eventName` is the plain example
 * and is listed below: the GA4 `collect` endpoint accepts an arbitrary event
 * name from anyone holding the measurement id, which is public by construction,
 * sitting in the tag on the site. Every event parameter that becomes a
 * dimension has the same property. A list that claimed completeness would be
 * making a promise about Google's ingestion surface that this repository is in
 * no position to keep.
 */
const FREE_TEXT_PREFIXES = ["customEvent:", "customItem:", "sessionCustomChannelGroup:"];
const FREE_TEXT_EXACT = new Set([
    // Injectable through the collect endpoint with nothing but the public
    // measurement id, no visit to the site required.
    "eventName",
    "pagePath",
    "pagePathPlusQueryString",
    "pageLocation",
    "fullPageUrl",
    "pageTitle",
    "pageReferrer",
    "landingPage",
    "landingPagePlusQueryString",
    "unifiedPagePathScreen",
    "unifiedPageScreen",
    "unifiedScreenName",
    "unifiedScreenClass",
    "hostName",
    "linkUrl",
    "linkText",
    "linkDomain",
    "fileName",
    "searchTerm",
    "manualTerm",
    "sessionManualTerm",
    "sessionManualAdContent",
    "googleAdsKeyword",
    "campaignName",
    "sessionCampaignName",
    "firstUserCampaignName",
    "transactionId",
    "orderCoupon",
    "itemName",
]);
/**
 * Dimensions Google's own thresholding exists to protect. Allowed, because
 * marketers legitimately report on them, but a report using one always carries
 * the thresholding caveat: small cohorts may be silently withheld.
 */
export const THRESHOLD_PRONE_DIMENSIONS = [
    "userAgeBracket",
    "userGender",
    "brandingInterest",
    "audienceId",
    "audienceName",
    "audienceResourceName",
];
/**
 * @param propertyIdentifying Names this property, specifically, treats as
 *   person-identifying, from `userIdentifyingDimensionNames` below: its
 *   user-scoped custom definitions, and every deprecated alias of anything the
 *   static rules block. Supplying these from a live `getMetadata` response means
 *   a custom dimension created on a property *after* this skill shipped, or an
 *   old spelling Google still accepts, is classified correctly with no skill
 *   update. Empty is a valid argument: the static rules above are the gate, and
 *   this sharpens them.
 */
export function classifyDimension(name, propertyIdentifying = new Set()) {
    if (USER_IDENTIFYING_EXACT.has(name) ||
        USER_IDENTIFYING_PREFIXES.some((prefix) => name.startsWith(prefix)) ||
        propertyIdentifying.has(name)) {
        return "user-identifying";
    }
    if (FREE_TEXT_EXACT.has(name) || FREE_TEXT_PREFIXES.some((prefix) => name.startsWith(prefix))) {
        return "free-text";
    }
    return "ordinary";
}
/**
 * Every name this property will answer to for a dimension the rules above call
 * person-identifying, deprecated aliases included.
 *
 * The rules above match on a name, and a GA4 property answers to more than one
 * name per dimension: `getMetadata` returns `deprecatedApiNames` alongside
 * `apiName`, and the API still accepts the old spellings. That field was parsed
 * and never consulted, which left the check name-complete only by luck. Two ways
 * for a name to slip past, and this closes both by treating a dimension's names
 * as one group that stands or falls together:
 *
 * - An alias for a blocked dimension. Metadata says `apiName: "userId"` with a
 *   deprecated `"uid"`; `--dimensions uid` classified as ordinary and Google
 *   accepted it.
 * - A rename *of* a blocked dimension. Metadata says `apiName: "personId"` with
 *   a deprecated `"userId"`; the new name is unknown to the rules, and it is the
 *   same dimension.
 *
 * Fed to `classifyDimension` as its `propertyIdentifying` argument, which is why
 * that parameter is a set of names rather than a predicate: it already existed
 * for live custom definitions, and this is more of the same thing, names this
 * property treats as person-identifying that a shipped list cannot know.
 */
export function userIdentifyingDimensionNames(dimensions) {
    const blocked = new Set();
    for (const dimension of dimensions) {
        const names = [dimension.apiName, ...(dimension.deprecatedApiNames ?? [])].filter((name) => typeof name === "string" && name.length > 0);
        // Any one of a dimension's names being blocked blocks all of them: they name
        // the same column, so the safe answer is the same for each.
        if (names.some((name) => classifyDimension(name) === "user-identifying")) {
            for (const name of names) {
                blocked.add(name);
            }
        }
    }
    return blocked;
}
/** Dimensions in this request that make Google's thresholding likely. */
export function thresholdProneDimensions(dimensions) {
    return dimensions.filter((name) => THRESHOLD_PRONE_DIMENSIONS.includes(name));
}
export const DEFAULT_ACCESS_POLICY = {
    allowUserIdentifyingDimensions: false,
    propertyAllowlist: [],
};
/**
 * A refusal this skill made locally: a dimension it will not ask for, a
 * property outside the allowlist, an identifier that is not a property id.
 *
 * Extends Ga4Error, rather than a plain Error, for the same reason
 * Ga4RequestError in src/ga4/limits.ts does (read the comment there; this is
 * the same defect, found again in a second class that was not brought along
 * with the first). Anything that is not a Ga4Error falls through diagnose()
 * into the generic "UNEXPECTED" bucket, whose fix is "Run doctor to check the
 * setup" and whose exit code says Google refused the request. None of these
 * ever reach a socket: attributing this skill's own privacy refusal to Google
 * is both false and unfixable by the person who reads it.
 *
 * `code` is per-throw rather than fixed, because these are not all the same
 * kind of problem:
 *
 * - INVALID_REQUEST (exit 2) for a value the caller can correct: a blocked
 *   dimension, a property outside the allowlist, a string that is no kind of
 *   Google identifier at all.
 * - PROPERTY_NOT_FOUND (exit 3) for a measurement id or a Google tag/Ads id.
 *   Those identify something real in Google's world but not a property, and
 *   they are what people paste because it is the id on their own site. That
 *   code is what makes `doctor --json` report `blocked_on: "wrong_property"`,
 *   the setup step written for exactly this mistake, so the agent gets the
 *   conversation the state machine already has an answer for.
 * - NO_PROPERTY (exit 3) for a blank one, matching src/runtime.ts's own
 *   NO_PROPERTY when nothing was configured at all.
 */
export class PolicyError extends Ga4Error {
    constructor(message, options = {}) {
        super(options.code ?? "INVALID_REQUEST", message, options.fix ??
            "This skill decided that locally, before any request reached Google. Change the value " +
                "named above, or the setting that refuses it, and try again.");
        this.name = "PolicyError";
    }
}
/** The sentence that explains why a name off the column list still counts. */
function whyItStillCounts(use, names, one) {
    const it = one ? "it" : "them";
    const isAre = one ? "is" : "are";
    switch (use) {
        case "filter":
            return (`Filtering on ${names} asks for the rows belonging to particular people, so the numbers ` +
                `that come back describe those people even though ${names} ${isAre} not among the columns ` +
                `the report returns. Leaving ${it} out of the dimension list does not make this an ` +
                `aggregate question, and a filter value is itself personal data, so it is refused here too. `);
        case "sort":
            return (`Sorting by ${names} orders the report by which person each row belongs to, so it asks ` +
                `for person-level data even though ${names} ${isAre} not among the columns the report ` +
                `returns. `);
        case "columns":
            return "";
    }
}
/**
 * Refuse a query that asks for person-level dimensions, naming the opt-in.
 *
 * Called on every channel a dimension name can travel through, not only the
 * output column list: see `buildFilters` and `buildOrderBys` in
 * src/ga4/filters.ts. A gate on the column list alone was bypassable, and in
 * the worst way, because the refusal it left in place made the skill look like
 * it was enforcing something it was not.
 */
export function assertDimensionsAllowed(dimensions, policy, propertyIdentifying = new Set(), use = "columns") {
    if (policy.allowUserIdentifyingDimensions) {
        return;
    }
    const blocked = dimensions.filter((name) => classifyDimension(name, propertyIdentifying) === "user-identifying");
    if (blocked.length === 0) {
        return;
    }
    const one = blocked.length === 1;
    const it = one ? "it" : "them";
    const names = blocked.join(", ");
    throw new PolicyError(`${names} ${one ? "identifies" : "identify"} individual people, ` +
        `so this skill does not request ${it} by default. ` +
        whyItStillCounts(use, names, one) +
        `To allow ${it}, set the environment variable ` +
        `GA4_ALLOW_USER_DIMENSIONS to true. ` +
        `For counts of people, use the totalUsers or activeUsers metric instead; ` +
        `it answers "how many" without naming anyone.`, {
        fix: use === "columns"
            ? "This skill refused the question on this machine; Google was never asked. Ask for the " +
                "same numbers without that dimension, or have a person set the variable named above."
            : "This skill refused the question on this machine; Google was never asked. Ask the same " +
                "question without narrowing it to a person (a whole-site or per-page total, or the " +
                "activeUsers metric for how many), or have a person set the variable named above.",
    });
}
export function assertPropertyAllowed(propertyId, policy) {
    if (policy.propertyAllowlist.length === 0) {
        return;
    }
    if (!policy.propertyAllowlist.includes(propertyId)) {
        throw new PolicyError(`Property ${propertyId} is not in this skill's allowlist ` +
            `(${policy.propertyAllowlist.join(", ")}). Add it to the comma-separated ` +
            `GA4_PROPERTY_ALLOWLIST environment variable to query it.`, {
            fix: "Nothing was sent to Google: the allowlist is enforced on this machine. Ask for one of " +
                "the properties it names, or have a person widen GA4_PROPERTY_ALLOWLIST.",
        });
    }
}
const MEASUREMENT_ID = /^G-[A-Z0-9]+$/i;
const STREAM_OR_TAG_ID = /^(?:GT|AW|DC)-[A-Z0-9]+$/i;
const NUMERIC_ID = /^\d{6,}$/;
/**
 * Turn whatever the user pasted into a bare numeric property id.
 *
 * The measurement id (`G-XXXXXXX`) is the string people see most often (it is
 * in the tag on their site), and it is *not* the property id the API wants.
 * Getting this wrong produces an opaque 403, so it is worth its own message.
 */
export function normalizePropertyId(input) {
    const value = input.trim();
    if (!value) {
        throw new PolicyError("No GA4 property id. Run properties to list the ones this credential can read.", {
            code: "NO_PROPERTY",
            fix: "Pass --property, or set the GA4_PROPERTY_ID environment variable. " +
                "Run properties to list the ones this credential can read.",
        });
    }
    const withoutPrefix = value.replace(/^properties\//, "");
    if (NUMERIC_ID.test(withoutPrefix)) {
        return withoutPrefix;
    }
    // A measurement id and a tag or Ads id both name something real in Google's
    // world, just not a property, and both are the id somebody has in front of
    // them (it is in the tag on their own site). PROPERTY_NOT_FOUND is what
    // src/setup/state.ts turns into the `wrong_property` step, whose text names
    // this exact mistake. Anything else below is a value that identifies nothing
    // at all, which is ordinary bad input.
    const WRONG_KIND_OF_ID_FIX = "Run properties to list the numeric property ids this credential can read, then use one of " +
        "those, in --property or in GA4_PROPERTY_ID. Nothing was sent to Google.";
    if (MEASUREMENT_ID.test(value)) {
        throw new PolicyError(`"${value}" is a measurement id, which identifies a data stream rather than a property, ` +
            `and the reporting API cannot use it. You need the numeric property id: the ~9-digit ` +
            `number shown under Admin > Property details, or in the URL as p123456789. ` +
            `Run properties to list yours.`, { code: "PROPERTY_NOT_FOUND", fix: WRONG_KIND_OF_ID_FIX });
    }
    if (STREAM_OR_TAG_ID.test(value)) {
        throw new PolicyError(`"${value}" is a Google tag or Ads id, not a GA4 property id. ` +
            `Run properties to list the numeric property ids this credential can read.`, { code: "PROPERTY_NOT_FOUND", fix: WRONG_KIND_OF_ID_FIX });
    }
    throw new PolicyError(`"${value}" is not a GA4 property id. Expected a numeric id such as 123456789. ` +
        `Run properties to list the ones this credential can read.`);
}
