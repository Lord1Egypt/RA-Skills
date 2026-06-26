import { stringify } from 'yaml';
import type { Ingredient, Goals } from './types.ts';

function omitUndefined(obj: unknown): unknown {
  if (Array.isArray(obj)) return obj.map(omitUndefined);
  if (obj !== null && typeof obj === 'object') {
    const result: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(obj as Record<string, unknown>)) {
      if (v !== undefined && v !== null) {
        result[k] = omitUndefined(v);
      }
    }
    return result;
  }
  return obj;
}

export function print(data: unknown): void {
  const cleaned = omitUndefined(data);
  process.stdout.write(stringify(cleaned, { lineWidth: 0 }));
}

export function err(msg: string): void {
  process.stderr.write(`error: ${msg}\n`);
}

export function sumIngredients(ingredients: Ingredient[]): Omit<Goals, never> {
  const totals: Goals = {};
  for (const ing of ingredients) {
    for (const key of ['calories_kcal', 'protein_g', 'carbs_g', 'fiber_g', 'sugar_g', 'fat_g', 'sat_fat_g'] as (keyof Goals)[]) {
      const v = ing[key as keyof Ingredient] as number | undefined;
      if (v !== undefined) {
        totals[key] = (totals[key] ?? 0) + v;
      }
    }
  }
  // Round to 2 decimal places
  for (const key of Object.keys(totals) as (keyof Goals)[]) {
    totals[key] = Math.round((totals[key]! as number) * 100) / 100;
  }
  return totals;
}
