#!/usr/bin/env node
// mpx — fetch + decode MaxPreps _next/data JSON. No deps, no auth.
//
//   mpx.mjs <kind> [path]      fetch https://www.maxpreps.com/_next/data/<buildId>/<path>.json
//   mpx.mjs <kind> < file.json decode a payload already on stdin
//   mpx.mjs search "myers park"
//   mpx.mjs buildid
//
// kinds: search teams roster schedule stats rankings teamrankings standings
//        statcats statleaders team school athlete raw buildid
// flags: --all (keep isDeleted rows)  --raw (skip decoding, emit pageProps)

import { readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { readFile, writeFile } from 'node:fs/promises';

const HOST = 'https://www.maxpreps.com';
const UA =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';
const CACHE = join(tmpdir(), 'maxpreps-buildid.json');
const CACHE_TTL_MS = 6 * 60 * 60 * 1000;

// --- positional key maps, lifted verbatim from the site bundle -------------
// The site ships rows as bare arrays and rehydrates via deserializeObject:
//   a[keys[i]] = row[i]      // later duplicate keys overwrite earlier ones
// Duplicates below are intentional and mirror the site (values are identical).

const ROSTER_KEYS = ['linkedAthlete', 'linkedParents', 'canStartChat', 'accountInformation', 'athleteId', 'firstName', 'lastName', 'classYear', 'jersey', 'heightInches', 'heightFeet', 'weight', 'position1', 'position2', 'position3', 'hasStats', 'isCaptain', 'isDeleted', 'photoUrl', 'secondaryPhotoUrl', 'weightClass', 'isPlayerOfTheGame', 'isFemale', 'bio', 'hasPhoto', 'rosterId', 'schoolId', 'sportSeasonId', 'sportSeasonName', 'careerProfileId', 'createdOn', 'canonicalUrl', 'formattedPositions', 'formattedName', 'formattedHeight', 'calculatedHeight', 'formattedClassYear'];

const CONTEST_KEYS = ['teams', 'contestId', 'createdOn', 'isDeleted', 'hasResult', 'location', 'details', 'state', 'city', 'name', 'dateCode', 'date', 'tournamentBracketId', 'tournamentId', 'sportSeasonId', 'contestState', 'allowEditContestResults', 'hasContestPage', 'canonicalUrl', 'isDateTba', 'isTimeTba', 'contestAlias', 'isLiveGameInProgress', 'overtimePeriodsPlayed', 'overtimeShortAlias', 'currentLivePeriod', 'currentScorerUserId', 'rolesWhoCanEnterScores', 'reasonWhyCannotEnterScores', 'description', 'isLiveScoringEnabled', 'isGameChangerConnected', 'hasGameChangerImportedStats', 'bracketGameIndex', 'bracketGamesInMatchup', 'goFanUrl', 'nfhsStreamUrl', 'currentTeam', 'opponentTeam', 'bracketMatchupId', 'bracketIsPublished'];

const TEAM_KEYS = ['id', 'teamId', 'sportSeasonId', 'resultString', 'index', 'result', 'score', 'isTeamTBA', 'isForfeit', 'isDeleted', 'hasStats', 'homeAwayType', 'contestType', 'teamCanonicalUrl', 'name', 'city', 'state', 'address', 'zipCode', 'formattedName', 'mascotUrl', 'mascot', 'color1', 'color2', 'schoolNameAcronym', 'teamId', 'contestId', 'sportSeasonId', 'teamId', 'calculatedTeamContestResult', 'currentLiveScore', 'resultString'];

const CLASS_YEAR = { 9: 'Fr.', 10: 'So.', 11: 'Jr.', 12: 'Sr.' };

const deObj = (keys, row) => {
  if (row == null) return null;
  if (!Array.isArray(row)) return row; // already hydrated
  const o = {};
  for (let i = 0; i < keys.length; i++) o[keys[i]] = row[i];
  return o;
};
const deArr = (keys, rows) => (Array.isArray(rows) ? rows.map((r) => deObj(keys, r)) : []);

// Piping into `head` closes stdout early; that is not an error worth a stack trace.
process.stdout.on('error', (e) => {
  if (e.code === 'EPIPE') process.exit(0);
  throw e;
});

const die = (msg, code = 1) => {
  process.stderr.write(`mpx: ${msg}\n`);
  process.exit(code);
};

// --- buildId --------------------------------------------------------------

async function scrapeBuildId() {
  const res = await fetch(HOST + '/', { headers: { 'user-agent': UA } });
  if (!res.ok) die(`homepage returned ${res.status} while resolving buildId`, 4);
  const html = await res.text();
  const m = html.match(/"buildId":"([^"\\]+)/); // value carries a trailing \n escape
  if (!m) die('could not find buildId on the homepage — page shape changed', 5);
  return m[1];
}

async function getBuildId({ fresh = false } = {}) {
  if (!fresh) {
    try {
      const c = JSON.parse(await readFile(CACHE, 'utf8'));
      if (c.buildId && Date.now() - c.at < CACHE_TTL_MS) return c.buildId;
    } catch {
      /* no usable cache */
    }
  }
  const buildId = await scrapeBuildId();
  try {
    await writeFile(CACHE, JSON.stringify({ buildId, at: Date.now() }));
  } catch {
    /* cache is best-effort */
  }
  return buildId;
}

