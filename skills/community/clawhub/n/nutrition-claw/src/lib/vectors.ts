import { LocalIndex } from 'vectra';
import { getVectorsDir } from './storage.ts';
import type { VecMetadata } from './types.ts';

// Lazily initialised so the model only loads when search/add actually runs
let _embedFn: ((text: string) => Promise<number[]>) | null = null;

async function embed(text: string): Promise<number[]> {
  if (!_embedFn) {
    const mod = await import('@themaximalist/embeddings.js');
    const embeddings = mod.default;
    _embedFn = (t: string) => embeddings(t) as Promise<number[]>;
  }
  return _embedFn(text);
}

let _index: LocalIndex | null = null;

async function getIndex(): Promise<LocalIndex> {
  if (_index) return _index;
  const idx = new LocalIndex(getVectorsDir());
  if (!(await idx.isIndexCreated())) {
    await idx.createIndex({ version: 1 });
  }
  _index = idx;
  return _index;
}

export async function upsertVector(
  id: string,
  text: string,
  metadata: VecMetadata,
): Promise<void> {
  const idx = await getIndex();
  const vector = await embed(text);
  await idx.upsertItem({ id, vector, metadata: metadata as Record<string, string | number | boolean> });
}

export async function deleteVector(id: string): Promise<void> {
  const idx = await getIndex();
  try {
    await idx.deleteItem(id);
  } catch {
    // item may not exist, ignore
  }
}

export interface SearchResult {
  id: string;
  score: number;
  metadata: VecMetadata;
}

export async function searchVectors(
  query: string,
  topK: number,
  filterType?: 'meal' | 'ingredient' | 'food',
  dateFrom?: string,
  dateTo?: string,
): Promise<SearchResult[]> {
  const idx = await getIndex();
  const vector = await embed(query);

  const filter: Record<string, unknown> = {};
  if (filterType) filter['type'] = filterType;

  const results = await idx.queryItems(vector, query, topK * 3, Object.keys(filter).length ? filter : undefined);

  return results
    .filter(r => {
      const meta = r.item.metadata as unknown as VecMetadata;
      if (filterType && meta.type !== filterType) return false;
      if ((dateFrom || dateTo) && 'date' in meta) {
        if (dateFrom && meta.date < dateFrom) return false;
        if (dateTo && meta.date > dateTo) return false;
      }
      return true;
    })
    .slice(0, topK)
    .map(r => ({
      id: r.item.id!,
      score: r.score,
      metadata: r.item.metadata as unknown as VecMetadata,
    }));
}

export function mealVecId(mealId: string): string {
  return `meal:${mealId}`;
}

export function ingredientVecId(mealId: string, index: number): string {
  return `ing:${mealId}:${index}`;
}

export function foodVecId(name: string): string {
  return `food:${encodeURIComponent(name)}`;
}
