import type { MemoryRecord, RecordId, ProvenanceInfo } from './types';

export interface MergeRecord {
  canonical: RecordId;
  absorbed: RecordId[];
  strategy: 'name+type';
}

/** Jaccard similarity over word bags, range [0, 1]. */
function contentSimilarity(a: string, b: string): number {
  const words = (s: string) =>
    new Set(s.toLowerCase().replace(/[^a-z0-9\s]/g, '').split(/\s+/).filter(Boolean));
  const wa = words(a);
  const wb = words(b);
  const intersection = [...wa].filter(w => wb.has(w)).length;
  const union = new Set([...wa, ...wb]).size;
  return union === 0 ? 1 : intersection / union;
}

const SIMILARITY_THRESHOLD = 0.8;

function normalizeKey(record: MemoryRecord): string {
  return `${record.kind}::${record.entity.toLowerCase().trim().replace(/\s+/g, ' ')}`;
}

function electCanonical(group: MemoryRecord[]): MemoryRecord {
  return group.reduce((best, current) => {
    const cmp = best.timestamp.localeCompare(current.timestamp);
    if (cmp < 0) return best;
    if (cmp > 0) return current;
    return best.id <= current.id ? best : current;
  });
}

function mergeProvenance(group: MemoryRecord[]): ProvenanceInfo[] {
  const seen = new Set<string>();
  const result: ProvenanceInfo[] = [];
  for (const record of group) {
    for (const prov of record.provenance) {
      if (!seen.has(prov.sourceId)) {
        seen.add(prov.sourceId);
        result.push(prov);
      }
    }
  }
  return result;
}

export function deduplicateRecords(
  records: MemoryRecord[],
): { deduped: MemoryRecord[]; merged: MergeRecord[] } {
  if (records.length === 0) {
    return { deduped: [], merged: [] };
  }

  const groups = new Map<string, MemoryRecord[]>();
  for (const record of records) {
    const key = normalizeKey(record);
    const group = groups.get(key);
    if (group !== undefined) {
      group.push(record);
    } else {
      groups.set(key, [record]);
    }
  }

  const deduped: MemoryRecord[] = [];
  const merged: MergeRecord[] = [];

  for (const group of groups.values()) {
    if (group.length === 1) {
      deduped.push(group[0]);
      continue;
    }

    // Cluster records within the group by content similarity.
    // Records with low content similarity share entity+kind but differ in
    // meaning — they should remain separate (conflict detection handles them).
    const clusters: MemoryRecord[][] = [];
    for (const record of group) {
      let placed = false;
      for (const cluster of clusters) {
        const rep = cluster[0];
        if (contentSimilarity(rep.content, record.content) >= SIMILARITY_THRESHOLD) {
          cluster.push(record);
          placed = true;
          break;
        }
      }
      if (!placed) clusters.push([record]);
    }

    for (const cluster of clusters) {
      if (cluster.length === 1) {
        deduped.push(cluster[0]);
        continue;
      }
      const canonical = electCanonical(cluster);
      const absorbed = cluster.filter(r => r.id !== canonical.id).map(r => r.id);
      const mergedRecord: MemoryRecord = { ...canonical, provenance: mergeProvenance(cluster) };
      deduped.push(mergedRecord);
      merged.push({ canonical: canonical.id, absorbed, strategy: 'name+type' });
    }
  }

  return { deduped, merged };
}
