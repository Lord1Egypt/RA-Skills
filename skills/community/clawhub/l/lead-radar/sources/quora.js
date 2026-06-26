const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

/**
 * Quora scanner using Jina.ai reader to scrape search results.
 * No API key needed.
 */
async function scanQuora(keywords) {
  const query = encodeURIComponent(keywords.slice(0, 2).join(' '));
  const jinaUrl = `https://r.jina.ai/https://www.quora.com/search?q=${query}`;

  try {
    const res = await fetch(jinaUrl, {
      headers: {
        Accept: 'text/plain',
        'X-Return-Format': 'markdown',
      },
      timeout: 30000,
    });

    if (!res.ok) {
      console.error(`Quora/Jina fetch failed: ${res.status}`);
      return [];
    }

    const markdown = await res.text();
    return parsePosts(markdown);
  } catch (err) {
    console.error('Quora scan error:', err.message);
    return [];
  }
}

function parsePosts(markdown) {
  const posts = [];
  const lines = markdown.split('\n');

  let currentTitle = '';
  let currentUrl = '';
  let currentBody = '';
  let postCount = 0;

  for (const line of lines) {
    // Look for Quora question URLs
    const urlMatch = line.match(/https?:\/\/www\.quora\.com\/([\w-]+\/answer\/[\w-]+|[\w-]+)/i);
    if (urlMatch) {
      // Save previous post
      if (currentUrl && (currentTitle || currentBody.trim())) {
        posts.push(makePost(currentUrl, currentTitle, currentBody.trim(), postCount));
        postCount++;
      }
      currentUrl = urlMatch[0];
      currentTitle = '';
      currentBody = '';
      continue;
    }

    // Headings become titles
    const headingMatch = line.match(/^#{1,3}\s+(.+)/);
    if (headingMatch && !currentTitle) {
      currentTitle = headingMatch[1].trim();
      continue;
    }

    // Accumulate body text
    const cleaned = line.replace(/[#*_\[\]]/g, '').trim();
    if (cleaned && cleaned.length > 10) {
      currentBody += (currentBody ? ' ' : '') + cleaned;
    }
  }

  // Don't forget the last post
  if (currentUrl && (currentTitle || currentBody.trim())) {
    posts.push(makePost(currentUrl, currentTitle, currentBody.trim(), postCount));
  }

  return posts;
}

function makePost(url, title, body, index) {
  const slug = url.split('quora.com/')[1] || `quora_${index}`;
  return {
    id: `quora_${slug.slice(0, 80)}`,
    title: title || body.slice(0, 120),
    body: body.slice(0, 1000),
    url,
    source: 'Quora',
    subreddit: null,
    score: 0,
    created_utc: Math.floor(Date.now() / 1000),
  };
}

module.exports = { scanQuora };
