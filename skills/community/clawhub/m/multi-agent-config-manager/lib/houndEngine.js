/**
 * 猎犬引擎 - Hound Engine v1.0
 * 
 * 实现"猎犬与蜂巢"框架中的猎犬动态探索层
 * 猎犬特点：自由探索能力，采用ReAct循环（思考→行动→观察→反思），
 * 能在互联网荒野中顺藤摸瓜，动态调整搜索策略
 */

import fs from 'fs';
import path from 'path';
import { selectModel, buildModelPool } from './modelSelector.js';

// ===================== 猎犬错误类型 =====================

export const HoundErrorType = {
  TIMEOUT: 'timeout',
  EMPTY_RESULT: 'empty_result',
  NO_SOURCES: 'no_sources',
  LOW_QUALITY: 'low_quality',
  FILE_MISSING: 'file_missing',
  EXECUTION_FAILED: 'execution_failed',
  UNKNOWN: 'unknown'
};

// ===================== 猎犬任务配置生成器 =====================

/**
 * 生成猎犬的完整任务配置
 * @param {string} subTask - 子任务描述
 * @param {number} maxSteps - 最大步数限制
 * @param {number} timeLimit - 时间限制（分钟）
 * @returns {Object} 猎犬任务配置
 */
export function buildHoundTask(subTask, maxSteps = 20, timeLimit = 30) {
  return {
    subTask,
    maxSteps,
    timeLimit, // 分钟
    createdAt: new Date().toISOString(),
    type: 'hound_exploration',
    description: `猎犬探索任务：${subTask}`,
    requirements: {
      minSources: 3,
      minFacts: 5,
      sourceReliability: ['official', 'authoritative', 'trusted']
    }
  };
}

// ===================== 猎犬提示词生成器 =====================

/**
 * 生成猎犬的系统提示词
 * @param {string} subTask - 子任务描述
 * @param {Object} houndConfig - 猎犬配置
 * @returns {string} 猎犬提示词
 */
export function buildHoundPrompt(subTask, houndConfig) {
  const { maxSteps = 20, timeLimit = 30 } = houndConfig;
  
  // 生成安全的任务ID（用于文件名）
  const safeTaskId = subTask
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fa5]+/g, '_')
    .substring(0, 50);
  
  const outputFile = `Sub_Task_${safeTaskId}.md`;
  
  return `# 🐕 猎犬模式：不知疲倦的调查记者

## 🎯 你的身份
你是一位专业的调查记者，拥有强大的互联网搜索能力。你的职责是深入挖掘信息，找到核心数据和可靠信源。

## 🎯 核心任务
**回答以下问题：**
> ${subTask}

## 🔄 ReAct循环指令（必须遵循）
每执行一步，都必须按以下循环进行：

1. **思考（Think）**：分析当前信息，决定下一步搜索策略
2. **行动（Action）**：执行搜索或数据提取
3. **观察（Observe）**：分析搜索结果，提取关键信息
4. **反思（Reflect）**：评估找到的信息质量，决定下一步

## ⚠️ 护栏限制
- **最大步数**：${maxSteps} 步（每步 = 一轮搜索→提取→评估）
- **时间限制**：${timeLimit} 分钟
- **自我评估**：每5步问自己"数据足够了吗？"，不够就换搜索词
- **禁止套娃**：你**不允许** spawn 任何子代理！所有探索必须由你自己完成

## 📝 强制写日记要求
**每次发现有用数据必须立即写入本地文件！**
- 写入路径：当前目录的 \`02_Extracted_Facts/${outputFile}\`
- 格式：Markdown，包含URL引用和数据来源标注
- 内容：实时记录发现，不要等到最后才写

## 🧠 动态调整策略
1. **关键词优化**：如果搜索没有结果，尝试同义词、相关概念
2. **可信度优先**：优先查找官方、权威媒体、学术期刊
3. **交叉验证**：重要数据至少需要2个独立来源确认
4. **深度挖掘**：发现重要线索后，深入挖掘相关文档、报告、数据集

## 📊 数据质量标准
按照以下标准评估信息来源：
- **一级（官方）**：政府网站、官方统计、国际组织（联合国、世界银行等）
- **二级（权威媒体）**：主流媒体、学术期刊、权威研究报告
- **三级（自媒体/论坛）**：个人博客、社交媒体、用户生成内容（需谨慎对待）

## 📄 最终输出格式
**不要写长篇报告！** 使用结构化事实卡片格式：

\`\`\`markdown
# ${subTask} 调查结果

## 核心发现
- 发现1: [具体数据] — 来源: [URL]
- 发现2: [具体数据] — 来源: [URL]

## 数据质量评估
- 信息充分度: 高/中/低
- 来源可靠性: 一级(官方)/二级(权威媒体)/三级(自媒体)
- 缺失信息: [哪些关键数据没找到]

## 推荐后续探索
- [如果有值得继续挖掘的线索]
\`\`\`

## 🏁 完成任务标志
当你认为自己已经：
1. 找到了足够回答问题的核心数据
2. 验证了信息来源的可信度
3. 整理成上述结构化格式写入文件

请输出：**HOUND_MISSION_COMPLETE**

## ⚡ 立即开始
现在开始执行你的调查任务。记住：实时写入发现，遵循ReAct循环，保持批判性思维！`;
}

