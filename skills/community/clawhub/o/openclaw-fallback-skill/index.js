const axios = require('axios');

class OpenClawFallbackSkill {
  constructor(config) {
    this.config = config;
    this.name = 'openclaw-fallback-skill';
    this.conversationHistory = new Map(); // 存储会话上下文
  }

  /**
   * 初始化技能
   */
  async init() {
    console.log('[FallbackSkill] 初始化完成');
    console.log(`[FallbackSkill] 配置的 API: ${this.config.apiUrl}`);
    
    // 验证 API 连接
    await this.testConnection();
  }

  /**
   * 测试 API 连接
   */
  async testConnection() {
    try {
      const testResult = await this.callCloudModel({
        messages: [{ role: 'user', content: 'ping' }],
        max_tokens: 5
      });
      console.log('[FallbackSkill] API 连接测试成功');
    } catch (error) {
      console.error('[FallbackSkill] API 连接测试失败:', error.message);
      // 不抛出错误，允许继续运行
    }
  }

  /**
   * 事件处理器：在模型响应前检查
   */
  async onBeforeResponse(context) {
    const { userMessage, localResponse, confidence } = context;

    // 检查是否需要 fallback
    const needsFallback = this.shouldFallback(localResponse, confidence);

    if (needsFallback) {
      console.log('[FallbackSkill] 检测到本地模型回答质量不足，触发 fallback');
      
      const cloudResponse = await this.getCloudResponse(userMessage, context);
      
      if (cloudResponse) {
        // 替换响应为云端模型的结果
        context.response = cloudResponse;
        context.usedFallback = true;
        context.fallbackModel = this.config.modelName;
      }
    }

    return context;
  }

  /**
   * 判断是否需要 fallback
   */
  shouldFallback(response, confidence) {
    // 场景1: 置信度过低
    if (confidence && confidence < this.config.fallbackThreshold) {
      return true;
    }

    // 场景2: 响应内容为空或太短
    if (!response || response.length < 10) {
      return true;
    }

    // 场景3: 包含无法回答的关键词
    const unableKeywords = [
      '无法回答', '不能回答', '不知道', 'not sure', 
      "i don't know", "can't answer", "unable to"
    ];
    
    const lowerResponse = response.toLowerCase();
    if (unableKeywords.some(keyword => lowerResponse.includes(keyword))) {
      return true;
    }

    // 场景4: 响应内容过于通用（如"这是一个好问题"但没有实质内容）
    const genericPatterns = [
      /^这是一个好问题/,
      /^that's a good question/,
      /^i understand/
    ];
    
    if (genericPatterns.some(pattern => pattern.test(response))) {
      return true;
    }

    return true;
  }

  /**
   * 调用云端大模型
   */
  async getCloudResponse(userMessage, context) {
    const sessionId = context.sessionId || 'default';
    
    // 获取会话历史
    let history = this.conversationHistory.get(sessionId) || [];
    
    // 构建消息列表
    const messages = [
      {
        role: 'system',
        content: this.buildSystemPrompt(context)
      },
      ...history.slice(-10), // 保留最近10条对话
      {
        role: 'user',
        content: userMessage
      }
    ];

    // 尝试调用 API，支持重试
    for (let attempt = 1; attempt <= this.config.maxRetries; attempt++) {
      try {
        const response = await this.callCloudModel({
          messages,
          temperature: 0.7,
          max_tokens: 2000,
          stream: this.config.enableStreaming
        });

        // 更新历史
        history.push(
          { role: 'user', content: userMessage },
          { role: 'assistant', content: response }
        );
        this.conversationHistory.set(sessionId, history);

        return response;
      } catch (error) {
        console.error(`[FallbackSkill] API 调用失败 (尝试 ${attempt}/${this.config.maxRetries}):`, error.message);
        
        if (attempt === this.config.maxRetries) {
          // 所有重试都失败，返回友好的错误提示
          return this.getFallbackErrorMessage(error);
        }
        
        // 等待后重试
        await this.sleep(1000 * attempt);
      }
    }

    return null;
  }

