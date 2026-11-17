/**
 * Search Unsplash for a post cover image.
 *
 * IMPORTANT for distribution: this script does NOT ship any API key.
 * Provide your own key via config.json ("unsplashAccessKey") or the
 * UNSPLASH_ACCESS_KEY environment variable. Without a key, posting without an
 * image is still fully supported.
 *
 * Usage:
 *   node search-image.js <search-query>            # keyword search (needs key)
 *   node search-image.js <unsplash-photo-page-url> # resolve a photo PAGE link
 *                                                  # to a direct image URL
 *
 * Photo-page links (https://unsplash.com/photos/<slug-or-id>) are web pages,
 * not images - embedding them directly breaks the image in a published post.
 * resolveUnsplashUrl() turns them into direct images.unsplash.com URLs:
 * - File-ID form (unsplash.com/photos/1507513319174-e556268bb244, the
 *   images.unsplash.com file name): direct URL is constructed locally and
 *   HEAD-verified - no key needed.
 * - Slug / short-id form (unsplash.com/photos/a-title-xYz123): resolved via
 *   the official API, which requires an Unsplash key - unsplash.com itself
 *   is behind a proof-of-work bot-shield, so keyless page scraping is
 *   impossible and the script asks for a direct image URL instead.
 */
// Config resolution mirrors api-client.js: user override in the state dir wins,
// then the bundled default. Kept local (not imported) so this module stays
// dependency-free for standalone use.
const { loadConfig: loadResolvedConfig } = require('./lib/api-client');

