/**
 * 物理外挂记忆池 - "猎犬与蜂巢"框架第一层
 *
 * 核心目标：通过本地文件系统替代LLM上下文窗口传递信息
 * 优势：
 * - 上下文溢出风险低
 * - 子代理崩溃时信息不丢失
 * - 主代理可高效检索大量研究结果
 *
 * 文件路径：C:\Users\mrcft\.openclaw\workspace\skills\multi-agent-config-manager\lib\memoryPool.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ===== 配置常量 =====

const PROJECT_ROOT = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace', 'research_projects');
const PROJECT_SUBDIRS = [
  '00_Master_Plan.md',
  '01_Raw_Sources',
  '02_Extracted_Facts',
  '03_Drafts',
  '04_Final_Report.md',
  'SOP_Checklist.md',
  'Decision_Log.md',
  'hound_manifest.json'
];

// ===== 工具函数 =====

/**
 * 获取当前时间戳
 */
function getCurrentTimestamp() {
  const now = new Date();
  return {
    iso: now.toISOString(),
    unix: Math.floor(now.getTime() / 1000),
    display: now.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })
  };
}

/**
 * 原子性写入（写入前备份）
 */
async function atomicWrite(filePath, content) {
  const dir = path.dirname(filePath);

  // 确保目录存在
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // 备份已存在的文件
  if (fs.existsSync(filePath)) {
    const backupPath = `${filePath}.backup_${Date.now()}`;
    fs.copyFileSync(filePath, backupPath);
  }

  // 写入新内容
  fs.writeFileSync(filePath, content, 'utf8');
}

/**
 * 读取JSON文件
 */
function readJson(filePath) {
  if (!fs.existsSync(filePath)) {
    return null;
  }
  const content = fs.readFileSync(filePath, 'utf8');
  try {
    return JSON.parse(content);
  } catch (e) {
    console.error(`Failed to parse JSON: ${filePath}`, e);
    return null;
  }
}

/**
 * 写入JSON文件
 */
function writeJson(filePath, data) {
  const content = JSON.stringify(data, null, 2);
  atomicWrite(filePath, content);
}

// ===== 1. 研究项目目录初始化器 =====

/**
 * 初始化研究项目目录结构
 * @param {string} goal - 研究目标
 * @param {string} projectName - 项目名称
 * @returns {string} 项目目录路径
 */
