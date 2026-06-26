#!/usr/bin/env node
/**
 * ouyi-api.js — Direct call to Ouyi API
 * Usage: node ouyi-api.js "your question"
 * Returns: JSON {content, reasoningTokens, error}
 */

const https = require('https');

const API_KEY = process.env.OUYI_API_KEY || 'your-api-key-here';
const MODEL = 'ouyi-openclaw';

function chat(messages) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      model: MODEL,
      messages: messages
    });

    const options = {
      hostname: 'api.rcouyi.com',
      port: 443,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          const content = parsed.choices?.[0]?.message?.content || '';
          const reasoningTokens = parsed.usage?.completion_tokens_details?.reasoning_tokens || 0;
          
          if (parsed.error) {
            resolve({ content: null, reasoningTokens: 0, error: parsed.error.message || JSON.stringify(parsed.error) });
          } else {
            resolve({ content: content, reasoningTokens, model: parsed.model, error: null });
          }
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}. Response: ${data.slice(0, 300)}`));
        }
      });
    });

    req.on('error', e => reject(e));
    req.setTimeout(90000, () => { req.destroy(); reject(new Error('Request timeout (>90s)')); });
    req.write(postData);
    req.end();
  });
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(JSON.stringify({ error: 'No question provided. Usage: node ouyi-api.js "your question"' }));
    process.exit(1);
  }

  // Check if input is a JSON string (from piped input)
  let question;
  try {
    const input = args.join(' ');
    const parsed = JSON.parse(input);
    question = parsed.prompt || parsed.question || parsed.content || input;
  } catch {
    question = args.join(' ');
  }

  const systemPrompt = 'You are a helpful assistant. Reply in the same language as the user question.';
  
  try {
    const result = await chat([
      { role: 'system', content: systemPrompt },
      { role: 'user', content: question }
    ]);
    
    console.log(JSON.stringify(result));
  } catch (e) {
    console.log(JSON.stringify({ content: null, reasoningTokens: 0, error: e.message }));
    process.exit(1);
  }
}

main();
