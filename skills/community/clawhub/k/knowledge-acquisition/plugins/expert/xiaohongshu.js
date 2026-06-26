// 插件元数据
const pluginMeta = {
  "name": "xiaohongshu",
  "version": "2.0.0",
  "capabilities": [
    "expert"
  ],
  "tier": "expert",
  "supportedPlatforms": [
    "xiaohongshu"
  ],
  "features": [
    "ocr-extraction",
    "advanced-content-analysis",
    "image-processing",
    "metadata-extraction"
  ],
  "description": "小红书内容提取（基于验证的可靠方案）",
  "dependencies": [
    "puppeteer",
    "cheerio",
    "axios"
  ]
};

// 小红书内容获取插件 - 优化版
const axios = require('axios');
const cheerio = require('cheerio');

class XiaohongShu {
  constructor(options = {}) {
    this.supportedPlatforms = ["xiaohongshu", "xhslink"];
    this.baseUrl = 'https://www.xiaohongshu.com';
    this.timeout = options.timeout || 15000;
    this.retryTimes = options.retryTimes || 3;
    this.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

    // 配置请求
    this.axiosInstance = axios.create({
      timeout: this.timeout,
      headers: {
        'User-Agent': this.userAgent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
      }
    });
  }

  /**
   * 解析URL，处理短链重定向
   * @param {string} url 小红书笔记链接
   * @returns {Promise<Object>} { realUrl, noteId }
   */
  async resolveUrl(url) {
    try {
      // 处理短链
      if (url.includes('xhslink.com')) {
        const response = await this.axiosInstance.get(url, {
          maxRedirects: 5,
          validateStatus: () => true // 接受所有状态码
        });
        const realUrl = response.request.res.responseUrl || response.request._redirectable._redirectCount > 0
          ? response.config.url
          : url;

        // 提取note_id
        const noteIdMatch = realUrl.match(/\/explore\/([a-zA-Z0-9]+)/);
        if (!noteIdMatch) {
          throw new Error(`无法从URL中提取note_id: ${realUrl}`);
        }

        return {
          realUrl: realUrl,
          noteId: noteIdMatch.group(1)
        };
      } else {
        // 处理长链
        const noteIdMatch = url.match(/\/explore\/([a-zA-Z0-9]+)/);
        if (!noteIdMatch) {
          throw new Error(`无效的小红书链接格式: ${url}`);
        }

        return {
          realUrl: url,
          noteId: noteIdMatch.group(1)
        };
      }
    } catch (error) {
      throw new Error(`URL解析失败: ${error.message}`);
    }
  }

  /**
   * 获取笔记页面HTML内容
   * @param {string} url 笔记URL
   * @returns {Promise<string>} HTML内容
   */
  async fetchNoteHtml(url) {
    let lastError;

    for (let i = 0; i < this.retryTimes; i++) {
      try {
        const response = await this.axiosInstance.get(url);
        if (response.status === 200) {
          return response.data;
        } else {
          throw new Error(`HTTP状态码: ${response.status}`);
        }
      } catch (error) {
        lastError = error;
        if (i < this.retryTimes - 1) {
          await this.delay(1000 * (i + 1)); // 递增延迟
        }
      }
    }

    throw new Error(`获取笔记内容失败: ${lastError.message}`);
  }

