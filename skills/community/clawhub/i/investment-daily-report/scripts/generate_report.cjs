#!/usr/bin/env node
// 投研日报生成器 v1.2.0
// 架构：Node.js 主控 → 通过 Gateway localhost:19000 代理调用 NeoData API
// 关键修复：直接用 Node.js 发 HTTP 请求，无需 Python 脚本（绕过 PowerShell/Python 编码地狱）
// Usage: node generate_report.cjs [--market cn|hk|us|all] [--quick] [--output path]

const https = require('https');
const http = require('http');
const path = require('path');
const fs = require('fs');
const zlib = require('zlib');
const os = require('os');

const TEMP = process.env.TEMP || os.tmpdir();
const TODAY = new Date().toISOString().slice(0, 10);

// ============ CLI ============
let market = 'all', quick = false, outputPath = '';
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--market' && args[i + 1]) market = args[++i].toLowerCase();
  else if (args[i] === '--quick') quick = true;
  else if (args[i] === '--output' && args[i + 1]) outputPath = args[++i];
}

// ============ HTTP via Gateway ============
// Gateway 在 localhost:19000 监听 HTTP/HTTPS，通过 proxy/api 代理 API 请求
// Remote-URL header 告诉 Gateway 目标服务
function apiQuery(queryText) {
  return new Promise((resolve) => {
    const body = JSON.stringify({
      channel: "neodata",
      sub_channel: "qclaw",
      query: queryText,
      request_id: "r" + Date.now(),
      data_type: "api",
      se_params: {},
      extra_params: {}
    });

    const reqOpts = {
      hostname: 'localhost',
      port: 19000,
      path: '/proxy/api',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        'Remote-URL': 'https://jprx.m.qq.com/aizone/skillserver/v1/proxy/teamrouter_neodata/query',
        'Accept-Encoding': 'identity'   // 禁止压缩，由 Gateway 处理
      }
    };

    const req = http.request(reqOpts, (res) => {
      // Gateway 可能返回 gzip，手动解压缩
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        // Gateway 自动解压缩，但以防万一这里也处理
        let text;
        try {
          text = buf.toString('utf8');
          // 去掉 BOM
          if (text.charCodeAt(0) === 0xFEFF) text = text.slice(1);
        } catch (e) {
          resolve({ error: '解码失败: ' + e.message, recalls: [] });
          return;
        }

        try {
          const parsed = JSON.parse(text);
          const recalls = parsed?.data?.apiData?.apiRecall || [];
          // 也提取 docData 中的文档标题和摘要
          const docs = [];
          const docGroups = parsed?.data?.docData?.docRecall || [];
          for (const g of docGroups) {
            for (const doc of (g.docList || []).slice(0, 3)) {
              docs.push({ type: 'doc', title: doc.title || '', summary: (doc.summary || '').slice(0, 300) });
            }
          }
          resolve([...recalls, ...docs]);
        } catch (e) {
          // JSON 解析失败，打印前 200 字符用于调试
          resolve({ error: 'JSON解析失败: ' + e.message + ' | 响应片段: ' + text.slice(0, 200), recalls: [] });
        }
      });
    });

    req.on('error', (e) => resolve({ error: '请求失败: ' + e.message, recalls: [] }));
    req.setTimeout(20000, () => { req.destroy(); resolve({ error: '请求超时', recalls: [] }); });
    req.write(body);
    req.end();
  });
}

// ============ Content formatter ============
function fmt(content, maxLen = 1000) {
  if (!content) return '暂无数据';
  return content.replace(/\r/g, '').replace(/\n{3,}/g, '\n\n').trim().slice(0, maxLen);
}

