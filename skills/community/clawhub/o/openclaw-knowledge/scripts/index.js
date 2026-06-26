import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const VAULT_DIR = path.join(__dirname, '..', 'docs');
const INDEX_PATH = path.join(__dirname, 'vault-index.json');

export class Indexer {
  async buildIndex() {
    const documents = [];
    const categories = ['automation', 'channels', 'cli', 'concepts', 'gateway',
                       'guides', 'help', 'install', 'nodes', 'platforms',
                       'plugins', 'providers', 'reference', 'root', 'security',
                       'start', 'tools', 'web'];

    for (const category of categories) {
      const categoryPath = path.join(VAULT_DIR, category);
      try {
        const files = await fs.readdir(categoryPath);
        const mdFiles = files.filter(f => f.endsWith('.md'));

        for (const file of mdFiles) {
          const filePath = path.join(categoryPath, file);
          const doc = await this.processFile(filePath, category);
          if (doc) documents.push(doc);
        }
      } catch (err) {
        if (err.code !== 'ENOENT') console.error(`Error reading ${category}: ${err.message}`);
      }
    }

    const index = {
      indexVersion: '1.0',
      lastUpdated: new Date().toISOString(),
      totalDocuments: documents.length,
      documents
    };

    await fs.writeFile(INDEX_PATH, JSON.stringify(index, null, 2), 'utf-8');
    console.log(`Index built: ${documents.length} documents`);
    return index;
  }

  async processFile(filePath, category) {
    const content = await fs.readFile(filePath, 'utf-8');
    const relativePath = path.relative(VAULT_DIR, filePath);
    const fileName = path.basename(filePath, '.md');

    const frontmatter = this.extractFrontmatter(content);
    const title = frontmatter.title || fileName;

    const cleanContent = this.cleanContent(content);
    const headings = this.extractHeadings(cleanContent);
    const summary = this.extractSummary(cleanContent);
    const tags = this.extractTags(cleanContent, headings, title);

    return {
      id: `${category}/${fileName}`,
      path: relativePath.replace(/\\/g, '/'),
      title,
      category,
      tags,
      headings,
      summary,
      contentHash: crypto.createHash('md5').update(content).digest('hex').substring(0, 8)
    };
  }

