import { type FetchLike } from "./http.js";
export type DateRange = {
    startDate: string;
    endDate: string;
    name?: string;
};
export type MinuteRange = {
    startMinutesAgo?: number;
    endMinutesAgo?: number;
    name?: string;
};
export type MatchType = "EXACT" | "BEGINS_WITH" | "ENDS_WITH" | "CONTAINS" | "FULL_REGEXP" | "PARTIAL_REGEXP";
export type Filter = {
    fieldName: string;
    stringFilter?: {
        matchType?: MatchType;
        value: string;
        caseSensitive?: boolean;
    };
    inListFilter?: {
        values: string[];
        caseSensitive?: boolean;
    };
    numericFilter?: {
        operation: string;
        value: {
            int64Value?: string;
            doubleValue?: number;
        };
    };
    betweenFilter?: {
        fromValue: unknown;
        toValue: unknown;
    };
};
export type FilterExpression = {
    andGroup?: {
        expressions: FilterExpression[];
    };
    orGroup?: {
        expressions: FilterExpression[];
    };
    notExpression?: FilterExpression;
    filter?: Filter;
};
export type OrderBy = {
    desc?: boolean;
    metric?: {
        metricName: string;
    };
    dimension?: {
        dimensionName: string;
        orderType?: "ALPHANUMERIC" | "CASE_INSENSITIVE_ALPHANUMERIC" | "NUMERIC";
    };
};
export type RunReportRequest = {
    dimensions?: Array<{
        name: string;
    }>;
    metrics?: Array<{
        name: string;
    }>;
    dateRanges?: DateRange[];
    dimensionFilter?: FilterExpression;
    metricFilter?: FilterExpression;
    orderBys?: OrderBy[];
    /** int64 on the wire: Google expects these as JSON strings. */
    limit?: string;
    offset?: string;
    keepEmptyRows?: boolean;
    returnPropertyQuota?: boolean;
};
export type MetricType = "TYPE_INTEGER" | "TYPE_FLOAT" | "TYPE_SECONDS" | "TYPE_MILLISECONDS" | "TYPE_MINUTES" | "TYPE_HOURS" | "TYPE_STANDARD" | "TYPE_CURRENCY" | "TYPE_FEET" | "TYPE_MILES" | "TYPE_METERS" | "TYPE_KILOMETERS";
export type QuotaStatus = {
    consumed?: number;
    remaining?: number;
};
/**
 * Two of these six drop "PerProperty" from their documentation label. Keying
 * off the doc-table wording silently yields `undefined`, and a client that
 * reads `undefined` never learns it is running out of quota.
 */
export type PropertyQuota = {
    tokensPerDay?: QuotaStatus;
    tokensPerHour?: QuotaStatus;
    tokensPerProjectPerHour?: QuotaStatus;
    concurrentRequests?: QuotaStatus;
    serverErrorsPerProjectPerHour?: QuotaStatus;
    potentiallyThresholdedRequestsPerHour?: QuotaStatus;
};
export declare const PROPERTY_QUOTA_FIELDS: readonly ["tokensPerDay", "tokensPerHour", "tokensPerProjectPerHour", "concurrentRequests", "serverErrorsPerProjectPerHour", "potentiallyThresholdedRequestsPerHour"];
export type ResponseMetaData = {
    dataLossFromOtherRow?: boolean;
    subjectToThresholding?: boolean;
    emptyReason?: string;
    currencyCode?: string;
    timeZone?: string;
    samplingMetadatas?: Array<{
        samplesReadCount?: string;
        samplingSpaceSize?: string;
    }>;
    schemaRestrictionResponse?: {
        activeMetricRestrictions?: Array<{
            metricName?: string;
            restrictedMetricTypes?: string[];
        }>;
    };
};
export type ReportRow = {
    dimensionValues?: Array<{
        value?: string;
    }>;
    metricValues?: Array<{
        value?: string;
    }>;
};
export type RunReportResponse = {
    dimensionHeaders?: Array<{
        name?: string;
    }>;
    metricHeaders?: Array<{
        name?: string;
        type?: MetricType;
    }>;
    rows?: ReportRow[];
    totals?: ReportRow[];
    rowCount?: number;
    metadata?: ResponseMetaData;
    propertyQuota?: PropertyQuota;
};
export type FieldMetadata = {
    apiName?: string;
    uiName?: string;
    description?: string;
    category?: string;
    customDefinition?: boolean;
    deprecatedApiNames?: string[];
    type?: MetricType;
};
export type MetadataResponse = {
    dimensions?: FieldMetadata[];
    metrics?: FieldMetadata[];
};
export type AccountSummary = {
    name?: string;
    account?: string;
    displayName?: string;
    propertySummaries?: Array<{
        property?: string;
        displayName?: string;
        propertyType?: string;
        parent?: string;
    }>;
};
export type Ga4ClientOptions = {
    getAccessToken(signal?: AbortSignal): Promise<string>;
    fetchImpl?: FetchLike;
};
export type Ga4Client = ReturnType<typeof createGa4Client>;
export declare function createGa4Client(options: Ga4ClientOptions): {
    runReport(propertyId: string, request: RunReportRequest, signal?: AbortSignal): Promise<RunReportResponse>;
    runRealtimeReport(propertyId: string, request: Omit<RunReportRequest, "dateRanges"> & {
        minuteRanges?: MinuteRange[];
    }, signal?: AbortSignal): Promise<RunReportResponse>;
    /**
     * Every dimension and metric this property supports, including the custom
     * ones defined on it. The authoritative field catalog; the skill ships no
     * hardcoded list that could go stale against a rename.
     */
    getMetadata(propertyId: string, signal?: AbortSignal): Promise<MetadataResponse>;
    /** Every property this credential can read, so nobody has to hunt for an id. */
    listAccountSummaries(signal?: AbortSignal): Promise<AccountSummary[]>;
};
/** Warn when a quota bucket is nearly gone, naming the bucket. */
export declare function quotaWarning(quota: PropertyQuota | undefined): string | undefined;
