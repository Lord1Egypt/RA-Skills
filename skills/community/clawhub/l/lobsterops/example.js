// LobsterOps Usage Example
// ========================
//
// This example demonstrates basic usage of LobsterOps for AI agent observability.

const { LobsterOps } = require('./src/core/LobsterOps');

async function runExample() {
  console.log('🦞 LobsterOps Usage Example');
  console.log('====================');
  
  // Create a LobsterOps instance
  // Choose your storage backend:
  const ops = new LobsterOps({
    storageType: 'sqlite',           // Lightweight file-based SQL (great for Replit)
    storageConfig: {
      filename: './example-lobsterops.db' // SQLite database file
    },
    instanceId: 'example-agent-001' // Optional: custom instance ID
  });
  
  try {
    // Initialize LobsterOps and storage backend
    await ops.init();
    console.log('✅ LobsterOps initialized');
    
    // Show which storage backend is being used
    const stats = await ops.getStats();
    console.log(`📦 Using storage backend: ${stats.backend}`);
    
    // Simulate logging various AI agent events using specialized helpers
    console.log('\n📝 Logging AI agent events...');
    
    // 1. Agent startup/lifecycle event
    const lifecycleEventId = await ops.logLifecycle({
      agentId: 'research-agent-alpha',
      action: 'startup',
      status: 'healthy',
      version: '1.2.3',
      environment: 'production',
      host: 'replit-vm-42'
    });
    console.log(`   Lifecycle event logged: ${lifecycleEventId}`);
    
    // 2. Agent thought/reasoning
    const thoughtEventId = await ops.logThought({
      agentId: 'research-agent-alpha',
      thought: 'Looking at the sales data, I notice Q3 showed unexpected growth in the enterprise segment. This could be due to the new marketing campaign or seasonal factors.',
      context: 'Analyzing Q4 sales forecast',
      confidence: 0.8
    });
    console.log(`   Thought logged: ${thoughtEventId}`);
    
    // 3. Tool usage
    const toolEventId = await ops.logToolCall({
      agentId: 'research-agent-alpha',
      toolName: 'web-search',
      toolInput: { 
        query: 'enterprise sales growth Q3 2026 marketing campaign impact',
        maxResults: 10
      },
      toolOutput: { 
        results: [
          { title: 'Marketing Campaign ROI Analysis', url: 'https://example.com/roi' },
          { title: 'Q3 Enterprise Sales Report', url: 'https://example.com/sales-q3' }
        ],
        searchTimeMs: 850
      },
      durationMs: 900,
      success: true,
      cost: 0.002 // Example cost in USD
    });
    console.log(`   Tool call logged: ${toolEventId}`);
    
    // 4. Agent decision
    const decisionEventId = await ops.logDecision({
      agentId: 'research-agent-alpha',
      decision: 'Increase Q4 forecast for enterprise segment by 15%',
      confidence: 0.85,
      alternativesConsidered: [
        'Maintain current forecast',
        'Decrease forecast due to market uncertainty',
        'Request additional data collection'
      ],
      reasoning: 'Marketing campaign showing positive ROI and early indicators suggest sustained growth',
      dataSources: ['marketing-analytics', 'sales-crm', 'customer-surveys'],
      impact: 'high'
    });
    console.log(`   Decision logged: ${decisionEventId}`);
    
    // 5. Agent error (for demonstration)
    const errorEventId = await ops.logError({
      agentId: 'research-agent-alpha',
      errorType: 'APITimeoutError',
      errorMessage: 'Request to external analytics API timed out after 30 seconds',
      severity: 'medium',
      retryCount: 1,
      recovered: true,
      fallbackUsed: 'cached-data'
    });
    console.log(`   Error logged: ${errorEventId}`);
    
    // 6. Spawning a subagent
    const spawnEventId = await ops.logSpawning({
      parentAgentId: 'research-agent-alpha',
      childAgentId: 'data-analyst-agent-001',
      childAgentType: 'data-analysis',
      task: 'Analyze correlation between marketing spend and sales velocity',
      spawnReason: 'Specialized task requiring domain expertise'
    });
    console.log(`   Spawn event logged: ${spawnEventId}`);
    
    console.log('\n🔍 Querying and analyzing AI agent activity...');
    
    // Get complete trace of our agent's activity
    const agentTrace = await ops.getAgentTrace('research-agent-alpha');
    console.log(`   Agent trace contains ${agentTrace.length} events`);
    
    // Get recent thoughts specifically
    const recentThoughts = await ops.queryEvents({
      type: 'agent-thought',
      agentId: 'research-agent-alpha'
    });
    console.log(`   Found ${recentThoughts.length} recent thoughts`);
    
    // Get all tool calls
    const toolCalls = await ops.queryEvents({
      type: 'tool-call'
    });
    console.log(`   Found ${toolCalls.length} tool calls total`);
    
    // Get errors that need attention
    const errors = await ops.queryEvents({
      type: 'agent-error',
      severity: ['high', 'medium']
    });
    console.log(`   Found ${errors.length} errors requiring attention`);
    
    // Get a specific event by ID
    const specificEvent = await ops.getEvent(lifecycleEventId);
    if (specificEvent) {
      console.log(`\n🎯 Specific event details:`);
      console.log(`   Type: ${specificEvent.type}`);
      console.log(`   Agent: ${specificEvent.agentId}`);
      console.log(`   Action: ${specificEvent.action}`);
      console.log(`   Time: ${specificEvent.timestamp}`);
      if (specificEvent.thought) {
        console.log(`   Thought: ${specificEvent.thought.substring(0, 100)}...`);
      }
    }
    
    // Update an error event (mark as resolved)
    await ops.updateEvent(errorEventId, {
      resolved: true,
      resolutionTime: new Date().toISOString(),
      resolutionNotes: 'Increased API timeout to 60 seconds for analytics endpoint'
    });
    console.log(`\n🔄 Updated error event with resolution info`);
    
    // Get updated storage statistics
    const updatedStats = await ops.getStats();
    console.log(`\n📊 Storage Statistics:`);
    console.log(`   Backend: ${updatedStats.backend}`);
    console.log(`   Total Events: ${updatedStats.eventCount || updatedStats.totalEvents || 0}`);
    if (updatedStats.filename) {
      console.log(`   Database File: ${updatedStats.filename}`);
      console.log(`   Database Size: ${updatedStats.databaseSizeMB} MB`);
    }
    if (updatedStats.tableName) {
      console.log(`   Table Name: ${updatedStats.tableName}`);
    }
    console.log(`   Instance ID: ${updatedStats.instanceId}`);
    
    console.log(`\n✅ Example completed successfully!`);
    console.log(`💡 Try checking the './example-lobsterops.db' SQLite database file.`);
    console.log(`🔬 LobsterOps is now ready for AI agent observability in your projects!`);
    
  } catch (error) {
    console.error('❌ Example failed:', error);
  } finally {
    // Always cleanup resources
    await ops.close();
    console.log('🔚 LobsterOps closed');
  }
}

// Run the example if this file is executed directly
if (require.main === module) {
  runExample().catch(console.error);
}

module.exports = { runExample };