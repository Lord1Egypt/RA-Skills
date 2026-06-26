// 飞书云盘配置文件 - 统一管理
const path = require('path');

// 验证必需的配置
function validateFeishuConfig(config) {
  const errors = [];
  const appId = config?.auth?.appId;
  const appSecret = config?.auth?.appSecret;
  const baseFolderToken = config?.drive?.baseFolderToken;

  if (!appId || appId === '你的飞书应用ID') {
    errors.push('FEISHU_APP_ID 未设置或使用默认值');
  }

  if (!appSecret || appSecret === '你的飞书应用秘钥') {
    errors.push('FEISHU_APP_SECRET 未设置或使用默认值');
  }

  if (!baseFolderToken || baseFolderToken === '你的飞书云盘根文件夹token') {
    errors.push('FEISHU_BASE_FOLDER_TOKEN 未设置或使用默认值');
  }

  if (errors.length > 0) {
    console.warn('飞书配置警告：');
    errors.forEach(error => console.warn(`  - ${error}`));
    return false;
  }

  return true;
}

// 飞书配置
const feishuConfig = {
  // 基础认证配置
  auth: {
    appId: process.env.FEISHU_APP_ID || '你的飞书应用ID',
    appSecret: process.env.FEISHU_APP_SECRET || '你的飞书应用秘钥',
    // 应用访问令牌缓存（避免频繁获取）
    accessToken: null,
    tokenExpireTime: 0
  },

  // 云盘空间配置
  drive: {
    spaceName: process.env.FEISHU_SPACE_NAME || '快乐小狗空间',
    baseFolderToken: process.env.FEISHU_BASE_FOLDER_TOKEN || '你的飞书云盘根文件夹token',
    domain: 'https://open.feishu.cn',
    // API端点
    endpoints: {
      auth: '/open-apis/auth/v3/tenant_access_token/internal',
      upload: '/open-apis/drive/v1/medias/upload_all',
      file: '/open-apis/drive/v1/files',
      permissions: '/open-apis/drive/v2/permissions'
    }
  },

  // 文件夹配置
  folders: {
    // 是否自动创建分类文件夹
    autoCreate: true,
    // 文件夹命名规则
    namingRule: 'date_category', // 'date_category', 'category_date', 'category'
    // 最大文件夹深度
    maxDepth: 3,
    // 已知分类文件夹映射（避免频繁创建）
    categoryFolderMap: {}
  },

  // 权限配置
  permissions: {
    // 默认文件权限
    defaultFilePermission: {
      type: 'anyone_can_view',
      commentPermission: 'anyone_can_comment',
      needNotify: false
    },
    // 外部访问控制
    externalAccess: {
      enabled: false,
      shareable: true,
      allowDownload: true
    }
  },

  // 上传配置
  upload: {
    // 支持的文件类型
    allowedTypes: ['text/markdown', 'text/plain', 'application/pdf'],
    // 最大文件大小（字节，默认10MB）
    maxFileSize: 10 * 1024 * 1024,
    // 分片上传阈值（超过此大小使用分片上传）
    chunkSize: 5 * 1024 * 1024,
    // 并发上传数
    concurrency: 2
  },

  // 缓存配置
  cache: {
    // 文件上传缓存（避免重复上传）
    enabled: true,
    // 缓存存储路径
    storagePath: path.join(__dirname, '../cache/feishu'),
    // 缓存有效期（毫秒）
    ttl: 24 * 60 * 60 * 1000 // 24小时
  },

  // 重试和超时配置
  retry: {
    maxTimes: 3,
    delayMs: 1000,
    exponentialBackoff: true
  },

  timeout: {
    connect: 10000,  // 连接超时
    upload: 60000,   // 上传超时
    api: 30000       // API调用超时
  },

  // 环境特定配置
  environments: {
    development: {
      domain: 'https://open.feishu.cn',
      debug: true,
      logLevel: 'debug'
    },
    test: {
      domain: 'https://open.feishu.cn',
      debug: true,
      logLevel: 'info'
    },
    production: {
      domain: 'https://open.feishu.cn',
      debug: false,
      logLevel: 'warn'
    }
  },

  // 获取当前环境配置
  getCurrentConfig() {
    const env = process.env.NODE_ENV || 'development';
    return {
      ...this,
      ...this.environments[env] || this.environments.development
    };
  },

  // 验证配置
  validate() {
    const config = this.getCurrentConfig();
    return validateFeishuConfig(config);
  },

  // 获取认证信息
  getAuthConfig() {
    const config = this.getCurrentConfig();
    return config.auth;
  },

  // 获取驱动配置
  getDriveConfig() {
    const config = this.getCurrentConfig();
    return config.drive;
  },

  // 获取上传配置
  getUploadConfig() {
    const config = this.getCurrentConfig();
    return config.upload;
  }
};

// 初始化时验证配置
if (process.env.NODE_ENV !== 'test') {
  feishuConfig.validate();
}

module.exports = feishuConfig;
