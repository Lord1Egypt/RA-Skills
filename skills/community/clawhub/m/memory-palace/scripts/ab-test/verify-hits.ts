/**
 * Detailed Analysis of Previously Failed Queries
 */

import { MemoryPalaceManager } from '../../src/manager.js';
import { LocalVectorSearchProvider } from '../../src/background/vector-search.js';
import * as fs from 'fs/promises';
import * as path from 'path';

// Store memories and check specific queries in detail
async function detailedAnalysis() {
  const workspaceDir = '/data/.subagent/.jarvis';
  
  const vectorSearch = new LocalVectorSearchProvider({
    host: '127.0.0.1',
    port: 8765,
    dbPath: '/data/agent-memory-palace/data/vectors-test.db',
    scriptPath: '/data/agent-memory-palace/scripts/vector-service.py',
  });
  
  const palace = new MemoryPalaceManager({
    workspaceDir,
    vectorSearch,
  });
  
  // Get stats
  const stats = await palace.stats();
  console.log('Memory Palace Stats:', stats);
  
  // Detailed queries for previously failed cases
  const queries = [
    {
      name: 'Programming Language Preference',
      query: '我之前说过的编程语言偏好是什么？',
      expectedContent: 'TypeScript',
    },
    {
      name: 'Health and Exercise',
      query: '健康和运动相关的安排有什么？',
      expectedContent: '健身',
    },
    {
      name: 'Wednesday Preparation',
      query: '如果明天是周三，我需要准备什么？',
      expectedContent: '周三',
    },
  ];
  
  console.log('\n=== DETAILED ANALYSIS ===\n');
  
  for (const q of queries) {
    console.log(`\n--- ${q.name} ---`);
    console.log(`Query: "${q.query}"`);
    console.log(`Expected to find: "${q.expectedContent}"`);
    
    const results = await palace.recall(q.query, { topK: 3 });
    
    console.log(`\nTop 3 results:`);
    results.forEach((r, i) => {
      const contains = r.memory.content.includes(q.expectedContent);
      console.log(`${i + 1}. [${contains ? '✅' : '❌'}] Score: ${r.score.toFixed(3)}`);
      console.log(`   Content: "${r.memory.content.substring(0, 80)}..."`);
      console.log(`   Tags: ${r.memory.tags.join(', ')}`);
    });
  }
}

detailedAnalysis().catch(console.error);