/**
 * Session Persistence Tests
 * 
 * Tests for:
 * 1. Save session state to disk
 * 2. Auto-recovery on restart
 * 3. State migration (active → hibernating → archived)
 */

const fs = require('fs');
const path = require('path');
const { SessionPersistenceManager, SessionState } = require('./session-manager');

// Test configuration
const TEST_DIR = path.join(__dirname, 'test-data');
const STATE_FILE = path.join(TEST_DIR, 'test-session-state.json');
const SESSIONS_DIR = path.join(TEST_DIR, 'sessions');
const ARCHIVE_DIR = path.join(TEST_DIR, 'archive');

let testManager = null;
let testsPassed = 0;
let testsFailed = 0;

/**
 * Setup test environment
 */
async function setup() {
  console.log('\n=== Setting up test environment ===\n');
  
  // Clean test directory
  if (fs.existsSync(TEST_DIR)) {
    fs.rmSync(TEST_DIR, { recursive: true });
  }
  fs.mkdirSync(TEST_DIR, { recursive: true });
  
  // Create test manager with custom paths
  testManager = new SessionPersistenceManager();
  testManager.stateFile = STATE_FILE;
  testManager.sessionsDir = SESSIONS_DIR;
  testManager.archiveDir = ARCHIVE_DIR;
  
  // Faster timeouts for testing
  testManager.hibernationTimeout = 2 * 1000; // 2 seconds
  testManager.archiveTimeout = 4 * 1000; // 4 seconds
  
  await testManager.initialize();
  console.log('Test environment ready\n');
}

/**
 * Cleanup test environment
 */
function cleanup() {
  console.log('\n=== Cleaning up ===\n');
  if (fs.existsSync(TEST_DIR)) {
    fs.rmSync(TEST_DIR, { recursive: true });
  }
}

/**
 * Assert helper
 */
function assert(condition, message) {
  if (condition) {
    console.log('✓', message);
    testsPassed++;
  } else {
    console.error('✗', message);
    testsFailed++;
  }
}

/**
 * Test 1: Create and save session
 */
async function testCreateSession() {
  console.log('\n--- Test 1: Create and Save Session ---');
  
  const sessionId = 'test-session-1';
  const session = await testManager.createSession(sessionId, 'user-123', 'feishu');
  
  assert(session !== null, 'Session created');
  assert(session.id === sessionId, 'Session ID matches');
  assert(session.userId === 'user-123', 'User ID matches');
  assert(session.channel === 'feishu', 'Channel matches');
  assert(session.state === SessionState.ACTIVE, 'Initial state is ACTIVE');
  
  // Check state file exists
  assert(fs.existsSync(STATE_FILE), 'State file created on disk');
  
  // Check session directory exists
  const sessionDir = path.join(SESSIONS_DIR, sessionId);
  assert(fs.existsSync(sessionDir), 'Session directory created');
  
  // Verify state can be loaded
  const savedState = JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
  assert(savedState.sessions.length === 1, 'Session saved in state file');
  assert(savedState.sessions[0].id === sessionId, 'Session ID in state file matches');
  
  console.log('Test 1 complete');
}

/**
 * Test 2: Session context persistence
 */
async function testSessionContext() {
  console.log('\n--- Test 2: Session Context Persistence ---');
  
  const sessionId = 'test-session-2';
  await testManager.createSession(sessionId, 'user-456', 'feishu');
  
  // Set context
  await testManager.setSessionContext(sessionId, 'userMd', '# Test User\n\nHello');
  await testManager.setSessionContext(sessionId, 'customData', { key: 'value' });
  await testManager.setSessionVariable(sessionId, 'counter', 42);
  
  // Verify context saved
  const session = testManager.getSession(sessionId);
  assert(session.context.userMd === '# Test User\n\nHello', 'Context userMd saved');
  assert(session.context.customData.key === 'value', 'Context customData saved');
  assert(session.variables.counter === 42, 'Variable saved');
  
  // Verify files on disk
  const contextPath = path.join(SESSIONS_DIR, sessionId, 'context.json');
  assert(fs.existsSync(contextPath), 'Context file created');
  
  const contextData = JSON.parse(fs.readFileSync(contextPath, 'utf-8'));
  assert(contextData.userMd === '# Test User\n\nHello', 'Context file content matches');
  
  const userMdPath = path.join(SESSIONS_DIR, sessionId, 'user.md');
  assert(fs.existsSync(userMdPath), 'User.md file created');
  
  console.log('Test 2 complete');
}

