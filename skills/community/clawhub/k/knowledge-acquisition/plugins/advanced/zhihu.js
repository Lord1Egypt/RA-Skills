// 插件元数据
const pluginMeta = {
  "name": "zhihu",
  "version": "1.0.0",
  "capabilities": [
    "advanced"
  ],
  "tier": "advanced",
  "supportedPlatforms": [
    "zhihu"
  ],
  "features": [
    "content-extraction",
    "advanced-classification",
    "qa-content"
  ],
  "description": "知乎内容提取",
  "dependencies": [
    "axios",
    "cheerio"
  ]
};

// 知乎内容获取插件
const fetch = require('node-fetch');

class ZhiHu {
  constructor(options = {}) {
    this.supportedPlatforms = ["zhihu"];
    this.cookie = options.cookie; // 可能需要登录凭证
    this.baseUrl = 'https://www.zhihu.com/api/v4';
  }

  /**
   * 获取热门问题列表
   * @param {number} limit 数量限制
   */
  async getHotQuestions(limit = 20) {
    try {
      const url = `${this.baseUrl}/search/hot_list?limit=${limit}`;
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
          'Cookie': this.cookie
        }
      });

      const data = await response.json();

      return data.data.map(item => ({
        title: item.target.title || item.target.question?.title,
        excerpt: item.target.excerpt || item.target.question?.excerpt,
        url: `https://www.zhihu.com/question/${item.target.id}`,
        score: item.detail_text || `${item.hot} 热度`,
        publishTime: new Date(item.created_time * 1000),
        tags: this.extractTags(item.target.question?.topics),
        source: 'zhihu',
        type: 'question'
      }));
    } catch (error) {
      console.error('获取知乎热门问题失败:', error);
      return [];
    }
  }

  /**
   * 获取指定用户的回答
   * @param {string} userId 用户ID
   * @param {number} limit 数量限制
   */
  async getUserAnswers(userId, limit = 20) {
    try {
      const url = `${this.baseUrl}/people/${userId}/answers?include=data[*].content&limit=${limit}`;
      const response = await fetch(url, {
        headers: this.getHeaders()
      });

      const data = await response.json();

      return data.data.map(item => ({
        title: item.question.title,
        content: item.content,
        excerpt: this.extractExcerpt(item.content),
        url: `https://www.zhihu.com/question/${item.question.id}/answer/${item.id}`,
        voteupCount: item.voteup_count,
        publishTime: new Date(item.created_time * 1000),
        tags: this.extractTags(item.question.topics),
        source: 'zhihu',
        type: 'answer',
        author: item.author.name
      }));
    } catch (error) {
      console.error('获取知乎用户回答失败:', error);
      return [];
    }
  }

  /**
   * 获取专栏文章
   * @param {string} columnId 专栏ID
   */
  async getColumnArticles(columnId) {
    // 实现专栏文章获取
    return [];
  }

  extractExcerpt(content) {
    if (!content) return '';
    // 移除HTML标签，提取前200字符
    const text = content.replace(/<[^>]+>/g, '');
    return text.slice(0, 200) + '...';
  }

  extractTags(topics) {
    if (!topics || !Array.isArray(topics)) return [];
    return topics.map(topic => topic.name);
  }

  getHeaders() {
    return {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
      'Cookie': this.cookie || ''
    };
  }
}

module.exports = ZhiHu;