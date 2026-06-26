/**
 * Comprehensive Multi-Hop Benchmark
 */

import MemoryStore from './dist/storage/index.js';

// LOCOMO-style multi-hop data
const locomoData = [
  // Project facts
  { content: 'Elev8Advisory is an AI-powered HR tool for small businesses. It creates HR policies automatically.', type: 'semantic', entities: ['Elev8Advisory'] },
  { content: 'Elev8Advisory has a customer paying $500/month for HR policy generation.', type: 'semantic', entities: ['Elev8Advisory'] },
  { content: 'Elev8Advisory is the current priority project.', type: 'semantic', entities: ['Elev8Advisory'] },
  { content: 'BrandForge is an AI-powered branding tool with $320 revenue.', type: 'semantic', entities: ['BrandForge'] },
  { content: 'BrandForge is secondary priority after Elev8Advisory.', type: 'semantic', entities: ['BrandForge'] },
  { content: 'Muninn is a memory system using SQLite and Nomic embeddings.', type: 'semantic', entities: ['Muninn', 'SQLite', 'Ollama'] },
  { content: 'Muninn Phase 1 completed with 100% router accuracy and 91% entity precision.', type: 'semantic', entities: ['Muninn'] },
];

// Caroline multi-hop data
const carolineData = [
  { content: 'Caroline went to the LGBTQ support group on May 7th. She found it very supportive.', type: 'episodic', timestamp: '2023-05-07T10:00:00Z' },
  { content: 'Caroline works at a tech startup as a product manager.', type: 'semantic' },
  { content: 'Caroline discussed her job situation on May 10th. She mentioned feeling burned out and considering a career change.', type: 'episodic', timestamp: '2023-05-10T14:00:00Z' },
  { content: 'Caroline has been at her current job for 3 years.', type: 'semantic' },
  { content: 'Caroline talked about her new project at work on May 15th. She seemed excited about the challenge.', type: 'episodic', timestamp: '2023-05-15T09:00:00Z' },
  { content: 'The project involves redesigning the company website.', type: 'semantic' },
  { content: 'David mentioned Caroline in a meeting. He said she was doing great work on the website project.', type: 'episodic' },
  { content: 'The website project deadline was moved to June 1st. Caroline will need to work extra hours.', type: 'episodic' },
];

const questions = [
  // LOCOMO q13 (failing)
  {
    id: 'q13',
    query: 'What projects is Phillip building and what are their current statuses?',
    expectedKeywords: ['Elev8Advisory', 'priority', 'BrandForge', 'secondary', 'Muninn', 'Phase 1'],
    type: 'multi-hop',
    difficulty: 'hard'
  },
  // Caroline temporal multi-hop
  {
    id: 'caroline-1',
    query: 'What did Caroline say about her job after she went to the LGBTQ support group?',
    expectedKeywords: ['burned out', 'career change', 'burned', 'considering'],
    type: 'temporal-multi-hop',
    difficulty: 'hard'
  },
  // Caroline evolution
  {
    id: 'caroline-2',
    query: 'How did Caroline\'s feelings about work change from May 7th to May 15th?',
    expectedKeywords: ['burned out', 'excited', 'supportive', 'challenge'],
    type: 'temporal-evolution',
    difficulty: 'hard'
  },
  // Caroline connection
  {
    id: 'caroline-3',
    query: 'What project is Caroline working on and who praised her work?',
    expectedKeywords: ['website', 'David', 'project', 'redesign'],
    type: 'connection',
    difficulty: 'medium'
  },
  // Temporal
  {
    id: 'caroline-4',
    query: 'When is the website project deadline?',
    expectedKeywords: ['June 1st', 'June', 'deadline'],
    type: 'temporal',
    difficulty: 'easy'
  },
];

async function run() {
  console.log('🔍 Comprehensive Multi-Hop Benchmark\n');
  console.log('='.repeat(60));
  
  const store = new MemoryStore('/tmp/comprehensive-multihop.db');
  
  console.log('\n📝 Seeding LOCOMO data...');
  for (const mem of locomoData) {
    await store.remember(mem.content, mem.type, { entities: mem.entities });
  }
  
  console.log('📝 Seeding Caroline data...');
  for (const mem of carolineData) {
    await store.remember(mem.content, mem.type, { 
      timestamp: mem.timestamp,
      sessionId: mem.timestamp ? 'session-' + mem.timestamp.split('T')[0] : undefined
    });
  }
  
  console.log(`   Stored ${locomoData.length + carolineData.length} memories\n`);
  
  let totalScore = 0;
  let passed = 0;
  const results = [];
  
  for (const q of questions) {
    console.log(`\n📋 ${q.id}: [${q.type}] [${q.difficulty}]`);
    console.log(`   Query: "${q.query}"`);
    
    const results_raw = await store.recall(q.query, { limit: 5 });
    
    const combinedResults = results_raw.map(r => r.content.toLowerCase()).join(' ');
    const foundKeywords = q.expectedKeywords.filter(kw => 
      combinedResults.includes(kw.toLowerCase())
    );
    
    const score = foundKeywords.length / q.expectedKeywords.length;
    const pass = score >= 0.5;
    
    if (pass) passed++;
    totalScore += score;
    results.push({ id: q.id, type: q.type, difficulty: q.difficulty, score, pass });
    
    console.log(`   ${pass ? '✅' : '❌'} Score: ${Math.round(score * 100)}%`);
    console.log(`   Found: [${foundKeywords.join(', ')}]`);
    console.log(`   Expected: [${q.expectedKeywords.join(', ')}]`);
    
    if (results_raw.length > 0) {
      console.log(`   Top 2 results:`);
      results_raw.slice(0, 2).forEach((r, i) => {
        console.log(`     ${i + 1}. "${r.content.substring(0, 60)}..."`);
      });
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 RESULTS BY TYPE');
  
  const typeResults = new Map();
  for (const r of results) {
    if (!typeResults.has(r.type)) typeResults.set(r.type, { passed: 0, total: 0, scores: [] });
    const t = typeResults.get(r.type);
    t.total++;
    if (r.pass) t.passed++;
    t.scores.push(r.score);
  }
  
  for (const [type, data] of typeResults) {
    const avgScore = data.scores.reduce((a, b) => a + b, 0) / data.scores.length;
    console.log(`  ${type}: ${data.passed}/${data.total} passed (${Math.round(avgScore * 100)}% avg)`);
  }
  
  console.log('\n📊 RESULTS BY DIFFICULTY');
  const diffResults = new Map();
  for (const r of results) {
    if (!diffResults.has(r.difficulty)) diffResults.set(r.difficulty, { passed: 0, total: 0, scores: [] });
    const d = diffResults.get(r.difficulty);
    d.total++;
    if (r.pass) d.passed++;
    d.scores.push(r.score);
  }
  
  for (const [diff, data] of diffResults) {
    const avgScore = data.scores.reduce((a, b) => a + b, 0) / data.scores.length;
    console.log(`  ${diff}: ${data.passed}/${data.total} passed (${Math.round(avgScore * 100)}% avg)`);
  }
  
  console.log('\n' + '='.repeat(60));
  console.log(`📊 OVERALL: ${passed}/${questions.length} passed (${Math.round(passed / questions.length * 100)}%)`);
  console.log(`📊 AVERAGE SCORE: ${Math.round(totalScore / questions.length * 100)}%`);
  console.log('='.repeat(60));
  
  store.close();
  
  const fs = await import('fs');
  fs.unlinkSync('/tmp/comprehensive-multihop.db');
}

run().catch(console.error);