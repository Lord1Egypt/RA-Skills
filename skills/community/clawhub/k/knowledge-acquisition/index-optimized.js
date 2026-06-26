'use strict';

const axios = require('axios');
const cheerio = require('cheerio');
const puppeteer = require('puppeteer');
const crypto = require('crypto');
const os = require('os');
const ffmpeg = require('fluent-ffmpeg');
const { Readable } = require('stream');
const { Client } = require('@larksuiteoapi/node-sdk');

// 导入配置
const feishuConfig = require('./config/feishu-config');
const config = require('./config/happy-dog-config');
const { pluginLoader } = require('./plugins/plugin-loader');
const { extractorInstance } = require('./lib/dynamic-content-extractor');

// 配置验证
const LARK_CONFIG = {
  appId: feishuConfig.getAuthConfig().appId,
  appSecret: feishuConfig.getAuthConfig().appSecret,
  cloudDriveSpaceName: feishuConfig.getDriveConfig().spaceName,
  baseFolderToken: feishuConfig.getDriveConfig().baseFolderToken
};

const larkClient = new Client({
  appId: LARK_CONFIG.appId,
  appSecret: LARK_CONFIG.appSecret,
  domain: feishuConfig.getDriveConfig().domain
});

// 错误级别定义
const ErrorLevel = {
  WARNING: 'warning',
  ERROR: 'error',
  CRITICAL: 'critical'
};

// 创建错误提醒消息
function createErrorMessage(step, error, level = ErrorLevel.ERROR) {
  const timestamp = new Date().toISOString();
  const icon = level === ErrorLevel.CRITICAL ? '🚨' : level === ErrorLevel.ERROR ? '❌' : '⚠️';
  return `${icon} ${error.message}\n步骤：${step}\n时间：${timestamp}`;
}

// 执行步骤包装器，增加错误处理和监控
async function executeStep(stepName, stepFunction, context = {}) {
  const startTime = Date.now();
  context.trace.push({
    step: stepName,
    status: 'started',
    timestamp: new Date().toISOString()
  });

  try {
    const result = await stepFunction();
    const duration = Date.now() - startTime;

    context.trace.push({
      step: stepName,
      status: 'completed',
      duration: `${duration}ms`,
      timestamp: new Date().toISOString()
    });

    console.log(`✓ 步骤"${stepName}"完成，耗时 ${duration}ms`);
    return result;
  } catch (error) {
    const duration = Date.now() - startTime;

    context.trace.push({
      step: stepName,
      status: 'failed',
      error: error.message,
      duration: `${duration}ms`,
      timestamp: new Date().toISOString()
    });

    console.error(`✗ 步骤"${stepName}"失败：${error.message}`);

    // 根据错误类型决定是否继续
    if (error.isCritical) {
      throw error;
    }

    return null;
  }
}

// 步骤1：接受微信链接验证
async function validateWeChatLink(input) {
  const stepName = 'validate-link';
  const urlPattern = /^https?:\/\/\S+/i;

  if (!input || typeof input !== 'string') {
    throw new Error('输入无效：请发送有效的链接地址', true);
  }

  const urls = input.match(urlPattern);
  if (!urls || urls.length === 0) {
    throw new Error('未检测到链接：请发送包含链接的消息，支持小红书、微信公众号、网页等', true);
  }

  // 检查支持的平台
  const supportedPlatforms = ['xiaohongshu.com', 'xhslink.com', 'mp.weixin.qq.com', 'zhihu.com', 'bilibili.com', 'github.com'];
  const unsupportedUrls = urls.filter(url => !supportedPlatforms.some(platform => url.includes(platform)));

  if (unsupportedUrls.length > 0 && urls.length === unsupportedUrls.length) {
    throw new Error(`暂不支持该链接：${unsupportedUrls[0]}\n支持的平台：${supportedPlatforms.join('、')}`, true);
  }

  // 返回需要处理的URL列表
  return urls.filter(url => supportedPlatforms.some(platform => url.includes(platform)));
}