export function initProject(goal, projectName) {
  // 创建项目目录
  const projectDir = path.join(PROJECT_ROOT, projectName);
  if (fs.existsSync(projectDir)) {
    throw new Error(`Project directory already exists: ${projectDir}`);
  }

  fs.mkdirSync(projectDir, { recursive: true });

  // 创建子目录和文件
  PROJECT_SUBDIRS.forEach(item => {
    const fullPath = path.join(projectDir, item);
    if (item.endsWith('.md') || item.endsWith('.json')) {
      atomicWrite(fullPath, '');
    } else {
      fs.mkdirSync(fullPath, { recursive: true });
    }
  });

  // 初始化主大纲
  const masterPlanPath = path.join(projectDir, '00_Master_Plan.md');
  const initialPlan = `# ${projectName}

## 研究目标
${goal}

## 项目结构
- 00_Master_Plan.md - 主研究大纲与进度指示器
- 01_Raw_Sources/ - 原始网页和PDF
- 02_Extracted_Facts/ - 提取的结构化事实
- 03_Drafts/ - 章节初稿
- 04_Final_Report.md - 最终报告
- SOP_Checklist.md - 状态机检查清单
- Decision_Log.md - 决策日志
- hound_manifest.json - 猎犬任务清单

## 进度指示器
- Phase 1: Planning - 研究规划
- Phase 2: Hunting - 信息搜集
- Phase 3: Drafting - 初稿撰写
- Phase 4: Reviewing - 审核修订
- Phase 5: Finalizing - 最终定稿

> **创建时间**: ${getCurrentTimestamp().display}
`;

  atomicWrite(masterPlanPath, initialPlan);

  // 初始化猎犬清单
  const houndManifestPath = path.join(projectDir, 'hound_manifest.json');
  const initialManifest = {
    version: '1.0',
    createdAt: getCurrentTimestamp().iso,
    hounds: [],
    stats: {
      total: 0,
      completed: 0,
      pending: 0,
      failed: 0
    }
  };
  writeJson(houndManifestPath, initialManifest);

  // 初始化决策日志
  const decisionLogPath = path.join(projectDir, 'Decision_Log.md');
  const initialDecisionLog = `# 决策日志

## 决策记录

> **创建时间**: ${getCurrentTimestamp().display}

### 决策格式
- **时间**: YYYY-MM-DD HH:mm:ss
- **决策**: [简短描述]
- **原因**: [决策依据]
- **结果**: [决策结果]
- **影响**: [长期影响]

---

`;

  atomicWrite(decisionLogPath, initialDecisionLog);

  // 初始化SOP检查清单
  const sopChecklistPath = path.join(projectDir, 'SOP_Checklist.md');
  const initialSopChecklist = `# SOP检查清单

## 研究流程检查点

### Phase 1: Planning
- [ ] 明确研究目标和范围
- [ ] 制定子任务分解
- [ ] 分配猎犬任务

### Phase 2: Hunting
- [ ] 猎犬开始执行
- [ ] 原始来源已收集
- [ ] 事实已提取并验证

### Phase 3: Drafting
- [ ] Writer开始撰写
- [ ] 草稿已保存
- [ ] 各章节完成

### Phase 4: Reviewing
- [ ] Critic审核完成
- [ ] 修订意见已记录
- [ ] 问题已解决

### Phase 5: Finalizing
- [ ] 最终报告生成
- [ ] 所有检查项通过
- [ ] 项目归档

---

> **创建时间**: ${getCurrentTimestamp().display}
`;

  atomicWrite(sopChecklistPath, initialSopChecklist);

  return projectDir;
}

// ===== 2. 主大纲管理器 =====

/**
 * 写入主研究大纲
 * @param {string} projectDir - 项目目录
 * @param {string} planContent - 大纲内容
 */
export function writeMasterPlan(projectDir, planContent) {
  const filePath = path.join(projectDir, '00_Master_Plan.md');
  atomicWrite(filePath, planContent);
}

/**
 * 读取主研究大纲
 * @param {string} projectDir - 项目目录
 * @returns {string|null} 大纲内容
 */
export function readMasterPlan(projectDir) {
  const filePath = path.join(projectDir, '00_Master_Plan.md');
  if (!fs.existsSync(filePath)) {
    return null;
  }
  return fs.readFileSync(filePath, 'utf8');
}

/**
 * 更新主大纲进度标记
 * @param {string} projectDir - 项目目录
 * @param {string} phase - 阶段名称
 * @param {string} status - 状态（pending/running/completed/failed）
 */
export function updateMasterPlanProgress(projectDir, phase, status) {
  const filePath = path.join(projectDir, '00_Master_Plan.md');
  let content = fs.readFileSync(filePath, 'utf8');

  // 更新进度标记
  const progressRegex = new RegExp(`## ${phase}[^\\n]*\\n- \\[\\]`, 'g');
  const statusEmoji = {
    'pending': '⚪',
    'running': '🔵',
    'completed': '🟢',
    'failed': '🔴'
  };

  content = content.replace(progressRegex, `## ${phase}\n- [${statusEmoji[status] || '⚪'}] ${status}`);

  // 更新时间戳
  const timestampRegex = /> \*\*更新时间\*\*: [^\n]*/;
  const newTimestamp = `> **更新时间**: ${getCurrentTimestamp().display}`;
  content = content.replace(timestampRegex, newTimestamp);

  atomicWrite(filePath, content);
}

// ===== 3. 原始来源管理器 =====

/**
 * 保存原始来源
 * @param {string} projectDir - 项目目录
 * @param {string} sourceId - 来源ID
 * @param {string} content - 内容
 * @param {object} metadata - 元数据（URL、抓取时间、来源类型、猎犬ID）
 */
