// Simple stateMachine.js generator - no template strings
const fs = require('fs');
const path = require('path');

const content = `/**
 * 蜂巢状态机 (Hive State Machine)
 * "猎犬与蜂巢"框架 — 蜂巢管控层
 */

import fs from 'node:fs';
import path from 'node:path';

const PHASES = [
  { number: 1, key: 'deconstruction', label: '拆解与发散（Task Deconstruction）' },
  { number: 2, key: 'exploration', label: '单点深度爆破（The Exploration）' },
  { number: 3, key: 'synthesis', label: '收敛与拼图（Synthesis）' },
  { number: 4, key: 'verification', label: '交叉验证与补漏（Verification）' },
  { number: 5, key: 'finalization', label: '终稿输出（Finalization）' },
];

const PHASE_KEYS = PHASES.map(p => p.key);

const DEFAULT_DIRS = {
  masterPlan: '00_Master_Plan.md',
  extracted: '02_Extracted_Facts',
  drafts: '03_Drafts',
  finalReport: '04_Final_Report.md',
  sopChecklist: 'SOP_Checklist.md',
  decisionLog: 'Decision_Log.md',
};

const PHASE_STEPS = {
  1: [
    { text: '分析用户课题，检索基础背景', output: DEFAULT_DIRS.masterPlan },
    { text: '生成包含5-8个维度的假设树/大纲，写入 {masterPlan}', output: DEFAULT_DIRS.masterPlan },
    { text: '将大纲转化为N个子研究任务，写入子任务清单', output: DEFAULT_DIRS.masterPlan },
  ],
  2: [
    { text: '读取子任务清单', output: DEFAULT_DIRS.masterPlan },
    { text: '为每个子任务派生猎犬Agent', output: DEFAULT_DIRS.extracted },
    { text: '检查所有猎犬是否完成（ls {extracted}/ 查看文件）', output: DEFAULT_DIRS.extracted },
    { text: '评估猎犬带回的证据充分度', output: DEFAULT_DIRS.extracted },
  ],
  3: [
    { text: '启动Writer Agent（只读本地文件，禁止联网）', output: DEFAULT_DIRS.drafts },
    { text: 'Writer读取 {masterPlan} + {extracted}/ 所有材料', output: DEFAULT_DIRS.drafts },
    { text: '生成 {drafts}/ 中的章节初稿', output: DEFAULT_DIRS.drafts },
    { text: '检查初稿完整性', output: DEFAULT_DIRS.drafts },
  ],
  4: [
    { text: '启动Critic Agent审查初稿', output: DEFAULT_DIRS.drafts },
    { text: 'Critic寻找逻辑断层、缺乏数据支撑、来源不明的段落', output: null },
    { text: '如有重大漏洞 → 退回阶段2，派新猎犬补充证据', output: null },
    { text: 'Critic通过 → 打钩', output: DEFAULT_DIRS.drafts },
  ],
  5: [
    { text: 'Writer根据Critic反馈修订终稿', output: DEFAULT_DIRS.finalReport },
    { text: '写入 {finalReport}', output: DEFAULT_DIRS.finalReport },
    { text: '生成执行摘要', output: DEFAULT_DIRS.finalReport },
  ],
};

function timestamp() {
  return new Date().toISOString().replace('T', ' ').slice(0, 19);
}

function safeRead(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch {
    return null;
  }
}

function exists(targetPath) {
  try {
    fs.accessSync(targetPath);
    return true;
  } catch {
    return false;
  }
}

function fillStepText(stepText, directories) {
  let text = stepText;
  for (const [key, val] of Object.entries(directories)) {
    const pattern = '{' + key + '}';
    text = text.replace(new RegExp(pattern, 'g'), val);
  }
  return text;
}

function buildPhaseBlock(phase, directories, subTasks) {
  const steps = PHASE_STEPS[phase.number] || [];
  const lines = [];
  const phaseLabel = '阶段 ' + phase.number + '：' + phase.label;
  lines.push('## ' + phaseLabel);
  lines.push('');

  const statusDesc = phaseStatusDesc(phase.key);
  lines.push('**状态描述**：' + statusDesc);
  lines.push('');

  if (phase.number > 1) {
    const prevPhase = PHASES[phase.number - 2];
    const prevLabel = '阶段 ' + prevPhase.number + '（' + prevPhase.label + '）';
    lines.push('**前置条件**：' + prevLabel + '全部步骤已打钩 ✅');
    lines.push('');
  }

  lines.push('**执行动作**：');
  for (const step of steps) {
    const filledText = fillStepText(step.text, directories);
    lines.push('[ ] ' + filledText);
  }
  lines.push('');

  const outputs = steps
    .filter(s => s.output)
    .map(s => fillStepText(s.output, directories));
  if (outputs.length > 0) {
    lines.push('**产出物路径**：' + outputs.join('、'));
    lines.push('');
  }

  lines.push('**完成标记**：[待完成]');
  lines.push('');

  return lines.join('\\n');
}

function phaseStatusDesc(key) {
  const map = {
    deconstruction: '将用户课题拆解为可独立探索的子问题，建立研究大纲与假设树',
    exploration: '为每个子问题派生猎犬Agent，独立深度探索并带回事实证据',
    synthesis: '将所有猎犬带回的证据按大纲拼合，生成章节初稿',
    verification: 'Critic审查初稿，寻找逻辑断层和数据缺失；重大漏洞退回阶段2补证',
    finalization: '根据Critic反馈修订终稿，输出完整研究报告与执行摘要',
  };
  return map[key] || '';
}

function parsePhaseHeader(line) {
  const m = line.match(/^##\\s+阶段\\s+(\\d+)/);
  if (m) return parseInt(m[1], 10);
  return null;
}

function parseStepCheck(line) {
  const m = line.match(/^\\[(x| )\\]\\s+(.*)/);
  if (m) return { checked: m[1] === 'x', text: m[2] };
  return null;
}

export function generateSOP(goal, subTasks = [], directories = {}) {
  const dirs = { ...DEFAULT_DIRS, ...directories };
  const phaseBlocks = PHASES.map(phase => buildPhaseBlock(phase, dirs, subTasks));

  let sopContent = '# 研究流程状态机 — ' + goal + '\\n';
  sopContent += '> 生成时间：' + timestamp() + '\\n';
  sopContent += '> 研究目标：' + goal + '\\n';
  sopContent += '> 总阶段数：' + PHASES.length + '\\n';
  sopContent += '> 严格模式：不可跳跃、不可乱序、每步必打钩\\n';
  sopContent += '---\\n\\n';
  sopContent += phaseBlocks.join('\\n');
  sopContent += '---\\n\\n';
  sopContent += '## 快速状态总览\\n\\n';
  sopContent += '| 阶段 | 状态 | 完成时间 |\\n';
  sopContent += '|------|------|----------|\\n';
  sopContent += PHASES.map(p => '| ' + p.number + '. ' + p.label.split('（')[0] + ' | ⬜ 待执行 | — |').join('\\n');
  sopContent += '\\n';

  const sopPath = dirs.sopChecklist;
  const decisionLogContent = '# 决策日志 — ' + goal + '\\n\\n';
  const decisionLogPath = dirs.decisionLog;

  return { sopContent, sopPath, decisionLogContent, decisionLogPath };
}

export function readSOPState(sopPath) {
  const content = safeRead(sopPath);
  if (!content) {
    return { currentPhase: null, phases: [], completedPhases: [], pendingPhases: PHASES.map(p => p.number), violations: ['SOP文件不存在: ' + sopPath] };
  }

  const lines = content.split('\\n');
  const phases = [];
  let currentPhase = null;
  let currentPhaseObj = null;
  const violations = [];

  for (const line of lines) {
    const phaseNum = parsePhaseHeader(line);
    if (phaseNum) {
      if (currentPhaseObj) {
        phases.push(currentPhaseObj);
      }
      currentPhase = phaseNum;
      const phaseDef = PHASES.find(p => p.number === phaseNum);
      currentPhaseObj = {
        number: phaseNum,
        label: phaseDef ? phaseDef.label : '阶段' + phaseNum,
        totalSteps: 0,
        completedSteps: 0,
        steps: [],
      };
      continue;
    }

    if (currentPhaseObj) {
      const step = parseStepCheck(line);
      if (step) {
        currentPhaseObj.totalSteps++;
        currentPhaseObj.steps.push(step);
        if (step.checked) {
          currentPhaseObj.completedSteps++;
        }
      }
    }
  }

  if (currentPhaseObj) {
    phases.push(currentPhaseObj);
  }

  const completedPhases = [];
  const pendingPhases = [];
  let foundCurrent = false;

  for (const p of phases) {
    if (p.completedSteps === p.totalSteps && p.totalSteps > 0) {
      completedPhases.push(p.number);
      if (!foundCurrent) continue;
    } else {
      if (!foundCurrent) {
        foundCurrent = true;
        currentPhase = p.number;
      }
      pendingPhases.push(p.number);
    }
  }

  for (const completedNum of completedPhases) {
    for (let i = 1; i < completedNum; i++) {
      if (!completedPhases.includes(i) && phases.find(p => p.number === i)) {
        violations.push('阶段' + completedNum + '已完成，但阶段' + i + '未完成 — 流程跳跃违规');
      }
    }
  }

  if (completedPhases.length === phases.length && phases.length > 0) {
    currentPhase = null;
  }

  return {
    currentPhase,
    phases,
    completedPhases,
    pendingPhases,
    violations,
  };
}

export function advanceSOPState(sopPath, phaseName, resultSummary = {}) {
  const phaseNum = resolvePhaseNumber(phaseName);
  if (!phaseNum) {
    return { success: false, message: '无法识别阶段标识: ' + phaseName };
  }

  const state = readSOPState(sopPath);
  if (state.violations.length > 0) {
    return { success: false, message: '存在流程违规，无法推进: ' + state.violations.join('; ') };
  }

  const validation = validatePhaseTransition(sopPath, null, phaseNum);
  if (!validation.valid) {
    return { success: false, message: '阶段转换不合法: ' + validation.reason };
  }

  const content = safeRead(sopPath);
  if (!content) {
    return { success: false, message: 'SOP文件不存在: ' + sopPath };
  }

  let updated = content;
  const phaseDef = PHASES.find(p => p.number === phaseNum);
  const completedSteps = resultSummary.completedSteps || [];

  const lines = updated.split('\\n');
  let inTargetPhase = false;
  let nextPhaseFound = false;

  for (let i = 0; i < lines.length; i++) {
    const phaseNumInLine = parsePhaseHeader(lines[i]);

    if (phaseNumInLine === phaseNum) {
      inTargetPhase = true;
      continue;
    }
    if (phaseNumInLine && phaseNumInLine !== phaseNum && inTargetPhase) {
      nextPhaseFound = true;
      break;
    }

    if (inTargetPhase) {
      const step = parseStepCheck(lines[i]);
      if (step && !step.checked) {
        const shouldCheck = completedSteps.length === 0 || completedSteps.some(cs => step.text.includes(cs));
        if (shouldCheck) {
          lines[i] = lines[i].replace('[ ]', '[x]');
        }
      }
    }
  }

  const phaseObj = state.phases.find(p => p.number === phaseNum);
  const allChecked = phaseObj
    ? (phaseObj.completedSteps + (completedSteps.length === 0 ? phaseObj.totalSteps : completedSteps.length)) >= phaseObj.totalSteps
    : true;

  if (allChecked) {
    for (let i = 0; i < lines.length; i++) {
      if (inTargetPhase && lines[i].includes('[待完成]')) {
        lines[i] = lines[i].replace('[待完成]', '✅ 已完成 @ ' + timestamp());
      }
    }
    const phaseShortLabel = phaseDef.label.split('（')[0];
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].includes(phaseNum + '. ' + phaseShortLabel) && lines[i].includes('⬜')) {
        lines[i] = lines[i].replace('⬜ 待执行', '✅ 已完成').replace('—', timestamp());
      }
    }
  }

  updated = lines.join('\\n');
  fs.writeFileSync(sopPath, updated, 'utf-8');

  if (resultSummary.decision) {
    const dirs = deriveDirsFromSOPPath(sopPath);
    logDecision(dirs.decisionLog, resultSummary.decision, resultSummary.reason || '未记录', { ...resultSummary.context, phase: '阶段' + phaseNum + ':' + phaseDef.label, alternatives: resultSummary.alternatives });
  }

  return { success: true, message: '阶段' + phaseNum + '推进成功', updatedContent: updated };
}

export function buildHivePrompt(sopPath, goal) {
  const dirs = deriveDirsFromSOPPath(sopPath);
  const baseDir = path.dirname(sopPath);

  let prompt = '# 蜂巢主控系统提示词\\n\\n';
  prompt += '## 人设定义\\n\\n';
  prompt += '你不是研究员，你是流程状态机执行程序。\\n';
  prompt += '你的唯一职责是按照 SOP 文件（' + sopPath + '）中的流程阶段，逐条打钩推进。\\n';
  prompt += '你没有自由发挥的空间。你是一台机器，不是一个人。\\n\\n';
  prompt += '## 核心指令\\n\\n';
  prompt += '1. **每次行动前，先读取 ' + sopPath + ' 查看当前进度**\\n';
  prompt += '   - 识别当前阶段（第一个有未打钩步骤的阶段）\\n';
  prompt += '   - 只执行当前阶段的步骤\\n';
  prompt += '   - 绝不跳步、绝不提前执行后续阶段\\n\\n';
  prompt += '2. **当前状态没打钩，绝对不允许执行下一个状态**\\n';
  prompt += '   - 阶段1全部打钩 → 才能进入阶段2\\n';
  prompt += '   - 阶段2全部打钩 → 才能进入阶段3\\n';
  prompt += '   - 任何阶段未完成，后续阶段一律禁止\\n\\n';
  prompt += '3. **通讯方式：文件系统协议**\\n';
  prompt += '   - 不跟子代理聊天，通过文件系统下达指令和接收成果\\n';
  prompt += '   - 指令文件：' + path.join(baseDir, dirs.extracted) + '/ → 猎犬任务描述文件\\n';
  prompt += '   - 成果文件：' + path.join(baseDir, dirs.extracted) + '/ → 猎犬带回的证据文件\\n';
  prompt += '   - 初稿文件：' + path.join(baseDir, dirs.drafts) + '/ → Writer输出\\n';
  prompt += '   - 终稿文件：' + path.join(baseDir, dirs.finalReport) + ' → 最终报告\\n\\n';
  prompt += '4. **决策日志：每个关键决策必须记录理由**\\n';
  prompt += '   - 记录到 ' + path.join(baseDir, dirs.decisionLog) + '\\n';
  prompt += '   - 格式：时间 | 决策内容 | 原因 | 上下文 | 替代方案\\n';
  prompt += '   - 没有理由的决策 = 坏决策\\n\\n';
  prompt += '5. **阶段完成后的动作**\\n';
  prompt += '   - 调用 advanceSOPState() 打钩推进\\n';
  prompt += '   - 记录决策日志\\n';
  prompt += '   - 检查产出物文件是否真实存在\\n';
  prompt += '   - 更新 SOP 状态总览\\n\\n';
  prompt += '## 研究目标\\n\\n';
  prompt += goal + '\\n\\n';
  prompt += '## 严格约束清单\\n\\n';
  prompt += '- ❌ 不允许跳跃阶段\\n';
  prompt += '- ❌ 不允许乱序执行步骤\\n';
  prompt += '- ❌ 不允许在没有证据的情况下做结论\\n';
  prompt += '- ❌ 不允许忽略 Critic 的反馈\\n';
  prompt += '- ❌ 不允许不记录决策理由\\n';
  prompt += '- ✅ 必须逐条打钩推进\\n';
  prompt += '- ✅ 必须验证产出物存在\\n';
  prompt += '- ✅ 必须记录决策日志\\n';
  prompt += '- ✅ Critic 发现重大漏洞时，必须退回阶段2\\n\\n';
  prompt += '## 执行循环\\n\\n';
  prompt += '```\\n';
  prompt += 'while (有未完成阶段) {\\n';
  prompt += '  1. readSOPState() → 获取当前阶段\\n';
  prompt += '  2. 执行当前阶段步骤\\n';
  prompt += '  3. validatePhaseTransition() → 验证转换合法性\\n';
  prompt += '  4. advanceSOPState() → 打钩推进\\n';
  prompt += '  5. logDecision() → 记录关键决策\\n';
  prompt += '}\\n';
  prompt += '```\\n';

  return prompt;
}

