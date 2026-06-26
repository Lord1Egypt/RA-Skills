#!/usr/bin/env node

/**
 * 谋道 - 基于「道法术器」框架的AI规划工具
 * 
 * 新增调研模块：在生成方案前进行全方位调研
 * 
 * 用法:
 *   node moudao.js --quick "我想做直播"
 *   node moudao.js --deep "我想做副业" --profile "上班族"
 *   node moudao.js --research "我想做直播"  # 新增：调研模式
 *   node moudao.js --diagnose "直播没人看" --context "我想做直播"
 */

const https = require('https');
const http = require('http');

// ========== 调研 Prompt ==========

const RESEARCH_PROMPT = `你是一个专业的商业调研分析师。用户有一个想法，你需要帮助用户进行全面的前期调研。

调研维度：
1. **行业概况**：市场规模、增长趋势、发展阶段、主要玩家
2. **用户画像**：目标用户是谁、核心需求、痛点分析
3. **竞品分析**：主要竞争对手、成功案例、失败教训
4. **门槛评估**：入场门槛、所需资源、核心能力
5. **风险识别**：潜在风险、市场陷阱、常见失败原因
6. **机会窗口**：当前机会点、蓝海区域、差异化方向

要求：
1. 调研要客观真实，基于行业常识和逻辑推理
2. 数据和案例要有说服力，可以用估算数据
3. 风险分析要全面，不回避问题
4. 机会分析要具体，给出可把握的方向
5. 最后给出"调研结论"和"建议是否推进"

严格以JSON格式返回：
{
  "industry": {
    "name": "行业名称",
    "scale": "市场规模估算",
    "growth": "增长趋势描述",
    "stage": "行业阶段（萌芽期/成长期/成熟期/衰退期）",
    "players": ["主要玩家1", "主要玩家2"],
    "summary": "行业概况总结"
  },
  "users": {
    "primary": {"profile": "核心用户画像", "needs": ["需求1"], "painPoints": ["痛点1"]},
    "secondary": {"profile": "次要用户画像", "needs": [], "painPoints": []},
    "summary": "用户分析总结"
  },
  "competitors": {
    "major": [{"name": "竞品名", "strength": "优势", "weakness": "劣势", "share": "市场份额估算"}],
    "successCases": [{"name": "案例名", "key": "成功关键"}],
    "failureCases": [{"name": "案例名", "reason": "失败原因"}],
    "summary": "竞品分析总结"
  },
  "barriers": {
    "entry": {"level": "低/中/高", "factors": ["门槛因素1", "门槛因素2"]},
    "resources": {"required": ["必需资源1"], "nice_to_have": ["加分资源1"]},
    "skills": {"must_have": ["核心能力1"], "learnable": ["可习得能力1"]},
    "summary": "门槛评估总结"
  },
  "risks": {
    "market": ["市场风险1"],
    "operation": ["运营风险1"],
    "financial": ["财务风险1"],
    "legal": ["法律合规风险1"],
    "summary": "风险分析总结"
  },
  "opportunities": {
    "trends": ["趋势机会1"],
    "gaps": ["市场空白1"],
    "differentiation": ["差异化方向1"],
    "summary": "机会分析总结"
  },
  "conclusion": {
    "feasibility": 7,
    "recommendation": "建议是否推进（强烈推荐/推荐/谨慎推荐/不推荐）",
    "reasons": ["理由1", "理由2"],
    "nextSteps": ["下一步建议1", "下一步建议2"]
  }
}`;

// ========== 快速方案 Prompt（调整版） ==========

