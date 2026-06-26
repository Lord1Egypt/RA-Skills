const fs = require('fs');
const https = require('https');

const API_KEY = process.env.OPENAI_API_KEY || '';
const API_BASE = process.env.OPENAI_API_BASE || 'api.openai-proxy.org';
const MODEL = 'gpt-5.1';

const prompt = `请写一篇关于人工智能对职场影响的深度分析文章，3000字左右。要求：
1. 分5个章节
2. 每个章节600字左右
3. 包含具体案例
4. 分析AI对不同行业的影响
5. 讨论人类如何应对AI带来的变革

请用Markdown格式输出，章节标题用##开头。`;

function callOpenAI(message) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      model: MODEL,
      messages: [{ role: 'user', content: message }],
      max_completion_tokens: 8000
    });

    const options = {
      hostname: API_BASE,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.error) {
            reject(new Error(result.error.message));
          } else {
            resolve(result.choices[0].message.content);
          }
        } catch (e) {
          reject(new Error('Parse error: ' + e.message));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function main() {
  console.log('Generating article...');
  const content = await callOpenAI(prompt);
  
  // Save to file
  const filename = 'ai-future-article.md';
  fs.writeFileSync(filename, content);
  console.log(`Article saved to: ${filename}`);
  console.log(`Length: ${content.length} characters`);
}

main().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
