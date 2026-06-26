#!/usr/bin/env node

/**
 * MCP-Storyboard: 多场景分镜图片生成 MCP 服务器
 *
 * 功能：调用 BizyAir 异步 API 生成故事绘本分镜场景图
 * 支持：模特提示词自动追加、尺寸映射、批量生成
 *
 * @version 2.1.0
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ErrorCode,
  McpError
} from '@modelcontextprotocol/sdk/types.js';

// ============ 配置常量 ============
const CONFIG = {
  API_BASE: 'https://api.bizyair.cn/w/v1/webapp/task/openapi',
  WEB_APP_ID: 38223,
  DEFAULT_WIDTH: 928,
  DEFAULT_HEIGHT: 1664,
  DEFAULT_BATCH_SIZE: 4,
  MAX_BATCH_SIZE: 10,

  // 超时配置
  CREATE_TIMEOUT: 30000,      // 创建任务超时 30 秒
  POLL_TIMEOUT: 900000,       // 轮询超时 15 分钟（支持 3-10 分钟的长时任务）
  POLL_INTERVAL: 5000,        // 轮询间隔 5 秒
  PROGRESS_INTERVAL: 30000,   // 进度提示间隔 30 秒
  QUERY_TIMEOUT: 20000,       // 单次查询超时 20 秒

  // 重试配置
  MAX_RETRIES: 3,
  RETRY_DELAY: 2000,

  // 尺寸映射表 (比例 -> [width, height])
  SIZE_MAP: {
    '1:1': [1240, 1240],
    '4:3': [1080, 1440],
    '3:4': [1440, 1080],
    '9:16': [928, 1664],
    '16:9': [1664, 928],
    '1:2': [870, 1740],
    '2:1': [1740, 870],
    '1:3': [720, 2160],
    '3:1': [2160, 720],
    '2:3': [960, 1440],
    '3:2': [1440, 960],
    '2:5': [720, 1800],
    '5:2': [1800, 720],
    '3:5': [960, 1600],
    '5:3': [1600, 960],
    '4:5': [1080, 1350],
    '5:4': [1350, 1080]
  },

  // 模特触发关键词
  MODEL_KEYWORDS: {
    zh: ['模特', '人物', '人像', '女性', '女士', '女孩', '美女', '穿搭', '展示', '试穿'],
    en: ['model', 'woman', 'female', 'girl', 'portrait', 'character', 'person']
  },

  // 模特追加提示词
  MODEL_SUFFIX: ',漏斗身材，大胸展示，moweifei，feifei 妃妃,一位大美女，完美身材，写实人像写真、中式风格、韩式写真、人像写真，氛围海报，艺术摄影,a photo-realistic shoot from a front camera angle about a young woman , a 20-year-old asian woman with light skin and brown hair styled in a single hair bun, looking directly at the camera with a neutral expression, '
};

// ============ 工具函数 ============

/**
 * 等延时的工具函数
 * @param {number} ms - 毫秒数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 记录日志到 stderr（MCP 标准输出方式）
 * @param {string} level - 日志级别
 * @param {string} message - 日志消息
 */
function log(level, message) {
  const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
  console.error(`[${timestamp}] [${level}] ${message}`);
}

/**
 * 检测是否包含模特相关关键词
 * @param {string} text - 用户输入文本
 * @returns {boolean}
 */
function hasModelKeyword(text) {
  if (!text) return false;
  const lowerText = text.toLowerCase();

  // 检查中文关键词
  for (const kw of CONFIG.MODEL_KEYWORDS.zh) {
    if (text.includes(kw)) return true;
  }

  // 检查英文关键词
  for (const kw of CONFIG.MODEL_KEYWORDS.en) {
    if (lowerText.includes(kw)) return true;
  }

  return false;
}

/**
 * 处理 prompt：自动追加模特提示词
 * @param {string} prompt - 原始 prompt
 * @returns {string}
 */
function processPrompt(prompt) {
  if (!prompt) return '';

  if (hasModelKeyword(prompt)) {
    // 避免重复追加
    if (!prompt.includes('moweifei') && !prompt.includes('elegant woman')) {
      log('INFO', '检测到模特关键词，已追加优化提示词');
      return prompt + CONFIG.MODEL_SUFFIX;
    }
  }
  return prompt;
}

/**
 * 解析尺寸参数
 * @param {string} ratio - 比例字符串
 * @param {number} width - 宽度
 * @param {number} height - 高度
 * @returns {{width: number, height: number}}
 */
