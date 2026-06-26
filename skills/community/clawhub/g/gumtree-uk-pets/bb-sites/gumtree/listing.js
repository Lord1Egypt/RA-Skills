/* @meta
{
  "name": "gumtree/listing",
  "description": "Fetch a Gumtree UK listing detail page: full description, price, location, first image and all image URLs (JSON-LD + fallbacks)",
  "domain": "www.gumtree.com",
  "args": {
    "url": {"required": true, "description": "Full listing URL or path, e.g. /p/.../123456 or https://www.gumtree.com/p/..."}
  },
  "readOnly": true,
  "example": "bb-browser site gumtree/listing /p/coffee-table/item/1512630746"
}
*/

async (args) => {
  const absolutize = (u) => {
    if (!u || typeof u !== 'string') return '';
    const t = u.trim();
    if (t.startsWith('http')) return t;
    if (t.startsWith('//')) return 'https:' + t;
    if (t.startsWith('/')) return 'https://www.gumtree.com' + t;
    return 'https://www.gumtree.com/' + t;
  };

  const productFromJsonLd = (d) => {
    if (!d || typeof d !== 'object') return null;
    if (d['@type'] === 'Product' && d.name) return d;
    if (Array.isArray(d)) {
      for (const n of d) {
        const p = productFromJsonLd(n);
        if (p) return p;
      }
    }
    if (Array.isArray(d['@graph'])) {
      for (const n of d['@graph']) {
        if (n && n['@type'] === 'Product' && n.name) return n;
      }
    }
    if (d['@graph'] && d['@graph']['@type'] === 'Product') return d['@graph'];
    return null;
  };

  const normalizeImages = (imageField) => {
    if (!imageField) return [];
    if (typeof imageField === 'string') return [absolutize(imageField)];
    if (Array.isArray(imageField)) return imageField.map(absolutize).filter(Boolean);
    if (imageField.url) return [absolutize(imageField.url)];
    return [];
  };

  const parseMetaProperty = (html, prop) => {
    const m = html.match(new RegExp('<meta\\s+property="' + prop + '"\\s+content="([^"]*)"', 'i'));
    if (!m) return '';
    return m[1]
      .replace(/&amp;/g, '&')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>');
  };

  if (!args.url) return { error: 'Missing argument: url', hint: 'e.g. bb-browser site gumtree/listing "https://www.gumtree.com/p/.../ID"' };

  let path = String(args.url).trim();
  if (!path.startsWith('http')) {
    if (!path.startsWith('/')) path = '/' + path;
    path = 'https://www.gumtree.com' + path;
  }

  const resp = await fetch(path, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      Accept: 'text/html,application/xhtml+xml',
      'Accept-Language': 'en-GB,en;q=0.9',
    },
  });
  if (!resp.ok) return { error: 'HTTP ' + resp.status, url: path };

  const finalUrl = resp.url || path;
  const html = await resp.text();

  if (/\/for-sale\//.test(finalUrl) && (html.includes('adRemoved') || finalUrl.includes('adRemoved='))) {
    return { error: 'Listing not available (removed or category redirect)', url: finalUrl, hint: 'Try a fresh /p/... URL from gumtree/search' };
  }

  let title = '';
  let description = '';
  let firstImage = '';
  let images = [];
  let price = '';
  let priceCurrency = 'GBP';
  let location = '';

  const doc = new DOMParser().parseFromString(html, 'text/html');
  const scripts = doc.querySelectorAll('script[type="application/ld+json"]');
  for (const s of scripts) {
    const raw = (s.textContent || '').trim();
    if (!raw) continue;
    try {
      const d = JSON.parse(raw);
      const p = productFromJsonLd(d);
      if (p) {
        title = (p.name || '').trim();
        description = (p.description || '').trim().replace(/\s+/g, ' ');
        images = normalizeImages(p.image);
        firstImage = images[0] || '';
        const o = p.offers;
        if (o) {
          if (typeof o.price === 'string' || typeof o.price === 'number') {
            price = o.price === 0 || o.price === '0' ? 'FREE' : String(o.price);
          }
          if (o.priceCurrency) priceCurrency = String(o.priceCurrency);
          const av = o.availableAtOrFrom;
          if (av && typeof av === 'string') location = av;
        }
        break;
      }
    } catch (e) {
      /* try next */
    }
  }

  if (!description) {
    const ogd = doc.querySelector('meta[property="og:description"]');
    if (ogd) description = (ogd.getAttribute('content') || '').trim();
  }
  if (!description) description = parseMetaProperty(html, 'og:description');

  if (!title) {
    const ogp = doc.querySelector('meta[property="og:title"]');
    if (ogp) title = (ogp.getAttribute('content') || '').split('|')[0].trim();
  }

  if (images.length === 0) {
    const ogi = doc.querySelector('meta[property="og:image"]');
    if (ogi) {
      firstImage = absolutize(ogi.getAttribute('content') || '');
      if (firstImage) images = [firstImage];
    }
  } else {
    firstImage = images[0];
  }

  const firstImageMarkdown = firstImage && title
    ? '![' + title.replace(/[[\]]/g, '').slice(0, 80) + '](' + firstImage + ')'
    : (firstImage ? '![](' + firstImage + ')' : undefined);

  return {
    url: finalUrl,
    title: title || undefined,
    description: description || undefined,
    price: price || undefined,
    priceCurrency,
    location: location || undefined,
    firstImageUrl: firstImage || undefined,
    imageUrls: images,
    countImages: images.length,
    firstImageMarkdown: firstImageMarkdown || undefined,
  };
}
