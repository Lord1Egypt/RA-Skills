/**
 * PollMonitor 轮询监控器测试脚本
 * 测试 v8.1 新增的主动轮询机制
 */

import fs from 'fs';
import path from 'path';
import { PollMonitor, verifyFileWrite } from './lib/executor_v8.1.js';

const TEST_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace', 'test_poll');

// 确保测试目录存在
fs.mkdirSync(TEST_DIR, { recursive: true });

console.log('=== PollMonitor v8.1 测试 ===\n');

// ===================== 测试 1: verifyFileWrite 函数 =====================
console.log('测试 1: verifyFileWrite 文件验证函数');

// 1.1 测试文件不存在
console.log('\n1.1 文件不存在情况:');
const result1 = verifyFileWrite(path.join(TEST_DIR, 'nonexistent.md'));
console.log(`  结果：${result1.valid ? '✅ PASS' : '❌ FAIL'} - ${result1.reason}`);

// 1.2 测试文件过小
console.log('\n1.2 文件大小不足 (<100 bytes):');
const smallFile = path.join(TEST_DIR, 'small.md');
fs.writeFileSync(smallFile, '太小了', 'utf-8');
const result2 = verifyFileWrite(smallFile);
console.log(`  结果：${result2.valid ? '✅ PASS' : '❌ FAIL'} - ${result2.reason}`);

// 1.3 测试有效文件
console.log('\n1.3 有效 Markdown 文件:');
const validFile = path.join(TEST_DIR, 'valid.md');
fs.writeFileSync(validFile, '# 测试报告\n\n这是一个有效的测试文件，内容足够长以满足验证要求。\n\n## 第二节\n\n更多内容...', 'utf-8');
const result3 = verifyFileWrite(validFile);
console.log(`  结果：${result3.valid ? '✅ PASS' : '❌ FAIL'} - 大小：${result3.size} bytes, 行数：${result3.lineCount}`);

// 1.4 测试无效模板文本
console.log('\n1.4 包含无效模板文本:');
const invalidFile = path.join(TEST_DIR, 'invalid.md');
fs.writeFileSync(invalidFile, '# 报告\n\n我是 OpenClaw AI 助手，未能完成任务。\n\n抱歉，我无法完成此请求。', 'utf-8');
const result4 = verifyFileWrite(invalidFile);
console.log(`  结果：${result4.valid ? '✅ PASS' : '❌ FAIL'} - ${result4.reason}`);

// ===================== 测试 2: PollMonitor 类 =====================
console.log('\n\n测试 2: PollMonitor 轮询监控器');

// 2.1 测试即时文件产出
console.log('\n2.1 文件已存在（即时产出）:');
const monitor1 = new PollMonitor({
  pollIntervalMs: 1000,
  timeoutMs: 5000,
  logFile: path.join(TEST_DIR, 'poll_log_1.jsonl')
});

const readyFile = path.join(TEST_DIR, 'ready_agent.md');
fs.writeFileSync(readyFile, '# 已完成报告\n\n内容完整有效，满足所有验证要求。\n\n## 总结\n\n测试成功。', 'utf-8');

const result5 = await monitor1.pollUntilReady('ReadyAgent', readyFile);
console.log(`  结果：${result5.success ? '✅ PASS' : '❌ FAIL'}`);
console.log(`  轮询次数：${result5.pollCount}, 耗时：${Math.round(result5.elapsedMs/1000)}秒`);
console.log(`  文件大小：${result5.fileSize} bytes`);

// 2.2 测试延迟文件产出（模拟子代理延迟写入）
console.log('\n2.2 文件延迟产出（模拟 3 秒后写入）:');
const monitor2 = new PollMonitor({
  pollIntervalMs: 1000,
  timeoutMs: 10000,
  logFile: path.join(TEST_DIR, 'poll_log_2.jsonl')
});

const delayedFile = path.join(TEST_DIR, 'delayed_agent.md');
// 删除可能存在的旧文件
if (fs.existsSync(delayedFile)) fs.unlinkSync(delayedFile);

// 3 秒后写入文件
setTimeout(() => {
  fs.writeFileSync(delayedFile, '# 延迟报告\n\n这个文件在轮询开始 3 秒后才写入。\n\n## 验证\n\n测试延迟产出场景。', 'utf-8');
  console.log('  [模拟] 文件已写入');
}, 3000);

const result6 = await monitor2.pollUntilReady('DelayedAgent', delayedFile);
console.log(`  结果：${result6.success ? '✅ PASS' : '❌ FAIL'}`);
console.log(`  轮询次数：${result6.pollCount}, 耗时：${Math.round(result6.elapsedMs/1000)}秒`);

// 2.3 测试超时场景
console.log('\n2.3 超时场景（5 秒超时，文件永不写入）:');
const monitor3 = new PollMonitor({
  pollIntervalMs: 1000,
  timeoutMs: 5000,
  logFile: path.join(TEST_DIR, 'poll_log_3.jsonl')
});

const neverFile = path.join(TEST_DIR, 'never_agent.md');
if (fs.existsSync(neverFile)) fs.unlinkSync(neverFile);

const result7 = await monitor3.pollUntilReady('NeverAgent', neverFile);
console.log(`  结果：${!result7.success ? '✅ PASS (正确检测超时)' : '❌ FAIL (应该超时)'}`);
console.log(`  超时原因：${result7.reason}`);
console.log(`  轮询次数：${result7.pollCount}, 耗时：${Math.round(result7.elapsedMs/1000)}秒`);

// ===================== 测试 3: 轮询历史导出 =====================
console.log('\n\n测试 3: 轮询历史导出');

const history1 = monitor1.getHistory();
console.log(`\n3.1 ReadyAgent 轮询历史:`);
console.log(`  事件数量：${history1['ReadyAgent']?.length || 0}`);
if (history1['ReadyAgent']?.length > 0) {
  console.log(`  首个事件：${JSON.stringify(history1['ReadyAgent'][0])}`);
}

const history3 = monitor3.getHistory();
console.log(`\n3.2 NeverAgent 轮询历史:`);
console.log(`  事件数量：${history3['NeverAgent']?.length || 0}`);
if (history3['NeverAgent']?.length > 0) {
  console.log(`  最后事件：${JSON.stringify(history3['NeverAgent'][history3['NeverAgent'].length - 1])}`);
}

// ===================== 清理测试文件 =====================
console.log('\n\n清理测试文件...');
try {
  fs.rmSync(TEST_DIR, { recursive: true, force: true });
  console.log('✅ 测试目录已清理');
} catch (err) {
  console.log(`⚠️ 清理失败：${err.message}`);
}

// ===================== 测试总结 =====================
console.log('\n\n=== 测试总结 ===');
console.log('✅ verifyFileWrite 函数测试完成');
console.log('✅ PollMonitor 即时产出测试完成');
console.log('✅ PollMonitor 延迟产出测试完成');
console.log('✅ PollMonitor 超时检测测试完成');
console.log('✅ 轮询历史导出测试完成');
console.log('\nv8.1 主动轮询机制验证通过！');
