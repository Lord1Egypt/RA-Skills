import { nanoid } from 'nanoid';
import { readDayLog, writeDayLog, getMealById, readFoods, readGoals } from '../lib/storage.ts';
import { print, err, sumIngredients } from '../lib/format.ts';
import {
  upsertVector, deleteVector, searchVectors,
  mealVecId, ingredientVecId,
} from '../lib/vectors.ts';
import type { Meal, Ingredient, Unit, Goals } from '../lib/types.ts';
import { WEIGHT_UNITS, VOLUME_UNITS, TO_BASE, GOAL_DIRECTION, NUTRIENT_KEYS } from '../lib/types.ts';

type Args = Record<string, string | boolean | undefined>;

const NUTRIENT_FLAGS = ['calories_kcal', 'protein_g', 'carbs_g', 'fiber_g', 'sugar_g', 'fat_g', 'sat_fat_g'] as const;

function buildImpact(date: string, added: Partial<Ingredient>): Record<string, unknown> {
  const log    = readDayLog(date);
  const goals  = readGoals();
  const allIng = log.flatMap(m => m.ingredients);
  const totals = sumIngredients(allIng) as Goals;

  const impact: Record<string, unknown> = {};

  for (const key of NUTRIENT_KEYS) {
    const delta   = (added as Record<string, number | undefined>)[key];
    const total   = totals[key] ?? 0;
    const goal    = goals[key];
    const type    = GOAL_DIRECTION[key];

    // Only include nutrients that were part of this ingredient or have a goal
    if (delta === undefined && goal === undefined) continue;

    const entry: Record<string, unknown> = {};
    if (delta !== undefined) entry['added'] = delta;
    entry['total'] = total;

    if (goal !== undefined) {
      // remaining: positive = still have headroom (max) or still need (min)
      //            negative = exceeded limit (max=bad) or hit target (min=good)
      const remaining = Math.round((goal - total) * 100) / 100;
      entry['goal']      = goal;
      entry['remaining'] = remaining;
      entry['pct']       = Math.round((total / goal) * 1000) / 10; // one decimal, e.g. 43.2
      if (type === 'max') {
        entry['status'] = remaining < 0 ? 'over' : 'ok';
      } else {
        entry['status'] = remaining > 0 ? 'under' : 'ok';
      }
    }

    impact[key] = entry;
  }

  return impact;
}

function extractNutrients(args: Args): Partial<Ingredient> {
  const out: Partial<Ingredient> = {};
  for (const key of NUTRIENT_FLAGS) {
    const flag = key.replace(/_/g, '-');
    const val = args[flag] ?? args[key];
    if (val !== undefined && val !== true) {
      (out as Record<string, number>)[key] = Number(val);
    }
  }
  return out;
}

function requireDate(args: Args): string {
  const d = args['date'] as string | undefined;
  if (!d) { err('--date YYYY-MM-DD is required'); process.exit(1); }
  return d;
}

function requireTime(args: Args): string {
  const t = args['time'] as string | undefined;
  if (!t) { err('--time HH:MM is required'); process.exit(1); }
  return t;
}

function formatMeal(meal: Meal) {
  const total = sumIngredients(meal.ingredients);
  return {
    id: meal.id,
    name: meal.name,
    time: meal.time,
    ingredients: meal.ingredients.map((ing, i) => ({ index: i, ...ing })),
    total,
  };
}

// ── Meal CRUD ──────────────────────────────────────────────────────────────

async function mealAdd(args: Args): Promise<void> {
  const date = requireDate(args);
  const time = requireTime(args);
  const name = args['name'] as string | undefined;
  if (!name) { err('--name is required'); process.exit(1); }

  const id = nanoid(8);
  const meal: Meal = { id, time, name, ingredients: [] };

  const log = readDayLog(date);
  log.push(meal);
  writeDayLog(date, log);

  await upsertVector(mealVecId(id), name, { type: 'meal', mealId: id, date });
  print({ id });
}

function mealList(args: Args): void {
  const date = requireDate(args);
  const log = readDayLog(date);
  print({ date, meals: log.map(formatMeal) });
}

async function mealUpdate(mealId: string | undefined, args: Args): Promise<void> {
  if (!mealId) { err('meal id required'); process.exit(1); }
  const found = getMealById(mealId);
  if (!found) { err(`meal not found: ${mealId}`); process.exit(1); }

  const { meal, date } = found;
  if (args['name']) meal.name = args['name'] as string;

  const log = readDayLog(date);
  const idx = log.findIndex(m => m.id === mealId);
  log[idx] = meal;
  writeDayLog(date, log);

  await upsertVector(mealVecId(mealId), meal.name, { type: 'meal', mealId, date });
  print({ id: mealId, name: meal.name });
}

