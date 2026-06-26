/* @meta
{
  "name": "gumtree/search",
  "description": "Search Gumtree UK classifieds (titles, prices, first image URL, locations, listing URLs) via public search HTML",
  "domain": "www.gumtree.com",
  "args": {
    "query": {"required": true, "description": "Search keywords (e.g. sofa, iPhone, VW Golf)"},
    "location": {"required": false, "description": "Location or postcode (default: United Kingdom)"},
    "page": {"required": false, "description": "Results page number (default: 1)"},
    "category": {"required": false, "description": "search_category (default: all; e.g. cars-vans-motorbikes)"}
  },
  "readOnly": true,
  "example": "bb-browser site gumtree/search \"sofa\""
}
*/

async (args) => {
  const absolutize = (u) => {
    if (!u || typeof u !== 'string') return '';
    const t = u.trim();
    if (t.startsWith('http')) return t;
    if (t.startsWith('//')) return 'https:' + t;
    if (t.startsWith('/')) return 'https://www.gumtree.com' + t;
    return t;
  };

  if (!args.query) return {error: 'Missing argument: query', hint: 'e.g. bb-browser site gumtree/search "sofa"'};

  const location = args.location || args.search_location || 'United Kingdom';
  const category = args.category || args.search_category || 'all';
  const page = Math.max(1, parseInt(String(args.page || '1'), 10) || 1);

  const params = new URLSearchParams({
    q: String(args.query),
    search_category: String(category),
    search_location: String(location),
  });
  if (page > 1) params.set('page', String(page));

  const url = 'https://www.gumtree.com/search?' + params.toString();
  const resp = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      Accept: 'text/html,application/xhtml+xml',
      'Accept-Language': 'en-GB,en;q=0.9',
    },
  });
  if (!resp.ok) return {error: 'HTTP ' + resp.status, url};

  const html = await resp.text();
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');

  const results = [];
  doc.querySelectorAll('article[data-q="search-result"]').forEach((article) => {
    const a = article.querySelector('a[data-q="search-result-anchor"]');
    if (!a) return;
    const path = a.getAttribute('href') || '';
    const listingUrl = path.startsWith('http') ? path : 'https://www.gumtree.com' + path;

    const img = a.querySelector('figure img[alt], img.lazyload[alt], img[alt]');
    const coverAlt = img ? (img.getAttribute('alt') || '').trim() : '';

    let snippet = '';
    a.querySelectorAll('p').forEach((p) => {
      const t = (p.textContent || '').trim().replace(/\s+/g, ' ');
      if (t.length > snippet.length) snippet = t;
    });

    const priceEl = a.querySelector('[data-q="tile-price"]');
    const price = priceEl ? priceEl.textContent.trim() : '';

    const locEl = a.querySelector('[data-q="tile-location"]');
    const loc = locEl ? locEl.textContent.trim() : '';

    const rawSrc = img ? (img.getAttribute('src') || img.getAttribute('data-src') || img.getAttribute('data-lazy') || '') : '';
    const firstImageUrl = absolutize(rawSrc);
    const displayTitle = (coverAlt || snippet.slice(0, 120) || listingUrl).toString();
    const safeAlt = displayTitle.replace(/[[\]]/g, '').slice(0, 100);
    const firstImageMarkdown = firstImageUrl
      ? '![' + safeAlt + '](' + firstImageUrl + ')'
      : undefined;

    results.push({
      title: displayTitle,
      price,
      location: loc,
      url: listingUrl,
      snippet: snippet || undefined,
      firstImageUrl: firstImageUrl || undefined,
      image: firstImageUrl || undefined,
      firstImageMarkdown: firstImageMarkdown || undefined,
    });
  });

  return {
    query: args.query,
    location,
    category,
    page,
    url,
    count: results.length,
    results,
  };
}