function parseSize(ratio, width, height) {
  // 优先使用用户指定的具体宽高
  if (width && height) {
    return {
      width: Math.min(Math.max(parseInt(width), 256), 4096),
      height: Math.min(Math.max(parseInt(height), 256), 4096)
    };
  }

  // 根据比例映射
  if (ratio && CONFIG.SIZE_MAP[ratio]) {
    const [w, h] = CONFIG.SIZE_MAP[ratio];
    return { width: w, height: h };
  }

  // 默认尺寸
  return {
    width: CONFIG.DEFAULT_WIDTH,
    height: CONFIG.DEFAULT_HEIGHT
  };
}

// ============ BizyAir API 调用 ============

/**
 * 创建异步图片生成任务
 * @param {Object} params - 请求参数
 * @returns {Promise<string>} - requestId
 */
async function createAsyncTask(params) {
  const { apiKey, prompt, width, height, batchSize } = params;

  const url = `${CONFIG.API_BASE}/create`;
  const requestBody = {
    web_app_id: CONFIG.WEB_APP_ID,
    suppress_preview_output: true,
    input_values: {
      '107:BizyAirSiliconCloudLLMAPI.user_prompt': prompt,
      '81:EmptySD3LatentImage.width': width,
      '81:EmptySD3LatentImage.height': height,
      '81:EmptySD3LatentImage.batch_size': batchSize
    }
  };

  log('INFO', `创建任务: ${prompt.substring(0, 50)}...`);
  log('DEBUG', `请求参数: ${width}x${height}, batch=${batchSize}`);

  let lastError;
  for (let attempt = 1; attempt <= CONFIG.MAX_RETRIES; attempt++) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
          'X-Bizyair-Task-Async': 'enable'
        },
        body: JSON.stringify(requestBody),
        signal: AbortSignal.timeout(CONFIG.CREATE_TIMEOUT)
      });

      if (!response.ok) {
        const errorText = await response.text().catch(() => 'unknown error');
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const result = await response.json();

      // 提取 requestId（支持多种命名格式）
      const requestId = result.requestId || result.request_id;

      if (!requestId) {
        log('ERROR', `响应中未找到 requestId: ${JSON.stringify(result)}`);
        throw new Error('API 响应格式错误：缺少 requestId');
      }

      log('INFO', `任务已创建: ${requestId}`);
      return requestId;

    } catch (error) {
      lastError = error;

      if (attempt < CONFIG.MAX_RETRIES) {
        log('WARN', `创建失败，第 ${attempt} 次重试... (${error.message})`);
        await sleep(CONFIG.RETRY_DELAY);
      }
    }
  }

  throw new Error(`创建任务失败（已重试 ${CONFIG.MAX_RETRIES} 次）: ${lastError.message}`);
}

/**
 * 轮询任务状态直到完成
 * @param {string} apiKey - API 密钥
 * @param {string} requestId - 任务 ID
 * @returns {Promise<boolean>}
 */
async function pollTaskStatus(apiKey, requestId) {
  const url = `${CONFIG.API_BASE}/detail`;
  const startTime = Date.now();
  let lastProgressTime = startTime;

  log('INFO', '⏳ 开始轮询任务状态（预计 3-10 分钟，请耐心等待）...');

  let pollCount = 0;
  const maxPolls = Math.ceil(CONFIG.POLL_TIMEOUT / CONFIG.POLL_INTERVAL);

  while (true) {
    pollCount++;
    const elapsed = Date.now() - startTime;
    const elapsedMinutes = (elapsed / 60000).toFixed(1);

    // 检查超时
    if (elapsed > CONFIG.POLL_TIMEOUT) {
      throw new Error(`任务轮询超时（${CONFIG.POLL_TIMEOUT / 60000} 分钟）`);
    }

    // 定期输出进度（每 30 秒）
    const now = Date.now();
    if (now - lastProgressTime >= CONFIG.PROGRESS_INTERVAL) {
      log('INFO', `⏱️ 任务进行中... 已等待 ${elapsedMinutes} 分钟 (轮询 ${pollCount}/${maxPolls})`);
      lastProgressTime = now;

      // 发送心跳通知，确保 MCP 连接保持活跃
      console.error(JSON.stringify({
        type: 'progress',
        elapsed: elapsed,
        elapsedMinutes: elapsedMinutes,
        pollCount: pollCount,
        maxPolls: maxPolls
      }));
    }

    try {
      const response = await fetch(`${url}?requestId=${encodeURIComponent(requestId)}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${apiKey}`
        },
        signal: AbortSignal.timeout(CONFIG.QUERY_TIMEOUT)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const result = await response.json();
      const data = result.data || {};
      const status = data.status;

      log('DEBUG', `[${pollCount}] 任务状态: ${status} (${elapsedMinutes}分钟)`);

      // 任务完成
      if (status === 'Success') {
        log('INFO', `✅ 任务完成（总耗时 ${elapsedMinutes} 分钟，轮询 ${pollCount} 次）`);
        return true;
      }

      // 任务失败
      if (status === 'Failed' || status === 'Canceled') {
        const errorInfo = data.error_info || {};
        const errorMsg = errorInfo.message || errorInfo.error_type || '未知错误';
        log('ERROR', `任务${status}: ${errorMsg}`);
        throw new Error(`任务${status}: ${errorMsg}`);
      }

      // 任务进行中，继续等待
      await sleep(CONFIG.POLL_INTERVAL);

    } catch (error) {
      // 如果是网络错误或超时，记录后继续轮询
      if (error.name === 'AbortError' || error.message.includes('timeout') || error.message.includes('HTTP')) {
        log('WARN', `[${pollCount}] 查询失败，继续轮询... (${error.message})`);
        await sleep(CONFIG.POLL_INTERVAL);
        continue;
      }
      // 其他错误直接抛出
      throw error;
    }
  }
}