// ===================== 猎犬spawn参数构建器 =====================

/**
 * 构建 sessions_spawn 调用参数
 * @param {Object} houndConfig - 猎犬配置
 * @param {Object} directories - 目录结构
 * @returns {Object} spawn参数
 */
export function buildHoundSpawnParams(houndConfig, directories) {
  const { subTask, maxSteps = 20, timeLimit = 30 } = houndConfig;
  
  // 生成猎犬提示词
  const prompt = buildHoundPrompt(subTask, houndConfig);
  
  // 选择适合搜索的模型
  const modelResult = selectModel('Research_Analyst', {
    complexity: 'complex',
    taskType: 'research',
    allowFree: false // 搜索任务通常需要较强能力
  });
  
  // 确保选择有效模型
  let modelId = modelResult.model || 'deepseek/deepseek-chat';
  if (modelResult.error) {
    // 降级方案
    const modelPool = buildModelPool();
    const searchModels = modelPool.all.filter(m => 
      !m.id.includes('code') && 
      !m.tier?.includes('free')
    );
    if (searchModels.length > 0) {
      modelId = searchModels[0].id;
    }
  }
  
  // 构建挂载目录
  const mountDirs = {
    rawSources: directories?.rawSources || path.join(process.cwd(), '01_Raw_Sources'),
    extractedFacts: directories?.extractedFacts || path.join(process.cwd(), '02_Extracted_Facts')
  };
  
  // 确保目录存在
  fs.mkdirSync(mountDirs.rawSources, { recursive: true });
  fs.mkdirSync(mountDirs.extractedFacts, { recursive: true });
  
  return {
    runtime: 'subagent',
    mode: 'run',
    task: prompt,
    label: `hound-${subTask.substring(0, 30).replace(/\s+/g, '-')}`,
    model: modelId,
    timeoutSeconds: timeLimit * 60, // 转换为秒
    cwd: mountDirs.extractedFacts, // 设置工作目录到提取事实目录
    env: {
      HOUND_TASK: subTask,
      HOUND_MAX_STEPS: maxSteps.toString(),
      OUTPUT_DIR: mountDirs.extractedFacts,
      RAW_SOURCES_DIR: mountDirs.rawSources
    },
    onError: 'retry',
    retryCount: 1
  };
}

// ===================== 猎犬结果评估器 =====================

/**
 * 评估猎犬带回的证据质量
 * @param {string} resultFile - 结果文件路径
 * @param {string} subTask - 原始子任务
 * @returns {Object} 评估结果
 */
export function evaluateHoundResult(resultFile, subTask) {
  try {
    // 1. 检查文件存在性
    if (!fs.existsSync(resultFile)) {
      return {
        success: false,
        score: 0,
        error: HoundErrorType.FILE_MISSING,
        diagnosis: `文件不存在: ${resultFile}`,
        suggestions: ['检查输出目录是否正确', '确认猎犬是否成功执行']
      };
    }
    
    // 2. 检查文件大小
    const stats = fs.statSync(resultFile);
    if (stats.size === 0) {
      return {
        success: false,
        score: 0,
        error: HoundErrorType.EMPTY_RESULT,
        diagnosis: '文件为空',
        suggestions: ['可能是搜索未找到结果', '可能需要调整搜索策略']
      };
    }
    
    // 3. 读取文件内容
    const content = fs.readFileSync(resultFile, 'utf-8');
    
    // 4. 提取核心指标
    const metrics = extractMetrics(content, subTask);
    
    // 5. 计算综合评分 (0-1)
    const score = calculateHoundScore(metrics);
    
    return {
      success: score >= 0.6, // 60分及格线
      score,
      metrics,
      fileInfo: {
        path: resultFile,
        size: stats.size,
        lines: content.split('\n').length
      },
      assessment: getQualityAssessment(metrics),
      suggestions: getImprovementSuggestions(metrics, score)
    };
    
  } catch (error) {
    return {
      success: false,
      score: 0,
      error: HoundErrorType.EXECUTION_FAILED,
      diagnosis: `评估过程中出错: ${error.message}`,
      suggestions: ['检查文件权限', '验证文件编码格式']
    };
  }
}

