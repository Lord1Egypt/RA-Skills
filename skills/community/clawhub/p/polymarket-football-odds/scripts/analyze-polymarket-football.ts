#!/usr/bin/env -S node --experimental-strip-types

declare const process: {
  argv?: string[];
  env?: Record<string, string | undefined>;
  exitCode?: number;
} | undefined;

type JsonObject = Record<string, unknown>;

type CliOptions = {
  input?: string;
  json: boolean;
  selfTest: boolean;
  help: boolean;
  fixtureId?: number;
  date?: string;
  days: number;
};

export type AnalyzePolymarketFootballOptions = {
  input: string;
  apiKey: string;
  fixtureId?: number;
  date?: string;
  days?: number;
};

type GammaMarket = JsonObject & {
  slug?: string;
  question?: string;
  title?: string;
  marketTitle?: string;
  outcomes?: string[] | string;
  outcomePrices?: string[] | string;
  lastTradePrice?: number | string;
  bestBid?: number | string;
  bestAsk?: number | string;
};

type GammaEvent = JsonObject & {
  id?: string;
  slug?: string;
  title?: string;
  ticker?: string;
  subtitle?: string;
  description?: string;
  startDate?: string;
  endDate?: string;
  eventDate?: string;
  gameStartTime?: string;
  markets?: GammaMarket[];
};

type PolymarketInfo = {
  input: string;
  slug: string;
  slugKind: "event" | "market" | "unknown";
  event?: GammaEvent;
  market?: GammaMarket;
  title?: string;
  candidateTeams: string[];
  kickoff?: string;
  marketPrices: Array<{ outcome: string; price?: number }>;
  targetTeam?: string;
};

type ApiEnvelope<T> = {
  get?: string;
  parameters?: JsonObject;
  errors?: unknown[] | JsonObject;
  results?: number;
  paging?: JsonObject;
  response: T;
};

type TeamSearchItem = {
  team?: {
    id?: number;
    name?: string;
    country?: string;
    code?: string;
  };
};

type Fixture = {
  fixture?: {
    id?: number;
    date?: string;
    timestamp?: number;
    status?: JsonObject;
  };
  league?: {
    id?: number;
    name?: string;
    country?: string;
    season?: number;
    round?: string;
  };
  teams?: {
    home?: { id?: number; name?: string; winner?: boolean | null };
    away?: { id?: number; name?: string; winner?: boolean | null };
  };
  goals?: { home?: number | null; away?: number | null };
};

type FixtureMatch = {
  fixture: Fixture;
  score: number;
  confidence: "high" | "medium" | "low";
  mapping: {
    firstTeamSide?: "home" | "away";
    secondTeamSide?: "home" | "away";
  };
  candidates: Array<{ id?: number; home?: string; away?: string; date?: string; score: number }>;
};

type Prediction = {
  predictions?: {
    winner?: { id?: number; name?: string; comment?: string };
    win_or_draw?: boolean;
    under_over?: string;
    goals?: { home?: string; away?: string };
    advice?: string;
    percent?: { home?: string; draw?: string; away?: string };
  };
  league?: JsonObject;
  teams?: {
    home?: { id?: number; name?: string };
    away?: { id?: number; name?: string };
  };
};

export type AnalysisResult = {
  polymarket: {
    slug: string;
    title?: string;
    teams: string[];
    kickoff?: string;
    marketPrices: Array<{ outcome: string; price?: number }>;
    targetTeam?: string;
  };
  fixture?: {
    id?: number;
    date?: string;
    league?: string;
    country?: string;
    home?: string;
    away?: string;
    confidence?: "high" | "medium" | "low";
    score?: number;
  };
  prediction?: {
    home?: string;
    draw?: string;
    away?: string;
    homeTeam?: string;
    awayTeam?: string;
    targetTeam?: string;
    targetTeamWin?: string;
    winner?: string;
    advice?: string;
  };
  fixtureCandidates?: FixtureMatch["candidates"];
};

const API_BASE = "https://v3.football.api-sports.io";
const GAMMA_BASE = "https://gamma-api.polymarket.com";