/**
 * 获取任务结果
 * @param {string} apiKey - API 密钥
 * @param {string} requestId - 任务 ID
 * @returns {Promise<Array<string>>} - 图片 URL 列表
 */
async function getTaskResults(apiKey, requestId) {
  const url = `${CONFIG.API_BASE}/outputs`;

  log('INFO', '获取任务结果...');

  const response = await fetch(`${url}?requestId=${encodeURIComponent(requestId)}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${apiKey}`
    },
    signal: AbortSignal.timeout(30000)
  });

  if (!response.ok) {
    throw new Error(`获取结果失败: HTTP ${response.status}`);
  }

  const result = await response.json();
  const outputs = result.data?.outputs || [];

  const imageUrls = outputs
    .filter(item => item.audit_status === 2 && item.object_url)
    .map(item => item.object_url);

  log('INFO', `获取到 ${imageUrls.length} 张图片`);

  if (imageUrls.length === 0) {
    log('WARN', '未获取到有效的图片 URL');
  }

  return imageUrls;
}

/**
 * 完整的异步图片生成流程
 * @param {Object} params - 请求参数
 * @returns {Promise<Array<string>>} - 图片 URL 列表
 */
async function generateImages(params) {
  const { apiKey, prompt, width, height, batchSize } = params;

  // 步骤 1: 创建异步任务
  const requestId = await createAsyncTask({ apiKey, prompt, width, height, batchSize });

  // 步骤 2: 轮询任务状态
  await pollTaskStatus(apiKey, requestId);

  // 步骤 3: 获取结果
  const imageUrls = await getTaskResults(apiKey, requestId);

  return imageUrls;
}

// ============ MCP Server 初始化 ============

const server = new Server(
  {
    name: 'storyboard-mcp',
    version: '2.1.0'
  },
  {
    capabilities: {
      tools: {}
    }
  }
);

// 注册工具列表
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'generate_image',
        description: '生成故事绘本分镜场景图，支持模特提示词自动追加、尺寸控制和批量生成',
        inputSchema: {
          type: 'object',
          properties: {
            prompt: {
              type: 'string',
              description: '图片生成描述内容（中文或英文）'
            },
            ratio: {
              type: 'string',
              description: '图片比例，如 "9:16", "1:1" 等（可选，默认 9:16）',
              enum: Object.keys(CONFIG.SIZE_MAP)
            },
            width: {
              type: 'integer',
              description: '图片宽度（像素），指定后 ratio 失效（可选）',
              minimum: 256,
              maximum: 4096
            },
            height: {
              type: 'integer',
              description: '图片高度（像素），指定后 ratio 失效（可选）',
              minimum: 256,
              maximum: 4096
            },
            batch_size: {
              type: 'integer',
              description: '生成批次数量，默认 4，最大 10',
              minimum: 1,
              maximum: CONFIG.MAX_BATCH_SIZE,
              default: CONFIG.DEFAULT_BATCH_SIZE
            },
            skip_model_append: {
              type: 'boolean',
              description: '是否跳过模特提示词自动追加（默认 false）',
              default: false
            }
          },
          required: ['prompt']
        }
      }
    ]
  };
});

