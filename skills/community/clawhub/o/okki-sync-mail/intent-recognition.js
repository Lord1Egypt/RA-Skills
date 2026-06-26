#!/usr/bin/env node

/**
 * 邮件意图识别模块
 * 使用 LLM 对邮件主题和正文进行分类
 * 返回：{ intent, confidence, key_entities, language }
 */

const fs = require('fs');
const path = require('path');

// 加载 intent schema
const SCHEMA_PATH = path.join(__dirname, 'config', 'intent-schema.json');
let intentSchema = null;

function loadSchema() {
  if (!intentSchema) {
    try {
      intentSchema = JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
    } catch (err) {
      console.error('❌ 无法加载 intent schema:', err.message);
      intentSchema = { intents: [], default_intent: { id: 'unknown' } };
    }
  }
  return intentSchema;
}

/**
 * 获取 intent 配置
 */
function getIntentConfig(intentId) {
  const schema = loadSchema();
  const intent = schema.intents.find(i => i.id === intentId);
  return intent || schema.default_intent;
}

/**
 * 使用关键词进行初步意图匹配（作为 LLM 的补充/降级方案）
 */
function keywordMatch(subject, body) {
  const schema = loadSchema();
  const text = `${subject} ${body}`.toLowerCase();
  
  let bestMatch = null;
  let bestScore = 0;
  
  for (const intent of schema.intents) {
    let score = 0;
    
    // 匹配英文关键词
    for (const keyword of intent.keywords_en) {
      if (text.includes(keyword.toLowerCase())) {
        score += 1;
      }
    }
    
    // 匹配中文关键词
    for (const keyword of intent.keywords_zh) {
      if (text.includes(keyword)) {
        score += 1;
      }
    }
    
    if (score > bestScore) {
      bestScore = score;
      bestMatch = intent.id;
    }
  }
  
  // 归一化置信度
  const confidence = bestScore > 0 ? Math.min(bestScore / 5, 0.7) : 0;
  
  return {
    intent: bestMatch || 'unknown',
    confidence,
    method: 'keyword'
  };
}

/**
 * 使用 LLM 进行意图分类
 * 调用 OpenRouter API (claude-sonnet-4)
 */
async function classifyWithLLM(subject, body) {
  const schema = loadSchema();
  
  const intentList = schema.intents.map(i => 
    `- ${i.id}: ${i.name_en} (${i.name_zh})`
  ).join('\n');
  
  const prompt = `You are an email intent classifier for a B2B electronics company (Farreach Electronic - HDMI/DP/USB cables).

Classify the following email into ONE of these intents:
${intentList}

Return ONLY a JSON object with this structure:
{
  "intent": "<intent_id>",
  "confidence": <0.0-1.0>,
  "key_entities": ["entity1", "entity2"],
  "language": "en|zh|other",
  "reasoning": "<brief explanation>"
}

Email to classify:
Subject: ${subject}
Body: ${body.slice(0, 2000)}

Classification:`;

  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
        'HTTP-Referer': 'https://farreach-electronic.com',
        'X-Title': 'Farreach EmailIntent',
      },
      body: JSON.stringify({
        model: 'anthropic/claude-sonnet-4',
        messages: [
          {
            role: 'system',
            content: 'You are an email intent classifier. Return ONLY valid JSON. No markdown, no explanations outside the JSON.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.1,
        max_tokens: 200
      })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    const content = data.choices?.[0]?.message?.content || '{}';
    
    // 解析 JSON（可能包含 markdown 代码块）
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    const jsonStr = jsonMatch ? jsonMatch[0] : content;
    const result = JSON.parse(jsonStr);
    
    return {
      intent: result.intent || 'unknown',
      confidence: result.confidence || 0.5,
      key_entities: result.key_entities || [],
      language: result.language || 'en',
      reasoning: result.reasoning || '',
      method: 'llm'
    };
  } catch (err) {
    console.error('⚠️  LLM 分类失败，降级到关键词匹配:', err.message);
    return keywordMatch(subject, body);
  }
}

/**
 * 主分类函数
 * 结合 LLM 和关键词匹配
 */
async function classifyIntent(subject, body) {
  console.log('🔍 开始意图识别...');
  console.log(`   主题：${subject?.slice(0, 50) || '无'}`);
  
  // 调用 LLM 分类
  const llmResult = await classifyWithLLM(subject || '', body || '');
  
  console.log(`🎯 意图识别结果:`);
  console.log(`   Intent: ${llmResult.intent}`);
  console.log(`   Confidence: ${(llmResult.confidence * 100).toFixed(1)}%`);
  console.log(`   Language: ${llmResult.language}`);
  console.log(`   Method: ${llmResult.method}`);
  if (llmResult.key_entities?.length > 0) {
    console.log(`   Entities: ${llmResult.key_entities.join(', ')}`);
  }
  
  return llmResult;
}

module.exports = {
  classifyIntent,
  getIntentConfig,
  keywordMatch,
  loadSchema
};
