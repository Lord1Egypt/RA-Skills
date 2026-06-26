# PDF Templates

DocuScan uses basic CSS templates to make the generated PDFs look professional. You can inject these styles into the HTML wrapper before calling `generate-pdf.sh`.

## Clean & Modern (Default)
```html
<style>
  body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }
  h1, h2, h3 {
    color: #111;
    margin-bottom: 0.5em;
  }
  h1 { border-bottom: 2px solid #eee; padding-bottom: 0.2em; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
  }
  th, td {
    padding: 12px;
    border: 1px solid #ddd;
    text-align: left;
  }
  th { background-color: #f8f9fa; font-weight: bold; }
  ul, ol { padding-left: 2rem; }
  .page-break { page-break-after: always; }
</style>
```

## Formal (For Contracts & Letters)
```html
<style>
  body {
    font-family: 'Times New Roman', Times, serif;
    line-height: 1.5;
    color: #000;
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }
  h1, h2, h3 { text-align: center; }
  p { margin-bottom: 1rem; text-indent: 1.5rem; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
  }
  th, td { padding: 8px; border: 1px solid #000; }
  .page-break { page-break-after: always; }
</style>
```

## Compact (For Receipts & Code/Logs)
```html
<style>
  body {
    font-family: monospace;
    line-height: 1.3;
    font-size: 14px;
    color: #000;
    max-width: 600px;
    margin: 0 auto;
    padding: 1rem;
  }
  h1 { font-size: 18px; border-bottom: 1px dashed #000; padding-bottom: 5px; }
  table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
  th, td { padding: 4px; text-align: left; }
  th { border-bottom: 1px dashed #000; }
</style>
```