const QUICK_PLAN_PROMPT = `你是一个基于「道法术器」认知框架的AI顾问。

用户已经完成了前期调研，现在需要根据调研结果生成具体方案。

调研结果会作为输入，你需要：
1. 基于调研结论，判断方案的可行性
2. 结合调研发现的用户画像、竞品情况、门槛要求，定制方案
3. 针对调研发现的风险，给出规避措施
4. 抓住调研发现的机会点，设计差异化策略

道法术器包含四个层级：
- 道（底层规律）：结合调研发现的行业规律
- 法（方法体系）：针对调研发现的门槛和竞品情况
- 术（执行技法）：考虑调研发现的用户需求
- 器（工具推荐）：匹配调研发现的资源要求

严格以JSON格式返回：
{
  "feasibility_check": {
    "score": 8,
    "can_proceed": true,
    "concerns": ["关注点1"],
    "advantages": ["优势1"]
  },
  "anchor": "锚点层级",
  "anchor_analysis": "分析说明",
  "dao": {
    "principles": [{"title": "规律名", "desc": "描述", "from_research": "来自调研的依据"}],
    "misconceptions": [{"wrong": "错误认知", "right": "正确认知"}]
  },
  "fa": [
    {"name": "方法名", "fit": "适合情况", "desc": "描述", "steps": ["步骤1"], "based_on": "基于调研发现"}
  ],
  "shu": [
    {"phase": "阶段名", "weeks": "第X-Y周", "tasks": [{"title": "任务", "hours": "耗时", "standard": "完成标准"}]}
  ],
  "qi": [
    {"task": "场景", "tools": [{"name": "工具名", "free": true, "desc": "描述"}]}
  ],
  "risk_mitigation": [{"risk": "风险", "solution": "规避措施"}],
  "opportunity_capture": [{"opportunity": "机会点", "action": "行动方案"}]
}`;

// ========== 深度规划 Prompt（调整版） ==========

const DEEP_PLAN_PROMPT = `你是一个基于「天时地利人和 × 道法术器」认知框架的AI顾问。

用户已经完成了前期调研，现在需要根据调研结果生成深度规划方案。

调研结果会作为输入，你需要：
1. 天时判断：基于调研的行业趋势和机会窗口
2. 地利分析：基于调研的资源评估和平台选择
3. 人和方案：结合用户画像和竞品分析，定制道法术器方案

要求：
1. 天时判断要引用调研的趋势数据
2. 地利分析要结合调研的资源评估
3. 方案要针对调研发现的用户痛点
4. 要有针对调研风险的规避措施
5. 要抓住调研发现的机会点

严格以JSON格式返回：
{
  "tianshi": {
    "score": 7,
    "trend": "趋势描述（引用调研）",
    "timing": "时机判断",
    "window": "窗口期",
    "risks": ["风险"]
  },
  "dili": {
    "score": 6,
    "resources": "资源分析（引用调研）",
    "platform": "推荐平台",
    "advantages": ["优势"],
    "gaps": ["短板"]
  },
  "anchor": "锚点层级",
  "anchor_analysis": "分析说明",
  "dao": {
    "principles": [{"title": "规律名", "desc": "描述", "from_research": "调研依据"}],
    "misconceptions": [{"wrong": "错误认知", "right": "正确认知"}]
  },
  "fa": [
    {"name": "方法名", "fit": "适配说明", "desc": "描述", "steps": ["步骤"]}
  ],
  "shu": [
    {"phase": "阶段名", "weeks": "第X-Y周", "tasks": [{"title": "任务", "hours": "耗时", "standard": "标准"}]}
  ],
  "qi": [
    {"task": "场景", "tools": [{"name": "工具名", "free": true, "desc": "描述"}]}
  ],
  "risk_mitigation": [{"risk": "风险", "solution": "规避措施"}],
  "opportunity_capture": [{"opportunity": "机会点", "action": "行动方案"}]
}`;

const DIAGNOSE_PROMPT = `用户正在执行一个基于「道法术器」框架的计划，遇到了问题。
诊断问题出在哪一层（天时/地利/道/法/术/器），给出调整建议。

严格以JSON格式返回：
{
  "summary": "诊断总结",
  "issues": [{"level": "天时/地利/道/法/术/器", "problem": "具体问题", "advice": "调整建议"}],
  "adjustment": {"before": "调整前", "after": "调整后"}
}`;

// ========== 工具函数 ==========

function extractJSON(text) {
  try { return JSON.parse(text); } catch {}
  
  const m = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (m) {
    try { return JSON.parse(m[1]); } catch {}
  }
  
  const s = text.indexOf("{");
  const e = text.lastIndexOf("}");
  if (s !== -1 && e > s) {
    let raw = text.substring(s, e + 1);
    raw = raw.replace(/,\s*([}\]])/g, "$1");
    raw = raw.replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g, "");
    try { return JSON.parse(raw); } catch {}
  }
  return null;
}

