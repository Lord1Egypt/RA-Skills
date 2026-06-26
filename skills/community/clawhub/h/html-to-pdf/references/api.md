# API Reference

## convertHtmlToPdf(inputPath, outputPath, options)

Convert HTML file or URL to PDF.

### Parameters

- **inputPath** (string): Path to HTML file or URL (http/https)
- **outputPath** (string): Output PDF file path
- **options** (object, optional): Puppeteer PDF options
  - `format` (string): Paper format (A4, Letter, etc.) - default: 'A4'
  - `margin` (object): Page margins - default: '10mm all sides'
    - `top`, `right`, `bottom`, `left` (string): e.g., '10mm', '1cm'
  - `landscape` (boolean): Landscape mode - default: false
  - `scale` (number): Zoom scale (0.1 - 2) - default: 1
  - `displayHeaderFooter` (boolean): Show header/footer - default: false
  - `headerTemplate` (string): HTML for header
  - `footerTemplate` (string): HTML for footer
  - `printBackground` (boolean): Print background - default: true
  - `pageRanges` (string): e.g., '1-5, 8, 11-13'

### Returns

Promise: `{ success: true, path: '<output-path>' }`

### Examples

```javascript
const convertHtmlToPdf = require('./html-to-pdf.js');

// Simple conversion
await convertHtmlToPdf('input.html', 'output.pdf');

// With custom options
await convertHtmlToPdf('page.html', 'output.pdf', {
  format: 'A4',
  landscape: true,
  margin: { top: '20mm', bottom: '20mm' }
});

// From URL
await convertHtmlToPdf(
  'https://example.com',
  'output.pdf',
  { format: 'Letter' }
);
```