export function validatePhaseTransition(sopPath, fromPhase, toPhase) {
  const state = readSOPState(sopPath);
  const baseDir = path.dirname(sopPath);

  if (!PHASES.find(p => p.number === toPhase)) {
    return { valid: false, reason: '目标阶段' + toPhase + '不存在（合法范围1-5）' };
  }

  for (let i = 1; i < toPhase; i++) {
    if (!state.completedPhases.includes(i)) {
      const phaseDef = PHASES.find(p => p.number === i);
      return { valid: false, reason: '前置阶段' + i + '（' + phaseDef?.label + '）尚未完成' };
    }
  }

  const dirs = deriveDirsFromSOPPath(sopPath);
  const missingFiles = [];

  const requiredOutputs = {
    1: [path.join(baseDir, dirs.masterPlan)],
    2: [path.join(baseDir, dirs.extracted)],
    3: [path.join(baseDir, dirs.drafts)],
    4: [],
    5: [path.join(baseDir, dirs.finalReport)],
  };

  const prevPhase = toPhase - 1;
  if (prevPhase >= 1 && requiredOutputs[prevPhase]) {
    for (const filePath of requiredOutputs[prevPhase]) {
      if (!exists(filePath)) {
        missingFiles.push(filePath);
      }
    }
  }

  if (missingFiles.length > 0) {
    return { valid: false, reason: '前置阶段' + prevPhase + '的产出物文件缺失', missingFiles };
  }

  if (state.violations.length > 0) {
    return { valid: false, reason: '流程存在违规: ' + state.violations.join('; ') };
  }

  return { valid: true };
}