function callLLM(systemPrompt, userMessage, apiKey, baseUrl) {
  return new Promise((resolve, reject) => {
    const url = new URL(baseUrl || 'https://api.deepseek.com/chat/completions');
    
    const data = JSON.stringify({
      model: process.env.LLM_MODEL || 'deepseek-chat',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userMessage }
      ],
      temperature: 0.3,
      max_tokens: 4096,
      response_format: { type: 'json_object' }
    });
    
    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data),
        'Authorization': `Bearer ${apiKey}`
      }
    };
    
    const client = url.protocol === 'https:' ? https : http;
    
    const req = client.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          if (res.statusCode !== 200) {
            reject(new Error(`API错误: ${res.statusCode} ${body}`));
            return;
          }
          const parsed = JSON.parse(body);
          const content = parsed.choices?.[0]?.message?.content || '{}';
          const result = extractJSON(content);
          if (!result) {
            reject(new Error('无法解析JSON响应'));
            return;
          }
          resolve(result);
        } catch (e) {
          reject(e);
        }
      });
    });
    
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function formatResearchOutput(result, format) {
  if (format === 'json') {
    return JSON.stringify(result, null, 2);
  }
  
  // Markdown 格式
  let md = `# 前期调研报告\n\n`;
  
  // 行业概况
  if (result.industry) {
    md += `## 1. 行业概况\n\n`;
    md += `- **行业名称**: ${result.industry.name}\n`;
    md += `- **市场规模**: ${result.industry.scale}\n`;
    md += `- **增长趋势**: ${result.industry.growth}\n`;
    md += `- **行业阶段**: ${result.industry.stage}\n`;
    md += `- **主要玩家**: ${result.industry.players?.join('、') || '暂无'}\n\n`;
    md += `> ${result.industry.summary}\n\n`;
  }
  
  // 用户分析
  if (result.users) {
    md += `## 2. 用户分析\n\n`;
    md += `### 核心用户\n\n`;
    if (result.users.primary) {
      md += `- **画像**: ${result.users.primary.profile}\n`;
      md += `- **核心需求**: ${result.users.primary.needs?.join('、') || '暂无'}\n`;
      md += `- **痛点**: ${result.users.primary.painPoints?.join('、') || '暂无'}\n\n`;
    }
    md += `> ${result.users.summary}\n\n`;
  }
  
  // 竞品分析
  if (result.competitors) {
    md += `## 3. 竞品分析\n\n`;
    md += `### 主要竞争对手\n\n`;
    md += `| 竞品 | 优势 | 劣势 | 市场份额 |\n`;
    md += `|------|------|------|----------|\n`;
    result.competitors.major?.forEach(c => {
      md += `| ${c.name} | ${c.strength} | ${c.weakness} | ${c.share} |\n`;
    });
    md += `\n### 成功案例\n\n`;
    result.competitors.successCases?.forEach(c => {
      md += `- **${c.name}**: ${c.key}\n`;
    });
    md += `\n### 失败教训\n\n`;
    result.competitors.failureCases?.forEach(c => {
      md += `- **${c.name}**: ${c.reason}\n`;
    });
    md += `\n> ${result.competitors.summary}\n\n`;
  }
  
  // 门槛评估
  if (result.barriers) {
    md += `## 4. 门槛评估\n\n`;
    md += `### 入场门槛\n\n`;
    md += `- **难度**: ${result.barriers.entry?.level}\n`;
    md += `- **门槛因素**: ${result.barriers.entry?.factors?.join('、') || '暂无'}\n\n`;
    md += `### 必需资源\n\n`;
    md += `- **必需**: ${result.barriers.resources?.required?.join('、') || '暂无'}\n`;
    md += `- **加分**: ${result.barriers.resources?.nice_to_have?.join('、') || '暂无'}\n\n`;
    md += `### 核心能力\n\n`;
    md += `- **必须有**: ${result.barriers.skills?.must_have?.join('、') || '暂无'}\n`;
    md += `- **可习得**: ${result.barriers.skills?.learnable?.join('、') || '暂无'}\n\n`;
    md += `> ${result.barriers.summary}\n\n`;
  }
  
  // 风险分析
  if (result.risks) {
    md += `## 5. 风险识别\n\n`;
    md += `| 类型 | 风险 |\n`;
    md += `|------|------|\n`;
    result.risks.market?.forEach(r => md += `| 市场 | ${r} |\n`);
    result.risks.operation?.forEach(r => md += `| 运营 | ${r} |\n`);
    result.risks.financial?.forEach(r => md += `| 财务 | ${r} |\n`);
    result.risks.legal?.forEach(r => md += `| 法律 | ${r} |\n`);
    md += `\n> ${result.risks.summary}\n\n`;
  }
  
  // 机会分析
  if (result.opportunities) {
    md += `## 6. 机会窗口\n\n`;
    md += `### 趋势机会\n\n`;
    result.opportunities.trends?.forEach(t => md += `- ${t}\n`);
    md += `\n### 市场空白\n\n`;
    result.opportunities.gaps?.forEach(g => md += `- ${g}\n`);
    md += `\n### 差异化方向\n\n`;
    result.opportunities.differentiation?.forEach(d => md += `- ${d}\n`);
    md += `\n> ${result.opportunities.summary}\n\n`;
  }
  
  // 调研结论
  if (result.conclusion) {
    md += `---\n\n`;
    md += `## 调研结论\n\n`;
    md += `### 可行性评分: ${result.conclusion.feasibility}/10\n\n`;
    md += `### 建议: **${result.conclusion.recommendation}**\n\n`;
    md += `### 理由\n\n`;
    result.conclusion.reasons?.forEach(r => md += `- ${r}\n`);
    md += `\n### 下一步建议\n\n`;
    result.conclusion.nextSteps?.forEach((s, i) => md += `${i + 1}. ${s}\n`);
  }
  
  return md;
}

