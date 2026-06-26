/**
 * Memory V2.5 Demo Data Initialization
 * Creates sample data for testing and demonstration
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = process.argv[2] || './demo-memory-v2.5.db';

console.log('🚀 Initializing Memory V2.5 Demo Data...');
console.log(`📁 Database: ${dbPath}`);

const db = new sqlite3.Database(dbPath);

// Read and execute schema
const fs = require('fs');
const schemaPath = path.join(__dirname, '..', 'database', 'schema.sql');
const schema = fs.readFileSync(schemaPath, 'utf8');

// Execute schema
const statements = schema.split(';').filter(s => s.trim());

async function initDemo() {
  try {
    // Run schema
    for (const statement of statements) {
      if (statement.trim()) {
        await new Promise((resolve, reject) => {
          db.exec(statement, (err) => {
            if (err) reject(err);
            else resolve();
          });
        });
      }
    }
    console.log('✅ Schema initialized');

    // Insert demo data
    console.log('📝 Inserting demo data...');

    // Demo priorities
    await insertDemoData(db, 'memory_priorities', [
      { message_id: 'demo-msg-001', conversation_id: 1, priority_level: 1, importance_score: 95, keywords: '["urgent","critical"]', context_summary: 'Critical system alert' },
      { message_id: 'demo-msg-002', conversation_id: 1, priority_level: 2, importance_score: 75, keywords: '["important","review"]', context_summary: 'Important decision pending' },
      { message_id: 'demo-msg-003', conversation_id: 1, priority_level: 3, importance_score: 50, keywords: '["normal","routine"]', context_summary: 'Regular update' }
    ]);

    // Demo learning
    await insertDemoData(db, 'memory_learning', [
      { message_id: 'demo-learn-001', conversation_id: 1, learning_topic: 'OpenClaw Skill Development', topic_category: 'programming', progress_status: 'in_progress', progress_percentage: 65, milestone_count: 5, completed_milestones: 3, notes: 'Learning to build OpenClaw skills with proper architecture' },
      { message_id: 'demo-learn-002', conversation_id: 1, learning_topic: 'AI Agent Orchestration', topic_category: 'ai', progress_status: 'started', progress_percentage: 25, milestone_count: 4, completed_milestones: 1, notes: 'Understanding multi-agent systems' },
      { message_id: 'demo-learn-003', conversation_id: 1, learning_topic: 'Memory Systems Design', topic_category: 'system_design', progress_status: 'completed', progress_percentage: 100, milestone_count: 3, completed_milestones: 3, notes: 'Completed study of memory management patterns' }
    ]);

    // Demo decisions
    await insertDemoData(db, 'memory_decisions', [
      { message_id: 'demo-dec-001', conversation_id: 1, decision_type: 'architecture', decision_question: 'Which database to use?', decision_context: 'Choosing storage for agent memory', options_considered: '["SQLite","PostgreSQL","MySQL"]', chosen_option: 'SQLite', rationale: 'Lightweight, embedded, perfect for local agent memory', confidence_level: 4, expected_outcome: 'Simple deployment and maintenance', outcome_status: 'implemented', review_date: '2026-04-25' },
      { message_id: 'demo-dec-002', conversation_id: 1, decision_type: 'framework', decision_question: 'Which AI framework?', decision_context: 'Selecting agent framework', options_considered: '["LangChain","AutoGPT","OpenClaw"]', chosen_option: 'OpenClaw', rationale: 'Native support, better integration', confidence_level: 5, expected_outcome: 'Seamless agent experience', outcome_status: 'validated', review_date: '2026-04-20' },
      { message_id: 'demo-dec-003', conversation_id: 1, decision_type: 'deployment', decision_question: 'Cloud or local deployment?', decision_context: 'Infrastructure decision', options_considered: '["Cloud VPS","Local Server","Hybrid"]', chosen_option: 'Hybrid', rationale: 'Balance of control and scalability', confidence_level: 3, expected_outcome: 'Flexible deployment options', outcome_status: 'pending', review_date: '2026-05-01' }
    ]);

    // Demo evolution
    await insertDemoData(db, 'memory_evolution', [
      { skill_name: 'JavaScript', skill_category: 'programming', proficiency_level: 8, experience_points: 2500, usage_count: 150, success_count: 140, failure_count: 10, performance_metrics: '{"complexity":8,"efficiency":9}' },
      { skill_name: 'SQLite', skill_category: 'database', proficiency_level: 7, experience_points: 1800, usage_count: 80, success_count: 75, failure_count: 5, performance_metrics: '{"complexity":6,"efficiency":8}' },
      { skill_name: 'Agent Design', skill_category: 'ai', proficiency_level: 6, experience_points: 1200, usage_count: 45, success_count: 40, failure_count: 5, performance_metrics: '{"complexity":9,"efficiency":7}' },
      { skill_name: 'Project Management', skill_category: 'management', proficiency_level: 7, experience_points: 2000, usage_count: 100, success_count: 95, failure_count: 5, performance_metrics: '{"complexity":7,"efficiency":8}' }
    ]);

    console.log('✅ Demo data inserted');

    // Verify
    const tables = ['memory_priorities', 'memory_learning', 'memory_decisions', 'memory_evolution'];
    for (const table of tables) {
      const count = await new Promise((resolve, reject) => {
        db.get(`SELECT COUNT(*) as count FROM ${table}`, (err, row) => {
          if (err) reject(err);
          else resolve(row.count);
        });
      });
      console.log(`  - ${table}: ${count} records`);
    }

    console.log('\n✅ Demo database ready!');
    console.log(`📁 Location: ${dbPath}`);
    console.log('\n💡 Usage:');
    console.log(`   const api = new MemoryAPI('${dbPath}');`);
    console.log('   await api.init();');

    db.close();
    process.exit(0);
  } catch (err) {
    console.error('\n❌ Error:', err.message);
    db.close();
    process.exit(1);
  }
}

function insertDemoData(db, table, rows) {
  return Promise.all(rows.map(row => {
    const columns = Object.keys(row).join(', ');
    const placeholders = Object.keys(row).map(() => '?').join(', ');
    const values = Object.values(row);
    
    return new Promise((resolve, reject) => {
      db.run(`INSERT INTO ${table} (${columns}) VALUES (${placeholders})`, values, function(err) {
        if (err) reject(err);
        else resolve(this.lastID);
      });
    });
  }));
}

initDemo();
