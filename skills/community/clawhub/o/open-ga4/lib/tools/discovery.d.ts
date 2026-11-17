import type { Ga4Runtime } from "../runtime.js";
export type FieldsParams = {
    query: string;
    kind?: "any" | "dimension" | "metric";
    property_id?: string;
    limit?: number;
};
export declare function runFields(runtime: Ga4Runtime, params: FieldsParams, signal?: AbortSignal): Promise<{
    markdown: string;
    details: unknown;
}>;
/**
 * One of runDiagnose's five checks, stable across a reword of `label`
 * (display text somebody will reword). src/setup/state.ts matches on this,
 * not on `label`, for exactly one decision: whether a later check proves
 * reports work despite a disabled Admin API. A label match there would
 * silently break the day the label's wording changed.
 */
export type CheckId = "credentials" | "admin_api" | "property_selection" | "data_api_report" | "privacy_settings";
/**
 * `code` is the Ga4Error code behind a "fail", when there was one. It is what
 * src/setup/state.ts keys on to build `doctor --json`'s machine-readable
 * state: undefined for a check that is not error-driven at all (the privacy
 * settings check below never sets it), present for everything else.
 */
export type Check = {
    id: CheckId;
    label: string;
    status: "pass" | "fail" | "skip";
    detail: string;
    fix?: string;
    code?: string;
};
export type PropertiesParams = Record<string, never>;
/**
 * The GA4 properties a credential can read. Setup needs this before any
 * report is possible, and doctor lists the same properties as one of
 * its checks, so both call this rather than each parsing account summaries
 * on their own.
 */
export declare function runProperties(runtime: Ga4Runtime, _params: PropertiesParams, signal?: AbortSignal): Promise<{
    markdown: string;
    details: unknown;
}>;
export type DiagnoseParams = {
    property_id?: string;
};
export declare function runDiagnose(runtime: Ga4Runtime, params: DiagnoseParams, signal?: AbortSignal): Promise<{
    markdown: string;
    details: unknown;
}>;
