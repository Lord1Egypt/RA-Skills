import { pathToFileURL } from 'node:url';
import { SkillError, american, assertOptions, createClient, fail, integer, md, parseArgs, stable } from './lib/api.mjs';
import { discover, discoveryFlags, snapshots } from './lib/discovery.mjs';

export function identity(line) {
  if (!line || !line.selection_key || !line.market_key || !line.bookmaker || line.period === undefined || line.period === null) return null;
  return {
    event_id: line.event_id, selection_key: line.selection_key, market_key: line.market_key,
    bet_type: line.bet_type ?? line.type ?? null, metric: line.metric ?? null,
    period: String(line.period), period_str: line.period_str ?? null,
    line: line.line ?? null, side: line.side ?? null, player_name: line.player_name ?? null,
    market_contract: line.market_contract ?? null, selection_parameters: line.selection_parameters ?? null,
    number_of_outcomes: line.number_of_outcomes ?? null,
  };
}

export function comparePages(pages, { now = Date.now(), selectionKey, marketKey, maxGroups = 100, requestedBookmakers = [] } = {}) {
  const groups = new Map(), excluded = [], skipped = {};
  const skip = reason => { skipped[reason] = (skipped[reason] || 0) + 1; };
  const included = new Set();
  for (const { data, excludedHeader } of pages) {
    excluded.push(...(data.excluded_bookmakers || []));
    if (excludedHeader) excluded.push({ header: excludedHeader });
    for (const bookmaker of data.bookmakers_included || []) included.add(bookmaker);
    for (const row of data.items) {
      if (selectionKey && row.selection_key !== selectionKey) continue;
      if (marketKey && row.market_key !== marketKey) continue;
      const keyFields = identity(row);
      if (!keyFields || keyFields.event_id !== data.event_id) { skip('missing_or_mismatched_identity'); continue; }
      if (/exchange|prediction/i.test(row.source_type || '') || row.exchange || row.best_lay_price != null) { skip('non_sportsbook_price'); continue; }
      if (row.is_available === false || (row.is_available !== undefined && row.is_available !== true)) { skip('unavailable'); continue; }
      if (typeof row.odds !== 'number' || !Number.isFinite(row.odds) || row.odds <= 1) { skip('invalid_price'); continue; }
      included.add(row.bookmaker);
      const timestamp = data.bookmaker_as_of_ts_ms?.[row.bookmaker];
      const validTime = typeof timestamp === 'number' && Number.isFinite(timestamp) && timestamp > 0 && timestamp <= now + 5000;
      const target = data.target_refresh_interval_seconds;
      const age = validTime ? Math.max(0, (now - timestamp) / 1000) : null;
      let freshness = 'unknown';
      if ((data.stale_bookmakers || []).includes(row.bookmaker)) freshness = 'stale';
      else if (validTime && typeof target === 'number' && Number.isFinite(target) && target > 0) freshness = age <= 2 * target ? 'fresh' : 'stale';
      const key = JSON.stringify(stable(keyFields));
      if (!groups.has(key)) groups.set(key, { selection: keyFields, selection_name: row.selection_name || row.selection_key, quotes: [] });
      groups.get(key).quotes.push({
        bookmaker: row.bookmaker, odds_decimal: row.odds, odds_american: american(row.odds),
        implied_probability: 1 / row.odds, accepted_at: validTime ? new Date(timestamp).toISOString() : null,
        age_seconds: age, freshness,
      });
    }
  }
  const result = [];
  for (const group of groups.values()) {
    const books = new Map();
    for (const quote of group.quotes) {
      const prior = books.get(quote.bookmaker);
      if (!prior) books.set(quote.bookmaker, quote);
      else if (prior.odds_decimal !== quote.odds_decimal) prior.freshness = 'conflicting';
      else if (prior.accepted_at !== quote.accepted_at || prior.freshness !== quote.freshness) prior.freshness = 'conflicting';
    }
    group.quotes = [...books.values()].sort((a, b) => b.odds_decimal - a.odds_decimal || a.bookmaker.localeCompare(b.bookmaker));
    const fresh = group.quotes.filter(quote => quote.freshness === 'fresh');
    const best = fresh.length ? Math.max(...fresh.map(quote => quote.odds_decimal)) : null;
    group.best_fresh_quotes = fresh.filter(quote => quote.odds_decimal === best).map(quote => quote.bookmaker);
    result.push(group);
  }
  return {
    event_id: pages[0]?.data.event_id, retrieved_at: new Date(now).toISOString(),
    pagination: { pages: pages.length, complete: true, atomic: pages.length === 1 },
    snapshot_timestamps: pages.map(page => ({ as_of_ts_ms: page.data.as_of_ts_ms ?? null, resume: page.data.resume ?? null })),
    bookmakers_returned: [...included].sort(),
    requested_bookmakers_without_returned_lines: requestedBookmakers.filter(book => !included.has(book)),
    excluded_bookmakers: excluded, skipped_rows: skipped,
    total_groups: result.length, displayed_groups: Math.min(maxGroups, result.length), truncated: result.length > maxGroups,
    groups: result.slice(0, maxGroups),
  };
}

