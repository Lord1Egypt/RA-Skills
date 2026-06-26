// 插件加载器 - 支持渐进式功能披露
const path = require('path');
const config = require('../config/happy-dog-config.js');

// 插件能力枚举
const PluginCapabilities = {
  BASIC: 'basic',          // 基础能力
  ADVANCED: 'advanced',    // 进阶能力
  EXPERT: 'expert'         // 专家能力
};

// 插件定义
const pluginDefinitions = {
  // 基础层插件
  core: {
    'wechat': {
      file: 'wechat.js',
      capabilities: [PluginCapabilities.BASIC],
      description: '微信公众号内容提取',
      features: ['content-extraction', 'basic-classification'],
      priority: 1
    },
    'content-extractor': {
      file: 'content-extractor.js',
      capabilities: [PluginCapabilities.BASIC],
      description: '通用内容提取器',
      features: ['content-extraction', 'generic-web'],
      priority: 0,  // 最高优先级，核心组件
      required: true  // 必需插件
    }
  },

  // 进阶层插件
  advanced: {
    'zhihu': {
      file: 'zhihu.js',
      capabilities: [PluginCapabilities.ADVANCED],
      description: '知乎内容提取',
      features: ['content-extraction', 'advanced-classification'],
      priority: 2
    },
    'bilibili': {
      file: 'bilibili.js',
      capabilities: [PluginCapabilities.ADVANCED],
      description: 'B站视频提取',
      features: ['video-extraction', 'subtitle-extraction'],
      priority: 2
    },
    'github': {
      file: 'github.js',
      capabilities: [PluginCapabilities.ADVANCED],
      description: 'GitHub项目提取',
      features: ['repo-extraction', 'readme-analysis'],
      priority: 2
    }
  },

  // 专家层插件
  expert: {
    'xiaohongshu': {
      file: 'xiaohongshu.js',
      capabilities: [PluginCapabilities.EXPERT],
      description: '小红书内容提取（需要Puppeteer）',
      features: ['ocr-extraction', 'advanced-content-analysis'],
      priority: 3,
      dependencies: ['puppeteer']
    }
  }
};

// 插件加载器类
class PluginLoader {
  constructor() {
    this.loadedPlugins = new Map();
    this.initializedPlugins = new Map();
    this.currentTier = config.getCurrentTier();
  }

  normalizePluginModule(name, pluginModule) {
    if (!pluginModule) {
      return pluginModule;
    }

    if (typeof pluginModule.extractContent === 'function' || typeof pluginModule.handlePlatform === 'function') {
      return pluginModule;
    }

    const instance = pluginModule.instance;
    if (instance) {
      const supportedPlatforms =
        pluginModule.supportedPlatforms ||
        pluginModule.pluginMeta?.supportedPlatforms ||
        instance.supportedPlatforms ||
        (name === 'content-extractor'
          ? ['generic', 'xiaohongshu', 'zhihu', 'bilibili', 'github']
          : [name]);

      const normalized = {
        supportedPlatforms,
      };

      if (typeof instance.initialize === 'function') {
        normalized.initialize = instance.initialize.bind(instance);
      }
      if (typeof instance.extractContent === 'function') {
        normalized.extractContent = instance.extractContent.bind(instance);
      } else if (typeof instance.extractArticleFromUrl === 'function') {
        normalized.extractContent = instance.extractArticleFromUrl.bind(instance);
      }
      if (typeof instance.handlePlatform === 'function') {
        normalized.handlePlatform = instance.handlePlatform.bind(instance);
      }

      return normalized;
    }

    if (typeof pluginModule === 'function' && typeof pluginModule.prototype?.extractContent === 'function') {
      const created = new pluginModule();
      if (!created.supportedPlatforms) {
        created.supportedPlatforms =
          name === 'content-extractor' ? ['generic', 'xiaohongshu', 'zhihu', 'bilibili', 'github'] : [name];
      }
      return created;
    }

    return pluginModule;
  }

  // 获取当前可用的插件列表
  getAvailablePlugins() {
    const available = [];

    // 根据当前层级加载插件
    if (this.currentTier === 'basic' || this.currentTier === 'advanced' || this.currentTier === 'expert') {
      available.push(...Object.entries(pluginDefinitions.core));
    }

    if (this.currentTier === 'advanced' || this.currentTier === 'expert') {
      available.push(...Object.entries(pluginDefinitions.advanced));
    }

    if (this.currentTier === 'expert') {
      available.push(...Object.entries(pluginDefinitions.expert));
    }

    // 按优先级排序
    return available.sort(([,a], [,b]) => a.priority - b.priority);
  }