// 处理工具调用
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name !== 'generate_image') {
    throw new McpError(
      ErrorCode.MethodNotFound,
      `未知工具: ${name}`
    );
  }

  try {
    // 1. 参数校验
    if (!args?.prompt) {
      throw new McpError(
        ErrorCode.InvalidParams,
        '缺少必需参数: prompt'
      );
    }

    // 2. 获取 API Key
    const apiKey = process.env.BIZYAIR_API_KEY;
    if (!apiKey) {
      log('ERROR', 'BIZYAIR_API_KEY 未设置');
      throw new McpError(
        ErrorCode.InternalError,
        '服务器配置错误: BIZYAIR_API_KEY 环境变量未设置'
      );
    }

    // 3. 处理 prompt（模特提示词追加）
    let finalPrompt = args.prompt;
    if (!args.skip_model_append) {
      finalPrompt = processPrompt(args.prompt);
    }

    // 4. 解析尺寸参数
    const { width, height } = parseSize(
      args.ratio,
      args.width,
      args.height
    );

    // 5. 解析批次参数
    const batchSize = Math.min(
      Math.max(parseInt(args.batch_size) || CONFIG.DEFAULT_BATCH_SIZE, 1),
      CONFIG.MAX_BATCH_SIZE
    );

    // 6. 调用异步 API 生成图片
    log('INFO', '🚀 开始图片生成任务...');
    log('INFO', '💡 图片生成通常需要 3-10 分钟，请耐心等待，期间会定期输出进度');
    const imageUrls = await generateImages({
      apiKey,
      prompt: finalPrompt,
      width,
      height,
      batchSize
    });

    // 7. 构造返回结果
    const result = {
      content: [
        {
          type: 'text',
          text: `✅ 成功生成 ${imageUrls.length} 张图片\n\n` +
                `📐 尺寸: ${width}×${height}\n` +
                `🔄 批次: ${batchSize}\n` +
                `🎨 Prompt: ${finalPrompt.substring(0, 100)}${finalPrompt.length > 100 ? '...' : ''}\n`
        }
      ]
    };

    // 添加图片 URL 列表
    if (imageUrls.length > 0) {
      const urlList = imageUrls.map((url, idx) =>
        `${idx + 1}. ${url}`
      ).join('\n');
      result.content.push({
        type: 'text',
        text: `\n🔗 图片 URL 列表:\n${urlList}`
      });
    }

    log('INFO', `任务完成，返回 ${imageUrls.length} 个图片 URL`);
    return result;

  } catch (error) {
    log('ERROR', `任务失败: ${error.message}`);

    if (error instanceof McpError) {
      throw error;
    }

    return {
      content: [
        {
          type: 'text',
          text: `❌ 图片生成失败: ${error.message}\n\n` +
                `💡 建议:\n` +
                `• 检查 BIZYAIR_API_KEY 是否有效\n` +
                `• 简化 prompt 描述内容\n` +
                `• 调整尺寸或批次参数后重试\n` +
                `• 图片生成通常需要 3-10 分钟，如超时可能是服务器繁忙，请稍后再试\n` +
                `• 如持续失败，请联系技术支持`
        }
      ]
    };
  }
});

// ============ 服务器启动 ============

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  log('INFO', '🚀 storyboard-mcp 服务器已启动');
  log('INFO', `📦 支持工具: generate_image`);
  log('INFO', `🔑 API Key: ${process.env.BIZYAIR_API_KEY ? '✓ 已配置' : '✗ 未配置'}`);
  log('INFO', `📐 默认尺寸: ${CONFIG.DEFAULT_WIDTH}×${CONFIG.DEFAULT_HEIGHT}`);
  log('INFO', `🔄 默认批次: ${CONFIG.DEFAULT_BATCH_SIZE} (最大 ${CONFIG.MAX_BATCH_SIZE})`);
  log('INFO', `⏱️ 轮询超时: ${CONFIG.POLL_TIMEOUT / 60000} 分钟 (支持 3-10 分钟长时任务)`);
  log('INFO', `💡 进度提示: 每 ${CONFIG.PROGRESS_INTERVAL / 1000} 秒输出一次`);
}

main().catch((error) => {
  log('ERROR', `💥 服务器启动失败: ${error.message}`);
  process.exit(1);
});

// 优雅退出处理
process.on('SIGINT', () => {
  log('INFO', '👋 接收到退出信号，正在关闭服务器...');
  server.close();
  process.exit(0);
});