export function logDecision(logPath, decision, reason, context = {}) {
  let decisionLogPath = logPath;
  if (logPath.endsWith('.md') && !logPath.includes('Decision_Log')) {
    const dirs = deriveDirsFromSOPPath(logPath);
    decisionLogPath = path.join(path.dirname(logPath), dirs.decisionLog);
  }

  const phaseLabel = context.phase || '未指定阶段';
  const alternatives = context.alternatives || '未考虑';
  const contextStr = typeof context === 'string' ? context : JSON.stringify(context, null, 2);

  const entry = '## ' + timestamp() + ' ' + phaseLabel + '\\n\\n';
  entry += '- **决策**: ' + decision + '\\n';
  entry += '- **原因**: ' + reason + '\\n';
  entry += '- **替代方案**: ' + alternatives + '\\n';
  entry += '- **上下文**: ' + contextStr + '\\n\\n';

  const existing = safeRead(decisionLogPath) || '';
  const updated = existing.trimEnd() + '\\n\\n' + entry;

  const dir = path.dirname(decisionLogPath);
  if (!exists(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.writeFileSync(decisionLogPath, updated + '\\n', 'utf-8');

  return { success: true, message: '决策已记录到 ' + decisionLogPath };
}

function deriveDirsFromSOPPath(sopPath) {
  return { ...DEFAULT_DIRS };
}

function resolvePhaseNumber(phaseName) {
  if (typeof phaseName === 'number') return phaseName;
  const asNum = parseInt(phaseName, 10);
  if (!isNaN(asNum) && asNum >= 1 && asNum <= 5) return asNum;
  const byKey = PHASES.find(p => p.key === phaseName);
  if (byKey) return byKey.number;
  const m = phaseName.match(/阶段\\s*(\\d+)/);
  if (m) return parseInt(m[1], 10);
  const byLabel = PHASES.find(p => phaseName.includes(p.label) || phaseName.includes(p.label.split('（')[0]));
  if (byLabel) return byLabel.number;
  return null;
}

export {
  PHASES,
  PHASE_KEYS,
  DEFAULT_DIRS,
  generateSOP,
  readSOPState,
  advanceSOPState,
  buildHivePrompt,
  validatePhaseTransition,
  logDecision,
};
`;

const outputPath = path.join(__dirname, 'stateMachine.js');
fs.writeFileSync(outputPath, content, 'utf-8');
console.log('stateMachine.js created successfully');
console.log('File size:', (content.length / 1024).toFixed(2), 'KB');
