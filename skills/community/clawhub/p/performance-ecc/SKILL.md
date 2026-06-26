---
name: performance
description: Optimize web performance and LLM API costs. Covers loading speed, runtime efficiency, resource optimization, and cost-aware LLM pipelines with model routing, budget tracking, and prompt caching.
license: MIT
metadata:
  author: web-quality-skills
  version: "2.0"
  origin: "ECC + web-quality-skills"
---

# Performance Optimization

Deep performance optimization covering web performance (Lighthouse, Core Web Vitals) and LLM API cost optimization. Focuses on loading speed, runtime efficiency, resource optimization, and intelligent model routing.

## How it works

1. Identify performance bottlenecks in code, assets, and API usage
2. Prioritize by impact on Core Web Vitals and cost
3. Provide specific optimizations with code examples
4. Measure improvement with before/after metrics

## Performance budget

| Resource | Budget | Rationale |
|----------|--------|-----------|
| Total page weight | < 1.5 MB | 3G loads in ~4s |
| JavaScript (compressed) | < 300 KB | Parsing + execution time |
| CSS (compressed) | < 100 KB | Render blocking |
| Images (above-fold) | < 500 KB | LCP impact |
| Fonts | < 100 KB | FOIT/FOUT prevention |
| Third-party | < 200 KB | Uncontrolled latency |

## Critical rendering path

### Server response
* **TTFB < 800ms.** Time to First Byte should be fast. Use CDN, caching, and efficient backends.
* **Enable compression.** Gzip or Brotli for text assets. Brotli preferred (15-20% smaller).
* **HTTP/2 or HTTP/3.** Multiplexing reduces connection overhead.
* **Edge caching.** Cache HTML at CDN edge when possible.

### Resource loading

**Preconnect to required origins:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com" crossorigin>
```

**Preload critical resources:**
```html
<!-- LCP image -->
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">

<!-- Critical font -->
<link rel="preload" href="/font.woff2" as="font" type="font/woff2" crossorigin>
```

**Defer non-critical CSS:**
```html
<!-- Critical CSS inlined -->
<style>/* Above-fold styles */</style>

<!-- Non-critical CSS -->
<link rel="preload" href="/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/styles.css"></noscript>
```

### JavaScript optimization

**Defer non-essential scripts:**
```html
<!-- Parser-blocking (avoid) -->
<script src="/critical.js"></script>

<!-- Deferred (preferred) -->
<script defer src="/app.js"></script>

<!-- Async (for independent scripts) -->
<script async src="/analytics.js"></script>

<!-- Module (deferred by default) -->
<script type="module" src="/app.mjs"></script>
```

**Code splitting patterns:**
```javascript
// Route-based splitting
const Dashboard = lazy(() => import('./Dashboard'));

// Component-based splitting
const HeavyChart = lazy(() => import('./HeavyChart'));

// Feature-based splitting
if (user.isPremium) {
  const PremiumFeatures = await import('./PremiumFeatures');
}
```

**Tree shaking best practices:**
```javascript
// ❌ Imports entire library
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Imports only what's needed
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

## Image optimization

### Format selection
| Format | Use case | Browser support |
|--------|----------|-----------------|
| AVIF | Photos, best compression | 92%+ |
| WebP | Photos, good fallback | 97%+ |
| PNG | Graphics with transparency | Universal |
| SVG | Icons, logos, illustrations | Universal |

### Responsive images
```html
<picture>
  <!-- AVIF for modern browsers -->
  <source 
    type="image/avif"
    srcset="hero-400.avif 400w,
            hero-800.avif 800w,
            hero-1200.avif 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">
  
  <!-- WebP fallback -->
  <source 
    type="image/webp"
    srcset="hero-400.webp 400w,
            hero-800.webp 800w,
            hero-1200.webp 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">
  
  <!-- JPEG fallback -->
  <img 
    src="hero-800.jpg"
    srcset="hero-400.jpg 400w,
            hero-800.jpg 800w,
            hero-1200.jpg 1200w"
    sizes="(max-width: 600px) 100vw, 50vw"
    width="1200" 
    height="600"
    alt="Hero image"
    loading="lazy"
    decoding="async">
</picture>
```

### LCP image priority
```html
<!-- Above-fold LCP image: eager loading, high priority -->
<img 
  src="hero.webp" 
  fetchpriority="high"
  loading="eager"
  decoding="sync"
  alt="Hero">

<!-- Below-fold images: lazy loading -->
<img 
  src="product.webp" 
  loading="lazy"
  decoding="async"
  alt="Product">
```

## Font optimization

### Loading strategy
```css
/* System font stack as fallback */
body {
  font-family: 'Custom Font', -apple-system, BlinkMacSystemFont, 
               'Segoe UI', Roboto, sans-serif;
}

/* Prevent invisible text */
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* or optional for non-critical */
  font-weight: 400;
  font-style: normal;
  unicode-range: U+0000-00FF; /* Subset to Latin */
}
```