async function main(): Promise<void> {
  const options = parseArgs(process?.argv?.slice(2) ?? []);

  if (options.help) {
    printHelp();
    return;
  }

  if (options.selfTest) {
    runSelfTest();
    return;
  }

  if (!options.input) {
    throw new Error("Missing Polymarket URL or slug. Run with --help for usage.");
  }

  const apiKey = getApiFootballKey();
  if (!apiKey) {
    throw new Error("Missing API_FOOTBALL_KEY. Set API_FOOTBALL_KEY, API_SPORTS_KEY, or APIFOOTBALL_KEY in the environment.");
  }

  const result = await analyzePolymarketFootball({
    input: options.input,
    apiKey,
    fixtureId: options.fixtureId,
    date: options.date,
    days: options.days,
  });

  if (options.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    printHumanSummary(result);
  }
}

export async function analyzePolymarketFootball(options: AnalyzePolymarketFootballOptions): Promise<AnalysisResult> {
  const polymarket = await getPolymarketInfo(options.input);
  if (polymarket.candidateTeams.length < 2 && !options.fixtureId) {
    const found = polymarket.title ? ` Title: ${polymarket.title}` : "";
    throw new Error(`Could not confidently extract two teams from Polymarket.${found}`);
  }

  const fixtureMatch = await resolveFixture(options.apiKey, polymarket, {
    input: options.input,
    json: false,
    selfTest: false,
    help: false,
    fixtureId: options.fixtureId,
    date: options.date,
    days: options.days ?? 1,
  });
  const fixtureId = getFixtureId(fixtureMatch.fixture);
  if (!fixtureId) {
    throw new Error("Matched fixture is missing an API-Football fixture ID.");
  }

  const prediction = await getPrediction(options.apiKey, fixtureId);
  return buildResult(polymarket, fixtureMatch, prediction);
}

function parseArgs(args: string[]): CliOptions {
  const options: CliOptions = {
    json: false,
    selfTest: false,
    help: false,
    days: 1,
  };

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--json") {
      options.json = true;
    } else if (arg === "--self-test") {
      options.selfTest = true;
    } else if (arg === "--help" || arg === "-h") {
      options.help = true;
    } else if (arg === "--fixture-id") {
      const value = args[++i];
      if (!value || !/^\d+$/.test(value)) throw new Error("--fixture-id requires a numeric value.");
      options.fixtureId = Number(value);
    } else if (arg === "--date") {
      const value = args[++i];
      if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error("--date requires YYYY-MM-DD.");
      options.date = value;
    } else if (arg === "--days") {
      const value = args[++i];
      if (!value || !/^\d+$/.test(value)) throw new Error("--days requires a non-negative integer.");
      options.days = Number(value);
    } else if (arg.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else if (!options.input) {
      options.input = arg;
    } else {
      throw new Error(`Unexpected argument: ${arg}`);
    }
  }

  return options;
}

function printHelp(): void {
  console.log(`Usage:
  API_FOOTBALL_KEY=... node --experimental-strip-types scripts/analyze-polymarket-football.ts <polymarket-url-or-slug> [options]

Options:
  --json              Print JSON output.
  --fixture-id <id>   Use a known API-Football fixture ID.
  --date YYYY-MM-DD   Override fixture-search date.
  --days <n>          Search plus/minus n days around the date. Default: 1.
  --self-test         Run parser tests without network calls.
  --help              Show this help.`);
}

function getApiFootballKey(): string | undefined {
  if (typeof process === "undefined") return undefined;
  return process.env?.API_FOOTBALL_KEY || process.env?.API_SPORTS_KEY || process.env?.APIFOOTBALL_KEY;
}

