// 微信公众号内容获取插件 - 基础层（基于验证方案优化）
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

// 插件元数据
const pluginMeta = {
  name: 'wechat',
  version: '2.0.0',
  capabilities: ['basic'],
  tier: 'core',
  supportedPlatforms: ['wechat'],
  features: ['content-extraction', 'basic-classification', 'image-extraction'],
  description: '微信公众号内容提取（直接从文章URL提取）',
  dependencies: ['axios', 'cheerio']
};

class WeChat {
  constructor(options = {}) {
    this.supportedPlatforms = ["wechat"];
    this.timeout = options.timeout || 15000;
    this.retryTimes = options.retryTimes || 3;
    this.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36';
    this.imageDir = options.imageDir || path.join(process.cwd(), 'temp', 'wechat_images');

    // 确保图片目录存在
    if (!fs.existsSync(this.imageDir)) {
      fs.mkdirSync(this.imageDir, { recursive: true });
    }

    // 配置请求
    this.axiosInstance = axios.create({
      timeout: this.timeout,
      headers: {
        'User-Agent': this.userAgent
      }
    });
  }

  /**
   * 从URL提取公众号信息
   * @param {string} url 微信文章URL
   */
  extractAccountInfo(url) {
    // 尝试提取__biz参数
    const bizMatch = url.match(/[?&]__biz=([^&]+)/);
    const biz = bizMatch ? decodeURIComponent(bizMatch[1]) : '';

    // 尝试提取mid参数
    const midMatch = url.match(/[?&]mid=([^&]+)/);
    const mid = midMatch ? decodeURIComponent(midMatch[1]) : '';

    return {
      biz,
      mid,
      accountName: biz // 可以通过API获取公众号名称
    };
  }

  /**
   * 获取图片扩展名
   * @param {Object} response HTTP响应
   * @param {string} fallbackUrl 备用URL
   */
  guessImageExt(response, fallbackUrl = '') {
    const contentType = (response.headers['content-type'] || '').split(';')[0].trim().toLowerCase();
    const extByType = {
      'image/jpeg': '.jpg',
      'image/jpg': '.jpg',
      'image/png': '.png',
      'image/gif': '.gif',
      'image/webp': '.webp'
    };

    if (extByType[contentType]) {
      return extByType[contentType];
    }

    // 检查文件头
    const head = response.data.slice(0, 16);
    if (head.length >= 8) {
      if (head[0] === 0x89 && head[1] === 0x50 && head[2] === 0x4E && head[3] === 0x47) {
        return '.png';
      }
      if (head[0] === 0xFF && head[1] === 0xD8) {
        return '.jpg';
      }
      if (head[0] === 0x47 && head[1] === 0x49 && head[2] === 0x46) {
        return '.gif';
      }
    }

    // 从URL推断
    const urlLower = fallbackUrl.toLowerCase();
    for (const ext of ['.png', '.jpg', '.jpeg', '.gif', '.webp']) {
      if (urlLower.includes(ext)) {
        return ext === '.jpeg' ? '.jpg' : ext;
      }
    }

    return '.jpg';
  }

  /**
   * 规范化目录名
   * @param {string} name 原始名称
   */
  sanitizeDirName(name) {
    name = (name || '').trim();
    if (!name) {
      return '无标题';
    }
    const forbidden = '/\\:*?"<>|';
    let cleaned = '';
    for (const ch of name) {
      cleaned += forbidden.includes(ch) ? '_' : ch;
    }
    cleaned = cleaned.replace(/\s+/g, ' ');
    return cleaned.slice(0, 80) || '无标题';
  }

  /**
   * 下载图片
   * @param {string} imageUrl 图片URL
   * @param {string} fileName 文件名
   * @param {string} referer 引用页
   */
  async downloadImage(imageUrl, fileName, referer = '') {
    try {
      const response = await this.axiosInstance.get(imageUrl, {
        responseType: 'arraybuffer',
        headers: referer ? { Referer: referer } : {}
      });

      const ext = this.guessImageExt({
        headers: response.headers,
        data: response.data
      }, imageUrl);

      const finalFileName = fileName.includes('.') ? fileName : `${fileName}${ext}`;
      const filePath = path.join(this.imageDir, finalFileName);

      fs.writeFileSync(filePath, response.data);
      return {
        success: true,
        path: filePath,
        url: imageUrl,
        fileName: finalFileName
      };
    } catch (error) {
      console.error(`下载图片失败 ${imageUrl}: ${error.message}`);
      return {
        success: false,
        url: imageUrl,
        error: error.message
      };
    }
  }

