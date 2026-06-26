const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

/**
 * Reddit scanner with automatic A → B → C fallback:
 *
 *   A) old.reddit.com .json — fastest, best results, but can get IP-blocked (403)
 *   B) Pullpush.io API — Reddit archive, free, no auth, reliable
 *   C) Reddit RSS feeds — always works, but no search (local keyword filtering)
 *
 * The scanner tries A first. If A returns 403, it switches to B for all
 * remaining requests. If B also fails, it falls back to C.
 */

const TARGET_SUBREDDITS = [
  'entrepreneur',
  'startups',
  'SaaS',
  'smallbusiness',
  'freelance',
  'microsaas',
  'sideproject',
  'forhire',
  'webdev',
  'marketing',
];

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';
const ONE_DAY_SECS = 86400;

// ─── Strategy A: old.reddit.com .json ──────────────────────────────

async function strategyA(query, subreddit = null) {
  const oneDayAgo = Math.floor(Date.now() / 1000) - ONE_DAY_SECS;

  const params = new URLSearchParams({
    q: query,
    sort: 'new',
    t: 'day',
    limit: '25',
    restrict_sr: subreddit ? '1' : '0',
  });

  const base = subreddit
    ? `https://old.reddit.com/r/${subreddit}/search.json`
    : 'https://old.reddit.com/search.json';

  const res = await fetch(`${base}?${params}`, {
    headers: { 'User-Agent': USER_AGENT },
    timeout: 15000,
  });

  if (res.status === 403 || res.status === 429) return null; // Signal: blocked
  if (!res.ok) return null;

  const data = await res.json();
  return (data?.data?.children || [])
    .map((child) => child.data)
    .filter((post) => post.created_utc > oneDayAgo)
    .map((post) => ({
      id: `reddit_${post.id}`,
      title: post.title || '',
      body: (post.selftext || '').slice(0, 1000),
      url: `https://reddit.com${post.permalink}`,
      source: 'Reddit',
      subreddit: post.subreddit,
      score: post.score,
      created_utc: post.created_utc,
    }));
}

// ─── Strategy B: Pullpush.io (Pushshift successor) ────────────────

async function strategyB(query, subreddits = []) {
  const results = [];
  const seenIds = new Set();

  // Pullpush uses epoch timestamps for after/before
  const oneDayAgoEpoch = Math.floor(Date.now() / 1000) - ONE_DAY_SECS;
  const params = new URLSearchParams({
    q: query,
    size: '100',
    sort: 'desc',
    sort_type: 'created_utc',
    after: String(oneDayAgoEpoch),
  });

  // If subreddits provided, add them as filter
  if (subreddits.length > 0) {
    params.set('subreddit', subreddits.join(','));
  }

  try {
    const res = await fetch(
      `https://api.pullpush.io/reddit/search/submission/?${params}`,
      {
        headers: { 'User-Agent': USER_AGENT },
        timeout: 20000,
      }
    );

    if (!res.ok) {
      console.error(`[Reddit/Pullpush] API failed: ${res.status}`);
      return null; // Signal: try next strategy
    }

    const data = await res.json();
    const posts = data?.data || [];

    for (const post of posts) {
      const id = `reddit_${post.id}`;
      if (seenIds.has(id)) continue;
      seenIds.add(id);

      results.push({
        id,
        title: post.title || '',
        body: (post.selftext || '').slice(0, 1000),
        url: post.permalink
          ? `https://reddit.com${post.permalink}`
          : `https://reddit.com/r/${post.subreddit}/comments/${post.id}`,
        source: 'Reddit',
        subreddit: post.subreddit || '',
        score: post.score || 0,
        created_utc: post.created_utc || Math.floor(Date.now() / 1000),
      });
    }
  } catch (err) {
    console.error(`[Reddit/Pullpush] Error:`, err.message);
    return null; // Signal: try next strategy
  }

  return results;
}

// ─── Strategy C: Reddit RSS feeds (always works) ──────────────────

