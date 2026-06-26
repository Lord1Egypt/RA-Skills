import { Skill, Context, Next } from '@openclaw/core';
import https from 'https';

interface TokenResult {
  riskLevel: string;
  score: number;
  isHoneypot: boolean;
  isMintable: boolean;
  buyTax: number;
  sellTax: number;
  ownerPercent: number;
  holders: number;
  isOpenSource: boolean;
}

function fetchTokenSecurity(address: string, chainId: string = '56'): Promise<TokenResult> {
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

export default new Skill({
  name: 'token-safety',
  description: '检测 BSC 代币风险（土狗扫描）',
  async run(ctx: Context, next: Next) {
    const address = ctx.args.address as string;
    if (!address) {
      ctx.reply('请提供代币合约地址，例如：0x...');
      return next();
    }

    try {
      const result = await fetchTokenSecurity(address);
      const message = `
🔍 代币检测结果 (${address})
风险等级: ${result.riskLevel}
总分: ${result.score}

📊 详情:
- 蜜罐风险: ${result.isHoneypot ? '⚠️ 是' : '✅ 否'}
- 是否可增发: ${result.isMintable ? '⚠️ 是' : '✅ 否'}
- 买入税: ${result.buyTax}%
- 卖出税: ${result.sellTax}%
- 部署者持有比例: ${result.ownerPercent}%
- 持币地址数: ${result.holders}
- 合约是否开源: ${result.isOpenSource ? '✅ 是' : '⚠️ 否'}
      `;
      ctx.reply(message);
    } catch (err) {
      ctx.reply(`检测失败: ${err.message}`);
    }
    return next();
  },
});