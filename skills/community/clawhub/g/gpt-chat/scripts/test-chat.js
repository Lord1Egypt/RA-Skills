const https = require('https');
const API_KEY = process.env.OPENAI_API_KEY || '';

const postData = JSON.stringify({
  model: 'gpt-4o-mini',
  messages: [{ role: 'user', content: 'hi' }],
  max_tokens: 5
});

const options = {
  hostname: 'api.openai.com',
  path: '/v1/chat/completions',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Length': Buffer.byteLength(postData)
  }
};

console.log('Testing chat API...');

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    try {
      const json = JSON.parse(data);
      if (json.error) {
        console.log('Error:', json.error.type, '-', json.error.message);
      } else if (json.choices && json.choices[0]) {
        console.log('Success! Response:', json.choices[0].message.content);
      } else {
        console.log('Response:', data.slice(0, 300));
      }
    } catch (e) {
      console.log('Parse error:', e.message);
      console.log('Raw response:', data.slice(0, 200));
    }
  });
});

req.on('error', (e) => {
  console.log('Request error:', e.message);
});

req.write(postData);
req.end();
