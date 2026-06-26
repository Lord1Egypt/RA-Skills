#!/usr/bin/env node
/**
 * Letundra News Parser
 * Fetches news from letundra.com via RSS feed
 *
 * Usage:
 *   node letundra_yandex.js news [limit]
 *   node letundra_yandex.js news --limit=20
 *   node letundra_yandex.js test
 *
 * Note: This script uses the site's public RSS feed endpoint.
 * For AI assistants, use web_fetch instead.
 */

const https = require('https');

// Simple XML parser for RSS
class RSSParser {
  static decodeHtmlEntities(str) {
    if (!str) return '';
    return str
      .replace(/&#8212;/g, '—')
      .replace(/&#8211;/g, '–')
      .replace(/&#8220;/g, '"')
      .replace(/&#8221;/g, '"')
      .replace(/&#171;/g, '"')
      .replace(/&#187;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&#x27;/g, "'");
  }

  static parse(xmlString) {
    const result = { items: [], channel: {} };

    const titleMatch = xmlString.match(/<channel>[\s\S]*?<title>([^<]+)<\/title>/);
    if (titleMatch) result.channel.title = titleMatch[1];

    const linkMatch = xmlString.match(/<channel>[\s\S]*?<link>(https?:\/\/[^<]+)<\/link>/);
    if (linkMatch) result.channel.link = linkMatch[1];

    const descMatch = xmlString.match(/<channel>[\s\S]*?<description>([^<]+)<\/description>/);
    if (descMatch) result.channel.description = descMatch[1];

    const itemRegex = /<item[^>]*>([\s\S]*?)<\/item>/g;
    let match;
    while ((match = itemRegex.exec(xmlString)) !== null) {
      const itemXml = match[1];
      const item = {};

      let titleMatch = itemXml.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/);
      if (titleMatch) item.title = this.decodeHtmlEntities(titleMatch[1].trim());
      else {
        titleMatch = itemXml.match(/<title>([^<]+)<\/title>/);
        if (titleMatch) item.title = this.decodeHtmlEntities(titleMatch[1].trim());
      }

      const linkMatch = itemXml.match(/<link>(https?:\/\/[^<]+)<\/link>/);
      if (linkMatch) item.link = linkMatch[1];

      let descMatch = itemXml.match(/<description><!\[CDATA\[([\s\S]*?)\]\]><\/description>/);
      if (descMatch) item.description = this.decodeHtmlEntities(descMatch[1].trim());
      else {
        descMatch = itemXml.match(/<description>([^<]+)<\/description>/);
        if (descMatch) item.description = this.decodeHtmlEntities(descMatch[1].trim());
      }

      const pubDateMatch = itemXml.match(/<pubDate>([^<]+)<\/pubDate>/);
      if (pubDateMatch) item.pubDate = pubDateMatch[1];

      const categoryMatches = itemXml.match(/<category>([^<]+)<\/category>/g);
      if (categoryMatches) {
        item.categories = categoryMatches.map(c => c.replace(/<\/?category>/g, ''));
      }

      if (item.title) result.items.push(item);
    }

    return result;
  }
}

class LetundraNewsParser {
  constructor() {
    this.feedUrl = 'https://letundra.com/?yandex_feed=news';
  }

  async fetch(url) {
    return new Promise((resolve, reject) => {
      const req = https.get(url, {
        headers: {
          'User-Agent': 'Letundra-NewsReader/1.0 (+https://letundra.com)',
          'Accept': 'application/rss+xml, application/xml, text/xml',
          'Accept-Language': 'ru-RU,en-US;q=0.7',
        },
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          if (res.statusCode >= 400) {
            reject(new Error(`HTTP ${res.statusCode}`));
          } else {
            resolve(data);
          }
        });
      });
      req.on('error', reject);
      req.setTimeout(15000, () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });
    });
  }

  async getNews(limit = 10) {
    const xml = await this.fetch(this.feedUrl);
    const parsed = RSSParser.parse(xml);
    return this.formatNews(parsed.items.slice(0, limit));
  }

  formatNews(items) {
    return items.map((item, index) => ({
      number: index + 1,
      title: item.title || 'No title',
      link: item.link || '',
      description: this.stripHtml(item.description || ''),
      pubDate: this.formatDate(item.pubDate || ''),
      categories: item.categories || [],
    }));
  }

  stripHtml(html) {
    return html
      .replace(/<[^>]+>/g, '')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&#171;/g, '"')
      .replace(/&#187;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&#8212;/g, '—')
      .replace(/&#8220;/g, '"')
      .replace(/&#8221;/g, '"')
      .trim()
      .substring(0, 500);
  }

  formatDate(dateStr) {
    if (!dateStr) return '';
    try {
      const date = new Date(dateStr);
      if (isNaN(date.getTime())) return dateStr;
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      });
    } catch (e) {
      return dateStr;
    }
  }

  generateRSS(items) {
    const rssItems = items.map(item => {
      const categories = item.categories.map(c => `      <category>${this.escapeXml(c)}</category>`).join('\n');
      return `    <item>
      <title>${this.escapeXml(item.title)}</title>
      <link>${this.escapeXml(item.link)}</link>
      <description><![CDATA[${item.description}]]></description>
      <pubDate>${item.pubDate}</pubDate>
${categories}
    </item>`;
    }).join('\n');

    return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Letundra News</title>
    <link>https://letundra.com/ru/news/</link>
    <description>Travel news from Letundra.com</description>
    <language>ru</language>
${rssItems}
  </channel>
</rss>`;
  }

  escapeXml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  async test() {
    console.log('Testing RSS feed...\n');
    try {
      const xml = await this.fetch(this.feedUrl);
      const parsed = RSSParser.parse(xml);
      console.log('Success! Items:', parsed.items.length);
      if (parsed.items.length > 0) {
        console.log('First:', parsed.items[0].title?.substring(0, 60));
      }
      return { success: true, items: parsed.items.length };
    } catch (error) {
      console.log('Error:', error.message);
      return { success: false, error: error.message };
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  const parser = new LetundraNewsParser();
  let limit = 10;

  const limitArg = args.find(a => a.startsWith('--limit='));
  if (limitArg) limit = parseInt(limitArg.split('=')[1]) || 10;

  try {
    switch (args[0]) {
      case 'test':
        const result = await parser.test();
        process.exit(result.success ? 0 : 1);
        break;
      case 'news':
        console.log(JSON.stringify(await parser.getNews(limit), null, 2));
        break;
      case 'news:rss':
        console.log(parser.generateRSS(await parser.getNews(limit)));
        break;
      case 'news:markdown':
        const news = await parser.getNews(limit);
        console.log('# Latest Letundra News\n');
        news.forEach(item => {
          console.log(`## ${item.number}. ${item.title}`);
          console.log(`Date: ${item.pubDate}`);
          if (item.categories.length) console.log(`Tags: ${item.categories.join(', ')}`);
          if (item.description) console.log(`\n${item.description}`);
          console.log(`[Read more](${item.link})\n`);
        });
        break;
      default:
        console.log('Usage: node letundra_yandex.js test|news|news:rss|news:markdown [--limit=N]');
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