  /**
   * 从微信文章URL提取内容
   * @param {string} articleUrl 文章URL
   * @param {Object} options 提取选项
   */
  async extractArticleFromUrl(articleUrl, options = {}) {
    try {
      // 获取页面内容
      const response = await this.axiosInstance.get(articleUrl);
      response.encoding = 'utf-8';
      const $ = cheerio.load(response.data);

      // 提取标题
      const title = $('#activity-name').text().trim() || $('h1').text().trim() || '无标题';

      // 创建文章专属目录
      const articleDirName = this.sanitizeDirName(title.slice(0, 10));
      const articleDir = path.join(this.imageDir, articleDirName);

      if (!fs.existsSync(articleDir)) {
        fs.mkdirSync(articleDir, { recursive: true });
      }

      // 提取正文内容
      const contentDiv = $('#js_content');
      if (!contentDiv.length) {
        throw new Error('未找到文章内容区域');
      }

      // 处理图片
      const images = [];
      const imageMap = new Map();
      let imageIndex = 0;

      // 查找所有图片
      contentDiv.find('img').each((i, elem) => {
        const $img = $(elem);
        let imgUrl = $img.attr('data-src') || $img.attr('src') || $img.attr('data-type') === 'png' && $img.attr('data-src');

        if (!imgUrl) return;

        // 处理相对URL
        if (imgUrl.startsWith('//')) {
          imgUrl = 'https:' + imgUrl;
        } else if (imgUrl.startsWith('/')) {
          imgUrl = 'https://mp.weixin.qq.com' + imgUrl;
        }

        imageIndex++;
        const imageId = `IMG_${imageIndex}`;
        imageMap.set(imageId, {
          index: imageIndex,
          originalUrl: imgUrl,
          placeholder: `[[${imageId}]]`
        });

        // 标记图片位置
        $img.replaceWith(`[[${imageId}]]`);
      });

      // 下载图片（如果需要）
      if (options.downloadImages !== false) {
        for (const [imageId, imgInfo] of imageMap) {
          const fileName = `${imgInfo.index}`;
          const result = await this.downloadImage(
            imgInfo.originalUrl,
            fileName,
            articleUrl
          );

          if (result.success) {
            imgInfo.localPath = result.path;
            imgInfo.fileName = result.fileName;
            images.push({
              index: imgInfo.index,
              url: imgInfo.originalUrl,
              localPath: result.path,
              fileName: result.fileName
            });
          }
        }
      }

      // 提取纯文本内容
      const textContent = contentDiv.text()
        .replace(/\[\[IMG_\d+\]\]/g, '') // 移除图片占位符
        .replace(/\s+/g, ' ')
        .trim();

      // 提取作者信息
      const author = $('#js_author_name').text().trim() ||
                     $('.rich_media_meta_text').text().trim() ||
                     '佚名';

      // 提取发布时间
      let publishTime = '';
      const timeText = $('#publish_time').text().trim() ||
                       $('.rich_media_meta_text').eq(1).text().trim();

      if (timeText) {
        // 尝试解析时间格式
        const timeMatch = timeText.match(/(\d{4}-\d{2}-\d{2})/);
        if (timeMatch) {
          publishTime = new Date(timeMatch[1]).toISOString();
        } else {
          publishTime = timeText;
        }
      }

      // 提取文章摘要
      const summary = options.includeSummary ? this.generateSummary(textContent) : '';

      // 提取账号信息
      const accountInfo = this.extractAccountInfo(articleUrl);

      return {
        title,
        type: 'article',
        content: textContent,
        summary,
        author,
        authorId: accountInfo.biz,
        publishTime,
        sourceUrl: articleUrl,
        platform: 'wechat',
        images,

        // 元数据
        metadata: {
          accountInfo,
          articleDir,
          imageCount: images.length,
          wordCount: textContent.length
        },

        // 格式化的内容（包含图片占位符）
        formattedContent: contentDiv.html()
      };
    } catch (error) {
      throw new Error(`提取微信文章失败: ${error.message}`);
    }
  }

  /**
   * 生成文章摘要
   * @param {string} content 文章内容
   */
  generateSummary(content) {
    const sentences = content.split(/[。！？.!?]/).filter(s => s.trim());
    return sentences.slice(0, 3).join('。') + '。';
  }

  /**
   * 处理平台内容 - 统一接口
   */
  async handlePlatform(platform, url, options = {}) {
    if (!this.supportedPlatforms.includes(platform)) {
      throw new Error(`不支持的平台: ${platform}`);
    }

    return await this.extractArticleFromUrl(url, options);
  }

  /**
   * 获取指定公众号的文章列表
   * @param {string} accountId 公众号ID
   * @param {number} count 获取数量
   */
  async getArticles(accountId, count = 10) {
    // 由于API限制，此功能需要额外的RSS服务
    console.warn('获取文章列表功能需要RSS服务支持');
    return [];
  }

  /**
   * 搜索公众号文章
   * @param {string} keyword 搜索关键词
   * @param {number} count 获取数量
   */
  async searchArticles(keyword, count = 10) {
    console.warn('搜索功能需要额外的搜索服务支持');
    return [];
  }

  /**
   * 清理临时文件
   * @param {number} olderThanMs 清理多久之前的文件（毫秒）
   */
  cleanupTempFiles(olderThanMs = 24 * 60 * 60 * 1000) {
    try {
      const files = fs.readdirSync(this.imageDir);
      const now = Date.now();

      files.forEach(file => {
        const filePath = path.join(this.imageDir, file);
        const stats = fs.statSync(filePath);

        if (now - stats.mtimeMs > olderThanMs) {
          if (fs.statSync(filePath).isDirectory()) {
            fs.rmSync(filePath, { recursive: true });
          } else {
            fs.unlinkSync(filePath);
          }
        }
      });
    } catch (error) {
      console.error(`清理临时文件失败: ${error.message}`);
    }
  }

  // 插件初始化钩子
  async initialize() {
    console.log('微信插件初始化完成（优化版）');

    // 定期清理临时文件
    setInterval(() => {
      this.cleanupTempFiles();
    }, 60 * 60 * 1000); // 每小时清理一次
  }
}

// 导出插件
module.exports = {
  WeChat,
  pluginMeta,
  // 提取器实例
  instance: new WeChat()
};