---
name: html-to-pdf
description: Convert HTML files and URLs to PDF using Puppeteer. Use when a user needs to convert HTML documents, web pages, or reports to PDF format with custom formatting options (margins, page size, orientation, headers/footers).
---

# HTML to PDF Conversion

Convert HTML files and web pages to professional PDF documents using Puppeteer.

## Quick Start

### CLI Usage

```bash
node scripts/html-to-pdf.js input.html output.pdf
node scripts/html-to-pdf.js input.html output.pdf A4
node scripts/html-to-pdf.js https://example.com output.pdf A4
```

### Programmatic Usage

```javascript
const convertHtmlToPdf = require('./scripts/html-to-pdf.js');

// Simple conversion
await convertHtmlToPdf('input.html', 'output.pdf');

// With options
await convertHtmlToPdf('input.html', 'output.pdf', {
  format: 'Letter',
  landscape: true,
  margin: { top: '20mm', bottom: '20mm' }
});
```

## Features

- ✅ Convert local HTML files
- ✅ Convert web URLs (http/https)
- ✅ Customizable page formats (A4, Letter, etc.)
- ✅ Custom margins and spacing
- ✅ Landscape/portrait modes
- ✅ Print backgrounds
- ✅ Headers and footers
- ✅ Page ranges
- ✅ Zoom scaling

## Common Options

| Option | Type | Default | Notes |
|--------|------|---------|-------|
| format | string | 'A4' | A4, Letter, A3, A5, etc. |
| landscape | boolean | false | Landscape orientation |
| margin | object | 10mm all | { top, right, bottom, left } |
| scale | number | 1 | 0.1 to 2.0 |
| printBackground | boolean | true | Include background colors |
| displayHeaderFooter | boolean | false | Show header/footer |

## Advanced Usage

### With Headers and Footers

```javascript
await convertHtmlToPdf('page.html', 'output.pdf', {
  displayHeaderFooter: true,
  headerTemplate: '<div>Page <span class="pageNumber"></span></div>',
  footerTemplate: '<div>© 2024</div>',
  margin: { top: '40px', bottom: '40px' }
});
```

### Specific Page Ranges

```javascript
await convertHtmlToPdf('document.html', 'pages-1-5.pdf', {
  pageRanges: '1-5'
});
```

## Installation

Requires Node.js and npm:

```bash
npm install puppeteer
```

## Reference

For complete API documentation and all available options, see [api.md](references/api.md).
