const https = require('https');

const apiKey = process.env.OUTLINE_API_KEY;
const outlineUrl = process.env.OUTLINE_URL.replace('/mcp', '/api');

async function getDocument(id) {
  const url = `${outlineUrl}/documents.info`;
  const data = JSON.stringify({ id });
  
  const options = {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(url, options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(JSON.parse(body)));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

const documentId = process.argv[2];
if (!documentId) {
  console.error("Error: Document ID is required.");
  process.exit(1);
}

getDocument(documentId).then(doc => {
  console.log(doc.data.text);
}).catch(console.error);
