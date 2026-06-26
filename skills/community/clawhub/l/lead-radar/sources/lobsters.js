const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

/**
 * Lobsters scanner — computing-focused link aggregation.
 * No search API exists. We fetch /newest.json and /hottest.json
 * then filter locally by keywords.
 */
async function scanLobsters(keywords) {
  const results = [];
  const seenIds = new Set();
  const oneDayAgo = Date.now() - 86400 * 1000;
  const lowerKeywords = keywords.map((k) => k.toLowerCase().split(' ')).flat();

  // Fetch both newest and hottest for wider coverage
  const pages = ['newest', 'hottest'];

  for (const page of pages) {
    try {
      const res = await fetch(`https://lobste.rs/${page}.json`, {
        headers: {
          'User-Agent': 'LeadRadar/1.0',
          Accept: 'application/json',
        },
        timeout: 15000,
      });

      if (!res.ok) {
        console.error(`Lobsters ${page} failed: ${res.status}`);
        continue;
      }

      const stories = await res.json();

      for (const story of stories) {
        const createdAt = new Date(story.created_at).getTime();
        if (createdAt < oneDayAgo) continue;

        const id = `lobsters_${story.short_id}`;
        if (seenIds.has(id)) continue;

        // Check if story matches any keyword
        const text = `${story.title || ''} ${story.description || ''} ${(story.tags || []).join(' ')}`.toLowerCase();
        if (!lowerKeywords.some((kw) => text.includes(kw))) continue;

        seenIds.add(id);
        results.push({
          id,
          title: story.title || '',
          body: (story.description || '').slice(0, 1000),
          url: story.comments_url || story.url || `https://lobste.rs/s/${story.short_id}`,
          source: 'Lobsters',
          subreddit: (story.tags || []).join(', ') || null,
          score: story.score || 0,
          created_utc: Math.floor(createdAt / 1000),
        });
      }
    } catch (err) {
      console.error(`Lobsters ${page} error:`, err.message);
    }

    await new Promise((r) => setTimeout(r, 500));
  }

  return results;
}

module.exports = { scanLobsters };