function formatPlanOutput(result, format) {
  if (format === 'json') {
    return JSON.stringify(result, null, 2);
  }
  
  // 使用原有的格式化逻辑
  let md = '';
  
  if (result.feasibility_check) {
    md += `## 可行性评估\n\n`;
    md += `**评分**: ${result.feasibility_check.score}/10\n\n`;
    md += `- **建议推进**: ${result.feasibility_check.can_proceed ? '是' : '否'}\n`;
    md += `- **关注点**: ${result.feasibility_check.concerns?.join('、') || '暂无'}\n`;
    md += `- **优势**: ${result.feasibility_check.advantages?.join('、') || '暂无'}\n\n`;
  }
  
  if (result.tianshi) {
    md += `## 天时（时机趋势）\n\n`;
    md += `**评分**: ${result.tianshi.score}/10\n\n`;
    md += `- **趋势**: ${result.tianshi.trend}\n`;
    md += `- **时机**: ${result.tianshi.timing}\n`;
    md += `- **窗口期**: ${result.tianshi.window}\n`;
    md += `- **风险**: ${result.tianshi.risks?.join('、') || '暂无'}\n\n`;
  }
  
  if (result.dili) {
    md += `## 地利（环境资源）\n\n`;
    md += `**评分**: ${result.dili.score}/10\n\n`;
    md += `- **资源分析**: ${result.dili.resources}\n`;
    md += `- **推荐平台**: ${result.dili.platform}\n`;
    md += `- **优势**: ${result.dili.advantages?.join('、') || '暂无'}\n`;
    md += `- **短板**: ${result.dili.gaps?.join('、') || '暂无'}\n\n`;
  }
  
  if (result.anchor) {
    md += `> **锚点层级**: ${result.anchor} — ${result.anchor_analysis}\n\n`;
  }
  
  if (result.dao) {
    md += `## 道（底层规律）\n\n`;
    result.dao.principles?.forEach(p => {
      md += `- **${p.title}**: ${p.desc}`;
      if (p.from_research) md += ` _(调研依据: ${p.from_research})_`;
      md += '\n';
    });
    if (result.dao.misconceptions?.length) {
      md += `\n**常见误区**:\n`;
      result.dao.misconceptions.forEach(m => {
        md += `- ❌ ${m.wrong} → ✅ ${m.right}\n`;
      });
    }
    md += '\n';
  }
  
  if (result.fa?.length) {
    md += `## 法（方法体系）\n\n`;
    result.fa.forEach(f => {
      md += `### ${f.name}\n`;
      md += `> 适合: ${f.fit}\n\n`;
      md += `${f.desc}\n\n`;
      md += `**步骤**: ${f.steps?.join(' → ') || '暂无'}\n\n`;
    });
  }
  
  if (result.shu?.length) {
    md += `## 术（执行技法）\n\n`;
    result.shu.forEach(s => {
      md += `### ${s.phase} (${s.weeks})\n\n`;
      md += `| 任务 | 耗时 | 完成标准 |\n`;
      md += `|------|------|----------|\n`;
      s.tasks?.forEach(t => {
        md += `| ${t.title} | ${t.hours} | ${t.standard} |\n`;
      });
      md += '\n';
    });
  }
  
  if (result.qi?.length) {
    md += `## 器（工具推荐）\n\n`;
    result.qi.forEach(q => {
      md += `### ${q.task}\n\n`;
      q.tools?.forEach(t => {
        md += `- **${t.name}**${t.free ? '（免费）' : ''}: ${t.desc}\n`;
      });
      md += '\n';
    });
  }
  
  if (result.risk_mitigation?.length) {
    md += `## 风险规避\n\n`;
    md += `| 风险 | 规避措施 |\n`;
    md += `|------|----------|\n`;
    result.risk_mitigation.forEach(r => {
      md += `| ${r.risk} | ${r.solution} |\n`;
    });
    md += '\n';
  }
  
  if (result.opportunity_capture?.length) {
    md += `## 机会把握\n\n`;
    md += `| 机会点 | 行动方案 |\n`;
    md += `|--------|----------|\n`;
    result.opportunity_capture.forEach(o => {
      md += `| ${o.opportunity} | ${o.action} |\n`;
    });
    md += '\n';
  }
  
  return md;
}

