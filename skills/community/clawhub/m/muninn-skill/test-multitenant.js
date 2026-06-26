/**
 * Test multi-tenancy in Muninn Memory System
 */

import { MemoryStore } from './dist/storage/index.js';
import { rmSync, existsSync } from 'fs';

const TEST_DB = '/tmp/muninn-multitenant-test.db';

async function main() {
  // Clean up any existing test database
  if (existsSync(TEST_DB)) {
    rmSync(TEST_DB);
  }

  console.log('🧪 Testing Muninn Multi-Tenancy\n');
  
  const store = new MemoryStore(TEST_DB);
  
  console.log('✅ Store initialized\n');
  
  // Test 1: Create memories for different users
  console.log('📝 Creating memories for different users...');
  
  const aliceMemory = await store.remember(
    'Alice loves hiking in the mountains',
    'semantic',
    { user_id: 'alice' }
  );
  console.log(`  Alice memory: ${aliceMemory.id}`);
  
  const bobMemory = await store.remember(
    'Bob prefers coding late at night',
    'semantic',
    { user_id: 'bob' }
  );
  console.log(`  Bob memory: ${bobMemory.id}`);
  
  const defaultMemory = await store.remember(
    'Default user likes coffee',
    'semantic'
  );
  console.log(`  Default memory: ${defaultMemory.id}`);
  
  console.log('\n');
  
  // Test 2: Alice should only see her memories
  console.log('🔍 Testing Alice\'s view...');
  const aliceResults = await store.recall('what does alice like', { user_id: 'alice' });
  console.log(`  Alice sees ${aliceResults.length} memories`);
  
  const aliceHasBob = aliceResults.some(m => m.content.includes('Bob'));
  
  if (aliceHasBob) {
    console.log('  ❌ FAIL: Alice can see Bob\'s memory!');
    process.exit(1);
  } else {
    console.log('  ✅ PASS: Alice cannot see Bob\'s memory');
  }
  
  // Test 3: Bob should only see his memories
  console.log('\n🔍 Testing Bob\'s view...');
  const bobResults = await store.recall('what does bob like', { user_id: 'bob' });
  console.log(`  Bob sees ${bobResults.length} memories`);
  
  const bobHasAlice = bobResults.some(m => m.content.includes('Alice'));
  
  if (bobHasAlice) {
    console.log('  ❌ FAIL: Bob can see Alice\'s memory!');
    process.exit(1);
  } else {
    console.log('  ✅ PASS: Bob cannot see Alice\'s memory');
  }
  
  // Test 4: Stats should show all memories
  console.log('\n📊 Testing stats...');
  const stats = store.getStats();
  console.log(`  Total memories: ${stats.total}`);
  
  // Test 5: Verify user_id is stored
  console.log('\n🔑 Testing user_id storage...');
  const aliceMem = store.getMemory(aliceMemory.id);
  if (aliceMem && aliceMem.user_id === 'alice') {
    console.log('  ✅ PASS: user_id stored correctly');
  } else {
    console.log('  ❌ FAIL: user_id not stored correctly');
    console.log(`    Expected: alice, Got: ${aliceMem?.user_id}`);
    process.exit(1);
  }
  
  console.log('\n');
  console.log('═════════════════════════════════════════════════');
  console.log('✅ ALL MULTI-TENANCY TESTS PASSED!');
  console.log('═════════════════════════════════════════════════\n');
  
  store.close();
  rmSync(TEST_DB);
  
  process.exit(0);
}

main().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
