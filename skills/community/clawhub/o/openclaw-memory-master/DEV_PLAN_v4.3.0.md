/**
 * Test Runner for Smart Memory Curation System
 * 
 * Run with: node test/run-tests.js
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const path = require('path');
const fs = require('fs');

const execAsync = promisify(exec);

async function runTests() {
  console.log('🧪 Preparing to run comprehensive tests...\n');
  
  // Check if TypeScript is installed
  try {
    await execAsync('tsc --version');
  } catch (error) {
    console.log('⚠️ TypeScript not found. Installing TypeScript locally...');
    try {
      await execAsync('npm install typescript --no-save');
    } catch (installError) {
      console.error('❌ Failed to install TypeScript:', installError.message);
      return { success: false, error: installError };
    }
  }
  
  // Check if ts-node is installed
  let tsNodeAvailable = true;
  try {
    await execAsync('ts-node --version');
  } catch (error) {
    tsNodeAvailable = false;
    console.log('⚠️ ts-node not found. Will compile TypeScript first.');
  }
  
  const testFile = path.join(__dirname, 'comprehensive.test.ts');
  
  if (!fs.existsSync(testFile)) {
    console.error('❌ Test file not found:', testFile);
    return { success: false, error: 'Test file not found' };
  }
  
  try {
    if (tsNodeAvailable) {
      console.log('🚀 Running tests with ts-node...\n');
      const { stdout, stderr } = await execAsync(`ts-node ${testFile}`, {
        cwd: path.dirname(__dirname),
        stdio: 'inherit'
      });
    } else {
      console.log('🔧 Compiling TypeScript...');
      await execAsync('tsc --outDir dist --module commonjs --target es2020 --lib es2020,dom --esModuleInterop --resolveJsonModule --declaration src/**/*.ts test/**/*.ts', {
        cwd: path.dirname(__dirname)
      });
      
      console.log('🚀 Running compiled tests...\n');
      const compiledTestFile = path.join(__dirname, '..', 'dist', 'test', 'comprehensive.test.js');
      const { stdout, stderr } = await execAsync(`node ${compiledTestFile}`, {
        cwd: path.dirname(__dirname),
        stdio: 'inherit'
      });
    }
    
    console.log('\n✅ Tests completed successfully!');
    return { success: true };
    
  } catch (error) {
    console.error('❌ Test execution failed:');
    if (error.stdout) console.log(error.stdout);
    if (error.stderr) console.log(error.stderr);
    return { success: false, error };
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  runTests().then(result => {
    if (result.success) {
      console.log('\n🎉 All tests passed!');
      process.exit(0);
    } else {
      console.error('\n⚠️ Tests failed.');
      process.exit(1);
    }
  }).catch(error => {
    console.error('❌ Unexpected error:', error);
    process.exit(1);
  });
}

module.exports = { runTests };