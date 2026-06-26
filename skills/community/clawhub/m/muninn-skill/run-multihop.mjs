/**
 * Multi-Hop Retrieval Benchmark
 */

import MemoryStore from './dist/storage/index.js';

// Multi-hop test data
const sessions = [
  {
    id: 's1',
    timestamp: '2023-05-07T10:00:00Z',
    memories: [
      { content: 'Caroline went to the LGBTQ support group. She found it very supportive and made new friends.', type: 'episodic' },
      { content: 'Caroline works at a tech startup as a product manager.', type: 'semantic' },
    ]
  },
  {
    id: 's2',
    timestamp: '2023-05-10T14:00:00Z',
    memories: [
      { content: 'Caroline discussed her job situation. She mentioned feeling burned out and considering a career change.', type: 'episodic' },
      { content: 'Caroline has been at her current job for 3 years.', type: 'semantic' },
    ]
  },
  {
    id: 's3',
    timestamp: '2023-05-15T09:00:00Z',
    memories: [
      { content: 'Caroline talked about her new project at work. She seemed excited about the challenge.', type: 'episodic' },
      { content: 'The project involves redesigning the company website.', type: 'semantic' },
    ]
  },
  {
    id: 's4',
    timestamp: '2023-05-20T11:00:00Z',
    memories: [
      { content: 'David mentioned Caroline in a meeting. He said she was doing great work on the website project.', type: 'episodic' },
    ]
  },
  {
    id: 's5',
    timestamp: '2023-05-25T15:00:00Z',
    memories: [
      { content: 'The website project deadline was moved to June 1st. Caroline will need to work extra hours.', type: 'episodic' },
    ]
  },
];

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
  console.log('='.repeat(60));
  
  const store = new MemoryStore('/tmp/multihop-benchmark.db');
  
  console.log('\n📝 Seeding memories...');
  for (const session of sessions) {
    for (const mem of session.memories) {
      await store.remember(mem.content, mem.type, {
        sessionId: session.id,
        timestamp: session.timestamp
      });
    }
  }
  console.log(`   Stored ${sessions.reduce((sum, s) => sum + s.memories.length, 0)} memories\n`);
  
  let totalScore = 0;
  let passed = 0;
  
  for (const q of questions) {
    console.log(`\n📋 ${q.id}: [${q.type}] [${q.difficulty}]`);
    console.log(`   Query: "${q.query}"`);
    
    const results = await store.recall(q.query, { limit: 5 });
    
    const combinedResults = results.map(r => r.content.toLowerCase()).join(' ');
    const foundKeywords = q.expectedKeywords.filter(kw => 
      combinedResults.includes(kw.toLowerCase())
    );
    
    const score = foundKeywords.length / q.expectedKeywords.length;
    const pass = score >= 0.5;
    
    if (pass) passed++;
    totalScore += score;
    
    console.log(`   ${pass ? '✅' : '❌'} Score: ${Math.round(score * 100)}%`);
    console.log(`   Found: [${foundKeywords.join(', ')}]`);
    
    if (results.length > 0) {
      console.log(`   Top: "${results[0].content.substring(0, 80)}..."`);
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 RESULTS');
  console.log(`Passed: ${passed}/${questions.length} (${Math.round(passed / questions.length * 100)}%)`);
  console.log(`Average: ${Math.round(totalScore / questions.length * 100)}%`);
  console.log('='.repeat(60));
  
  store.close();
  
  const fs = await import('fs');
  fs.unlinkSync('/tmp/multihop-benchmark.db');
}

run().catch(console.error);