const { countTokens } = require('gpt-tokenizer');

class TaskAnalyzer {
  constructor() {
    this.sensitivePatterns = [
      /password/i,
      /api[_-]?key/i, 
      /secret/i,
      /token/i,
      /credential/i,
      /auth/i,
      /login/i,
      /access[_-]?key/i,
      /private[_-]?key/i,
      /sk-[a-zA-Z0-9]{20,}/i // OpenAI-style API keys
    ];
    
    this.taskTypeKeywords = {
      long_document: [/总结|分析|文档|长文本|报告|论文|研究/i],
      creative_writing: [/创意|写作|故事|生成|创作|文案|营销/i],
      coding: [/代码|编程|调试|开发|实现|算法|函数/i],
      general: [/一般|普通|日常|简单|基本/i]
    };
  }

  analyzeTask(prompt, context = "", requirements = {}) {
    const contextLength = this.estimateContextLength(prompt, context);
    const privacyLevel = this.detectPrivacyLevel(prompt);
    const taskType = this.classifyTaskType(prompt);
    
    let reason = "";
    if (privacyLevel === 'high') {
      reason = "privacy sensitive content detected";
    } else if (contextLength > 32768) {
      reason = "large context requirement";
    } else {
      reason = "general purpose routing";
    }
    
    return {
      contextLength,
      privacyLevel,
      taskType,
      costSensitivity: requirements.costSensitive || false,
      performanceCritical: requirements.performanceCritical || false,
      reason
    };
  }
  
  estimateContextLength(prompt, context) {
    try {
      // Use precise token counting for better accuracy
      const promptTokens = countTokens(prompt);
      const contextTokens = countTokens(context);
      return promptTokens + contextTokens;
    } catch (error) {
      // Fallback to character-based estimation
      console.warn("Token counting failed, using fallback method");
      return Math.floor((prompt + context).length / 4);
    }
  }
  
  detectPrivacyLevel(prompt) {
    // Enhanced privacy detection with multiple checks
    const lowerPrompt = prompt.toLowerCase();
    
    // Check for sensitive patterns
    const hasSensitivePattern = this.sensitivePatterns.some(pattern => 
      pattern.test(prompt)
    );
    
    // Check for common sensitive contexts
    const sensitiveContexts = [
      'my password is',
      'api key',
      'secret key', 
      'access token',
      'authentication',
      'login credentials'
    ];
    
    const hasSensitiveContext = sensitiveContexts.some(ctx => 
      lowerPrompt.includes(ctx)
    );
    
    return (hasSensitivePattern || hasSensitiveContext) ? 'high' : 'low';
  }
  
  classifyTaskType(prompt) {
    const lowerPrompt = prompt.toLowerCase();
    
    // Check each task type
    for (const [type, patterns] of Object.entries(this.taskTypeKeywords)) {
      if (patterns.some(pattern => pattern.test(lowerPrompt))) {
        return type;
      }
    }
    
    // Default to general if no specific type matches
    return 'general';
  }
}

module.exports = TaskAnalyzer;