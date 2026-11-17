import { pathToFileURL } from 'node:url';
import { SkillError, assertOptions, createClient, fail, parseArgs } from './api.mjs';
import { discover, discoveryFlags, snapshots } from './discovery.mjs';

export async function main(argv = process.argv.slice(2)) {
  const { command, options: o } = parseArgs(argv, [...discoveryFlags, 'event-id', 'bookmakers', 'types', 'periods']);
  if (o.help || !command) {
    console.log('Odds API JavaScript starter — Node.js 22+\n\nCommands:\n  catalog --kind sports|leagues|bookmakers [--sport SPORT] [--country-code CC]\n  events --sport SPORT [--league LEAGUE] --from UTC --to UTC [--team NAME]\n  snapshot --event-id ID [--bookmakers KEYS] [--types TYPES] [--periods LABELS]\n\nNetwork calls require the runtime ODDS_API_KEY variable. No key is included.');
    return;
  }
  if (!['catalog', 'events', 'snapshot'].includes(command)) throw new SkillError('Unknown command. Use --help.');
  let result;
  if (command === 'snapshot') {
    assertOptions(o, ['event-id', 'bookmakers', 'types', 'periods']);
    const pages = await snapshots(createClient(), o['event-id'], { bookmakers: o.bookmakers, types: o.types, periods: o.periods });
    // Keep page-level freshness and continuation metadata intact.
    result = { event_id: o['event-id'], complete: true, pages: pages.map(page => page.data) };
  } else result = await discover(createClient(), command, o);
  console.log(JSON.stringify(result, null, 2));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main().catch(fail);
