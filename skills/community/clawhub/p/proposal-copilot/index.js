const BILLING_API_URL = 'https://skillpay.me';
const BILLING_API_KEY = 'sk_2842f59e03e64e418c15771b0928c3f94a1f1da73ae7e72adc8f483e9f6fe6b1';
const SKILL_ID = '585cbb06-8eea-4eb2-b059-9b4a5010bb57';  // 你的新技能ID
const PRICE_PER_CALL = 0.001;

async function callBilling(endpoint, method = 'POST', payload = {}) {
  const headers = {
    'X-API-Key': BILLING_API_KEY,
    'Content-Type': 'application/json',
  };
  const url = new URL(`${BILLING_API_URL}${endpoint}`);
  const opts = { method, headers };
  if (method === 'GET') {
    Object.entries(payload).forEach(([k, v]) => url.searchParams.set(k, String(v)));
  } else {
    opts.body = JSON.stringify(payload);
  }
  const res = await fetch(url.toString(), opts);
  return res.json();
}

async function charge(userId) {
  const data = await callBilling('/api/v1/billing/charge', 'POST', {
    user_id: userId,
    skill_id: SKILL_ID,
    amount: PRICE_PER_CALL,
  });
  if (data.success) return { ok: true, balance: data.balance };
  return {
    ok: false,
    error: data.error || 'charge_failed',
    balance: data.balance,
    payment_url: data.payment_url,
  };
}

function scoreJD(jd) {
  const text = (jd || '').toLowerCase();
  let budget = 12;      // 0-30
  let clarity = 8;      // 0-20
  let fit = 10;         // 0-25
  let client = 6;       // 0-15
  let feasibility = 7;  // 0-10

  // budget signals
  if (/\$|usd|hour|budget|fixed price|hourly/.test(text)) budget += 10;
  if (/expert|senior|complex|enterprise/.test(text)) budget += 4;

  // clarity signals
  if (/requirements|deliverables|timeline|scope|must have/.test(text)) clarity += 8;
  if (/example|sample|reference|figma|spec/.test(text)) clarity += 3;

  // skill-fit signals
  if (/python|javascript|node|automation|api|scraping|ai|llm/.test(text)) fit += 10;
  if (/excel|xml|data|parser|integration/.test(text)) fit += 4;

  // client quality signals
  if (/payment verified|5\.?0|hires|spent/.test(text)) client += 6;

  // feasibility signals
  if (/urgent|asap|today/.test(text)) feasibility -= 3;
  if (/1 week|7 days|two weeks|14 days|milestone/.test(text)) feasibility += 2;

  budget = Math.max(0, Math.min(30, budget));
  clarity = Math.max(0, Math.min(20, clarity));
  fit = Math.max(0, Math.min(25, fit));
  client = Math.max(0, Math.min(15, client));
  feasibility = Math.max(0, Math.min(10, feasibility));

  const score = budget + clarity + fit + client + feasibility;
  const decision = score >= 70 ? 'BID' : score >= 50 ? 'MAYBE' : 'SKIP';
  const summary = decision === 'BID'
    ? '建议投：性价比和中标概率都不错。'
    : decision === 'MAYBE'
      ? '可投可不投：建议先优化报价和切入点再投。'
      : '不建议投：投入产出比偏低。';

  const reasons = [
    `Budget match: ${budget}/30`,
    `Requirement clarity: ${clarity}/20`,
    `Skill fit: ${fit}/25`,
    `Client quality: ${client}/15`,
    `Delivery feasibility: ${feasibility}/10`,
  ];
  return { score, decision, reasons, summary };
}

function buildProposal(jd, style = 'professional') {
  const base = (jd || '').slice(0, 300);
  if (style === 'concise') {
    return `Hi,\n\nI can complete this project with clear scope, fast turnaround, and reliable delivery. I have hands-on experience in similar jobs and can start right away.\n\nPlan:\n- Confirm scope and milestones\n- Deliver first version quickly\n- Iterate based on feedback\n\nI'm ready to begin today.\n\nBest regards`;
  }
  if (style === 'sales') {
    return `Hi there,\n\nYour project is exactly the type of work I deliver best: fast execution, low communication overhead, and business-ready output.\n\nWhy me:\n- I focus on measurable outcomes, not generic output\n- I deliver milestone-by-milestone so you stay in control\n- I communicate clearly and proactively\n\nExecution plan:\n1) Scope lock + quick win\n2) Core implementation\n3) QA + handover\n\nIf helpful, I can send a 24-hour mini plan before you hire.\n\nBest regards`;
  }
  return `Hi there,\n\nI reviewed your job post carefully and can deliver this project with clear milestones, proactive communication, and production-quality output.\n\nWhat I will do:\n- Clarify scope and success criteria quickly\n- Implement solution with clean, maintainable code\n- Test thoroughly and provide handover support\n\nContext understood:\n${base}\n\nI can start immediately and provide a first progress update within 24 hours.\n\nBest regards`;
}

function buildPricing(mode = 'hourly', minRate = 20, maxRate = 35) {
  if (mode === 'fixed') {
    return {
      type: 'fixed',
      total: 480,
      milestones: [
        { name: 'Discovery', amount: 80, days: 1 },
        { name: 'Implementation', amount: 280, days: 4 },
        { name: 'Testing & Handover', amount: 120, days: 2 },
      ],
    };
  }
  const low = Number(minRate) || 20;
  const high = Number(maxRate) || 35;
  return {
    type: 'hourly',
    recommended_rate: Math.round((low + high) / 2),
    alt_rate_low: low,
    alt_rate_high: high,
  };
}