  /**
   * 调用云端模型 API
   */
  async callCloudModel(params) {
    const { apiUrl, apiKey, modelName, timeout } = this.config;
    
    // 根据不同的 API 格式构建请求
    const requestBody = this.buildApiRequestBody(params, modelName);
    
    const response = await axios({
      method: 'post',
      url: apiUrl,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        ...this.getCustomHeaders()
      },
      data: requestBody,
      timeout: timeout * 1000
    });

    // 解析不同 API 格式的响应
    return this.parseApiResponse(response.data);
  }

  /**
   * 构建 API 请求体（支持多种格式）
   */
  buildApiRequestBody(params, modelName) {
    // OpenAI 兼容格式
    if (this.config.apiUrl.includes('openai') || this.config.apiUrl.includes('v1/chat')) {
      return {
        model: modelName,
        messages: params.messages,
        temperature: params.temperature || 0.7,
        max_tokens: params.max_tokens || 2000,
        stream: params.stream || false
      };
    }
    
    // Claude/Anthropic 格式
    if (this.config.apiUrl.includes('anthropic')) {
      return {
        model: modelName,
        messages: params.messages,
        max_tokens: params.max_tokens || 2000,
        temperature: params.temperature || 0.7,
        stream: params.stream || false
      };
    }
    
    // 通用格式（可自定义）
    return {
      model: modelName,
      messages: params.messages,
      ...params
    };
  }

  /**
   * 解析 API 响应
   */
  parseApiResponse(data) {
    // OpenAI 格式
    if (data.choices && data.choices[0] && data.choices[0].message) {
      return data.choices[0].message.content;
    }
    
    // Claude 格式
    if (data.content && data.content[0] && data.content[0].text) {
      return data.content[0].text;
    }
    
    // 其他格式，尝试直接提取
    if (data.response) return data.response;
    if (data.text) return data.text;
    if (data.result) return data.result;
    
    // 如果都不匹配，返回原始数据
    return JSON.stringify(data);
  }

  /**
   * 构建系统提示词
   */
  buildSystemPrompt(context) {
    const basePrompt = `你是一个智能助手，正在帮助用户解决问题。
请提供准确、详细、有帮助的回答。
如果问题涉及实时信息或你不确定的内容，请诚实说明。`;

    // 如果有上下文信息，添加到提示词中
    if (context.metadata && context.metadata.userInfo) {
      return `${basePrompt}\n\n用户信息: ${JSON.stringify(context.metadata.userInfo)}`;
    }

    return basePrompt;
  }

  /**
   * 获取自定义请求头
   */
  getCustomHeaders() {
    const headers = {};
    
    // 如果配置中有额外 headers
    if (this.config.customHeaders) {
      Object.assign(headers, this.config.customHeaders);
    }
    
    return headers;
  }

  /**
   * 获取 fallback 失败时的错误消息
   */
  getFallbackErrorMessage(error) {
    const errorMessages = {
      'ECONNREFUSED': '无法连接到云端模型服务，请检查网络和 API 地址',
      'ETIMEDOUT': '云端模型响应超时，请稍后再试',
      '401': 'API 密钥无效，请检查配置',
      '403': 'API 密钥权限不足',
      '429': 'API 请求频率超限，请稍后再试'
    };
    
    let errorKey = error.code || (error.response?.status);
    let message = errorMessages[errorKey] || `云端模型调用失败: ${error.message}`;
    
    return `⚠️ ${message}\n\n建议：检查您的 API 配置或稍后重试。`;
  }

  /**
   * 清理会话历史（可选）
   */
  clearHistory(sessionId) {
    if (sessionId) {
      this.conversationHistory.delete(sessionId);
    } else {
      this.conversationHistory.clear();
    }
  }

  /**
   * 休眠函数
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * 技能卸载时的清理
   */
  async destroy() {
    console.log('[FallbackSkill] 清理会话历史');
    this.conversationHistory.clear();
  }
}

// 导出技能
module.exports = OpenClawFallbackSkill;