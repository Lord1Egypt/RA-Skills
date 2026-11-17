import { SkillError, assertOptions, collectPages, eventId, integer, windowBounds } from './api.mjs';

export const discoveryFlags = ['kind', 'sport', 'league', 'country-code', 'from', 'to', 'team', 'limit'];

export async function discover(client, command, options) {
  if (command === 'catalog') {
    assertOptions(options, ['kind', 'sport', 'country-code', 'format']);
    const kind = options.kind || 'sports';
    if (!['sports', 'leagues', 'bookmakers'].includes(kind)) throw new SkillError('--kind must be sports, leagues, or bookmakers.');
    if (options.sport && kind !== 'leagues') throw new SkillError('--sport applies to the leagues catalog.');
    if (options['country-code'] && kind !== 'bookmakers') throw new SkillError('--country-code applies to the bookmakers catalog.');
    const { data } = await client.get('/' + kind, { sport: options.sport, country_code: options['country-code'] });
    if (!Array.isArray(data.items)) throw new SkillError('Catalog response is missing items.');
    return { kind, items: data.items, ...(data.details ? { details: data.details } : {}) };
  }
  assertOptions(options, ['sport', 'league', 'from', 'to', 'team', 'limit', 'format']);
  if (!options.sport) throw new SkillError('Discover a sport first, then supply --sport.');
  const { start, end } = windowBounds(options.from, options.to);
  if (end - start > 7 * 86400000) throw new SkillError('Use an events window of seven days or less.');
  const pages = await collectPages(client, '/events', {
    sport: options.sport, league: options.league,
    start_from: Math.floor(start / 1000), start_to: Math.floor(end / 1000),
    limit: integer(options.limit, 200, 1, 1000, '--limit'),
  });
  const unique = new Map();
  for (const page of pages) for (const row of page.data.items) {
    if (!row || typeof row.event_id !== 'string') throw new SkillError('An event response is missing its canonical event ID.');
    eventId(row.event_id);
    const team = options.team?.toLocaleLowerCase();
    if (team && ![row.home_team, row.away_team].some(name => String(name || '').toLocaleLowerCase().includes(team))) continue;
    unique.set(row.event_id, {
      event_id: row.event_id, sport: row.sport, league: row.league,
      home_team: row.home_team, away_team: row.away_team,
      start_time: row.start_time, live_status: row.live_status ?? row.event_state ?? null,
    });
  }
  return { items: [...unique.values()], pages: pages.length, complete: true };
}

export async function snapshots(client, id, query = {}) {
  eventId(id);
  const pages = await collectPages(client, `/events/${id}/odds/snapshot`, {
    price_fields: 'odds', include_unavailable: false, include_stale: false, ...query,
  }, { snapshot: true });
  if (pages.some(page => page.data.event_id !== id)) throw new SkillError('Snapshot event ID does not match the requested event.');
  return pages;
}
