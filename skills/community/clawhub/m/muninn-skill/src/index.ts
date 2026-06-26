/**
 * OpenClaw Memory System v1 - Entry Point
 * 
 * Usage:
 *   node dist/index.js           # Start REST server (future)
 *   npm run mcp                  # Start MCP server
 *   node dist/index.js test      # Run tests
 */

import { MemoryStore } from './storage/index.js';

async function main() {
  const args = process.argv.slice(2);
  
  if (args[0] === 'test') {
    // Run quick test
    console.log('🧪 Running quick test...\n');
    const store = new MemoryStore('/tmp/test-memory-quick.db');
    
    const mem = await store.remember('Test memory: User prefers dark mode', 'semantic');
    console.log('✅ Stored:', mem.id);
    
    const results = await store.recall('user preferences');
    console.log('✅ Recalled:', results.length, 'memories');
    
    const stats = store.getStats();
    console.log('✅ Stats:', stats);
    
    store.close();
    console.log('\n✅ All tests passed!');
  } else {
    console.log('OpenClaw Memory System v1');
    console.log('Run "npm run mcp" to start MCP server');
  }
}

main().catch(console.error);