export function saveRawSource(projectDir, sourceId, content, metadata) {
  const rawSourcesDir = path.join(projectDir, '01_Raw_Sources');

  // 确保目录存在
  if (!fs.existsSync(rawSourcesDir)) {
    fs.mkdirSync(rawSourcesDir, { recursive: true });
  }

  const filePath = path.join(rawSourcesDir, `${sourceId}.md`);
  const timestamp = getCurrentTimestamp();

  const sourceContent = `# ${sourceId}

## 元数据
- **URL**: ${metadata.url || 'N/A'}
- **来源类型**: ${metadata.sourceType || 'unknown'}
- **猎犬ID**: ${metadata.houndId || 'N/A'}
- **抓取时间**: ${timestamp.display}
- **Unix时间戳**: ${timestamp.unix}

## 内容
${content}

---

*来源ID: ${sourceId} | 猎犬: ${metadata.houndId || 'N/A'} | 时间: ${timestamp.iso}*
`;

  atomicWrite(filePath, sourceContent);
}

/**
 * 列出所有原始来源
 * @param {string} projectDir - 项目目录
 * @returns {Array} 来源列表
 */
export function listRawSources(projectDir) {
  const rawSourcesDir = path.join(projectDir, '01_Raw_Sources');
  if (!fs.existsSync(rawSourcesDir)) {
    return [];
  }

  const files = fs.readdirSync(rawSourcesDir);
  const sources = [];

  files.forEach(file => {
    if (file.endsWith('.md')) {
      const filePath = path.join(rawSourcesDir, file);
      const stat = fs.statSync(filePath);
      sources.push({
        id: file.replace('.md', ''),
        path: filePath,
        size: stat.size,
        modifiedTime: stat.mtime
      });
    }
  });

  return sources.sort((a, b) => b.modifiedTime - a.modifiedTime);
}

/**
 * 获取特定原始来源
 * @param {string} projectDir - 项目目录
 * @param {string} sourceId - 来源ID
 * @returns {object|null} 来源内容
 */
export function getRawSource(projectDir, sourceId) {
  const rawSourcesDir = path.join(projectDir, '01_Raw_Sources');
  const filePath = path.join(rawSourcesDir, `${sourceId}.md`);

  if (!fs.existsSync(filePath)) {
    return null;
  }

  return fs.readFileSync(filePath, 'utf8');
}

// ===== 4. 提取事实管理器 =====

/**
 * 保存提取的事实
 * @param {string} projectDir - 项目目录
 * @param {string} subTaskId - 子任务ID
 * @param {Array} facts - 事实列表（数据+来源URL+可靠性评级）
 * @param {number} qualityScore - 证据充分度（0-1）
 */
export function saveExtractedFact(projectDir, subTaskId, facts, qualityScore = 1.0) {
  const extractedFactsDir = path.join(projectDir, '02_Extracted_Facts');

  // 确保目录存在
  if (!fs.existsSync(extractedFactsDir)) {
    fs.mkdirSync(extractedFactsDir, { recursive: true });
  }

  const filePath = path.join(extractedFactsDir, `${subTaskId}.md`);
  const timestamp = getCurrentTimestamp();

  // 格式化事实列表
  const factsMarkdown = facts.map((fact, index) => {
    const reliability = fact.reliability || 'medium';
    const reliabilityEmoji = {
      'high': '✅',
      'medium': '⚠️',
      'low': '❌'
    };

    return `### ${index + 1}. ${fact.title || 'Fact ' + (index + 1)}
- **数据**: ${fact.data}
- **来源**: ${fact.sourceUrl}
- **可靠性**: ${reliabilityEmoji[reliability] || '⚠️'} ${reliability.toUpperCase()}
- **猎犬ID**: ${fact.houndId || 'N/A'}
${fact.notes ? `- **备注**: ${fact.notes}` : ''}
`;
  }).join('\n');

  const factContent = `# ${subTaskId} - 提取的事实

## 元数据
- **子任务ID**: ${subTaskId}
- **证据充分度**: ${qualityScore.toFixed(2)} (${qualityScore >= 0.8 ? '高' : qualityScore >= 0.5 ? '中' : '低'})
- **猎犬ID**: ${facts[0]?.houndId || 'N/A'}
- **提取时间**: ${timestamp.display}
- **事实数量**: ${facts.length}

## 提取的事实
${factsMarkdown}

---

*子任务: ${subTaskId} | 猎犬: ${facts[0]?.houndId || 'N/A'} | 事实数: ${facts.length} | 时间: ${timestamp.iso}*
`;

  atomicWrite(filePath, factContent);
}

