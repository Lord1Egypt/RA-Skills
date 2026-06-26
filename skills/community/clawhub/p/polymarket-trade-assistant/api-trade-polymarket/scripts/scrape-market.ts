/**
 * Fetch Polymarket event data: Rules, Annotations (Market Context), Comments.
 *
 * Pure HTTP approach — no browser dependency. Uses:
 *   1. Page HTML fetch → parse __NEXT_DATA__ for event info, rules, annotations
 *   2. Gamma API → comments (by numeric Series ID)
 *
 * Usage:
 *   npx tsx scrape-market.ts --slug <event-slug>
 *   npx tsx scrape-market.ts --slug <slug> --sections context,comments,rules
 *   npx tsx scrape-market.ts --slug <slug> --sections comments --comment-limit 20 --comment-sort likes
 *
 * Limitation: "Market Context" tab content that is rendered purely by client-side JS
 * cannot be extracted without a browser. This script returns the raw annotations from
 * __NEXT_DATA__ instead (often marked hidden by Polymarket).
 */

import { parseArgs } from "node:util";

// ── Types ──────────────────────────────────────────────────────────────────

interface CommentItem {
  rank: number;
  user: string;
  body: string;
  likes: number;
  created_at: string;
  is_holder: boolean;
  positions: any[];
}

interface AnnotationItem {
  title: string;
  summary: string;
  hidden: boolean;
  date: string;
  tweets_count: number;
}

interface ScrapeResult {
  slug: string;
  title: string;
  fetched_at: string;
  market_context?: {
    available: boolean;
    source: "next_data_annotations";
    annotations: AnnotationItem[];
  };
  rules?: {
    description: string | null;
    resolution_source: string | null;
  };
  comments?: {
    total: number;
    source: "api";
    items: CommentItem[];
  };
  market_data?: {
    volume: number | null;
    liquidity: number | null;
    markets_count: number;
    outcomes: { question: string; best_bid: number | null; best_ask: number | null }[];
  };
  status: string;
  error?: string;
}

// ── CLI args ───────────────────────────────────────────────────────────────

const { values } = parseArgs({
  options: {
    slug: { type: "string" },
    sections: { type: "string", default: "context,rules,comments" },
    "comment-limit": { type: "string", default: "20" },
    "comment-sort": { type: "string", default: "likes" },
  },
  strict: false,
});

const slug = values.slug as string | undefined;
const sections = ((values.sections as string) ?? "context,rules,comments").split(",").map((s) => s.trim());
const commentLimit = parseInt((values["comment-limit"] as string) ?? "20", 10);
const commentSort = (values["comment-sort"] as string) ?? "likes";

if (!slug) {
  console.log(JSON.stringify({ error: "--slug is required", status: "arg_error" }));
  process.exit(1);
}

// ── HTTP helpers ──────────────────────────────────────────────────────────

const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36";

async function fetchJSON(url: string): Promise<any> {
  const resp = await fetch(url, { headers: { "User-Agent": UA } });
  if (!resp.ok) throw new Error(`HTTP ${resp.status} for ${url}`);
  return resp.json();
}

async function fetchHTML(url: string): Promise<string> {
  const resp = await fetch(url, { headers: { "User-Agent": UA } });
  if (!resp.ok) throw new Error(`HTTP ${resp.status} for ${url}`);
  return resp.text();
}

// ── __NEXT_DATA__ extraction from SSR HTML ────────────────────────────────

interface NextDataInfo {
  title: string;
  description: string;
  resolutionSource: string | null;
  seriesId: string | null;
  eventId: string | null;
  annotations: any[];
  volume: number | null;
  liquidity: number | null;
  markets: any[];
}

