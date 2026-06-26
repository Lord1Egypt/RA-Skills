const linter = require('../index');
const fs = require('fs');
const path = require('path');

// Create a temporary test directory
const testDir = path.join(__dirname, 'temp_test');
if (!fs.existsSync(testDir)) fs.mkdirSync(testDir);

// Create valid markdown file
const validFile = path.join(testDir, 'valid.md');
fs.writeFileSync(validFile, '# Header\n\n[Link](./valid.md)');

// Create invalid markdown file
const invalidFile = path.join(testDir, 'invalid.md');
fs.writeFileSync(invalidFile, '# Header\n\n[Broken](./missing.md)');

async function runTest() {
  console.log('Running markdown-linter test...');
  
  try {
    const report = await linter.scan(testDir);
    console.log('Report:', JSON.stringify(report, null, 2));
    
    // Check if broken links count matches expectation
    if (report.brokenLinksCount === 1) {
      console.log('Test PASSED: Detected 1 broken link correctly.');
      // Cleanup
      fs.rmSync(testDir, { recursive: true, force: true });
      process.exit(0);
    } else {
      console.error('Test FAILED: Expected 1 broken link, got', report.brokenLinksCount);
      // Cleanup
      fs.rmSync(testDir, { recursive: true, force: true });
      process.exit(1);
    }
  } catch (err) {
    console.error('Test FAILED with error:', err);
    // Cleanup
    if (fs.existsSync(testDir)) fs.rmSync(testDir, { recursive: true, force: true });
    process.exit(1);
  }
}

runTest();