// --- fetch ----------------------------------------------------------------

async function fetchData(path, { fresh = false } = {}) {
  const [bare, qs] = String(path).replace(/^\/+|\/+$/g, '').split('?');
  const buildId = await getBuildId({ fresh });
  const url = `${HOST}/_next/data/${encodeURIComponent(buildId)}/${bare}.json${qs ? '?' + qs : ''}`;
  const res = await fetch(url, { headers: { 'user-agent': UA } });
  if (res.status === 404 && !fresh) return fetchData(path, { fresh: true }); // stale buildId
  if (res.status === 404) die(`404 for /${bare} — path does not exist on maxpreps.com`, 3);
  if (!res.ok) die(`${res.status} fetching ${url}`, 4);
  return res.json();
}

// --- decoders -------------------------------------------------------------

// homeAwayType: 0 = home, 1 = away, 2 = neutral site; anything else (including
// a string like "0") = unknown. Mirrors decodeHomeAway in src/decode.ts.
const HOME_AWAY = ['home', 'away', 'neutral'];
const homeAway = (raw) => (typeof raw === 'number' ? HOME_AWAY[raw] : undefined) ?? 'unknown';

// #0 is a real jersey: fall back only for blank/non-numeric, never a falsy 0.
// Mirrors jerseySortKey in src/decode.ts.
const jerseyKey = (j) => {
  const n = j != null && String(j).trim() !== '' ? Number(j) : NaN;
  return Number.isFinite(n) ? n : Number.MAX_SAFE_INTEGER;
};