### Preloading critical fonts
```html
<link rel="preload" href="/fonts/heading.woff2" as="font" type="font/woff2" crossorigin>
```

### Variable fonts
```css
/* One file instead of multiple weights */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}
```

## Caching strategy

### Cache-Control headers
```
# HTML (short or no cache)
Cache-Control: no-cache, must-revalidate

# Static assets with hash (immutable)
Cache-Control: public, max-age=31536000, immutable

# Static assets without hash
Cache-Control: public, max-age=86400, stale-while-revalidate=604800

# API responses
Cache-Control: private, max-age=0, must-revalidate
```

### Service worker caching
```javascript
// Cache-first for static assets
self.addEventListener('fetch', (event) => {
  if (event.request.destination === 'image' ||
      event.request.destination === 'style' ||
      event.request.destination === 'script') {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        return cached || fetch(event.request).then((response) => {
          const clone = response.clone();
          caches.open('static-v1').then((cache) => cache.put(event.request, clone));
          return response;
        });
      })
    );
  }
});
```

## Runtime performance

### Avoid layout thrashing
```javascript
// ❌ Forces multiple reflows
elements.forEach(el => {
  const height = el.offsetHeight; // Read
  el.style.height = height + 10 + 'px'; // Write
});

// ✅ Batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight); // All reads
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px'; // All writes
});
```

### Debounce expensive operations
```javascript
function debounce(fn, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

// Debounce scroll/resize handlers
window.addEventListener('scroll', debounce(handleScroll, 100));
```

### Use requestAnimationFrame
```javascript
// ❌ May cause jank
setInterval(animate, 16);

// ✅ Synced with display refresh
function animate() {
  // Animation logic
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

### Virtualize long lists
```javascript
// For lists > 100 items, render only visible items
// Use libraries like react-window, vue-virtual-scroller, or native CSS:
.virtual-list {
  content-visibility: auto;
  contain-intrinsic-size: 0 50px; /* Estimated item height */
}
```

## Third-party scripts

### Load strategies
```javascript
// ❌ Blocks main thread
<script src="https://analytics.example.com/script.js"></script>

// ✅ Async loading
<script async src="https://analytics.example.com/script.js"></script>

// ✅ Delay until interaction
<script>
document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      const script = document.createElement('script');
      script.src = 'https://widget.example.com/embed.js';
      document.body.appendChild(script);
      observer.disconnect();
    }
  });
  observer.observe(document.querySelector('#widget-container'));
});
</script>
```

### Facade pattern
```html
<!-- Show static placeholder until interaction -->
<div class="youtube-facade" 
     data-video-id="abc123" 
     onclick="loadYouTube(this)">
  <img src="/thumbnails/abc123.jpg" alt="Video title">
  <button aria-label="Play video">▶</button>
</div>
```

## Measurement

### Key metrics
| Metric | Target | Tool |
|--------|--------|------|
| LCP | < 2.5s | Lighthouse, CrUX |
| FCP | < 1.8s | Lighthouse |
| Speed Index | < 3.4s | Lighthouse |
| TBT | < 200ms | Lighthouse |
| TTI | < 3.8s | Lighthouse |

### Testing commands
```bash
# Lighthouse CLI
npx lighthouse https://example.com --output html --output-path report.html

# Web Vitals library
import {onLCP, onINP, onCLS} from 'web-vitals';
onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

## References

For Core Web Vitals specific optimizations, see [Core Web Vitals](../core-web-vitals/SKILL.md).

---

# LLM Cost Optimization

Patterns for controlling LLM API costs while maintaining quality. Combines model routing, budget tracking, retry logic, and prompt caching into a composable pipeline.

## When to Use

- Building applications that call LLM APIs (Claude, GPT, etc.)
- Processing batches of items with varying complexity
- Need to stay within a budget for API spend
- Optimizing cost without sacrificing quality on complex tasks

## Core Concepts

### 1. Model Routing by Task Complexity

Automatically select cheaper models for simple tasks, reserving expensive models for complex ones.

```typescript
const MODEL_SONNET = "claude-sonnet-4-6";
const MODEL_HAIKU = "claude-haiku-4-5-20251001";

const SONNET_TEXT_THRESHOLD = 10000;  // chars
const SONNET_ITEM_THRESHOLD = 30;     // items

function selectModel(
  textLength: number,
  itemCount: number,
  forceModel?: string
): string {
  if (forceModel) return forceModel;
  if (textLength >= SONNET_TEXT_THRESHOLD || itemCount >= SONNET_ITEM_THRESHOLD) {
    return MODEL_SONNET;  // Complex task
  }
  return MODEL_HAIKU;  // Simple task (3-4x cheaper)
}
```

### 2. Immutable Cost Tracking

Track cumulative spend with frozen records. Each API call returns a new tracker — never mutates state.

