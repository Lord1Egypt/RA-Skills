#!/usr/bin/env node
/**
 * Polymarket 套利晨报发送脚本
 * 运行扫描器 → 读取结果 → 直接发 Telegram
 * 用于 cron 定时任务，无需 AI 中转
 */

import { execSync } from 'child_process';
import { readFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// .env loader
try {
  const envPath = join(__dirname, '.env');
  if (existsSync(envPath)) {
    for (const line of readFileSync(envPath, 'utf8').split(/\r?\n/)) {
      const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/i);
      if (m && !(m[1] in process.env)) process.env[m[1]] = m[2];
    }
  }
} catch {}

// ── 邮件发送（通过 Apple Mail + osascript）───────────────────────────────────
async function sendEmail(subject, body) {
  const to = process.env.SMTP_TO || process.env.SMTP_USER || 'you@example.com';
  // 转义 AppleScript 字符串
  const esc = s => s.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
  const script = `
tell application "Mail"
  set newMessage to make new outgoing message with properties {subject:"${esc(subject)}", content:"${esc(body)}", visible:false}
  tell newMessage
    make new to recipient at end of to recipients with properties {address:"${esc(to)}"}
  end tell
  send newMessage
end tell
`;
  const escaped = script.replace(/'/g, `'"'"'`);
  execSync(`osascript -e '${escaped}'`, { timeout: 30000 });
}


function formatOpportunities(opportunities, scanTime) {
  if (opportunities.length === 0) {
    return `📊 <b>Polymarket 套利晨报</b> [${scanTime}]\n\n暂无机会（阈值 3%-50%）`;
  }

  const negRisk = opportunities.filter(o => o.isNegRisk);
  const regular = opportunities.filter(o => !o.isNegRisk);

  let msg = `🎯 <b>Polymarket 套利晨报</b> [${scanTime}]\n`;
  msg += `发现 <b>${opportunities.length}</b> 个机会`;
  if (negRisk.length > 0) msg += `（${negRisk.length} 个 ⭐NegRisk）`;
  msg += '\n\n';

  const printOpps = (opps, label) => {
    if (opps.length === 0) return '';
    let out = `<b>${label}</b>\n`;
    for (const opp of opps.slice(0, 8)) { // 最多展示8个
      out += `\n<b>[${opp.type}]</b> ${opp.title}\n`;
      out += `💰 利润: <b>${opp.expectedProfit}</b>  |  总量: $${(opp.volume / 1000).toFixed(0)}k`;
      if (opp.volume24hr > 0) out += `  | 24h: $${(opp.volume24hr / 1000).toFixed(0)}k`;
      out += '\n';
      out += `📐 概率和: ${(opp.sum * 100).toFixed(2)}% (偏离 ${opp.deviation > 0 ? '+' : ''}${(opp.deviation * 100).toFixed(2)}%)\n`;
      out += `🎯 ${opp.strategy}\n`;
      out += `🔗 <a href="${opp.url}">${opp.url}</a>\n`;
      // 展示前5个选项
      for (const m of opp.markets.slice(0, 5)) {
        out += `  ${(m.yesPrice * 100).toFixed(1)}%  ${m.question.slice(0, 50)}\n`;
      }
      if (opp.markets.length > 5) out += `  ...共 ${opp.markets.length} 个选项\n`;
      out += '─────────\n';
    }
    if (opps.length > 8) out += `\n（还有 ${opps.length - 8} 个机会未显示）\n`;
    return out;
  };

  if (negRisk.length > 0) {
    msg += printOpps(negRisk, '⭐ NegRisk 高质量市场');
  }
  if (regular.length > 0) {
    msg += printOpps(regular, '📋 普通多选市场');
  }

  return msg;
}

async function main() {
  const scanTime = new Date().toLocaleString('zh-CN', { timeZone: 'Europe/Stockholm' });
  console.log(`[${scanTime}] 运行扫描器...`);

  try {
    // 运行扫描器
    execSync(`node ${join(__dirname, 'scanner.js')}`, {
      stdio: 'inherit',
      cwd: __dirname,
      timeout: 120000, // 2分钟超时
    });

    // 读取结果
    const outputPath = join(__dirname, 'opportunities.json');
    if (!existsSync(outputPath)) {
      throw new Error('opportunities.json 不存在，扫描器可能失败了');
    }

    const data = JSON.parse(readFileSync(outputPath, 'utf8'));
    const { opportunities = [] } = data;

    console.log(`扫描完成，找到 ${opportunities.length} 个机会`);

    // 格式化并发邮件
    const msg = formatOpportunities(opportunities, scanTime);
    const subject = `📊 Polymarket 套利晨报 [${scanTime}] — ${opportunities.length} 个机会`;
    const plainText = msg.replace(/<[^>]+>/g, ''); // 去掉 HTML 标签
    try {
      await sendEmail(subject, plainText);
      console.log('✅ 晨报已发送到邮箱');
    } catch (mailErr) {
      console.error('❌ 邮件发送失败:', mailErr.message);
    }
  } catch (err) {
    const errMsg = `❌ Polymarket 套利扫描失败 [${scanTime}]\n${err.message}`;
    console.error(errMsg);
    try {
      await sendEmail(`❌ Polymarket 扫描失败 [${scanTime}]`, errMsg);
    } catch (e2) {
      console.error('发送错误通知也失败了:', e2.message);
    }
    process.exit(1);
  }
}

main();