async function mealDelete(mealId: string | undefined): Promise<void> {
  if (!mealId) { err('meal id required'); process.exit(1); }
  const found = getMealById(mealId);
  if (!found) { err(`meal not found: ${mealId}`); process.exit(1); }

  const { meal, date } = found;
  const log = readDayLog(date);
  writeDayLog(date, log.filter(m => m.id !== mealId));

  await deleteVector(mealVecId(mealId));
  for (let i = 0; i < meal.ingredients.length; i++) {
    await deleteVector(ingredientVecId(mealId, i));
  }
  print({ deleted: mealId });
}

// ── Ingredient CRUD ────────────────────────────────────────────────────────

function scaleFoodEntry(args: Args): { ingredient: Partial<Ingredient>; matchedFood: string } | null {
  const foodQuery = args['food'] as string | undefined;
  if (!foodQuery) return null;

  const amount = Number(args['amount']);
  const unit   = args['unit'] as Unit | undefined;
  if (!amount || !unit) {
    err('--amount and --unit are required when using --food');
    process.exit(1);
  }

  const foods = readFoods();
  // Exact match first, then case-insensitive
  let matchedName = Object.keys(foods).find(n => n === foodQuery)
    ?? Object.keys(foods).find(n => n.toLowerCase() === foodQuery.toLowerCase());

  if (!matchedName) {
    err(`food not found: "${foodQuery}" — use 'food search' to find the exact name, or add it first`);
    process.exit(1);
  }

  const entry = foods[matchedName!];
  const allUnits = [...WEIGHT_UNITS, ...VOLUME_UNITS];

  if (!allUnits.includes(unit)) {
    err(`invalid unit: ${unit}. Valid: ${allUnits.join(', ')}`);
    process.exit(1);
  }

  // Validate same dimension
  const foodIsWeight = WEIGHT_UNITS.includes(entry.per_unit as typeof WEIGHT_UNITS[number]);
  const inputIsWeight = WEIGHT_UNITS.includes(unit as typeof WEIGHT_UNITS[number]);
  if (foodIsWeight !== inputIsWeight) {
    err(`unit dimension mismatch: food is stored per ${entry.per_unit} (${foodIsWeight ? 'weight' : 'volume'}) but you provided ${unit}`);
    process.exit(1);
  }

  const baseAmount   = amount * TO_BASE[unit];
  const basePerAmount = entry.per_amount * TO_BASE[entry.per_unit];
  const scale = baseAmount / basePerAmount;

  const ingredient: Partial<Ingredient> = {};
  for (const key of NUTRIENT_FLAGS) {
    const v = (entry as Record<string, number | undefined>)[key];
    if (v !== undefined) {
      (ingredient as Record<string, number>)[key] = Math.round(v * scale * 100) / 100;
    }
  }

  return { ingredient, matchedFood: matchedName! };
}

async function ingredientAdd(mealId: string | undefined, args: Args): Promise<void> {
  if (!mealId) { err('meal id required'); process.exit(1); }
  const found = getMealById(mealId);
  if (!found) { err(`meal not found: ${mealId}`); process.exit(1); }

  let nutrients: Partial<Ingredient>;
  let name: string;
  let matchedFood: string | undefined;

  const fromFood = scaleFoodEntry(args);
  if (fromFood) {
    nutrients = fromFood.ingredient;
    matchedFood = fromFood.matchedFood;
    name = (args['name'] as string | undefined) ?? matchedFood;
  } else {
    name = args['name'] as string | undefined ?? '';
    if (!name) { err('--name is required'); process.exit(1); }
    nutrients = extractNutrients(args);
  }

  const { meal, date } = found;
  const index = meal.ingredients.length;
  const ingredient: Ingredient = { name, ...nutrients };
  meal.ingredients.push(ingredient);

  const log = readDayLog(date);
  const mealIdx = log.findIndex(m => m.id === mealId);
  log[mealIdx] = meal;
  writeDayLog(date, log);

  await upsertVector(
    ingredientVecId(mealId, index),
    name,
    { type: 'ingredient', mealId, index, date },
  );

  const result: Record<string, unknown> = { index };
  if (matchedFood) result['matched'] = matchedFood;
  result['impact'] = buildImpact(date, ingredient);
  print(result);
}

async function ingredientUpdate(mealId: string | undefined, indexStr: string | undefined, args: Args): Promise<void> {
  if (!mealId) { err('meal id required'); process.exit(1); }
  if (indexStr === undefined) { err('ingredient index required'); process.exit(1); }
  const index = parseInt(indexStr, 10);

  const found = getMealById(mealId);
  if (!found) { err(`meal not found: ${mealId}`); process.exit(1); }
  const { meal, date } = found;

  if (index < 0 || index >= meal.ingredients.length) {
    err(`ingredient index ${index} out of range (0–${meal.ingredients.length - 1})`);
    process.exit(1);
  }

  const updates = extractNutrients(args);
  if (args['name']) meal.ingredients[index].name = args['name'] as string;
  Object.assign(meal.ingredients[index], updates);

  const log = readDayLog(date);
  log[log.findIndex(m => m.id === mealId)] = meal;
  writeDayLog(date, log);

  await upsertVector(
    ingredientVecId(mealId, index),
    meal.ingredients[index].name,
    { type: 'ingredient', mealId, index, date },
  );

  print({ index, ...meal.ingredients[index], impact: buildImpact(date, meal.ingredients[index]) });
}

