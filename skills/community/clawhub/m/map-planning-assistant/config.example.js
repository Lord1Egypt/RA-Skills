/**
 * 配置示例文件
 * 复制此文件为 config.js 并填写你的配置
 */

module.exports = {
  // 高德地图API配置
  amap: {
    // 你的高德API密钥
    apiKey: process.env.AMAP_API_KEY || 'YOUR_AMAP_API_KEY',

    // API基础地址
    baseUrl: 'https://restapi.amap.com/v3',

    // 请求超时时间（毫秒）
    timeout: 8000,

    // 重试次数
    maxRetry: 1
  },

  // 数据存储配置
  storage: {
    // 数据存储目录
    dataDir: './data',

    // 记忆文件名
    memoryFile: 'memory.json',

    // 画像文件名
    profileFile: 'profile.json',

    // 活动文件名
    activityFile: 'activity.json'
  },

  // POI搜索配置
  poi: {
    // 默认搜索半径（米）
    defaultRadius: 3000,

    // 最大搜索半径（米）
    maxRadius: 5000,

    // 最小评分阈值
    minRating: 4.0,

    // 单次最大返回数量
    maxResults: 100,

    // 每页返回数量
    pageSize: 20
  },

  // 路线规划配置
  route: {
    // 默认交通方式
    defaultMode: 'walking',

    // 最大POI数量
    maxPoisPerRoute: 10,

    // 最大天数
    maxDays: 7
  },

  // 记忆系统配置
  memory: {
    // 临时记忆过期时间（毫秒）
    temporaryExpiry: 7 * 24 * 60 * 60 * 1000,

    // 最大交互记录数
    maxInteractions: 50,

    // 最大地图记录数
    maxMaps: 100,

    // 最大路线记录数
    maxRoutes: 50
  },

  // 活动管理配置
  activity: {
    // 活动刷新间隔（毫秒）
    refreshInterval: 24 * 60 * 60 * 1000,

    // 最大活动数
    maxActivities: 100
  },

  // 夜间学习配置
  nightLearning: {
    // 学习时间（24小时制）
    startHour: 2,
    endHour: 4,

    // 是否启用
    enabled: true
  },

  // 输出配置
  output: {
    // 最大推荐点位数
    maxRecommendations: 10,

    // 是否显示二维码
    showQRCode: true,

    // 是否显示活动推荐
    showActivities: true,

    // 是否显示人文讲解
    showCulture: true
  }
};
