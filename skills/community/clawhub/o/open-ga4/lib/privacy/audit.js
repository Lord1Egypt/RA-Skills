import { appendFile } from "node:fs/promises";
/** A logger that does nothing, used when no path is configured. */
export const NULL_AUDIT_LOGGER = {
    async record() {
        // Intentionally empty.
    },
};
export function createAuditLogger(options) {
    const now = options.now ?? (() => new Date());
    const append = options.append ?? ((path, line) => appendFile(path, line, "utf8"));
    return {
        async record(entry) {
            const line = JSON.stringify({
                time: now().toISOString(),
                tool: entry.tool,
                property: entry.propertyId,
                ...(entry.dimensions?.length ? { dimensions: [...entry.dimensions] } : {}),
                ...(entry.metrics?.length ? { metrics: [...entry.metrics] } : {}),
                ...(entry.filterFields?.length ? { filterFields: [...entry.filterFields] } : {}),
                ...(entry.sortField ? { sortField: entry.sortField } : {}),
                ...(entry.dateRange ? { dateRange: entry.dateRange } : {}),
                ...(entry.rows === undefined ? {} : { rows: entry.rows }),
            }) + "\n";
            try {
                await append(options.path, line);
            }
            catch (error) {
                // A failing audit log must not take analytics down. Report it once and
                // carry on: losing a log line is better than losing the answer.
                options.onError?.(`Could not append to the GA4 audit log at ${options.path}: ` +
                    `${error instanceof Error ? error.message : String(error)}`);
            }
        },
    };
}