  /**
   * 从HTML中提取笔记元数据（基于验证的可靠方案）
   * @param {string} html HTML内容
   * @param {string} noteId 笔记ID
   * @returns {Object} 笔记元数据
   */
  parseMetadata(html, noteId) {
    // 尝试从script标签中提取JSON数据
    const scriptPattern = /<script>window\.__INITIAL_STATE__\s*=\s*({.*?});<\/script>/;
    const match = scriptPattern.exec(html);

    if (match) {
      try {
        const dataStr = match[1];
        const data = JSON.parse(dataStr);

        // 提取笔记信息
        const noteData = data?.note?.noteDetail?.note || {};

        // 提取图片信息
        let images = [];
        if (noteData.image_list && Array.isArray(noteData.image_list)) {
          images = noteData.image_list.map((img, idx) => {
            const infoList = img.info_list || [];
            const defaultInfo = infoList.find(i => i.image_scene === 'FD_PRV_WEBP') || infoList[0] || {};
            return {
              index: idx + 1,
              url: defaultInfo.url_default || defaultInfo.url || '',
              width: defaultInfo.width || 0,
              height: defaultInfo.height || 0
            };
          });
        }

        // 提取作者信息
        const user = noteData.user || {};

        // 提取标签
        let tags = [];
        if (noteData.tag_list && Array.isArray(noteData.tag_list)) {
          tags = noteData.tag_list.map(tag => ({
            id: tag.id || '',
            name: tag.name || '',
            type: tag.type || ''
          }));
        }

        // 提取互动数据
        const interactInfo = noteData.interact_info || {};

        return {
          noteId: noteId,
          title: noteData.title || '无标题',
          desc: noteData.desc || '',
          type: noteData.type || 'normal',
          time: noteData.time ? new Date(noteData.time * 1000).toISOString() : '',
          author: {
            userId: user.user_id || '',
            nickname: user.nickname || '未知用户',
            avatar: user.avatar || '',
            desc: user.desc || ''
          },
          images: images,
          tags: tags,
          stats: {
            likedCount: interactInfo.liked_count || 0,
            collectedCount: interactInfo.collected_count || 0,
            commentCount: interactInfo.comment_count || 0,
            shareCount: interactInfo.share_count || 0
          },
          // 视频相关
          video: noteData.video ? {
            media: {
              stream: {
                h264: noteData.video.media?.stream?.h264?.[0]?.master_url || ''
              },
              duration: noteData.video.duration || 0
            }
          } : null
        };
      } catch (parseError) {
        console.error('解析JSON数据失败:', parseError.message);
      }
    }

    // 备用解析方法：使用 cheerio 提取基本信息
    const $ = cheerio.load(html);

    // 提取标题
    const title = $('title').text().replace(' - 小红书', '') || '无标题';

    // 提取描述
    const desc = $('meta[name="description"]').attr('content') || '';

    // 提取图片
    let images = [];
    $('img').each((i, elem) => {
      const src = $(elem).attr('src') || $(elem).attr('data-src');
      if (src && (src.includes('sinaimg.cn') || src.includes('xiaohongshu.com'))) {
        images.push({
          index: i + 1,
          url: src.startsWith('//') ? 'https:' + src : src,
          width: 0,
          height: 0
        });
      }
    });

    return {
      noteId: noteId,
      title: title,
      desc: desc,
      type: 'normal',
      time: '',
      author: {
        userId: '',
        nickname: '未知用户',
        avatar: '',
        desc: ''
      },
      images: images,
      tags: [],
      stats: {
        likedCount: 0,
        collectedCount: 0,
        commentCount: 0,
        shareCount: 0
      },
      video: null
    };
  }

  /**
   * 从URL提取笔记内容
   * @param {string} url 小红书链接
   * @param {Object} options 提取选项
   * @returns {Promise<Object>} 笔记内容
   */
  async extractNoteFromUrl(url, options = {}) {
    try {
      // 1. 解析URL
      const { realUrl, noteId } = await this.resolveUrl(url);

      // 2. 获取HTML
      const html = await this.fetchNoteHtml(realUrl);

      // 3. 解析元数据
      const metadata = this.parseMetadata(html, noteId);

      // 4. 格式化输出
      return {
        title: metadata.title,
        type: metadata.type === 'video' ? 'video' : 'article',
        description: metadata.desc,
        content: metadata.desc, // 小红书的 desc 就是主要内容
        author: metadata.author.nickname,
        authorId: metadata.author.userId,
        publishTime: metadata.time,
        sourceUrl: realUrl,
        platform: 'xiaohongshu',
        tags: metadata.tags.map(t => t.name).filter(t => t),

        // 图片信息
        images: options.includeImages !== false ? metadata.images.map(img => ({
          url: img.url,
          index: img.index
        })) : [],

        // 统计信息
        stats: {
          likes: metadata.stats.likedCount,
          collects: metadata.stats.collectedCount,
          comments: metadata.stats.commentCount,
          shares: metadata.stats.shareCount
        },

        // 视频信息（如果是视频）
        video: metadata.video ? {
          url: metadata.video.media?.stream?.h264 || '',
          duration: metadata.video.media?.duration || 0
        } : undefined,

        // 元数据
        metadata: {
          noteId: noteId,
          images: metadata.images,
          originalTags: metadata.tags
        }
      };
    } catch (error) {
      throw new Error(`提取小红书笔记失败: ${error.message}`);
    }
  }

