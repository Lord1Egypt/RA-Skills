export type SourceType =
  | 'slack'
  | 'github'
  | 'calendar'
  | 'notion'
  | 'trello'
  | 'email';

export type Status =
  | 'open'
  | 'in_progress'
  | 'waiting'
  | 'done'
  | 'snoozed';

export interface ActionItem {
  id: string;
  source: string;
  sourceType: SourceType;
  title: string;
  summary: string;
  owner: string;
  participants: string[];
  createdAt: string;
  updatedAt: string;
  dueAt: string | null;
  url: string;
  status: Status;
  priorityScore: number;
  blocker: string | null;
  replyDraft: string | null;
  followUpQuestion: string | null;
  suggestedNextAction: string | null;
  dedupeKeys: string[];
  confidence: number;
}

export interface SkippedSource {
  sourceName: string;
  reason: string;
}

export interface ItemCounts {
  total: number;
  afterDedupe: number;
  byTier: Record<string, number>;
}

export interface ActionBoard {
  generatedAt: string;
  totalItems: number;
  tiers: {
    urgent: ActionItem[];
    active: ActionItem[];
    low: ActionItem[];
  };
  metadata: {
    tierThresholds: {
      urgent: number;
      active: number;
    };
  };
}

export interface PipelineResult {
  markdown: string;
  actionBoard: ActionBoard;
  skippedSources: SkippedSource[];
  counts: ItemCounts;
}
