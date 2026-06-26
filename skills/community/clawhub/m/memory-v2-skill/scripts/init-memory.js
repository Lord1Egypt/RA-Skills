/**
 * Initialize Memory V2 Database
 * Usage: node scripts/init-memory.js [database-path]
 */

const MemoryAPI = require('../api');
const path = require('path');

const dbPath = process.argv[2] || './memory-v2.db';

console.log('🚀 Initializing Memory V2 Database...\n');

(async () => {
    try {
        const api = new MemoryAPI(dbPath);
        await api.init();
        
        console.log('✅ Database initialized successfully!');
        console.log(`📁 Location: ${path.resolve(dbPath)}`);
        console.log('\nNext steps:');
        console.log('  1. Use the API to track learning, decisions, etc.');
        console.log('  2. Run tests: npm test');
        console.log('  3. Create backups: npm run backup');
        
        await api.close();
    } catch (err) {
        console.error('❌ Initialization failed:', err.message);
        process.exit(1);
    }
})();
