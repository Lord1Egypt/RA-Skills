import { parseCliArgs } from './lib/args.js';
import { ensureDirs } from './lib/storage.js';
import { err } from './lib/format.js';

const HELP = `
life-state — daily mood / energy / sleep capture for the lifekit ecosystem

USAGE
  life-state <command> [flags]

COMMANDS

  set                               Capture or update today's state (merges with existing)
    --mood <m>                      great | good | normal | tired | terrible (freeform also accepted)
    --energy <n>                    1-10 numeric scale
    --sleep <q>                     good | ok | poor (freeform also accepted)
    --sore <list>                   Comma-separated muscle groups (e.g. "chest,triceps")
    --note "<text>"                 Free-text annotation
    --date YYYY-MM-DD               Override date (default: today)

  get                               Read today's state
    --date YYYY-MM-DD               Read another day

  week                              Aggregate the last N days (default 7)
    --days <n>                      Window size in days

DATA      ~/.life/state/YYYY-MM-DD.json  (one JSON file per day, fully local)
OUTPUT    YAML on stdout, errors on stderr

OTHER SKILLS reading this state:
  morning_brief — should adapt suggestions based on yesterday's energy and sleep
  future workout suggester — adapts volume/intensity to today's energy and soreness
  bedtime brief — adapts wind-down to the day's note
`.trim();

async function main(): Promise<void> {
  ensureDirs();

  const { positionals, flags } = parseCliArgs(process.argv.slice(2));

  if (positionals.length === 0 || flags['help'] || positionals[0] === 'help') {
    console.log(HELP);
    process.exit(0);
  }

  const [cmd] = positionals;

  switch (cmd) {
    case 'set': {
      const { setCommand } = await import('./commands/set.js');
      setCommand(flags);
      break;
    }
    case 'get': {
      const { getCommand } = await import('./commands/get.js');
      getCommand(flags);
      break;
    }
    case 'week': {
      const { weekCommand } = await import('./commands/week.js');
      weekCommand(flags);
      break;
    }
    default:
      err(`unknown command: ${cmd}\nRun 'life-state --help' for usage.`);
      process.exit(1);
  }
}

main().catch(e => {
  err(String(e?.message ?? e));
  process.exit(1);
});
