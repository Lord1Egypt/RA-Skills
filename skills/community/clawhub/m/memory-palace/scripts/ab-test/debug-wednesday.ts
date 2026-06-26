/**
 * Debug Wednesday query - check why "技术分享会" memory is not ranked first
 */

import { MemoryPalaceManager } from '../../src/manager.js';
import { LocalVectorSearchProvider } from '../../src/background/vector-search.js';

async function debugWednesdayQuery() {
  const vectorSearch = new LocalVectorSearchProvider({
    host: '127.0.0.1',
    port: 8765,
    dbPath: '/data/agent-memory-palace/data/vectors-test.db',
    scriptPath: '/data/agent-memory-palace/scripts/vector-service.py',
  });
  
  const palace = new MemoryPalaceManager({
    workspaceDir: '/data/.subagent/.jarvis',
    vectorSearch,
  });
  
  const query = '如果明天是周三，我需要准备什么？';
  console.log(`Query: "${query}"\n`);
  
  // Get more results to see where the Wednesday memory is
  const results = await palace.recall(query, { topK: 10 });
  
  console.log('Top 10 results:');
  results.forEach((r, i) => {
    const hasWednesday = r.memory.content.includes('周三');
    const hasTechShare = r.memory.content.includes('技术分享');
    const hasPrepare = r.memory.content.includes('准备');
    
    console.log(`${i + 1}. Score: ${r.score.toFixed(3)} [周三:${hasWednesday ? '✅' : '❌'}] [技术分享:${hasTechShare ? '✅' : '❌'}] [准备:${hasPrepare ? '✅' : '❌'}]`);
    console.log(`   Content: "${r.memory.content.substring(0, 60)}..."`);
    console.log(`   Tags: ${r.memory.tags.join(', ')}`);
    console.log();
  });
  
  // Check if Wednesday memory exists
  console.log('\n=== Looking for Wednesday memory in storage ===');
  const allMemories = await palace.list({ limit: 100 });
  const wednesdayMemories = allMemories.filter(m => 
    m.content.includes('周三') || m.tags.includes('周三')
  );
  
  console.log(`Found ${wednesdayMemories.length} memories with '周三':`);
  wednesdayMemories.forEach(m => {
    console.log(`  - ${m.id}: "${m.content.substring(0, 60)}..."`);
  });
}

debugWednesdayQuery().catch(console.error);