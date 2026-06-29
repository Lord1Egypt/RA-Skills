# Code Examples

All examples use ESM imports. Node.js >= 22 required.

## Basic queue crawling

```js
import Crawler from "crawler";

const c = new Crawler({
  maxConnections: 10,
  callback: (error, res, done) => {
    if (error) {
      console.error(error);
    } else {
      const $ = res.$;
      console.log($("title").text());
    }
    done(); // REQUIRED: release the slot
  },
});

c.on("drain", () => console.log("All done — queue empty"));

// Add URLs
c.add("https://example.com");
c.add(["https://a.com", "https://b.com"]);

// Add tasks with per-task options
c.add({
  url: "https://example.com/item/1",
  jQuery: false,
  callback: (e, res, done) => {
    console.log("Grabbed", res.body.length, "bytes");
    done();
  },
});

// Add raw HTML (for testing — no network request)
c.add({ html: "<title>Test</title>" });
```

## Rate limiting

```js
const c = new Crawler({
  rateLimit: 1000,   // >=1000ms gap between requests; forces maxConnections=1
  retries: 2,
  retryInterval: 3000,
  timeout: 20000,
  callback: (e, res, done) => {
    if (!e) console.log(res.$("title").text());
    done();
  },
});

c.add(tasks);
```

## Per-proxy rate limiters

```js
const c = new Crawler({
  rateLimit: 2000,
  maxConnections: 1,
  callback: (e, res, done) => { done(); },
});

c.add({ url: "https://site/page/1", rateLimiterId: 1, proxy: "http://p1:port" });
c.add({ url: "https://site/page/2", rateLimiterId: 2, proxy: "http://p2:port" });
c.add({ url: "https://site/page/3", rateLimiterId: 1, proxy: "http://p1:port" });
```

Tuning a limiter at runtime:

```js
c.setLimiter(0, "rateLimit", 1000);   // default limiter
c.setLimiter(1, "rateLimit", 500);    // limiter with id=1
```

## Data extraction with Cheerio

```js
const c = new Crawler({
  callback: (e, res, done) => {
    if (e) { done(); return; }
    const $ = res.$;

    // Extract text
    const titles = $("h2.title").map((i, el) => $(el).text().trim()).get();

    // Extract links
    const links = $("a").map((i, el) => $(el).attr("href")).get();

    // Extract structured data
    const items = [];
    $(".product-card").each((i, el) => {
      items.push({
        name: $(el).find(".name").text().trim(),
        price: $(el).find(".price").text().trim(),
        link: $(el).find("a").attr("href"),
      });
    });

    console.log(items);
    done();
  },
});

c.add(["https://example.com/products/page/1", "https://example.com/products/page/2"]);
```

## Passing data with userParams

```js
c.add({
  url: "https://site/item/42",
  userParams: { id: 42, category: "books" },
});

// In callback:
const { id, category } = res.options.userParams;
console.log(`Processing item ${id} in ${category}`);
```

## Binary file download

```js
import Crawler from "crawler";
import fs from "fs";

const c = new Crawler({
  encoding: null,     // keep body as Buffer
  jQuery: false,      // skip Cheerio parsing
  callback: (err, res, done) => {
    if (err) {
      console.error(err);
      done();
      return;
    }
    const filename = res.options.userParams.filename;
    fs.writeFileSync(filename, res.body);
    console.log(`Saved ${filename} (${res.body.length} bytes)`);
    done();
  },
});

c.add({
  url: "https://example.com/image.png",
  userParams: { filename: "./downloads/image.png" },
});
```

## Direct requests (send)

```js
const c = new Crawler();

// Promise form
const res = await c.send("https://example.com");
console.log(res.statusCode, res.body.length);

// Callback form (2 args, no done())
c.send({
  url: "https://example.com",
  callback: (error, response) => {
    if (error) console.error(error);
    else console.log(response.body);
  },
});
```

## HTTP/2

```js
c.add({
  url: "https://nghttp2.org/httpbin/status/200",
  http2: true,
  callback: (e, res, done) => {
    console.log(res.statusCode);
    done();
  },
});

// With proxy + Charles (self-signed cert)
c.add({
  url: "https://example.com",
  http2: true,
  proxy: "http://127.0.0.1:8888",
  rejectUnauthorized: false,
  callback: (e, res, done) => { done(); },
});
```

## Proxy rotation via events

```js
const proxies = ["http://p1:8080", "http://p2:8080", "http://p3:8080"];
let idx = 0;

const c = new Crawler({
  maxConnections: 5,
  callback: (e, res, done) => { done(); },
});

c.on("schedule", options => {
  options.proxy = proxies[idx];
  idx = (idx + 1) % proxies.length;
});

c.on("request", options => {
  // Last-moment modification before sending
  options.searchParams = { t: Date.now() };
});

c.add(["https://example.com/page/1", "https://example.com/page/2", "..."]);
```

## preRequest hook

```js
const c = new Crawler({
  preRequest: (options, done) => {
    // 'options' is the final request config passed to `got`
    console.log("About to request:", options.url);
    done(); // must call to proceed
  },
  callback: (e, res, done) => {
    console.log(res.statusCode);
    done();
  },
});

c.add("https://example.com");

// Per-task preRequest (overrides global)
c.add({
  url: "https://example.com/special",
  preRequest: (options, done) => {
    options.headers["X-Custom"] = "value";
    done();
  },
});
```

## Full spider example

A complete spider that crawls a paginated listing, extracts data, and follows links:

```js
import Crawler from "crawler";
import fs from "fs";

const results = [];
const baseUrl = "https://example.com/products";

const c = new Crawler({
  maxConnections: 5,
  rateLimit: 1000,
  retries: 3,
  callback: (error, res, done) => {
    if (error) {
      console.error(`Failed: ${res.options.url} — ${error.message}`);
      done();
      return;
    }

    const $ = res.$;

    // Extract items on this page
    $(".product-item").each((i, el) => {
      results.push({
        title: $(el).find(".title").text().trim(),
        price: $(el).find(".price").text().trim(),
        link: $(el).find("a").attr("href"),
      });
    });

    // Follow next page link
    const nextPage = $("a.next").attr("href");
    if (nextPage) {
      c.add(`${baseUrl}${nextPage}`);
    }

    done();
  },
});

c.on("drain", () => {
  fs.writeFileSync("results.json", JSON.stringify(results, null, 2));
  console.log(`Done. Scraped ${results.length} items.`);
});

// Start with the first page
c.add(`${baseUrl}?page=1`);
```