async function getPolymarketInfo(input: string): Promise<PolymarketInfo> {
  const extracted = extractPolymarketSlug(input);
  const event = await fetchGammaEvent(extracted.slug);
  const market = event ? choosePrimaryMarket(event, extracted.slug) : await fetchGammaMarket(extracted.slug);
  const eventFromMarket = !event && market ? extractEventFromMarket(market) : undefined;
  const finalEvent = event || eventFromMarket;
  const finalMarket = market || (finalEvent ? choosePrimaryMarket(finalEvent, extracted.slug) : undefined);
  const title = pickFirstString(finalEvent?.title, finalEvent?.ticker, finalMarket?.question, finalMarket?.title, finalMarket?.marketTitle);
  const candidateTeams = extractTeams(finalEvent, finalMarket);
  const marketPrices = extractMarketPrices(finalMarket);
  const kickoff = pickFirstString(
    stringField(finalEvent, "gameStartTime"),
    stringField(finalEvent, "eventDate"),
    stringField(finalEvent, "startDate"),
    stringField(finalEvent, "endDate"),
    stringField(finalMarket, "gameStartTime"),
    stringField(finalMarket, "endDate"),
  );

  return {
    input,
    slug: extracted.slug,
    slugKind: extracted.kind,
    event: finalEvent,
    market: finalMarket,
    title,
    candidateTeams,
    kickoff,
    marketPrices,
    targetTeam: inferTargetTeam(finalMarket, title, candidateTeams),
  };
}

function extractPolymarketSlug(input: string): { slug: string; kind: "event" | "market" | "unknown" } {
  const trimmed = input.trim();
  try {
    const url = new URL(trimmed);
    const segments = url.pathname.split("/").filter(Boolean).map(decodeURIComponent);
    const eventIndex = segments.indexOf("event");
    if (eventIndex >= 0 && segments[eventIndex + 1]) {
      return { slug: segments[eventIndex + 1], kind: "event" };
    }
    const marketIndex = segments.indexOf("market");
    if (marketIndex >= 0 && segments[marketIndex + 1]) {
      return { slug: segments[marketIndex + 1], kind: "market" };
    }
    const last = segments[segments.length - 1];
    if (last) return { slug: last, kind: "unknown" };
  } catch {
    // Treat non-URL input as a raw slug below.
  }

  return { slug: trimmed.replace(/^\/+|\/+$/g, ""), kind: "unknown" };
}

async function fetchGammaEvent(slug: string): Promise<GammaEvent | undefined> {
  const pathResult = await tryFetchJson<GammaEvent>(`${GAMMA_BASE}/events/slug/${encodeURIComponent(slug)}`);
  if (pathResult && objectHasUsefulKeys(pathResult)) return pathResult;

  const queryResult = await tryFetchJson<GammaEvent[] | GammaEvent>(`${GAMMA_BASE}/events?slug=${encodeURIComponent(slug)}`);
  return Array.isArray(queryResult) ? queryResult[0] : queryResult;
}

async function fetchGammaMarket(slug: string): Promise<GammaMarket | undefined> {
  const pathResult = await tryFetchJson<GammaMarket>(`${GAMMA_BASE}/markets/slug/${encodeURIComponent(slug)}`);
  if (pathResult && objectHasUsefulKeys(pathResult)) return pathResult;

  const queryResult = await tryFetchJson<GammaMarket[] | GammaMarket>(`${GAMMA_BASE}/markets?slug=${encodeURIComponent(slug)}`);
  return Array.isArray(queryResult) ? queryResult[0] : queryResult;
}

async function tryFetchJson<T>(url: string, headers?: Record<string, string>): Promise<T | undefined> {
  try {
    return await fetchJson<T>(url, headers);
  } catch {
    return undefined;
  }
}

async function fetchJson<T>(url: string, headers: Record<string, string> = {}): Promise<T> {
  const response = await fetch(url, { headers: { accept: "application/json", ...headers } });
  const text = await response.text();

  if (!response.ok) {
    throw new Error(`HTTP ${response.status} for ${url}: ${text.slice(0, 300)}`);
  }

  try {
    return JSON.parse(text) as T;
  } catch (error) {
    throw new Error(`Invalid JSON from ${url}: ${(error as Error).message}`);
  }
}

