#!/usr/bin/env python3
"""Extract a generated image from ChatGPT via CDP fetch+blob approach.

Usage:
    python3 extract_image.py <tab_id> <output_path> [--cdp-port 9222] [--index N]

Finds the generated image in the ChatGPT conversation, fetches it via page-context
fetch (same-origin, no CORS issues), converts to base64, and saves to disk.

ChatGPT images appear as <img> elements with src like:
  - https://chatgpt.com/backend-api/estuary/content?id=file_XXX
  - blob: URLs
  - https://files.oaiusercontent.com/...
"""
import argparse
import base64
import json
import os
import subprocess
import sys


CDP_HOST = "127.0.0.1"


def cdp_eval(tab_id: str, expr: str, port: int = 9222, await_promise: bool = False) -> str:
    """Evaluate JS via CDP using the shared brave-browser-agent cdp_exec.py."""
    brave_dir = os.path.expanduser("brave-browser-agent/scripts")
    cdp_script = os.path.join(brave_dir, "cdp_exec.py")
    cmd = [sys.executable, cdp_script, "--port", str(port),
           "eval", tab_id, expr]
    if await_promise:
        cmd.append("--await-promise")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"cdp_exec failed: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description="Extract generated image from ChatGPT tab")
    ap.add_argument("tab_id", help="CDP tab ID of the ChatGPT page")
    ap.add_argument("output_path", help="Where to save the image file")
    ap.add_argument("--cdp-port", type=int, default=9222)
    ap.add_argument("--index", type=int, default=-1, help="Image index: -1=largest in conversation (default), 0=first large")
    args = ap.parse_args()

    port = args.cdp_port
    tab = args.tab_id
    out = args.output_path

    # 1. Find generated images in the conversation
    js_find = """
    (function() {
        var imgs = document.querySelectorAll('img');
        var results = [];
        for (var i = 0; i < imgs.length; i++) {
            var img = imgs[i];
            var w = img.naturalWidth || img.width || 0;
            var h = img.naturalHeight || img.height || 0;
            if (w >= 200 && h >= 200) {
                var inConv = !!img.closest(
                    '[data-testid*="conversation-turn"], .markdown, ' +
                    '[class*="response"], [class*="message"], [class*="turn"]'
                );
                var srcType = 'unknown';
                if (img.src.startsWith('blob:')) srcType = 'blob';
                else if (img.src.includes('oaiusercontent')) srcType = 'oai';
                else if (img.src.includes('backend-api')) srcType = 'backend';
                else if (img.src.startsWith('data:image')) srcType = 'data';
                results.push({
                    idx: i, w: w, h: h, srcType: srcType,
                    inConv: inConv, area: w * h,
                    src: img.src.substring(0, 100)
                });
            }
        }
        if (results.length === 0) return 'NOT_FOUND';
        results.sort(function(a, b) {
            if (a.inConv !== b.inConv) return a.inConv ? -1 : 1;
            return b.area - a.area;
        });
        return JSON.stringify(results.slice(0, 8));
    })()
    """
    info = cdp_eval(tab, js_find, port)
    if info == "NOT_FOUND":
        raise SystemExit("❌ No suitable image found. The image may not be ready yet.")

    print(f"Found images: {info}")
    images = json.loads(info)

    # Pick target image
    if args.index >= 0 and args.index < len(images):
        target = images[args.index]
    else:
        target = images[0]  # Already sorted: in-conversation, largest first
    idx = target["idx"]
    print(f"Target: index={idx}, {target['w']}x{target['h']}, srcType={target['srcType']}")

    # 2. Fetch the image using page-context fetch (same-origin, bypasses CORS)
    js_fetch = f"""
    (function() {{
        var imgs = document.querySelectorAll('img');
        var img = imgs[{idx}];
        if (!img) return 'NO_IMG';
        return fetch(img.src)
            .then(function(r) {{ return r.blob(); }})
            .then(function(blob) {{
                return new Promise(function(resolve) {{
                    var reader = new FileReader();
                    reader.onloadend = function() {{
                        window._gptImgB64 = reader.result.split(',')[1];
                        resolve('OK:' + window._gptImgB64.length);
                    }};
                    reader.readAsDataURL(blob);
                }});
            }})
            .catch(function(e) {{ return 'FETCH_ERROR:' + e.message; }});
    }})()
    """
    result = cdp_eval(tab, js_fetch, port, await_promise=True)
    print(f"Fetch: {result}")

    if not result or not result.startswith("OK:"):
        raise SystemExit(f"❌ Image fetch failed: {result}")

    total_len = int(result.split(":")[1])
    print(f"Base64 size: {total_len} chars (~{total_len * 3 // 4 // 1024}KB image)")

    # 3. Read base64 in chunks
    chunk_size = 100000
    parts = []
    offset = 0
    while offset < total_len:
        end = min(offset + chunk_size, total_len)
        js_chunk = f"window._gptImgB64.substring({offset},{end})"
        chunk = cdp_eval(tab, js_chunk, port)
        parts.append(chunk)
        offset = end
        pct = offset * 100 // total_len
        if pct % 20 < 5:
            print(f"  {pct}% ({offset}/{total_len})")

    img_data = base64.b64decode("".join(parts))

    # 4. Write file
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "wb") as f:
        f.write(img_data)
    print(f"✅ Saved {len(img_data)} bytes to {out}")


if __name__ == "__main__":
    main()
