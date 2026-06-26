/**
 * Multi-Hop Retrieval Benchmark
 * 
 * Tests specifically the multi-hop reasoning capability
 * Based on LOCOMO P6 (Multi-hop reasoning questions)
 */

import MemoryStore from '../storage/index.js';

// Multi-hop test data - multiple related facts that need to be connected
const sessions = [
  // Session 1: Initial mentions
  {
    id: 's1',
    timestamp: '2023-05-07T10:00:00Z',
    memories: [
      { content: 'Caroline went to the LGBTQ support group. She found it very supportive and made new friends.', type: 'episodic' },
      { content: 'Caroline works at a tech startup as a product manager.', type: 'semantic' },
    ]
  },
  // Session 2: Job discussion (after support group)
  {
    id: 's2',
    timestamp: '2023-05-10T14:00:00Z',
    memories: [
      { content: 'Caroline discussed her job situation. She mentioned feeling burned out and considering a career change.', type: 'episodic' },
      { content: 'Caroline has been at her current job for 3 years.', type: 'semantic' },
    ]
  },
  // Session 3: New project (later)
  {
    id: 's3',
    timestamp: '2023-05-15T09:00:00Z',
    memories: [
      { content: 'Caroline talked about her new project at work. She seemed excited about the challenge.', type: 'episodic' },
      { content: 'The project involves redesigning the company website.', type: 'semantic' },
    ]
  },
  // Session 4: David mention
  {
    id: 's4',
    timestamp: '2023-05-20T11:00:00Z',
    memories: [
      { content: 'David mentioned Caroline in a meeting. He said she was doing great work on the website project.', type: 'episodic' },
    ]
  },
  // Session 5: Project deadline
  {
    id: 's5',
    timestamp: '2023-05-25T15:00:00Z',
    memories: [
      { content: 'The website project deadline was moved to June 1st. Caroline will need to work extra hours.', type: 'episodic' },
    ]
  },
];

// Multi-hop questions
const questions = [
  {
    id: 'mh1',
    query: 'What did Caroline say about her job after she went to the LGBTQ support group?',
    expectedKeywords: ['burned out', 'career change', 'burned', 'considering'],
    type: 'temporal-multi-hop',
    difficulty: 'hard'
  },
  {
    id: 'mh2',
    query: 'How does Caroline feel about her work now compared to when she was burned out?',
    expectedKeywords: ['excited', 'project', 'challenge', 'great work'],
    type: 'temporal-evolution',
    difficulty: 'hard'
  },
  {
    id: 'mh3',
    query: 'What project is Caroline working on and who praised her work?',
    expectedKeywords: ['website', 'David', 'project', 'redesign'],
    type: 'connection',
    difficulty: 'medium'
  },
  {
    id: 'mh4',
    query: 'When does the website project need to be completed?',
    expectedKeywords: ['June 1st', 'June', 'deadline'],
    type: 'temporal',
    difficulty: 'easy'
  },
  {
    id: 'mh5',
    query: 'What is Caroline\'s role and how long has she been there?',
    expectedKeywords: ['product manager', '3 years', 'startup'],
    type: 'factual',
    difficulty: 'easy'
  },
];

async function run() {
  console.log('🔍 Multi-Hop Retrieval Benchmark\n');
  console.log('=' .repeat(60));
  
  const store = new MemoryStore('/tmp/multihop-benchmark.db');
  
  // Seed memories
  console.log('\n📝 Seeding memories...');
  for (const session of sessions) {
    for (const mem of session.memories) {
      await store.remember(mem.content, mem.type as any, {
        sessionId: session.id,
        timestamp: session.timestamp
      });
    }
  }
  console.log(`   Stored ${sessions.reduce((sum, s) => sum + s.memories.length, 0)} memories\n`);
  
  // Test each question
  let totalScore = 0;
  let passed = 0;
  
  for (const q of questions) {
    console.log(`\n📋 ${q.id}: [${q.type}] [${q.difficulty}]`);
    console.log(`   Query: "${q.query}"`);
    
    const results = await store.recall(q.query, { limit: 5 });
    
    // Check if any result contains expected keywords
    const combinedResults = results.map(r => r.content.toLowerCase()).join(' ');
    const foundKeywords = q.expectedKeywords.filter(kw => 
      combinedResults.includes(kw.toLowerCase())
    );
    
    const score = foundKeywords.length / q.expectedKeywords.length;
    const pass = score >= 0.5;
    
    if (pass) passed++;
    totalScore += score;
    
    console.log(`   ${pass ? '✅' : '❌'} Score: ${Math.round(score * 100)}%`);
    console.log(`   Found keywords: [${foundKeywords.join(', ')}]`);
    console.log(`   Expected: [${q.expectedKeywords.join(', ')}]`);
    
    if (results.length > 0) {
      console.log(`   Top result: "${results[0].content.substring(0, 80)}..."`);
    }
  }
  
  console.log('\n' + '=' .repeat(60));
  console.log('📊 BENCHMARK RESULTS');
  console.log('');
  console.log(`Passed: ${passed}/${questions.length} (${Math.round(passed / questions.length * 100)}%)`);
  console.log(`Average Score: ${Math.round(totalScore / questions.length * 100)}%`);
  console.log('');
  
  // By type
  const typeGroups = new Map<string, { passed: number; total: number }>();
  for (const q of questions) {
    const t = typeGroups.get(q.type) || { passed: 0, total: 0 };
    t.total++;
    // We'd need to track individual results properly for this
    typeGroups.set(q.type, t);
  }
  
  console.log('By Type:');
  for (const [type, _] of typeGroups) {
    console.log(`  ${type}: see results above`);
  }
  
  console.log('');
  console.log('=' .repeat(60));
  
  store.close();
  
  // Clean up
  const fs = await import('fs');
  fs.unlinkSync('/tmp/multihop-benchmark.db');
}

run().catch(console.error);