/**
 * 列出所有已提取事实
 * @param {string} projectDir - 项目目录
 * @returns {Array} 事实列表
 */
export function listExtractedFacts(projectDir) {
  const extractedFactsDir = path.join(projectDir, '02_Extracted_Facts');
  if (!fs.existsSync(extractedFactsDir)) {
    return [];
  }

  const files = fs.readdirSync(extractedFactsDir);
  const facts = [];

  files.forEach(file => {
    if (file.endsWith('.md')) {
      const filePath = path.join(extractedFactsDir, file);
      const stat = fs.statSync(filePath);
      const content = fs.readFileSync(filePath, 'utf8');

      // 解析元数据
      const metadataMatch = content.match(/证据充分度: ([\d.]+)/);
      const factsMatch = content.match(/事实数量: (\d+)/);

      facts.push({
        subTaskId: file.replace('.md', ''),
        path: filePath,
        size: stat.size,
        qualityScore: metadataMatch ? parseFloat(metadataMatch[1]) : 0,
        factCount: factsMatch ? parseInt(factsMatch[1]) : 0,
        modifiedTime: stat.mtime
      });
    }
  });

  return facts.sort((a, b) => b.modifiedTime - a.modifiedTime);
}

/**
 * 按子任务检索事实
 * @param {string} projectDir - 项目目录
 * @param {string} subTaskId - 子任务ID
 * @returns {object|null} 事实内容
 */
export function getExtractedFactsBySubTask(projectDir, subTaskId) {
  const extractedFactsDir = path.join(projectDir, '02_Extracted_Facts');
  const filePath = path.join(extractedFactsDir, `${subTaskId}.md`);

  if (!fs.existsSync(filePath)) {
    return null;
  }

  return fs.readFileSync(filePath, 'utf8');
}

/**
 * 评估事实覆盖度
 * @param {string} projectDir - 项目目录
 * @param {Array} subTaskIds - 子任务ID列表
 * @returns {object} 覆盖度评估结果
 */
export function assessFactsCoverage(projectDir, subTaskIds) {
  const extractedFactsDir = path.join(projectDir, '02_Extracted_Facts');
  const coverage = {
    total: subTaskIds.length,
    covered: 0,
    notCovered: [],
    averageQuality: 0,
    totalFacts: 0,
    details: {}
  };

  if (!fs.existsSync(extractedFactsDir)) {
    return coverage;
  }

  subTaskIds.forEach(subTaskId => {
    const filePath = path.join(extractedFactsDir, `${subTaskId}.md`);

    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf8');
      const qualityMatch = content.match(/证据充分度: ([\d.]+)/);
      const factsMatch = content.match(/事实数量: (\d+)/);

      const qualityScore = qualityMatch ? parseFloat(qualityMatch[1]) : 0;
      const factCount = factsMatch ? parseInt(factsMatch[1]) : 0;

      coverage.covered++;
      coverage.notCovered = coverage.notCovered.filter(id => id !== subTaskId);
      coverage.totalFacts += factCount;

      coverage.details[subTaskId] = {
        covered: true,
        qualityScore: qualityScore,
        factCount: factCount,
        status: qualityScore >= 0.8 ? 'excellent' : qualityScore >= 0.5 ? 'good' : 'needs_work'
      };

      coverage.averageQuality += qualityScore;
    } else {
      coverage.notCovered.push(subTaskId);
      coverage.details[subTaskId] = {
        covered: false,
        qualityScore: 0,
        factCount: 0,
        status: 'not_covered'
      };
    }
  });

  if (coverage.covered > 0) {
    coverage.averageQuality /= coverage.covered;
  }

  return coverage;
}

