/**
 * summarize.js - 内容总结模块
 * 
 * 使用 AI 生成内容摘要和关键知识点
 * 支持调用外部 AI 服务或本地总结
 */

/**
 * 生成内容摘要
 * @param {Object} content - 内容对象 {title, content, description}
 * @param {number} maxLength - 最大长度
 * @returns {string} 摘要文本
 */
function generateSummary(content, maxLength = 500) {
  const { title, content: body, description } = content;
  
  // 优先使用描述
  if (description && description.length > 50) {
    return truncateText(description, maxLength);
  }
  
  // 从正文提取摘要
  if (body && body.length > 100) {
    // 提取前几句作为摘要
    const sentences = body.split(/[。！？.!?]/).filter(s => s.trim().length > 10);
    
    if (sentences.length > 0) {
      let summary = '';
      for (const sentence of sentences) {
        const newSummary = summary + sentence.trim() + '。';
        if (newSummary.length > maxLength) {
          break;
        }
        summary = newSummary;
      }
      
      if (summary.length > 50) {
        return summary;
      }
    }
    
    // 如果句子提取失败，直接截断
    return truncateText(body, maxLength);
  }
  
  // 只有标题的情况
  if (title) {
    return `关于"${title}"的内容。`;
  }
  
  return '暂无摘要';
}

/**
 * 提取关键知识点
 * @param {Object} content - 内容对象
 * @param {number} maxPoints - 最大知识点数量
 * @returns {Array<string>} 知识点列表
 */
function extractKeyPoints(content, maxPoints = 5) {
  const { title, content: body, tags } = content;
  const keyPoints = [];
  
  // 从标签提取
  if (tags && tags.length > 0) {
    for (const tag of tags.slice(0, maxPoints)) {
      keyPoints.push(`关键词：${tag.replace(/^#/, '')}`);
    }
  }
  
  // 从正文提取关键句
  if (body && body.length > 200) {
    const sentences = body.split(/[。！？.!?]/).filter(s => s.trim().length > 20);
    
    // 简单启发式：选择包含关键词的句子
    const importantWords = ['重要', '关键', '核心', '主要', '首先', '其次', '最后', '注意', '提示', '总结'];
    
    for (const sentence of sentences) {
      if (keyPoints.length >= maxPoints) break;
      
      const isImportant = importantWords.some(word => sentence.includes(word));
      if (isImportant && !keyPoints.includes(sentence.trim())) {
        keyPoints.push(sentence.trim());
      }
    }
    
    // 如果还不够，添加前几句
    while (keyPoints.length < maxPoints && sentences.length > keyPoints.length) {
      const nextSentence = sentences[keyPoints.length].trim();
      if (nextSentence.length > 20 && !keyPoints.includes(nextSentence)) {
        keyPoints.push(nextSentence);
      }
    }
  }
  
  // 如果还是空的，基于标题生成
  if (keyPoints.length === 0 && title) {
    keyPoints.push(`主题：${title}`);
    keyPoints.push('详细内容请查看原文');
  }
  
  return keyPoints.slice(0, maxPoints);
}

/**
 * 生成标签
 * @param {Object} content - 内容对象
 * @param {number} maxTags - 最大标签数量
 * @returns {Array<string>} 标签列表
 */
function generateTags(content, maxTags = 5) {
  const { title, content: body, keywords, platform } = content;
  const tags = new Set();
  
  // 使用已有标签
  if (content.tags && content.tags.length > 0) {
    for (const tag of content.tags.slice(0, maxTags)) {
      tags.add(tag.replace(/^#/, ''));
    }
  }
  
  // 使用关键词
  if (keywords && keywords.length > 0) {
    for (const kw of keywords.slice(0, maxTags)) {
      tags.add(kw.trim());
    }
  }
  
  // 从标题提取
  if (title) {
    const titleWords = title.split(/\s+/).filter(w => w.length > 1);
    for (const word of titleWords.slice(0, 3)) {
      tags.add(word);
    }
  }
  
  // 添加平台标签
  if (platform) {
    tags.add(platform);
  }
  
  return Array.from(tags).slice(0, maxTags);
}

/**
 * 截断文本
 * @param {string} text - 待截断文本
 * @param {number} maxLength - 最大长度
 * @returns {string} 截断后的文本
 */
function truncateText(text, maxLength) {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - 3) + '...';
}

/**
 * 完整处理流程
 * @param {Object} content - 抓取的内容
 * @returns {Object} 处理后的内容
 */
function processContent(content) {
  const summary = generateSummary(content);
  const keyPoints = extractKeyPoints(content);
  const tags = generateTags(content);
  
  return {
    ...content,
    summary,
    keyPoints,
    tags,
    processedAt: new Date().toISOString()
  };
}

/**
 * 调用 AI 服务进行总结（可选）
 * 如果有 AI 服务配置，可以使用更智能的总结
 * @param {Object} content - 内容对象
 * @param {Object} aiConfig - AI 服务配置
 * @returns {Promise<Object>} AI 处理结果
 */
async function aiSummarize(content, aiConfig = null) {
  // 如果没有配置 AI 服务，使用本地总结
  if (!aiConfig) {
    return processContent(content);
  }
  
  // 这里可以集成各种 AI 服务
  // 例如：调用 OpenAI、Claude、文心一言等
  // 由于需要 API key，这里提供框架
  
  try {
    // 示例：调用 AI 服务的伪代码
    // const response = await fetch(aiConfig.endpoint, {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     'Authorization': `Bearer ${aiConfig.apiKey}`
    //   },
    //   body: JSON.stringify({
    //     prompt: `请总结以下内容，提取关键知识点：\n\n标题：${content.title}\n内容：${content.content?.substring(0, 2000)}`,
    //     max_tokens: 500
    //   })
    // });
    // const result = await response.json();
    // return {
    //   ...content,
    //   summary: result.summary,
    //   keyPoints: result.keyPoints,
    //   tags: result.tags
    // };
    
    // 暂时返回本地总结
    return processContent(content);
  } catch (error) {
    console.error('AI 总结失败，使用本地总结:', error.message);
    return processContent(content);
  }
}

// 导出模块
module.exports = {
  generateSummary,
  extractKeyPoints,
  generateTags,
  processContent,
  aiSummarize,
  truncateText
};

// CLI 模式支持
if (require.main === module) {
  const testContent = {
    title: process.argv[2] || '测试标题',
    content: process.argv[3] || '这是一段测试内容，用于演示总结功能。这里应该有一些重要的知识点和关键信息。',
    description: process.argv[4] || '',
    tags: ['#测试', '#演示'],
    keywords: ['测试', '演示', '功能']
  };
  
  const result = processContent(testContent);
  
  console.log('\n=== 总结结果 ===\n');
  console.log(`标题：${result.title}`);
  console.log(`\n摘要:\n${result.summary}`);
  console.log(`\n关键知识点:`);
  for (const point of result.keyPoints) {
    console.log(`  - ${point}`);
  }
  console.log(`\n标签：${result.tags.join(' ')}`);
}
