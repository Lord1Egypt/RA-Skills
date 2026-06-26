/**
 * Session Auto-Scaler Demo
 * 
 * This script demonstrates the auto-scaling functionality:
 * 1. Initialize the auto-scaler
 * 2. Simulate load on sessions
 * 3. Watch automatic scaling operations
 */

const path = require('path');
const { getSessionAutoScaler } = require('./session-autoscaler');
const { getSessionManager } = require('../session-persistence/session-manager');

async function demo() {
  console.log('='.repeat(60));
  console.log('Session Auto-Scaler Demo');
  console.log('='.repeat(60));
  console.log();
  
  // Initialize session manager first
  console.log('[1/5] Initializing Session Manager...');
  const sessionManager = getSessionManager();
  await sessionManager.initialize();
  console.log('✓ Session Manager initialized');
  console.log();
  
  // Initialize auto-scaler
  console.log('[2/5] Initializing Auto-Scaler...');
  const autoScaler = getSessionAutoScaler();
  await autoScaler.initialize();
  console.log('✓ Auto-Scaler initialized');
  console.log();
  
  // Create initial sessions
  console.log('[3/5] Creating initial sessions...');
  const session1 = await sessionManager.createSession('demo-session-1', 'user-1', 'feishu');
  const session2 = await sessionManager.createSession('demo-session-2', 'user-2', 'feishu');
  console.log('✓ Created 2 demo sessions');
  console.log();
  
  // Simulate load
  console.log('[4/5] Simulating load on sessions...');
  
  // Simulate messages on session 1 (high load)
  console.log('  - Sending 80 messages to session-1...');
  for (let i = 0; i < 80; i++) {
    autoScaler.recordMessage('demo-session-1');
    autoScaler.recordRequest('demo-session-1');
  }
  
  // Simulate messages on session 2 (low load)
  console.log('  - Sending 5 messages to session-2...');
  for (let i = 0; i < 5; i++) {
    autoScaler.recordMessage('demo-session-2');
    autoScaler.recordRequest('demo-session-2');
  }
  
  console.log('✓ Load simulated');
  console.log();
  
  // Show current status
  console.log('[5/5] Current Status:');
  console.log('-'.repeat(60));
  
  const status = autoScaler.getStatus();
  console.log('Active Sessions:', status.activeSessions);
  console.log('Total Scale Ups:', status.state.totalScaleUps);
  console.log('Total Scale Downs:', status.state.totalScaleDowns);
  console.log('Total Merges:', status.state.totalMerges);
  console.log();
  
  console.log('Session Metrics:');
  for (const session of status.sessions) {
    console.log(`  ${session.sessionId}:`);
    console.log(`    - Messages: ${session.messageCount}`);
    console.log(`    - Request Rate: ${session.requestRate.toFixed(2)}/min`);
    console.log(`    - Load Score: ${session.loadScore.toFixed(2)}`);
  }
  console.log();
  
  // Trigger manual check
  console.log('Triggering manual scaling check...');
  await autoScaler._checkAndScale();
  console.log('✓ Scaling check complete');
  console.log();
  
  // Show updated status
  console.log('Updated Status:');
  console.log('-'.repeat(60));
  const updatedStatus = autoScaler.getStatus();
  console.log('Active Sessions:', updatedStatus.activeSessions);
  console.log('Total Scale Ups:', updatedStatus.state.totalScaleUps);
  console.log('Total Scale Downs:', updatedStatus.state.totalScaleDowns);
  console.log('Total Merges:', updatedStatus.state.totalMerges);
  console.log();
  
  console.log('='.repeat(60));
  console.log('Demo Complete!');
  console.log('='.repeat(60));
  console.log();
  console.log('Next steps:');
  console.log('  1. Edit autoscaler-config.json to customize thresholds');
  console.log('  2. Integrate with your application:');
  console.log('     - Call recordMessage(sessionId) on each message');
  console.log('     - Call recordRequest(sessionId) on each request');
  console.log('  3. Monitor status with: node demo-autoscaler.js status');
  console.log('  4. Start auto-scaling: node start-autoscaler.js');
  console.log();
}

// Run demo
demo().catch(console.error);
