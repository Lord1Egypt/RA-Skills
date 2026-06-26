/**
 * config.js - 配置文件
 * 
 * 修改此文件来自定义 Knowledge Curator 的行为
 */

const path = require('path');

module.exports = {
  // ==================== 存储配置 ====================
  
  /**
   * 知识库根目录路径
   * 相对于 skill 目录或绝对路径
   */
  knowledgeBasePath: path.join(__dirname, '../knowledge-base'),
  
  /**
   * 索引文件路径
   * 存储所有条目的元数据
   */
  indexPath: path.join(__dirname, '../knowledge-base/index.json'),
  
  /**
   * 导出目录
   * 存放导出的文件
   */
  exportPath: path.join(__dirname, '../exports'),
  
  // ==================== 分类配置 ====================
  
  /**
   * 支持的分类列表
   * 添加或删除分类需同步更新目录结构
   */
  categories: ['科技', '生活', '学习', '娱乐', '工作', '健康'],
  
  /**
   * 分类特征词库（在 categorize.js 中定义）
   * 可根据需要调整权重和关键词
   */
  
  // ==================== 内容处理配置 ====================
  
  /**
   * 摘要最大长度（字符数）
   */
  summaryMaxLength: 500,
  
  /**
   * 关键知识点最大数量
   */
  maxKeyPoints: 5,
  
  /**
   * 标签最大数量
   */
  maxTags: 5,
  
  /**
   * 正文内容最大长度（超过会被截断）
   */
  contentMaxLength: 5000,
  
  // ==================== 去重配置 ====================
  
  /**
   * 去重检测相似度阈值 (0-1)
   * 越高越严格，0.85 表示 85% 相似即判定为重复
   */
  duplicateThreshold: 0.85,
  
  /**
   * 是否启用 URL 完全匹配去重
   */
  enableUrlDedup: true,
  
  /**
   * 是否启用内容指纹去重
   */
  enableFingerprintDedup: true,
  
  /**
   * 是否启用标题相似度去重
   */
  enableTitleDedup: true,
  
  // ==================== 网络请求配置 ====================
  
  /**
   * 请求延迟（毫秒）
   * 避免触发平台反爬机制
   */
  requestDelay: 1000,
  
  /**
   * 请求超时时间（毫秒）
   */
  requestTimeout: 10000,
  
  /**
   * User-Agent
   */
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  
  // ==================== 搜索配置 ====================
  
  /**
   * 默认搜索结果数量限制
   */
  defaultSearchLimit: 20,
  
  /**
   * 最大搜索结果数量
   */
  maxSearchLimit: 100,
  
  /**
   * 是否启用语义搜索
   * 使用同义词扩展提高搜索准确率
   */
  enableSemanticSearch: true,
  
  /**
   * 搜索匹配权重
   */
  searchWeights: {
    title: 10,      // 标题匹配权重
    tag: 5,         // 标签匹配权重
    category: 3,    // 分类匹配权重
    content: 1      // 正文匹配权重
  },
  
  // ==================== AI 配置（可选） ====================
  
  /**
   * AI 服务配置
   * 用于生成更智能的摘要和知识点
   * 留空则使用本地总结算法
   */
  aiService: null,
  
  /**
   * 示例 AI 配置（取消注释并填写后使用）
   */
  /*
  aiService: {
    provider: 'openai',  // 或 'anthropic', 'bailian', etc.
    apiKey: process.env.AI_API_KEY,
    endpoint: 'https://api.openai.com/v1/chat/completions',
    model: 'gpt-3.5-turbo',
    maxTokens: 500
  },
  */
  
  // ==================== 日志配置 ====================
  
  /**
   * 是否启用详细日志
   */
  verbose: true,
  
  /**
   * 日志文件路径（留空则只输出到控制台）
   */
  logFile: null,
  
  // ==================== 其他配置 ====================
  
  /**
   * 是否自动创建缺失的分类目录
   */
  autoCreateDirectories: true,
  
  /**
   * 是否在保存时生成预览
   */
  generatePreview: true,
  
  /**
   * 预览最大长度
   */
  previewMaxLength: 200,
  
  /**
   * 是否保留原始 HTML（用于调试）
   */
  keepRawHtml: false
};
