import { writeGoals } from '../lib/storage.ts';
import { print, err } from '../lib/format.ts';
import type { Goals } from '../lib/types.ts';

type Args = Record<string, string | boolean | undefined>;

type Sex = 'male' | 'female' | 'other';
type Activity = 'sedentary' | 'light' | 'moderate' | 'very' | 'extra';
type Goal = 'lose' | 'recomp' | 'maintain' | 'lean-bulk' | 'bulk';

const ACTIVITY_MULTIPLIERS: Record<Activity, number> = {
  sedentary: 1.2,
  light:     1.375,
  moderate:  1.55,
  very:      1.725,
  extra:     1.9,
};

function calcBmr(sex: Sex, weightKg: number, heightCm: number, age: number): number {
  const male   = 10 * weightKg + 6.25 * heightCm - 5 * age + 5;
  const female = 10 * weightKg + 6.25 * heightCm - 5 * age - 161;
  if (sex === 'male') return male;
  if (sex === 'female') return female;
  return (male + female) / 2;
}

function calcGoals(
  sex: Sex,
  weightKg: number,
  heightCm: number,
  age: number,
  activity: Activity,
  goal: Goal,
  rate?: number,
  surplus?: number,
): Goals {
  const bmr  = calcBmr(sex, weightKg, heightCm, age);
  const tdee = bmr * ACTIVITY_MULTIPLIERS[activity];

  let cals: number;
  if (goal === 'lose') {
    const r = rate ?? 0.5;
    cals = tdee - r * 1000;
  } else if (goal === 'recomp') {
    cals = tdee;
  } else if (goal === 'maintain') {
    cals = tdee;
  } else if (goal === 'lean-bulk') {
    cals = tdee + (surplus ?? 200);
  } else {
    cals = tdee + (surplus ?? 500);
  }

  cals = Math.max(cals, 1200);

  const inDeficit  = cals < tdee - 50;
  const inSurplus  = cals > tdee + 50;
  const proteinMult = inDeficit ? 2.0 : inSurplus ? 2.0 : 1.8;
  const protein_g   = Math.round(proteinMult * weightKg);
  const fat_g       = Math.round(Math.max(0.9 * weightKg, (0.25 * cals) / 9));
  const carbs_g     = Math.round((cals - protein_g * 4 - fat_g * 9) / 4);
  const fiber_g     = Math.round((14 * cals) / 1000);
  const sugar_g     = Math.round((0.10 * cals) / 4);
  const sat_fat_g   = Math.round((0.10 * cals) / 9);

  return {
    calories_kcal: Math.round(cals),
    protein_g,
    carbs_g:    Math.max(0, carbs_g),
    fiber_g,
    sugar_g,
    fat_g,
    sat_fat_g,
  };
}

// ── Non-interactive (flag-based) mode ──────────────────────────────────────

function hasAutoFlags(args: Args): boolean {
  return !!(args['sex'] || args['age'] || args['weight-kg'] || args['height-cm']);
}

function hasManualFlags(args: Args): boolean {
  return !!(args['calories-kcal'] || args['protein-g'] || args['carbs-g']);
}

function runNonInteractive(args: Args): void {
  let goals: Goals;

  if (hasManualFlags(args)) {
    goals = {};
    const map: Array<[string, keyof Goals]> = [
      ['calories-kcal', 'calories_kcal'],
      ['protein-g',     'protein_g'],
      ['carbs-g',       'carbs_g'],
      ['fiber-g',       'fiber_g'],
      ['sugar-g',       'sugar_g'],
      ['fat-g',         'fat_g'],
      ['sat-fat-g',     'sat_fat_g'],
    ];
    for (const [flag, key] of map) {
      if (args[flag] !== undefined) {
        goals[key] = Number(args[flag]);
      }
    }
  } else if (hasAutoFlags(args)) {
    const sex      = (args['sex'] as Sex)       ?? 'other';
    const age      = Number(args['age']         ?? 30);
    const weightKg = Number(args['weight-kg']   ?? 70);
    const heightCm = Number(args['height-cm']   ?? 170);
    const activity = (args['activity'] as Activity) ?? 'moderate';
    const goal     = (args['goal'] as Goal)     ?? 'maintain';
    const rate     = args['rate']    !== undefined ? Number(args['rate'])    : undefined;
    const surplus  = args['surplus'] !== undefined ? Number(args['surplus']) : undefined;

    goals = calcGoals(sex, weightKg, heightCm, age, activity, goal, rate, surplus);
  } else {
    err('no flags provided — run without flags for interactive mode');
    process.exit(1);
  }

  writeGoals(goals);
  print({ goals });
}

// ── Interactive mode ────────────────────────────────────────────────────────

