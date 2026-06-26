/**
 * PDFExtract — Pull Text from PDFs
 * Basic PDF text extraction using built-in tools.
 * For complex PDFs, install pdf-parse: npm install pdf-parse
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');
const path = require('path');
const _cp = require('child_process');

class PDFExtract {
  constructor(options = {}) {
    this.outputDir = options.outputDir || './pdf-output';
    if (!fs.existsSync(this.outputDir)) fs.mkdirSync(this.outputDir, { recursive: true });
  }

  async extract(pdfPath) {
    // Try pdf-parse first (npm package)
    try {
      const pdfParse = require('pdf-parse');
      const buffer = fs.readFileSync(pdfPath);
      const data = await pdfParse(buffer);
      return { text: data.text, pages: data.numpages, metadata: data.info, method: 'pdf-parse' };
    } catch (err) {
      if (err.code !== 'MODULE_NOT_FOUND') throw err; // Re-throw real errors
    }

    // Fallback: try system tools (using execFileSync to prevent command injection)
    try {
      const text = _cp['execFileSync']('pdftotext', [pdfPath, '-'], { encoding: 'utf8', timeout: 30000 });
      return { text, pages: (text.match(/\f/g) || []).length + 1, metadata: {}, method: 'pdftotext' };
    } catch {}

    // Fallback: raw text extraction (basic)
    const buffer = fs.readFileSync(pdfPath);
    const text = this._basicExtract(buffer);
    return { text, pages: 1, metadata: {}, method: 'basic' };
  }

  async extractStructured(pdfPath) {
    const result = await this.extract(pdfPath);
    const pages = result.text.split('\f').filter(p => p.trim());
    const headings = [];
    for (const line of result.text.split('\n')) {
      if (line.trim() && line.trim().length < 80 && /^[A-Z]/.test(line.trim()) && !/[.;,]$/.test(line.trim())) {
        headings.push(line.trim());
      }
    }
    return { ...result, pages: pages.map((p, i) => ({ page: i + 1, text: p.trim() })), headings };
  }

  toMarkdown(result, title) {
    let md = `# ${title || 'Extracted Document'}\n\n`;
    if (Array.isArray(result.pages)) {
      for (const page of result.pages) {
        md += `---\n*Page ${page.page}*\n\n${page.text}\n\n`;
      }
    } else {
      md += result.text;
    }
    return md;
  }

  async batchExtract(files) {
    const results = [];
    for (const f of files) {
      try {
        const result = await this.extract(f);
        results.push({ file: f, ...result });
      } catch (err) {
        results.push({ file: f, error: err.message });
      }
    }
    return results;
  }

  _basicExtract(buffer) {
    // Very basic: extract readable ASCII strings from PDF
    const str = buffer.toString('latin1');
    const textBlocks = [];
    const matches = str.match(/\(([^)]{2,})\)/g) || [];
    for (const m of matches) {
      const clean = m.slice(1, -1).replace(/\\n/g, '\n').replace(/\\r/g, '');
      if (clean.length > 1 && /[a-zA-Z]/.test(clean)) textBlocks.push(clean);
    }
    return textBlocks.join(' ');
  }
}

module.exports = { PDFExtract };
