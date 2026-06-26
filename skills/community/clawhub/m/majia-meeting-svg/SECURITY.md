# Security

This skill processes user-provided meeting transcripts locally and outputs self-contained SVG + PNG files. The PNG conversion script (`scripts/svg2png.py`) uses Puppeteer (headless Chrome) or cairosvg — both run locally with no network requests beyond the one-time `npm install` of Puppeteer. No data is stored externally or sent to any service.

## Reporting

If you find a security issue, please open a GitHub issue or contact the author directly.