  // 加载单个插件
  async loadPlugin(name, definition, tier) {
    try {
      // 检查插件能力是否符合当前层级
      if (!definition.capabilities.includes(this.currentTier) && !definition.capabilities.includes(PluginCapabilities.BASIC)) {
        console.warn(`插件 ${name} 不支持当前层级 ${this.currentTier}`);
        return null;
      }

      // 检查依赖
      if (definition.dependencies) {
        for (const dep of definition.dependencies) {
          try {
            require.resolve(dep);
          } catch (e) {
            console.warn(`插件 ${name} 缺少依赖 ${dep}，跳过加载`);
            return null;
          }
        }
      }

      // 加载插件文件
      const pluginPath = path.join(__dirname, tier, definition.file);
      const pluginModule = this.normalizePluginModule(name, require(pluginPath));

      // 包装插件以支持能力标记
      const wrappedPlugin = {
        name,
        description: definition.description,
        capabilities: definition.capabilities,
        features: definition.features,
        priority: definition.priority,
        tier,
        module: pluginModule
      };

      this.loadedPlugins.set(name, wrappedPlugin);
      console.log(`成功加载插件: ${name} (${tier})`);

      return wrappedPlugin;
    } catch (error) {
      console.error(`加载插件 ${name} 失败:`, error);
      return null;
    }
  }

  // 加载所有可用插件
  async loadAllPlugins() {
    const availablePlugins = this.getAvailablePlugins();
    const loadPromises = [];

    for (const [name, definition] of availablePlugins) {
      // 确定插件所属层级
      let tier = 'core';
      if (pluginDefinitions.advanced[name]) tier = 'advanced';
      if (pluginDefinitions.expert[name]) tier = 'expert';

      loadPromises.push(this.loadPlugin(name, definition, tier));
    }

    const results = await Promise.allSettled(loadPromises);

    // 统计加载结果
    const success = results.filter(r => r.status === 'fulfilled').length;
    const failed = results.length - success;

    console.log(`插件加载完成: 成功 ${success}, 失败 ${failed}`);
  }

  // 获取已加载的插件
  getPlugin(name) {
    return this.loadedPlugins.get(name);
  }

  // 获取指定功能的所有插件
  getPluginsByFeature(featureName) {
    const plugins = [];

    for (const [name, plugin] of this.loadedPlugins) {
      if (plugin.features.includes(featureName)) {
        plugins.push(plugin);
      }
    }

    return plugins.sort((a, b) => a.priority - b.priority);
  }

  // 初始化插件
  async initializePlugins() {
    for (const [name, plugin] of this.loadedPlugins) {
      try {
        // 如果插件有初始化方法
        if (plugin.module.initialize && typeof plugin.module.initialize === 'function') {
          await plugin.module.initialize();
          this.initializedPlugins.set(name, true);
          console.log(`初始化插件: ${name}`);
        } else {
          this.initializedPlugins.set(name, true);
        }
      } catch (error) {
        console.error(`初始化插件 ${name} 失败:`, error);
        this.initializedPlugins.set(name, false);
      }
    }
  }

  // 检查功能是否可用
  isFeatureAvailable(featureName) {
    // 首先检查配置是否启用该功能
    if (!config.isFeatureEnabled(featureName)) {
      return false;
    }

    // 然后检查是否有插件支持该功能
    const plugins = this.getPluginsByFeature(featureName);
    return plugins.length > 0;
  }

  // 卸载插件
  unloadPlugin(name) {
    if (this.loadedPlugins.has(name)) {
      this.loadedPlugins.delete(name);
      this.initializedPlugins.delete(name);
      console.log(`卸载插件: ${name}`);
    }
  }

  // 重新加载插件
  async reloadPlugin(name) {
    const plugin = this.loadedPlugins.get(name);
    if (plugin) {
      this.unloadPlugin(name);
      const definition = pluginDefinitions[plugin.tier][name];
      await this.loadPlugin(name, definition, plugin.tier);
    }
  }

  // 获取插件统计信息
  getStats() {
    const stats = {
      totalLoaded: this.loadedPlugins.size,
      totalInitialized: Array.from(this.initializedPlugins.values()).filter(v => v).length,
      currentTier: this.currentTier,
      pluginsByTier: {
        core: 0,
        advanced: 0,
        expert: 0
      }
    };

    for (const plugin of this.loadedPlugins.values()) {
      stats.pluginsByTier[plugin.tier]++;
    }

    return stats;
  }
}

// 创建全局插件加载器实例
const pluginLoader = new PluginLoader();

// 导出
module.exports = {
  pluginLoader,
  PluginCapabilities,
  pluginDefinitions
};