function choosePrimaryMarket(event: GammaEvent, slug: string): GammaMarket | undefined {
  const markets = Array.isArray(event.markets) ? event.markets : [];
  if (markets.length === 0) return undefined;

  const exact = markets.find((market) => market.slug === slug);
  if (exact) return exact;

  const moneyline = markets.find((market) => {
    const outcomes = parseStringArray(market.outcomes);
    const teamLikeOutcomes = outcomes.filter(isLikelyTeamName);
    return teamLikeOutcomes.length >= 2;
  });

  return moneyline || markets[0];
}

function extractEventFromMarket(market: GammaMarket): GammaEvent | undefined {
  const events = market.events;
  if (Array.isArray(events) && events.length > 0 && isObject(events[0])) {
    return events[0] as GammaEvent;
  }
  return undefined;
}

function extractTeams(event?: GammaEvent, market?: GammaMarket): string[] {
  const explicit = extractExplicitTeams(event, market);
  if (explicit.length >= 2) return explicit.slice(0, 2);

  const titleTexts = [
    stringField(event, "title"),
    stringField(event, "ticker"),
    stringField(event, "subtitle"),
    stringField(market, "question"),
    stringField(market, "title"),
    stringField(market, "marketTitle"),
  ].filter(Boolean) as string[];

  for (const text of titleTexts) {
    const pair = splitTeamPairFromText(text);
    if (pair.length >= 2) return pair.slice(0, 2);
  }

  const marketOutcomes = parseStringArray(market?.outcomes).filter(isLikelyTeamName);
  if (marketOutcomes.length >= 2) return dedupeNames(marketOutcomes).slice(0, 2);

  const eventMarkets = Array.isArray(event?.markets) ? event.markets : [];
  const outcomeCandidates: string[] = [];
  for (const eventMarket of eventMarkets) {
    outcomeCandidates.push(...parseStringArray(eventMarket.outcomes).filter(isLikelyTeamName));
  }

  return dedupeNames([...explicit, ...outcomeCandidates]).slice(0, 2);
}

function extractExplicitTeams(...objects: Array<JsonObject | undefined>): string[] {
  const keys = [
    "homeTeam",
    "awayTeam",
    "home_team",
    "away_team",
    "homeTeamName",
    "awayTeamName",
    "home",
    "away",
  ];
  const names: string[] = [];

  for (const object of objects) {
    if (!object) continue;
    for (const key of keys) {
      const value = object[key];
      if (typeof value === "string" && isLikelyTeamName(value)) names.push(cleanTeamName(value));
      if (isObject(value)) {
        const name = stringField(value, "name") || stringField(value, "title");
        if (name && isLikelyTeamName(name)) names.push(cleanTeamName(name));
      }
    }
    const teams = object.teams;
    if (Array.isArray(teams)) {
      for (const team of teams) {
        if (typeof team === "string" && isLikelyTeamName(team)) names.push(cleanTeamName(team));
        if (isObject(team)) {
          const name = stringField(team, "name") || stringField(team, "title");
          if (name && isLikelyTeamName(name)) names.push(cleanTeamName(name));
        }
      }
    }
  }

  return dedupeNames(names);
}

function splitTeamPairFromText(text: string): string[] {
  const cleaned = text
    .replace(/\([^)]*\)/g, " ")
    .replace(/\b(moneyline|winner|match result|full time result|to win)\b/gi, " ")
    .replace(/\?/g, " ")
    .trim();

  const patterns = [
    /^will\s+(.+?)\s+(?:beat|defeat|win against)\s+(.+)$/i,
    /^can\s+(.+?)\s+(?:beat|defeat|win against)\s+(.+)$/i,
    /^(.+?)\s+(?:vs\.?|v\.?|versus|at|@)\s+(.+)$/i,
    /^(.+?)\s+-\s+(.+)$/i,
  ];

  for (const pattern of patterns) {
    const match = cleaned.match(pattern);
    if (!match) continue;
    const left = cleanTeamName(match[1]);
    const right = cleanTeamName(match[2]);
    if (isLikelyTeamName(left) && isLikelyTeamName(right)) {
      return [left, right];
    }
  }

  return [];
}

