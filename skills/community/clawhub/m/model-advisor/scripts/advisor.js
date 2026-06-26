#!/usr/bin/env node
/**
 * model-advisor: 模型推荐 + 安全系数分析
 * 用法:
 *   node advisor.js security          -- 输出安全系数报告
 *   node advisor.js recommend <task>  -- 根据任务描述推荐最优模型
 *   node advisor.js auto              -- 根据历史任务自动分析并推荐
 *   node advisor.js full <task>       -- 安全系数 + 任务描述推荐
 */

import { readFileSync, existsSync, readdirSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const HOME = homedir();
const CONFIG_PATH = join(HOME, '.openclaw', 'openclaw.json');
const MODELS_PATH = join(HOME, '.openclaw', 'agents', 'main', 'agent', 'models.json');
const SESSIONS_DIR = join(HOME, '.openclaw', 'agents', 'main', 'sessions');
const SESSIONS_META = join(SESSIONS_DIR, 'sessions.json');

// ──────────────────────────────────────────
// 1. 读取配置
// ──────────────────────────────────────────
function loadConfig() {
  if (!existsSync(CONFIG_PATH)) {
    console.error(`配置文件不存在: ${CONFIG_PATH}`);
    process.exit(1);
  }
  return JSON.parse(readFileSync(CONFIG_PATH, 'utf8'));
}

function loadModels() {
  if (!existsSync(MODELS_PATH)) return null;
  return JSON.parse(readFileSync(MODELS_PATH, 'utf8'));
}

// ──────────────────────────────────────────
// 2. 安全系数计算
// ──────────────────────────────────────────
function calcSecurity(cfg) {
  const result = { score: 0, maxScore: 100, items: [] };

  function add(pts, label, detail) {
    result.score += pts;
    result.items.push({ pts, label, detail });
  }

  const gw = cfg.gateway ?? {};

  // 认证模式（30分）
  const authMode = gw.auth?.mode ?? 'none';
  if (authMode === 'token') {
    add(30, '✅ 认证方式', 'Token 认证（最高级）');
  } else if (authMode === 'password') {
    add(18, '⚠️  认证方式', 'Password 认证（中等）');
  } else {
    add(0, '❌ 认证方式', '无认证（高风险）');
  }

  // 绑定地址（25分）
  const bind = gw.bind ?? 'local';
  if (bind === 'loopback') {
    add(25, '✅ 网络绑定', 'loopback（仅本机访问，最安全）');
  } else if (bind === 'local') {
    add(15, '⚠️  网络绑定', 'local（局域网可访问）');
  } else if (bind === 'tailscale') {
    add(10, '⚠️  网络绑定', 'tailscale（受控外网）');
  } else {
    add(0, '❌ 网络绑定', `公网暴露（bind=${bind}，极高风险）`);
  }

  // Tailscale 状态（15分）
  const tsMode = gw.tailscale?.mode ?? 'off';
  if (tsMode === 'off') {
    add(15, '✅ Tailscale', '已关闭（无外部隧道）');
  } else {
    add(8, '⚠️  Tailscale', `已开启（mode=${tsMode}）`);
  }

  // 命令黑名单（20分）
  const denyList = gw.nodes?.denyCommands ?? [];
  const dangerCmds = ['camera.snap', 'camera.clip', 'screen.record', 'contacts.add', 'calendar.add', 'reminders.add', 'sms.send', 'shell'];
  const coveredDanger = dangerCmds.filter(c => denyList.includes(c));
  const denyScore = Math.min(20, Math.round((coveredDanger.length / dangerCmds.length) * 20));
  add(denyScore, denyScore >= 15 ? '✅ 命令黑名单' : '⚠️  命令黑名单',
    `已屏蔽 ${denyList.length} 条命令（高危命令覆盖 ${coveredDanger.length}/${dangerCmds.length}）`);

  // Gateway 模式（10分）
  const gwMode = gw.mode ?? 'local';
  if (gwMode === 'local') {
    add(10, '✅ Gateway 模式', 'local（本地运行）');
  } else {
    add(5, '⚠️  Gateway 模式', `${gwMode}（非本地模式）`);
  }

  // 安全等级
  const pct = Math.round((result.score / result.maxScore) * 100);
  result.level = pct >= 85 ? '🔒 高安全' : pct >= 60 ? '🔐 中等安全' : '🔓 低安全';
  result.pct = pct;

  return result;
}

// ──────────────────────────────────────────
// 3. 模型推荐逻辑
// ──────────────────────────────────────────
const MODEL_PROFILES = [
  {
    id: 'claude-opus-4-6',
    tier: 'opus',
    name: 'Claude Opus 4.6',
    strengths: ['复杂推理', '代码架构', '多步骤分析', '研究写作', '长文本理解', '技术文档'],
    speed: '较慢',
    cost: '高',
    keywords: ['架构', '分析', '设计', '优化', '重构', '文档', '调试', 'debug', '方案', '复杂', '系统', 'bug',
      '代码审查', '安全', '数据库', 'sql', 'java', '并发', '算法', '性能', '接口', 'api',
      '部署', '微服务', '中间件', 'redis', 'kafka', '分布式', '高并发', '死锁', '事务',
      'spring', 'docker', 'kubernetes', 'ci', 'cd', '测试', '单元测试', '集成测试',
      '需求', '评审', '技术方案', '报告', '漏洞', '攻击', '防御', '加密', '鉴权'],
  },
  {
    id: 'claude-sonnet-4-6',
    tier: 'sonnet',
    name: 'Claude Sonnet 4.6',
    strengths: ['日常编码', '问答', '摘要', '翻译', '简单分析', '内容生成'],
    speed: '中等',
    cost: '中',
    keywords: ['写', '翻译', '总结', '解释', '生成', '问答', '简单', '快速', '日常',
      '帮我', '怎么', '如何', '是什么', '什么是', '功能', '实现', '写一个', '修改',
      'git', '命令', '配置', '脚本', '工具', '自动化'],
  },
  {
    id: 'claude-haiku-4-5',
    tier: 'haiku',
    name: 'Claude Haiku 4.5',
    strengths: ['简单问答', '格式化', '分类', '快速响应', '轻量任务'],
    speed: '极快',
    cost: '低',
    keywords: ['格式', '分类', '标签', '快', '简短', '列表', '转换', '提取', '查找'],
  },
];

function recommendModel(task, availableModels) {
  const taskLower = task.toLowerCase();

  const scores = MODEL_PROFILES.map(m => {
    const hits = m.keywords.filter(kw => taskLower.includes(kw));
    return { model: m, hits, score: hits.length };
  });

  scores.sort((a, b) => b.score - a.score);
  const top = scores[0];

  const configuredIds = availableModels
    ? Object.values(availableModels.providers ?? {}).flatMap(p => (p.models ?? []).map(m => m.id))
    : [];

  const isAvailable = configuredIds.includes(top.model.id);

  return {
    recommended: top.model,
    hits: top.hits,
    score: top.score,
    isAvailable,
    configuredIds,
    allScores: scores,
  };
}

// ──────────────────────────────────────────
// 4. 历史任务分析
// ──────────────────────────────────────────

/**
 * 读取最近 N 个 session 的用户消息文本
 */
function loadHistoryMessages(maxSessions = 5, maxMsgsPerSession = 50) {
  if (!existsSync(SESSIONS_DIR)) return [];

  // 获取活跃 session ID
  let activeIds = [];
  if (existsSync(SESSIONS_META)) {
    try {
      const meta = JSON.parse(readFileSync(SESSIONS_META, 'utf8'));
      activeIds = Object.values(meta)
        .filter(s => s.sessionId)
        .sort((a, b) => (b.updatedAt ?? 0) - (a.updatedAt ?? 0))
        .slice(0, maxSessions)
        .map(s => s.sessionId);
    } catch { /* ignore */ }
  }

  // 若 sessions.json 没读到，扫描 .jsonl 文件
  if (activeIds.length === 0) {
    try {
      const files = readdirSync(SESSIONS_DIR)
        .filter(f => f.endsWith('.jsonl') && !f.includes('.deleted'))
        .slice(0, maxSessions);
      activeIds = files.map(f => f.replace('.jsonl', ''));
    } catch { /* ignore */ }
  }

  const messages = [];
  for (const id of activeIds) {
    const filePath = join(SESSIONS_DIR, `${id}.jsonl`);
    if (!existsSync(filePath)) continue;
    try {
      const lines = readFileSync(filePath, 'utf8').split('\n');
      let count = 0;
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const event = JSON.parse(line);
          if (
            event.type === 'message' &&
            event.message?.role === 'user' &&
            Array.isArray(event.message.content)
          ) {
            const text = event.message.content
              .filter(c => c.type === 'text')
              .map(c => c.text ?? '')
              .join(' ');
            if (text.trim()) {
              messages.push({ text, timestamp: event.timestamp, sessionId: id });
              count++;
              if (count >= maxMsgsPerSession) break;
            }
          }
        } catch { /* skip malformed line */ }
      }
    } catch { /* skip unreadable file */ }
  }

  return messages;
}