function printUsage() {
  console.log(`
谋道 - 基于「道法术器」框架的AI规划工具

用法:
  node moudao.js --research "想法"           前期调研
  node moudao.js --quick "想法"              快速方案（含调研）
  node moudao.js --deep "想法"               深度规划（含调研）
  node moudao.js --diagnose "问题"           迭代诊断

选项:
  --research <idea>      前期调研模式（仅调研）
  --quick <idea>         快速方案模式（调研 + 方案）
  --deep <idea>          深度规划模式（调研 + 深度方案）
  --diagnose <problem>   迭代诊断模式

  --profile <info>       用户背景信息
  --constraints <info>   约束条件
  --context <info>       原始目标（诊断模式必填）
  --skip-research        跳过调研，直接生成方案

  --format <format>      输出格式: json | md | text (默认: md)
  --output <file>        输出到文件

环境变量:
  DEEPSEEK_API_KEY       API密钥（必填）
  DEEPSEEK_BASE_URL      API地址（可选）
  LLM_MODEL              模型名称（可选，默认deepseek-chat）

示例:
  # 仅调研
  node moudao.js --research "我想做直播"

  # 快速方案（自动先调研）
  node moudao.js --quick "我想做副业" --profile "上班族，每周10小时"

  # 深度规划（自动先调研）
  node moudao.js --deep "我想开咖啡店"

  # 诊断执行问题
  node moudao.js --diagnose "没人看" --context "我想做直播"
`);
}