function cleanTeamName(value: string): string {
  return value
    .replace(/\b(will|can|to win|win|wins|beat|defeat|draws?|or draw|yes|no)\b/gi, " ")
    .replace(/\b(home|away)\b/gi, " ")
    .replace(/\s+/g, " ")
    .replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, "")
    .trim();
}

function isLikelyTeamName(value: string): boolean {
  const cleaned = cleanTeamName(value);
  if (cleaned.length < 3) return false;
  if (/^\d+(\.\d+)?%?$/.test(cleaned)) return false;
  if (/^(yes|no|draw|tie|over|under|other|home|away|cancelled)$/i.test(cleaned)) return false;
  if (/^[+-]?\d+(\.\d+)?$/.test(cleaned)) return false;
  return /\p{L}/u.test(cleaned);
}

function inferTargetTeam(market: GammaMarket | undefined, title: string | undefined, teams: string[]): string | undefined {
  const text = [market?.question, market?.title, market?.marketTitle, title].filter(Boolean).join(" ").toLowerCase();
  if (!text) return undefined;

  const mentioned = teams.filter((team) => text.includes(team.toLowerCase()));
  if (mentioned.length === 1 && /\b(win|wins|beat|defeat)\b/i.test(text)) return mentioned[0];
  return undefined;
}

function extractMarketPrices(market?: GammaMarket): Array<{ outcome: string; price?: number }> {
  if (!market) return [];
  const outcomes = parseStringArray(market.outcomes);
  const prices = parseStringArray(market.outcomePrices);
  return outcomes.map((outcome, index) => ({
    outcome,
    price: toNumber(prices[index]),
  }));
}

async function resolveFixture(apiKey: string, polymarket: PolymarketInfo, options: CliOptions): Promise<FixtureMatch> {
  if (options.fixtureId) {
    const fixture = await getFixtureById(apiKey, options.fixtureId);
    return {
      fixture,
      score: 2,
      confidence: "high",
      mapping: mapTeamsToFixture(polymarket.candidateTeams, fixture),
      candidates: fixtureToCandidates([fixture], polymarket.candidateTeams),
    };
  }

  const date = options.date || dateOnly(polymarket.kickoff);
  let fixtures: Fixture[] = [];

  if (date) {
    const dates = datesAround(date, options.days);
    const nested = await Promise.all(dates.map((day) => getFixturesByDate(apiKey, day)));
    fixtures = nested.flat();
  }

  if (fixtures.length === 0 && polymarket.candidateTeams[0]) {
    fixtures = await getFixturesByTeamSearch(apiKey, polymarket.candidateTeams[0]);
  }

  if (fixtures.length === 0) {
    throw new Error("API-Football returned no fixtures for the inferred date/team search.");
  }

  const scored = fixtureToCandidates(fixtures, polymarket.candidateTeams)
    .sort((a, b) => b.score - a.score)
    .slice(0, 8);

  const bestCandidate = scored[0];
  if (!bestCandidate || bestCandidate.score < 1.2) {
    throw new Error(`Could not confidently match an API-Football fixture. Best candidates: ${JSON.stringify(scored.slice(0, 5), null, 2)}`);
  }

  const bestFixture = fixtures.find((fixture) => getFixtureId(fixture) === bestCandidate.id);
  if (!bestFixture) throw new Error("Internal fixture matching error.");

  const runnerUp = scored[1]?.score ?? 0;
  const confidence = bestCandidate.score >= 1.8 && bestCandidate.score - runnerUp >= 0.25
    ? "high"
    : bestCandidate.score >= 1.5
      ? "medium"
      : "low";

  return {
    fixture: bestFixture,
    score: bestCandidate.score,
    confidence,
    mapping: mapTeamsToFixture(polymarket.candidateTeams, bestFixture),
    candidates: scored,
  };
}

async function getFixtureById(apiKey: string, fixtureId: number): Promise<Fixture> {
  const envelope = await footballGet<Fixture[]>(apiKey, "/fixtures", { id: String(fixtureId) });
  const fixture = envelope.response[0];
  if (!fixture) throw new Error(`No API-Football fixture found for id ${fixtureId}.`);
  return fixture;
}