/**
 * 根据历史消息分析任务类型分布，返回模型推荐
 */
function analyzeHistory(availableModels) {
  const messages = loadHistoryMessages();
  if (messages.length === 0) {
    return { error: '未找到历史会话数据', messages: 0 };
  }

  // 统计各模型档位的命中分
  const totalScores = MODEL_PROFILES.map(m => ({ model: m, totalHits: 0, hitKeywords: {} }));

  for (const { text } of messages) {
    const lower = text.toLowerCase();
    MODEL_PROFILES.forEach((m, idx) => {
      for (const kw of m.keywords) {
        if (lower.includes(kw)) {
          totalScores[idx].totalHits++;
          totalScores[idx].hitKeywords[kw] = (totalScores[idx].hitKeywords[kw] ?? 0) + 1;
        }
      }
    });
  }

  totalScores.sort((a, b) => b.totalHits - a.totalHits);
  const top = totalScores[0];
  const noSignal = top.totalHits === 0;

  // 取各档位 top-5 高频关键词
  const topKeywords = Object.entries(top.hitKeywords)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([kw, cnt]) => `${kw}(×${cnt})`);

  const configuredIds = availableModels
    ? Object.values(availableModels.providers ?? {}).flatMap(p => (p.models ?? []).map(m => m.id))
    : [];

  // 若无法从历史匹配，默认推荐 Opus（能力最强，适合未知场景）
  const recommended = noSignal ? MODEL_PROFILES[0] : top.model;
  const isAvailable = configuredIds.includes(recommended.id);

  return {
    recommended,
    totalHits: top.totalHits,
    topKeywords,
    isAvailable,
    configuredIds,
    allScores: totalScores,
    totalMessages: messages.length,
    noSignal,
  };
}

