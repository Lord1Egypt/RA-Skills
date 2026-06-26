const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

async function scanHN(keywords) {
  const query = keywords.join(' ');
  const yesterdayTs = Math.floor(Date.now() / 1000) - 86400;

  const params = new URLSearchParams({
    query,
    tags: '(ask_hn,show_hn,story)',
    numericFilters: `created_at_i>${yesterdayTs}`,
    hitsPerPage: '50',
  });

  try {
    const res = await fetch(`https://hn.algolia.com/api/v1/search?${params}`);

    if (!res.ok) {
      console.error(`HN search failed: ${res.status}`);
      return [];
    }

    const data = await res.json();

    return (data.hits || []).map((hit) => ({
      id: `hn_${hit.objectID}`,
      title: hit.title || '',
      body: (hit.story_text || hit.comment_text || '').slice(0, 1000),
      url: hit.url || `https://news.ycombinator.com/item?id=${hit.objectID}`,
      source: 'Hacker News',
      subreddit: null,
      score: hit.points || 0,
      created_utc: hit.created_at_i,
    }));
  } catch (err) {
    console.error('HN scan error:', err.message);
    return [];
  }
}

module.exports = { scanHN };