async function getFixturesByDate(apiKey: string, date: string): Promise<Fixture[]> {
  const envelope = await footballGet<Fixture[]>(apiKey, "/fixtures", { date });
  return envelope.response || [];
}

async function getFixturesByTeamSearch(apiKey: string, teamName: string): Promise<Fixture[]> {
  const teams = await footballGet<TeamSearchItem[]>(apiKey, "/teams", { search: teamName });
  const ids = (teams.response || [])
    .map((item) => item.team?.id)
    .filter((id): id is number => typeof id === "number")
    .slice(0, 3);

  const all: Fixture[] = [];
  for (const id of ids) {
    const next = await footballGet<Fixture[]>(apiKey, "/fixtures", { team: String(id), next: "20" });
    all.push(...(next.response || []));
  }
  return all;
}

async function getPrediction(apiKey: string, fixtureId: number): Promise<Prediction | undefined> {
  const envelope = await footballGet<Prediction[]>(apiKey, "/predictions", { fixture: String(fixtureId) });
  return envelope.response?.[0];
}

async function footballGet<T>(apiKey: string, path: string, params: Record<string, string>): Promise<ApiEnvelope<T>> {
  const url = new URL(`${API_BASE}${path}`);
  for (const [key, value] of Object.entries(params)) {
    url.searchParams.set(key, value);
  }

  const envelope = await fetchJson<ApiEnvelope<T>>(url.toString(), { "x-apisports-key": apiKey });
  const errors = envelope.errors;
  const hasErrors = Array.isArray(errors) ? errors.length > 0 : !!errors && Object.keys(errors).length > 0;
  if (hasErrors) {
    throw new Error(`API-Football error for ${path}: ${JSON.stringify(errors)}`);
  }
  return envelope;
}

function fixtureToCandidates(fixtures: Fixture[], teams: string[]): FixtureMatch["candidates"] {
  return fixtures.map((fixture) => ({
    id: getFixtureId(fixture),
    home: fixture.teams?.home?.name,
    away: fixture.teams?.away?.name,
    date: fixture.fixture?.date,
    score: scoreFixture(fixture, teams),
  }));
}

function scoreFixture(fixture: Fixture, teams: string[]): number {
  const first = teams[0] || "";
  const second = teams[1] || "";
  const home = fixture.teams?.home?.name || "";
  const away = fixture.teams?.away?.name || "";

  const direct = nameScore(first, home) + nameScore(second, away);
  const reverse = nameScore(first, away) + nameScore(second, home);
  return round(Math.max(direct, reverse), 3);
}

function mapTeamsToFixture(teams: string[], fixture: Fixture): FixtureMatch["mapping"] {
  const first = teams[0] || "";
  const second = teams[1] || "";
  const home = fixture.teams?.home?.name || "";
  const away = fixture.teams?.away?.name || "";
  const firstHome = nameScore(first, home);
  const firstAway = nameScore(first, away);
  const secondHome = nameScore(second, home);
  const secondAway = nameScore(second, away);

  return {
    firstTeamSide: firstHome >= firstAway && firstHome > 0.4 ? "home" : firstAway > 0.4 ? "away" : undefined,
    secondTeamSide: secondHome >= secondAway && secondHome > 0.4 ? "home" : secondAway > 0.4 ? "away" : undefined,
  };
}

function nameScore(a: string, b: string): number {
  const left = normalizeName(a);
  const right = normalizeName(b);
  if (!left || !right) return 0;
  if (left === right) return 1;
  if (left.includes(right) || right.includes(left)) return 0.9;

  const leftTokens = new Set(left.split(" ").filter(Boolean));
  const rightTokens = new Set(right.split(" ").filter(Boolean));
  const intersection = [...leftTokens].filter((token) => rightTokens.has(token)).length;
  const union = new Set([...leftTokens, ...rightTokens]).size;
  return union ? intersection / union : 0;
}

