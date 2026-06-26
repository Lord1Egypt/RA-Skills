/**
 * MiMo 联网搜索技能
 * 使用小米 MiMo 模型的联网搜索功能进行实时信息搜索
 */

const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

/**
 * 调用 MiMo 联网搜索 API
 * @param {string|Object} query - 搜索查询内容或配置对象
 * @returns {Promise<Object>} 搜索结果
 */
async function mimoWebSearch(query) {
  // 解析参数
  let config = {
    model: 'mimo-v2-flash',
    maxTokens: 1024,
    temperature: 1.0,
    topP: 0.95,
    maxKeyword: 3,
    forceSearch: true,
    limit: 1
  };

  if (typeof query === 'string') {
    config.query = query;
  } else if (typeof query === 'object') {
    config = { ...config, ...query };
  } else {
    throw new Error('Invalid query parameter');
  }

  // 检查 API Key
  const apiKey = process.env.MIMO_API_KEY;
  if (!apiKey) {
    throw new Error('MIMO_API_KEY environment variable is not set');
  }

  // 构建请求数据
  const requestData = {
    model: config.model,
    messages: [
      {
        role: 'user',
        content: config.query
      }
    ],
    tools: [
      {
        type: 'web_search',
        max_keyword: config.maxKeyword,
        force_search: config.forceSearch,
        limit: config.limit
      }
    ],
    max_completion_tokens: config.maxTokens,
    temperature: config.temperature,
    top_p: config.topP,
    stream: false,
    thinking: {
      type: 'disabled'
    }
  };

  // 构建 curl 命令
  const curlCommand = `curl -X POST "https://api.xiaomimimo.com/v1/chat/completions" \
    -H "api-key: ${apiKey}" \
    -H "Content-Type: application/json" \
    -d '${JSON.stringify(requestData)}'`;

  try {
    // 执行 curl 命令
    const { stdout, stderr } = await execPromise(curlCommand);

    if (stderr) {
      console.error('Curl stderr:', stderr);
    }

    // 解析响应
    const response = JSON.parse(stdout);

    if (response.error) {
      throw new Error(`API Error: ${response.error.message}`);
    }

    return {
      success: true,
      content: response.choices[0].message.content,
      usage: response.usage,
      citations: response.choices[0].annotations || []
    };
  } catch (error) {
    console.error('MiMo Web Search Error:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 批量搜索多个查询
 * @param {Array<string>} queries - 查询数组
 * @returns {Promise<Array<Object>>} 搜索结果数组
 */
async function batchMimoWebSearch(queries) {
  const results = [];
  for (const query of queries) {
    const result = await mimoWebSearch(query);
    results.push({ query, result });
  }
  return results;
}

/**
 * 搜索并格式化结果
 * @param {string} query - 搜索查询
 * @returns {Promise<string>} 格式化后的搜索结果
 */
async function searchAndFormat(query) {
  const result = await mimoWebSearch(query);

  if (!result.success) {
    return `搜索失败: ${result.error}`;
  }

  let formatted = `## 搜索结果\n\n`;
  formatted += `**查询**: ${query}\n\n`;
  formatted += `**结果**:\n${result.content}\n\n`;

  if (result.citations && result.citations.length > 0) {
    formatted += `**来源**:\n`;
    result.citations.forEach((citation, index) => {
      formatted += `${index + 1}. [${citation.title}](${citation.url})\n`;
    });
  }

  return formatted;
}

module.exports = {
  mimoWebSearch,
  batchMimoWebSearch,
  searchAndFormat
};