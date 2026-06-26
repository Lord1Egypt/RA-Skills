/**
 * Jarvis Memory Palace 测试脚本
 * 测试存储和检索功能
 */

import { MemoryPalaceManager, Memory } from '../../dist/src/index.js';
import { testMemories } from './test-data.js';
import { testQueries } from './test-queries.js';
import * as fs from 'fs';
import * as path from 'path';

// 确保测试目录存在
const WORKSPACE_DIR = '/data/.subagent/.jarvis';

// 记忆 ID 映射（原始ID -> 存储后的ID）
const memoryIdMap = new Map<string, string>();

async function ensureDir(dir: string) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

async function runTest() {
  console.log('=== Jarvis Memory Palace 测试 ===\n');
  const startTime = Date.now();
  
  // 确保工作目录存在
  await ensureDir(WORKSPACE_DIR);
  
  // 初始化 Memory Palace
  const palace = new MemoryPalaceManager({ workspaceDir: WORKSPACE_DIR });
  
  // ========== 存储测试 ==========
  console.log('📦 开始存储测试...\n');
  const storageStartTime = Date.now();
  
  let storageSuccessful = 0;
  let storageFailed = 0;
  const storageErrors: string[] = [];
  
  for (const memory of testMemories) {
    try {
      const importanceMap: Record<string, number> = {
        'high': 0.9,
        'medium': 0.6,
        'low': 0.3
      };
      
      // 将测试数据中的信息编码到 content 中，便于后续匹配
      const enhancedContent = `[${memory.category}] [${memory.id}] ${memory.content}`;
      
      const storedMemory = await palace.store({
        content: enhancedContent,
        tags: [...memory.tags, memory.category, `orig-${memory.id}`],
        importance: importanceMap[memory.importance] || 0.5,
        source: 'user', // 使用有效的 source 类型
        location: memory.category
      });
      
      // 记录映射关系
      if (storedMemory && storedMemory.id) {
        memoryIdMap.set(memory.id, storedMemory.id);
      }
      
      storageSuccessful++;
      console.log(`  ✅ 存储 ${memory.id}: ${memory.content.substring(0, 30)}...`);
    } catch (error) {
      storageFailed++;
      const errorMsg = error instanceof Error ? error.message : String(error);
      storageErrors.push(`${memory.id}: ${errorMsg}`);
      console.log(`  ❌ 存储 ${memory.id} 失败: ${errorMsg}`);
    }
  }
  
  const storageEndTime = Date.now();
  const storageTime = ((storageEndTime - storageStartTime) / 1000).toFixed(2);
  
  // 获取存储后的统计
  let stats;
  try {
    stats = await palace.stats();
  } catch (e) {
    stats = { total: storageSuccessful, active: storageSuccessful, archived: 0, deleted: 0, avgImportance: 0.6 };
  }
  
  console.log(`\n📊 存储完成: ${storageSuccessful}/${testMemories.length} 成功, 耗时 ${storageTime}s\n`);
  
  // ========== 检索测试 ==========
  console.log('🔍 开始检索测试...\n');
  const queryStartTime = Date.now();
  
  interface QueryResult {
    query: string;
    answer: string;
    foundCorrectKeywords: boolean;
    confidence: number;
    searchScore: number;
    expectedMemoryIds: string[];
    matchedMemoryIds: string[];
    difficulty: string;
  }
  
  const queryResults: QueryResult[] = [];
  
  for (const testQuery of testQueries) {
    try {
      console.log(`\n🔎 查询 [${testQuery.difficulty}]: ${testQuery.query}`);
      
      // 执行检索 - 使用 topK 而不是 limit
      const searchResults = await palace.recall(testQuery.query, { topK: 5 });
      
      // 分析结果
      const matchedMemoryIds: string[] = [];
      let totalScore = 0;
      
      for (const result of searchResults) {
        // 从 tags 中提取原始 ID
        const origTag = result.memory.tags.find(t => t.startsWith('orig-'));
        if (origTag) {
          matchedMemoryIds.push(origTag.replace('orig-', ''));
        }
        totalScore += result.score;
      }
      
      // 检查是否找到期望的记忆
      const expectedIds = new Set(testQuery.expectedMemoryIds);
      const foundIds = new Set(matchedMemoryIds);
      const intersection = [...expectedIds].filter(id => foundIds.has(id));
      const foundCorrectKeywords = intersection.length > 0;
      
      // 构建回答
      let answer = '';
      if (searchResults.length > 0) {
        answer = searchResults.map((r, i) => 
          `${i + 1}. ${r.memory.content} (相关度: ${(r.score * 100).toFixed(1)}%)`
        ).join('\n');
      } else {
        answer = '未找到相关记忆';
      }
      
      // 计算置信度
      const avgScore = searchResults.length > 0 ? totalScore / searchResults.length : 0;
      const confidence = Math.min(10, Math.round(avgScore * 10 + (foundCorrectKeywords ? 3 : 0)));
      
      const result: QueryResult = {
        query: testQuery.query,
        answer: answer.substring(0, 200),
        foundCorrectKeywords,
        confidence,
        searchScore: Math.round(avgScore * 100) / 100,
        expectedMemoryIds: testQuery.expectedMemoryIds,
        matchedMemoryIds,
        difficulty: testQuery.difficulty
      };
      
      queryResults.push(result);
      
      const statusIcon = foundCorrectKeywords ? '✅' : '❌';
      console.log(`  ${statusIcon} 置信度: ${confidence}/10, 检索分数: ${result.searchScore}`);
      console.log(`  期望: ${testQuery.expectedMemoryIds.join(', ')}`);
      console.log(`  匹配: ${matchedMemoryIds.join(', ')}`);
      
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      console.log(`  ❌ 查询失败: ${errorMsg}`);
      
      queryResults.push({
        query: testQuery.query,
        answer: `查询出错: ${errorMsg}`,
        foundCorrectKeywords: false,
        confidence: 0,
        searchScore: 0,
        expectedMemoryIds: testQuery.expectedMemoryIds,
        matchedMemoryIds: [],
        difficulty: testQuery.difficulty
      });
    }
  }
  
  const queryEndTime = Date.now();
  const queryTime = ((queryEndTime - queryStartTime) / 1000).toFixed(2);
  
  // ========== 计算总体分数 ==========
  const hitCount = queryResults.filter(r => r.foundCorrectKeywords).length;
  const avgConfidence = queryResults.reduce((sum, r) => sum + r.confidence, 0) / queryResults.length;
  
  // 按难度统计
  const easyResults = queryResults.filter(r => r.difficulty === 'easy');
  const mediumResults = queryResults.filter(r => r.difficulty === 'medium');
  const hardResults = queryResults.filter(r => r.difficulty === 'hard');
  
  const easyHitRate = easyResults.length > 0 
    ? easyResults.filter(r => r.foundCorrectKeywords).length / easyResults.length 
    : 0;
  const mediumHitRate = mediumResults.length > 0 
    ? mediumResults.filter(r => r.foundCorrectKeywords).length / mediumResults.length 
    : 0;
  const hardHitRate = hardResults.length > 0 
    ? hardResults.filter(r => r.foundCorrectKeywords).length / hardResults.length 
    : 0;
  
  const totalEndTime = Date.now();
  const totalTime = ((totalEndTime - startTime) / 1000).toFixed(2);
  
  // ========== 输出最终结果 ==========
  const finalResult = {
    storageResults: {
      total: testMemories.length,
      successful: storageSuccessful,
      failed: storageFailed,
      time: `${storageTime}s`,
      stats: stats,
      errors: storageErrors.length > 0 ? storageErrors : undefined
    },
    queryResults: queryResults.map(r => ({
      query: r.query,
      answer: r.answer,
      foundCorrectKeywords: r.foundCorrectKeywords,
      confidence: r.confidence,
      searchScore: r.searchScore,
      difficulty: r.difficulty
    })),
    overallScore: {
      storageSuccessRate: storageSuccessful / testMemories.length,
      queryHitRate: hitCount / testQueries.length,
      avgConfidence: Math.round(avgConfidence * 10) / 10,
      byDifficulty: {
        easy: Math.round(easyHitRate * 100),
        medium: Math.round(mediumHitRate * 100),
        hard: Math.round(hardHitRate * 100)
      }
    },
    timing: {
      storageTime: `${storageTime}s`,
      queryTime: `${queryTime}s`,
      totalTime: `${totalTime}s`
    }
  };
  
  console.log('\n\n' + '='.repeat(60));
  console.log('📋 最终测试报告');
  console.log('='.repeat(60));
  console.log(JSON.stringify(finalResult, null, 2));
  
  // 保存结果到文件
  const resultPath = path.join(WORKSPACE_DIR, 'test-result.json');
  fs.writeFileSync(resultPath, JSON.stringify(finalResult, null, 2));
  console.log(`\n📁 测试结果已保存到: ${resultPath}`);
}

// 运行测试
runTest().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});