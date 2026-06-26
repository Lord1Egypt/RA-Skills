#!/usr/bin/env node
/**
 * send-card.mjs — 将新闻 JSON 构建成飞书卡片并发送
 *
 * 接受一个或多个新闻主题的 JSON（通过 --sections 或 stdin），
 * 合并成一张卡片发送给目标用户。
 *
 * Usage:
 *   echo '[{"topic":"AI","items":[...]},{"topic":"时政","items":[...]}]' | \
 *     node send-card.mjs --title "每日日报" --target-user ou_xxx
 *
 *   node send-card.mjs \
 *     --json '[{"topic":"...","items":[...]}]' \
 *     --title "每日日报" \
 *     --target-user ou_xxx
 */

import { readFileSync } from 'fs';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) { args[key] = next; i++; }
      else args[key] = true;
    }
  }
  return args;
}

async function fetchFeishuToken(appId, appSecret) {
  const res = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`飞书 auth 失败: ${data.msg}`);
  return `Bearer ${data.tenant_access_token}`;
}

function categoryEmoji(title, category) {
  if (category === 'GEO') {
    if (/中美|贸易|制裁|外交/.test(title)) return '🌐';
    if (/两会|政策|监管/.test(title)) return '🏛️';
    if (/经济|股市|金融/.test(title)) return '📊';
    return '🌍';
  }
  if (category === 'SPORT') {
    if (/MLB|道奇|大谷/.test(title)) return '⚾';
    if (/NFL|NBA/.test(title)) return '🏀';
    if (/F1|赛车/.test(title)) return '🏎️';
    return '🏆';
  }
  if (/大模型|LLM|GPT|Claude|Gemini|DeepSeek/.test(title)) return '🧠';
  if (/芯片|GPU|算力|硬件/.test(title)) return '💻';
  if (/融资|投资|估值/.test(title)) return '💰';
  if (/Agent|自动化/.test(title)) return '🤖';
  return '🚀';
}

function buildCard(sections, title, subtitle) {
  const elements = [];

  if (subtitle) {
    elements.push({
      tag: 'markdown',
      content: subtitle,
    });
    elements.push({ tag: 'hr' });
  }

  for (const section of sections) {
    const { topic, items } = section;
    if (!items || items.length === 0) continue;

    elements.push({ tag: 'markdown', content: `**${topic}**` });

    for (const item of items) {
      const emoji = categoryEmoji(item.title, item.category || 'AI');
      const fallbackUrl = `https://www.google.com/search?q=${encodeURIComponent(item.title)}`;

      // 标题 + 摘要
      elements.push({
        tag: 'markdown',
        content: `${emoji} **${item.title}**\n${item.summary}`,
      });

      // 查看原文按钮
      elements.push({
        tag: 'column_set',
        flex_mode: 'none',
        columns: [{
          tag: 'column', width: 'weighted', weight: 1,
          elements: [{
            tag: 'button',
            text: { tag: 'plain_text', content: '📄 查看原文' },
            url: item.url || fallbackUrl,
            type: 'url', width: 'fill', size: 'small',
          }],
        }],
      });

      // AI洞察折叠块（有洞察才显示）
      if (item.insight) {
        elements.push({
          tag: 'collapsible_panel',
          expanded: false,
          header: {
            title: { tag: 'plain_text', content: '💡 查看AI洞察' },
            icon: { tag: 'standard_icon', token: 'down-small_outlined' },
            icon_position: 'follow_text',
            icon_expanded_angle: -180,
          },
          elements: [{ tag: 'markdown', content: item.insight }],
        });
      }

      elements.push({ tag: 'hr' });
    }
  }

  // 去掉最后一个 hr
  if (elements[elements.length - 1]?.tag === 'hr') elements.pop();

  return {
    schema: '2.0',
    header: {
      title: { tag: 'plain_text', content: title },
      template: 'blue',
    },
    body: { elements },
  };
}

async function sendCard(token, userId, card) {
  const res = await fetch('https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id', {
    method: 'POST',
    headers: { 'Authorization': token, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      receive_id: userId,
      msg_type: 'interactive',
      content: JSON.stringify(card),
    }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`飞书发送失败: ${JSON.stringify(data)}`);
  return data;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const {
    title = '📰 新闻日报',
    subtitle = '',
    json: jsonStr,
    'json-file': jsonFile,
    'target-user': userId,
    'dry-run': dryRun,
  } = args;

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  const targetUser = userId || process.env.TARGET_USER_ID;

  if (!targetUser && !dryRun) { console.error('❌ 缺少 --target-user 或 TARGET_USER_ID'); process.exit(1); }
  if (!appId || !appSecret) { console.error('❌ 缺少 FEISHU_APP_ID / FEISHU_APP_SECRET'); process.exit(1); }

  // 读取新闻数据
  let sections;
  if (jsonStr) {
    sections = JSON.parse(jsonStr);
  } else if (jsonFile) {
    sections = JSON.parse(readFileSync(jsonFile, 'utf-8'));
  } else {
    // 从 stdin 读
    const stdin = readFileSync('/dev/stdin', 'utf-8');
    sections = JSON.parse(stdin);
  }

  // 兼容单个 section 对象
  if (!Array.isArray(sections)) sections = [sections];

  const totalItems = sections.reduce((s, sec) => s + (sec.items?.length || 0), 0);
  console.log(`📦 共 ${sections.length} 个主题，${totalItems} 条新闻`);

  const card = buildCard(sections, title, subtitle);

  if (dryRun) {
    console.log('🧪 Dry-run:');
    console.log(JSON.stringify(card, null, 2));
    return;
  }

  const token = await fetchFeishuToken(appId, appSecret);
  const result = await sendCard(token, targetUser, card);
  console.log(`✅ 发送成功！message_id: ${result.data?.message_id}`);
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });
