#!/usr/bin/env python3

import argparse
from pathlib import Path

INDEX_HTML = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Pretext Starter</title>
    <script type=\"importmap\">
      {
        \"imports\": {
          \"@chenglou/pretext\": \"/node_modules/@chenglou/pretext/dist/layout.js\"
        }
      }
    </script>
    <script type=\"module\" src=\"./demo.mjs\"></script>
  </head>
  <body>
    <p id=\"target\">Hello from Pretext.</p>
  </body>
</html>
"""

DEMO_MJS = """import { layout, prepare } from '@chenglou/pretext';

await document.fonts.ready;

const target = document.getElementById('target');
const styles = getComputedStyle(target);
const font = styles.font;
const lineHeight = Number.parseFloat(styles.lineHeight);
const width = target.getBoundingClientRect().width;
const prepared = prepare(target.textContent || '', font);
const metrics = layout(prepared, width, lineHeight);

console.log('pretext metrics', metrics);
"""

def write_file(path: Path, contents: str) -> None:
    path.write_text(contents, encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description='Scaffold a minimal browser pretext demo.')
    parser.add_argument('--out', required=True, help='Output directory for the generated files')
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    write_file(out_dir / 'index.html', INDEX_HTML)
    write_file(out_dir / 'demo.mjs', DEMO_MJS)

    print(f'Created {out_dir / "index.html"}')
    print(f'Created {out_dir / "demo.mjs"}')


if __name__ == '__main__':
    main()
