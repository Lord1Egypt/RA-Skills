import { type FilterCondition } from "../ga4/filters.js";
import type { Ga4Runtime } from "../runtime.js";
type ReportOutcome = {
    markdown: string;
    details: Record<string, unknown>;
};
export type ReportParams = {
    report: string;
    property_id?: string;
    date_range?: string;
    start_date?: string;
    end_date?: string;
    limit?: number;
    filter_contains?: string;
};
export declare function runReport(runtime: Ga4Runtime, params: ReportParams, signal?: AbortSignal): Promise<ReportOutcome>;
export type CompareParams = {
    report: string;
    property_id?: string;
    date_range?: string;
    limit?: number;
};
export declare function runCompare(runtime: Ga4Runtime, params: CompareParams, signal?: AbortSignal): Promise<ReportOutcome>;
export type RealtimeParams = {
    breakdown?: string;
    property_id?: string;
    limit?: number;
};
export declare function runRealtime(runtime: Ga4Runtime, params: RealtimeParams, signal?: AbortSignal): Promise<ReportOutcome>;
export type QueryParams = {
    metrics: string[];
    dimensions?: string[];
    property_id?: string;
    date_range?: string;
    start_date?: string;
    end_date?: string;
    filters?: FilterCondition[];
    order_by?: string;
    limit?: number;
};
export declare function runQuery(runtime: Ga4Runtime, params: QueryParams, signal?: AbortSignal): Promise<ReportOutcome>;
export {};