const decoders = {
  raw: (p) => p,

  search: (p) => ({
    schools: p.initialSchoolResults ?? [],
    athletes: p.initialCareerResults ?? [],
  }),

  roster: (p, { all }) =>
    deArr(ROSTER_KEYS, p.athleteData)
      .filter((a) => all || !a.isDeleted)
      .map((a) => ({
        ...a,
        name: `${a.firstName ?? ''} ${a.lastName ?? ''}`.trim(),
        classYear: a.classYear,
        classYearLabel: CLASS_YEAR[a.classYear] ?? null,
        height:
          a.heightFeet && a.heightInches != null ? `${a.heightFeet}'${a.heightInches}"` : null,
        positions: [a.position1, a.position2, a.position3].filter(Boolean).join(', '),
      }))
      .sort((x, y) => jerseyKey(x.jersey) - jerseyKey(y.jersey)),

  schedule: (p, { all }) =>
    (Array.isArray(p.contests) ? p.contests : [])
      .map((c) => {
        const o = deObj(CONTEST_KEYS, c);
        o.teams = deArr(TEAM_KEYS, o.teams);
        o.currentTeam = deObj(TEAM_KEYS, o.currentTeam);
        o.opponentTeam = deObj(TEAM_KEYS, o.opponentTeam);
        return o;
      })
      .filter((c) => all || !c.isDeleted)
      .map((c) => ({
        date: c.date,
        opponent: c.opponentTeam?.formattedName ?? null,
        homeAway: homeAway(c.currentTeam?.homeAwayType),
        result: c.currentTeam?.result ?? null,
        teamScore: c.currentTeam?.score ?? null,
        opponentScore: c.opponentTeam?.score ?? null,
        // resultString is winner-first, matching the site's display
        resultString: c.currentTeam?.resultString ?? null,
        hasResult: c.hasResult,
        contestAlias: c.contestAlias,
        details: c.details,
        location: c.location,
        canonicalUrl: c.canonicalUrl,
        contestId: c.contestId,
      })),

  stats: (p) => p.playerStatLeadersData ?? null,

  // Leaderboard page: [<st>/]<sport>[/<season>]/rankings/<page> — the trailing
  // page number is required. 25 teams per page.
  rankings: (p) => {
    const d = p.rankingsListData ?? {};
    return {
      season: d.year ?? null,
      lastUpdated: d.lastUpdated ?? null,
      totalCount: d.totalCount ?? 0,
      teams: (d.rankings ?? []).map((t) => ({
        ...t,
        teamPath: (t.teamLink ?? '')
          .replace(/^https?:\/\/[^/]+\//, '')
          .replace(/\/(?:\d{2}-\d{2}\/)?(?:schedule|roster|stats|rankings|standings)\/?$/, ''),
      })),
    };
  },

  // Stat-leader category index. Each category's `path` is the leaf leaderboard —
  // it is NOT derivable from the stat name, so always take it from here.
  statcats: (p) =>
    (p.statLeadersData?.seasons ?? []).flatMap((s) =>
      (s.categories ?? []).map((c) => ({
        statName: c.statName,
        group: c.groupName,
        subGroup: c.subGroupName,
        nationalAverage: c.nationalAverage,
        contextAverage: c.contextAverage,
        minGamesPlayed: s.minGamesPlayed,
        path: (c.canonicalUrl ?? '').replace(/^https?:\/\/[^/]+\//, '').replace(/\/+$/, ''),
      })),
    ),

  // Leaf stat leaderboard. Stat values are self-describing via `columns`; the
  // surrounding 11-tuple was derived empirically (see references/recipes.md).
  // Note index 5 is CITY and index 6 is SCHOOL, not the other way round.
  statleaders: (p) => {
    const d = p.statLeadersListData ?? {};
    const cols = d.columns ?? [];
    const rows = d.rows ?? [];
    const ok = rows.every((r) => Array.isArray(r) && r.length === 11 && Array.isArray(r[8]) && r[8].length === cols.length);
    if (rows.length && !ok) return { warning: 'stat-leader row shape changed; rows returned undecoded', columns: cols, rawRows: rows };
    return rows.map((r) => ({
      rank: r[4],
      name: `${r[0]} ${r[1]}`.trim(),
      positions: r[3],
      schoolName: r[6],
      city: r[5],
      stateCode: r[10],
      athleteUrl: r[2],
      teamPath: String(r[9] ?? '').replace(/^https?:\/\/[^/]+\//, '').replace(/^\/+/, '')
        .replace(/\/(?:\d{2}-\d{2}\/)?(?:schedule|roster|stats|rankings|standings)\/?$/, ''),
      stats: Object.fromEntries(cols.map((c, i) => [c.displayName || c.name, r[8][i]])),
    }));
  },

  // A single team's rank in each context MaxPreps publishes for it.
  teamrankings: (p) =>
    (p.rankingsData?.contexts ?? []).map((c) => ({
      contextName: c.contextName,
      fullListUrl: c.canonicalUrl,
      nearby: c.entries ?? [],
    })),

  // The conference table the team sits in, plus highlighted stat leaders.
  standings: (p) => ({
    sections: (p.standingsData?.standingSections ?? []).map((s) => ({
      name: s.headerName ?? null,
      fullStandingsUrl: s.fullStandingsLink ?? null,
      teams: s.standings ?? [],
    })),
    leaderStats: p.leaderStats ?? [],
  }),

  team: (p) => ({
    ...(p.teamContext?.data ?? {}),
    seasons: p.teamContext?.teamSeasonPickerData ?? [],
    rankings: p.teamContext?.rankingsData ?? null,
    standings: p.teamContext?.standingsData ?? null,
  }),

  school: (p) => ({
    school: p.schoolContext ?? null,
    nearbySchools: p.nearbySchools ?? [],
    links: p.schoolLinksData ?? null,
  }),

  // Every team path the school actually publishes. Use this to resolve a sport
  // path instead of guessing — gender/level segments are not predictable.
  teams: (p) => {
    const seen = new Map();
    const walk = (n) => {
      if (Array.isArray(n)) return n.forEach(walk);
      if (!n || typeof n !== 'object') return;
      if (typeof n.canonicalUrl === 'string' && n.sport) {
        const path = n.canonicalUrl.replace(/^https?:\/\/[^/]+\//, '').replace(/\/$/, '');
        if (!seen.has(path)) {
          seen.set(path, {
            path,
            sport: n.sport,
            gender: n.gender ?? null,
            level: n.teamLevel ?? n.level ?? null,
            season: n.season ?? null,
            year: n.year ?? null,
          });
        }
      }
      Object.values(n).forEach(walk);
    };
    walk(p);
    return [...seen.values()].sort((a, b) => a.path.localeCompare(b.path));
  },

  athlete: (p) => ({
    name: p.athleteName ?? null,
    career: p.careerContext ?? null,
    history: p.careerHistoryData ?? null,
    availability: p.careerDataAvailability ?? null,
    cards: p.careerHomeCards ?? null,
  }),
};

// --- main -----------------------------------------------------------------

const argv = process.argv.slice(2);
const flags = new Set(argv.filter((a) => a.startsWith('--')));
const [kind, arg] = argv.filter((a) => !a.startsWith('--'));

if (!kind) die(`usage: mpx.mjs <${Object.keys(decoders).join('|')}|buildid> [path]`, 64);

if (kind === 'buildid') {
  process.stdout.write((await getBuildId({ fresh: flags.has('--fresh') })) + '\n');
  process.exit(0);
}

const decode = decoders[kind];
if (!decode) die(`unknown kind "${kind}" — one of: ${Object.keys(decoders).join(', ')}, buildid`, 64);

let payload;
if (kind === 'search') {
  if (!arg) die('search needs a query: mpx.mjs search "myers park"', 64);
  payload = await fetchData(`search?q=${encodeURIComponent(arg)}`);
} else if (arg) {
  payload = await fetchData(arg);
} else {
  const stdin = readFileSync(0, 'utf8');
  if (!stdin.trim()) die('no path argument and empty stdin', 64);
  try {
    payload = JSON.parse(stdin);
  } catch {
    die('stdin is not JSON (did the fetch fail?)', 2);
  }
}

const props = payload?.pageProps ?? payload;
const out = flags.has('--raw') ? props : decode(props, { all: flags.has('--all') });
process.stdout.write(JSON.stringify(out, null, 1) + '\n');
