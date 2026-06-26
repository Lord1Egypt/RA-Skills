#!/usr/bin/env node

const { MemoryLCM } = require('../src/index.js');

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];
  
  const sessionKey = args[1] || 'default';
  const lcm = new MemoryLCM(sessionKey);
  await lcm.init();
  
  switch (cmd) {
    case 'status': {
      const s = lcm.status();
      console.log('📊 Tony LCM Status');
      console.log(`   Total messages: ${s.total}`);
      console.log(`   Active (uncompacted): ${s.active}`);
      console.log(`   Sessions: ${s.sessions}`);
      console.log(`   Chunk summaries: ${s.summaries}`);
      break;
    }
    
    case 'search': {
      const query = args.slice(2).join(' ');
      if (!query) { console.error('Usage: tony-lcm search <query>'); process.exit(1); }
      const results = lcm.search(query);
      if (!results.length) { console.log('No results found.'); break; }
      results.forEach(r => {
        console.log(`[${r.timestamp}] ${r.role}: ${r.content.substring(0, 150)}...`);
        console.log('---');
      });
      break;
    }
    
    case 'recall': {
      const topic = args.slice(2).join(' ');
      const days = parseInt(args[args.length - 1]) || 7;
      if (!topic) { console.error('Usage: tony-lcm recall <topic> [days]'); process.exit(1); }
      const results = lcm.recall(topic, days);
      if (!results.length) { console.log('No results found.'); break; }
      results.forEach(r => {
        console.log(`[${r.created_at}] (${r.message_count} msgs):`);
        console.log(r.summary.substring(0, 200) + '...');
        console.log('---');
      });
      break;
    }
    
    case 'compact': {
      const result = lcm.compact();
      console.log('✅ Compacted:', result.compacted, 'messages');
      console.log('   Decisions extracted:', result.decisions);
      console.log('   Summaries created:', result.summaries);
      break;
    }
    
    case 'daily': {
      const result = lcm.daily();
      console.log('✅ Daily summary:', result.daily, 'messages processed');
      console.log('   Decisions synced:', result.decisions);
      break;
    }
    
    case 'sync': {
      // Sync decisions from recent uncompacted messages
      const messages = require('../src/messages').getUncompactedMessages(sessionKey, 50);
      const text = messages.map(m => m.content).join('\n');
      const { extractDecisions, syncToMemory } = require('../src/memory-sync');
      const decisions = extractDecisions(text);
      const today = new Date().toISOString().split('T')[0];
      const count = syncToMemory(today, decisions);
      console.log('✅ Synced', count, 'decisions to MEMORY.md');
      break;
    }
    
    default: {
      console.log('Tony LCM - Lossless Context Manager for OpenClaw');
      console.log('');
      console.log('Usage:');
      console.log('  tony-lcm status              # Show DB stats');
      console.log('  tony-lcm search <query>      # Search history');
      console.log('  tony-lcm recall <topic> [d] # Recall topic from last d days (default 7)');
      console.log('  tony-lcm compact             # Compact messages into summaries');
      console.log('  tony-lcm daily               # Generate daily summary');
      console.log('  tony-lcm sync                # Sync decisions to MEMORY.md');
      console.log('');
      console.log('All data stored in: ~/.openclaw/workspace/data/tony-lcm.db');
    }
  }
  
  process.exit(0);
}

main().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
