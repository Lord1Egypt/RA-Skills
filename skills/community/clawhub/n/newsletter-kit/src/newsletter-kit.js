/**
 * NewsletterKit — Email Newsletter Builder
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');

class NewsletterKit {
  constructor(options = {}) {
    this.name = options.name || 'Newsletter';
    this.sections = {};
    this.dataFile = options.dataFile || './newsletter-items.json';
    this._loadItems();
  }

  addItem(item) {
    const section = item.section || 'General';
    if (!this.sections[section]) this.sections[section] = [];
    this.sections[section].push({
      title: item.title,
      url: item.url || null,
      note: item.note || '',
      added: new Date().toISOString()
    });
    this._saveItems();
    return { section, count: this.sections[section].length };
  }

  generate(options = {}) {
    const format = options.format || 'markdown';
    const intro = options.intro || '';
    if (format === 'markdown') return this._generateMarkdown(intro);
    if (format === 'html') return this._generateHTML(intro);
    return this._generateText(intro);
  }

  clear() { this.sections = {}; this._saveItems(); }

  _generateMarkdown(intro) {
    let md = `# ${this.name}\n*${new Date().toLocaleDateString()}*\n\n`;
    if (intro) md += intro + '\n\n';
    for (const [section, items] of Object.entries(this.sections)) {
      md += `## ${section}\n\n`;
      for (const item of items) {
        md += item.url ? `- [${item.title}](${item.url})` : `- ${item.title}`;
        if (item.note) md += ` — ${item.note}`;
        md += '\n';
      }
      md += '\n';
    }
    return md;
  }

  _esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  _generateHTML(intro) {
    let html = `<h1>${this._esc(this.name)}</h1><p><em>${new Date().toLocaleDateString()}</em></p>`;
    if (intro) html += `<p>${this._esc(intro)}</p>`;
    for (const [section, items] of Object.entries(this.sections)) {
      html += `<h2>${this._esc(section)}</h2><ul>`;
      for (const item of items) {
        const safeUrl = item.url && /^https?:\/\//i.test(item.url) ? item.url : null;
        html += `<li>${safeUrl ? `<a href="${this._esc(safeUrl)}">${this._esc(item.title)}</a>` : this._esc(item.title)}`;
        if (item.note) html += ` — ${this._esc(item.note)}`;
        html += '</li>';
      }
      html += '</ul>';
    }
    return html;
  }

  _generateText(intro) {
    let text = `${this.name} — ${new Date().toLocaleDateString()}\n\n`;
    if (intro) text += intro + '\n\n';
    for (const [section, items] of Object.entries(this.sections)) {
      text += `=== ${section} ===\n`;
      for (const item of items) {
        text += `• ${item.title}`;
        if (item.url) text += ` (${item.url})`;
        if (item.note) text += ` — ${item.note}`;
        text += '\n';
      }
      text += '\n';
    }
    return text;
  }

  _loadItems() { try { this.sections = JSON.parse(fs.readFileSync(this.dataFile, 'utf8')); } catch {} }
  _saveItems() { try { fs.writeFileSync(this.dataFile, JSON.stringify(this.sections, null, 2)); } catch {} }
}

module.exports = { NewsletterKit };
