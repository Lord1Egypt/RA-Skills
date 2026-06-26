/**
 * Session Persistence Integration Example
 * 
 * This file shows how to integrate the session persistence module
 * into the OpenClaw main application
 */

const { getSessionManager, SessionState } = require('./session-manager');

/**
 * Example: Integrating into OpenClaw's main application
 */
class OpenClawApp {
  constructor() {
    this.sessionManager = getSessionManager();
    this.initialized = false;
  }
  
  /**
   * Initialize the application with session persistence
   */
  async initialize() {
    console.log('[OpenClaw] Initializing...');
    
    // Initialize session manager (loads existing sessions from disk)
    const success = await this.sessionManager.initialize();
    
    if (success) {
      this.initialized = true;
      console.log('[OpenClaw] Session persistence enabled');
      
      // Log recovered sessions
      const recoveredSessions = this.sessionManager.getActiveSessions()
        .filter(s => s.metadata.recovered);
      
      if (recoveredSessions.length > 0) {
        console.log(`[OpenClaw] Recovered ${recoveredSessions.length} sessions from previous run`);
        for (const session of recoveredSessions) {
          console.log(`  - ${session.id} (user: ${session.userId}, channel: ${session.channel})`);
        }
      }
    } else {
      console.error('[OpenClaw] Failed to initialize session persistence');
    }
    
    return success;
  }
  
  /**
   * Handle incoming message
   * @param {string} sessionId - Session ID
   * @param {string} userId - User ID
   * @param {string} channel - Channel type
   * @param {string} message - Message content
   */
  async handleMessage(sessionId, userId, channel, message) {
    // Get or create session
    let session = this.sessionManager.getSession(sessionId);
    
    if (!session) {
      console.log(`[OpenClaw] Creating new session: ${sessionId}`);
      session = await this.sessionManager.createSession(sessionId, userId, channel);
      
      // Initialize session with user context if available
      // This would typically load from your user database
      await this.sessionManager.setSessionContext(sessionId, 'userId', userId);
    }
    
    // Update session activity (also wakes up hibernating sessions)
    await this.sessionManager.touchSession(sessionId);
    
    // Increment message count
    await this.sessionManager.setSessionVariable(sessionId, 'totalMessages', session.messageCount);
    
    console.log(`[OpenClaw] Message in session ${sessionId} (${session.state})`);
    
    // Process the message...
    // Your message handling logic here
    
    return session;
  }
  
  /**
   * Get session info for a specific user
   */
  getSessionInfo(sessionId) {
    const session = this.sessionManager.getSession(sessionId);
    
    if (!session) {
      return null;
    }
    
    return {
      id: session.id,
      userId: session.userId,
      channel: session.channel,
      state: session.state,
      createdAt: new Date(session.createdAt).toISOString(),
      lastActivityAt: new Date(session.lastActivityAt).toISOString(),
      messageCount: session.messageCount,
      context: session.context,
      variables: session.variables
    };
  }
  
  /**
   * Get dashboard statistics
   */
  getDashboardStats() {
    const stats = this.sessionManager.getStats();
    const activeSessions = this.sessionManager.getActiveSessions();
    
    return {
      ...stats,
      activeSessionList: activeSessions.map(s => ({
        id: s.id,
        userId: s.userId,
        channel: s.channel,
        messageCount: s.messageCount
      })),
      uptime: process.uptime()
    };
  }
  
  /**
   * Graceful shutdown
   */
  async shutdown() {
    console.log('[OpenClaw] Shutting down...');
    
    // Save all session states
    await this.sessionManager._saveState();
    
    console.log('[OpenClaw] Session states saved');
    console.log('[OpenClaw] Goodbye!');
  }
}

/**
 * Example usage
 */
async function main() {
  const app = new OpenClawApp();
  
  // Initialize
  await app.initialize();
  
  // Simulate handling messages
  console.log('\n--- Simulating Messages ---\n');
  
  await app.handleMessage('session-001', 'user-alice', 'feishu', 'Hello!');
  await app.handleMessage('session-001', 'user-alice', 'feishu', 'How are you?');
  await app.handleMessage('session-002', 'user-bob', 'feishu', 'Hi there!');
  
  // Show session info
  console.log('\n--- Session Info ---\n');
  const info = app.getSessionInfo('session-001');
  console.log(JSON.stringify(info, null, 2));
  
  // Show dashboard stats
  console.log('\n--- Dashboard Stats ---\n');
  const stats = app.getDashboardStats();
  console.log(JSON.stringify(stats, null, 2));
  
  // Shutdown
  await app.shutdown();
}

// Handle process signals for graceful shutdown
process.on('SIGINT', async () => {
  const app = new OpenClawApp();
  await app.shutdown();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  const app = new OpenClawApp();
  await app.shutdown();
  process.exit(0);
});

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { OpenClawApp };