function buildFollowups(client = 'there', role = 'project') {
  return {
    d1: `Hi ${client}, just checking in on the ${role} post. Happy to answer any questions and share a quick implementation plan.`,
    d3: `Hi ${client}, following up in case this is still open. I can start immediately and provide a first deliverable quickly.`,
    d7: `Hi ${client}, final follow-up from my side. If useful, I can send a concise scope + timeline breakdown before you decide.`,
  };
}

async function run(input, userId) {
  const [rawCmd, rawSub, ...rest] = input.trim().split(/\s+/);

  // command aliases
  const cmdMap = {
    'proposal': 'proposal',
    '提案': 'proposal',
    'create': 'create',
    '评分': 'score',
    'score': 'score',
    '报价': 'price',
    'price': 'price',
    '跟进': 'followup',
    'followup': 'followup',
    '帮助': 'help',
    'help': 'help',
  };
  const cmd = cmdMap[String(rawCmd || '').toLowerCase()] || String(rawCmd || '').toLowerCase();
  const sub = cmdMap[String(rawSub || '').toLowerCase()] || rawSub;

  if (cmd !== 'proposal') {
    return { ok: false, error: 'unknown_command', message: '请使用 proposal 或 提案 命令' };
  }

  // style + preview support: proposal 生成 [预览|preview] [concise|professional|sales] <JD...>
  let style = 'professional';
  let contentTokens = rest;
  let previewMode = false;

  if (cmd === '生成' && ['预览', 'preview'].includes((contentTokens[0] || '').toLowerCase())) {
    previewMode = true;
    contentTokens = contentTokens.slice(1);
  }
  if (cmd === '生成' && ['concise', 'professional', 'sales'].includes((contentTokens[0] || '').toLowerCase())) {
    style = contentTokens[0].toLowerCase();
    contentTokens = contentTokens.slice(1);
  }

  const jd = contentTokens.join(' ');

  // paid calls: 生成(完整版) / 报价 / 跟进
  const paid = cmd === '生成' && !previewMode || sub === '报价' || sub === '跟进';

  if (sub === '评分') {
    return { ok: true, ...scoreJD(jd) };
  }

  if (sub === '报价') {
    const mode = (contentTokens[0] || '').toLowerCase() === 'fixed' || contentTokens[0] || '').toLowerCase() === 'hourly' ? 'fixed' : 'hourly';
    const min = Number(contentTokens[1]) || 20;
    const max = Number(contentTokens[2]) || 35;
    return { ok: true, pricing: buildPricing(mode, min, max) };
  }

  if (sub === '跟进') {
    const client = contentTokens[0] || 'there';
    const role = contentTokens.slice(1).join(' ') || 'project';
    return { ok: true, followups: buildFollowups(client, role) };
  }

  // default: 生成
  const scored = scoreJD(jd);
  const fullProposal = buildProposal(jd, style);

  if (cmd === '生成' && previewMode) {
    const preview = fullProposal.split('\n').slice(0, 3).join('\n');
    return {
      ok: true,
      preview: true,
      proposal_style: style,
      score: scored.score,
      decision: scored.decision,
      summary: scored.summary,
      proposal_preview: preview,
      unlock_hint: '使用「提案 生成 <style> <JD>」解锁完整版（0.001U/次）'
    };
  }

  return {
    ok: true,
    proposal_style: style,
    score: scored.score,
    decision: scored.decision,
    summary: scored.summary,
    proposal_en: fullProposal,
    pricing: buildPricing('hourly', 20, 35),
    milestones: buildPricing('fixed').milestones,
    followups: buildFollowups('there', 'project'),
  };
}

module.exports = {
  name: 'proposal-copilot-v2',
  description: 'Upwork proposal generation with AI scoring, pricing, and follow-up templates',
  version: '2.0.0',
  handle: async (input, context) => {
    const userId = context?.user || 'default_user';
    
    // 解析用户输入
    const tokens = input.trim().split(/\s+/);
    const command = tokens[0]?.toLowerCase();
    const args = tokens.slice(1);
    
    // 处理命令
    return JSON.stringify(await run(command, args, userId), null, 2);
  },
  
  // 技能信息
  info: function() {
    return `🎯 Proposal Copilot v2.0\n\n` +
           `📋 功能:\n` +
           `• 提案 评分 <JD文本>`\n` +
           `• 提案 生成 [concise|professional|sales] <JD文本>  # 付费完整版\n` +
           `• 提案 生成 预览 [concise|professional|sales] <JD文本>  # 免费预览\n` +
           `• 提案 报价 <fixed|hourly> [min] [max]  # 付费建议\n` +
           `• 提案 跟进 <客户名> <岗位简述>  # 付费跟进\n` +
           `• 提案 帮助  # 显示所有命令和用法\n\n` +
           `💎 付费功能: 评分、生成、报价、跟进\n` +
           `• 命名更新: proposal-copilot-v2\n` +
           `• 计费系统: SkillPay.me 集成\n` +
           `• 技能 ID: 585cbb06-8eea-4eb2-b059-9b4a5010bb57\n\n` +
           `🎯 使用示例:\n` +
           `@openclaw 提案 评分 Python API automation budget $500 payment verified\n` +
           `@openclaw 提案 生成 professional Build scraping bot with timeline and deliverables\n` +
           `@openclaw 提案 报价 hourly 25 35\n` +
           `@openclaw 提案 跟进 client web scraping\n`;
  }
};