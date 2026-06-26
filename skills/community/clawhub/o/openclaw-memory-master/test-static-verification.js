/**
 * Simple test to verify modules can be loaded
 */

console.log('🧪 Simple Module Load Test\n');

// Try to load TypeScript files using ts-node programmatically
const tsNode = require('ts-node');

// Register ts-node
tsNode.register({
  compilerOptions: {
    module: 'commonjs',
    target: 'es2020',
    esModuleInterop: true,
    skipLibCheck: true
  },
  transpileOnly: true
});

async function testModuleLoading() {
  console.log('1. Testing module imports...');
  
  try {
    // Try to import the main curator
    console.log('   Loading SmartMemoryCurator...');
    const { SmartMemoryCurator } = require('../src/smart/SmartMemoryCurator.ts');
    console.log('   ✅ SmartMemoryCurator loaded successfully');
    
    // Try to import other modules
    console.log('\n2. Loading other modules...');
    
    const modules = [
      { name: 'AutoClassifier', path: '../src/smart/AutoClassifier.ts' },
      { name: 'AutoTagger', path: '../src/smart/AutoTagger.ts' },
      { name: 'DeduplicationEngine', path: '../src/smart/DeduplicationEngine.ts' },
      { name: 'ImportanceScorer', path: '../src/smart/ImportanceScorer.ts' },
      { name: 'RelationDiscoverer', path: '../src/smart/RelationDiscoverer.ts' }
    ];
    
    for (const module of modules) {
      try {
        require(module.path);
        console.log(`   ✅ ${module.name} loaded successfully`);
      } catch (error) {
        console.log(`   ❌ ${module.name} failed: ${error.message}`);
      }
    }
    
    console.log('\n3. Testing instantiation...');
    
    try {
      const curator = new SmartMemoryCurator();
      console.log('   ✅ SmartMemoryCurator instantiated');
      
      // Test basic functionality
      console.log('\n4. Testing basic analysis...');
      
      const testMemory = {
        content: 'Testing smart memory curation system',
        metadata: { test: true }
      };
      
      const startTime = Date.now();
      const result = await curator.analyze(testMemory);
      const processingTime = Date.now() - startTime;
      
      console.log('   Analysis completed in', processingTime, 'ms');
      console.log('   Category:', result.category);
      console.log('   Tags:', result.tags.slice(0, 3).join(', '));
      console.log('   Importance:', result.importance);
      console.log('   Is duplicate:', result.isDuplicate);
      
      console.log('\n🎉 BASIC TESTS PASSED!');
      return true;
      
    } catch (error) {
      console.log('   ❌ Instantiation/Analysis failed:', error.message);
      console.log('   Stack:', error.stack);
      return false;
    }
    
  } catch (error) {
    console.log('❌ Module loading failed:', error.message);
    console.log('Stack:', error.stack);
    return false;
  }
}

// Run test
testModuleLoading().then(success => {
  if (success) {
    console.log('\n✅ All basic tests passed!');
    process.exit(0);
  } else {
    console.log('\n⚠️ Some tests failed. See errors above.');
    process.exit(1);
  }
}).catch(error => {
  console.error('❌ Test runner crashed:', error);
  process.exit(1);
});