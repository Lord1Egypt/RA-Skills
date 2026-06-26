/**
 * 猎犬引擎测试脚本
 */

import * as houndEngine from './lib/houndEngine.js';

console.log('=== 测试猎犬引擎 v1.0 ===\n');

// 测试1: 构建猎犬任务
console.log('测试1: 构建猎犬任务配置');
const subTask = '调查中国2024年新能源汽车市场增长率';
const houndTask = houndEngine.buildHoundTask(subTask, 15, 25);
console.log('任务配置:', JSON.stringify(houndTask, null, 2));
console.log('✓ 任务配置生成成功\n');

// 测试2: 生成猎犬提示词
console.log('测试2: 生成猎犬提示词');
const prompt = houndEngine.buildHoundPrompt(subTask, houndTask);
console.log('提示词长度:', prompt.length, '字符');
console.log('提示词片段（前500字符）:', prompt.substring(0, 500) + '...');
console.log('✓ 提示词生成成功\n');

// 测试3: 创建目录结构
console.log('测试3: 创建猎犬目录结构');
const tempDir = './test_hound_dirs';
const directories = houndEngine.createHoundDirectories(tempDir);
console.log('创建的目录:', directories);
console.log('✓ 目录结构创建成功\n');

// 测试4: 生成spawn参数
console.log('测试4: 生成猎犬spawn参数');
const spawnParams = houndEngine.buildHoundSpawnParams(houndTask, directories);
console.log('spawn参数键:', Object.keys(spawnParams));
console.log('模型:', spawnParams.model);
console.log('运行时:', spawnParams.runtime);
console.log('标签:', spawnParams.label);
console.log('✓ spawn参数生成成功\n');

// 测试5: 模拟结果评估
console.log('测试5: 模拟猎犬结果评估');

// 创建一个模拟结果文件
const mockResultContent = `# 调查中国2024年新能源汽车市场增长率 调查结果

## 核心发现
- 发现1: 2024年中国新能源汽车销量预计增长35% — 来源: https://www.caam.org.cn/2024-report
- 发现2: 电动汽车市场渗透率将达到40% — 来源: https://www.autoindustry.cn/ev-stats
- 发现3: 主要增长驱动为政策补贴和技术进步 — 来源: https://www.gov.cn/new-energy-policy

## 数据质量评估
- 信息充分度: 高
- 来源可靠性: 一级(官方)/二级(权威媒体)
- 缺失信息: 详细的季度增长数据和区域分布

## 推荐后续探索
- 各主要汽车厂商的具体销量数据
- 不同类型新能源汽车（纯电、插混、氢燃料）的细分增长
`;

const mockResultFile = `${directories.extractedFacts}/Sub_Task_新能源汽车市场增长率.md`;
import fs from 'fs';
fs.writeFileSync(mockResultFile, mockResultContent);

const evaluation = houndEngine.evaluateHoundResult(mockResultFile, subTask);
console.log('评估结果:', JSON.stringify(evaluation, null, 2));
console.log('✓ 结果评估成功\n');

// 测试6: 诊断和重试策略
console.log('测试6: 诊断失败和重试策略');

// 模拟一个失败结果
const failedResult = {
  success: false,
  score: 0.3,
  error: houndEngine.HoundErrorType.LOW_QUALITY,
  diagnosis: '质量评分过低（30分）',
  metrics: {
    factCount: 1,
    sourceCount: 1,
    hasTaskTitle: true,
    hasCoreFindings: true,
    hasQualityAssessment: false
  }
};

const diagnosis = houndEngine.diagnoseHoundFailure(failedResult);
console.log('诊断结果:', JSON.stringify(diagnosis, null, 2));

const retryConfig = houndEngine.buildHoundRetry(houndTask, {
  originalConfig: houndTask,
  errorType: diagnosis.errorType,
  details: diagnosis.details
});
console.log('重试配置:', JSON.stringify(retryConfig, null, 2));
console.log('✓ 诊断和重试策略成功\n');

// 测试7: 生成报告
console.log('测试7: 生成猎犬工作报告');

const results = [
  { success: true, score: 0.85, metrics: { factCount: 5, sourceCount: 4 } },
  { success: true, score: 0.72, metrics: { factCount: 3, sourceCount: 3 } },
  { success: false, score: 0.35, error: houndEngine.HoundErrorType.EMPTY_RESULT, metrics: { factCount: 0, sourceCount: 0 } },
  { success: false, score: 0.28, error: houndEngine.HoundErrorType.TIMEOUT, metrics: { factCount: 2, sourceCount: 1 } }
];

const report = houndEngine.generateHoundReport(results);
console.log('工作报告:', JSON.stringify(report, null, 2));

// 清理测试文件
console.log('\n=== 测试完成 ===');
console.log('清理测试目录...');
import { exec } from 'child_process';
exec(`rm -rf ${tempDir}`, (error) => {
  if (error) {
    console.log(`清理失败，请手动删除: ${tempDir}`);
  } else {
    console.log('测试目录已清理');
  }
});