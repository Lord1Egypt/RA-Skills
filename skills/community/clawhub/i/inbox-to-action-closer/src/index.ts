import type { ActionItem, ActionBoard, PipelineResult, SkippedSource, ItemCounts } from './types.js';
import { deduplicateItems } from './dedupe.js';
import { scoreItems } from './score.js';
import { renderMarkdown, groupByTier, URGENT_THRESHOLD, ACTIVE_THRESHOLD } from './render.js';

export interface RawSourceInput {
  name: string;
  data: unknown;
  normalize: (raw: unknown) => ActionItem[];
}

export async function runPipeline(sources: RawSourceInput[]): Promise<PipelineResult> {
  const allItems: ActionItem[] = [];
  const skippedSources: SkippedSource[] = [];

  for (const source of sources) {
    try {
      const items = source.normalize(source.data);
      allItems.push(...items);
    } catch (error: unknown) {
      const reason = error instanceof Error ? error.message : String(error);
      skippedSources.push({ sourceName: source.name, reason });
    }
  }

  const totalBeforeDedupe = allItems.length;

  const deduped = deduplicateItems(allItems);
  const scored = scoreItems(deduped);

  scored.sort((a, b) => b.priorityScore - a.priorityScore);

  const markdown = renderMarkdown(scored);
  const tiers = groupByTier(scored);

  const actionBoard: ActionBoard = {
    generatedAt: new Date().toISOString(),
    totalItems: scored.length,
    tiers: {
      urgent: tiers.urgent,
      active: tiers.active,
      low: tiers.low,
    },
    metadata: {
      tierThresholds: {
        urgent: URGENT_THRESHOLD,
        active: ACTIVE_THRESHOLD,
      },
    },
  };

  const counts: ItemCounts = {
    total: totalBeforeDedupe,
    afterDedupe: scored.length,
    byTier: {
      urgent: tiers.urgent.length,
      active: tiers.active.length,
      low: tiers.low.length,
    },
  };

  return { markdown, actionBoard, skippedSources, counts };
}
