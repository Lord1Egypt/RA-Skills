import { parseCliArgs } from './lib/args.ts';
import { ensureDirs } from './lib/storage.ts';
import { err } from './lib/format.ts';

const HELP = `
nutrition-claw — local nutrition tracker

USAGE
  nutrition-claw <command> [subcommand] [args]

COMMANDS

  configure                         Set up nutrition goals (interactive or via flags)
    --sex male|female|other         Auto mode: biological sex for BMR
    --age <n>                       Auto mode: age in years
    --weight-kg <n>                 Auto mode: weight in kg
    --height-cm <n>                 Auto mode: height in cm
    --activity sedentary|light|moderate|very|extra
    --goal lose|recomp|maintain|lean-bulk|bulk
    --rate 0.25|0.5|0.75            Loss rate kg/week (lose goal)
    --surplus 200|350|500           Calorie surplus (bulk goal)
    --calories-kcal|--protein-g|--carbs-g|--fiber-g|--sugar-g|--fat-g|--sat-fat-g <n>
                                    Manual mode: set each nutrient directly

  goals get                         Show current goals
  goals set [nutrients...]          Update individual goal values
  goals delete [--nutrient <key>]   Delete one or all goals

  meal add --name <n> --date <d> --time <t>   Create meal, returns id
  meal list --date <d>                         List meals with totals
  meal update <id> --name <n>                  Rename meal
  meal delete <id>                             Delete meal + ingredients
  meal search <query> [--from <d>] [--to <d>] Semantic search by meal name

  meal ingredient add <meal-id> --name <n> [nutrients...]
  meal ingredient add <meal-id> --food <query> --amount <n> --unit <u>
  meal ingredient update <meal-id> <index> [nutrients...]
  meal ingredient delete <meal-id> <index>
  meal ingredient search <query> [--from <d>] [--to <d>]

  food add --name <n> --per-amount <n> --per-unit <u> [nutrients...]
  food get <name>                   Exact name lookup
  food list                         List all food entries
  food update <name> [nutrients...] Update specific fields
  food delete <name>                Remove food entry
  food search <query>               Semantic search in food library

  summary --date <d>                Daily totals vs goals
  history --from <d> --to <d>       Multi-day nutrient overview
         [--days <n>]               Substitute for --to (from + n days)

NUTRIENTS
  --calories-kcal  --protein-g  --carbs-g  --fiber-g
  --sugar-g        --fat-g      --sat-fat-g

UNITS
  WEIGHT  g  kg  oz  lb
  VOLUME  ml  L  fl_oz  cup  tbsp  tsp

DATES    YYYY-MM-DD  (always required, never inferred)
TIME     HH:MM       (required for meal add)

OUTPUT   YAML — unset nutrient fields omitted; errors on stderr
DATA     ~/.nutrition-claw/  (fully local, no network required)
`.trim();

async function main(): Promise<void> {
  ensureDirs();

  const { positionals, flags: args } = parseCliArgs(process.argv.slice(2));

  if (positionals.length === 0 || args['help'] || positionals[0] === 'help') {
    console.log(HELP);
    process.exit(0);
  }

  const [cmd, ...rest] = positionals;

  switch (cmd) {
    case 'configure': {
      const { configureCommand } = await import('./commands/configure.ts');
      await configureCommand(args);
      break;
    }
    case 'goals': {
      const [sub] = rest;
      if (!sub) { err('goals requires a subcommand: get | set | delete'); process.exit(1); }
      const { goalsCommand } = await import('./commands/goals.ts');
      await goalsCommand(sub, args);
      break;
    }
    case 'meal': {
      const [sub, ...mRest] = rest;
      if (!sub) { err('meal requires a subcommand: add | list | update | delete | search | ingredient'); process.exit(1); }
      const { mealCommand } = await import('./commands/meal.ts');
      await mealCommand(sub, mRest, args);
      break;
    }
    case 'food': {
      const [sub, ...fRest] = rest;
      if (!sub) { err('food requires a subcommand: add | get | list | update | delete | search'); process.exit(1); }
      const { foodCommand } = await import('./commands/food.ts');
      await foodCommand(sub, args, fRest);
      break;
    }
    case 'summary': {
      const { summaryCommand } = await import('./commands/summary.ts');
      summaryCommand(args);
      break;
    }
    case 'history': {
      const { historyCommand } = await import('./commands/history.ts');
      historyCommand(args);
      break;
    }
    default:
      err(`unknown command: ${cmd}\nRun 'nutrition-claw --help' for usage.`);
      process.exit(1);
  }
}

main().catch(e => {
  err(String(e?.message ?? e));
  process.exit(1);
});