async function runInteractive(): Promise<void> {
  const { select, number: promptNumber, confirm } = await import('@inquirer/prompts');

  const mode = await select({
    message: 'How would you like to set your goals?',
    choices: [
      { name: 'Automatic — calculate from body profile + fitness objective', value: 'auto' },
      { name: 'Manual — enter each nutrient target directly', value: 'manual' },
    ],
  });

  let goals: Goals;

  if (mode === 'auto') {
    const sex = await select<Sex>({
      message: 'Sex (used for BMR calculation):',
      choices: [
        { name: 'Male', value: 'male' },
        { name: 'Female', value: 'female' },
        { name: 'Other (average of male/female formula)', value: 'other' },
      ],
    });

    const age = await promptNumber({ message: 'Age (years):', default: 30, min: 10, max: 120 });
    const weightKg = await promptNumber({ message: 'Weight (kg):', default: 70, min: 20, max: 300 });
    const heightCm = await promptNumber({ message: 'Height (cm):', default: 170, min: 100, max: 250 });

    const activity = await select<Activity>({
      message: 'Activity level:',
      choices: [
        { name: 'Sedentary (desk job, little movement)',              value: 'sedentary' },
        { name: 'Lightly active (exercise 1–3 days/week)',            value: 'light' },
        { name: 'Moderately active (exercise 3–5 days/week)',         value: 'moderate' },
        { name: 'Very active (exercise 6–7 days/week)',               value: 'very' },
        { name: 'Extra active (physical job + daily exercise)',        value: 'extra' },
      ],
    });

    const goal = await select<Goal>({
      message: 'Primary goal:',
      choices: [
        { name: 'Lose weight',                                        value: 'lose' },
        { name: 'Body recomposition (lose fat, build muscle)',        value: 'recomp' },
        { name: 'Maintain weight',                                    value: 'maintain' },
        { name: 'Build muscle — lean bulk (+200 kcal/day)',           value: 'lean-bulk' },
        { name: 'Build muscle — aggressive bulk (+500 kcal/day)',     value: 'bulk' },
      ],
    });

    let rate: number | undefined;
    let surplus: number | undefined;

    if (goal === 'lose') {
      const rateChoice = await select<string>({
        message: 'Target weight-loss rate:',
        choices: [
          { name: 'Mild    — 0.25 kg/week (−250 kcal/day)',    value: '0.25' },
          { name: 'Standard — 0.5 kg/week (−500 kcal/day)',    value: '0.5' },
          { name: 'Aggressive — 0.75 kg/week (−750 kcal/day)', value: '0.75' },
        ],
      });
      rate = Number(rateChoice);
    } else if (goal === 'bulk') {
      const surplusChoice = await select<string>({
        message: 'Daily calorie surplus:',
        choices: [
          { name: 'Lean    — +200 kcal/day', value: '200' },
          { name: 'Moderate — +350 kcal/day', value: '350' },
          { name: 'Aggressive — +500 kcal/day', value: '500' },
        ],
      });
      surplus = Number(surplusChoice);
    }

    goals = calcGoals(sex, weightKg, heightCm, age, activity, goal, rate, surplus);
  } else {
    // manual
    const calories_kcal = await promptNumber({ message: 'Calories (kcal/day):', default: 2000, min: 500 });
    const protein_g     = await promptNumber({ message: 'Protein goal (g/day, min):', default: 150, min: 0 });
    const carbs_g       = await promptNumber({ message: 'Carbs limit (g/day, max):', default: 250, min: 0 });
    const fiber_g       = await promptNumber({ message: 'Fiber goal (g/day, min):', default: 25, min: 0 });
    const sugar_g       = await promptNumber({ message: 'Sugar limit (g/day, max):', default: 50, min: 0 });
    const fat_g         = await promptNumber({ message: 'Fat limit (g/day, max):', default: 65, min: 0 });
    const sat_fat_g     = await promptNumber({ message: 'Saturated fat limit (g/day, max):', default: 20, min: 0 });

    goals = { calories_kcal, protein_g, carbs_g, fiber_g, sugar_g, fat_g, sat_fat_g };
  }

  console.log('\nComputed goals:');
  const { stringify } = await import('yaml');
  console.log(stringify({ goals }, { lineWidth: 0 }));

  const ok = await confirm({ message: 'Save these goals?', default: true });
  if (!ok) {
    console.log('Cancelled.');
    return;
  }

  writeGoals(goals);
  console.log('Goals saved.');
}

// ── Entry point ─────────────────────────────────────────────────────────────

export async function configureCommand(args: Args): Promise<void> {
  const hasFlags = hasAutoFlags(args) || hasManualFlags(args);
  if (hasFlags) {
    runNonInteractive(args);
  } else {
    await runInteractive();
  }
}
