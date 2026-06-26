/**
 * LoveClaw - 定时任务脚本
 * 每日匹配 & 晚8点报告
 */

const path = require('path');
const os = require('os');
const fs = require('fs');
const { execFileSync } = require('child_process');

// 设置工作目录
const SKILL_DIR = path.join(os.homedir(), '.openclaw', 'workspace', 'skills', 'loveclaw');
process.chdir(SKILL_DIR);

// 加载模块
const data = require('./data');
const match = require('./match');
const bazi = require('./bazi');

/**
 * 执行每日匹配
 */
function runDailyMatching() {
  console.log('[定时任务] 开始执行每日匹配...');
  
  // 重置所有用户的每日匹配状态
  match.resetDailyStatus();
  
  // 执行匹配
  const results = match.runAllDailyMatches();
  
  console.log(`[定时任务] 匹配完成，${results.matched.length} 对 mutual match 成功`);
  console.log(`[定时任务] ${results.noMatch.length} 位用户今日无匹配`);
  
  return results;
}

/**
 * 生成晚8点报告
 */
async function runEveningReports() {
  console.log('[定时任务] 开始生成晚间报告...');
  
  const reports = [];
  
  // 1. 处理有匹配的用户
  const unreportedMatches = data.getUnreportedMatches();
  
  for (const matchRecord of unreportedMatches) {
    const partnerId = matchRecord.userId2;
    const partner = data.getProfile(partnerId);
    
    if (!partner) continue;
    
    const profile = data.getProfile(matchRecord.userId1);
    if (!profile) continue;
    
    let score = matchRecord.compatibility;
    let repDetail = { interpretation: '你们的八字比较匹配，缘分不错！' };
    if (profile.bazi && partner.bazi && profile.bazi.yearGan && partner.bazi.yearGan) {
      const s1 = bazi.calculateMatchScore(profile.bazi, partner.bazi);
      const s2 = bazi.calculateMatchScore(partner.bazi, profile.bazi);
      score = Math.min(s1, s2);
      repDetail = bazi.generateMatchReport(profile.bazi, partner.bazi, score);
    }
    const message = match.formatMatchReport(profile, partner, score, repDetail);
    
    // 标记已报告
    data.markMatchReported(matchRecord.id);
    
    reports.push({
      userId: matchRecord.userId1,
      channel: profile.channel || 'webchat',
      target: profile.notificationTarget || profile.userId,
      hasMatch: true,
      message
    });
  }
  
  // 2. 处理无匹配的用户 - 发送命运消息
  const noMatchUserIds = match.getTodayNoMatchUserIds();
  
  for (const userId of noMatchUserIds) {
    const profile = data.getProfile(userId);
    if (!profile) continue;
    
    // 检查用户今日是否已有报告
    const todayMatch = data.getUserTodayMatch(userId);
    if (todayMatch && todayMatch.reported) continue;
    
    reports.push({
      userId,
      channel: profile.channel || 'webchat',
      target: profile.notificationTarget || profile.userId,
      hasMatch: false,
      message: match.formatNoMatchMessage(profile),
    });
  }
  
  console.log(`[定时任务] 生成 ${reports.filter(r => r.hasMatch).length} 份匹配报告`);
  console.log(`[定时任务] 发送 ${reports.filter(r => !r.hasMatch).length} 份无匹配通知`);
  
  // 输出 JSON 格式的报告供 agent 发送
  console.log('【REPORTS_JSON】' + JSON.stringify(reports) + '【REPORTS_JSON_END】');
  
  return reports;
}

/**
 * 发送无匹配通知（单独调用）
 */
function sendNoMatchNotifications() {
  console.log('[定时任务] 发送无匹配通知...');
  
  const noMatchUserIds = match.getTodayNoMatchUserIds();
  
  for (const userId of noMatchUserIds) {
    const profile = data.getProfile(userId);
    if (!profile) continue;
    
    const message = `🌙 今日缘分未到...\n\n`;
    
    console.log(`[通知] 发送给 ${profile.name}: 爱情龙虾今日匹配失败`);
  }
  
  return noMatchUserIds;
}

/**
 * 检查并注册 cron 任务
 * 使用 openclaw cron add 命令行接口（与 cron tool 相同的后端）
 */
