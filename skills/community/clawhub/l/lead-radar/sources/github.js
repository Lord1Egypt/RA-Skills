const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

/**
 * GitHub Discussions scanner using GitHub's public search API.
 * No auth needed for public repos (rate limited to 10 req/min).
 * Docs: https://docs.github.com/en/rest/search
 */
async function scanGitHub(keywords) {
  const results = [];
  const seenIds = new Set();

  // Search discussions and issues where people ask for tools
  const query = keywords.slice(0, 2).join(' OR ');
  const oneDayAgo = new Date(Date.now() - 86400 * 1000).toISOString().split('T')[0];

  try {
    // GitHub search API — search issues/discussions
    const encoded = encodeURIComponent(`${query} is:open created:>=${oneDayAgo}`);
    const res = await fetch(
      `https://api.github.com/search/issues?q=${encoded}&sort=created&order=desc&per_page=25`,
      {
        headers: {
          'User-Agent': 'LeadRadar/1.0',
          Accept: 'application/vnd.github.v3+json',
        },
        timeout: 15000,
      }
    );

    if (!res.ok) {
      if (res.status === 403) {
        console.warn('GitHub API rate limited, skipping');
        return [];
      }
      console.error(`GitHub API failed: ${res.status}`);
      return [];
    }

    const data = await res.json();
    const items = data?.items || [];

    for (const item of items) {
      const id = `github_${item.id}`;
      if (seenIds.has(id)) continue;
      seenIds.add(id);

      results.push({
        id,
        title: item.title || '',
        body: (item.body || '').slice(0, 1000),
        url: item.html_url,
        source: 'GitHub',
        subreddit: null,
        score: item.reactions?.total_count || 0,
        created_utc: item.created_at
          ? Math.floor(new Date(item.created_at).getTime() / 1000)
          : Math.floor(Date.now() / 1000),
      });
    }
  } catch (err) {
    console.error('GitHub scan error:', err.message);
  }

  return results;
}

module.exports = { scanGitHub };
