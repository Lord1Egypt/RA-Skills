# Scraping — Extraction From Rendered Pages

A browser is the most expensive way to read a document. Use it only when rendering is genuinely required, and keep the run bounded to what the user asked for.

Contents: [Escalation Ladder](#escalation-ladder) · [Bounded Extraction](#bounded-extraction) · [Pagination](#pagination) · [Infinite Scroll](#infinite-scroll) · [Throttling And Concurrency](#throttling-and-concurrency) · [Reliability](#reliability) · [Boundaries](#boundaries)

## Escalation Ladder

Stop at the first rung that works:

1. **Documented API** — stable, paginated, rate-limited on purpose. Check the docs and the network tab before anything else.
2. **The page's own JSON endpoints** — most SPAs fetch their data from an internal API visible in the trace's Network tab; calling it directly with `page.request` or plain fetch skips rendering entirely.
3. **Embedded structured data** — `<script type="application/ld+json">`, `__NEXT_DATA__`, or a hydration payload in the HTML. A plain HTTP GET plus JSON parse.
4. **Static HTML parse** — server-rendered markup, no browser.
5. **Playwright** — only if the content exists solely after client-side rendering or user interaction.

Rung 2 is the one most often skipped: opening the trace of a single manual visit usually reveals a clean JSON endpoint, and the whole job collapses into a few HTTP calls.

## Bounded Extraction

```typescript
const page = await context.newPage();
await page.goto(url, { waitUntil: 'domcontentloaded' });

const cards = page.getByTestId('product-card');
await expect(cards.first()).toBeVisible();       // gate: proves the render happened

const products = await cards.evaluateAll(nodes => nodes.map(n => ({
  name: n.querySelector('.name')?.textContent?.trim() ?? null,
  price: n.querySelector('.price')?.textContent?.trim() ?? null,
  url: n.querySelector('a')?.href ?? null,
})));
```

`evaluateAll` and `$$eval` do not wait — without the visibility gate above, a slow render returns `[]` and the job reports success with zero rows. Every extraction needs a gate and a **non-empty assertion** before the data is trusted.

Scope to the collection, never the page: extracting `document.querySelectorAll('a')` on a listing page pulls the nav, the footer, and the cookie banner into the dataset.

## Pagination

```typescript
async function collect(page: Page, maxPages = 20) {
  const all = [];
  for (let i = 0; i < maxPages; i++) {
    all.push(...await extract(page));
    const next = page.getByRole('link', { name: 'Next' });
    if (!(await next.count()) || await next.isDisabled()) break;
    const firstBefore = await page.getByTestId('row').first().textContent();
    await next.click();
    await expect(page.getByTestId('row').first()).not.toHaveText(firstBefore ?? '');
    await sleep(delayMs);        // scrape_delay_ms, default 1000
  }
  return all;
}
```

- `maxPages` is not optional. An unbounded loop against a site that always renders a Next link runs until something dies.
- Wait for the **content to change**, not for the click to resolve — a click plus a fixed sleep duplicates page 1 whenever the server is slow.
- URL-parameter pagination (`?page=3`) is preferable when available: resumable, parallelizable, and unaffected by state.

## Infinite Scroll

```typescript
let previous = 0;
for (let i = 0; i < 50; i++) {
  const count = await page.getByTestId('item').count();
  if (count === previous) break;               // no growth = the end
  previous = count;
  await page.mouse.wheel(0, 5000);
  await page.waitForTimeout(delayMs);          // the one legitimate sleep: politeness, not synchronization
}
```

Virtualized lists recycle DOM nodes, so the count plateaus while more data loads — in that case collect on each pass and deduplicate by a stable id instead of reading everything at the end.

## Throttling And Concurrency

- One request per `scrape_delay_ms` (default 1000 ms) per host. Configure it; do not hardcode.
- Concurrency means **contexts, not browsers**: one browser, N contexts, N ≤ 4 against a single host. A browser per worker exhausts memory long before it speeds anything up.
- Honor `429` and `Retry-After` by backing off exponentially and stopping after two consecutive failures — hammering a rate limiter gets the IP blocked and the data lost.
- Block assets to cut bandwidth and time: `page.route('**/*.{png,jpg,woff2,mp4}', r => r.abort())`. Keep CSS if layout affects what renders.

## Reliability

```typescript
async function withRetry<T>(fn: () => Promise<T>, attempts = 3): Promise<T> {
  for (let i = 1; ; i++) {
    try { return await fn(); }
    catch (e) { if (i >= attempts) throw e; await sleep(1000 * 2 ** (i - 1)); }
  }
}
```

- Retry the page, not the whole run: a fresh context per attempt avoids inheriting a broken state.
- Checkpoint results to disk as you go. A three-hour job that holds everything in memory loses everything to one crash.
- Validate the shape before storing: null-heavy rows mean the selectors drifted, and a silent schema change is worse than a crash.
- Log the URL with every record. Debugging an extraction without provenance is guesswork.

## Boundaries

- Respect `robots.txt` and the site's terms; where they conflict with the request, say so and stop.
- Personal data pulls compliance obligations (GDPR, CCPA) with it — that decision belongs to the user, and `scrape` covers the framework.
- Not done here: fingerprint spoofing, CAPTCHA-solving services, rotating residential exits, or logging into someone else's account. A site that requires those to be read is a site that has said no.
- Stay inside the scope requested: one page means one page, not a crawl of the domain.
- Public data at low volume with a real delay is the posture this skill supports.