// ──────────────────────────────────────────
// 5. 输出
// ──────────────────────────────────────────
function printSecurity(sec, cfg) {
  const gw = cfg.gateway ?? {};
  console.log('');
  console.log('═══════════════════════════════════════════');
  console.log('         OpenClaw 安全系数报告');
  console.log('═══════════════════════════════════════════');
  console.log('');
  console.log(`  综合安全系数：${sec.pct}% / 100%   ${sec.level}`);
  console.log(`  得分：${sec.score} / ${sec.maxScore} 分`);
  console.log('');
  console.log('  ─── 评分明细 ───────────────────────────');
  for (const item of sec.items) {
    console.log(`  ${item.label.padEnd(14)} +${String(item.pts).padStart(2)}分  ${item.detail}`);
  }
  console.log('');
  console.log('  ─── 当前配置摘要 ───────────────────────');
  console.log(`  端口          ${gw.port ?? 'N/A'}`);
  console.log(`  绑定地址      ${gw.bind ?? 'N/A'}`);
  console.log(`  认证模式      ${gw.auth?.mode ?? 'N/A'}`);
  console.log(`  Gateway 模式  ${gw.mode ?? 'N/A'}`);
  console.log(`  Tailscale     ${gw.tailscale?.mode ?? 'N/A'}`);
  console.log(`  黑名单命令数  ${(gw.nodes?.denyCommands ?? []).length}`);
  console.log('═══════════════════════════════════════════');
  console.log('');
}

