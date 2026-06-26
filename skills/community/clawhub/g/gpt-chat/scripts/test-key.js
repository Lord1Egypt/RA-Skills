const https = require('https');
const API_KEY = process.env.OPENAI_API_KEY || '';

console.log('Testing API key...');

const req = https.get(`https://api.openai.com/v1/models`, {
  headers: {
    'Authorization': `Bearer ${API_KEY}`
  }
}, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    try {
      const json = JSON.parse(data);
      if (json.error) {
        console.log('Error:', json.error.message);
      } else {
        console.log('API key is valid!');
        console.log('Available models:', json.data?.slice(0, 5).map(m => m.id).join(', '));
      }
    } catch (e) {
      console.log('Response:', data.slice(0, 200));
    }
  });
});

req.on('error', (e) => {
  console.log('Network error:', e.message);
});
