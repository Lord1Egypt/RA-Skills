/**
 * fetch.js - 内容抓取模块
 * 
 * 负责从各种平台抓取内容
 * 支持：小红书、B 站、知乎、YouTube、通用网页
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

// 平台识别规则
const PLATFORM_RULES = {
  xiaohongshu: {
    patterns: [/xiaohongshu\.com/i, /xhslink\.com/i],
    name: '小红书'
  },
  bilibili: {
    patterns: [/bilibili\.com/i, /b23\.tv/i],
    name: 'B 站'
  },
  zhihu: {
    patterns: [/zhihu\.com/i, /zhuanlan\.zhihu\.com/i],
    name: '知乎'
  },
  youtube: {
    patterns: [/youtube\.com/i, /youtu\.be/i],
    name: 'YouTube'
  },
  weibo: {
    patterns: [/weibo\.com/i, /m\.weibo\.cn/i],
    name: '微博'
  },
  'mp.weixin': {
    patterns: [/mp\.weixin\.qq\.com/i],
    name: '微信公众号'
  }
};

/**
 * 识别链接所属平台
 * @param {string} url - 待识别的 URL
 * @returns {Object} 平台信息 {id, name}
 */
function identifyPlatform(url) {
  for (const [platformId, config] of Object.entries(PLATFORM_RULES)) {
    for (const pattern of config.patterns) {
      if (pattern.test(url)) {
        return { id: platformId, name: config.name };
      }
    }
  }
  return { id: 'generic', name: '网页' };
}

/**
 * 获取网页内容
 * @param {string} url - 目标 URL
 * @returns {Promise<string>} 网页 HTML 内容
 */
function fetchHtml(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
      }
    };
    
    const req = protocol.get(url, options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        resolve(data);
      });
    });
    
    req.on('error', (err) => {
      reject(err);
    });
    
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('请求超时'));
    });
  });
}

/**
 * 提取网页元数据
 * @param {string} html - 网页 HTML
 * @param {string} url - 原始 URL
 * @returns {Object} 元数据对象
 */
function extractMetadata(html, url) {
  const metadata = {
    title: '',
    description: '',
    content: '',
    keywords: [],
    author: '',
    publishDate: '',
    platform: identifyPlatform(url)
  };
  
  // 提取标题
  const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  if (titleMatch) {
    metadata.title = titleMatch[1].trim();
  }
  
  // 提取描述
  const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']+)["'][^>]*>/i) ||
                    html.match(/<meta[^>]*content=["']([^"']+)["'][^>]*name=["']description["'][^>]*>/i);
  if (descMatch) {
    metadata.description = descMatch[1].trim();
  }
  
  // 提取关键词
  const keywordsMatch = html.match(/<meta[^>]*name=["']keywords["'][^>]*content=["']([^"']+)["'][^>]*>/i) ||
                        html.match(/<meta[^>]*content=["']([^"']+)["'][^>]*name=["']keywords["'][^>]*>/i);
  if (keywordsMatch) {
    metadata.keywords = keywordsMatch[1].split(/[,，]/).map(k => k.trim()).filter(k => k);
  }
  
  // 提取作者
  const authorMatch = html.match(/<meta[^>]*name=["']author["'][^>]*content=["']([^"']+)["'][^>]*>/i) ||
                      html.match(/<meta[^>]*content=["']([^"']+)["'][^>]*name=["']author["'][^>]*>/i);
  if (authorMatch) {
    metadata.author = authorMatch[1].trim();
  }
  
  // 提取正文内容（简化版，移除标签）
  const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
  if (bodyMatch) {
    let content = bodyMatch[1];
    // 移除脚本和样式
    content = content.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
    content = content.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
    // 移除 HTML 标签
    content = content.replace(/<[^>]+>/g, ' ');
    // 清理空白
    content = content.replace(/\s+/g, ' ').trim();
    // 限制长度
    if (content.length > 5000) {
      content = content.substring(0, 5000) + '...';
    }
    metadata.content = content;
  }
  
  return metadata;
}

/**
 * 针对特定平台的抓取策略
 */
const PLATFORM_STRATEGIES = {
  bilibili: {
    async fetch(url) {
      const html = await fetchHtml(url);
      const metadata = extractMetadata(html, url);
      
      // B 站特殊处理：尝试提取视频信息
      const videoIdMatch = url.match(/BV\w+/i) || url.match(/av\d+/i);
      if (videoIdMatch) {
        metadata.videoId = videoIdMatch[0];
      }
      
      // 尝试提取 UP 主信息
      const upMatch = html.match(/"name":"([^"]+)"/i);
      if (upMatch) {
        metadata.uploader = upMatch[1];
      }
      
      return metadata;
    }
  },
  
  zhihu: {
    async fetch(url) {
      const html = await fetchHtml(url);
      const metadata = extractMetadata(html, url);
      
      // 知乎特殊处理：尝试提取问题和回答
      const questionMatch = html.match(/<h1[^>]*class="QuestionHeader-title"[^>]*>([^<]+)<\/h1>/i);
      if (questionMatch) {
        metadata.question = questionMatch[1].trim();
      }
      
      return metadata;
    }
  },
  
  youtube: {
    async fetch(url) {
      const html = await fetchHtml(url);
      const metadata = extractMetadata(html, url);
      
      // YouTube 特殊处理：提取视频 ID
      const videoIdMatch = url.match(/(?:v=|\/)([a-zA-Z0-9_-]{11})(?:\?|&|\/|$)/i);
      if (videoIdMatch) {
        metadata.videoId = videoIdMatch[1];
      }
      
      return metadata;
    }
  },
  
  xiaohongshu: {
    async fetch(url) {
      const html = await fetchHtml(url);
      const metadata = extractMetadata(html, url);
      
      // 小红书特殊处理：尝试提取标签
      const tagMatches = html.match(/#[^#\s]+/g) || [];
      if (tagMatches.length > 0) {
        metadata.tags = tagMatches.slice(0, 10);
      }
      
      return metadata;
    }
  },
  
  generic: {
    async fetch(url) {
      const html = await fetchHtml(url);
      return extractMetadata(html, url);
    }
  }
};

/**
 * 主抓取函数
 * @param {string} url - 目标 URL
 * @returns {Promise<Object>} 抓取结果
 */
async function fetchContent(url) {
  try {
    const platform = identifyPlatform(url);
    const strategy = PLATFORM_STRATEGIES[platform.id] || PLATFORM_STRATEGIES.generic;
    
    console.log(`正在抓取 ${platform.name} 内容：${url}`);
    
    const result = await strategy.fetch(url);
    result.url = url;
    result.fetchTime = new Date().toISOString();
    
    return result;
  } catch (error) {
    console.error(`抓取失败：${error.message}`);
    throw error;
  }
}

// 导出模块
module.exports = {
  fetchContent,
  identifyPlatform,
  fetchHtml,
  extractMetadata,
  PLATFORM_RULES,
  PLATFORM_STRATEGIES
};

// CLI 模式支持
if (require.main === module) {
  const url = process.argv[2];
  if (!url) {
    console.error('用法：node fetch.js <URL>');
    process.exit(1);
  }
  
  fetchContent(url)
    .then(result => {
      console.log('\n=== 抓取结果 ===');
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(err => {
      console.error('错误:', err.message);
      process.exit(1);
    });
}
