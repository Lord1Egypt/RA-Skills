import { guardedFetch } from "./http.js";
/**
 * The Google Analytics REST surface this skill uses, all of it.
 *
 * Five read methods, no writes. Hand-written against the v1beta discovery
 * documents rather than generated from protos, so the whole client is one
 * readable file and adding a call is a visible diff.
 */
const DATA_API = "https://analyticsdata.googleapis.com/v1beta";
const ADMIN_API = "https://analyticsadmin.googleapis.com/v1beta";
export const PROPERTY_QUOTA_FIELDS = [
    "tokensPerDay",
    "tokensPerHour",
    "tokensPerProjectPerHour",
    "concurrentRequests",
    "serverErrorsPerProjectPerHour",
    "potentiallyThresholdedRequestsPerHour",
];
export function createGa4Client(options) {
    async function call(url, body, signal) {
        return guardedFetch(url, {
            body,
            accessToken: await options.getAccessToken(signal),
            fetchImpl: options.fetchImpl,
            signal,
        });
    }
    return {
        async runReport(propertyId, request, signal) {
            return (await call(`${DATA_API}/properties/${propertyId}:runReport`, { ...request, returnPropertyQuota: true }, signal));
        },
        async runRealtimeReport(propertyId, request, signal) {
            return (await call(`${DATA_API}/properties/${propertyId}:runRealtimeReport`, { ...request, returnPropertyQuota: true }, signal));
        },
        /**
         * Every dimension and metric this property supports, including the custom
         * ones defined on it. The authoritative field catalog; the skill ships no
         * hardcoded list that could go stale against a rename.
         */
        async getMetadata(propertyId, signal) {
            return (await guardedFetch(`${DATA_API}/properties/${propertyId}/metadata`, {
                accessToken: await options.getAccessToken(signal),
                fetchImpl: options.fetchImpl,
                signal,
            }));
        },
        /** Every property this credential can read, so nobody has to hunt for an id. */
        async listAccountSummaries(signal) {
            const summaries = [];
            let pageToken;
            do {
                const query = new URLSearchParams({ pageSize: "200" });
                if (pageToken) {
                    query.set("pageToken", pageToken);
                }
                const page = (await guardedFetch(`${ADMIN_API}/accountSummaries?${query}`, {
                    accessToken: await options.getAccessToken(signal),
                    fetchImpl: options.fetchImpl,
                    signal,
                }));
                summaries.push(...(page.accountSummaries ?? []));
                pageToken = page.nextPageToken;
            } while (pageToken);
            return summaries;
        },
    };
}
/** Warn when a quota bucket is nearly gone, naming the bucket. */
export function quotaWarning(quota) {
    if (!quota) {
        return undefined;
    }
    for (const field of PROPERTY_QUOTA_FIELDS) {
        const status = quota[field];
        if (status?.remaining === undefined || status.consumed === undefined) {
            continue;
        }
        const total = status.remaining + status.consumed;
        if (total > 0 && status.remaining / total < 0.1) {
            return (`Google Analytics quota "${field}" for this property is below 10% remaining ` +
                `(${status.remaining} left). Further reports may start failing until it resets.`);
        }
    }
    return undefined;
}
