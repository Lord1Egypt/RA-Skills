#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

RENDER_SNIPPET = r'''
const { chromium } = require("playwright");
(async () => {
  const argv = process.argv.slice(-2);
  const url = argv[0];
  const waitMs = Number(argv[1] || 2500);
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ userAgent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" });
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
  await page.waitForTimeout(waitMs);
  const result = await page.evaluate(() => {
    const pick = (sel) => document.querySelector(sel)?.content || document.querySelector(sel)?.innerText || null;
    const title = document.title || pick('meta[property="og:title"]') || null;
    const description = pick('meta[name="description"]') || pick('meta[property="og:description"]');
    const author = pick('meta[name="author"]') || pick('meta[property="article:author"]');
    const published = pick('meta[property="article:published_time"]') || pick('time[datetime]');
    const article = document.querySelector('article');
    let text = '';
    if (article) {
      text = article.innerText || '';
    }
    if (!text || text.trim().length < 300) {
      const paras = [...document.querySelectorAll('main p, article p, [role="main"] p, p')]
        .map(x => (x.innerText || '').trim())
        .filter(Boolean)
        .filter(x => x.length >= 40);
      text = paras.join('\n\n');
    }
    return {
      final_url: location.href,
      title,
      description,
      author,
      published_time: published,
      text,
      excerpt: (text || '').slice(0, 280)
    };
  });
  await browser.close();
  process.stdout.write(JSON.stringify(result, null, 2));
})().catch(err => {
  process.stderr.write(String(err && err.stack || err));
  process.exit(1);
});
'''


def find_node() -> Optional[str]:
    return shutil.which("node")


def npm_global_root() -> Optional[str]:
    npm = shutil.which("npm")
    if not npm:
        return None
    run = subprocess.run([npm, "root", "-g"], capture_output=True, text=True)
    if run.returncode != 0:
        return None
    root = run.stdout.strip()
    return root or None


def node_env_with_global_modules() -> dict:
    env = os.environ.copy()
    root = npm_global_root()
    if root:
        existing = env.get("NODE_PATH", "")
        env["NODE_PATH"] = f"{root}:{existing}" if existing else root
    return env


def has_playwright() -> bool:
    node = find_node()
    if not node:
        return False
    check = subprocess.run(
        [node, "-e", "require.resolve('playwright'); console.log('ok')"],
        capture_output=True,
        text=True,
        env=node_env_with_global_modules(),
    )
    return check.returncode == 0


def browser_install_hint() -> str:
    hints = [
        "Browser rendering is scripted, but the local runtime dependency is missing.",
        "Install Node Playwright and a browser, then rerun.",
        "Example:",
        "  npm install -g playwright",
        "  playwright install chromium",
    ]
    return "\n".join(hints)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a webpage in headless Chromium via Playwright.")
    parser.add_argument("url")
    parser.add_argument("--wait-ms", type=int, default=2500)
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--max-chars", type=int, default=8000)
    args = parser.parse_args()

    node = find_node()
    if not node or not has_playwright():
        payload = {
            "url": args.url,
            "method": "browser-render:unavailable",
            "error": browser_install_hint(),
        }
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(payload["error"])
        return 2

    cmd = [node, "-e", RENDER_SNIPPET, args.url, str(args.wait_ms)]
    run = subprocess.run(cmd, capture_output=True, text=True, env=node_env_with_global_modules())
    if run.returncode != 0:
        payload = {
            "url": args.url,
            "method": "browser-render:failed",
            "error": run.stderr.strip() or run.stdout.strip() or "playwright render failed",
        }
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(payload["error"])
        return 1

    data = json.loads(run.stdout)
    data["url"] = args.url
    data["method"] = "browser-render:playwright"
    if args.max_chars and data.get("text"):
        data["text"] = data["text"][: args.max_chars]
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    print(f"Title: {data.get('title') or ''}")
    if data.get("author"):
        print(f"Author: {data['author']}")
    if data.get("published_time"):
        print(f"Published: {data['published_time']}")
    if data.get("description"):
        print(f"Description: {data['description']}")
    print(f"Method: {data['method']}")
    print()
    print(data.get("text") or "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
