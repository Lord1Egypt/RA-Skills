#!/usr/bin/env python3
"""
Excalidraw to PNG exporter using Excalidraw's exportToBlob API.

Uses Playwright + local HTTP server + ExcalidrawLib.exportToBlob()
for reliable rendering with fonts and Chinese text support.

Usage:
    python3 export-png.py input.excalidraw output.png [--width 1600] [--height 1000]

Requirements:
    pip install playwright
    playwright install chromium
"""

import sys
import os
import json
import argparse
import tempfile
import shutil
import threading
import http.server
import socketserver
import base64
import time
from pathlib import Path


def build_html(data_json: str, width: int, height: int) -> str:
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@excalidraw/excalidraw@0.17.6/dist/excalidraw.production.min.js"></script>
</head><body>
<div id="root" style="width:{width}px;height:{height}px"></div>
<script>
const DATA = {data_json};

window.addEventListener('load', () => {{
  const Lib = window.ExcalidrawLib;
  if (!Lib) {{ window.__EXPORT_ERROR = 'ExcalidrawLib not found'; return; }}
  
  function App() {{
    const [api, setApi] = React.useState(null);
    React.useEffect(() => {{
      if (!api) return;
      setTimeout(async () => {{
        try {{
          const blob = await Lib.exportToBlob({{
            elements: DATA.elements || [],
            appState: {{ 
              ...(DATA.appState || {{}}), 
              viewBackgroundColor: '#ffffff',
              exportWithDarkMode: false,
              exportBackground: true,
            }},
            files: DATA.files || {{}},
            exportPadding: 40,
          }});
          const reader = new FileReader();
          reader.onload = () => {{ window.__EXPORT_DATA = reader.result; }};
          reader.readAsDataURL(blob);
        }} catch(e) {{
          window.__EXPORT_ERROR = e.message;
        }}
      }}, 3000);
    }}, [api]);
    
    return React.createElement('div', {{style:{{width:'{width}px',height:'{height}px'}}}},
      React.createElement(Lib.Excalidraw, {{
        excalidrawAPI: setApi,
        initialData: {{ elements: DATA.elements, appState: DATA.appState }},
      }})
    );
  }}
  ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
}});
</script></body></html>"""


def export_png(input_path: str, output_path: str, width: int = 1600, height: int = 1000):
    """Export an Excalidraw file to PNG using exportToBlob API."""
    input_file = Path(input_path).resolve()
    output_file = Path(output_path).resolve()

    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data_json = json.dumps(data, ensure_ascii=False)
    html_content = build_html(data_json, width, height)

    tmpdir = tempfile.mkdtemp()
    try:
        html_path = os.path.join(tmpdir, 'render.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Start local HTTP server (avoids file:// ORB restrictions)
        port = 18765
        for p in range(18765, 18775):
            try:
                httpd = socketserver.TCPServer(('127.0.0.1', p), 
                    type('H', (http.server.SimpleHTTPRequestHandler,), {'log_message': lambda *a: None}))
                port = p
                break
            except OSError:
                continue

        httpd.allow_reuse_address = True
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        os.chdir(tmpdir)

        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                page = browser.new_page(viewport={'width': width, 'height': height})

                print(f"Loading Excalidraw...", file=sys.stderr)
                page.goto(f'http://127.0.0.1:{port}/render.html', 
                         wait_until='networkidle', timeout=60000)

                print("Waiting for export...", file=sys.stderr)
                for i in range(30):
                    time.sleep(1)
                    result = page.evaluate(
                        "() => ({ data: window.__EXPORT_DATA, error: window.__EXPORT_ERROR })")
                    if result.get("data"):
                        b64 = result["data"].split(",")[1]
                        output_file.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_file, "wb") as f:
                            f.write(base64.b64decode(b64))
                        size = output_file.stat().st_size
                        print(f"✅ PNG exported: {output_file} ({size:,} bytes / {size/1024:.1f} KB)")
                        break
                    if result.get("error"):
                        print(f"Export error: {result['error']}", file=sys.stderr)
                        sys.exit(1)
                else:
                    print("Timeout waiting for export", file=sys.stderr)
                    sys.exit(1)

                browser.close()
        finally:
            httpd.shutdown()

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description='Export Excalidraw to PNG')
    parser.add_argument('input', help='Input .excalidraw file')
    parser.add_argument('output', help='Output .png file')
    parser.add_argument('--width', type=int, default=1600, help='Viewport width (default: 1600)')
    parser.add_argument('--height', type=int, default=1000, help='Viewport height (default: 1000)')
    args = parser.parse_args()
    export_png(args.input, args.output, args.width, args.height)


if __name__ == '__main__':
    main()