// 步骤2：内容提取（使用动态插件系统）
async function extractContentFromUrls(urls, context) {
  const extractedContents = [];
  const errors = [];

  for (const url of urls) {
    try {
      // 使用动态内容提取器
      const content = await executeStep(
        `extract-${extractorInstance.detectPlatform(url)}`,
        () => extractorInstance.extractContent(url, {
          timeout: config.basic.timeoutMs,
          maxContentLength: config.getCurrentLimits().maxContentLength
        }),
        context
      );

      if (content) {
        extractedContents.push({
          ...content,
          originalUrl: url
        });
      }
    } catch (error) {
      errors.push({
        url,
        step: 'content-extraction',
        error: error.message
      });
      console.error(`提取内容失败 - ${url}: ${error.message}`);
    }
  }

  if (extractedContents.length === 0) {
    throw new Error(`所有链接提取失败\n失败详情：\n${errors.map(e => `- ${e.url}: ${e.error}`).join('\n')}`, true);
  }

  // 提取失败但成功部分时给出警告
  if (errors.length > 0) {
    const warningMessage = createErrorMessage(
      'batch-extraction',
      new Error(`部分链接提取成功 (${extractedContents.length}/${urls.length})`),
      ErrorLevel.WARNING
    );
    context.warnings.push(warningMessage);
  }

  return extractedContents;
}

// 步骤3：分类整理
async function classifyContents(contents, context) {
  const classifiedContents = [];

  for (const content of contents) {
    try {
      const classification = await executeStep(
        'classify-content',
        () => {
          // 检查是否启用高级分类
          if (config.isFeatureEnabled('advanced-classification')) {
            return classifyContentAdvanced(content);
          } else {
            return classifyContentBasic(content);
          }
        },
        context
      );

      classifiedContents.push({
        ...content,
        classification: classification || {
          category: '灵感',
          confidence: 60,
          evidence: ['默认分类'],
          reason: '无法准确分类，使用默认分类'
        }
      });
    } catch (error) {
      console.error(`分类失败 - ${content.title}: ${error.message}`);
      classifiedContents.push({
        ...content,
        classification: {
          category: '灵感',
          confidence: 30,
          evidence: ['分类失败'],
          reason: error.message
        }
      });
    }
  }

  return classifiedContents;
}

// 基础分类实现
function classifyContentBasic(content) {
  const text = (content.title + ' ' + (content.content || '')).toLowerCase();
  const categories = config.categories;
  let bestCategory = '灵感';
  let bestScore = 0;

  for (const [category, catConfig] of Object.entries(categories)) {
    const score = catConfig.keywords.reduce((sum, keyword) => {
      return sum + (text.includes(keyword.toLowerCase()) ? 1 : 0);
    }, 0);

    if (score > bestScore) {
      bestScore = score;
      bestCategory = category;
    }
  }

  const confidence = bestScore > 0 ? Math.min(90, 50 + bestScore * 10) : 30;

  return {
    category: bestCategory,
    confidence,
    evidence: bestScore > 0 ? [`匹配到${bestScore}个相关关键词`] : [],
    reason: `基于关键词匹配，得分：${bestScore}`
  };
}

// 高级分类实现（可调用AI）
async function classifyContentAdvanced(content) {
  // 这里可以集成AI分类逻辑
  // 暂时使用基础分类的增强版
  return classifyContentBasic(content);
}

// 步骤4：理解分析并套用笔记模板
async function generateNotes(contents, context) {
  const notes = [];

  for (const content of contents) {
    try {
      const markdown = await executeStep(
        'generate-note',
        () => generateMarkdownNoteEnhanced(content, context.traceId),
        context
      );

      notes.push({
        content,
        markdown,
        fileName: generateFileName(content)
      });
    } catch (error) {
      console.error(`生成笔记失败 - ${content.title}: ${error.message}`);
      // 生成简化版笔记
      const simpleMarkdown = generateSimpleNote(content);
      notes.push({
        content,
        markdown: simpleMarkdown,
        fileName: generateFileName(content),
        isSimple: true
      });
    }
  }

  return notes;
}