export function markdown(result) {
  if (!result.groups) return JSON.stringify(result, null, 2);
  const lines = [`# Odds comparison: ${md(result.event_id)}`, '', `Retrieved: ${result.retrieved_at}. Pages: ${result.pagination.pages}. Groups: ${result.displayed_groups}/${result.total_groups}.`, ''];
  for (const group of result.groups) {
    const s = group.selection;
    lines.push(`## ${md(group.selection_name)} | ${md(s.bet_type)} | ${md(s.metric)} | ${md(s.period_str ?? s.period)} | line ${md(s.line)}`, '',
      `Identity: ${md(JSON.stringify(s))}`, '', '| Bookmaker | Decimal | American | Accepted UTC | Freshness | Best fresh |', '|---|---:|---:|---|---|---|');
    for (const quote of group.quotes) lines.push(`| ${md(quote.bookmaker)} | ${quote.odds_decimal} | ${quote.odds_american} | ${quote.accepted_at || 'Unknown'} | ${quote.freshness} | ${group.best_fresh_quotes.includes(quote.bookmaker) ? 'Yes' : ''} |`);
    lines.push('');
  }
  lines.push(`Excluded bookmakers: ${md(JSON.stringify(result.excluded_bookmakers))}`, `Requested without lines: ${md(result.requested_bookmakers_without_returned_lines.join(', ')) || 'None'}`, `Skipped rows: ${md(JSON.stringify(result.skipped_rows))}`);
  if (result.truncated) lines.push('Output truncated. Narrow the selection or market filters.');
  if (result.pagination.pages > 1) lines.push('Pages were fetched sequentially; this is not an atomic capture.');
  if (!result.groups.length) lines.push('No eligible sportsbook quotes matched these filters.');
  return lines.join('\n');
}

export async function main(argv = process.argv.slice(2)) {
  const { command, options: o } = parseArgs(argv, [...discoveryFlags, 'event-id', 'bookmakers', 'types', 'periods', 'selection-key', 'market-key', 'max-groups', 'format']);
  if (o.help || !command) {
    console.log(`Sports Odds Comparison — Node.js 22+, runtime ODDS_API_KEY\n\nCommands:\n  catalog --kind sports|leagues|bookmakers [--sport SPORT] [--country-code CC]\n  events --sport SPORT [--league LEAGUE] --from UTC --to UTC [--team NAME] [--limit 200]\n  compare --event-id ID [--bookmakers KEYS] [--types TYPES] [--periods LABELS]\n          [--selection-key KEY] [--market-key KEY] [--max-groups 100]\n\n--format json|markdown (default json). UTC bounds must end in Z.\nNo credentials are accepted as arguments. Network calls are read-only.`);
    return;
  }
  if (!['catalog', 'events', 'compare'].includes(command)) throw new SkillError('Unknown command. Use --help.');
  if (o.format && !['json', 'markdown'].includes(o.format)) throw new SkillError('--format must be json or markdown.');
  let result;
  if (command === 'compare') {
    assertOptions(o, ['event-id', 'bookmakers', 'types', 'periods', 'selection-key', 'market-key', 'max-groups', 'format']);
    const maxGroups = integer(o['max-groups'], 100, 1, 500, '--max-groups');
    const pages = await snapshots(createClient(), o['event-id'], { bookmakers: o.bookmakers, types: o.types, periods: o.periods });
    result = comparePages(pages, { selectionKey: o['selection-key'], marketKey: o['market-key'], maxGroups, requestedBookmakers: o.bookmakers?.split(',').map(value => value.trim()).filter(Boolean) });
  } else result = await discover(createClient(), command, o);
  console.log(o.format === 'markdown' ? markdown(result) : JSON.stringify(result, null, 2));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main().catch(fail);
