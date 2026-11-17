export declare const EXIT: {
    readonly OK: 0;
    readonly UNEXPECTED: 1;
    readonly BAD_INPUT: 2;
    readonly SETUP_INCOMPLETE: 3;
    readonly GOOGLE_REFUSED: 4;
};
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
export declare function exitCodeFor(error: unknown): number;