// ========== 主函数 ==========

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
    printUsage();
    process.exit(0);
  }
  
  // 解析参数
  let mode = null;
  let idea = null;
  let profile = null;
  let constraints = null;
  let context = null;
  let format = 'md';
  let output = null;
  let skipResearch = false;
  
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--research':
        mode = 'research';
        idea = args[++i];
        break;
      case '--quick':
        mode = 'quick';
        idea = args[++i];
        break;
      case '--deep':
        mode = 'deep';
        idea = args[++i];
        break;
      case '--diagnose':
        mode = 'diagnose';
        idea = args[++i];
        break;
      case '--profile':
        profile = args[++i];
        break;
      case '--constraints':
        constraints = args[++i];
        break;
      case '--context':
        context = args[++i];
        break;
      case '--format':
        format = args[++i];
        break;
      case '--output':
        output = args[++i];
        break;
      case '--skip-research':
        skipResearch = true;
        break;
    }
  }
  
  if (!mode || !idea) {
    console.error('错误: 请指定模式 (--research/--quick/--deep/--diagnose) 和目标想法');
    printUsage();
    process.exit(1);
  }
  
  const apiKey = process.env.DEEPSEEK_API_KEY;
  if (!apiKey) {
    console.error('错误: 请设置环境变量 DEEPSEEK_API_KEY');
    process.exit(1);
  }
  
  const baseUrl = process.env.DEEPSEEK_BASE_URL;
  
  try {
    // 诊断模式不走调研流程
    if (mode === 'diagnose') {
      const userMessage = `目标：${context || '未指定'}\n遇到的问题：${idea}`;
      console.error('正在诊断问题...');
      const result = await callLLM(DIAGNOSE_PROMPT, userMessage, apiKey, baseUrl);
      const outputText = formatPlanOutput(result, format);
      
      if (output) {
        const fs = require('fs');
        fs.writeFileSync(output, outputText);
        console.error(`诊断结果已保存到: ${output}`);
      } else {
        console.log(outputText);
      }
      return;
    }
    
    // 调研模式：仅输出调研报告
    if (mode === 'research') {
      let userMessage = `用户的想法：${idea}`;
      if (profile) userMessage += `\n\n用户背景：${profile}`;
      if (constraints) userMessage += `\n\n约束条件：${constraints}`;
      
      console.error('正在进行前期调研...');
      const researchResult = await callLLM(RESEARCH_PROMPT, userMessage, apiKey, baseUrl);
      const outputText = formatResearchOutput(researchResult, format);
      
      if (output) {
        const fs = require('fs');
        fs.writeFileSync(output, outputText);
        console.error(`调研报告已保存到: ${output}`);
      } else {
        console.log(outputText);
      }
      return;
    }
    
    // 快速/深度模式：先调研，再生成方案
    let researchResult = null;
    
    if (!skipResearch) {
      let researchMessage = `用户的想法：${idea}`;
      if (profile) researchMessage += `\n\n用户背景：${profile}`;
      if (constraints) researchMessage += `\n\n约束条件：${constraints}`;
      
      console.error('第一步：正在进行前期调研...');
      researchResult = await callLLM(RESEARCH_PROMPT, researchMessage, apiKey, baseUrl);
      console.error('调研完成！');
    }
    
    console.error('第二步：正在生成方案...');
    
    let systemPrompt = mode === 'deep' ? DEEP_PLAN_PROMPT : QUICK_PLAN_PROMPT;
    let userMessage = `用户的想法：${idea}`;
    
    if (profile) userMessage += `\n\n用户背景：${profile}`;
    if (constraints) userMessage += `\n\n约束条件：${constraints}`;
    
    if (researchResult) {
      userMessage += `\n\n=== 前期调研结果 ===\n`;
      userMessage += `\n【行业概况】${researchResult.industry?.summary || '暂无'}`;
      userMessage += `\n【用户分析】${researchResult.users?.summary || '暂无'}`;
      userMessage += `\n【竞品分析】${researchResult.competitors?.summary || '暂无'}`;
      userMessage += `\n【门槛评估】${researchResult.barriers?.summary || '暂无'}`;
      userMessage += `\n【风险分析】${researchResult.risks?.summary || '暂无'}`;
      userMessage += `\n【机会分析】${researchResult.opportunities?.summary || '暂无'}`;
      userMessage += `\n【可行性评分】${researchResult.conclusion?.feasibility || '暂无'}/10`;
      userMessage += `\n【建议】${researchResult.conclusion?.recommendation || '暂无'}`;
      userMessage += `\n【下一步建议】${researchResult.conclusion?.nextSteps?.join('、') || '暂无'}`;
    }
    
    const planResult = await callLLM(systemPrompt, userMessage, apiKey, baseUrl);
    
    // 输出
    let outputText = '';
    
    if (researchResult && format !== 'json') {
      outputText += formatResearchOutput(researchResult, format);
      outputText += '\n---\n\n';
      outputText += `# 执行方案\n\n`;
      outputText += formatPlanOutput(planResult, format);
    } else {
      outputText = formatPlanOutput(planResult, format);
    }
    
    if (output) {
      const fs = require('fs');
      fs.writeFileSync(output, outputText);
      console.error(`方案已保存到: ${output}`);
    } else {
      console.log(outputText);
    }
    
  } catch (error) {
    console.error('错误:', error.message);
    process.exit(1);
  }
}

main();
