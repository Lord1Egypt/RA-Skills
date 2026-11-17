import { appendFile } from "node:fs/promises";

/**
 * Optional local audit log.
 *
 * Off unless `privacy.auditLogPath` is set. When on, it records what was
 * *asked*, never what came back. A log that contained report rows would be
 * exactly the personal data this skill works to keep off disk, so response
 * bodies, row values and totals never reach it.
 *
 * One part of the question is held back for the same reason: a filter's value.
 * Which fields were filtered on and sorted by is recorded, because that is what
 * says whether a report was about a person at all; what they were filtered *to*
 * is not, because that is the person.
 *
 * This is the only module in the skill that writes to a file, which is what
 * makes the "no report data is written to disk" claim checkable:
 * `surface.test.ts` asserts no other shipped module calls a write API.
 *
 * The claim is worded that way rather than as "nothing is written to disk"
 * deliberately. The shorter form was what the documentation used to say, and it
 * is false the moment somebody sets `GA4_AUDIT_LOG`, which makes a promise out
 * of a default. What survives every setting is the narrower claim: no row, no
 * value and no total from a report reaches a file.
 */

export type AuditEntry = {
  tool: string;
  propertyId: string;
  dimensions?: readonly string[];
  metrics?: readonly string[];
  dateRange?: string;
  /**
   * The field names a filter narrowed the report to, and the field name it was
   * sorted by. Names only, never values.
   *
   * The dimension and metric lists above describe the shape of the answer; they
   * do not say which slice of it was asked for. A report whose columns are page
   * paths and dates can still be a report about one named person, because the
   * filter is what selects the rows and the filter field never appears as a
   * column. Recording only the columns made exactly that query indistinguishable
   * in this log from an ordinary whole-site one.
   *
   * The *value* is deliberately absent, and that is not an oversight to be
   * fixed later. A filter value is the identifier itself (a customer id, an
   * email, a URL with a token in it), so writing it here would put the personal
   * data this skill keeps off disk onto disk, in the file people enable to feel
   * safer. The field name answers "was this a question about a person" without
   * answering "which person".
   */
  filterFields?: readonly string[];
  sortField?: string;
  /** How many rows came back. A count, never a value. */
  rows?: number;
};

export type AuditLogger = {
  record(entry: AuditEntry): Promise<void>;
};

/** A logger that does nothing, used when no path is configured. */
export const NULL_AUDIT_LOGGER: AuditLogger = {
  async record(): Promise<void> {
    // Intentionally empty.
  },
};

export type AuditLoggerOptions = {
  path: string;
  now?: () => Date;
  /** Injected for tests. */
  append?: (path: string, line: string) => Promise<void>;
  onError?: (message: string) => void;
};

export function createAuditLogger(options: AuditLoggerOptions): AuditLogger {
  const now = options.now ?? (() => new Date());
  const append = options.append ?? ((path: string, line: string) => appendFile(path, line, "utf8"));

  return {
    async record(entry: AuditEntry): Promise<void> {
      const line =
        JSON.stringify({
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
      } catch (error) {
        // A failing audit log must not take analytics down. Report it once and
        // carry on: losing a log line is better than losing the answer.
        options.onError?.(
          `Could not append to the GA4 audit log at ${options.path}: ` +
            `${error instanceof Error ? error.message : String(error)}`,
        );
      }
    },
  };
}