/**
 * 从内容中提取指标
 */
function extractMetrics(content, subTask) {
  const metrics = {
    hasTaskTitle: false,
    hasCoreFindings: false,
    hasQualityAssessment: false,
    hasFollowUp: false,
    sourceCount: 0,
    factCount: 0,
    urlCount: 0,
    sourceTypes: [],
    contentLength: content.length
  };
  
  // 检查结构化元素
  const lines = content.split('\n');
  let inCoreFindings = false;
  let inQualityAssessment = false;
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    // 检查任务标题
    if (trimmed.startsWith('#') && trimmed.includes(subTask.substring(0, 20))) {
      metrics.hasTaskTitle = true;
    }
    
    // 检查核心发现部分
    if (trimmed.startsWith('##') && trimmed.includes('核心发现')) {
      inCoreFindings = true;
      metrics.hasCoreFindings = true;
      continue;
    }
    
    // 检查质量评估部分
    if (trimmed.startsWith('##') && (trimmed.includes('质量评估') || trimmed.includes('数据质量'))) {
      inQualityAssessment = true;
      metrics.hasQualityAssessment = true;
      inCoreFindings = false;
      continue;
    }
    
    // 检查后续探索部分
    if (trimmed.startsWith('##') && trimmed.includes('后续探索')) {
      metrics.hasFollowUp = true;
      inQualityAssessment = false;
      continue;
    }
    
    // 在核心发现中计数
    if (inCoreFindings && trimmed.startsWith('-')) {
      metrics.factCount++;
      
      // 提取URL
      const urlMatch = trimmed.match(/https?:\/\/[^\s)]+/);
      if (urlMatch) {
        metrics.urlCount++;
        metrics.sourceCount++;
      }
      
      // 识别来源类型
      if (trimmed.includes('官方')) {
        metrics.sourceTypes.push('official');
      } else if (trimmed.includes('权威媒体')) {
        metrics.sourceTypes.push('authoritative');
      } else if (trimmed.includes('自媒体')) {
        metrics.sourceTypes.push('user_generated');
      }
    }
    
    // 在质量评估中识别
    if (inQualityAssessment && trimmed.includes(':')) {
      if (trimmed.includes('信息充分度')) {
        metrics.adequacy = trimmed.split(':')[1]?.trim() || '未知';
      }
      if (trimmed.includes('来源可靠性')) {
        metrics.reliability = trimmed.split(':')[1]?.trim() || '未知';
      }
    }
  }
  
  return metrics;
}

/**
 * 计算猎犬评分
 */
function calculateHoundScore(metrics) {
  let score = 0;
  const maxScore = 100;
  
  // 基础结构分 (30分)
  if (metrics.hasTaskTitle) score += 10;
  if (metrics.hasCoreFindings) score += 10;
  if (metrics.hasQualityAssessment) score += 10;
  
  // 内容质量分 (50分)
  const factScore = Math.min(metrics.factCount * 5, 20); // 每个事实5分，最多20分
  score += factScore;
  
  const sourceScore = Math.min(metrics.sourceCount * 6, 18); // 每个来源6分，最多18分
  score += sourceScore;
  
  // URL有效性分 (12分)
  const urlRatio = metrics.factCount > 0 ? metrics.urlCount / metrics.factCount : 0;
  score += Math.min(Math.floor(urlRatio * 12), 12);
  
  // 转换到 0-1 范围
  return score / maxScore;
}

/**
 * 获取质量评估
 */
function getQualityAssessment(metrics) {
  if (metrics.score >= 0.8) {
    return '优秀：信息充分，来源可靠，结构完整';
  } else if (metrics.score >= 0.6) {
    return '良好：基本满足要求，有改进空间';
  } else if (metrics.score >= 0.4) {
    return '一般：信息不足或来源有限';
  } else {
    return '较差：需要大幅改进';
  }
}

