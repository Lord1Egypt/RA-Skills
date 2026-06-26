/**
 * Polaris Report — OpenClaw Skill
 *
 * Intelligence briefs from The Polaris Report.
 * Hundreds of curated sources, 18 categories, bias scored, confidence rated.
 *
 * All requests go to api.thepolarisreport.com (read-only, public endpoints).
 * No credentials, tokens, or user data are sent or stored.
 */

const API_BASE = "https://api.thepolarisreport.com";
const SITE_URL = "https://thepolarisreport.com";

const CATEGORIES = [
  "tech", "policy", "markets", "global", "science", "health",
  "startups", "ai_ml", "cybersecurity", "climate", "defense",
  "realestate", "biotech", "crypto", "politics", "energy", "space", "sports",
];

// ── Helpers ──────────────────────────────────────────────────────────────────

async function apiFetch(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

function confidenceBar(score) {
  const pct = Math.round((score || 0) * 100);
  return `${pct}%`;
}

function briefLink(id) {
  return `${SITE_URL}/brief/${id}`;
}

function footer() {
  return `\n—\nPowered by The Polaris Report\n${SITE_URL}`;
}

// ── /news [category] [limit] ─────────────────────────────────────────────────

async function handleNews(args) {
  let category = null;
  let limit = 5;

  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);
  for (const tok of tokens) {
    if (CATEGORIES.includes(tok.toLowerCase())) {
      category = tok.toLowerCase();
    } else if (/^\d+$/.test(tok)) {
      limit = Math.min(parseInt(tok, 10), 20);
    }
  }

  const params = new URLSearchParams({ limit: String(limit) });
  if (category) params.set("category", category);

  const data = await apiFetch(`/api/v1/agent-feed?${params}`);
  const briefs = data.briefs || [];

  if (briefs.length === 0) {
    return `No briefs found${category ? ` for "${category}"` : ""}. Try a different category.${footer()}`;
  }

  const header = category
    ? `Latest ${category.toUpperCase()} Intelligence`
    : "Latest Intelligence Briefs";

  const lines = [`${header}\n`];

  for (const b of briefs) {
    lines.push(
      `▸ ${b.headline}`,
      `  ${b.category.toUpperCase()} · Confidence ${confidenceBar(b.confidence)} · Bias ${(b.bias || 0).toFixed(2)}`,
      `  ${b.summary}`,
      `  ${briefLink(b.id)}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /brief [topic] ───────────────────────────────────────────────────────────

async function handleBrief(args) {
  const topic = (args || "").trim();
  if (!topic) {
    return "Usage: /brief [topic]\nExample: /brief impact of AI on healthcare";
  }

  const res = await fetch(`${API_BASE}/api/v1/generate/brief`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  });

  if (!res.ok) {
    if (res.status === 429) {
      return "Rate limit reached. Free tier allows 3 brief generations per day.\nUpgrade at https://thepolarisreport.com/pricing";
    }
    throw new Error(`API error ${res.status}`);
  }

  const data = await res.json();
  const b = data.brief;

  const lines = [
    `${b.headline}`,
    `${"─".repeat(40)}`,
    `${b.category.toUpperCase()} · Confidence ${confidenceBar(b.provenance?.confidence_score)} · Bias ${(b.provenance?.bias_score || 0).toFixed(2)}`,
    "",
    b.body,
  ];

  if (b.counter_argument) {
    lines.push("", "Counter-Argument:", b.counter_argument);
  }

  if (data.brief_url) {
    lines.push("", `Read more: ${SITE_URL}${data.brief_url}`);
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /search [query] ──────────────────────────────────────────────────────────

async function handleSearch(args) {
  const query = (args || "").trim();
  if (!query || query.length < 2) {
    return "Usage: /search [query]\nExample: /search semiconductor export controls";
  }

  const params = new URLSearchParams({ q: query, limit: "5" });
  const data = await apiFetch(`/api/v1/search?${params}`);
  const briefs = data.briefs || [];

  if (briefs.length === 0) {
    return `No results for "${query}". Try different keywords.${footer()}`;
  }

  const lines = [`Search: "${query}" — ${data.total} result${data.total !== 1 ? "s" : ""}\n`];

  for (const b of briefs) {
    lines.push(
      `▸ ${b.headline}`,
      `  ${b.category.toUpperCase()} · Confidence ${confidenceBar(b.confidence)} · Bias ${(b.bias || 0).toFixed(2)}`,
      `  ${b.summary}`,
      `  ${briefLink(b.id)}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /trending ────────────────────────────────────────────────────────────────

async function handleTrending() {
  const data = await apiFetch("/api/v1/popular?limit=5");
  const briefs = data.briefs || [];

  if (briefs.length === 0) {
    return `No trending briefs right now. Check back soon.${footer()}`;
  }

  const lines = ["Trending Now\n"];

  for (const b of briefs) {
    const id = b.brief_id || b.id;
    const summary = b.deck || b.summary || "";
    lines.push(
      `▸ ${b.headline}`,
      `  ${b.category.toUpperCase()} · ${b.views_24h || 0} views today · Confidence ${confidenceBar(b.confidence)}`,
      `  ${summary}`,
      `  ${briefLink(id)}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /entities [query] ────────────────────────────────────────────────────────

async function handleEntities(args) {
  const query = (args || "").trim();

  const params = new URLSearchParams({ limit: "10" });
  if (query) params.set("q", query);

  const data = await apiFetch(`/api/v1/entities?${params}`);
  const entities = data.entities || [];

  if (entities.length === 0) {
    return `No entities found${query ? ` matching "${query}"` : ""}. Try a different search.${footer()}`;
  }

  const header = query
    ? `Entities matching "${query}"`
    : "Top Entities by Mention Count";

  const lines = [`${header}\n`];

  for (const e of entities) {
    const ticker = e.ticker ? ` (${e.ticker})` : "";
    lines.push(
      `▸ ${e.name}${ticker}`,
      `  ${(e.type || "unknown").toUpperCase()} · ${e.brief_count} brief${e.brief_count !== 1 ? "s" : ""}${e.last_seen ? ` · Last seen ${e.last_seen.slice(0, 10)}` : ""}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /trending-entities ──────────────────────────────────────────────────────

async function handleTrendingEntities() {
  const data = await apiFetch("/api/v1/entities/trending?limit=10");
  const entities = data.entities || [];

  if (entities.length === 0) {
    return `No trending entities right now. Check back soon.${footer()}`;
  }

  const lines = ["Trending Entities (last 24h)\n"];

  for (const e of entities) {
    const ticker = e.ticker ? ` (${e.ticker})` : "";
    lines.push(
      `▸ ${e.name}${ticker}`,
      `  ${(e.type || "unknown").toUpperCase()} · ${e.mentions_24h} mention${e.mentions_24h !== 1 ? "s" : ""}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /historical [from] [to] ─────────────────────────────────────────────────

async function handleHistorical(args) {
  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);

  if (tokens.length === 0) {
    return "Usage: /historical [from] [to]\nDates in YYYY-MM-DD format. 'to' defaults to today.\nExample: /historical 2026-03-01 2026-03-10";
  }

  const from = tokens[0];
  const to = tokens[1] || new Date().toISOString().slice(0, 10);

  // Basic date validation
  if (!/^\d{4}-\d{2}-\d{2}$/.test(from)) {
    return `Invalid date format: "${from}". Use YYYY-MM-DD.`;
  }
  if (tokens[1] && !/^\d{4}-\d{2}-\d{2}$/.test(to)) {
    return `Invalid date format: "${to}". Use YYYY-MM-DD.`;
  }

  const params = new URLSearchParams({ from, to, limit: "10" });
  const data = await apiFetch(`/api/v1/historical?${params}`);
  const briefs = data.briefs || [];
  const total = data.meta?.total || briefs.length;

  if (briefs.length === 0) {
    return `No briefs found between ${from} and ${to}.${footer()}`;
  }

  const lines = [`Historical Briefs: ${from} to ${to} — ${total} total\n`];

  for (const b of briefs) {
    const date = (b.published_at || "").slice(0, 10);
    lines.push(
      `▸ ${b.headline}`,
      `  ${b.category.toUpperCase()} · ${date} · Confidence ${confidenceBar(b.confidence)} · Bias ${(b.bias || 0).toFixed(2)}`,
      `  ${b.summary}`,
      `  ${briefLink(b.id)}`,
      "",
    );
  }

  if (total > 10) {
    lines.push(`Showing 10 of ${total} results. View all at ${SITE_URL}/feed\n`);
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /timeline [brief_id] ────────────────────────────────────────────────────

async function handleTimeline(args) {
  const briefId = (args || "").trim();
  if (!briefId) {
    return "Usage: /timeline [brief_id]\nExample: /timeline PR-2026-0319-042";
  }

  const data = await apiFetch(`/api/v1/brief/${briefId}/timeline`);
  const timeline = data.timeline || [];

  if (timeline.length === 0) {
    return `No timeline data for ${briefId}.${footer()}`;
  }

  const lines = [
    `${data.headline}`,
    `${"─".repeat(40)}`,
    `${data.update_count} update${data.update_count !== 1 ? "s" : ""} · ${data.source_count} sources`,
    "",
  ];

  for (const t of timeline) {
    const conf = t.confidence ? ` · Confidence ${confidenceBar(t.confidence)}` : "";
    const delta = t.confidence_delta ? ` (${t.confidence_delta > 0 ? "+" : ""}${t.confidence_delta.toFixed(2)})` : "";
    lines.push(
      `v${t.version} — ${(t.timestamp || "").slice(0, 16)}`,
      `  ${t.event}${conf}${delta}`,
      "",
    );
  }

  lines.push(`${briefLink(briefId)}`, footer());
  return lines.join("\n");
}

// ── /forecast [topic] ─────────────────────────────────────────────────────────

async function handleForecast(args) {
  const topic = (args || "").trim();
  if (!topic) {
    return "Usage: /forecast [topic]\nExample: /forecast AI regulation";
  }

  const res = await fetch(`${API_BASE}/api/v1/forecast`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  });

  if (!res.ok) {
    if (res.status === 429) {
      return "Rate limit reached. Try again shortly.";
    }
    throw new Error(`API error ${res.status}`);
  }

  const data = await res.json();
  const predictions = data.predictions || [];

  if (predictions.length === 0) {
    return `No predictions available for "${topic}".${footer()}`;
  }

  const lines = [
    `Forecast: ${topic}`,
    `${"─".repeat(40)}`,
    "",
  ];

  for (const p of predictions) {
    const likelihood = p.likelihood ? ` · ${Math.round(p.likelihood * 100)}% likely` : "";
    const timeframe = p.timeframe ? ` · ${p.timeframe}` : "";
    lines.push(
      `▸ ${p.prediction}`,
      `  ${likelihood}${timeframe}`,
    );
    if (p.signals_to_watch?.length) {
      lines.push(`  Signals: ${p.signals_to_watch.join(", ")}`);
    }
    if (p.falsification_criteria) {
      lines.push(`  Falsified if: ${p.falsification_criteria}`);
    }
    lines.push("");
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /events [type] [subject] ──────────────────────────────────────────────────

async function handleEvents(args) {
  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);
  const params = new URLSearchParams({ limit: "10" });

  const EVENT_TYPES = [
    "acquisition", "funding", "launch", "partnership", "regulatory",
    "leadership_change", "ipo", "merger", "layoff", "expansion",
  ];

  for (const tok of tokens) {
    if (EVENT_TYPES.includes(tok.toLowerCase())) {
      params.set("type", tok.toLowerCase());
    } else {
      // Treat as subject filter
      params.set("subject", tok);
    }
  }

  const data = await apiFetch(`/api/v1/events?${params}`);
  const events = data.events || [];

  if (events.length === 0) {
    return `No events found${tokens.length ? ` matching "${tokens.join(" ")}"` : ""}. Try different filters.${footer()}`;
  }

  const lines = ["Recent Events\n"];

  for (const e of events) {
    const value = e.value ? ` · ${e.currency || "$"}${e.value}` : "";
    const date = e.date ? ` · ${e.date.slice(0, 10)}` : "";
    lines.push(
      `▸ ${(e.type || "event").toUpperCase()}: ${e.subject}${e.object ? ` → ${e.object}` : ""}`,
      `  ${value}${date}`,
      `  ${briefLink(e.brief_id)}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /ticker [symbol] ────────────────────────────────────────────────────────

async function handleTicker(args) {
  const input = (args || "").trim().toUpperCase();
  if (!input) {
    return "Usage: /ticker [symbol]\nExample: /ticker NVDA\nBatch: /ticker NVDA,AAPL,TSLA";
  }

  // If comma-separated, do batch resolve
  if (input.includes(",")) {
    const params = new URLSearchParams({ q: input });
    const data = await apiFetch(`/api/v1/ticker/resolve?${params}`);
    const resolved = data.resolved || [];
    const unresolved = data.unresolved || [];

    if (resolved.length === 0) {
      return `No tickers resolved from "${input}". Check the symbols and try again.${footer()}`;
    }

    const lines = [`Ticker Resolution — ${resolved.length} resolved, ${unresolved.length} unresolved\n`];

    for (const r of resolved) {
      const sector = r.sector ? ` · ${r.sector}` : "";
      lines.push(
        `▸ ${r.ticker} — ${r.entity_name}`,
        `  ${r.exchange || "N/A"} · ${(r.asset_type || "equity").toUpperCase()}${sector}`,
        "",
      );
    }

    if (unresolved.length > 0) {
      lines.push(`Unresolved: ${unresolved.join(", ")}`, "");
    }

    lines.push(footer());
    return lines.join("\n");
  }

  // Single ticker lookup
  const data = await apiFetch(`/api/v1/ticker/${encodeURIComponent(input)}`);

  const sentiment = data.sentiment_score != null
    ? `Sentiment ${data.sentiment_score > 0 ? "+" : ""}${data.sentiment_score}`
    : "No sentiment data";
  const sector = data.sector ? ` · ${data.sector}` : "";
  const trending = data.trending ? " · TRENDING" : "";

  const lines = [
    `${data.ticker} — ${data.entity_name}`,
    `${"─".repeat(40)}`,
    `${data.exchange || "N/A"} · ${(data.asset_type || "equity").toUpperCase()}${sector}`,
    `${data.briefs_24h} brief${data.briefs_24h !== 1 ? "s" : ""} in last 24h · ${sentiment}${trending}`,
    footer(),
  ];

  return lines.join("\n");
}

// ── /ticker-score [symbol] ──────────────────────────────────────────────────

async function handleTickerScore(args) {
  const symbol = (args || "").trim().toUpperCase();
  if (!symbol) {
    return "Usage: /ticker-score [symbol]\nExample: /ticker-score NVDA";
  }

  const data = await apiFetch(`/api/v1/ticker/${encodeURIComponent(symbol)}/score`);

  const signalLabel = {
    strong_bullish: "STRONG BULLISH",
    bullish: "BULLISH",
    neutral: "NEUTRAL",
    bearish: "BEARISH",
    strong_bearish: "STRONG BEARISH",
  };

  const c = data.components;
  const sentCurrent = c.sentiment.current_24h != null
    ? `${c.sentiment.current_24h > 0 ? "+" : ""}${c.sentiment.current_24h}`
    : "N/A";
  const sentWeek = c.sentiment.week_avg != null
    ? `${c.sentiment.week_avg > 0 ? "+" : ""}${c.sentiment.week_avg}`
    : "N/A";

  const lines = [
    `${data.ticker} — Trading Signal`,
    `${"─".repeat(40)}`,
    `Signal: ${signalLabel[data.signal] || data.signal}`,
    `Composite Score: ${data.composite_score > 0 ? "+" : ""}${data.composite_score}`,
    "",
    `Sentiment (40%)`,
    `  24h: ${sentCurrent} · 7d avg: ${sentWeek}`,
    "",
    `Momentum (25%)`,
    `  ${c.momentum.value > 0 ? "+" : ""}${c.momentum.value} · ${c.momentum.direction}`,
    "",
    `Volume (20%)`,
    `  ${c.volume.briefs_24h} briefs today · ${c.volume.briefs_7d} this week`,
    `  Velocity: ${c.volume.daily_avg_this_week}/day (${c.volume.velocity_change_pct > 0 ? "+" : ""}${c.volume.velocity_change_pct}% vs last week)`,
    "",
    `Events (15%)`,
    `  ${c.events.count_7d} event${c.events.count_7d !== 1 ? "s" : ""} in 7d${c.events.latest_type ? ` · Latest: ${c.events.latest_type}` : ""}`,
    "",
    `Sector: ${data.sector || "N/A"} · Exchange: ${data.exchange || "N/A"}`,
    footer(),
  ];

  return lines.join("\n");
}

// ── /sectors [days] ─────────────────────────────────────────────────────────

async function handleSectors(args) {
  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);
  let days = 7;

  for (const tok of tokens) {
    if (/^\d+$/.test(tok)) {
      days = Math.min(90, Math.max(1, parseInt(tok, 10)));
    }
  }

  const params = new URLSearchParams({ days: String(days) });
  const data = await apiFetch(`/api/v1/sectors?${params}`);
  const sectors = data.sectors || [];

  if (sectors.length === 0) {
    return `No sector data available for the last ${days} day${days !== 1 ? "s" : ""}.${footer()}`;
  }

  const lines = [`Sector Overview — last ${days} day${days !== 1 ? "s" : ""}\n`];

  for (const s of sectors) {
    const sentimentStr = s.avg_sentiment > 0 ? `+${s.avg_sentiment}` : `${s.avg_sentiment}`;
    const signalTag = s.signal === "bullish" ? " BULLISH" : s.signal === "bearish" ? " BEARISH" : "";
    lines.push(
      `▸ ${s.sector}${signalTag}`,
      `  ${s.ticker_count} ticker${s.ticker_count !== 1 ? "s" : ""} · ${s.brief_count} brief${s.brief_count !== 1 ? "s" : ""} · Sentiment ${sentimentStr}`,
      `  Top: ${s.top_ticker} (${s.top_brief_count} brief${s.top_brief_count !== 1 ? "s" : ""})`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /portfolio [holdings] ───────────────────────────────────────────────────

async function handlePortfolio(args) {
  const input = (args || "").trim();
  if (!input) {
    return "Usage: /portfolio [ticker:weight, ...]\nExample: /portfolio NVDA:0.30 AAPL:0.25 TSLA:0.20 MSFT:0.25\nWeights are optional (default 0 = equal).";
  }

  // Parse holdings: "NVDA:0.30 AAPL:0.25" or "NVDA AAPL TSLA"
  const tokens = input.split(/[\s,]+/).filter(Boolean);
  const holdings = tokens.map(tok => {
    const parts = tok.split(":");
    const ticker = parts[0].toUpperCase();
    const weight = parts[1] ? Math.min(1, Math.max(0, parseFloat(parts[1]) || 0)) : 0;
    return { ticker, weight };
  }).filter(h => h.ticker);

  // If no weights provided, distribute equally
  const hasWeights = holdings.some(h => h.weight > 0);
  if (!hasWeights) {
    const equal = Math.round((1 / holdings.length) * 100) / 100;
    for (const h of holdings) h.weight = equal;
  }

  if (holdings.length === 0) {
    return "No valid tickers provided. Usage: /portfolio NVDA:0.30 AAPL:0.25";
  }

  const res = await fetch(`${API_BASE}/api/v1/portfolio/feed`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ holdings }),
  });

  if (!res.ok) {
    if (res.status === 429) {
      return "Rate limit reached. Try again shortly.";
    }
    const text = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${text}`);
  }

  const data = await res.json();
  const summary = data.portfolio_summary || [];
  const briefs = data.briefs || [];

  const lines = [
    `Portfolio Analysis — ${data.holdings_resolved} holding${data.holdings_resolved !== 1 ? "s" : ""} resolved`,
    `${"─".repeat(40)}`,
    "",
  ];

  if (data.holdings_unresolved?.length > 0) {
    lines.push(`Unresolved: ${data.holdings_unresolved.join(", ")}`, "");
  }

  // Holdings summary
  lines.push("Holdings:\n");
  for (const h of summary) {
    const sentStr = h.avg_sentiment != null
      ? ` · Sentiment ${h.avg_sentiment > 0 ? "+" : ""}${h.avg_sentiment}`
      : "";
    lines.push(
      `▸ ${h.ticker} (${Math.round(h.weight * 100)}%)`,
      `  ${h.sector || "N/A"} · ${h.briefs_in_period} brief${h.briefs_in_period !== 1 ? "s" : ""}${sentStr}`,
      "",
    );
  }

  // Top briefs
  if (briefs.length > 0) {
    const shown = briefs.slice(0, 5);
    lines.push(`Top ${shown.length} Brief${shown.length !== 1 ? "s" : ""} by Relevance:\n`);
    for (const b of shown) {
      const tickers = b.matching_tickers?.length ? ` · ${b.matching_tickers.join(", ")}` : "";
      lines.push(
        `▸ ${b.headline}`,
        `  Relevance ${b.portfolio_relevance}${tickers}`,
        `  ${briefLink(b.id)}`,
        "",
      );
    }
  }

  if (data.total_briefs > 5) {
    lines.push(`${data.total_briefs} total briefs found. View more at ${SITE_URL}/feed\n`);
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /events-calendar [ticker] [days] ────────────────────────────────────────

async function handleEventsCalendar(args) {
  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);
  const params = new URLSearchParams({ limit: "20" });

  const EVENT_TYPES = [
    "acquisition", "funding", "launch", "partnership", "regulatory",
    "leadership_change", "ipo", "merger", "layoff", "expansion",
  ];

  for (const tok of tokens) {
    if (/^\d+d?$/.test(tok)) {
      const days = parseInt(tok.replace("d", ""), 10);
      params.set("days", String(Math.min(90, Math.max(1, days))));
    } else if (EVENT_TYPES.includes(tok.toLowerCase())) {
      params.set("type", tok.toLowerCase());
    } else {
      // Treat as ticker
      params.set("ticker", tok.toUpperCase());
    }
  }

  const data = await apiFetch(`/api/v1/events/calendar?${params}`);
  const events = data.events || [];

  if (events.length === 0) {
    const tickerHint = data.ticker ? ` for ${data.ticker}` : "";
    return `No events found${tickerHint}. Try a different ticker or time range.${footer()}`;
  }

  const tickerLabel = data.ticker ? ` — ${data.ticker}` : "";
  const typeLabel = data.event_type ? ` (${data.event_type})` : "";
  const lines = [`Events Calendar${tickerLabel}${typeLabel} — ${data.total_events} event${data.total_events !== 1 ? "s" : ""}\n`];

  // Type summary
  if (data.event_types?.length > 0) {
    const summaryParts = data.event_types.slice(0, 5).map(t => `${t.type}: ${t.count}`);
    lines.push(`${summaryParts.join(" · ")}`, "");
  }

  for (const e of events) {
    const value = e.value ? ` · ${e.currency || "$"}${e.value}` : "";
    const date = e.published_at ? e.published_at.slice(0, 10) : "";
    const session = e.market_session ? ` · ${e.market_session}` : "";
    lines.push(
      `▸ ${(e.event_type || "event").toUpperCase()}: ${e.subject}${e.object ? ` → ${e.object}` : ""}`,
      `  ${date}${session}${value}`,
      `  ${e.brief_headline || ""}`,
      `  ${briefLink(e.brief_id)}`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /web-search [query] ─────────────────────────────────────────────────────

async function handleWebSearch(args) {
  const query = (args || "").trim();
  if (!query || query.length < 2) {
    return "Usage: /web-search [query]\nExample: /web-search latest AI breakthroughs";
  }

  const params = new URLSearchParams({ q: query, limit: "5" });
  const data = await apiFetch(`/api/v1/web-search?${params}`);
  const results = data.results || [];

  if (results.length === 0) {
    return `No web results for "${query}".${footer()}`;
  }

  const lines = [`Web Search: "${query}"\n`];

  for (const r of results) {
    lines.push(
      `▸ ${r.title || r.url}`,
      `  ${r.url}`,
    );
    if (r.snippet) {
      lines.push(`  ${r.snippet}`);
    }
    if (r.trust_score != null) {
      lines.push(`  Trust: ${Math.round(r.trust_score * 100)}%`);
    }
    lines.push("");
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /crawl [url] ────────────────────────────────────────────────────────────

async function handleCrawl(args) {
  const url = (args || "").trim();
  if (!url) {
    return "Usage: /crawl [url]\nExample: /crawl https://example.com/article";
  }

  const res = await fetch(`${API_BASE}/api/v1/crawl`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, depth: 1, max_pages: 1, include_links: false }),
  });

  if (!res.ok) {
    if (res.status === 429) {
      return "Rate limit reached. Try again shortly.";
    }
    throw new Error(`API error ${res.status}`);
  }

  const data = await res.json();
  const pages = data.pages || [];

  if (pages.length === 0) {
    return `Could not extract content from ${url}.${footer()}`;
  }

  const lines = [];
  for (const p of pages) {
    lines.push(
      p.title || p.url || url,
      `${"─".repeat(40)}`,
    );
    if (p.word_count) lines.push(`Words: ${p.word_count}`);
    if (p.text) lines.push("", p.text.length > 2000 ? p.text.slice(0, 2000) + "..." : p.text);
    lines.push("");
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /candles [symbol] [range] ────────────────────────────────────────────────

async function handleCandles(args) {
  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);
  const symbol = tokens[0];
  if (!symbol) {
    return "Usage: /candles [symbol] [range]\nExample: /candles NVDA 3mo\nRanges: 1mo, 3mo, 6mo, 1y, 2y, 5y";
  }

  const RANGES = ["1mo", "3mo", "6mo", "1y", "2y", "5y"];
  let range = "6mo";
  if (tokens[1] && RANGES.includes(tokens[1].toLowerCase())) {
    range = tokens[1].toLowerCase();
  }

  const params = new URLSearchParams({ interval: "1d", range });
  const data = await apiFetch(`/api/v1/ticker/${encodeURIComponent(symbol.toUpperCase())}/candles?${params}`);
  const candles = data.candles || [];

  if (candles.length === 0) {
    return `No candle data found for "${symbol.toUpperCase()}".${footer()}`;
  }

  const lines = [
    `${data.ticker} — OHLCV Candles`,
    `${"─".repeat(40)}`,
    `${data.entity_name || ""} · ${data.exchange || "N/A"} · ${data.interval} · ${data.range}`,
    `${data.candle_count} candle${data.candle_count !== 1 ? "s" : ""}`,
    "",
  ];

  // Show last 10
  const shown = candles.slice(-10);
  if (candles.length > 10) {
    lines.push(`(showing last 10 of ${candles.length})`, "");
  }

  for (const c of shown) {
    lines.push(
      `${c.date}  O:${c.open}  H:${c.high}  L:${c.low}  C:${c.close}  V:${(c.volume || 0).toLocaleString()}`,
    );
  }

  lines.push("", footer());
  return lines.join("\n");
}

// ── /technicals [symbol] ────────────────────────────────────────────────────

async function handleTechnicals(args) {
  const symbol = (args || "").trim().toUpperCase();
  if (!symbol) {
    return "Usage: /technicals [symbol]\nExample: /technicals NVDA";
  }

  const data = await apiFetch(`/api/v1/ticker/${encodeURIComponent(symbol)}/technicals`);
  const indicators = data.indicators || {};
  const summary = data.summary || {};

  const signalLabel = {
    strong_buy: "STRONG BUY",
    buy: "BUY",
    neutral: "NEUTRAL",
    sell: "SELL",
    strong_sell: "STRONG SELL",
  };

  const lines = [
    `${data.ticker} — Technical Analysis`,
    `${"─".repeat(40)}`,
    `Signal: ${signalLabel[summary.signal] || summary.signal || "N/A"}`,
    `Buy: ${summary.buy_count || 0} · Sell: ${summary.sell_count || 0} · Neutral: ${summary.neutral_count || 0}`,
    "",
  ];

  const price = data.price || {};
  if (price.close != null) {
    lines.push(`Price: $${price.close} · High: $${price.high} · Low: $${price.low}`, "");
  }

  const indicatorOrder = ["sma_20", "ema_12", "rsi", "macd", "bollinger", "atr", "stochastic", "adx", "obv", "vwap"];
  for (const key of indicatorOrder) {
    const ind = indicators[key];
    if (ind) {
      const val = ind.value != null ? ind.value : ind.latest != null ? ind.latest : "N/A";
      const sig = ind.signal ? ` [${ind.signal.toUpperCase()}]` : "";
      lines.push(`▸ ${key.toUpperCase()}: ${val}${sig}`);
    }
  }

  lines.push("", footer());
  return lines.join("\n");
}

// ── /market-movers ──────────────────────────────────────────────────────────

async function handleMarketMovers() {
  const data = await apiFetch("/api/v1/market/movers");

  const lines = ["Market Movers\n"];

  const sections = [
    { key: "gainers", label: "Top Gainers" },
    { key: "losers", label: "Top Losers" },
    { key: "most_active", label: "Most Active" },
  ];

  for (const { key, label } of sections) {
    const items = data[key] || [];
    if (items.length > 0) {
      lines.push(`${label}:`);
      for (const item of items.slice(0, 5)) {
        const sym = item.symbol || item.ticker || "?";
        const price = item.price != null ? `$${item.price}` : "N/A";
        const change = item.change_percent != null ? item.change_percent : item.changesPercentage;
        lines.push(`  ▸ ${sym} — ${price} (${change != null ? `${change > 0 ? "+" : ""}${change}%` : "N/A"})`);
      }
      lines.push("");
    }
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /economy [indicator] ────────────────────────────────────────────────────

async function handleEconomy(args) {
  const indicator = (args || "").trim().toLowerCase();

  if (indicator && indicator !== "all") {
    const data = await apiFetch(`/api/v1/economy/${encodeURIComponent(indicator)}`);
    const latest = data.latest || {};
    const lines = [
      `${data.name || indicator}`,
      `${"─".repeat(40)}`,
      `Series: ${data.series_id || "N/A"} · ${data.frequency || "N/A"} · ${data.units || "N/A"}`,
      `Latest: ${latest.value || "N/A"} (${latest.date || "N/A"})`,
      "",
    ];

    const observations = (data.observations || []).slice(0, 10);
    if (observations.length > 0) {
      lines.push("Recent observations:");
      for (const obs of observations) {
        lines.push(`  ${obs.date} = ${obs.value}`);
      }
    }

    lines.push("", footer());
    return lines.join("\n");
  }

  // Summary of all indicators
  const data = await apiFetch("/api/v1/economy");
  const indicators = data.indicators || [];

  if (indicators.length === 0) {
    return `No economic data available.${footer()}`;
  }

  const lines = [`Economic Indicators (${indicators.length})\n`];

  for (const ind of indicators) {
    lines.push(
      `▸ ${ind.name || ind.slug}`,
      `  ${ind.latest_value || "N/A"} (${ind.latest_date || "N/A"})`,
      "",
    );
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /crypto [symbol] ────────────────────────────────────────────────────────

async function handleCrypto(args) {
  const symbol = (args || "").trim().toUpperCase();

  if (symbol) {
    const data = await apiFetch(`/api/v1/crypto/${encodeURIComponent(symbol)}`);
    const price = data.price || data.current_price;
    const change = data.change_24h || data.price_change_percentage_24h;

    const lines = [
      `${data.symbol || symbol} — ${data.name || "Unknown"}`,
      `${"─".repeat(40)}`,
      `Price: $${price || "N/A"}`,
      `24h Change: ${change != null ? `${change > 0 ? "+" : ""}${change}%` : "N/A"}`,
      `Market Cap: $${data.market_cap || "N/A"}`,
      `24h Volume: $${data.volume_24h || data.total_volume || "N/A"}`,
    ];

    if (data.ath) {
      lines.push(`ATH: $${data.ath} (${data.ath_change_percentage != null ? `${data.ath_change_percentage}%` : "N/A"})`);
    }

    if (data.market_cap_rank) {
      lines.push(`Rank: #${data.market_cap_rank}`);
    }

    lines.push("", footer());
    return lines.join("\n");
  }

  // Market overview
  const data = await apiFetch("/api/v1/crypto");

  const lines = [
    "Crypto Market Overview",
    `${"─".repeat(40)}`,
    `Total Market Cap: $${data.total_market_cap || "N/A"}`,
    `BTC Dominance: ${data.btc_dominance || "N/A"}%`,
    `24h Volume: $${data.total_volume_24h || "N/A"}`,
    "",
  ];

  const top = data.top_coins || [];
  if (top.length > 0) {
    lines.push("Top Coins:");
    for (const coin of top.slice(0, 10)) {
      const sym = coin.symbol || "?";
      const p = coin.price || coin.current_price || "?";
      const ch = coin.change_24h || coin.price_change_percentage_24h;
      lines.push(`  ▸ ${sym} — $${p} (${ch != null ? `${ch > 0 ? "+" : ""}${ch}%` : "N/A"})`);
    }
    lines.push("");
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /defi [protocol] ────────────────────────────────────────────────────────

async function handleDefi(args) {
  const protocol = (args || "").trim().toLowerCase();

  if (protocol) {
    const data = await apiFetch(`/api/v1/crypto/defi/${encodeURIComponent(protocol)}`);

    const lines = [
      `${data.name || protocol} — DeFi Protocol`,
      `${"─".repeat(40)}`,
      `TVL: $${data.tvl || "N/A"}`,
      `Chain: ${data.chain || data.chains || "N/A"}`,
    ];

    if (data.category) lines.push(`Category: ${data.category}`);
    if (data.url) lines.push(`URL: ${data.url}`);

    const history = data.tvl_history || [];
    if (history.length > 0) {
      lines.push("", "Recent TVL:");
      for (const h of history.slice(-5)) {
        lines.push(`  ${h.date} — $${h.tvl}`);
      }
    }

    lines.push("", footer());
    return lines.join("\n");
  }

  // Overview
  const data = await apiFetch("/api/v1/crypto/defi");

  const lines = [
    "DeFi Overview",
    `${"─".repeat(40)}`,
    `Total TVL: $${data.total_tvl || "N/A"}`,
    "",
  ];

  const protocols = data.top_protocols || data.protocols || [];
  if (protocols.length > 0) {
    lines.push("Top Protocols:");
    for (const p of protocols.slice(0, 10)) {
      lines.push(`  ▸ ${p.name || "?"} — TVL: $${p.tvl || "?"} (${p.chain || p.chains || "N/A"})`);
    }
    lines.push("");
  }

  const chains = data.chains || [];
  if (Array.isArray(chains) && chains.length > 0 && typeof chains[0] === "object") {
    lines.push("Chain TVL:");
    for (const ch of chains.slice(0, 10)) {
      lines.push(`  ▸ ${ch.name || "?"} — $${ch.tvl || "?"}`);
    }
    lines.push("");
  }

  lines.push(footer());
  return lines.join("\n");
}

// ── /screener [query] ────────────────────────────────────────────────────────

async function handleScreener(args) {
  const query = (args || "").trim();
  if (!query) {
    return "Usage: /screener [query]\nExample: /screener oversold tech stocks with upcoming earnings";
  }

  const res = await fetch(`${API_BASE}/api/v1/screener/natural`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, limit: 10 }),
  });

  if (!res.ok) throw new Error(`API error ${res.status}`);
  const data = await res.json();
  const results = data.results || [];

  if (results.length === 0) {
    return `No stocks found matching "${query}".${footer()}`;
  }

  const lines = [
    `Screener: "${query}"`,
    `${"─".repeat(40)}`,
    "",
  ];

  for (const r of results.slice(0, 10)) {
    const ticker = r.ticker || "?";
    const name = r.name || "";
    const sentiment = r.sentiment_score != null ? r.sentiment_score.toFixed(2) : "N/A";
    const sector = r.sector || "N/A";
    lines.push(`▸ ${ticker} — ${name}`);
    lines.push(`  Sentiment: ${sentiment} | Sector: ${sector}`);
  }

  lines.push("", footer());
  return lines.join("\n");
}

// ── /backtest [strategy_json] ────────────────────────────────────────────────

async function handleBacktest(args) {
  const input = (args || "").trim();
  if (!input) {
    return 'Usage: /backtest [strategy JSON]\nExample: /backtest {"entry_filters":{"rsi_below":30},"exit_filters":{"rsi_above":50},"asset_type":"equity","sector":"Semiconductors"}';
  }

  let strategy;
  try {
    strategy = JSON.parse(input);
  } catch {
    return "Invalid JSON. Please provide a valid strategy object.";
  }

  const res = await fetch(`${API_BASE}/api/v1/backtest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ strategy, period: "1y" }),
  });

  if (!res.ok) throw new Error(`API error ${res.status}`);
  const data = await res.json();
  const perf = data.performance || {};

  const lines = [
    "Backtest Results",
    `${"─".repeat(40)}`,
    `Period: ${data.period || "1y"}`,
    `Total Return: ${perf.total_return_pct != null ? `${perf.total_return_pct}%` : "N/A"}`,
    `Max Drawdown: ${perf.max_drawdown_pct != null ? `${perf.max_drawdown_pct}%` : "N/A"}`,
    `Sharpe Ratio: ${perf.sharpe_ratio || "N/A"}`,
    `Win Rate: ${perf.win_rate != null ? `${perf.win_rate}%` : "N/A"}`,
    `Total Trades: ${perf.total_trades || "N/A"}`,
    "",
    footer(),
  ];

  return lines.join("\n");
}

// ── /correlation [tickers] [days] ────────────────────────────────────────────

async function handleCorrelation(args) {
  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);
  if (tokens.length < 2) {
    return "Usage: /correlation [ticker1] [ticker2] [ticker3...] [days]\nExample: /correlation NVDA AMD INTC 90";
  }

  let days = 30;
  const tickers = [];
  for (const tok of tokens) {
    if (/^\d+$/.test(tok)) {
      days = parseInt(tok, 10);
    } else {
      tickers.push(tok.toUpperCase());
    }
  }

  if (tickers.length < 2) {
    return "At least 2 tickers are required for correlation analysis.";
  }

  const res = await fetch(`${API_BASE}/api/v1/correlation`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tickers, days }),
  });

  if (!res.ok) throw new Error(`API error ${res.status}`);
  const data = await res.json();
  const matrix = data.matrix || [];
  const resultTickers = data.tickers || tickers;

  const lines = [
    `Correlation Matrix (${data.period_days || days} day lookback)`,
    `${"─".repeat(40)}`,
    "",
  ];

  // Header
  lines.push("       " + resultTickers.map(t => t.padStart(7)).join(""));
  for (let i = 0; i < matrix.length; i++) {
    const label = (resultTickers[i] || "?").padEnd(6);
    const vals = (matrix[i] || []).map(v =>
      typeof v === "number" ? v.toFixed(2).padStart(7) : "   N/A "
    ).join("");
    lines.push(`${label} ${vals}`);
  }

  lines.push("", footer());
  return lines.join("\n");
}

// ── /price [symbol] ──────────────────────────────────────────────────────────

async function handlePrice(args) {
  const symbol = (args || "").trim().toUpperCase();
  if (!symbol) return "Usage: /price NVDA";

  const data = await apiFetch(`/api/v1/ticker/${encodeURIComponent(symbol)}/price`);
  const arrow = (data.change_pct || 0) >= 0 ? "+" : "";
  const lines = [
    `${data.entity_name || symbol} (${data.ticker || symbol})`,
    `${"─".repeat(30)}`,
    `Price: $${data.price}`,
    `Change: ${arrow}${(data.change_pct || 0).toFixed(2)}%`,
    `Exchange: ${data.exchange || "N/A"}`,
    `Market: ${data.market_state || "N/A"}`,
    footer(),
  ];
  return lines.join("\n");
}

// ── /social [symbol] ─────────────────────────────────────────────────────────

async function handleSocial(args) {
  const symbol = (args || "").trim().toUpperCase();
  if (!symbol) return "Usage: /social NVDA";

  const data = await apiFetch(`/api/v1/ticker/${encodeURIComponent(symbol)}/social`);
  const s = data.social || {};
  const sent = s.sentiment || {};
  const reddit = s.reddit || {};

  const lines = [
    `Social Sentiment: ${data.entity_name || symbol}`,
    `${"─".repeat(30)}`,
    `Overall: ${sent.overall_sentiment || "neutral"} (score: ${sent.score || 0})`,
    `Confidence: ${((sent.confidence || 0) * 100).toFixed(0)}%`,
    `Reddit: ${reddit.post_count || 0} posts`,
    `Bull/Bear/Neutral: ${sent.bull_count || 0}/${sent.bear_count || 0}/${sent.neutral_count || 0}`,
  ];
  if (sent.key_themes && sent.key_themes.length > 0) {
    lines.push("", "Themes:");
    sent.key_themes.slice(0, 5).forEach(t => lines.push(`  • ${t}`));
  }
  lines.push(footer());
  return lines.join("\n");
}

// ── /social-trending ─────────────────────────────────────────────────────────

async function handleSocialTrending() {
  const data = await apiFetch("/api/v1/social/trending");
  const trending = data.trending || [];

  if (trending.length === 0) return "No trending social data right now." + footer();

  const lines = [
    "Trending on Social Media",
    `${"─".repeat(30)}`,
    "",
  ];
  trending.slice(0, 15).forEach((t, i) => {
    lines.push(`${i + 1}. $${t.ticker} — ${t.mention_count} mentions, ${t.sentiment} (${t.score})`);
  });
  lines.push(footer());
  return lines.join("\n");
}

// ── /ipo ─────────────────────────────────────────────────────────────────────

async function handleIpo() {
  const data = await apiFetch("/api/v1/ipo/calendar");
  const ipos = data.ipos || data.filings || [];

  if (ipos.length === 0) return "No upcoming IPOs found." + footer();

  const lines = [
    "IPO Calendar (SEC EDGAR)",
    `${"─".repeat(30)}`,
    "",
  ];
  ipos.slice(0, 10).forEach(ipo => {
    lines.push(`${ipo.company || ipo.entity || "Unknown"}`);
    if (ipo.ticker) lines.push(`  Ticker: ${ipo.ticker}`);
    if (ipo.filed_at || ipo.date) lines.push(`  Date: ${ipo.filed_at || ipo.date}`);
    lines.push("");
  });
  lines.push(footer());
  return lines.join("\n");
}

// ── /alerts [action] ─────────────────────────────────────────────────────────

async function handleAlerts(args) {
  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);
  const action = (tokens[0] || "list").toLowerCase();

  if (action === "list") {
    const data = await apiFetch("/api/v1/alerts");
    const alerts = data.alerts || [];
    if (alerts.length === 0) return "No active alerts. Create one with: /alerts create NVDA price_above 150" + footer();

    const lines = ["Your Alerts", `${"─".repeat(30)}`, ""];
    alerts.forEach(a => {
      lines.push(`${a.ticker} — ${a.type} ${a.threshold || ""} (${a.status || "active"})`);
    });
    lines.push(footer());
    return lines.join("\n");
  }

  return "Usage:\n  /alerts list — view active alerts\n  /alerts create NVDA price_above 150 — create alert\n\nFull alert management available at thepolarisreport.com/developers" + footer();
}

// ── /report [symbol] [tier] ───────────────────────────────────────────────────

async function handleReport(args) {
  const tokens = (args || "").trim().split(/\s+/).filter(Boolean);
  const symbol = (tokens[0] || "").toUpperCase();
  if (!symbol) return "Usage: /report NVDA [quick|full|deep]";

  const tier = (tokens[1] || "quick").toLowerCase();
  if (!["quick", "full", "deep"].includes(tier)) {
    return "Tier must be quick, full, or deep. Example: /report NVDA full";
  }

  const creditCost = tier === "deep" ? 1000 : tier === "full" ? 100 : 10;
  const estTime = tier === "deep" ? "~5 min" : tier === "full" ? "~65 sec" : "~6 sec";

  // Try cached first for quick scans
  if (tier === "quick") {
    try {
      const cached = await apiFetch(`/api/v1/reports/cached/${encodeURIComponent(symbol)}`);
      if (cached && cached.report && cached.report.markdown) {
        return cached.report.markdown + footer();
      }
    } catch { /* not cached, generate fresh */ }
  }

  // Generate report
  try {
    const res = await fetch(`${API_BASE}/api/v1/reports/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ticker: symbol, tier }),
    });
    if (!res.ok) throw new Error(`API error ${res.status}`);
    const data = await res.json();
    const reportId = data.report_id;

    if (!reportId) return `Failed to start report for ${symbol}.`;

    // Poll for completion
    const maxWait = tier === "deep" ? 360000 : tier === "full" ? 120000 : 30000;
    const pollInterval = 3000;
    const start = Date.now();

    while (Date.now() - start < maxWait) {
      await new Promise(r => setTimeout(r, pollInterval));
      try {
        const poll = await apiFetch(`/api/v1/reports/${reportId}`);
        if (poll && poll.report) {
          if (poll.report.status === "complete" && poll.report.markdown) {
            return poll.report.markdown + footer();
          }
          if (poll.report.status === "failed") {
            return `Report generation failed for ${symbol}. Try again.`;
          }
        }
      } catch { /* keep polling */ }
    }

    return `Report is still generating. Check back at: ${SITE_URL}/reports/${reportId}`;
  } catch (err) {
    return `Error generating report for ${symbol}: ${err.message}`;
  }
}

// ── Skill Entry Point ────────────────────────────────────────────────────────

module.exports = {
  name: "polaris-report",

  commands: {
    news: {
      description: "Get the latest verified intelligence briefs",
      execute: async (args) => {
        try {
          return await handleNews(args);
        } catch (err) {
          return `Error fetching briefs: ${err.message}`;
        }
      },
    },

    brief: {
      description: "Generate an intelligence brief on any topic",
      execute: async (args) => {
        try {
          return await handleBrief(args);
        } catch (err) {
          return `Error generating brief: ${err.message}`;
        }
      },
    },

    search: {
      description: "Search verified intelligence",
      execute: async (args) => {
        try {
          return await handleSearch(args);
        } catch (err) {
          return `Error searching: ${err.message}`;
        }
      },
    },

    trending: {
      description: "See what's trending right now",
      execute: async () => {
        try {
          return await handleTrending();
        } catch (err) {
          return `Error fetching trending: ${err.message}`;
        }
      },
    },

    entities: {
      description: "Search extracted entities (people, orgs, products) across briefs",
      execute: async (args) => {
        try {
          return await handleEntities(args);
        } catch (err) {
          return `Error searching entities: ${err.message}`;
        }
      },
    },

    "trending-entities": {
      description: "See which entities are most mentioned in the last 24 hours",
      execute: async () => {
        try {
          return await handleTrendingEntities();
        } catch (err) {
          return `Error fetching trending entities: ${err.message}`;
        }
      },
    },

    historical: {
      description: "Search briefs within a date range",
      execute: async (args) => {
        try {
          return await handleHistorical(args);
        } catch (err) {
          return `Error searching historical briefs: ${err.message}`;
        }
      },
    },

    timeline: {
      description: "See how a living brief evolved over time",
      execute: async (args) => {
        try {
          return await handleTimeline(args);
        } catch (err) {
          return `Error fetching timeline: ${err.message}`;
        }
      },
    },

    forecast: {
      description: "Get structured predictions on what's likely to happen next",
      execute: async (args) => {
        try {
          return await handleForecast(args);
        } catch (err) {
          return `Error fetching forecast: ${err.message}`;
        }
      },
    },

    events: {
      description: "Browse structured events extracted from coverage",
      execute: async (args) => {
        try {
          return await handleEvents(args);
        } catch (err) {
          return `Error fetching events: ${err.message}`;
        }
      },
    },

    ticker: {
      description: "Resolve or look up a ticker symbol",
      execute: async (args) => {
        try {
          return await handleTicker(args);
        } catch (err) {
          return `Error looking up ticker: ${err.message}`;
        }
      },
    },

    "ticker-score": {
      description: "Get composite trading signal for a ticker",
      execute: async (args) => {
        try {
          return await handleTickerScore(args);
        } catch (err) {
          return `Error fetching ticker score: ${err.message}`;
        }
      },
    },

    sectors: {
      description: "Show all sectors with sentiment overview",
      execute: async (args) => {
        try {
          return await handleSectors(args);
        } catch (err) {
          return `Error fetching sectors: ${err.message}`;
        }
      },
    },

    portfolio: {
      description: "Analyze a portfolio of tickers with weights",
      execute: async (args) => {
        try {
          return await handlePortfolio(args);
        } catch (err) {
          return `Error analyzing portfolio: ${err.message}`;
        }
      },
    },

    "events-calendar": {
      description: "Show structured events filterable by ticker",
      execute: async (args) => {
        try {
          return await handleEventsCalendar(args);
        } catch (err) {
          return `Error fetching events calendar: ${err.message}`;
        }
      },
    },

    "web-search": {
      description: "Search the web with optional Polaris trust scoring",
      execute: async (args) => {
        try {
          return await handleWebSearch(args);
        } catch (err) {
          return `Error searching web: ${err.message}`;
        }
      },
    },

    crawl: {
      description: "Extract structured content from a URL",
      execute: async (args) => {
        try {
          return await handleCrawl(args);
        } catch (err) {
          return `Error crawling URL: ${err.message}`;
        }
      },
    },

    candles: {
      description: "Get OHLCV candlestick data for a ticker",
      execute: async (args) => {
        try {
          return await handleCandles(args);
        } catch (err) {
          return `Error fetching candles: ${err.message}`;
        }
      },
    },

    technicals: {
      description: "Get all technical indicators and signal summary for a ticker",
      execute: async (args) => {
        try {
          return await handleTechnicals(args);
        } catch (err) {
          return `Error fetching technicals: ${err.message}`;
        }
      },
    },

    "market-movers": {
      description: "Get top market gainers, losers, and most active stocks",
      execute: async () => {
        try {
          return await handleMarketMovers();
        } catch (err) {
          return `Error fetching market movers: ${err.message}`;
        }
      },
    },

    economy: {
      description: "Get economic indicators (GDP, CPI, unemployment, etc.)",
      execute: async (args) => {
        try {
          return await handleEconomy(args);
        } catch (err) {
          return `Error fetching economy data: ${err.message}`;
        }
      },
    },

    crypto: {
      description: "Get crypto token data or market overview",
      execute: async (args) => {
        try {
          return await handleCrypto(args);
        } catch (err) {
          return `Error fetching crypto data: ${err.message}`;
        }
      },
    },

    defi: {
      description: "Get DeFi TVL overview or protocol detail",
      execute: async (args) => {
        try {
          return await handleDefi(args);
        } catch (err) {
          return `Error fetching DeFi data: ${err.message}`;
        }
      },
    },

    screener: {
      description: "Screen stocks using natural language",
      execute: async (args) => {
        try {
          return await handleScreener(args);
        } catch (err) {
          return `Error running screener: ${err.message}`;
        }
      },
    },

    backtest: {
      description: "Backtest a news-driven trading strategy",
      execute: async (args) => {
        try {
          return await handleBacktest(args);
        } catch (err) {
          return `Error running backtest: ${err.message}`;
        }
      },
    },

    correlation: {
      description: "Get correlation matrix for multiple tickers",
      execute: async (args) => {
        try {
          return await handleCorrelation(args);
        } catch (err) {
          return `Error computing correlation: ${err.message}`;
        }
      },
    },

    price: {
      description: "Get live price and change for a ticker",
      execute: async (args) => {
        try {
          return await handlePrice(args);
        } catch (err) {
          return `Error fetching price: ${err.message}`;
        }
      },
    },

    social: {
      description: "Get social media sentiment for a ticker",
      execute: async (args) => {
        try {
          return await handleSocial(args);
        } catch (err) {
          return `Error fetching social sentiment: ${err.message}`;
        }
      },
    },

    "social-trending": {
      description: "See what tickers are trending on social media",
      execute: async () => {
        try {
          return await handleSocialTrending();
        } catch (err) {
          return `Error fetching social trending: ${err.message}`;
        }
      },
    },

    ipo: {
      description: "Get upcoming IPO calendar from SEC EDGAR",
      execute: async () => {
        try {
          return await handleIpo();
        } catch (err) {
          return `Error fetching IPO calendar: ${err.message}`;
        }
      },
    },

    alerts: {
      description: "Manage price and sentiment alerts",
      execute: async (args) => {
        try {
          return await handleAlerts(args);
        } catch (err) {
          return `Error managing alerts: ${err.message}`;
        }
      },
    },

    report: {
      description: "Generate an AI analysis report for any ticker",
      execute: async (args) => {
        try {
          return await handleReport(args);
        } catch (err) {
          return `Error generating report: ${err.message}`;
        }
      },
    },
  },
};
