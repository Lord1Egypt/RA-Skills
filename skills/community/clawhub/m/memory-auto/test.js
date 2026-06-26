# Memory Auto Archive - Test Script

// Simulate the archive flow without PowerShell

const WORKSPACE = 'C:\\Users\\42517\\.openclaw\\workspace';
const MEMORY_DIR = join(WORKSPACE, 'memory');

console.log('=== TEST MEMORY AUTO ARCHIVE ===');

// Check yesterday file
const yesterday = new Date();
yesterday.setDate(yesterday.getDate() - 1);
const yStr = yesterday.toISOString().split('T')[0];
const dailyFile = join(MEMORY_DIR, `${yStr}.md`);

console.log(`Would create: ${dailyFile}`);
console.log('(Skipping actual execution for safety)');
