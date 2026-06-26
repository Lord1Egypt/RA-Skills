const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

/**
 * Hashnode scanner using their public GraphQL API.
 * Endpoint: https://gql.hashnode.com
 * No API key needed.
 */
async function scanHashnode(keywords) {
  const query = keywords.slice(0, 2).join(' ');

  // Use the feed query (FeedFilter doesn't support 'query', so just get recent relevant posts)
  const graphqlQuery = {
    query: `
      query {
        feed(first: 25, filter: { type: RELEVANT }) {
          edges {
            node {
              id
              title
              brief
              url
              publishedAt
              reactionCount
            }
          }
        }
      }
    `,
  };

  try {
    const res = await fetch('https://gql.hashnode.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(graphqlQuery),
      timeout: 15000,
    });

    if (!res.ok) {
      const errText = await res.text().catch(() => '');
      console.error(`Hashnode API failed: ${res.status} — ${errText.slice(0, 200)}`);
      return fallbackSearch(keywords);
    }

    const data = await res.json();

    // Check for GraphQL errors
    if (data.errors) {
      console.error('Hashnode GraphQL errors:', JSON.stringify(data.errors[0]?.message || data.errors));
      return fallbackSearch(keywords);
    }

    const edges = data?.data?.feed?.edges || [];

    if (edges.length === 0) {
      console.log('Hashnode: no results from GraphQL, trying fallback');
      return fallbackSearch(keywords);
    }

    return edges
      .map((edge) => edge.node)
      .filter(Boolean)
      .map((post) => ({
        id: `hashnode_${post.id}`,
        title: post.title || '',
        body: (post.brief || '').slice(0, 1000),
        url: post.url || `https://hashnode.com/post/${post.id}`,
        source: 'Hashnode',
        subreddit: null,
        score: post.reactionCount || 0,
        created_utc: post.publishedAt
          ? Math.floor(new Date(post.publishedAt).getTime() / 1000)
          : Math.floor(Date.now() / 1000),
      }));
  } catch (err) {
    console.error('Hashnode scan error:', err.message);
    return fallbackSearch(keywords);
  }
}

/**
 * Fallback: use Hashnode's RSS-like tag feeds via their API.
 */
async function fallbackSearch(keywords) {
  const keyword = keywords[0] || 'freelance';
  const tag = keyword.toLowerCase().replace(/\s+/g, '-');

  const graphqlQuery = {
    query: `
      query TagPosts($tag: String!) {
        tag(slug: $tag) {
          posts(first: 20, sortBy: DATE_PUBLISHED_DESC) {
            edges {
              node {
                id
                title
                brief
                url
                publishedAt
                reactionCount
              }
            }
          }
        }
      }
    `,
    variables: { tag },
  };

  try {
    const res = await fetch('https://gql.hashnode.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(graphqlQuery),
      timeout: 15000,
    });

    if (!res.ok) return [];

    const data = await res.json();
    if (data.errors) return [];

    const edges = data?.data?.tag?.posts?.edges || [];

    return edges
      .map((edge) => edge.node)
      .filter(Boolean)
      .map((post) => ({
        id: `hashnode_${post.id}`,
        title: post.title || '',
        body: (post.brief || '').slice(0, 1000),
        url: post.url || `https://hashnode.com/post/${post.id}`,
        source: 'Hashnode',
        subreddit: null,
        score: post.reactionCount || 0,
        created_utc: post.publishedAt
          ? Math.floor(new Date(post.publishedAt).getTime() / 1000)
          : Math.floor(Date.now() / 1000),
      }));
  } catch (err) {
    console.error('Hashnode fallback error:', err.message);
    return [];
  }
}

module.exports = { scanHashnode };