/**
 * 获取改进建议
 */
function getImprovementSuggestions(metrics, score) {
  const suggestions = [];
  
  if (!metrics.hasTaskTitle) {
    suggestions.push('缺少明确的任务标题');
  }
  
  if (!metrics.hasCoreFindings) {
    suggestions.push('缺少"核心发现"章节');
  }
  
  if (!metrics.hasQualityAssessment) {
    suggestions.push('缺少"数据质量评估"章节');
  }
  
  if (metrics.factCount < 3) {
    suggestions.push(`事实数量不足（当前: ${metrics.factCount}，建议至少: 3）`);
  }
  
  if (metrics.sourceCount < 2) {
    suggestions.push(`信息来源不足（当前: ${metrics.sourceCount}，建议至少: 2）`);
  }
  
  const urlRatio = metrics.factCount > 0 ? metrics.urlCount / metrics.factCount : 0;
  if (urlRatio < 0.7) {
    suggestions.push('多数事实缺少来源引用（建议为每个事实提供URL）');
  }
  
  if (score < 0.6) {
    suggestions.push('总体评分较低，建议重新执行任务或调整搜索策略');
  }
  
  return suggestions;
}

// ===================== 猎犬重试策略 =====================

/**
 * 猎犬失败时生成重试配置
 * @param {Object} failedHound - 失败的猎犬配置
 * @param {Object} diagnosis - 诊断结果
 * @returns {Object} 重试配置
 */
export function buildHoundRetry(failedHound, diagnosis) {
  const { originalConfig, errorType, details } = diagnosis;
  
  const retryConfig = { ...originalConfig };
  
  // 根据错误类型调整策略
  switch (errorType) {
    case HoundErrorType.EMPTY_RESULT:
    case HoundErrorType.NO_SOURCES:
      // 空结果：调整搜索词，减少步数
      retryConfig.maxSteps = Math.max(5, Math.floor((retryConfig.maxSteps || 20) * 0.7));
      retryConfig.enhancedKeywords = true;
      retryConfig.searchStrategy = 'broaden_scope';
      break;
      
    case HoundErrorType.TIMEOUT:
      // 超时：减少步数，增加时间
      retryConfig.maxSteps = Math.max(10, Math.floor((retryConfig.maxSteps || 20) * 0.8));
      retryConfig.timeLimit = Math.min(45, (retryConfig.timeLimit || 30) * 1.3);
      break;
      
    case HoundErrorType.LOW_QUALITY:
      // 低质量：切换模型，增强提示
      retryConfig.switchModel = true;
      retryConfig.enhancedPrompt = true;
      retryConfig.minQualityThreshold = 'medium';
      break;
      
    case HoundErrorType.FILE_MISSING:
      // 文件缺失：确保目录存在，减少步数
      retryConfig.ensureDirectories = true;
      retryConfig.maxSteps = Math.max(10, Math.floor((retryConfig.maxSteps || 20) * 0.8));
      break;
      
    default:
      // 默认：保守重试
      retryConfig.maxSteps = Math.max(10, Math.floor((retryConfig.maxSteps || 20) * 0.8));
      retryConfig.timeLimit = Math.min(40, (retryConfig.timeLimit || 30) * 1.2);
      break;
  }
  
  // 添加重试标记
  retryConfig.retryCount = (originalConfig.retryCount || 0) + 1;
  retryConfig.lastError = errorType;
  retryConfig.retryReason = details;
  
  return retryConfig;
}

/**
 * 生成诊断结果
 * @param {Object} houndResult - 猎犬结果
 * @returns {Object} 诊断结果
 */
export function diagnoseHoundFailure(houndResult) {
  const { error, metrics, score, diagnosis: existingDiagnosis } = houndResult;
  
  let errorType = error || HoundErrorType.UNKNOWN;
  let details = existingDiagnosis || '未知错误';
  
  // 根据指标进一步诊断
  if (!error && metrics) {
    if (metrics.factCount === 0) {
      errorType = HoundErrorType.EMPTY_RESULT;
      details = '未找到任何事实';
    } else if (metrics.sourceCount < 2) {
      errorType = HoundErrorType.NO_SOURCES;
      details = `来源不足（仅${metrics.sourceCount}个）`;
    } else if (score < 0.4) {
      errorType = HoundErrorType.LOW_QUALITY;
      details = `质量评分过低（${(score * 100).toFixed(1)}分）`;
    }
  }
  
  return {
    errorType,
    details,
    timestamp: new Date().toISOString(),
    metrics,
    recommendations: getRetryRecommendations(errorType, metrics)
  };
}

