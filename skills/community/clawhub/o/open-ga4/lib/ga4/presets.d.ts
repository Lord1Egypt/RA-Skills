import type { FilterExpression, OrderBy } from "./client.js";
/**
 * Named report shapes.
 *
 * GA4 has roughly 200 dimensions and 150 metrics with names like
 * `sessionDefaultChannelGroup` and `screenPageViews`. A model asked to invent
 * that combination gets it wrong often enough to be annoying, and every wrong
 * guess costs a round trip and a slice of the client-error budget.
 *
 * A preset turns "what are my top pages" into a field list that is known to
 * work. The escape hatch stays open: `query` takes explicit
 * dimensions and metrics for anything not covered here.
 *
 * Every apiName below survived a verification pass against Google's published
 * dimension and metric schema. Names that could not be confirmed were left out
 * rather than guessed at.
 */
export type Preset = {
    id: string;
    /** Shown to the model in the tool description, so it reads as an intent. */
    intent: string;
    kind: "core" | "realtime";
    dimensions: string[];
    metrics: string[];
    orderBys?: OrderBy[];
    dimensionFilter?: FilterExpression;
    limit: number;
    /** Appended to the rendered report when the shape needs explaining. */
    note?: string;
};
export declare const PRESETS: readonly Preset[];
export declare function findPreset(id: string): Preset | undefined;
