/**
 * Test Time Reasoning Engine directly
 */

import { createTimeReasoning } from '../../src/background/time-reasoning.js';

const engine = createTimeReasoning(new Date('2026-03-18T12:00:00Z')); // Wednesday

const testQueries = [
  '如果明天是周三，我需要准备什么？',
  '下周有什么需要提前准备的事情？',
  '这个月有什么会议安排？',
  '3月15日有什么安排？',
];

console.log('=== Time Reasoning Engine Test ===\n');
console.log('Current date: 2026-03-18 (Wednesday)\n');

for (const query of testQueries) {
  console.log(`Query: "${query}"`);
  
  const context = engine.parseTimeQuery(query);
  console.log('  Time Context:', {
    hasTimeReasoning: context.hasTimeReasoning,
    relativeTime: context.relativeTime,
    dayOfWeek: context.dayOfWeek,
    parsedDate: context.parsedDate,
    keywords: context.keywords,
  });
  
  const conditional = engine.resolveConditionalTime(query);
  console.log('  Conditional:', conditional);
  
  console.log();
}

// Also test combined keywords
console.log('\n=== Combined Keywords for Wednesday Query ===');
const wednesdayQuery = '如果明天是周三，我需要准备什么？';
const context = engine.parseTimeQuery(wednesdayQuery);
const conditional = engine.resolveConditionalTime(wednesdayQuery);

const allKeywords = [...new Set([
  ...context.keywords,
  ...(conditional.isConditional ? conditional.keywords : []),
])];

console.log('All keywords:', allKeywords);