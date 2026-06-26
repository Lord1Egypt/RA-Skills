export type RecordId = string & { readonly __brand: 'RecordId' };

export type RecordKind = 'fact' | 'goal' | 'speculation';

export interface ProvenanceInfo {
  sourceId: string;
  sourceLabel: string;
  capturedAt: string;
  confidence?: number;
}

export interface MemoryRecord {
  id: RecordId;
  kind: RecordKind;
  entity: string;
  content: string;
  timestamp: string;
  provenance: ProvenanceInfo[];
  tags?: string[];
  /** Set to 'resolved' to exclude this record from conflict detection. */
  resolution?: string;
  /** ISO timestamp set when the record's conflict was resolved; also excludes it from detection. */
  resolvedAt?: string;
}

export interface SchemaViolation {
  recordId: RecordId;
  field: string;
  message: string;
}

export interface ConflictPair {
  a: MemoryRecord;
  b: MemoryRecord;
  reason: string;
}

export interface AdjudicationReport {
  input_count: number;
  deduped_count: number;
  classified: Record<RecordKind, number>;
  readonly conflicts: readonly ConflictPair[];
  readonly archived: readonly MemoryRecord[];
  readonly schema_violations: readonly SchemaViolation[];
  readonly provenance_chain: readonly ProvenanceInfo[];
}
