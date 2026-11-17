# Client snippets

Every snippet reads the login from `PROXMINT_USERNAME` and `PROXMINT_PASSWORD`. To target a location, append the
targeting to the username before building the URL, for example `user = os.environ["PROXMINT_USERNAME"] + "__cr.us"`.

## curl

```bash
# HTTP and HTTPS sites, port 823
curl -x "http://$PROXMINT_USERNAME:$PROXMINT_PASSWORD@gw.proxmint.com:823" https://api.ipify.org

# A country: targeting goes in the username
curl -x "http://${PROXMINT_USERNAME}__cr.us:$PROXMINT_PASSWORD@gw.proxmint.com:823" https://api.ipify.org

# SOCKS5, port 824. socks5h sends DNS lookups through the proxy too
curl -x "socks5h://$PROXMINT_USERNAME:$PROXMINT_PASSWORD@gw.proxmint.com:824" https://api.ipify.org
```

In bash, write `${PROXMINT_USERNAME}__cr.us` with braces, or the shell reads `PROXMINT_USERNAME__cr` as the
variable name.

## Python: requests

```python
import os
import requests

proxy = f"http://{os.environ['PROXMINT_USERNAME']}:{os.environ['PROXMINT_PASSWORD']}@gw.proxmint.com:823"
r = requests.get("https://api.ipify.org", proxies={"http": proxy, "https": proxy}, timeout=30)
print(r.text)
```

A `requests.Session` reuses connections, so several requests can leave through the same IP. Use a fresh session
per request when each one needs its own IP.

## Python: httpx

```python
import asyncio
import os
import httpx

PROXY = f"http://{os.environ['PROXMINT_USERNAME']}:{os.environ['PROXMINT_PASSWORD']}@gw.proxmint.com:823"

async def main():
    async with httpx.AsyncClient(proxy=PROXY, timeout=30) as client:
        r = await client.get("https://api.ipify.org")
        print(r.text)

asyncio.run(main())
```

httpx 0.26 and later take `proxy=`. Older versions take `proxies=`.

## Python: aiohttp

```python
import asyncio
import os
import aiohttp

PROXY = "http://gw.proxmint.com:823"
AUTH = aiohttp.BasicAuth(os.environ["PROXMINT_USERNAME"], os.environ["PROXMINT_PASSWORD"])

async def main():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        async with session.get("https://api.ipify.org", proxy=PROXY, proxy_auth=AUTH) as r:
            print(await r.text())

asyncio.run(main())
```

## Scrapy

```python
# settings.py: HttpProxyMiddleware ships with Scrapy and is enabled by default
import os

PROXY = f"http://{os.environ['PROXMINT_USERNAME']}:{os.environ['PROXMINT_PASSWORD']}@gw.proxmint.com:823"
```

```python
# in the spider
yield scrapy.Request(url, meta={"proxy": self.settings["PROXY"]}, callback=self.parse)
```

Setting the proxy per request lets one crawl mix locations: build a different username for each target.

## Node.js: fetch (undici)

```javascript
import { ProxyAgent } from "undici";

const { PROXMINT_USERNAME: user, PROXMINT_PASSWORD: pass } = process.env;
const agent = new ProxyAgent(`http://${user}:${encodeURIComponent(pass)}@gw.proxmint.com:823`);

const res = await fetch("https://api.ipify.org", { dispatcher: agent });
console.log(await res.text());
```

Node's built-in fetch ignores `HTTP_PROXY`. Pass a dispatcher per request, or set one globally with undici's
`setGlobalDispatcher`. With axios, pass an `https-proxy-agent` instance as `httpsAgent` and set `proxy: false`.

## Go: net/http

```go
proxyURL := &url.URL{
    Scheme: "http",
    User:   url.UserPassword(os.Getenv("PROXMINT_USERNAME"), os.Getenv("PROXMINT_PASSWORD")),
    Host:   "gw.proxmint.com:823",
}
client := &http.Client{
    Transport: &http.Transport{Proxy: http.ProxyURL(proxyURL)},
    Timeout:   30 * time.Second,
}
resp, err := client.Get("https://api.ipify.org")
```

One `http.Client` is safe to share across goroutines.

## Playwright

```python
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(proxy={
        "server": "http://gw.proxmint.com:823",
        "username": os.environ["PROXMINT_USERNAME"],  # targeting goes here: login__cr.de
        "password": os.environ["PROXMINT_PASSWORD"],
    })
    page = browser.new_page()
    page.goto("https://api.ipify.org")
    print(page.inner_text("body"))
    browser.close()
```

Keep `server` as host and port only. Chromium can't read credentials embedded in the proxy URL, which is why
Playwright takes them as separate fields. Node is the same: pass `{ server, username, password }` to `launch`.

## Puppeteer

```javascript
import puppeteer from "puppeteer";

const browser = await puppeteer.launch({ args: ["--proxy-server=http://gw.proxmint.com:823"] });
const page = await browser.newPage();
await page.authenticate({
  username: process.env.PROXMINT_USERNAME, // targeting goes here: login__cr.fr
  password: process.env.PROXMINT_PASSWORD,
});
await page.goto("https://api.ipify.org");
console.log(await page.evaluate(() => document.body.innerText));
await browser.close();
```

Call `page.authenticate` before `page.goto`, or the first navigation fails with `407`.

## Selenium

Chrome and Firefox WebDriver have no way to send a proxy username and password. Two clean options:

1. **Allowlist the machine's IP** on the product's Access tab, then start the browser with no login:

   ```python
   from selenium import webdriver

   options = webdriver.ChromeOptions()
   options.add_argument("--proxy-server=http://gw.proxmint.com:823")
   driver = webdriver.Chrome(options=options)
   ```

   Location then comes from the product's saved Targeting.

2. **Run Proxmint's local proxy container**, which adds the login and targeting for you and listens on
   localhost. Setup and options: `https://proxmint.com/docs/docker`.

   Then point the browser at `--proxy-server=http://127.0.0.1:8080`. Keep the port bound to `127.0.0.1`:
   anyone who can reach it spends the user's bandwidth.
