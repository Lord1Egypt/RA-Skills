/**
 * Test multi-hop retrieval
 */

import { MemoryStore } from './dist/storage/index.js';
import { multiHopRetrieval, extractQueryEntities, extractTemporalConstraints, expandKeywords } from './dist/retrieval/multi-hop.js';

async function main() {
  console.log('=== Multi-Hop Retrieval Test ===\n');
  
  // Create test store
  const store = new MemoryStore('./test-multihop.db');
  
  // Seed with test data
  console.log('Seeding test memories...\n');
  
  await store.remember('Caroline went to the LGBTQ support group on May 7th. She found it very supportive.', 'episodic', {
    sessionId: 'session-1',
    timestamp: '2023-05-07T10:00:00Z'
  });
  
  await store.remember('Caroline discussed her job situation on May 10th. She mentioned feeling burned out and considering a career change.', 'episodic', {
    sessionId: 'session-2',
    timestamp: '2023-05-10T14:00:00Z'
  });
  
  await store.remember('Caroline talked about her new project at work. She seemed excited about the challenge.', 'episodic', {
    sessionId: 'session-3',
    timestamp: '2023-05-15T09:00:00Z'
  });
  
  await store.remember('David mentioned Caroline in a meeting. He said she was doing great work on the project.', 'episodic', {
    sessionId: 'session-4',
    timestamp: '2023-05-20T11:00:00Z'
  });
  
  await store.remember('The project deadline was moved to June 1st. Caroline will need to work extra hours.', 'semantic', {
    sessionId: 'session-4',
    timestamp: '2023-05-20T11:30:00Z'
  });
  
  // Test entity extraction
  console.log('=== Entity Extraction ===');
  const query1 = 'What did Caroline say about her job after she went to the LGBTQ support group?';
  const entities = extractQueryEntities(query1);
  console.log(`Query: "${query1}"`);
  console.log(`Entities: ${entities.join(', ')}\n`);
  
  // Test temporal constraint extraction
  console.log('=== Temporal Constraints ===');
  const temporal = extractTemporalConstraints(query1);
  console.log(`Temporal constraint: ${JSON.stringify(temporal)}\n`);
  
  // Test keyword expansion
  console.log('=== Keyword Expansion ===');
  const keywords = expandKeywords(['job', 'worried']);
  console.log(`Expanded keywords: ${keywords.join(', ')}\n`);
  
  // Test multi-hop retrieval
  console.log('=== Multi-Hop Retrieval ===');
  const result = await multiHopRetrieval(
    query1,
    (entity, limit) => store.getMemoriesByEntity(entity, limit),
    {
      limit: 10,
      entityBudget: 50,
      allMemories: store.getAllMemories(),
      enableFallback: false
    }
  );
  
  console.log(`Method: ${result.method}`);
  console.log(`Confidence: ${result.confidence.toFixed(2)}`);
  console.log(`Memories found: ${result.memories.length}\n`);
  
  result.memories.forEach((m, i) => {
    console.log(`${i + 1}. [${m.timestamp?.split('T')[0] || 'no date'}] ${m.content.substring(0, 100)}...`);
    console.log(`   Entities: ${(m.entities || []).join(', ')}`);
    console.log(`   Salience: ${(m.salience || 0.5).toFixed(2)}\n`);
  });
  
  // Test a different query
  console.log('=== Test Query 2 ===');
  const query2 = 'How is the project going?';
  const result2 = await multiHopRetrieval(
    query2,
    (entity, limit) => store.getMemoriesByEntity(entity, limit),
    {
      limit: 5,
      enableFallback: false
    }
  );
  
  console.log(`Query: "${query2}"`);
  console.log(`Method: ${result2.method}`);
  console.log(`Confidence: ${result2.confidence.toFixed(2)}`);
  console.log(`Memories: ${result2.memories.length}\n`);
  
  // Clean up
  store.close();
  
  // Delete test database
  const fs = await import('fs');
  fs.unlinkSync('./test-multihop.db');
  
  console.log('=== Test Complete ===');
}

main().catch(console.error);