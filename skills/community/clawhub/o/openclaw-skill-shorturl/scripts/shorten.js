/**
 * ShortURL - 短网址生成
 * 用法: node shorten.js <长网址> [域名] [自定义后缀]
 */

const https = require('https');

function shortenUrl(longUrl, domain = 'https://surl.bot/', backHalf = '', memberId = '') {
  return new Promise((resolve, reject) => {
    const apiUrl = 'https://www.shorturl.bot/api/urls/shorturl';
    
    const payload = JSON.stringify({
      url: longUrl,
      domain: domain,
      backHalf: backHalf,
      memberId: memberId
    });

    const req = https.request(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.short) {
            resolve({
              short_url: result.short,
              original_url: result.url,
              id: result.id || '',
              timestamp: result._ts || '',
              owner_id: result.ownerId || '',
              ip: result.submitterIp || ''
            });
          } else {
            reject(new Error('缩短失败'));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// CLI 入口
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('用法: node shorten.js <长网址> [域名] [自定义后缀]');
  process.exit(1);
}

const url = args[0];
const domain = args[1] || 'https://surl.bot/';
const backHalf = args[2] || '';

shortenUrl(url, domain, backHalf)
  .then(result => {
    // 默认只输出短网址
    console.log(result.short_url);
  })
  .catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
