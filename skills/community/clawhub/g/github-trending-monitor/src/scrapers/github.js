const axios = require('axios');
const cheerio = require('cheerio');

/**
 * GitHub Trending Scraper
 *
 * Fetches trending repositories from GitHub by scraping the trending page
 * or using the GitHub API as fallback.
 */
class GitHubTrendingScraper {
  constructor(githubToken = null) {
    this.githubToken = githubToken;
    this.baseURL = 'https://github.com';
    this.headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5'
    };
  }

  /**
   * Get trending repositories
   * @param {string} language - Programming language filter (optional)
   * @param {string} since - Time range: daily, weekly, monthly
   * @returns {Promise<Array>}
   */
  async getTrending(language = '', since = 'daily') {
    try {
      const url = this.buildURL(language, since);
      const response = await axios.get(url, { headers: this.headers });
      const repos = this.parse(response.data);

      if (repos.length === 0) {
        console.warn('No repos parsed from page, trying fallback...');
        return await this.getFallback(language, since);
      }

      return repos;
    } catch (error) {
      console.error('GitHub trending scrape failed:', error.message);
      return await this.getFallback(language, since);
    }
  }

  /**
   * Build the trending page URL
   */
  buildURL(language, since) {
    let url = `${this.baseURL}/trending`;
    if (language) url += `/${encodeURIComponent(language.toLowerCase())}`;
    url += `?since=${since}`;
    return url;
  }

  /**
   * Parse HTML response from GitHub trending page
   */
  parse(html) {
    const $ = cheerio.load(html);
    const repos = [];

    $('article.Box-row').each((index, element) => {
      try {
        const $el = $(element);

        // Extract author and repo name
        const titleEl = $el.find('h2 a');
        const titleText = titleEl.attr('href') || '';
        const parts = titleText.replace(/^\//, '').split('/');
        const author = parts[0] || '';
        const name = parts[1] || '';

        // Extract description
        const description = $el.find('p').first().text().trim();

        // Extract language
        const language = $el.find('[itemprop="programmingLanguage"]').text().trim();

        // Extract stars
        const starsText = $el.find('a[href$="/stargazers"]').first().text().trim().replace(/,/g, '');
        const stars = parseInt(starsText, 10) || 0;

        // Extract forks
        const forksText = $el.find('a[href$="/forks"]').first().text().trim().replace(/,/g, '');
        const forks = parseInt(forksText, 10) || 0;

        // Extract today's stars
        const todayText = $el.find('.d-inline-block.float-sm-right').text().trim();
        const todayMatch = todayText.match(/([\d,]+)\s+stars? today/i);
        const todayStars = todayMatch ? parseInt(todayMatch[1].replace(/,/g, ''), 10) : 0;

        if (author && name) {
          repos.push({
            rank: index + 1,
            author,
            name,
            fullName: `${author}/${name}`,
            description: description || 'No description provided.',
            language: language || 'Unknown',
            stars,
            forks,
            todayStars,
            url: `${this.baseURL}/${author}/${name}`
          });
        }
      } catch (err) {
        // Skip malformed entries
      }
    });

    return repos;
  }

  /**
   * Fallback using GitHub Search API
   */
  async getFallback(language, since) {
    try {
      const dateMap = { daily: 1, weekly: 7, monthly: 30 };
      const days = dateMap[since] || 1;
      const date = new Date();
      date.setDate(date.getDate() - days);
      const dateStr = date.toISOString().split('T')[0];

      let query = `created:>${dateStr}`;
      if (language) query += ` language:${language}`;

      const headers = { 'Accept': 'application/vnd.github.v3+json' };
      if (this.githubToken) {
        headers['Authorization'] = `token ${this.githubToken}`;
      }

      const response = await axios.get('https://api.github.com/search/repositories', {
        params: { q: query, sort: 'stars', order: 'desc', per_page: 25 },
        headers
      });

      return response.data.items.map((repo, index) => ({
        rank: index + 1,
        author: repo.owner.login,
        name: repo.name,
        fullName: repo.full_name,
        description: repo.description || 'No description provided.',
        language: repo.language || 'Unknown',
        stars: repo.stargazers_count,
        forks: repo.forks_count,
        todayStars: 0,
        url: repo.html_url
      }));
    } catch (error) {
      console.error('GitHub API fallback failed:', error.message);
      return [];
    }
  }

  /**
   * Get trending by multiple languages at once
   * @param {string[]} languages - List of languages
   * @param {string} since - Time range
   */
  async getTrendingMultiple(languages, since = 'daily') {
    const results = {};
    for (const lang of languages) {
      results[lang || 'all'] = await this.getTrending(lang, since);
    }
    return results;
  }
}

module.exports = GitHubTrendingScraper;
