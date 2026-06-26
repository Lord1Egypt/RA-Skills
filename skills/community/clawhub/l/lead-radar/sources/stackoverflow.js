const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

/**
 * Stack Overflow scanner using the public Stack Exchange API.
 * No API key needed for basic usage (300 requests/day quota).
 * Docs: https://api.stackexchange.com/docs
 */
async function scanStackOverflow(keywords) {
  const query = keywords.join(' OR ');
  const yesterdayTs = Math.floor(Date.now() / 1000) - 86400;

  const params = new URLSearchParams({
    order: 'desc',
    sort: 'creation',
    intitle: query,
    fromdate: String(yesterdayTs),
    site: 'stackoverflow',
    filter: '!nNPvSNdWme', // includes body excerpt
    pagesize: '50',
  });

  try {
    const res = await fetch(
      `https://api.stackexchange.com/2.3/search/advanced?${params}`,
      { headers: { 'Accept-Encoding': 'gzip' } }
    );

    if (!res.ok) {
      console.error(`Stack Overflow search failed: ${res.status}`);
      return [];
    }

    const data = await res.json();

    if (data.backoff) {
      console.warn(`Stack Overflow API backoff requested: ${data.backoff}s`);
    }

    return (data.items || []).map((item) => ({
      id: `so_${item.question_id}`,
      title: decodeHtml(item.title || ''),
      body: decodeHtml((item.body_markdown || item.excerpt || '')).slice(0, 1000),
      url: item.link || `https://stackoverflow.com/questions/${item.question_id}`,
      source: 'Stack Overflow',
      subreddit: null,
      score: item.score || 0,
      created_utc: item.creation_date,
    }));
  } catch (err) {
    console.error('Stack Overflow scan error:', err.message);
    return [];
  }
}

function decodeHtml(text) {
  return text
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

module.exports = { scanStackOverflow };