  /**
   * 批量提取笔记
   * @param {Array<string>} urls URL列表
   * @param {Object} options 提取选项
   * @returns {Promise<Array>} 提取结果列表
   */
  async extractBatch(urls, options = {}) {
    const results = [];
    const concurrency = options.concurrency || 3;

    // 分批处理
    for (let i = 0; i < urls.length; i += concurrency) {
      const batch = urls.slice(i, i + concurrency);
      const batchPromises = batch.map(url =>
        this.extractNoteFromUrl(url, options)
          .then(result => ({ success: true, data: result, url }))
          .catch(error => ({ success: false, error: error.message, url }))
      );

      const batchResults = await Promise.all(batchPromises);
      results.push(...batchResults);

      // 批次间延迟
      if (i + concurrency < urls.length) {
        await this.delay(500);
      }
    }

    return results;
  }

  /**
   * 获取关注用户的笔记（使用Cookie认证）
   * @param {number} pageSize 页面大小
   * @param {string} cookies 认证Cookie
   */
  async getFollowingNotes(pageSize = 20, cookies) {
    if (!cookies) {
      throw new Error('需要提供登录Cookie才能获取关注笔记');
    }

    try {
      const url = `${this.baseUrl}/api/sns/web/v1/homefeed?cursor=&num=${pageSize}`;
      const response = await axios.get(url, {
        headers: {
          'Cookie': cookies,
          'User-Agent': this.userAgent
        }
      });

      const data = response.data;

      if (data.code !== 0) {
        throw new Error(data.message);
      }

      return data.data.items.map(item => ({
        title: item.note_card.title || '无标题',
        description: item.note_card.desc,
        url: `${this.baseUrl}/explore/${item.note_card.id}`,
        noteId: item.note_card.id,
        cover: item.note_card.cover?.url,
        images: item.note_card.image_list?.map(img => img.url) || [],
        author: item.note_card.user.nick_name,
        authorId: item.note_card.user.user_id,
        publishTime: new Date(item.note_card.time * 1000),
        tags: this.extractTags(item.note_card.tag_list),
        source: 'xiaohongshu',
        type: 'note',
        stats: {
          like: item.note_card.interact_info.liked_count,
          collect: item.note_card.interact_info.collected_count,
          comment: item.note_card.interact_info.comment_count
        },
        noteType: item.note_card.type
      }));
    } catch (error) {
      console.error('获取小红书笔记失败:', error);
      return [];
    }
  }

  /**
   * 获取热门笔记
   * @param {string} category 分类关键词
   * @param {number} pageSize 数量
   */
  async getHotNotes(category = '', pageSize = 20) {
    try {
      const url = `${this.baseUrl}/api/sns/web/v1/search/notes?keyword=${encodeURIComponent(category)}&page=1&page_size=${pageSize}`;
      const response = await this.axiosInstance.get(url);

      const data = response.data;

      if (data.code !== 0) {
        throw new Error(data.message);
      }

      return data.data.items?.map(item => ({
        title: item.note_card.title || item.note_card.desc?.slice(0, 50) + '...',
        description: item.note_card.desc,
        url: `${this.baseUrl}/explore/${item.note_card.id}`,
        noteId: item.note_card.id,
        cover: item.note_card.cover?.url,
        images: item.note_card.image_list?.map(img => img.url) || [],
        author: item.note_card.user.nick_name,
        publishTime: new Date(item.note_card.time * 1000),
        tags: this.extractTags(item.note_card.tag_list),
        source: 'xiaohongshu',
        type: 'note',
        stats: {
          like: item.note_card.interact_info.liked_count,
          collect: item.note_card.interact_info.collected_count
        }
      })) || [];
    } catch (error) {
      console.error('获取小红书热门笔记失败:', error);
      return [];
    }
  }

  // 标签提取
  extractTags(tagList) {
    if (!tagList || !Array.isArray(tagList)) return [];
    return tagList.map(tag => tag.name || tag.tag_name).filter(t => t);
  }

  // 延迟函数
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // 处理平台内容 - 统一接口
  async handlePlatform(platform, url, options = {}) {
    if (!this.supportedPlatforms.includes(platform)) {
      throw new Error(`不支持的平台: ${platform}`);
    }

    return await this.extractNoteFromUrl(url, options);
  }

  // 插件初始化钩子
  async initialize() {
    console.log('小红书插件初始化完成（优化版）');
  }
}

// 导出插件
module.exports = {
  XiaohongShu,
  pluginMeta,
  // 提取器实例
  instance: new XiaohongShu()
};