/**
 * Test 3: Session recovery after restart
 */
async function testSessionRecovery() {
  console.log('\n--- Test 3: Session Recovery After Restart ---');
  
  const sessionId = 'test-session-3';
  await testManager.createSession(sessionId, 'user-789', 'feishu');
  await testManager.setSessionContext(sessionId, 'testData', 'recovery-test');
  
  // Simulate restart: create new manager and initialize
  const newManager = new SessionPersistenceManager();
  newManager.stateFile = STATE_FILE;
  newManager.sessionsDir = SESSIONS_DIR;
  newManager.archiveDir = ARCHIVE_DIR;
  newManager.hibernationTimeout = 2 * 1000;
  newManager.archiveTimeout = 4 * 1000;
  
  await newManager.initialize();
  
  const recoveredSession = newManager.getSession(sessionId);
  assert(recoveredSession !== null, 'Session recovered after restart');
  assert(recoveredSession.userId === 'user-789', 'User ID recovered');
  assert(recoveredSession.context.testData === 'recovery-test', 'Context recovered');
  assert(recoveredSession.metadata.recovered === true, 'Recovery flag set');
  
  console.log('Test 3 complete');
}

/**
 * Test 4: State migration (active → hibernating)
 */
async function testHibernation() {
  console.log('\n--- Test 4: State Migration (Active → Hibernating) ---');
  
  const sessionId = 'test-session-4';
  await testManager.createSession(sessionId, 'user-hibernate', 'feishu');
  
  // Manually set last activity to past
  const session = testManager.getSession(sessionId);
  session.lastActivityAt = Date.now() - (3 * 1000); // 3 seconds ago
  
  // Wait for migration checker (runs every 60 seconds, but we check every minute)
  // For testing, we manually trigger the migration logic
  await new Promise(resolve => setTimeout(resolve, 100));
  
  // Manually check migration (simulating the checker)
  const now = Date.now();
  for (const [sid, sess] of testManager.sessions) {
    if (sess.state === SessionState.ACTIVE) {
      const inactiveTime = now - sess.lastActivityAt;
      if (inactiveTime > testManager.hibernationTimeout) {
        await testManager.hibernateSession(sid);
      }
    }
  }
  
  const updatedSession = testManager.getSession(sessionId);
  assert(updatedSession.state === SessionState.HIBERNATING, 'Session hibernated');
  assert(updatedSession.hibernatedAt !== null, 'Hibernated timestamp set');
  
  console.log('Test 4 complete');
}

/**
 * Test 5: State migration (hibernating → archived)
 */
async function testArchival() {
  console.log('\n--- Test 5: State Migration (Hibernating → Archived) ---');
  
  const sessionId = 'test-session-5';
  await testManager.createSession(sessionId, 'user-archive', 'feishu');
  
  // Manually set to hibernating with old timestamp
  const session = testManager.getSession(sessionId);
  session.state = SessionState.HIBERNATING;
  session.hibernatedAt = Date.now() - (5 * 1000); // 5 seconds ago
  
  // Manually trigger migration (simulating the checker)
  const now = Date.now();
  for (const [sid, sess] of testManager.sessions) {
    if (sess.state === SessionState.HIBERNATING) {
      const hibernatingTime = now - sess.hibernatedAt;
      if (hibernatingTime > testManager.archiveTimeout) {
        await testManager.archiveSession(sid);
      }
    }
  }
  
  // Session should be archived (state changed to ARCHIVED)
  const archivedSession = testManager.getSession(sessionId);
  assert(archivedSession !== undefined, 'Session remains in manager for audit trail');
  assert(archivedSession.state === SessionState.ARCHIVED, 'Session state is ARCHIVED');
  
  // Check archive directory
  const archivePath = path.join(ARCHIVE_DIR, sessionId);
  assert(fs.existsSync(archivePath), 'Session directory moved to archive');
  
  // Check state file
  const savedState = JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
  const archivedInState = savedState.sessions.find(s => s.id === sessionId);
  assert(archivedInState !== undefined, 'Archived session in state file');
  assert(archivedInState.state === SessionState.ARCHIVED, 'State is ARCHIVED');
  assert(archivedInState.archivedAt !== null, 'Archived timestamp set');
  
  console.log('Test 5 complete');
}

