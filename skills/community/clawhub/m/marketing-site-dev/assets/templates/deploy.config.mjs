// 部署配置 · Deployment config
// Consumed by scripts/deploy.mjs and scripts/cdn-refresh.mjs.
// Edit the values for your project. The structure here is locked — the scripts
// import this default export and expect these exact keys.
export default {
  // ─── TOS bucket ─────────────────────────────────────────────────────────
  bucket: 'CHANGE-ME-bucket-name',         // must be globally unique on Volcengine TOS
  region: 'cn-beijing',                    // pick the region closest to your users
  endpoint: 'tos-cn-beijing.volces.com',   // must match region above

  // ─── Local build output ─────────────────────────────────────────────────
  distDir: 'dist',                         // Astro's default

  // ─── CDN accelerated domains (used by cdn:refresh) ──────────────────────
  cdnDomains: [
    'CHANGE-ME.example.com',
    'www.CHANGE-ME.example.com',
  ],

  // ─── Cache-Control rules: first matching prefix wins ────────────────────
  cacheRules: [
    // Astro fingerprinted chunks: long-cache, immutable
    { prefix: '_astro/', cacheControl: 'public, max-age=31536000, immutable' },
    // Brand assets (SVGs etc.) refreshed monthly is fine
    { prefix: 'brand/',  cacheControl: 'public, max-age=2592000' },
    // Favicon stable for a day
    { prefix: 'favicon.svg', cacheControl: 'public, max-age=86400' },
  ],
  // Fallback (HTML, sitemap, robots.txt): always revalidate
  defaultCacheControl: 'public, max-age=0, must-revalidate',
};