// 增强的Markdon笔记生成
function generateMarkdownNoteEnhanced(content, traceId) {
  const {
    title,
    classification,
    sourceUrl,
    author,
    publishTime,
    content: text,
    platform
  } = content;

  const dateStr = new Date().toLocaleDateString('zh-CN');
  const category = classification.category;

  // 根据类型生成不同的模板
  let template = '';

  switch (platform) {
    case 'xiaohongshu':
      template = generateXiaohongshuTemplate(content);
      break;
    case 'wechat':
      template = generateWechatTemplate(content);
      break;
    case 'bilibili':
      template = generateBilibiliTemplate(content);
      break;
    case 'github':
      template = generateGithubTemplate(content);
      break;
    default:
      template = generateGenericTemplate(content);
  }

  return template;
}

// 生成文件名
function generateFileName(content) {
  const date = new Date().toISOString().slice(0, 10);
  const safeTitle = content.title.replace(/[<>:"/\\|?*]/g, '-').slice(0, 50);
  return `${date}-${safeTitle}.md`;
}

// 简化笔记生成
function generateSimpleNote(content) {
  return `# ${content.title}

**来源**：${content.sourceUrl}
**分类**：${content.classification.category}

## 内容摘要
${(content.content || '').slice(0, 500)}...

---
*由快乐小狗信息整理器自动生成*
trace_id: ${content.traceId || 'unknown'}
`;
}

// 各平台模板生成函数
function generateXiaohongshuTemplate(content) {
  return `# ${content.title}

> 📱 小红书笔记

## 基本信息
- **作者**：${content.author || '未知'}
- **发布时间**：${new Date(content.publishTime).toLocaleDateString('zh-CN')}
- **笔记链接**：${content.sourceUrl}
- **分类**：${content.classification.category}

## 内容详情
${content.content || '无内容'}

## 标签和互动
${content.tags ? `**标签**：${content.tags.join('、')}` : ''}
${content.stats ? `\n**互动数据**：\n- 👍 点赞：${content.stats.likes || 0}\n- 💬 评论：${content.stats.comments || 0}` : ''}

## 可执行建议
1. [ ] 记录核心要点和灵感
2. [ ] 思考如何应用到实际工作生活
3. [ ] 分享给相关朋友或团队

---
*分类置信度：${content.classification.confidence}%*
*分类依据：${content.classification.evidence?.join('、') || '无'}*
*由快乐小狗信息整理器自动生成*
trace_id: ${content.traceId || 'unknown'}
`;
}

function generateWechatTemplate(content) {
  return `# ${content.title}

> 📮 微信文章

## 文章信息
- **来源**：${content.source || '微信公众号'}
- **作者**：${content.author || '未知'}
- **发布时间**：new Date(content.publishTime).toLocaleDateString('zh-CN')}
- **文章链接**：${content.sourceUrl}
- **分类**：${content.classification.category}

## 核心观点
${content.summary || extractKeyPoints(content.content)}

## 详细内容
${content.content || '无内容'}

## 行动清单
1. [ ] 总结文章核心观点
2. [ ] 思考实际应用场景
3. [ ] 制定实施计划

---
*分类置信度：${content.classification.confidence}%*
*由快乐小狗信息整理器自动生成*
trace_id: ${content.traceId || 'unknown'}
`;
}

function generateBilibiliTemplate(content) {
  return `# ${content.title}

> 🎬 B站视频

## 视频信息
- **UP主**：${content.author || '未知'}
- **发布时间**：${new Date(content.publishTime).toLocaleDateString('zh-CN')}
- **视频链接**：${content.sourceUrl}
- **分类**：${content.classification.category}
- **时长**：${content.duration ? formatDuration(content.duration) : '未知'}

## 视频简介
${content.description || '暂无简介'}

## 字幕/文稿
${content.subtitles ? content.subtitles.map(s => s.text).join('\n') : '无字幕'}

## 互动数据
${content.stats ? `
- 👀 播放量：${content.stats.views || 0}
- 👍 点赞：${content.stats.likes || 0}
- 💬 评论：${content.stats.comments || 0}
- ⭐ 收藏：${content.stats.favorites || 0}` : ''}

## 学习要点
1. [ ] 整理视频知识点
2. [ ] 实践视频中提到的方法
3. [ ] 关注UP主更新

---
*分类置信度：${content.classification.confidence}%*
*由快乐小狗信息整理器自动生成*
trace_id: ${content.traceId || 'unknown'}
`;
}

function generateGithubTemplate(content) {
  return `# ${content.title}

> 💻 GitHub 项目

## 项目信息
- **作者/组织**：${content.author || '未知'}
- **项目链接**：${content.sourceUrl}
- **仓库地址**：${content.url || content.sourceUrl}
- **分类**：${content.classification.category}

## 项目简介
${content.description || '暂无简介'}

## 技术栈
${content.language ? `- 主要语言：${content.language}` : ''}
${content.topics ? `- 主题标签：${content.topics.join('、')}` : ''}

## 项目数据
${content.stats ? `
- 🌟 Stars: ${content.stats.stars || 0}
- 🍴 Forks: ${content.stats.forks || 0}
- 🐛 Issues: ${content.stats.issues || 0}` : ''}

## README 内容
${content.readme ? content.readme.slice(0, 1000) + '...' : '无README'}

## 使用建议
1. [ ] 克隆/下载项目到本地
2. [ ] 阅读文档了解使用方法
3. [ ] 根据需求进行定制修改

---
*分类置信度：${content.classification.confidence}%*
*由快乐小狗信息整理器自动生成*
trace_id: ${content.traceId || 'unknown'}
`;
}

function generateGenericTemplate(content) {
  return `# ${content.title}

> 🌐 网页内容

## 基本信息
- **来源网站**：${extractDomain(content.sourceUrl)}
- **发布时间**：${content.publishTime ? new Date(content.publishTime).toLocaleDateString('zh-CN') : '未知'}
- **页面链接**：${content.sourceUrl}
- **分类**：${content.classification.category}

## 页面内容
${content.content || '暂无内容'}

## 关键信息提取
1. [ ] 提炼核心观点
2. [ ] 记录相关链接
3. [ ] 思考实际应用

---
*分类置信度：${content.classification.confidence}%*
*分类依据：${content.classification.evidence?.join('、') || '无'}*
*由快乐小狗信息整理器自动生成*
trace_id: ${content.traceId || 'unknown'}
`;
}

// 步骤5：保存到飞书云盘
async function saveToFeishuCloud(notes, context) {
  const results = [];
  const errors = [];

  // 验证飞书配置
  const isValidConfig = feishuConfig.validate();
  if (!isValidConfig) {
    throw new Error('飞书配置无效，请检查环境变量 FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BASE_FOLDER_TOKEN', true);
  }

  for (const note of notes) {
    try {
      const result = await executeStep(
        `save-to-feishu-${note.content.platform}`,
        () => saveNoteToFeishu(note, context),
        context
      );

      if (result) {
        results.push({
          title: note.content.title,
          category: note.content.classification.category,
          ...result
        });
      }
    } catch (error) {
      errors.push({
        title: note.content.title,
        error: error.message
      });
      console.error(`保存失败 - ${note.content.title}: ${error.message}`);
    }
  }

  if (results.length === 0) {
    throw new Error(`所有笔记保存失败\n失败详情：\n${errors.map(e => `- ${e.title}: ${e.error}`).join('\n')}`, true);
  }

  // 部分失败时的处理
  if (errors.length > 0) {
    const warningMessage = createErrorMessage(
      'batch-save',
      new Error(`部分笔记保存成功 (${results.length}/${notes.length})`),
      ErrorLevel.WARNING
    );
    context.warnings.push(warningMessage);
  }

  return results;
}

// 保存单个笔记到飞书
async function saveNoteToFeishu(note, context) {
  const category = note.content.classification.category;
  const filename = note.fileName;

  // 创建或获取分类文件夹
  const folderToken = await getOrCreateCategoryFolder(category);

  // 上传文件
  const uploadResult = await uploadMarkdownFile(
    note.markdown,
    filename,
    folderToken
  );

  return {
    path: `${LARK_CONFIG.cloudDriveSpaceName}/${category}/${filename}`,
    fileUrl: uploadResult.fileUrl,
    fileToken: uploadResult.fileToken
  };
}

// 获取或创建分类文件夹
async function getOrCreateCategoryFolder(category) {
  try {
    const fileApi = larkClient?.drive?.v1?.file;
    if (!fileApi?.list || !fileApi?.createFolder) {
      throw new Error('drive file api unavailable');
    }
    const folderList = await fileApi.list({
      params: {
        folder_token: LARK_CONFIG.baseFolderToken,
        page_size: 200
      }
    });
    const entries = folderList.data?.files ?? [];
    const existingFolder = entries.find((entry) => entry.type === 'folder' && entry.name === category);
    if (existingFolder) {
      return existingFolder.token;
    }
    const newFolder = await fileApi.createFolder({
      data: {
        name: category,
        folder_token: LARK_CONFIG.baseFolderToken
      }
    });
    const token = newFolder.data?.token;
    if (!token) {
      throw new Error('missing folder token');
    }
    return token;
  } catch (error) {
    throw new Error(`创建分类文件夹失败: ${error.message}`);
  }
}

// 上传Markdown文件
async function uploadMarkdownFile(content, filename, folderToken) {
  try {
    const buffer = Buffer.from(content, 'utf8');
    const fileApi = larkClient?.drive?.v1?.file;
    if (!fileApi?.uploadAll) {
      throw new Error('drive file upload api unavailable');
    }

    const uploadResult = await fileApi.uploadAll({
      data: {
        file_name: filename,
        parent_type: 'explorer',
        parent_node: folderToken,
        size: buffer.length,
        file: buffer
      }
    });
    const uploadedFileToken = uploadResult?.file_token;
    if (!uploadedFileToken) {
      throw new Error('missing uploaded file token');
    }

    const permissionApi = larkClient?.drive?.v2?.permissionPublic;
    if (!permissionApi?.patch) {
      throw new Error('drive permission api unavailable');
    }
    await permissionApi.patch({
      path: { token: uploadedFileToken },
      params: { type: 'file' },
      data: {
        external_access_entity: 'open',
        comment_entity: 'anyone_can_view'
      }
    });

    return {
      fileUrl: `https://my.feishu.cn/drive/file/${uploadedFileToken}`,
      fileToken: uploadedFileToken
    };
  } catch (error) {
    throw new Error(`上传文件失败: ${error.message}`);
  }
}

// 获取飞书访问令牌
let larkTokenState = { token: '', expireAt: 0 };
async function getLarkTenantToken() {
  const now = Date.now();
  if (larkTokenState.token && larkTokenState.expireAt > now + 5 * 60 * 1000) {
    return larkTokenState.token;
  }

  const response = await axios.post(
    `${feishuConfig.getDriveConfig().domain}${feishuConfig.getDriveConfig().endpoints.auth}`,
    {
      app_id: LARK_CONFIG.appId,
      app_secret: LARK_CONFIG.appSecret
    }
  );

  larkTokenState = {
    token: response.data.tenant_access_token,
    expireAt: now + response.data.expire * 1000
  };

  return larkTokenState.token;
}

// 主处理函数 - 严格按照流程执行
async function main(input, context = {}) {
  // 初始化上下文
  context.trace = context.trace || [];
  context.warnings = context.warnings || [];
  context.startTime = Date.now();

  try {
    // 初始化插件系统
    await extractorInstance.initialize();

    console.log('=== 开始处理微信消息 ===');

    // 步骤1：验证微信链接
    const urls = await executeStep(
      'validate-links',
      () => validateWeChatLink(input),
      context
    );

    if (!urls || urls.length === 0) {
      throw new Error('未找到可处理的链接', true);
    }

    console.log(`待处理链接数量：${urls.length}`);

    // 步骤2：提取内容
    const contents = await executeStep(
      'extract-contents',
      () => extractContentFromUrls(urls, context),
      context
    );

    // 步骤3：分类整理
    const classifiedContents = await executeStep(
      'classify-contents',
      () => classifyContents(contents, context),
      context
    );

    // 步骤4：生成笔记
    const notes = await executeStep(
      'generate-notes',
      () => generateNotes(classifiedContents, context),
      context
    );

    // 步骤5：保存到飞书
    const saveResults = await executeStep(
      'save-to-feishu',
      () => saveToFeishuCloud(notes, context),
      context
    );

    // 构建返回消息
    const duration = Date.now() - context.startTime;
    let response = `✅ 处理完成！\n\n`;
    response += `📊 处理统计：\n`;
    response += `- 处理链接：${urls.length}\n`;
    response += `- 成功提取：${contents.length}\n`;
    response += `- 生成笔记：${notes.length}\n`;
    response += `- 保存成功：${saveResults.length}\n`;
    response += `- 处理耗时：${duration}ms\n\n`;

    response += `📁 保存位置：\n`;
    saveResults.forEach(result => {
      response += `- 【${result.title}】\n`;
      response += `  分类：${result.category}\n`;
      response += `  飞书文档：${result.fileUrl}\n\n`;
    });

    // 添加警告信息（如果有）
    if (context.warnings.length > 0) {
      response += `⚠️ 警告信息：\n`;
      response += context.warnings.map(w => w).join('\n\n');
    }

    response += `\ntrace_id: ${context.trace[0]?.traceId || 'unknown'}`;

    return response;

  } catch (error) {
    const duration = Date.now() - context.startTime;

    // 构建错误消息
    let errorMessage = `❌ 处理失败\n\n`;
    errorMessage += `错误信息：${error.message}\n`;
    errorMessage += `处理耗时：${duration}ms\n`;

    // 添加错误追踪信息
    if (context.trace.length > 0) {
      errorMessage += `\n📋 执行步骤：\n`;
      context.trace.forEach(step => {
        const status = step.status === 'completed' ? '✓' : step.status === 'failed' ? '✗' : '○';
        errorMessage += `${status} ${step.step}`;
        if (step.duration) errorMessage += ` (${step.duration})`;
        if (step.status === 'failed') errorMessage += ` - ${step.error}`;
        errorMessage += '\n';
      });
    }

    // 如果是严重错误，添加恢复建议
    if (error.isCritical || error.message.includes('配置')) {
      errorMessage += `\n🔧 恢复建议：\n`;
      errorMessage += `1. 检查网络连接是否正常\n`;
      errorMessage += `2. 确认链接是否可访问\n`;
      errorMessage += `3. 联系管理员检查配置\n`;
    }

    return errorMessage;
  }
}

// 辅助函数
function extractDomain(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return '未知站点';
  }
}

function formatDuration(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function extractKeyPoints(text) {
  if (!text) return '';
  const sentences = text.split(/[。！？.!?]/).filter(s => s.trim());
  return sentences.slice(0, 3).join('。\n') + '。';
}

// 导出
module.exports = {
  main,
  validateWeChatLink,
  extractContentFromUrls,
  classifyContents,
  generateNotes,
  saveToFeishuCloud
};
