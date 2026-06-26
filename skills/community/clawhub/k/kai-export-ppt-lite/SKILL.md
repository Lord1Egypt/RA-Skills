---
name: kai-export-ppt-lite
description: Use when exporting HTML presentations to editable PPTX in sandbox environments where Playwright cannot be installed. Pure Python: bs4 + python-pptx + Pillow. Keywords: export pptx sandbox, html to pptx no browser, editable powerpoint from html.
version: 1.6.9
metadata:
  openclaw:
    emoji: "📄"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
    install:
      - id: beautifulsoup4
        kind: uv
        package: beautifulsoup4
        label: beautifulsoup4 (HTML parsing)
      - id: lxml
        kind: uv
        package: lxml
        label: lxml (HTML parser backend)
      - id: python-pptx
        kind: uv
        package: python-pptx
        label: python-pptx (editable PPTX generation)
      - id: Pillow
        kind: uv
        package: Pillow
        label: Pillow (image handling)
---

# kai-export-ppt-lite

Export HTML presentations to **editable PPTX** without a browser. Pure Python — no Playwright, no Chrome, no Node.js.

## Commands

| Command | What it does |
|---------|-------------|
| `python3 <skill-path>/scripts/export-sandbox-pptx.py <file.html> [output.pptx] [--width 1440] [--height 900]` | Canonical entrypoint; works as a real file or as inline-retrieved script |
| `python3 <skill-path>/scripts/run-skill-export.py <file.html> [output.pptx] [--width 1440] [--height 900]` | Optional tiny bootstrap when the runtime exposes a real installed skill directory |

## Dependencies

| Package | Install |
|---------|---------|
| `beautifulsoup4` | Usually auto-installed by skill metadata or `pip install beautifulsoup4` |
| `lxml` | Usually auto-installed by skill metadata or `pip install lxml` |
| `python-pptx` | Usually auto-installed by skill metadata or `pip install python-pptx` |
| `Pillow` | Usually auto-installed by skill metadata or `pip install Pillow` |

## Usage

```bash
python3 <skill-path>/scripts/export-sandbox-pptx.py <file.html> [output.pptx] [--width 1440] [--height 900]
```

Local repo execution remains available:

```bash
python3 scripts/export-sandbox-pptx.py <file.html> [output.pptx] [--width 1440] [--height 900]
```

## Sandbox Execution

Do not assume anything about the agent runtime. This skill must tolerate:

- no stable skill root path
- no `__file__`
- notebook / cell-style inline execution
- dependencies either preinstalled or missing

When this skill runs inside a hosted sandbox, use this decision order:

1. Default path: retrieve and execute `scripts/export-sandbox-pptx.py`.
2. If the runtime exposes a real installed skill directory, you may instead call:
   ```bash
   python3 <skill-path>/scripts/export-sandbox-pptx.py input.html output.pptx
   ```
3. If the runtime only supports inline Python execution, retrieve `scripts/export-sandbox-pptx.py` and inline it directly.
4. Pass the HTML input via the sandbox VFS/attachment mechanism and write the PPTX to the sandbox artifact directory.
5. Let the script self-bootstrap dependencies first. Skill metadata / `requirements.txt` are optimizations, not assumptions.
6. `scripts/run-skill-export.py` is an optional optimization only. Do not require it for correctness.

### Why this is the stable path

- `scripts/export-sandbox-pptx.py` is the only execution surface that does not require assuming a skill root, env var, or installer-specific layout.
- The exporter now tolerates missing `__file__`, degrades when vendored `contracts/` are absent, and attempts runtime dependency bootstrap before failing.
- `run-skill-export.py` remains useful when the environment is richer, but it is not part of the correctness boundary.
- If vendored `contracts/` are unavailable, export still runs; only preset-specific fidelity hints degrade.

### Prohibited patterns

- assuming an installed skill directory exists
- assuming `__file__` exists in notebook / cell-based sandboxes
- assuming build-time dependency installation always happened
- making `run-skill-export.py` the only supported path

### Options

| Flag | Description |
|------|-------------|
| `--width N` | Slide width in pixels (default: 1440) |
| `--height N` | Slide height in pixels (default: 900) |
| `--with-chrome` | Add page counter and nav dots |

## What it extracts

| HTML Element | PPTX Output |
|-------------|-------------|
| `h1-h6, p, li, span` | Editable text boxes |
| `div` with background/border | Rounded rectangles with fill |
| `table, tr, td, th` | Cell rectangles with text frames |
| `img` (http/file/data-uri) | Embedded pictures |
| `svg` | Placeholder rectangle |

## Limitations (no browser)

- CSS variables: only `:root` static substitution
- Layout: simulated flex-column, not pixel-perfect
- Computed styles: unavailable, relies on inline style + `<style>` blocks
- JavaScript: not executed, so IntersectionObserver-gated content won't appear

## Comparison

| | kai-html-export (full) | kai-export-ppt-lite |
|---|---|---|
| Runtime | Playwright + Chrome | Pure Python |
| Sandbox compatible | ❌ | ✅ |
| Output quality | Pixel-perfect | Semantic layout |
| Editable text | ✅ | ✅ |
| Image mode PPTX | ✅ (screenshot) | ❌ |
| Dependencies | playwright, python-pptx | bs4, lxml, python-pptx, Pillow |