function printRecommendation(rec, task) {
  console.log('');
  console.log('═══════════════════════════════════════════');
  console.log('         最优模型推荐');
  console.log('═══════════════════════════════════════════');
  console.log('');
  console.log(`  任务描述：${task}`);
  console.log('');
  console.log(`  推荐模型：${rec.recommended.name}  (${rec.recommended.id})`);
  console.log(`  响应速度：${rec.recommended.speed}`);
  console.log(`  成本参考：${rec.recommended.cost}`);
  console.log(`  擅长领域：${rec.recommended.strengths.join('、')}`);
  if (rec.hits.length > 0) {
    console.log(`  命中关键词：${rec.hits.join(', ')}`);
  }
  console.log('');
  if (!rec.isAvailable) {
    console.log(`  ⚠️  注意：推荐模型 ${rec.recommended.id} 未在当前 provider 中配置`);
    if (rec.configuredIds.length > 0) {
      console.log(`     当前已配置：${rec.configuredIds.join(', ')}`);
      console.log(`     建议使用：${rec.configuredIds[0]}`);
    }
  } else {
    console.log(`  ✅ 该模型已在当前配置中可用`);
  }
  console.log('');
  console.log('  ─── 其他模型参考 ───────────────────────');
  for (const s of rec.allScores.slice(1)) {
    console.log(`  ${s.model.name.padEnd(22)} 匹配度 ${s.score} 分  ${s.model.strengths.slice(0, 3).join('、')}`);
  }
  console.log('═══════════════════════════════════════════');
  console.log('');
}

function printAutoRecommendation(ana) {
  console.log('');
  console.log('═══════════════════════════════════════════');
  console.log('     历史任务分析 · 自动模型推荐');
  console.log('═══════════════════════════════════════════');
  console.log('');

  if (ana.error) {
    console.log(`  ⚠️  ${ana.error}`);
    console.log('     请使用 recommend <任务描述> 手动指定任务。');
    console.log('');
    return;
  }

  console.log(`  分析会话数：最近 ${ana.totalMessages} 条历史消息`);
  console.log('');
  if (ana.noSignal) {
    console.log(`  ℹ️  历史消息中未匹配到明显的任务特征，默认推荐能力最强的模型。`);
    console.log('');
  }
  console.log(`  推荐模型：${ana.recommended.name}  (${ana.recommended.id})`);
  console.log(`  响应速度：${ana.recommended.speed}`);
  console.log(`  成本参考：${ana.recommended.cost}`);
  console.log(`  擅长领域：${ana.recommended.strengths.join('、')}`);
  if (ana.topKeywords.length > 0) {
    console.log(`  高频关键词：${ana.topKeywords.join('  ')}`);
  }
  console.log('');

  if (!ana.isAvailable) {
    console.log(`  ⚠️  注意：推荐模型 ${ana.recommended.id} 未在当前 provider 中配置`);
    if (ana.configuredIds.length > 0) {
      console.log(`     当前已配置：${ana.configuredIds.join(', ')}`);
      console.log(`     建议使用：${ana.configuredIds[0]}`);
    }
  } else {
    console.log(`  ✅ 该模型已在当前配置中可用`);
  }

  console.log('');
  console.log('  ─── 各模型历史命中率 ──────────────────');
  const maxHits = Math.max(...ana.allScores.map(s => s.totalHits), 1);
  for (const s of ana.allScores) {
    const bar = '█'.repeat(Math.round((s.totalHits / maxHits) * 15)).padEnd(15);
    console.log(`  ${s.model.name.padEnd(22)} ${bar} ${s.totalHits} 次`);
  }
  console.log('═══════════════════════════════════════════');
  console.log('');
}

// ──────────────────────────────────────────
// 6. 入口
// ──────────────────────────────────────────
const [,, cmd, ...rest] = process.argv;
const task = rest.join(' ');

const cfg = loadConfig();
const models = loadModels();

if (cmd === 'security') {
  printSecurity(calcSecurity(cfg), cfg);
} else if (cmd === 'recommend' && task) {
  const rec = recommendModel(task, models);
  printRecommendation(rec, task);
} else if (cmd === 'auto') {
  const ana = analyzeHistory(models);
  printAutoRecommendation(ana);
} else if (cmd === 'full' && task) {
  printSecurity(calcSecurity(cfg), cfg);
  const rec = recommendModel(task, models);
  printRecommendation(rec, task);
} else if (cmd === 'full') {
  // full without task → security + auto history
  printSecurity(calcSecurity(cfg), cfg);
  const ana = analyzeHistory(models);
  printAutoRecommendation(ana);
} else {
  console.log('用法:');
  console.log('  node advisor.js security              -- 安全系数报告');
  console.log('  node advisor.js auto                  -- 根据历史任务自动推荐模型');
  console.log('  node advisor.js recommend <任务描述>  -- 根据任务描述推荐模型');
  console.log('  node advisor.js full [任务描述]        -- 完整报告（安全系数 + 模型推荐）');
  process.exit(1);
}