/**
 * Test 6: Session touch (activity update)
 */
async function testSessionTouch() {
  console.log('\n--- Test 6: Session Touch (Activity Update) ---');
  
  const sessionId = 'test-session-6';
  await testManager.createSession(sessionId, 'user-touch', 'feishu');
  
  const session = testManager.getSession(sessionId);
  const oldActivity = session.lastActivityAt;
  const oldCount = session.messageCount;
  
  // Wait a bit
  await new Promise(resolve => setTimeout(resolve, 100));
  
  // Touch session
  await testManager.touchSession(sessionId);
  
  const updatedSession = testManager.getSession(sessionId);
  assert(updatedSession.lastActivityAt > oldActivity, 'Activity timestamp updated');
  assert(updatedSession.messageCount === oldCount + 1, 'Message count incremented');
  
  console.log('Test 6 complete');
}

/**
 * Test 7: Wake up hibernating session
 */
async function testWakeUp() {
  console.log('\n--- Test 7: Wake Up Hibernating Session ---');
  
  const sessionId = 'test-session-7';
  await testManager.createSession(sessionId, 'user-wakeup', 'feishu');
  
  // Manually hibernate
  const session = testManager.getSession(sessionId);
  session.state = SessionState.HIBERNATING;
  session.hibernatedAt = Date.now();
  
  // Touch to wake up
  await testManager.touchSession(sessionId);
  
  const updatedSession = testManager.getSession(sessionId);
  assert(updatedSession.state === SessionState.ACTIVE, 'Session awakened to ACTIVE');
  assert(updatedSession.hibernatedAt === null, 'Hibernated timestamp cleared');
  
  console.log('Test 7 complete');
}

/**
 * Test 8: Session statistics
 */
async function testStatistics() {
  console.log('\n--- Test 8: Session Statistics ---');
  
  const stats = testManager.getStats();
  
  assert(typeof stats.total === 'number', 'Total count exists');
  assert(typeof stats.active === 'number', 'Active count exists');
  assert(typeof stats.hibernating === 'number', 'Hibernating count exists');
  assert(typeof stats.archived === 'number', 'Archived count exists');
  
  console.log('Stats:', stats);
  console.log('Test 8 complete');
}

/**
 * Test 9: Export sessions
 */
async function testExport() {
  console.log('\n--- Test 9: Export Sessions ---');
  
  const exportPath = await testManager.exportSessions();
  
  assert(fs.existsSync(exportPath), 'Export file created');
  
  const exportData = JSON.parse(fs.readFileSync(exportPath, 'utf-8'));
  assert(exportData.version === 1, 'Export version correct');
  assert(Array.isArray(exportData.sessions), 'Sessions array exists');
  assert(exportData.exportedAt !== null, 'Export timestamp set');
  
  // Cleanup export file
  fs.unlinkSync(exportPath);
  
  console.log('Test 9 complete');
}

/**
 * Run all tests
 */
async function runTests() {
  console.log('╔════════════════════════════════════════╗');
  console.log('║   Session Persistence Test Suite      ║');
  console.log('╚════════════════════════════════════════╝');
  
  try {
    await setup();
    
    await testCreateSession();
    await testSessionContext();
    await testSessionRecovery();
    await testHibernation();
    await testArchival();
    await testSessionTouch();
    await testWakeUp();
    await testStatistics();
    await testExport();
    
    console.log('\n╔════════════════════════════════════════╗');
    console.log('║            Test Results              ║');
    console.log('╚════════════════════════════════════════╝');
    console.log(`Passed: ${testsPassed}`);
    console.log(`Failed: ${testsFailed}`);
    console.log(`Total:  ${testsPassed + testsFailed}`);
    
    if (testsFailed === 0) {
      console.log('\n✓ All tests passed!\n');
    } else {
      console.error('\n✗ Some tests failed!\n');
      process.exit(1);
    }
  } catch (error) {
    console.error('\n✗ Test suite error:', error);
    process.exit(1);
  } finally {
    cleanup();
  }
}

// Run tests
runTests();
