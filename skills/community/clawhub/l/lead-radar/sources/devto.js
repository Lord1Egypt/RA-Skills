const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

/**
 * Dev.to scanner using their free public API.
 * No API key needed.
 * Docs: https://developers.forem.com/api/v1
 */
async function scanDevTo(keywords) {
  const results = [];
  const seenIds = new Set();

  // Search with each keyword separately for better coverage
  const searchTerms = keywords.slice(0, 3);

  for (const term of searchTerms) {
    try {
      const encoded = encodeURIComponent(term);
      const res = await fetch(
        `https://dev.to/api/articles?per_page=25&top=1&search=${encoded}`,
        {
          headers: {
            'User-Agent': 'LeadRadar/1.0',
            Accept: 'application/json',
          },
          timeout: 15000,
        }
      );

      if (!res.ok) {
        console.error(`Dev.to API failed for "${term}": ${res.status}`);
        continue;
      }

      const articles = await res.json();

      // Filter to last 24h
      const oneDayAgo = Date.now() - 86400 * 1000;

      for (const article of articles) {
        const publishedAt = new Date(article.published_at || article.created_at).getTime();
        if (publishedAt < oneDayAgo) continue;

        const id = `devto_${article.id}`;
        if (seenIds.has(id)) continue;
        seenIds.add(id);

        results.push({
          id,
          title: article.title || '',
          body: (article.description || '').slice(0, 1000),
          url: article.url || `https://dev.to/${article.path}`,
          source: 'Dev.to',
          subreddit: null,
          score: article.public_reactions_count || 0,
          created_utc: Math.floor(publishedAt / 1000),
        });
      }
    } catch (err) {
      console.error(`Dev.to scan error for "${term}":`, err.message);
    }

    // Small delay between requests
    await new Promise((r) => setTimeout(r, 500));
  }

  return results;
}

module.exports = { scanDevTo };