function parseNextData(html: string): NextDataInfo | null {
  const match = html.match(/<script[^>]*id=["']__NEXT_DATA__["'][^>]*>([\s\S]*?)<\/script>/);
  if (!match) return null;

  try {
    const data = JSON.parse(match[1]);
    const dh = data?.props?.pageProps?.dehydratedState;
    if (!dh?.queries) return null;

    // Find the event query (key starts with "/api/event/slug")
    const eventQuery = dh.queries.find(
      (q: any) => q.queryKey?.[0] === "/api/event/slug",
    );
    const event = eventQuery?.state?.data ?? {};
    const markets = event.markets ?? [];

    // Find the annotations query
    const annoQuery = dh.queries.find(
      (q: any) => q.queryKey?.[0] === "annotations",
    );
    const annotations = annoQuery?.state?.data ?? [];

    // Extract series numeric ID
    const seriesArr = event.series ?? [];
    const seriesId: string | null = seriesArr[0]?.id ?? null;

    return {
      title: event.title ?? "",
      description: event.description ?? markets[0]?.description ?? "",
      resolutionSource: event.resolutionSource ?? markets[0]?.resolutionSource ?? "",
      seriesId,
      eventId: event.id ?? null,
      annotations,
      volume: event.volume ?? null,
      liquidity: event.liquidity ?? null,
      markets,
    };
  } catch {
    return null;
  }
}

// ── Comments via Gamma API ────────────────────────────────────────────────

async function fetchCommentsAPI(
  entityId: string,
  entityType: string,
  limit: number,
  sort: string,
): Promise<{ total: number; items: CommentItem[] } | null> {
  const order = sort === "newest" ? "createdAt" : "reactionCount";
  const url =
    `https://gamma-api.polymarket.com/comments?parent_entity_type=${entityType}` +
    `&parent_entity_id=${entityId}&order=${order}&ascending=false` +
    `&get_positions=true&limit=${limit}`;

  try {
    const data = await fetchJSON(url);
    if (!Array.isArray(data) || data.length === 0) return null;

    // API may not enforce small limits; truncate client-side
    const sliced = data.slice(0, limit);
    const items: CommentItem[] = sliced.map((c: any, i: number) => ({
      rank: i + 1,
      user: c.profile?.name ?? c.profile?.pseudonym ?? "anonymous",
      body: c.body ?? "",
      likes: c.reactionCount ?? 0,
      created_at: c.createdAt ?? "",
      is_holder: Array.isArray(c.positions) && c.positions.length > 0,
      positions: c.positions ?? [],
    }));

    return { total: items.length, items };
  } catch {
    return null;
  }
}

// ── Event info via Gamma API (fallback when __NEXT_DATA__ unavailable) ────

interface GammaEventInfo {
  title: string;
  description: string;
  resolutionSource: string;
  seriesId: string | null;
  eventId: string | null;
  volume: number | null;
  liquidity: number | null;
  markets: any[];
}

async function fetchEventFromGamma(eventSlug: string): Promise<GammaEventInfo | null> {
  try {
    const events = await fetchJSON(`https://gamma-api.polymarket.com/events?slug=${eventSlug}`);
    const event = Array.isArray(events) ? events[0] : events;
    if (!event) return null;

    const seriesArr = event.series ?? [];
    return {
      title: event.title ?? "",
      description: event.description ?? event.markets?.[0]?.description ?? "",
      resolutionSource: event.resolutionSource ?? "",
      seriesId: seriesArr[0]?.id ?? null,
      eventId: event.id ?? null,
      volume: event.volume ?? null,
      liquidity: event.liquidity ?? null,
      markets: event.markets ?? [],
    };
  } catch {
    return null;
  }
}

// ── Main ───────────────────────────────────────────────────────────────────

async function main() {
  const result: ScrapeResult = {
    slug: slug!,
    title: "",
    fetched_at: new Date().toISOString(),
    status: "ok",
  };

  // ── Step 1: Try __NEXT_DATA__ from page HTML ──────────────────────────
  let nextData: NextDataInfo | null = null;

  const needsNextData = sections.includes("context") || sections.includes("rules");
  if (needsNextData) {
    try {
      const html = await fetchHTML(`https://polymarket.com/event/${slug}`);
      nextData = parseNextData(html);
    } catch {
      // Fall through to Gamma API
    }
  }

  // ── Step 2: Gamma API fallback for event info ─────────────────────────
  let gammaEvent: GammaEventInfo | null = null;
  if (!nextData) {
    gammaEvent = await fetchEventFromGamma(slug!);
  }

  const title = nextData?.title ?? gammaEvent?.title ?? "";
  const seriesId = nextData?.seriesId ?? gammaEvent?.seriesId ?? null;
  const eventId = nextData?.eventId ?? gammaEvent?.eventId ?? null;
  result.title = title;

  // ── Market Context (annotations from __NEXT_DATA__) ───────────────────
  if (sections.includes("context")) {
    const rawAnnotations = nextData?.annotations ?? [];
    const annotations: AnnotationItem[] = rawAnnotations.map((a: any) => ({
      title: a.title ?? "",
      summary: a.summary ?? "",
      hidden: a.hidden ?? true,
      date: a.iso_date_time ?? a.created_at ?? "",
      tweets_count: a.tweets?.length ?? 0,
    }));

    result.market_context = {
      available: annotations.length > 0,
      source: "next_data_annotations",
      annotations,
    };
  }

  // ── Rules ─────────────────────────────────────────────────────────────
  if (sections.includes("rules")) {
    const desc = nextData?.description ?? gammaEvent?.description ?? null;
    const resSrc = nextData?.resolutionSource ?? gammaEvent?.resolutionSource ?? null;
    result.rules = {
      description: desc || null,
      resolution_source: resSrc || null,
    };
  }

  // ── Comments via API ──────────────────────────────────────────────────
  if (sections.includes("comments")) {
    let comments = null;

    if (seriesId) {
      comments = await fetchCommentsAPI(seriesId, "Series", commentLimit, commentSort);
    }
    if (!comments && eventId) {
      comments = await fetchCommentsAPI(eventId, "Event", commentLimit, commentSort);
    }

    result.comments = comments
      ? { total: comments.total, source: "api", items: comments.items }
      : { total: 0, source: "api", items: [] };
  }

  // ── Market data ───────────────────────────────────────────────────────
  const markets = nextData?.markets ?? gammaEvent?.markets ?? [];
  if (markets.length > 0) {
    result.market_data = {
      volume: nextData?.volume ?? gammaEvent?.volume ?? null,
      liquidity: nextData?.liquidity ?? gammaEvent?.liquidity ?? null,
      markets_count: markets.length,
      outcomes: markets.map((m: any) => ({
        question: m.question ?? m.groupItemTitle ?? "",
        best_bid: m.bestBid ?? null,
        best_ask: m.bestAsk ?? null,
      })),
    };
  }

  console.log(JSON.stringify(result, null, 2));
}

main().catch((err) => {
  console.log(
    JSON.stringify({
      slug: slug ?? "",
      title: "",
      fetched_at: new Date().toISOString(),
      status: "fatal_error",
      error: err.message,
    }),
  );
  process.exit(1);
});
