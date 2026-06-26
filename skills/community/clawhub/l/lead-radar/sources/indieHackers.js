const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

async function scanIH(keywords) {
  const query = encodeURIComponent(keywords.slice(0, 2).join(' '));
  const jinaUrl = `https://r.jina.ai/https://www.indiehackers.com/search?q=${query}`;

  try {
    const res = await fetch(jinaUrl, {
      headers: {
        Accept: 'text/plain',
        'X-Return-Format': 'markdown',
      },
      timeout: 30000,
    });

    if (!res.ok) {
      console.error(`Indie Hackers/Jina fetch failed: ${res.status}`);
      return [];
    }

    const markdown = await res.text();
    return parsePosts(markdown);
  } catch (err) {
    console.error('Indie Hackers scan error:', err.message);
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
    // Look for IH post URLs
    const urlMatch = line.match(/https?:\/\/www\.indiehackers\.com\/post\/([a-z0-9-]+)/i);
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
  const slug = url.split('/post/')[1] || `ih_${index}`;
  return {
    id: `ih_${slug}`,
    title: title || body.slice(0, 120),
    body: body.slice(0, 1000),
    url,
    source: 'Indie Hackers',
    subreddit: null,
    score: 0,
    created_utc: Math.floor(Date.now() / 1000),
  };
}

module.exports = { scanIH };