  cleanContent(content) {
    return content
      .replace(/<AgentInstructions>[\s\S]*?<\/AgentInstructions>/gi, '')
      .replace(/^>\s*##\s*Documentation Index[\s\S]*?(?=\n#)/gm, '')
      .replace(/^\s*<!--[\s\S]*?-->\s*$/gm, '')
      .replace(/^>\s*##\s*Submitting Feedback[\s\S]*$/gm, '')
      .trim();
  }

  extractFrontmatter(content) {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return {};
    const frontmatter = {};
    for (const line of match[1].split('\n')) {
      const idx = line.indexOf(':');
      if (idx > 0) {
        const key = line.substring(0, idx).trim();
        let value = line.substring(idx + 1).trim().replace(/^["']|["']$/g, '');
        frontmatter[key] = value;
      }
    }
    return frontmatter;
  }

  extractHeadings(content) {
    const headings = [];
    const regex = /^#{1,6}\s+(.+)$/gm;
    let match;
    while ((match = regex.exec(content)) !== null) headings.push(match[1].trim());
    return headings;
  }

  extractSummary(content) {
    const lines = content.split('\n');
    let bodyStart = 0;

    const frontmatterMatch = content.match(/^---\n[\s\S]*?\n---\n?/);
    if (frontmatterMatch) {
      bodyStart = frontmatterMatch[0].length;
    }

    let afterTitle = false;
    let summaryLines = [];

    for (let i = bodyStart; i < lines.length; i++) {
      const line = lines[i];

      if (line.startsWith('#')) {
        afterTitle = true;
        continue;
      }

      if (afterTitle) {
        if (line.trim() === '' || line.startsWith('>') || line.startsWith('<!--')) {
          continue;
        }

        const textLine = line.replace(/<[^>]+>/g, '').replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/[#*`_~]/g, '').trim();
        if (textLine.length > 10) {
          summaryLines.push(textLine);
          if (summaryLines.length >= 3) break;
        }
      }
    }

    const summary = summaryLines.join(' ').replace(/\s+/g, ' ').trim();
    return summary.substring(0, 300);
  }

  extractTags(content, headings, title) {
    const tags = new Set();
    const frontmatter = this.extractFrontmatter(content);
    if (frontmatter.tags) {
      frontmatter.tags.replace(/[\[\]]/g, '').split(',').forEach(t => tags.add(t.trim()));
    }
    title.split(/[\s\-_]+/).forEach(w => { if (w.length > 2) tags.add(w.toLowerCase()); });
    headings.forEach(h => h.split(/[\s\-_]+/).forEach(w => { if (w.length > 3) tags.add(w.toLowerCase()); }));
    return Array.from(tags).slice(0, 20);
  }

  stripMarkdown(content) {
    return content
      .replace(/^---[\s\S]*?---\n?/, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .replace(/[#*`_~\[\]]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }
}

export class Searcher {
  constructor() {
    this.index = null;
  }

  async loadIndex() {
    if (this.index) return this.index;
    try {
      const data = await fs.readFile(INDEX_PATH, 'utf-8');
      this.index = JSON.parse(data);
      return this.index;
    } catch (err) {
      if (err.code === 'ENOENT') throw new Error('Index not found. Run: npm run reindex');
      throw err;
    }
  }

  async search(query, options = {}) {
    const { category, limit = 10, format = 'text' } = options;
    const index = await this.loadIndex();
    const queryTerms = query.toLowerCase().split(/\s+/).filter(t => t.length > 0);
    const results = [];

    for (const doc of index.documents) {
      if (category && doc.category !== category) continue;
      const score = this.calculateScore(doc, queryTerms);
      if (score > 0) {
        results.push({
          path: doc.path,
          title: doc.title,
          category: doc.category,
          score,
          summary: doc.summary,
          matchedTerms: this.getMatchedTerms(doc, queryTerms)
        });
      }
    }

    results.sort((a, b) => b.score - a.score);
    const limited = results.slice(0, limit);

    if (format === 'json') {
      return { query, total: results.length, returned: limited.length, results: limited };
    }

    return this.formatText(query, limited);
  }

  calculateScore(doc, queryTerms) {
    let score = 0;
    const titleLower = doc.title.toLowerCase();
    const categoryLower = doc.category.toLowerCase();
    const tagsLower = doc.tags.map(t => t.toLowerCase());
    const headingsStr = doc.headings.join(' ').toLowerCase();
    const summaryLower = doc.summary.toLowerCase();

    for (const term of queryTerms) {
      if (titleLower.includes(term)) score += 10;
      if (categoryLower.includes(term)) score += 2;
      if (tagsLower.some(t => t.includes(term))) score += 5;
      if (headingsStr.includes(term)) score += 3;
      if (summaryLower.includes(term)) score += 1;
    }

    const allTerms = titleLower + ' ' + tagsLower.join(' ') + ' ' + headingsStr + ' ' + summaryLower;
    const matchRatio = queryTerms.filter(t => allTerms.includes(t)).length / queryTerms.length;
    score *= (0.5 + matchRatio * 0.5);
    return score;
  }

  getMatchedTerms(doc, queryTerms) {
    const text = (doc.title + ' ' + doc.tags.join(' ') + ' ' + doc.headings.join(' ') + ' ' + doc.summary).toLowerCase();
    return queryTerms.filter(t => text.includes(t));
  }

  formatText(query, results) {
    if (results.length === 0) return `No results found for: "${query}"\n`;
    let output = `Search results for: "${query}"\nFound ${results.length} result(s)\n\n`;
    for (const r of results) {
      output += `📄 ${r.path}\n   Title: ${r.title}\n   Category: ${r.category}\n   Score: ${r.score.toFixed(2)}\n`;
      if (r.summary) {
        const short = r.summary.length > 150 ? r.summary.substring(0, 150) + '...' : r.summary;
        output += `   Summary: ${short}\n`;
      }
      output += '\n';
    }
    return output;
  }

  async listCategories() {
    const index = await this.loadIndex();
    const categories = {};
    for (const doc of index.documents) {
      categories[doc.category] = (categories[doc.category] || 0) + 1;
    }
    return categories;
  }
}
