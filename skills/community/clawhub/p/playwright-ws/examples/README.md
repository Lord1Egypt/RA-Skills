# Examples

## Basic Screenshot

```bash
node scripts/screenshot.js https://example.com output.png
```

## Full Page Screenshot

```bash
node scripts/screenshot.js https://example.com output.png --full-page
```

## PDF Generation

```bash
node scripts/pdf-export.js https://example.com output.pdf --format=A4
```

## Wait for Element

```bash
node scripts/screenshot.js https://example.com output.png --wait-for=".loaded" --delay=1000
```