// 动态内容提取器 - 支持渐进式功能披露
const { pluginLoader } = require('../plugins/plugin-loader');
const config = require('../config/happy-dog-config');

class DynamicContentExtractor {
  constructor() {
    this.platformHandlers = new Map();
    this.initialized = false;
  }

  // 初始化提取器
  async initialize() {
    if (this.initialized) return;

    console.log('初始化动态内容提取器...');

    // 加载所有插件
    await pluginLoader.loadAllPlugins();

    // 注册平台处理器
    await this.registerPlatformHandlers();

    // 初始化插件
    await pluginLoader.initializePlugins();

    this.initialized = true;
    console.log('动态内容提取器初始化完成');
  }

  // 注册平台处理器
  async registerPlatformHandlers() {
    for (const [name, plugin] of pluginLoader.loadedPlugins) {
      // 检查插件是否提供平台处理能力
      if (plugin.module.handlePlatform || plugin.module.extractContent) {
        // 获取插件支持的平台
        const platforms = plugin.module.supportedPlatforms || [name];

        for (const platform of platforms) {
          if (!this.platformHandlers.has(platform)) {
            this.platformHandlers.set(platform, []);
          }
          this.platformHandlers.get(platform).push(plugin);
          console.log(`注册平台处理器: ${platform} -> ${plugin.name}`);
        }
      }
    }
  }

  // 检测平台类型
  detectPlatform(url) {
    const platforms = {
      'xiaohongshu': /xiaohongshu\.com|xhslink\.com/i,
      'wechat': /mp\.weixin\.qq\.com|weixin\.qq\.com/i,
      'douyin': /douyin\.com|dyurl\.cn/i,
      'zhihu': /zhihu\.com/i,
      'bilibili': /bilibili\.com/i,
      'github': /github\.com/i
    };

    for (const [platform, regex] of Object.entries(platforms)) {
      if (regex.test(url)) {
        return platform;
      }
    }

    return 'generic';
  }

  // 获取可用的处理器
  getAvailableHandlers(platform) {
    const handlers = this.platformHandlers.get(platform) || [];

    // 根据当前功能层级过滤处理器
    const currentTier = config.getCurrentTier();
    return handlers.filter(handler => {
      return handler.capabilities.includes(currentTier) ||
             handler.capabilities.includes('basic');
    });
  }

  // 提取内容
  async extractContent(url, options = {}) {
    await this.initialize();

    const platform = this.detectPlatform(url);
    const handlers = this.getAvailableHandlers(platform);

    if (handlers.length === 0) {
      throw new Error(`没有找到适用于平台 ${platform} 的处理器`);
    }

    // 按优先级尝试处理器
    const errors = [];
    for (const handler of handlers) {
      try {
        console.log(`使用处理器 ${handler.name} 提取 ${platform} 内容`);

        let result;
        if (handler.module.extractContent) {
          result = await handler.module.extractContent(url, options);
        } else if (handler.module.handlePlatform) {
          result = await handler.module.handlePlatform(platform, url, options);
        }

        // 添加元数据
        result = {
          ...result,
 platform,
          handler: handler.name,
          tier: handler.tier,
          extractedAt: new Date().toISOString()
        };

        // 后处理：分类、摘要等
        if (config.isFeatureEnabled('advanced-classification')) {
          result.category = await this.classifyContent(result);
        }

        if (config.isFeatureEnabled('content-summarization')) {
          result.summary = await this.generateSummary(result);
        }

        return result;
      } catch (error) {
        console.error(`处理器 ${handler.name} 提取失败:`, error.message);
        errors.push({ handler: handler.name, error: error.message });
      }
    }

    throw new Error(`所有处理器都失败了: ${JSON.stringify(errors, null, 2)}`);
  }

  // 分类内容
  async classifyContent(content) {
    // 这里可以使用AI分类或关键词匹配
    // 暂时使用简单的关键词匹配
    const text = (content.title + ' ' + (content.content || '')).toLowerCase();
    const categories = config.categories;
    let bestCategory = '灵感';
    let bestScore = 0;

    for (const [category, config] of Object.entries(categories)) {
      const score = config.keywords.reduce((sum, keyword) => {
        return sum + (text.includes(keyword.toLowerCase()) ? 1 : 0);
      }, 0);

      if (score > bestScore) {
        bestScore = score;
        bestCategory = category;
      }
    }

    return bestCategory;
  }

  // 生成摘要
  async generateSummary(content) {
    // 简单的摘要生成：提取前几句话
    const text = content.content || content.description || '';
    if (text.length < 100) return text;

    const sentences = text.match(/[^.!?]+[.!?]+/g) || [];
    return sentences.slice(0, 3).join(' ').trim();
  }

  // 获取支持的平台列表
  getSupportedPlatforms() {
    const platforms = new Set();

    for (const [name, plugin] of pluginLoader.loadedPlugins) {
      const pluginPlatforms = plugin.module.supportedPlatforms || [name];
      pluginPlatforms.forEach(p => platforms.add(p));
    }

    return Array.from(platforms).sort();
  }

  // 获取处理器统计信息
  getHandlerStats() {
    const stats = {
      totalPlatforms: this.platformHandlers.size,
      totalHandlers: Array.from(this.platformHandlers.values())
        .reduce((sum, handlers) => sum + handlers.length, 0),
      handlersByPlatform: {}
    };

    for (const [platform, handlers] of this.platformHandlers) {
      stats.handlersByPlatform[platform] = handlers.map(h => ({
        name: h.name,
        tier: h.tier,
        capabilities: h.capabilities
      }));
    }

    return stats;
  }

  // 批量提取
  async batchExtract(urls, options = {}) {
    if (!config.isFeatureEnabled('batch-processing')) {
      throw new Error('批量处理功能在当前配置中未启用');
    }

    const limits = config.getCurrentLimits();
    const concurrency = Math.min(limits.maxConcurrentTasks, urls.length);

    const results = [];
    for (let i = 0; i < urls.length; i += concurrency) {
      const batch = urls.slice(i, i + concurrency);
      const batchResults = await Promise.allSettled(
        batch.map(url => this.extractContent(url, options))
      );

      results.push(...batchResults);
    }

    return results;
  }

  // 重新加载处理器
  async reloadHandlers() {
    this.platformHandlers.clear();
    await this.registerPlatformHandlers();
  }
}

// 创建单例实例
const extractorInstance = new DynamicContentExtractor();

// 导出
module.exports = {
  DynamicContentExtractor,
  extractorInstance
};