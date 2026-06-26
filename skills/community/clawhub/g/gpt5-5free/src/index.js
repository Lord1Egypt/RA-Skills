/**
 * gpt5.5free - 免费使用 GPT-5.5 示例
 */

// 使用 OpenRouter 免费模型或其他免费 API
const API_URL = process.env.OPENROUTER_API_URL || 'https://openrouter.ai/api/v1/chat/completions';
const API_KEY = process.env.OPENROUTER_API_KEY;

async function chat(prompt, model = 'meta-llama/llama-4-maverick:free') {
  if (!API_KEY) {
    console.error('Error: 请设置 OPENROUTER_API_KEY 环境变量');
    process.exit(1);
  }

  const res = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`,
      'HTTP-Referer': 'https://github.com/leic8959/gpt5.5free',
      'X-Title': 'gpt5.5free'
    },
    body: JSON.stringify({
      model,
      messages: [{ role: 'user', content: prompt }]
    })
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`API Error ${res.status}: ${err}`);
  }

  const data = await res.json();
  return data.choices?.[0]?.message?.content || 'No response';
}

// CLI 入口
if (require.main === module) {
  const prompt = process.argv[2] || 'Hello';
  chat(prompt).then(console.log).catch(console.error);
}

module.exports = { chat };