```typescript
interface CostRecord {
  model: string;
  inputTokens: number;
  outputTokens: number;
  costUsd: number;
}

interface CostTracker {
  budgetLimit: number;
  records: CostRecord[];
  totalCost: number;
  overBudget: boolean;
}

function createTracker(budgetLimit = 1.00): CostTracker {
  return {
    budgetLimit,
    records: [],
    totalCost: 0,
    overBudget: false
  };
}

function addCost(tracker: CostTracker, record: CostRecord): CostTracker {
  const newTotal = tracker.totalCost + record.costUsd;
  return {
    ...tracker,
    records: [...tracker.records, record],
    totalCost: newTotal,
    overBudget: newTotal > tracker.budgetLimit
  };
}
```

### 3. Narrow Retry Logic

Retry only on transient errors. Fail fast on authentication or bad request errors.

```typescript
const RETRYABLE_ERRORS = [
  "APIConnectionError",
  "RateLimitError",
  "InternalServerError"
];
const MAX_RETRIES = 3;

async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = MAX_RETRIES
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      const errorName = error.constructor.name;
      if (!RETRYABLE_ERRORS.includes(errorName) || attempt === maxRetries - 1) {
        throw error;
      }
      await sleep(Math.pow(2, attempt) * 1000);  // Exponential backoff
    }
  }
  throw new Error("Max retries exceeded");
}
```

### 4. Prompt Caching

Cache long system prompts to avoid resending them on every request.

```typescript
interface CachedMessage {
  role: "user";
  content: Array<{
    type: "text";
    text: string;
    cache_control?: { type: "ephemeral" };
  }>;
}

function buildCachedMessages(
  systemPrompt: string,
  userInput: string
): CachedMessage {
  return {
    role: "user",
    content: [
      {
        type: "text",
        text: systemPrompt,
        cache_control: { type: "ephemeral" }  // Cache this
      },
      {
        type: "text",
        text: userInput  // Variable part
      }
    ]
  };
}
```

## Complete Pipeline Example

```typescript
async function processWithCostControl(
  text: string,
  systemPrompt: string,
  tracker: CostTracker
): Promise<{ result: string; tracker: CostTracker }> {
  // 1. Route model based on complexity
  const model = selectModel(text.length, estimateItems(text));

  // 2. Check budget
  if (tracker.overBudget) {
    throw new Error(`Budget exceeded: $${tracker.totalCost.toFixed(2)}`);
  }

  // 3. Call with retry + caching
  const response = await callWithRetry(() =>
    anthropic.messages.create({
      model,
      messages: [buildCachedMessages(systemPrompt, text)]
    })
  );

  // 4. Track cost (immutable)
  const record: CostRecord = {
    model,
    inputTokens: response.usage.input_tokens,
    outputTokens: response.usage.output_tokens,
    costUsd: calculateCost(model, response.usage)
  };
  const newTracker = addCost(tracker, record);

  return { result: response.content[0].text, tracker: newTracker };
}
```

## Pricing Reference (2025-2026)

| Model | Input ($/1M tokens) | Output ($/1M tokens) | Relative Cost |
|-------|---------------------|----------------------|---------------|
| Haiku 4.5 | $0.80 | $4.00 | 1x |
| Sonnet 4.6 | $3.00 | $15.00 | ~4x |
| Opus 4.5 | $15.00 | $75.00 | ~19x |

## Best Practices

- **Start with the cheapest model** and only route to expensive models when complexity thresholds are met
- **Set explicit budget limits** before processing batches — fail early rather than overspend
- **Log model selection decisions** so you can tune thresholds based on real data
- **Use prompt caching** for system prompts over 1024 tokens — saves both cost and latency
- **Never retry on authentication or validation errors** — only transient failures (network, rate limit, server error)

## Anti-Patterns to Avoid

- Using the most expensive model for all requests regardless of complexity
- Retrying on all errors (wastes budget on permanent failures)
- Mutating cost tracking state (makes debugging and auditing difficult)
- Hardcoding model names throughout the codebase (use constants or config)
- Ignoring prompt caching for repetitive system prompts

## Batch Processing Pattern

```typescript
async function processBatch(
  items: string[],
  systemPrompt: string,
  budgetLimit = 10.00
): Promise<{ results: string[]; tracker: CostTracker }> {
  let tracker = createTracker(budgetLimit);
  const results: string[] = [];

  for (const item of items) {
    try {
      const { result, tracker: newTracker } = await processWithCostControl(
        item,
        systemPrompt,
        tracker
      );
      results.push(result);
      tracker = newTracker;
    } catch (error) {
      if (error.message.includes("Budget exceeded")) {
        console.warn(`Stopped at item ${results.length}/${items.length} due to budget`);
        break;
      }
      throw error;
    }
  }

  return { results, tracker };
}
```

---

*Optimize both web performance and API costs for maximum efficiency.*
