import { readFoods, writeFoods, readGoals, readEducationLog, appendEducationLog } from '../lib/storage.ts';
import { print, err } from '../lib/format.ts';
import { upsertVector, deleteVector, searchVectors, foodVecId } from '../lib/vectors.ts';
import type { FoodEntry, Unit, Goals } from '../lib/types.ts';
import { WEIGHT_UNITS, VOLUME_UNITS } from '../lib/types.ts';

type Args = Record<string, string | boolean | undefined>;

const ALL_UNITS = [...WEIGHT_UNITS, ...VOLUME_UNITS];
const NUTRIENT_FLAGS = ['calories_kcal', 'protein_g', 'carbs_g', 'fiber_g', 'sugar_g', 'fat_g', 'sat_fat_g'] as const;

function extractNutrients(args: Args): Partial<FoodEntry> {
  const entry: Partial<FoodEntry> = {};
  for (const key of NUTRIENT_FLAGS) {
    const flag = key.replace(/_/g, '-');
    const val = args[flag] ?? args[key];
    if (val !== undefined && val !== true) {
      (entry as Record<string, number>)[key] = Number(val);
    }
  }
  return entry;
}

/**
 * Generates nutritional education highlights for a food entry relative to the
 * user's goals. Returns an array of insight strings (positives and warnings),
 * or null if this food was recently educated about (present in the 20-line
 * rotating education.txt log).
 *
 * Each insight is a plain-English sentence — the agent should present these
 * conversationally, not just echo them verbatim.
 */
function buildEducation(name: string, entry: FoodEntry, goals: Goals): string[] | null {
  const educated = readEducationLog();
  if (educated.has(name)) return null; // recently educated — skip

  const insights: string[] = [];
  const ref = entry.per_amount;
  const unit = entry.per_unit;

  // Protein density — great if >15g per 100g/ml
  if (entry.protein_g !== undefined && goals.protein_g !== undefined) {
    const proteinPer100 = (entry.protein_g / ref) * 100;
    if (proteinPer100 >= 15) {
      insights.push(`High protein source: ${proteinPer100.toFixed(1)}g protein per 100${unit} — great for hitting your ${goals.protein_g}g daily protein goal.`);
    } else if (proteinPer100 < 5 && entry.calories_kcal !== undefined) {
      const calPer100 = (entry.calories_kcal / ref) * 100;
      if (calPer100 > 100) {
        insights.push(`Low protein for the calories: only ${proteinPer100.toFixed(1)}g protein per 100${unit} — won't help much with your ${goals.protein_g}g protein target.`);
      }
    }
  }

  // Calorie density
  if (entry.calories_kcal !== undefined) {
    const calPer100 = (entry.calories_kcal / ref) * 100;
    if (calPer100 > 300) {
      insights.push(`Calorie-dense: ${calPer100.toFixed(0)} kcal per 100${unit} — portion size matters here.`);
    } else if (calPer100 < 50) {
      insights.push(`Low calorie: only ${calPer100.toFixed(0)} kcal per 100${unit} — you can eat more of this without blowing your budget.`);
    }
  }

  // Saturated fat warning
  if (entry.sat_fat_g !== undefined && goals.sat_fat_g !== undefined) {
    const satFatPer100 = (entry.sat_fat_g / ref) * 100;
    if (satFatPer100 > 10) {
      insights.push(`High saturated fat: ${satFatPer100.toFixed(1)}g per 100${unit} — your daily limit is ${goals.sat_fat_g}g, so watch portions.`);
    }
  }

  // Sugar warning
  if (entry.sugar_g !== undefined && goals.sugar_g !== undefined) {
    const sugarPer100 = (entry.sugar_g / ref) * 100;
    if (sugarPer100 > 15) {
      insights.push(`High sugar: ${sugarPer100.toFixed(1)}g per 100${unit} — your daily limit is ${goals.sugar_g}g.`);
    }
  }

  // Fiber bonus
  if (entry.fiber_g !== undefined && goals.fiber_g !== undefined) {
    const fiberPer100 = (entry.fiber_g / ref) * 100;
    if (fiberPer100 >= 5) {
      insights.push(`Good fiber source: ${fiberPer100.toFixed(1)}g per 100${unit} — helps toward your ${goals.fiber_g}g daily fiber goal.`);
    }
  }

  // Healthy fat ratio — high fat but mostly unsaturated
  if (entry.fat_g !== undefined && entry.sat_fat_g !== undefined) {
    const totalFatPer100 = (entry.fat_g / ref) * 100;
    const satFatPer100 = (entry.sat_fat_g / ref) * 100;
    const unsatRatio = totalFatPer100 > 0 ? (totalFatPer100 - satFatPer100) / totalFatPer100 : 0;
    if (totalFatPer100 > 10 && unsatRatio > 0.7) {
      insights.push(`Mostly unsaturated fats (${(unsatRatio * 100).toFixed(0)}% of total fat) — the healthier kind.`);
    }
  }

  // Mark as recently educated — appended to rotating 20-line text file
  appendEducationLog(name);

  return insights.length > 0 ? insights : [];
}