// ===== 5. 猎犬状态追踪器 =====

/**
 * 注册猎犬任务
 * @param {string} projectDir - 项目目录
 * @param {string} houndId - 猎犬ID
 * @param {string} subTaskId - 子任务ID
 * @param {object} config - 猎犬配置
 */
export function registerHound(projectDir, houndId, subTaskId, config = {}) {
  const houndManifestPath = path.join(projectDir, 'hound_manifest.json');
  const manifest = readJson(houndManifestPath) || {
    version: '1.0',
    createdAt: getCurrentTimestamp().iso,
    hounds: [],
    stats: { total: 0, completed: 0, pending: 0, failed: 0 }
  };

  // 检查是否已存在
  const existingIndex = manifest.hounds.findIndex(h => h.houndId === houndId);
  if (existingIndex >= 0) {
    throw new Error(`Hound already registered: ${houndId}`);
  }

  // 添加新猎犬
  const newHound = {
    houndId,
    subTaskId,
    status: 'pending',
    config,
    createdAt: getCurrentTimestamp().iso,
    startedAt: null,
    completedAt: null,
    summary: null,
    errors: []
  };

  manifest.hounds.push(newHound);
  manifest.stats.total++;

  writeJson(houndManifestPath, manifest);
}

/**
 * 更新猎犬状态
 * @param {string} projectDir - 项目目录
 * @param {string} houndId - 猎犬ID
 * @param {string} status - 状态（pending/running/completed/failed）
 * @param {string} summary - 状态摘要
 */
export function updateHoundStatus(projectDir, houndId, status, summary = '') {
  const houndManifestPath = path.join(projectDir, 'hound_manifest.json');
  const manifest = readJson(houndManifestPath);

  if (!manifest) {
    throw new Error('Hound manifest not found');
  }

  const hound = manifest.hounds.find(h => h.houndId === houndId);
  if (!hound) {
    throw new Error(`Hound not found: ${houndId}`);
  }

  const timestamp = getCurrentTimestamp();
  const oldStatus = hound.status;

  // 更新状态
  hound.status = status;

  // 更新时间戳
  if (status === 'running' && !hound.startedAt) {
    hound.startedAt = timestamp.iso;
  } else if (status === 'completed') {
    hound.completedAt = timestamp.iso;
    if (oldStatus !== 'completed') {
      manifest.stats.completed++;
      manifest.stats.pending--;
    }
  } else if (status === 'failed') {
    hound.errors = hound.errors || [];
    hound.errors.push({
      time: timestamp.iso,
      message: summary || 'Unknown error'
    });
    manifest.stats.failed++;
    manifest.stats.pending--;
  }

  hound.summary = summary;

  writeJson(houndManifestPath, manifest);
}

/**
 * 获取猎犬清单
 * @param {string} projectDir - 项目目录
 * @returns {object} 猎犬清单
 */
export function getHoundManifest(projectDir) {
  const houndManifestPath = path.join(projectDir, 'hound_manifest.json');
  return readJson(houndManifestPath);
}

/**
 * 获取未完成的猎犬列表
 * @param {string} projectDir - 项目目录
 * @returns {Array} 未完成的猎犬
 */
export function getPendingHounds(projectDir) {
  const manifest = getHoundManifest(projectDir);
  if (!manifest) {
    return [];
  }
  return manifest.hounds.filter(h => h.status === 'pending');
}

/**
 * 获取已完成的猎犬列表
 * @param {string} projectDir - 项目目录
 * @returns {Array} 已完成的猎犬
 */
export function getCompletedHounds(projectDir) {
  const manifest = getHoundManifest(projectDir);
  if (!manifest) {
    return [];
  }
  return manifest.hounds.filter(h => h.status === 'completed');
}

