/**
 * Memory V2.0 Database Initialization
 * Extends Lossless Claw with personal modules
 */

const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');

class MemoryDatabase {
    constructor(dbPath = './memory-v2.db') {
        this.dbPath = dbPath;
        this.db = null;
    }

    async init() {
        return new Promise((resolve, reject) => {
            this.db = new sqlite3.Database(this.dbPath, (err) => {
                if (err) {
                    console.error('Error opening database:', err);
                    reject(err);
                } else {
                    console.log('✅ Connected to Memory V2.0 database');
                    resolve();
                }
            });
        });
    }

    async runSchema() {
        const schemaPath = path.join(__dirname, 'schema.sql');
        const schema = fs.readFileSync(schemaPath, 'utf8');
        
        // Split schema into individual statements
        const statements = schema
            .split(';')
            .map(s => s.trim())
            .filter(s => s.length > 0);

        for (const statement of statements) {
            await this.run(statement);
        }
        
        console.log('✅ Database schema initialized');
    }

    async run(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.run(sql, params, function(err) {
                if (err) {
                    console.error('SQL Error:', err);
                    reject(err);
                } else {
                    resolve({ id: this.lastID, changes: this.changes });
                }
            });
        });
    }

    async get(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.get(sql, params, (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }

    async all(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.all(sql, params, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    async close() {
        return new Promise((resolve, reject) => {
            this.db.close((err) => {
                if (err) {
                    reject(err);
                } else {
                    console.log('✅ Database connection closed');
                    resolve();
                }
            });
        });
    }

    // Health check
    async healthCheck() {
        try {
            const tables = await this.all(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'memory_%'"
            );
            return {
                status: 'healthy',
                tables: tables.map(t => t.name),
                timestamp: new Date().toISOString()
            };
        } catch (err) {
            return {
                status: 'unhealthy',
                error: err.message,
                timestamp: new Date().toISOString()
            };
        }
    }
}

// CLI usage
if (require.main === module) {
    const db = new MemoryDatabase();
    
    (async () => {
        try {
            await db.init();
            await db.runSchema();
            const health = await db.healthCheck();
            console.log('\n📊 Database Health:', health);
            await db.close();
            console.log('\n🎉 Memory V2.0 database initialized successfully!');
        } catch (err) {
            console.error('❌ Initialization failed:', err);
            process.exit(1);
        }
    })();
}

module.exports = MemoryDatabase;