function ensureCronJobs() {
  console.log('[定时任务] 检查 cron 任务注册状态...');
  
  const CRON_FILE = path.join(os.homedir(), '.openclaw', 'cron', 'jobs.json');
  const openclawBin = process.env.OPENCLAW_BIN || 'openclaw';
  
  try {
    // 用 openclaw cron list 检查现有任务
    let existingJobs = [];
    try {
      const out = execFileSync(openclawBin, ['cron', 'list', '--json'], {
        encoding: 'utf-8',
        timeout: 10000,
        stdio: ['pipe', 'pipe', 'ignore'],
      });
      const parsed = JSON.parse(out);
      existingJobs = parsed.jobs || [];
    } catch (e) {
      // 没有现有任务或解析失败
      existingJobs = [];
    }
    
    const jobNames = existingJobs.map(j => j.name || '');
    const hasDailyMatch = jobNames.some(n => n.includes('LoveClaw') && n.includes('每日匹配'));
    const hasEveningReport = jobNames.some(n => n.includes('晚间匹配报告'));
    
    if (hasDailyMatch && hasEveningReport) {
      console.log('[定时任务] cron 任务已完整注册，无需更新');
      return true;
    }
    
    // 注册每日匹配任务 (19:50)
    if (!hasDailyMatch) {
      try {
        execFileSync(
          openclawBin,
          [
            'cron',
            'add',
            '--name',
            'LoveClaw-每日匹配',
            '--cron',
            '50 19 * * *',
            '--tz',
            'Asia/Shanghai',
            '--session',
            'isolated',
            '--message',
            '执行每日八字匹配任务。请运行: cd ~/.openclaw/workspace/skills/loveclaw/scripts && node cron.js match。匹配结果已存入云端。',
            '--delivery',
            'none',
          ],
          { timeout: 15000, stdio: 'pipe' }
        );
        console.log('[定时任务] 已注册 LoveClaw-每日匹配');
      } catch (e) {
        console.error('[定时任务] 注册每日匹配失败:', e.message);
      }
    }
    
    // 注册晚间报告任务 (20:00)
    // 使用 isolated + --no-deliver：任务在独立会话运行，由 agent 内部使用 message 工具发送报告
    if (!hasEveningReport) {
      try {
        execFileSync(
          openclawBin,
          [
            'cron',
            'add',
            '--name',
            '晚间匹配报告',
            '--cron',
            '0 20 * * *',
            '--tz',
            'Asia/Shanghai',
            '--session',
            'isolated',
            '--message',
            '请执行 node ~/.openclaw/workspace/skills/loveclaw/scripts/cron.js report，生成晚间匹配报告。\n\n报告生成后，以希希的口吻（活泼、专业、像朋友聊天）处理：\n- 读取报告中的 channel 和 target 字段，确定发送目标\n- 如果有匹配用户：使用 message 工具发送到对应 channel（webchat 或 feishu），target 使用报告中的值，发送配对成功信息\n- 如果无匹配用户：使用 message 工具发送：🦞 爱情龙虾今日匹配失败，但是命运的齿轮依然转动，期待明日月老的大驾光临！（用户无需重复报名，明日继续自动匹配）\n- 如果无任何数据：不发送任何消息',
            '--no-deliver',
          ],
          { timeout: 15000, stdio: 'pipe' }
        );
        console.log('[定时任务] 已注册晚间匹配报告');
      } catch (e) {
        console.error('[定时任务] 注册晚间报告失败:', e.message);
      }
    }
    
    console.log('[定时任务] cron 任务注册完成');
    return true;
  } catch (e) {
    console.error('[定时任务] 检查注册状态失败:', e.message);
    return false;
  }
}

// 命令行接口（仅在直接 node cron.js 时执行，require() 时跳过）
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'match') {
    runDailyMatching();
  } else if (command === 'report') {
    runEveningReports().then(reports => {
      console.log('报告生成完成');
      process.exit(0);
    });
  } else if (command === 'nomatch') {
    sendNoMatchNotifications();
  } else if (command === 'ensure') {
    ensureCronJobs();
  } else {
    console.log('用法: node cron.js [match|report|nomatch|ensure]');
    process.exit(1);
  }
}

module.exports = { runDailyMatching, runEveningReports, sendNoMatchNotifications, ensureCronJobs };