async function ingredientDelete(mealId: string | undefined, indexStr: string | undefined): Promise<void> {
  if (!mealId) { err('meal id required'); process.exit(1); }
  if (indexStr === undefined) { err('ingredient index required'); process.exit(1); }
  const index = parseInt(indexStr, 10);

  const found = getMealById(mealId);
  if (!found) { err(`meal not found: ${mealId}`); process.exit(1); }
  const { meal, date } = found;

  if (index < 0 || index >= meal.ingredients.length) {
    err(`ingredient index ${index} out of range`);
    process.exit(1);
  }

  // Remove old vector and re-index remaining ingredients with updated indices
  const oldLen = meal.ingredients.length;
  meal.ingredients.splice(index, 1);

  const log = readDayLog(date);
  log[log.findIndex(m => m.id === mealId)] = meal;
  writeDayLog(date, log);

  // Delete all old ingredient vectors for this meal and reinsert
  for (let i = 0; i < oldLen; i++) {
    await deleteVector(ingredientVecId(mealId, i));
  }
  for (let i = 0; i < meal.ingredients.length; i++) {
    await upsertVector(
      ingredientVecId(mealId, i),
      meal.ingredients[i].name,
      { type: 'ingredient', mealId, index: i, date },
    );
  }

  print({ deleted: index });
}

// ── Search ─────────────────────────────────────────────────────────────────

async function mealSearch(query: string | undefined, args: Args): Promise<void> {
  if (!query) { err('search query required'); process.exit(1); }
  const from = args['from'] as string | undefined;
  const to   = args['to']   as string | undefined;

  const results = await searchVectors(query, 5, 'meal', from, to);
  const items = results.map(r => {
    const meta = r.metadata as { type: 'meal'; mealId: string; date: string };
    const found = getMealById(meta.mealId, meta.date);
    if (!found) return null;
    return { date: meta.date, score: Math.round(r.score * 100) / 100, ...formatMeal(found.meal) };
  }).filter(Boolean);

  print({ query, results: items });
}

async function ingredientSearch(query: string | undefined, args: Args): Promise<void> {
  if (!query) { err('search query required'); process.exit(1); }
  const from = args['from'] as string | undefined;
  const to   = args['to']   as string | undefined;

  const results = await searchVectors(query, 10, 'ingredient', from, to);

  // Deduplicate by mealId, keeping best score per meal
  const seen = new Map<string, { score: number; mealId: string; date: string; matched: string }>();
  for (const r of results) {
    const meta = r.metadata as { type: 'ingredient'; mealId: string; index: number; date: string };
    const found = getMealById(meta.mealId, meta.date);
    if (!found) continue;
    const ingName = found.meal.ingredients[meta.index]?.name ?? '';
    if (!seen.has(meta.mealId) || seen.get(meta.mealId)!.score < r.score) {
      seen.set(meta.mealId, { score: r.score, mealId: meta.mealId, date: meta.date, matched: ingName });
    }
  }

  const items = Array.from(seen.values())
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map(({ score, mealId, date, matched }) => {
      const found = getMealById(mealId, date);
      if (!found) return null;
      return {
        date,
        score: Math.round(score * 100) / 100,
        matched_ingredient: matched,
        ...formatMeal(found.meal),
      };
    })
    .filter(Boolean);

  print({ query, results: items });
}

// ── Command router ─────────────────────────────────────────────────────────

export async function mealCommand(
  sub: string,
  rest: string[],
  args: Args,
): Promise<void> {
  // meal search <query>
  if (sub === 'search') {
    return mealSearch(rest[0], args);
  }

  // meal ingredient ...
  if (sub === 'ingredient') {
    const [ingSub, ...ingRest] = rest;
    switch (ingSub) {
      case 'add':    return ingredientAdd(ingRest[0], args);
      case 'update': return ingredientUpdate(ingRest[0], ingRest[1], args);
      case 'delete': return ingredientDelete(ingRest[0], ingRest[1]);
      case 'search': return ingredientSearch(ingRest[0], args);
      default:
        err(`unknown meal ingredient subcommand: ${ingSub}. Use add | update | delete | search`);
        process.exit(1);
    }
  }

  // meal add | list | update | delete
  switch (sub) {
    case 'add':    return mealAdd(args);
    case 'list':   return mealList(args);
    case 'update': return mealUpdate(rest[0], args);
    case 'delete': return mealDelete(rest[0]);
    default:
      err(`unknown meal subcommand: ${sub}. Use add | list | update | delete | search | ingredient`);
      process.exit(1);
  }
}
