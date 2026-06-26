const SITE_URL = process.argv[2] || process.env.SITE_URL;
const INDEXNOW_KEY = process.argv[3] || process.env.INDEXNOW_KEY;

if (!SITE_URL || !INDEXNOW_KEY) {
  console.error("Usage: node submit-indexnow.mjs <site_url> <indexnow_key>");
  console.error("  Or set SITE_URL and INDEXNOW_KEY environment variables.");
  process.exit(1);
}

async function getUrls() {
  const sitemapUrl = SITE_URL.replace(/\/$/, "") + "/sitemap.xml";
  const res = await fetch(sitemapUrl);
  if (!res.ok) {
    throw new Error(`Failed to fetch sitemap: ${res.status} ${sitemapUrl}`);
  }
  const xml = await res.text();
  const matches = xml.matchAll(/<loc>([^<]+)<\/loc>/g);
  return [...matches].map((m) => m[1]);
}

async function main() {
  const urls = await getUrls();
  console.log(`Found ${urls.length} URLs in sitemap`);

  const host = new URL(SITE_URL).host;
  const body = JSON.stringify({
    host,
    key: INDEXNOW_KEY,
    keyLocation: `${SITE_URL.replace(/\/$/, "")}/${INDEXNOW_KEY}.txt`,
    urlList: urls,
  });

  const res = await fetch("https://api.indexnow.org/IndexNow", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body,
  });

  console.log(`IndexNow: ${res.status} ${res.statusText}`);
  if (!res.ok) {
    const text = await res.text();
    console.error(text);
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