function normalizeName(value: string): string {
  return value
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\b(fc|cf|sc|afc|club|the|women|u\d{2})\b/g, " ")
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function buildResult(polymarket: PolymarketInfo, fixtureMatch: FixtureMatch, prediction?: Prediction): AnalysisResult {
  const fixture = fixtureMatch.fixture;
  const percent = prediction?.predictions?.percent || {};
  const homeTeam = fixture.teams?.home?.name;
  const awayTeam = fixture.teams?.away?.name;
  const targetSide = polymarket.targetTeam ? sideForTeam(polymarket.targetTeam, fixture) : undefined;
  const targetTeamWin = targetSide === "home" ? percent.home : targetSide === "away" ? percent.away : undefined;

  return {
    polymarket: {
      slug: polymarket.slug,
      title: polymarket.title,
      teams: polymarket.candidateTeams,
      kickoff: polymarket.kickoff,
      marketPrices: polymarket.marketPrices,
      targetTeam: polymarket.targetTeam,
    },
    fixture: {
      id: getFixtureId(fixture),
      date: fixture.fixture?.date,
      league: fixture.league?.name,
      country: fixture.league?.country,
      home: homeTeam,
      away: awayTeam,
      confidence: fixtureMatch.confidence,
      score: fixtureMatch.score,
    },
    prediction: prediction ? {
      home: percent.home,
      draw: percent.draw,
      away: percent.away,
      homeTeam,
      awayTeam,
      targetTeam: polymarket.targetTeam,
      targetTeamWin,
      winner: prediction.predictions?.winner?.name,
      advice: prediction.predictions?.advice,
    } : undefined,
    fixtureCandidates: fixtureMatch.candidates,
  };
}

function sideForTeam(team: string, fixture: Fixture): "home" | "away" | undefined {
  const homeScore = nameScore(team, fixture.teams?.home?.name || "");
  const awayScore = nameScore(team, fixture.teams?.away?.name || "");
  if (homeScore >= awayScore && homeScore > 0.4) return "home";
  if (awayScore > 0.4) return "away";
  return undefined;
}

function printHumanSummary(result: AnalysisResult): void {
  console.log(`Polymarket: ${result.polymarket.title || result.polymarket.slug}`);
  console.log(`Extracted teams: ${result.polymarket.teams.join(" vs ") || "unknown"}`);
  if (result.polymarket.kickoff) console.log(`Polymarket date: ${result.polymarket.kickoff}`);
  console.log("");

  if (result.fixture) {
    const fixtureLine = [
      result.fixture.home,
      result.fixture.away ? `vs ${result.fixture.away}` : undefined,
      result.fixture.league ? `(${result.fixture.league}${result.fixture.country ? `, ${result.fixture.country}` : ""})` : undefined,
    ].filter(Boolean).join(" ");
    console.log(`API-Football fixture: ${fixtureLine}`);
    console.log(`Fixture ID: ${result.fixture.id ?? "unknown"} | Date: ${result.fixture.date ?? "unknown"} | Match confidence: ${result.fixture.confidence}`);
  }

  if (!result.prediction) {
    console.log("Prediction: unavailable for this fixture.");
    return;
  }

  console.log("");
  console.log("API-Football prediction:");
  console.log(`- ${result.prediction.homeTeam || "Home"} win: ${result.prediction.home || "n/a"}`);
  console.log(`- Draw: ${result.prediction.draw || "n/a"}`);
  console.log(`- ${result.prediction.awayTeam || "Away"} win: ${result.prediction.away || "n/a"}`);
  if (result.prediction.targetTeam && result.prediction.targetTeamWin) {
    console.log(`- ${result.prediction.targetTeam} win probability: ${result.prediction.targetTeamWin}`);
  }
  if (result.prediction.winner) console.log(`Predicted winner: ${result.prediction.winner}`);
  if (result.prediction.advice) console.log(`Advice: ${result.prediction.advice}`);

  if (result.polymarket.marketPrices.length > 0) {
    console.log("");
    console.log("Polymarket prices found:");
    for (const item of result.polymarket.marketPrices) {
      console.log(`- ${item.outcome}: ${item.price ?? "n/a"}`);
    }
  }
}

