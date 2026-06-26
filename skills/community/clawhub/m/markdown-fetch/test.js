/**
 * 测试 Markdown Fetch 功能
 * 
 * 运行: node test-markdown-fetch.js
 */

const { optimizedFetch, DEFAULT_HEADERS } = require('./index');

const TEST_URLS = [
  'https://example.com',  // 普通网站
  'https://cloudflare.com', // Cloudflare 托管
];

async function runTests() {
  console.log('🧪 Markdown Fetch 测试\n');
  console.log('默认 Headers:', DEFAULT_HEADERS);
  console.log('---\n');

  for (const url of TEST_URLS) {
    console.log(`📡 Fetching: ${url}`);
    
    try {
      const result = await optimizedFetch(url);
      
      console.log(`   Status: ${result.status}`);
      console.log(`   Format: ${result.format}`);
      console.log(`   Content-Type: ${result.contentType}`);
      
      if (result.tokensSaved) {
        console.log(`   💰 Token 节省: ${result.tokensSaved}`);
      }
      
      const preview = result.content ? result.content.substring(0, 100) : 'N/A';
      console.log(`   Preview: ${preview}...`);
      console.log('');
      
    } catch (error) {
      console.log(`   ❌ Error: ${error.message}`);
      console.log('');
    }
  }
}

// 如果直接运行
if (require.main === module) {
  runTests();
}

module.exports = { runTests };
