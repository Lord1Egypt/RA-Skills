// notion-sync.js — 坦坦 Notion 同步工具
// 用法: node notion-sync.js write <标题> <内容> [类型] [标签] [状态]
//        node notion-sync.js list [数量]
//        node notion-sync.js recent [天数]

const fs = require('fs');
const path = require('path');
const https = require('https');

// === 配置 ===
const configPath = path.join(process.env.USERPROFILE || '', '.config', 'notion');
const API_KEY = fs.readFileSync(path.join(configPath, 'api_key'), 'utf8').trim();
const DB_ID = fs.readFileSync(path.join(configPath, 'db_id'), 'utf8').trim();
const DS_ID = fs.readFileSync(path.join(configPath, 'ds_id'), 'utf8').trim();

// Notion API 封装
function notion(method, urlPath, body) {
  return new Promise((resolve, reject) => {
    const opts = {
      hostname: 'api.notion.com',
      path: urlPath,
      method: method,
      headers: {
        'Authorization': 'Bearer ' + API_KEY,
        'Notion-Version': '2025-09-03',
        'Content-Type': 'application/json'
      }
    };
    const req = https.request(opts, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error('Parse error: ' + data.substring(0, 200))); }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// 获取今天的日期字符串
function today() {
  const d = new Date();
  const tz = d.getTime() + (d.getTimezoneOffset() * 60000) + (8 * 3600000); // Asia/Shanghai
  const cn = new Date(tz);
  return cn.toISOString().split('T')[0];
}

// === 命令: 写入记录 ===
async function writeRecord(title, content, type, tags, status) {
  const result = await notion('POST', '/v1/pages', {
    parent: { database_id: DB_ID },
    properties: {
      'Name': { title: [{ text: { content: title || today() + ' 记录' } }] },
      '日期': { date: { start: today() } },
      '类型': { select: { name: type || '每日记录' } },
      '内容': { rich_text: [{ text: { content: content || '' } }] },
      '标签': { multi_select: (tags || '').split(',').filter(Boolean).map(t => ({ name: t.trim() })) },
      '状态': { select: { name: status || '待同步' } }
    }
  });
  if (result.object === 'error') {
    console.error('❌ 写入失败:', result.message);
    process.exit(1);
  }
  console.log('✅ 记录已写入: ' + title);
  console.log('   类型: ' + (type || '每日记录'));
  console.log('   标签: ' + (tags || '(无)'));
  console.log('   状态: ' + (status || '待同步'));
}

// === 命令: 列出记录 ===
async function listRecords(count) {
  const result = await notion('POST', '/v1/data_sources/' + DS_ID + '/query', {
    sorts: [{ property: '日期', direction: 'descending' }],
    page_size: count || 10
  });

  if (!result.results || result.results.length === 0) {
    console.log('📭 暂无记录');
    return;
  }

  console.log('\n📋 坦坦·工作日志 — 最近的 ' + result.results.length + ' 条记录\n');
  result.results.forEach((r, i) => {
    const p = r.properties;
    const title = (p.Name && p.Name.title && p.Name.title[0]) ? p.Name.title[0].text.content : '(无标题)';
    const date = (p['日期'] && p['日期'].date) ? p['日期'].date.start : '--';
    const type = (p['类型'] && p['类型'].select) ? p['类型'].select.name : '--';
    const tags = (p['标签'] && p['标签'].multi_select) ? p['标签'].multi_select.map(t => t.name).join(', ') : '';
    const status = (p['状态'] && p['状态'].select) ? p['状态'].select.name : '--';
    const content = (p['内容'] && p['内容'].rich_text && p['内容'].rich_text[0]) ? p['内容'].rich_text[0].text.content.substring(0, 80) + '...' : '';

    console.log('  #' + (i + 1) + '  ' + date + '  [' + type + ']');
    console.log('      ' + title);
    if (content) console.log('      ' + content);
    if (tags) console.log('      🏷️ ' + tags);
    console.log('      📎 ' + status);
    console.log('');
  });
}

// === 命令: 最近N天的记录(文件写入) ===
async function recentDays(days) {
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - (days || 7));
  const startStr = startDate.toISOString().split('T')[0];

  const result = await notion('POST', '/v1/data_sources/' + DS_ID + '/query', {
    filter: { property: '日期', date: { on_or_after: startStr } },
    sorts: [{ property: '日期', direction: 'descending' }]
  });

  if (!result.results || result.results.length === 0) {
    console.log('📭 最近 ' + (days || 7) + ' 天没有记录');
    return;
  }

  let output = '# 坦坦同步 - 最近' + (days || 7) + '天\n\n';
  result.results.forEach(r => {
    const p = r.properties;
    const title = (p.Name && p.Name.title && p.Name.title[0]) ? p.Name.title[0].text.content : '(无标题)';
    const date = (p['日期'] && p['日期'].date) ? p['日期'].date.start : '--';
    const type = (p['类型'] && p['类型'].select) ? p['类型'].select.name : '--';
    const content = (p['内容'] && p['内容'].rich_text) ? p['内容'].rich_text.map(t => t.text.content).join('') : '';
    const tags = (p['标签'] && p['标签'].multi_select) ? p['标签'].multi_select.map(t => t.name).join(', ') : '';

    output += '## ' + date + ' | ' + type + ' | ' + title + '\n\n';
    if (content) output += content + '\n\n';
    if (tags) output += '标签: ' + tags + '\n\n';
    output += '---\n\n';
  });

  console.log(output);
}

// === MAIN ===
async function main() {
  const cmd = process.argv[2];

  if (!cmd || cmd === 'help') {
    console.log('\n📝 坦坦 Notion 同步工具\n');
    console.log('用法:');
    console.log('  写记录:   node notion-sync.js write \"标题\" \"内容\" [类型] [标签] [状态]');
    console.log('  列记录:   node notion-sync.js list [数量]');
    console.log('  近况:     node notion-sync.js recent [天数]');
    console.log('  帮助:     node notion-sync.js help\n');
    console.log('示例:');
    console.log('  write \"2026-05-27 记录\" \"今天改了UI和扫\" \"每日记录\" \"驿站系统,UI改版\" \"待同步\"');
    return;
  }

  if (cmd === 'write') {
    await writeRecord(process.argv[3], process.argv[4], process.argv[5], process.argv[6], process.argv[7]);
  } else if (cmd === 'list') {
    await listRecords(parseInt(process.argv[3]) || 10);
  } else if (cmd === 'recent') {
    await recentDays(parseInt(process.argv[3]) || 7);
  } else {
    console.log('未知命令: ' + cmd);
    process.exit(1);
  }
}

main().catch(err => { console.error('❌', err.message); process.exit(1); });
