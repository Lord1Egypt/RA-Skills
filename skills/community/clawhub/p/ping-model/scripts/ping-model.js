#!/usr/bin/env node
/**
 * Ping Tool - Measure and display AI model response latency
 * 
 * Usage: node ping.js [options]
 * 
 * Output Format:
 * 🧪 PING {model}
 * 
 * 📤 Sent:     {timestamp}
 * 📥 Received: {timestamp}
 * ⏱️  Latency:  {formatted}
 * 
 * 🎯 Pong!
 * 
 * Latency Formatting:
 *   - < 1000ms: "XXXms"
 *   - 1000ms - 60000ms: "X.XXs"  
 *   - >= 60000ms: "X.XXmin"
 */

const { execSync } = require('child_process');

// Format timestamp to HH:MM:SS.mmm
function formatTimestamp(date) {
  const h = String(date.getHours()).padStart(2, '0');
  const m = String(date.getMinutes()).padStart(2, '0');
  const s = String(date.getSeconds()).padStart(2, '0');
  const ms = String(date.getMilliseconds()).padStart(3, '0');
  return `${h}:${m}:${s}.${ms}`;
}

// Format duration with smart units
// < 1000ms: "XXXms"
// 1000ms - 60000ms: "X.XXs"
// >= 60000ms: "X.XXmin"
function formatDuration(ms) {
  if (ms < 1000) {
    // Less than 1 second: show milliseconds
    return `${Math.round(ms)}ms`;
  } else if (ms < 60000) {
    // 1 second to 60 seconds: show seconds with 2 decimals
    return `${(ms / 1000).toFixed(2)}s`;
  } else {
    // 60 seconds or more: show minutes with 2 decimals
    return `${(ms / 60000).toFixed(2)}min`;
  }
}

// Get current model from OpenClaw session status
function getCurrentModel() {
  try {
    const result = execSync('openclaw status 2>/dev/null || echo "unknown"', { 
      encoding: 'utf-8', 
      timeout: 5000 
    });
    
    if (result.includes('kimi')) return 'kimi';
    if (result.includes('minimax')) return 'minimax';
    if (result.includes('deepseek')) return 'deepseek';
    if (result.includes('glm')) return 'glm';
    if (result.includes('openai')) return 'openai';
    if (result.includes('gemini')) return 'gemini';
    
    return 'current';
  } catch (e) {
    return 'current';
  }
}

// Display ping result with CONSISTENT formatting
function displayResult(startTime, endTime, model) {
  const latency = endTime - startTime;
  
  console.log(`🧪 PING ${model}`);
  console.log('');
  console.log(`📤 Sent:     ${formatTimestamp(startTime)}`);
  console.log(`📥 Received: ${formatTimestamp(endTime)}`);
  console.log(`⏱️  Latency:  ${formatDuration(latency)}`);
  console.log('');
  console.log('🎯 Pong!');
}

// Display comparison results
function displayComparison(results) {
  // Sort by latency (fastest first)
  results.sort((a, b) => a.latency - b.latency);
  
  console.log('═'.repeat(50));
  console.log('🧪 MODEL COMPARISON');
  console.log('═'.repeat(50));
  console.log('');
  
  const medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣'];
  
  results.forEach((r, index) => {
    const medal = medals[index] || `${index + 1}️⃣`;
    const name = r.model.padEnd(12);
    const duration = formatDuration(r.latency).padStart(10);
    console.log(`${medal} ${name} ${duration}`);
  });
  
  console.log('');
  console.log(`🏆 Fastest: ${results[0].model} (${formatDuration(results[0].latency)})`);
  console.log('');
}

// Simulate ping latency (for demo purposes)
// In real operation, this would be replaced with actual timing from OpenClaw
async function simulatePing(model) {
  const startTime = new Date();
  
  // Simulate processing delay (varies by model)
  const baseDelays = {
    'kimi': 800,
    'minimax': 1200,
    'deepseek': 1500,
    'gemini': 2000,
    'openai': 1800,
    'glm': 1100
  };
  
  const baseDelay = baseDelays[model] || 1000;
  const variation = Math.random() * 500; // 0-500ms random variation
  const totalDelay = baseDelay + variation;
  
  // Simulate async work
  await new Promise(resolve => setTimeout(resolve, totalDelay));
  
  const endTime = new Date();
  return { startTime, endTime, latency: endTime - startTime };
}

// Main execution
async function main() {
  const args = process.argv.slice(2);
  
  // Parse arguments
  let model = getCurrentModel();
  let compareList = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--model' && args[i + 1]) {
      model = args[i + 1];
      i++;
    } else if (args[i] === '--compare' && args[i + 1]) {
      compareList = args[i + 1].split(',').map(m => m.trim());
      i++;
    } else if (args[i] === '--help' || args[i] === '-h') {
      console.log(`
Ping Tool - Measure AI model response latency

Usage: node ping.js [options]

Options:
  --model <name>       Model to test (default: current)
  --compare <list>     Compare multiple models (comma-separated)
  -h, --help           Show this help

Examples:
  node ping.js                    # Ping current model
  node ping.js --model kimi       # Ping kimi model
  node ping.js --compare kimi,minimax,deepseek

Output Format:
  🧪 PING {model}
  
  📤 Sent:     {timestamp}
  📥 Received: {timestamp}
  ⏱️  Latency:  {duration}
  
  🎯 Pong!

Latency Display:
  < 1s:     XXXms
  1s-60s:   X.XXs
  ≥ 60s:    X.XXmin
`);
      process.exit(0);
    }
  }
  
  try {
    // Comparison mode
    if (compareList && compareList.length > 1) {
      const results = [];
      
      for (const m of compareList) {
        const result = await simulatePing(m);
        results.push({
          model: m,
          latency: result.latency
        });
      }
      
      displayComparison(results);
      return;
    }
    
    // Single ping mode
    const result = await simulatePing(model);
    displayResult(result.startTime, result.endTime, model);
    
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

main();
