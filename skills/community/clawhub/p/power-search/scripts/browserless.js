const fetch = require('node-fetch');
const cheerio = require('cheerio');

class Browserless {
  constructor(host = 'http://localhost', port = 3000) {
    this.baseUrl = `${host}:${port}`;
  }

  async fetchContent(url, timeout = 10000) {
    try {
      const response = await fetch(`${this.baseUrl}/content`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url,
          rejectResourceTypes: ['stylesheet', 'font', 'media', 'image'],
        }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Browserless error: ${response.status} - ${text}`);
      }

      const text = await response.text();
      return this.extractText(text);
    } catch (error) {
      throw new Error(`Failed to fetch ${url}: ${error.message}`);
    }
  }

  extractText(html) {
    try {
      const $ = cheerio.load(html);
      
      // Remove script and style tags
      $('script, style, noscript').remove();
      
      // Get text and clean it up
      let text = $.text();
      text = text.replace(/\s+/g, ' ').trim();
      
      return text.substring(0, 500); // Return first 500 chars as preview
    } catch (error) {
      return `Error extracting text: ${error.message}`;
    }
  }
}

module.exports = Browserless;