// ===== 6. 草稿管理器 =====

/**
 * 保存草稿
 * @param {string} projectDir - 项目目录
 * @param {string} sectionName - 章节名称
 * @param {string} content - 草稿内容
 */
export function saveDraft(projectDir, sectionName, content) {
  const draftsDir = path.join(projectDir, '03_Drafts');

  // 确保目录存在
  if (!fs.existsSync(draftsDir)) {
    fs.mkdirSync(draftsDir, { recursive: true });
  }

  const filePath = path.join(draftsDir, `${sectionName}.md`);
  const timestamp = getCurrentTimestamp();

  const draftContent = `# ${sectionName}

## 元数据
- **创建时间**: ${timestamp.display}
- **创建时间戳**: ${timestamp.iso}
- **章节**: ${sectionName}

## 内容
${content}

---

*草稿: ${sectionName} | 时间: ${timestamp.iso}*
`;

  atomicWrite(filePath, draftContent);
}

/**
 * 列出所有草稿
 * @param {string} projectDir - 项目目录
 * @returns {Array} 草稿列表
 */
export function listDrafts(projectDir) {
  const draftsDir = path.join(projectDir, '03_Drafts');
  if (!fs.existsSync(draftsDir)) {
    return [];
  }

  const files = fs.readdirSync(draftsDir);
  const drafts = [];

  files.forEach(file => {
    if (file.endsWith('.md')) {
      const filePath = path.join(draftsDir, file);
      const stat = fs.statSync(filePath);
      const content = fs.readFileSync(filePath, 'utf8');

      // 解析元数据
      const createdMatch = content.match(/创建时间: ([^\n]+)/);
      const createdMatchIso = content.match(/创建时间戳: ([^\n]+)/);

      drafts.push({
        sectionName: file.replace('.md', ''),
        path: filePath,
        size: stat.size,
        createdAt: createdMatch ? createdMatch[1] : '',
        createdAtIso: createdMatchIso ? createdMatchIso[1] : '',
        modifiedTime: stat.mtime
      });
    }
  });

  return drafts.sort((a, b) => b.modifiedTime - a.modifiedTime);
}

/**
 * 读取所有草稿内容
 * @param {string} projectDir - 项目目录
 * @returns {object} 草稿内容映射
 */
