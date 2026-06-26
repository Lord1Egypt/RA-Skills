const https = require('https');

function fetchTokenSecurity(address, chainId = '56') {
  return new Promise((resolve, reject) => {
    const url = `https://api.gopluslabs.io/api/v1/token_security/${chainId}?contract_addresses=${address}`;
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const result = json.result[address];
          if (!result) {
            reject(new Error('代币信息未找到'));
            return;
          }

          const isHoneypot = result.is_honeypot === '1';
          const isMintable = result.is_mintable === '1';
          const buyTax = parseFloat(result.buy_tax);
          const sellTax = parseFloat(result.sell_tax);
          const ownerPercent = parseFloat(result.owner_percent);
          const holders = parseInt(result.holder_count);
          const isOpenSource = result.is_open_source === '1';

          let score = 0;
          if (isHoneypot) score += 100;
          if (isMintable) score += 30;
          if (buyTax > 10 || sellTax > 10) score += 30;
          if (ownerPercent > 5) score += 20;
          if (holders < 1000) score += 15;
          if (!isOpenSource) score += 10;

          let riskLevel = 'Low';
          if (score >= 80) riskLevel = 'Critical';
          else if (score >= 50) riskLevel = 'High';
          else if (score >= 20) riskLevel = 'Medium';

          resolve({
            riskLevel,
            score,
            isHoneypot,
            isMintable,
            buyTax,
            sellTax,
            ownerPercent,
            holders,
            isOpenSource,
          });
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

// 测试地址（USDT）
const testAddress = '0x55d398326f99059ff775485246999027b3197955';
fetchTokenSecurity(testAddress).then(result => {
  console.log('\n✅ 检测结果:');
  console.log(`代币地址: ${testAddress}`);
  console.log(`风险等级: ${result.riskLevel}`);
  console.log(`总分: ${result.score}`);
  console.log(`\n详情:`);
  console.log(`- 蜜罐: ${result.isHoneypot ? '是' : '否'}`);
  console.log(`- 可增发: ${result.isMintable ? '是' : '否'}`);
  console.log(`- 买入税: ${result.buyTax}%`);
  console.log(`- 卖出税: ${result.sellTax}%`);
  console.log(`- 部署者持有比例: ${result.ownerPercent}%`);
  console.log(`- 持币地址数: ${result.holders}`);
  console.log(`- 开源: ${result.isOpenSource ? '是' : '否'}`);
}).catch(err => console.error('错误:', err.message));