function loadConfig() {
  try { return loadResolvedConfig(); } catch { return {}; }
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

const STOPWORDS = new Set([
  'beijing', 'shanghai', 'night', 'morning', 'street', 'city', 'park', 'light',
  'day', 'view', 'time', 'people', 'man', 'woman', 'person', 'group', 'standing',
  'walking', 'near', 'during', 'with', 'and', 'the', 'a', 'an', 'of', 'in', 'on',
  'at', 'for', 'from', 'this', 'that', 'photo', 'image', 'picture', 'scenic',
]);

function extractKeywords(query) {
  return query.toLowerCase().split(/[^a-z]+/).filter(w => w.length > 2 && !STOPWORDS.has(w));
}

function scoreImage(result, keywords) {
  const alt = (result.alt_description || '').toLowerCase();
  let score = 0;
  for (const k of keywords) {
    if (alt.includes(k)) score++;
  }
  return score;
}

async function searchUnsplashOnce(query, key) {
  const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&per_page=10&orientation=landscape`;

  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const resp = await fetch(url, {
        headers: { Authorization: `Client-ID ${key}` },
        signal: AbortSignal.timeout(10000),
      });
      if (!resp.ok) {
        console.warn(`  ⚠️ Unsplash query failed: ${query} (${resp.status})`);
        return [];
      }
      const data = await resp.json();
      const keywords = extractKeywords(query);
      // Keep every hit - the API already ranks by relevance. Local keyword
      // scoring only RE-RANKS (alt text is optional on Unsplash and often
      // missing, so filtering on it used to discard perfectly good results
      // for generic queries like "autumn park").
      const results = data.results
        .map(r => ({
          url: r.urls && r.urls.regular,
          alt: r.alt_description || query,
          source: 'unsplash',
          score: scoreImage(r, keywords),
        }))
        .filter(r => r.url)
        .sort((a, b) => b.score - a.score);
      return results.slice(0, 10);
    } catch (e) {
      console.warn(`  ⚠️ Attempt ${attempt + 1} failed: ${e.message}`);
      if (attempt === 0) await sleep(2000);
    }
  }
  return [];
}

async function searchImage(query, options = {}) {
  const { count = 3 } = options;
  const key = loadConfig().unsplashAccessKey || process.env.UNSPLASH_ACCESS_KEY;
  if (!key) {
    console.warn('  ⚠️ No Unsplash key configured (config.json "unsplashAccessKey" or UNSPLASH_ACCESS_KEY env).');
    console.warn('     Continuing without an image, or ask the user for an image URL / their own key.');
    return [];
  }
  const results = await searchUnsplashOnce(query, key);
  if (results.length > 0) {
    console.log(`  ✅ Found ${results.length} images for "${query}"`);
    return results.slice(0, count);
  }
  console.log(`  ⚠️ No images found for "${query}"`);
  return [];
}

/**
 * HEAD-check an image URL. Returns { ok, status, reason } so callers can
 * tell a 404 apart from a timeout or network failure.
 */
async function checkImageUrl(url) {
  try {
    const resp = await fetch(url, { method: 'HEAD', signal: AbortSignal.timeout(10000) });
    if (resp.status === 200) return { ok: true, status: 200, reason: 'ok' };
    return { ok: false, status: resp.status, reason: `HTTP ${resp.status}` };
  } catch (err) {
    const reason = err && (err.name === 'TimeoutError' || err.name === 'AbortError') ? 'timeout' : 'network error';
    return { ok: false, status: null, reason };
  }
}

/** Boolean convenience wrapper around checkImageUrl(). */
async function validateImageUrl(url) {
  return (await checkImageUrl(url)).ok;
}

const UNSPLASH_PHOTO_PAGE = /^https?:\/\/unsplash\.com\/photos\/([A-Za-z0-9_-]+)\/?(?:[?#].*)?$/i;
const UNSPLASH_DIRECT_IMAGE = /^https?:\/\/images\.unsplash\.com\//i;

/** True when the string is an Unsplash photo PAGE link (not a direct image URL). */
function isUnsplashPhotoUrl(url) {
  return typeof url === 'string' && UNSPLASH_PHOTO_PAGE.test(url.trim());
}

/**
 * Resolve an Unsplash link to a direct image URL. Accepts both photo-page
 * links (unsplash.com/photos/...) and direct image URLs (validated as-is).
 * Returns { url, alt } - the direct images.unsplash.com URL plus an alt text.
 */
async function resolveUnsplashUrl(url) {
  url = url.trim();

  if (UNSPLASH_DIRECT_IMAGE.test(url)) {
    const check = await checkImageUrl(url);
    if (!check.ok) throw new Error(`Unsplash image URL rejected (${check.reason}): ${url}`);
    return { url, alt: '' };
  }

  const m = url.match(UNSPLASH_PHOTO_PAGE);
  if (!m) throw new Error(`Not an Unsplash photo link: ${url}`);
  const seg = m[1];

  // File-ID form ("1507513319174-e556268bb244" or "photo-1507513319174-..."):
  // this is the images.unsplash.com FILE NAME, not a photo-page slug - the
  // API has no such id. The direct image URL can be constructed locally,
  // no key needed.
  const fileId = seg.replace(/^photo-/i, '');
  if (/^\d{9,14}-[a-f0-9]{9,16}$/i.test(fileId)) {
    const direct = `https://images.unsplash.com/photo-${fileId}`;
    const check = await checkImageUrl(direct);
    if (check.ok) return { url: direct, alt: '' };
    throw new Error(`Unsplash image no longer exists (${check.reason}): ${direct}`);
  }

  // Slug form "a-photo-title-aB3xYz9" -> the id is the last dash token;
  // bare-id form "aB3xYz9" is used as-is. If the extracted id 404s, retry
  // with the full segment (some ids contain dashes).
  const idCandidates = seg.includes('-') ? [seg.split('-').pop(), seg] : [seg];

  const key = loadConfig().unsplashAccessKey || process.env.UNSPLASH_ACCESS_KEY;
  if (!key) {
    throw new Error('Resolving an Unsplash photo-page link requires an Unsplash API key (unsplash.com blocks keyless server-side access). Configure "unsplashAccessKey" in config.json, or give a direct images.unsplash.com URL.');
  }

  for (const id of idCandidates) {
    try {
      const resp = await fetch(`https://api.unsplash.com/photos/${encodeURIComponent(id)}`, {
        headers: { Authorization: `Client-ID ${key}` },
        signal: AbortSignal.timeout(10000),
      });
      if (resp.status === 404) continue;
      if (!resp.ok) throw new Error(`Unsplash API HTTP ${resp.status}`);
      const data = await resp.json();
      if (data.urls && data.urls.regular) {
        return { url: data.urls.regular, alt: data.alt_description || '' };
      }
    } catch (err) {
      if (err.message && err.message.includes('Unsplash API')) throw err;
      // network/timeout on this id - try the next candidate
    }
  }
  throw new Error('Unsplash API returned no image for this photo link. Check the link, or give a direct image URL instead.');
}

async function main() {
  const query = process.argv[2];
  if (!query) {
    console.error('Usage: node search-image.js <search-query | unsplash-photo-page-url>');
    process.exit(1);
  }

  if (isUnsplashPhotoUrl(query)) {
    console.log(`Resolving Unsplash photo link: ${query}\n`);
    try {
      const { url, alt } = await resolveUnsplashUrl(query);
      console.log('✅ Direct image URL:');
      console.log(`   ${url}`);
      if (alt) console.log(`   Alt: ${alt}`);
      console.log('\nUse this URL directly (compose.js --image <url> resolves photo links automatically).');
      return;
    } catch (err) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 1;
      return;
    }
  }

  console.log(`Searching images for: "${query}"\n`);
  const images = await searchImage(query, { count: 5 });

  if (images.length === 0) {
    console.log('\nNo images found. Provide an image URL directly, or publish without an image.');
    process.exitCode = 1;
    return;
  }

  console.log('\nResults:');
  images.forEach((img, i) => {
    console.log(`${i + 1}. ${img.url}`);
    console.log(`   Alt: ${img.alt}`);
    console.log(`   Score: ${img.score}`);
    console.log('');
  });
}

if (require.main === module) {
  main().catch(err => {
    console.error('Error:', err.message);
    process.exitCode = 1;
  });
}

module.exports = { searchImage, checkImageUrl, validateImageUrl, isUnsplashPhotoUrl, resolveUnsplashUrl };