/**
 * 获取重试建议
 */
function getRetryRecommendations(errorType, metrics) {
  const recommendations = [];
  
  switch (errorType) {
    case HoundErrorType.EMPTY_RESULT:
      recommendations.push(
        '扩展搜索关键词范围',
        '尝试同义词和相关术语',
        '使用更广泛的搜索策略'
      );
      break;
      
    case HoundErrorType.NO_SOURCES:
      recommendations.push(
        '优先搜索权威网站（政府、学术期刊）',
        '使用高级搜索操作符',
        '尝试不同搜索引擎'
      );
      break;
      
    case HoundErrorType.LOW_QUALITY:
      recommendations.push(
        '增加事实数量要求',
        '提高来源可信度标准',
        '添加交叉验证步骤'
      );
      break;
      
    case HoundErrorType.TIMEOUT:
      recommendations.push(
        '减少最大步数',
        '优化搜索策略减少无效尝试',
        '设置更明确的搜索目标'
      );
      break;
      
    default:
      recommendations.push(
        '检查网络连接',
        '验证模型可用性',
        '简化任务目标'
      );
  }
  
  return recommendations;
}

// ===================== 辅助函数 =====================

/**
 * 生成猎犬工作的标准目录结构
 * @param {string} baseDir - 基础目录
 * @returns {Object} 目录结构
 */
export function createHoundDirectories(baseDir) {
  const directories = {
    rawSources: path.join(baseDir, '01_Raw_Sources'),
    extractedFacts: path.join(baseDir, '02_Extracted_Facts'),
    logs: path.join(baseDir, '03_Hound_Logs'),
    archives: path.join(baseDir, '04_Archives')
  };
  
  // 创建所有目录
  Object.values(directories).forEach(dir => {
    fs.mkdirSync(dir, { recursive: true });
  });
  
  return directories;
}

/**
 * 生成猎犬工作报告摘要
 * @param {Array} houndResults - 多个猎犬结果
 * @returns {Object} 报告摘要
 */
export function generateHoundReport(houndResults) {
  const total = houndResults.length;
  const successful = houndResults.filter(r => r.success).length;
  const avgScore = houndResults.reduce((sum, r) => sum + (r.score || 0), 0) / total;
  
  const metrics = {
    total,
    successful,
    successRate: total > 0 ? (successful / total) : 0,
    averageScore: avgScore,
    bestScore: Math.max(...houndResults.map(r => r.score || 0)),
    worstScore: Math.min(...houndResults.map(r => r.score || 0)),
    totalFacts: houndResults.reduce((sum, r) => sum + (r.metrics?.factCount || 0), 0),
    totalSources: houndResults.reduce((sum, r) => sum + (r.metrics?.sourceCount || 0), 0)
  };
  
  // 错误分析
  const errorTypes = {};
  houndResults.forEach(r => {
    if (!r.success && r.error) {
      errorTypes[r.error] = (errorTypes[r.error] || 0) + 1;
    }
  });
  
  return {
    summary: metrics,
    errors: errorTypes,
    timestamp: new Date().toISOString(),
    recommendations: generateOverallRecommendations(metrics, errorTypes)
  };
}

/**
 * 生成整体建议
 */
function generateOverallRecommendations(metrics, errorTypes) {
  const recommendations = [];
  
  if (metrics.successRate < 0.7) {
    recommendations.push('猎犬成功率较低，建议重新设计任务分解');
  }
  
  if (metrics.averageScore < 0.6) {
    recommendations.push('平均质量评分较低，需要改进搜索策略');
  }
  
  if (errorTypes[HoundErrorType.EMPTY_RESULT] > metrics.total * 0.3) {
    recommendations.push('空结果比例过高，可能需要调整搜索关键词或任务范围');
  }
  
  if (errorTypes[HoundErrorType.TIMEOUT] > metrics.total * 0.2) {
    recommendations.push('超时比例较高，建议减少步数或增加时间限制');
  }
  
  if (recommendations.length === 0) {
    recommendations.push('猎犬工作表现良好，继续保持当前策略');
  }
  
  return recommendations;
}