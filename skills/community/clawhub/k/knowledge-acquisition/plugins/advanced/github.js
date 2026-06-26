// 插件元数据
const pluginMeta = {
  "name": "github",
  "version": "1.0.0",
  "capabilities": [
    "advanced"
  ],
  "tier": "advanced",
  "supportedPlatforms": [
    "github"
  ],
  "features": [
    "repo-extraction",
    "readme-analysis",
    "project-info"
  ],
  "description": "GitHub项目信息提取",
  "dependencies": [
    "axios"
  ]
};

// GitHub 趋势项目获取插件
const fetch = require('node-fetch');

class GitHub {
  constructor(options = {}) {
    this.supportedPlatforms = ["github"];
    this.token = options.token; // GitHub Personal Access Token
    this.baseUrl = 'https://api.github.com';
    this.headers = {
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'smart-auto-note'
    };

    if (this.token) {
      this.headers['Authorization'] = `token ${this.token}`;
    }
  }

  /**
   * 获取 GitHub Trending 项目
   * @param {string} language 编程语言
   * @param {string} timeRange 时间范围 (daily, weekly, monthly)
   */
  async getTrending(language = '', timeRange = 'daily') {
    try {
      // GitHub 没有官方的 Trending API，需要爬取趋势页面
      const url = `https://github.com/trending/${language}?since=${timeRange}`;
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
      });

      const html = await response.text();
      return this.parseTrendingHTML(html);
    } catch (error) {
      console.error('获取 GitHub Trending 失败:', error);
      return [];
    }
  }

  /**
   * 获取指定仓库详细信息
   * @param {string} owner 仓库所有者
   * @param {string} repo 仓库名称
   */
  async getRepository(owner, repo) {
    try {
      const url = `${this.baseUrl}/repos/${owner}/${repo}`;
      const response = await fetch(url, { headers: this.headers });

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const data = await response.json();

      return {
        name: data.name,
        fullName: data.full_name,
        description: data.description,
        url: data.html_url,
        cloneUrl: data.clone_url,
        language: data.language,
        stars: data.stargazers_count,
        forks: data.forks_count,
        issues: data.open_issues_count,
        createdAt: data.created_at,
        updatedAt: data.updated_at,
        pushedAt: data.pushed_at,
        topics: data.topics,
        owner: {
          name: data.owner.login,
          type: data.owner.type,
          avatar: data.owner.avatar_url
        },
        license: data.license?.name,
        source: 'github',
        type: 'repository'
      };
    } catch (error) {
      console.error('获取仓库信息失败:', error);
      return null;
    }
  }

  /**
   * 获取仓库的 README 内容
   * @param {string} owner 仓库所有者
   * @param {string} repo 仓库名称
   */
  async getReadme(owner, repo) {
    try {
      const url = `${this.baseUrl}/repos/${owner}/${repo}/readme`;
      const response = await fetch(url, { headers: this.headers });

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const data = await response.json();
      const content = Buffer.from(data.content, 'base64').toString('utf-8');

      return {
        content: content,
        url: data.html_url
      };
    } catch (error) {
      console.error('获取 README 失败:', error);
      return null;
    }
  }

  /**
   * 获取仓库的 Release
   * @param {string} owner 仓库所有者
   * @param {string} repo 仓库名称
   */
  async getReleases(owner, repo) {
    try {
      const url = `${this.baseUrl}/repos/${owner}/${repo}/releases`;
      const response = await fetch(url, { headers: this.headers });

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const releases = await response.json();
      return releases.map(release => ({
        tagName: release.tag_name,
        name: release.name,
        description: release.body,
        author: release.author.login,
        publishedAt: release.published_at,
        downloadUrl: release.zipball_url,
        assets: release.assets.map(asset => ({
          name: asset.name,
          size: asset.size,
          downloadCount: asset.download_count,
          url: asset.browser_download_url
        }))
      }));
    } catch (error) {
      console.error('获取 Release 列表失败:', error);
      return [];
    }
  }

  /**
   * 解析 Trending 页面 HTML
   * @param {string} html 页面 HTML
   */
  parseTrendingHTML(html) {
    const repositories = [];

    // 使用正则表达式提取仓库信息（实际项目中建议使用 cheerio 等库解析）
    const repoRegex = /<article[\s\S]*?<h2[\s\S]*?href=\"\/([^""]+)\/([^""]+)\"[\s\S]*?title=\"([^\"]+)\"[\s\S]*?<p class=\"col-9[^>]*>([^<]*)<\/p>[\s\S]*?aria-label=\"star\">([^<]+)<\/a>[\s\S]*?aria-label=\"fork\">([^<]+)<\/a>[\s\S]*?<span class=\"d-inline-block[^>]*>([^<]+)<\/span>/g;

    let match;
    while ((match = repoRegex.exec(html)) !== null) {
      repositories.push({
        owner: match[1],
        name: match[2],
        fullName: `${match[1]}/${match[2]}`,
        description: match[4].trim(),
        url: `https://github.com/${match[1]}/${match[2]}`,
        stars: this.parseNumber(match[5]),
        forks: this.parseNumber(match[6]),
        language: match[7].trim(),
        source: 'github',
        type: 'trending'
      });
    }

    return repositories;
  }

  parseNumber(str) {
    // 解析类似 "123.4k" 的数字
    const num = parseFloat(str);
    if (str.includes('k')) return Math.round(num * 1000);
    return Math.round(num);
  }
}

module.exports = GitHub;