async function strategyC(keywords, subreddits) {
  const results = [];
  const seenIds = new Set();
  const oneDayAgo = Date.now() - ONE_DAY_SECS * 1000;
  const lowerKeywords = keywords.map((k) => k.toLowerCase().split(' ')).flat()
    .filter((w) => w.length > 2);

  for (const sub of subreddits) {
    try {
      const res = await fetch(`https://www.reddit.com/r/${sub}/new.rss?limit=50`, {
        headers: { 'User-Agent': USER_AGENT },
        timeout: 15000,
      });

      if (!res.ok) {
        console.error(`[Reddit/RSS] r/${sub} failed: ${res.status}`);
        continue;
      }

      const xml = await res.text();
      const entries = xml.split('<entry>').slice(1);

      for (const entry of entries) {
        const titleMatch = entry.match(/<title[^>]*>([\s\S]*?)<\/title>/);
        const linkMatch = entry.match(/<link[^>]*href="([^"]*)"[^>]*\/>/);
        const contentMatch = entry.match(/<content[^>]*>([\s\S]*?)<\/content>/);
        const updatedMatch = entry.match(/<updated>([\s\S]*?)<\/updated>/);

        if (!titleMatch || !linkMatch) continue;

        const title = titleMatch[1]
          .replace(/&amp;/g, '&').replace(/&lt;/g, '<')
          .replace(/&gt;/g, '>').replace(/&#39;/g, "'").replace(/&quot;/g, '"');
        const url = linkMatch[1];
        const content = contentMatch
          ? contentMatch[1].replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
          : '';
        const updated = updatedMatch ? new Date(updatedMatch[1]).getTime() : 0;

        if (updated && updated < oneDayAgo) continue;

        // Keyword relevance check
        const text = `${title} ${content}`.toLowerCase();
        if (!lowerKeywords.some((kw) => text.includes(kw))) continue;

        const idMatch = url.match(/\/comments\/(\w+)\//);
        const postId = idMatch ? idMatch[1] : `rss_${results.length}`;
        const id = `reddit_${postId}`;

        if (seenIds.has(id)) continue;
        seenIds.add(id);

        results.push({
          id,
          title,
          body: content.slice(0, 1000),
          url,
          source: 'Reddit',
          subreddit: sub,
          score: 0,
          created_utc: updated ? Math.floor(updated / 1000) : Math.floor(Date.now() / 1000),
        });
      }
    } catch (err) {
      console.error(`[Reddit/RSS] r/${sub} error:`, err.message);
    }

    await new Promise((r) => setTimeout(r, 2000));
  }

  return results;
}

// ─── Main scanner: A → B → C ──────────────────────────────────────

async function scanReddit(keywords) {
  // Build broad query from keywords
  const stopWords = new Set(['i', 'a', 'an', 'the', 'for', 'to', 'and', 'or', 'who', 'that', 'is', 'are', 'my', 'sell', 'with', 'of', 'in', 'on']);
  const words = new Set();
  for (const kw of keywords) {
    for (const w of kw.split(/\s+/)) {
      const clean = w.toLowerCase().replace(/[^\w]/g, '');
      if (clean.length > 2 && !stopWords.has(clean)) words.add(clean);
    }
  }
  const query = [...words].slice(0, 6).join(' OR ');
  console.log(`[Reddit] Search query: ${query}`);

  // ── Strategy A: old.reddit.com .json ──
  console.log('[Reddit] Trying Strategy A (old.reddit.com .json)...');
  const testResult = await strategyA(query).catch(() => null);

  if (testResult !== null) {
    // A works! Use it for all subreddits
    console.log(`[Reddit/A] Global search returned ${testResult.length} posts`);
    const results = [...testResult];
    const seenIds = new Set(results.map((p) => p.id));

    for (const sub of TARGET_SUBREDDITS) {
      try {
        const subResults = await strategyA(query, sub);
        if (subResults === null) {
          console.warn(`[Reddit/A] Blocked mid-scan at r/${sub}, stopping A`);
          break;
        }
        for (const post of subResults) {
          if (!seenIds.has(post.id)) {
            seenIds.add(post.id);
            results.push(post);
          }
        }
      } catch (err) {
        console.error(`[Reddit/A] r/${sub} error:`, err.message);
      }
      await new Promise((r) => setTimeout(r, 3000));
    }

    if (results.length > 0) {
      console.log(`[Reddit] Strategy A: ${results.length} posts`);
      return results;
    }
  }

  // ── Strategy B: Pullpush.io ──
  console.log('[Reddit] Strategy A blocked. Trying Strategy B (Pullpush.io)...');
  const pullpushResults = await strategyB(query, TARGET_SUBREDDITS).catch(() => null);

  if (pullpushResults !== null && pullpushResults.length >= 0) {
    console.log(`[Reddit] Strategy B: ${pullpushResults.length} posts`);
    return pullpushResults;
  }

  // ── Strategy C: RSS feeds ──
  console.log('[Reddit] Strategy B failed. Trying Strategy C (RSS feeds)...');
  const rssResults = await strategyC(keywords, TARGET_SUBREDDITS).catch(() => []);
  console.log(`[Reddit] Strategy C: ${rssResults.length} posts`);
  return rssResults;
}

module.exports = { scanReddit };
