import { Ga4Error } from "../ga4/errors.js";
export const EXIT = {
    OK: 0,
    UNEXPECTED: 1,
    BAD_INPUT: 2,
    SETUP_INCOMPLETE: 3,
    GOOGLE_REFUSED: 4,
};
/**
 * Codes that mean "you have not finished setting this up", not "Google said no".
 *
 * CREDENTIALS_MISSING is the single code for a missing credential: both
 * src/ga4/errors.ts and src/runtime.ts raise it, so there is exactly one
 * branch to reach here, not two.
 */
const SETUP_CODES = new Set([
    "CREDENTIALS_MISSING",
    "CREDENTIALS_REJECTED",
    "CLOCK_SKEW",
    "DATA_API_DISABLED",
    "ADMIN_API_DISABLED",
    "NO_PROPERTY_ACCESS",
    "NO_PROPERTY",
    "PROPERTY_NOT_FOUND",
]);
/**
 * Codes that are not an answer from Google and not something the caller can
 * correct: a failure diagnose() could not name at all, and a request the
 * egress guard refused to make (which can only happen if the skill tried to
 * reach a host that is not in its own source). Exit 1 is for "something broke
 * and nobody can say what", which is what both of these are.
 *
 * Until this set existed, UNEXPECTED landed on exit 4 with everything else,
 * which meant exit 1 was documented in SKILL.md and unreachable in code (every
 * error is converted to a Ga4Error before it gets here, so the `instanceof`
 * fallback below never fires in practice), while an internal failure was
 * reported to the user as a refusal from Google.
 */
const INTERNAL_CODES = new Set(["UNEXPECTED", "EGRESS_BLOCKED"]);
/**
 * Exit 4 is reserved for an answer that came back from Google.
 *
 * INVALID_REQUEST is the one code raised on both sides of the network: this
 * skill's own pre-flight checks use it, and so does Google's HTTP 400 ("that
 * query is invalid"). Both are exit 2, because the response to both is the
 * same and it is not the response exit 4 asks for: the query has to change,
 * and guessing again is the wrong move. SKILL.md's table says so rather than
 * claiming exit 2 is always local.
 */
export function exitCodeFor(error) {
    if (error instanceof Ga4Error) {
        if (SETUP_CODES.has(error.code))
            return EXIT.SETUP_INCOMPLETE;
        if (error.code === "INVALID_REQUEST")
            return EXIT.BAD_INPUT;
        if (INTERNAL_CODES.has(error.code))
            return EXIT.UNEXPECTED;
        return EXIT.GOOGLE_REFUSED;
    }
    return EXIT.UNEXPECTED;
}