export function readAllDrafts(projectDir) {
  const drafts = listDrafts(projectDir);
  const draftsContent = {};

  drafts.forEach(draft => {
    const content = fs.readFileSync(draft.path, 'utf8');
    // 提取内容（跳过元数据部分）
    const contentMatch = content.match(/## 内容\n([\s\S]*)/);
    draftsContent[draft.sectionName] = contentMatch ? contentMatch[1] : content;
  });

  return draftsContent;
}

// ===== 7. 最终报告管理器 =====

/**
 * 保存最终报告
 * @param {string} projectDir - 项目目录
 * @param {string} content - 报告内容
 */
export function saveFinalReport(projectDir, content) {
  const filePath = path.join(projectDir, '04_Final_Report.md');
  const timestamp = getCurrentTimestamp();

  const reportContent = `# 最终研究报告

## 元数据
- **生成时间**: ${timestamp.display}
- **生成时间戳**: ${timestamp.iso}

## 研究报告
${content}

---

*最终报告 | 时间: ${timestamp.iso}*
`;

  atomicWrite(filePath, reportContent);
}

/**
 * 读取最终报告
 * @param {string} projectDir - 项目目录
 * @returns {string|null} 报告内容
 */
export function readFinalReport(projectDir) {
  const filePath = path.join(projectDir, '04_Final_Report.md');
  if (!fs.existsSync(filePath)) {
    return null;
  }
  return fs.readFileSync(filePath, 'utf8');
}

// ===== 8. 项目状态总览器 =====

/**
 * 获取项目整体状态
 * @param {string} projectDir - 项目目录
 * @returns {object} 项目状态
 */
export function getProjectStatus(projectDir) {
  const status = {
    projectDir,
    timestamp: getCurrentTimestamp().display,
    directories: {},
    progress: {},
    hounds: {},
    facts: {},
    decisions: {},
    tokenEstimate: 0
  };

  // 检查目录结构
  status.directories = {
    masterPlan: fs.existsSync(path.join(projectDir, '00_Master_Plan.md')),
    rawSources: fs.existsSync(path.join(projectDir, '01_Raw_Sources')),
    extractedFacts: fs.existsSync(path.join(projectDir, '02_Extracted_Facts')),
    drafts: fs.existsSync(path.join(projectDir, '03_Drafts')),
    finalReport: fs.existsSync(path.join(projectDir, '04_Final_Report.md')),
    sopChecklist: fs.existsSync(path.join(projectDir, 'SOP_Checklist.md')),
    decisionLog: fs.existsSync(path.join(projectDir, 'Decision_Log.md')),
    houndManifest: fs.existsSync(path.join(projectDir, 'hound_manifest.json'))
  };

  // 读取主大纲进度
  const masterPlan = readMasterPlan(projectDir);
  if (masterPlan) {
    const phases = ['Planning', 'Hunting', 'Drafting', 'Reviewing', 'Finalizing'];
    phases.forEach(phase => {
      const phaseRegex = new RegExp(`## ${phase}[^\\n]*\\n- \\[[✅🔵⚪🔴])`);
      const match = phaseRegex.exec(masterPlan);
      if (match) {
        status.progress[phase] = match[1];
      }
    });
  }

  // 读取猎犬状态
  const houndManifest = getHoundManifest(projectDir);
  if (houndManifest) {
    status.hounds = {
      total: houndManifest.stats.total,
      completed: houndManifest.stats.completed,
      pending: houndManifest.stats.pending,
      failed: houndManifest.stats.failed,
      list: houndManifest.hounds
    };

    // 估算Token消耗（基于猎犬数量和任务数）
    status.tokenEstimate = houndManifest.stats.total * 500; // 每个猎犬任务约500 tokens
  }

  // 读取事实覆盖度
  const factsDir = path.join(projectDir, '02_Extracted_Facts');
  if (fs.existsSync(factsDir)) {
    const files = fs.readdirSync(factsDir);
    status.facts = {
      total: files.length,
      quality: 'unknown'
    };

    // 估算平均质量
    if (houndManifest) {
      const completedHounds = houndManifest.hounds.filter(h => h.status === 'completed');
      if (completedHounds.length > 0) {
        const avgQuality = completedHounds.reduce((sum, h) => {
          const houndManifest = getHoundManifest(projectDir);
          const hound = houndManifest.hounds.find(hound => hound.houndId === h.houndId);
          return sum + (hound?.qualityScore || 0);
        }, 0) / completedHounds.length;

        status.facts.quality = avgQuality >= 0.8 ? 'excellent' : avgQuality >= 0.5 ? 'good' : 'needs_work';
      }
    }
  }

  // 读取决策数量
  const decisionLogPath = path.join(projectDir, 'Decision_Log.md');
  if (fs.existsSync(decisionLogPath)) {
    const decisionLog = fs.readFileSync(decisionLogPath, 'utf8');
    const decisionMatches = decisionLog.match(/^### 决策记录/gm);
    status.decisions.count = decisionMatches ? decisionMatches.length : 0;
  }

  return status;
}

// ===== 导出所有核心函数 =====

export {
  initProject,
  writeMasterPlan,
  readMasterPlan,
  updateMasterPlanProgress,
  saveRawSource,
  listRawSources,
  getRawSource,
  saveExtractedFact,
  listExtractedFacts,
  getExtractedFactsBySubTask,
  assessFactsCoverage,
  registerHound,
  updateHoundStatus,
  getHoundManifest,
  getPendingHounds,
  getCompletedHounds,
  saveDraft,
  listDrafts,
  readAllDrafts,
  saveFinalReport,
  readFinalReport,
  getProjectStatus
};