function parseStringArray(value: unknown): string[] {
  if (!value) return [];
  if (Array.isArray(value)) return value.map(String);
  if (typeof value !== "string") return [];
  const trimmed = value.trim();
  if (!trimmed) return [];
  try {
    const parsed = JSON.parse(trimmed);
    if (Array.isArray(parsed)) return parsed.map(String);
  } catch {
    // Fall through to delimiter parsing.
  }
  return trimmed.split(",").map((part) => part.trim()).filter(Boolean);
}

function datesAround(date: string, days: number): string[] {
  const base = new Date(`${date}T12:00:00Z`);
  const results: string[] = [];
  for (let offset = -days; offset <= days; offset += 1) {
    const next = new Date(base);
    next.setUTCDate(base.getUTCDate() + offset);
    results.push(next.toISOString().slice(0, 10));
  }
  return results;
}

function dateOnly(value?: string): string | undefined {
  if (!value) return undefined;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return undefined;
  return date.toISOString().slice(0, 10);
}

function getFixtureId(fixture: Fixture): number | undefined {
  return fixture.fixture?.id;
}

function objectHasUsefulKeys(value: unknown): boolean {
  return isObject(value) && Object.keys(value).length > 0;
}

function isObject(value: unknown): value is JsonObject {
  return typeof value === "object" && value !== null;
}

function stringField(object: unknown, key: string): string | undefined {
  if (!isObject(object)) return undefined;
  const value = object[key];
  return typeof value === "string" && value.trim() ? value : undefined;
}

function pickFirstString(...values: Array<string | undefined>): string | undefined {
  return values.find((value) => typeof value === "string" && value.trim().length > 0);
}

function toNumber(value: unknown): number | undefined {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && value.trim() !== "") {
    const parsed = Number(value);
    if (Number.isFinite(parsed)) return parsed;
  }
  return undefined;
}

function dedupeNames(names: string[]): string[] {
  const seen = new Set<string>();
  const results: string[] = [];
  for (const name of names.map(cleanTeamName).filter(isLikelyTeamName)) {
    const key = normalizeName(name);
    if (seen.has(key)) continue;
    seen.add(key);
    results.push(name);
  }
  return results;
}

function round(value: number, digits: number): number {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function runSelfTest(): void {
  const slug = extractPolymarketSlug("https://polymarket.com/event/epl-arsenal-chelsea-2026-05-30?tid=123");
  assert(slug.slug === "epl-arsenal-chelsea-2026-05-30", "extract event slug");

  const teamsFromTitle = splitTeamPairFromText("Arsenal vs. Chelsea");
  assert(teamsFromTitle[0] === "Arsenal" && teamsFromTitle[1] === "Chelsea", "split vs title");

  const teamsFromQuestion = splitTeamPairFromText("Will Arsenal beat Chelsea?");
  assert(teamsFromQuestion[0] === "Arsenal" && teamsFromQuestion[1] === "Chelsea", "split beat question");

  const event = {
    title: "Liverpool vs Manchester City",
    markets: [{ outcomes: "[\"Liverpool\",\"Draw\",\"Manchester City\"]" }],
  } satisfies GammaEvent;
  const teams = extractTeams(event, event.markets?.[0]);
  assert(teams[0] === "Liverpool" && teams[1] === "Manchester City", "extract teams from event");

  const fixture: Fixture = {
    fixture: { id: 1, date: "2026-05-30T12:00:00Z" },
    teams: { home: { name: "Manchester City" }, away: { name: "Liverpool" } },
  };
  assert(scoreFixture(fixture, ["Liverpool", "Manchester City"]) > 1.7, "score reversed fixture");

  console.log("Self-test passed.");
}

function assert(condition: boolean, message: string): void {
  if (!condition) throw new Error(`Self-test failed: ${message}`);
}

function isCliEntryPoint(): boolean {
  if (typeof process === "undefined" || !process.argv?.[1]) return false;
  return import.meta.url === new URL(process.argv[1], "file://").href;
}

if (isCliEntryPoint()) {
  main().catch((error) => {
    console.error((error as Error).message);
    if (typeof process !== "undefined") process.exitCode = 1;
  });
}