export async function foodCommand(sub: string, args: Args, positional: string[]): Promise<void> {
  switch (sub) {
    case 'add':    return foodAdd(args);
    case 'get':    return foodGet(positional[0]);
    case 'list':   return foodList();
    case 'update': return foodUpdate(positional[0], args);
    case 'delete': return foodDelete(positional[0]);
    case 'search': return foodSearch(positional[0]);
    default:
      err(`unknown food subcommand: ${sub}. Use add | get | list | update | delete | search`);
      process.exit(1);
  }
}

async function foodAdd(args: Args): Promise<void> {
  const name = args['name'] as string | undefined;
  if (!name) { err('--name is required'); process.exit(1); }

  // Food library is for packaged/labelled products only.
  // Default reference amount is 100g (or 100ml for liquids — pass --per-unit ml explicitly).
  const per_amount = Number(args['per-amount'] ?? args['per_amount'] ?? 100);
  const per_unit   = (args['per-unit'] ?? args['per_unit'] ?? 'g') as Unit;

  if (!ALL_UNITS.includes(per_unit)) {
    err(`invalid unit: ${per_unit}. Valid: ${ALL_UNITS.join(', ')}`);
    process.exit(1);
  }

  const nutrients = extractNutrients(args);
  const entry: FoodEntry = { per_amount, per_unit, ...nutrients };

  const foods = readFoods();
  foods[name] = entry;
  writeFoods(foods);

  await upsertVector(foodVecId(name), name, { type: 'food', name });

  const goals = readGoals();
  const education = buildEducation(name, entry, goals);
  const output: Record<string, unknown> = { name, ...entry };
  if (education !== null) {
    // education is an array of insight strings; null means already seen recently
    output['education'] = education;
  }
  print(output);
}

function foodGet(name: string | undefined): void {
  if (!name) { err('food name required'); process.exit(1); }
  const foods = readFoods();
  if (!foods[name]) { err(`food not found: ${name}`); process.exit(1); }
  print({ name, ...foods[name] });
}

function foodList(): void {
  const foods = readFoods();
  const entries = Object.entries(foods).map(([name, entry]) => ({ name, ...entry }));
  print({ foods: entries });
}

async function foodUpdate(name: string | undefined, args: Args): Promise<void> {
  if (!name) { err('food name required'); process.exit(1); }
  const foods = readFoods();
  if (!foods[name]) { err(`food not found: ${name}`); process.exit(1); }

  const nutrients = extractNutrients(args);
  if (args['per-amount'] ?? args['per_amount']) {
    foods[name].per_amount = Number(args['per-amount'] ?? args['per_amount']);
  }
  if (args['per-unit'] ?? args['per_unit']) {
    const u = (args['per-unit'] ?? args['per_unit']) as Unit;
    if (!ALL_UNITS.includes(u)) { err(`invalid unit: ${u}`); process.exit(1); }
    foods[name].per_unit = u;
  }
  Object.assign(foods[name], nutrients);
  writeFoods(foods);
  print({ name, ...foods[name] });
}

async function foodDelete(name: string | undefined): Promise<void> {
  if (!name) { err('food name required'); process.exit(1); }
  const foods = readFoods();
  if (!foods[name]) { err(`food not found: ${name}`); process.exit(1); }
  delete foods[name];
  writeFoods(foods);
  await deleteVector(foodVecId(name));
  print({ deleted: name });
}

async function foodSearch(query: string | undefined): Promise<void> {
  if (!query) { err('search query required'); process.exit(1); }
  const results = await searchVectors(query, 5, 'food');
  const foods = readFoods();
  const items = results.map(r => {
    const meta = r.metadata as { type: 'food'; name: string };
    const entry = foods[meta.name];
    return entry ? { name: meta.name, score: Math.round(r.score * 100) / 100, ...entry } : null;
  }).filter(Boolean);
  print({ query, results: items });
}