// ============ Main ============
async function main() {
  console.log('📊 投研日报生成器 v1.2.0');
  console.log(`📅 ${TODAY}  |  市场: ${market === 'all' ? 'A股+港股+美股' : market.toUpperCase()}  |  ${quick ? '⚡快速' : '📋完整'}\n`);

  const queries = [
    { key: 'cn_overview', label: 'A股大盘',        q: '今日A股三大指数收盘行情涨跌幅成交额上证指数深证成指创业板科创50' },
    { key: 'hk_overview', label: '港股大盘',        q: '今日港股恒生指数恒生科技指数国企指数收盘涨跌幅成交额' },
    { key: 'us_overview', label: '美股大盘',        q: '今日美股道琼斯纳斯达克标普500收盘行情涨跌幅' },
    { key: 'cn_sectors',  label: '板块轮动',        q: '今日A股涨幅前五跌幅前五板块行业名称涨跌幅资金流入' },
    { key: 'cn_flow',     label: '资金流向',        q: '北向资金今日买卖沪股通深股通' },
    { key: 'cn_stocks',   label: '个股异动',        q: 'A股涨停板今日' },
    { key: 'events',      label: '重要公告',        q: '今日A股重要公告业绩预告增减持重大事项' },
    { key: 'macro',       label: '宏观商品',        q: '今日美元人民币汇率黄金原油期货价格' },
  ];

  const activeKeys = [];
  if (market === 'all' || market === 'cn') {
    activeKeys.push('cn_overview');
    if (!quick) activeKeys.push('cn_sectors', 'cn_flow', 'cn_stocks', 'events');
  }
  if (market === 'all' || market === 'hk') activeKeys.push('hk_overview');
  if (market === 'all' || market === 'us') activeKeys.push('us_overview');
  if (!quick) activeKeys.push('macro');

  const results = {};
  let ok = 0, failed = [];

  for (const k of activeKeys) {
    const qDef = queries.find(q => q.key === k);
    process.stdout.write(`  🔍 ${qDef.label}...`);
    const data = await apiQuery(qDef.q);

    if (data.error) {
      console.log(` ✗ (${data.error})`);
      failed.push({ key: k, err: data.error });
      results[k] = [];
    } else if (Array.isArray(data) && data.length > 0) {
      results[k] = data;
      console.log(` ✓ (${data.length}条)`);
      ok++;
    } else {
      console.log(' ✗ (无数据)');
      failed.push({ key: k, err: '无返回数据' });
      results[k] = [];
    }
  }

  // ============ Build Markdown ============
  let md = `# 投研日报 | ${TODAY}\n\n`;
  md += `> 自动生成于 ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n\n`;
  md += `---\n\n`;

  if (results.cn_overview?.length > 0) {
    md += `## 📈 A股大盘\n\n`;
    for (const b of results.cn_overview.slice(0, 2)) {
      if (b.content) md += fmt(b.content) + '\n\n';
    }
  }
  if (!quick && results.cn_sectors?.length > 0) {
    md += `## 🔥 板块轮动\n\n`;
    md += fmt(results.cn_sectors[0]?.content || '', 1500) + '\n\n';
  }
  if (!quick && results.cn_flow?.length > 0) {
    md += `## 💰 资金流向\n\n`;
    md += fmt(results.cn_flow[0]?.content || '', 1200) + '\n\n';
  }
  if (!quick && results.cn_stocks?.length > 0) {
    md += `## 🚨 个股异动\n\n`;
    md += fmt(results.cn_stocks[0]?.content || '', 1200) + '\n\n';
  }
  if (!quick && results.events?.length > 0) {
    md += `## 📢 重要公告\n\n`;
    for (const b of results.events.slice(0, 3)) {
      if (b.title || b.summary) md += `- **${b.title || ''}** ${b.summary || ''}\n`;
      else if (b.content) md += fmt(b.content, 300) + '\n';
    }
    md += '\n';
  }
  if (results.hk_overview?.length > 0) {
    md += `## 🇭🇰 港股大盘\n\n`;
    md += fmt(results.hk_overview[0]?.content || '', 1000) + '\n\n';
  }
  if (results.us_overview?.length > 0) {
    md += `## 🇺🇸 美股大盘\n\n`;
    md += fmt(results.us_overview[0]?.content || '', 1000) + '\n\n';
  }
  if (!quick && results.macro?.length > 0) {
    md += `## 🌍 大宗商品与汇率\n\n`;
    md += fmt(results.macro[0]?.content || '', 800) + '\n\n';
  }

  md += `---\n\n`;
  md += `*📊 数据来源：NeoData Financial Search*\n`;
  md += `*⚠️ 免责声明：以上内容仅供参考，不构成投资建议。*\n`;
  if (failed.length > 0) {
    md += `\n⚠️ ${failed.length} 项查询失败：\n`;
    for (const f of failed) md += `  - ${f.key}: ${f.err}\n`;
  }

  // outputPath 可能是目录，需要拼接文件名
  let outPath;
  if (outputPath) {
    const stat = fs.existsSync(outputPath) ? fs.statSync(outputPath) : null;
    if (stat && stat.isDirectory()) {
      outPath = path.join(outputPath, `investment-report-${TODAY}.md`);
    } else {
      outPath = outputPath;
    }
  } else {
    outPath = path.join(process.cwd(), `investment-report-${TODAY}.md`);
  }
  fs.writeFileSync(outPath, md, 'utf8');
  console.log(`\n✅ 日报已生成: ${outPath}`);
  console.log(`📊 查询: ${ok}/${activeKeys.length} 成功  |  📝 ${(Buffer.byteLength(md) / 1024).toFixed(1)} KB`);
  if (failed.length > 0) {
    console.log(`⚠️ 失败项:`);
    for (const f of failed) console.log(`  - ${f.key}: ${f.err}`);
  }
}

main().catch(e => { console.error('❌ 错误:', e.message); process.exit(1); });
