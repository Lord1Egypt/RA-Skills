// 快乐小狗配置文件 - 优化版
module.exports = {
  // 基础配置
  basic: {
    maxConcurrency: 3, // 最大并发处理数
    cacheTTL: 24 * 60 * 60 * 1000, // 缓存24小时
    maxVideoSeconds: 60, // 最大视频时长
    timeoutMs: 30000, // 默认超时时间
    retryTimes: 3,
    retryDelayMs: 250
  },

  // 知识分类（扩展版）
  categories: {
    // 原有分类
    '人工智能（AI）': {
      keywords: ['ai', '人工智能', '大模型', '机器学习', '深度学习', 'llm', '算法', '神经网络', 'agent', 'rag', 'chatgpt', 'gpt'],
      priority: 'high',
      color: '#FF6B6B'
    },
    '产品经理': {
      keywords: ['产品经理', 'prd', '需求', '用户体验', '原型', '权限设计', '产品迭代', 'mvp', 'roadmap', '埋点', '数据分析'],
      priority: 'high',
      color: '#4ECDC4'
    },
    '经济（投资/股票/保险/加密货币）': {
      keywords: ['股票', '基金', '投资', '保险', '加密货币', '比特币', '以太坊', '理财', '经济', '宏观', '资产配置', '财富管理'],
      priority: 'medium',
      color: '#45B7D1'
    },
    '心理学': {
      keywords: ['心理学', '认知', '情绪', '人格', '潜意识', '行为', '共情', '心理', '动机', '压力', '心理学原理'],
      priority: 'medium',
      color: '#96CEB4'
    },
    '商业机会': {
      keywords: ['创业', '商机', '商业模式', '变现', '流量', '增长', '商业机会', '客户开发', '渠道', 'b2b', 'b2c', '副业'],
      priority: 'high',
      color: '#FFEAA7'
    },
    '灵感': {
      keywords: ['灵感', '想法', '创意', '感悟', '备忘', '金句', '启发', '洞察', '思考', '点子'],
      priority: 'low',
      color: '#DDA0DD'
    },

    // 新增分类
    '学习成长': {
      keywords: ['学习', '课程', '教程', '培训', '书单', '知识', '技能', '成长', '提升', '教育', '学习方法'],
      priority: 'medium',
      color: '#74B9FF'
    }
  },

  // 平台处理规则
  platformRules: {
    xhs: {
      name: '小红书',
      enableOCR: true,
      maxPages: 1,
      waitTime: 2000
    },
    zhihu: {
      name: '知乎',
      includeComments: false,
      maxAnswers: 1
    },
    bilibili: {
      name: 'B站',
      extractSubtitles: true,
      maxDuration: 300,
      includeDanmaku: false
    },
    github: {
      name: 'GitHub',
      includeReadme: true,
      includeReleases: false,
      maxDescriptionLength: 1000
    },
    wechat: {
      name: '微信',
      includeImages: true,
      includeAuthorProfile: false
    },
    douyin: {
      name: '抖音',
      extractAudio: false,
      maxDuration: 60
    }
  },

  // 内容过滤规则
  filters: {
    safety: {
      // 安全规则
      forbiddenPatterns: [
        /色情|裸聊|约炮|成人视频/i,
        /恐怖袭击|制爆|枪支交易|暴力极端/i,
        /颠覆|煽动分裂|敏感政治/i,
        /赌博|博彩|彩票/i
      ],
      minLength: 50,
      maxLength: 10000
    },

    quality: {
      // 质量规则
      minEngagement: {
        likes: 0,
        views: 0,
        comments: 0
      },
      excludeKeywords: [
        '广告', '推广', '招商', '加盟',
        '兼职', '刷单', '代购'
 ],
      requireKeywords: [],
      includeKeywords: []
    },

    duplication: {
      // 去重规则
      enabled: true,
      similarityThreshold: 0.8,
      checkContent: true,
      checkUrl: true
    }
  },

  // 模板配置
  templates: {
    default: 'standard',
    autoSelect: true,
    customFooter: `
---
*内容由快乐小狗信息整理器自动提取和整理*
*如有疑问请联系管理员*
    `,
    dateFormat: 'YYYYMMDD',
    timestampFormat: true
  },

  // 存储配置
  storage: {
    lark: {
      enabled: true,
      spaceName: '快乐小狗空间',
      createFolderStructure: true,
      setPermissions: {
        externalAccess: false,
        commentPermission: 'anyone_can_comment'
      }
    },
    local: {
      enabled: false,
      basePath: './output',
      organizeByDate: true,
      organizeByCategory: true
    }
  },

  // 通知配置
  notifications: {
    enabled: true,
    channels: {
      lark: {
        enabled: true,
        onSuccess: true,
        onError: true
      },
      webhook: {
        enabled: false,
        url: process.env.WEBHOOK_URL || '',
        format: 'json'
      }
    }
  },

  // 特殊处理规则
  specialRules: {
    // 视频处理
    video: {
      extractAudio: true,
      generateSubtitles: true,
      maxDuration: 300,
      formats: ['mp4', 'mov', 'avi']
    },

    // 图片处理
    image: {
      extractOCR: true,
      ocrLanguages: ['zh-CN', 'en-US'],
      maxImages: 20,
      saveLocal: false
    },

    // 代码处理
    code: {
      highlightSyntax: true,
      detectLanguage: true,
      maxCodeBlocks: 10
    }
  },

  // 调试和日志
  debug: {
    enabled: process.env.DEBUG === 'true',
    level: 'info',
    saveToFile: false,
    maxLogSize: '10MB',
    traceId: true
  },

  // 功能层级配置 - 渐进式披露
  featureTiers: {
    // 基础层 - 默认暴露
    basic: {
      enabled: true,
      description: '核心内容提取和基础分类功能',
      features: [
        'content-extraction',      // 内容提取
        'basic-classification',    // 基础分类
        'simple-storage'          // 简单存储
      ],
      platforms: [
        'xiaohongshu',
        'wechat',
        'generic-web'
      ],
      limits: {
        maxConcurrentTasks: 1,
        maxContentLength: 5000,
        enableAdvancedAnalysis: false
      }
    },

    // 进阶层 - 按需启用
    advanced: {
      enabled: process.env.ENABLE_ADVANCED_FEATURES === 'true',
      description: '高级分析、批量处理、多平台聚合',
      features: [
        'batch-processing',       // 批量处理
        'advanced-classification', // 高级分类
        'content-summarization',   // 内容摘要
        'duplicate-detection',    // 重复检测
        'performance-analytics'    // 性能分析
      ],
      platforms: [
        'zhihu',
        'bilibili',
        'github'
      ],
      limits: {
        maxConcurrentTasks: 3,
        maxContentLength: 20000,
        enableAdvancedAnalysis: true,
        enableAPILogger: true
      }
    },

    // 专家层 - 配置启用
    expert: {
      enabled: process.env.ENABLE_EXPERT_FEATURES === 'true',
      description: '自定义规则、API接口、插件扩展',
      features: [
        'custom-rules',          // 自定义规则
        'api-endpoints',         // API接口
        'plugin-extension',      // 插件扩展
        'ai-powered-analysis',   // AI驱动分析
        'real-time-monitoring',  // 实时监控
        'advanced-reporting'     // 高级报告
      ],
      platforms: [
        'douyin',
        'custom-platform'
      ],
      limits: {
        maxConcurrentTasks: 5,
        maxContentLength: 50000,
        enableAdvancedAnalysis: true,
        enableAPILogger: true,
        enableDebugMode: true
      }
    }
  },

  // 功能开关配置
  featureFlags: {
    // 默认功能
    defaultFeatures: {
      contentExtraction: true,
      classification: true,
      storage: true
    },

    // 高级功能（需要环境变量启用）
    advancedFeatures: {
      batchProcessing: process.env.ENABLE_BATCH_PROCESSING === 'true',
      contentSummarization: process.env.ENABLE_SUMMARIZATION === 'true',
      duplicateDetection: process.env.ENABLE_DUPLICATE_DETECTION === 'true',
      performanceAnalytics: process.env.ENABLE_ANALYTICS === 'true'
    },

    // 专家功能（需要专业许可）
    expertFeatures: {
      customRules: process.env.ENABLE_CUSTOM_RULES === 'true',
      apiEndpoints: process.env.ENABLE_API === 'true',
      pluginExtension: process.env.ENABLE_PLUGINS === 'true',
      aiAnalysis: process.env.ENABLE_AI_ANALYSIS === 'true',
      realTimeMonitoring: process.env.ENABLE_MONITORING === 'true',
      advancedReporting: process.env.ENABLE_REPORTING === 'true'
    }
  },

  // 获取当前启用的功能层级
  getCurrentTier() {
    if (this.featureTiers.expert.enabled) {
      return 'expert';
    }
    if (this.featureTiers.advanced.enabled) {
      return 'advanced';
    }
    return 'basic';
  },

  // 检查功能是否启用
  isFeatureEnabled(featureName) {
    const tier = this.getCurrentTier();
    const tierConfig = this.featureTiers[tier];
    return tierConfig.features.includes(featureName);
  },

  // 检查平台是否支持
  isPlatformSupported(platformName) {
    const tier = this.getCurrentTier();
    const tierConfig = this.featureTiers[tier];
    return tierConfig.platforms.includes(platformName);
  },

  // 获取当前层级的限制配置
  getCurrentLimits() {
    const tier = this.getCurrentTier();
    return this.featureTiers[tier].limits;
  }
};