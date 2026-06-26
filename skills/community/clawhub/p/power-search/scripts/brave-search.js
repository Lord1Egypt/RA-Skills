const fetch = require('node-fetch');

class BraveSearch {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://api.search.brave.com/res/v1/web/search';
  }

  async search(query, limit = 10) {
    try {
      const params = new URLSearchParams({
        q: query,
        count: Math.min(limit, 20),
      });

      const response = await fetch(`${this.baseUrl}?${params}`, {
        headers: {
          'Accept': 'application/json',
          'X-Subscription-Token': this.apiKey,
        },
      });

      if (!response.ok) {
        throw new Error(`Brave API error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      // Parse results from nested structure
      const results = (data.web?.results || []).slice(0, limit).map((result, index) => ({
        rank: index + 1,
        title: result.title,
        url: result.url,
        description: result.description,
        age: result.age,
      }));

      return {
        query,
        count: results.length,
        results,
      };
    } catch (error) {
      throw new Error(`Brave Search failed: ${error.message}`);
    }
  }
}

module.exports = BraveSearch;
