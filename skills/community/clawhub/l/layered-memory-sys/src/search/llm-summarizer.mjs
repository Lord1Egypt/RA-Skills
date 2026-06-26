// llm-summarizer.mjs - LLM 摘要 (v1.2 功能)

import { getSessionContext } from './session-search.mjs';

// 用轻量模型总结 session
export async function summarizeSession(sessionId, options = {}) {
  const { maxLength = 100, model } = options;
  const messages = getSessionContext(sessionId, { contextSize: 20 });

  if (messages.length === 0) return null;

  // 提取对话文本
  const dialogue = messages
    .slice(0, 30)
    .map(m => `${m.role === 'user' ? '用户' : '助手'}: ${m.text.slice(0, 200)}`)
    .join('\n');

  // 摘要 prompt
  const prompt = `请用简洁的中文总结以下对话的要点（${maxLength}字以内），只提取关键信息和决策：

${dialogue}

摘要：`;

  // 调用 LLM（优先用免费模型）
  try {
    const summary = await callLLM(prompt, model);
    return summary;
  } catch (e) {
    console.warn('LLM 摘要失败:', e.message);
    // fallback：提取前几条消息的关键词
    return extractFallbackSummary(messages, maxLength);
  }
}

// 调用 LLM
async function callLLM(prompt, modelName) {
  // 优先使用豆包免费模型（已有 API key）
  const apiKeys = {
    doubao: process.env.DOUBAO_API_KEY || '',
    dashscope: process.env.DASHSCOPE_API_KEY || '',
  };

  // 豆包 API
  if (apiKeys.doubao) {
    const res = await fetch('https://ark.cn-beijing.volces.com/api/v3/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKeys.doubao}`,
      },
      body: JSON.stringify({
        model: modelName || 'doubao-seed-1-6-flash-250828',
        messages: [{ role: 'user', content: prompt }],
        max_tokens: maxLength || 200,
      }),
    });

    if (res.ok) {
      const data = await res.json();
      return data.choices?.[0]?.message?.content?.trim();
    }
  }

  // 通义 API
  if (apiKeys.dashscope) {
    const res = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKeys.dashscope}`,
      },
      body: JSON.stringify({
        model: modelName || 'qwen-turbo',
        messages: [{ role: 'user', content: prompt }],
        max_tokens: maxLength || 200,
      }),
    });

    if (res.ok) {
      const data = await res.json();
      return data.choices?.[0]?.message?.content?.trim();
    }
  }

  throw new Error('无可用的 LLM API');
}

// Fallback 摘要：提取关键词组合
function extractFallbackSummary(messages, maxLength) {
  const topics = new Set();
  const topicPatterns = [
    /(?:关于|讨论|做了|完成|实现)(.{2,10})/g,
    /(?:技能|记忆|系统|配置|服务|数据库|搜索)/g,
  ];

  for (const msg of messages.slice(0, 10)) {
    for (const p of topicPatterns) {
      let m;
      while ((m = p.exec(msg.text)) !== null) {
        topics.add(m[1] || m[0]);
      }
    }
  }

  const topicList = Array.from(topics).slice(0, 5);
  if (topicList.length === 0) return messages[0]?.text?.slice(0, maxLength) || '';

  return `对话涉及: ${topicList.join('、')}`;
}