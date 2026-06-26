/**
 * Session Persistence Demo
 * 
 * Demonstrates all features of the session persistence module
 */

const { getSessionManager, SessionState } = require('./session-manager');

async function demo() {
  console.log('╔════════════════════════════════════════╗');
  console.log('║   Session Persistence Demo            ║');
  console.log('╚════════════════════════════════════════╝\n');
  
  // Get the session manager
  const manager = getSessionManager();
  
  // Initialize (loads existing sessions from disk)
  console.log('1. Initializing session manager...');
  await manager.initialize();
  console.log('   ✓ Initialized\n');
  
  // Create some sessions
  console.log('2. Creating sessions...');
  const session1 = await manager.createSession('demo-session-1', 'user-001', 'feishu');
  const session2 = await manager.createSession('demo-session-2', 'user-002', 'feishu');
  console.log('   ✓ Created 2 sessions\n');
  
  // Set context and variables
  console.log('3. Setting session context...');
  await manager.setSessionContext('demo-session-1', 'userMd', '# User 001\n\nFirst demo user');
  await manager.setSessionVariable('demo-session-1', 'messageCount', 10);
  await manager.setSessionContext('demo-session-2', 'userMd', '# User 002\n\nSecond demo user');
  console.log('   ✓ Context saved\n');
  
  // Show current stats
  console.log('4. Current session statistics:');
  let stats = manager.getStats();
  console.log(`   Total: ${stats.total}`);
  console.log(`   Active: ${stats.active}`);
  console.log(`   Hibernating: ${stats.hibernating}`);
  console.log(`   Archived: ${stats.archived}\n`);
  
  // Simulate activity
  console.log('5. Simulating session activity...');
  await manager.touchSession('demo-session-1');
  console.log('   ✓ Touched demo-session-1\n');
  
  // Manually hibernate a session
  console.log('6. Manually hibernating demo-session-2...');
  await manager.hibernateSession('demo-session-2');
  const hibernatedSession = manager.getSession('demo-session-2');
  console.log(`   ✓ State: ${hibernatedSession.state}`);
  console.log(`   ✓ Hibernated at: ${new Date(hibernatedSession.hibernatedAt).toLocaleString()}\n`);
  
  // Show updated stats
  console.log('7. Updated statistics:');
  stats = manager.getStats();
  console.log(`   Total: ${stats.total}`);
  console.log(`   Active: ${stats.active}`);
  console.log(`   Hibernating: ${stats.hibernating}`);
  console.log(`   Archived: ${stats.archived}\n`);
  
  // Wake up hibernated session
  console.log('8. Waking up demo-session-2...');
  await manager.touchSession('demo-session-2');
  const awakenedSession = manager.getSession('demo-session-2');
  console.log(`   ✓ State: ${awakenedSession.state}\n`);
  
  // Archive a session
  console.log('9. Archiving demo-session-2...');
  await manager.archiveSession('demo-session-2');
  const archivedSession = manager.getSession('demo-session-2');
  console.log(`   ✓ State: ${archivedSession.state}`);
  console.log(`   ✓ Archived at: ${new Date(archivedSession.archivedAt).toLocaleString()}\n`);
  
  // Final stats
  console.log('10. Final statistics:');
  stats = manager.getStats();
  console.log(`    Total: ${stats.total}`);
  console.log(`    Active: ${stats.active}`);
  console.log(`    Hibernating: ${stats.hibernating}`);
  console.log(`    Archived: ${stats.archived}\n`);
  
  // Export sessions
  console.log('11. Exporting sessions...');
  const exportPath = await manager.exportSessions();
  console.log(`    ✓ Exported to: ${exportPath}\n`);
  
  // Show all sessions
  console.log('12. All sessions:');
  for (const [id, session] of manager.sessions) {
    console.log(`    - ${id}: ${session.state} (user: ${session.userId})`);
  }
  console.log('');
  
  console.log('╔════════════════════════════════════════╗');
  console.log('║   Demo Complete!                      ║');
  console.log('╚════════════════════════════════════════╝');
}

// Run demo
demo().catch(console.error);
