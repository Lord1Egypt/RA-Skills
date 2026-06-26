/**
 * Evolution Predictor
 * Predicts optimal next evolution actions based on history analysis
 * 
 * Features:
 * - Analyzes evolution history patterns
 * - Predicts optimal next actions
 * - Identifies high-value innovation opportunities
 * - Recommends gene selection based on context
 */

const fs = require('fs');
const path = require('path');

/**
 * Predict optimal next evolution action
 * @param {Object} options - Prediction options
 * @returns {Object} Prediction result
 */
function predictNextAction(options = {}) {
  const evolutionPath = options.evolutionPath || '/root/.openclaw/workspace/memory/evolution';
  const historyLimit = options.historyLimit || 30;
  
  const result = {
    timestamp: new Date().toISOString(),
    prediction: null,
    confidence: 0,
    reasoning: [],
    alternatives: [],
    metrics: {
      recentSuccessRate: 0,
      stagnationLevel: 0,
      innovationGap: 0
    }
  };
  
  try {
    // Read evolution state
    const statePath = path.join(evolutionPath, 'evolution_state.json');
    let cycleCount = 0;
    if (fs.existsSync(statePath)) {
      const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
      cycleCount = state.cycle_count || 0;
    }
    
    // Analyze recent GEP prompts
    const files = fs.readdirSync(evolutionPath)
      .filter(f => f.startsWith('gep_prompt_Cycle_') && f.endsWith('.txt'))
      .sort()
      .reverse()
      .slice(0, historyLimit);
    
    const signalCounts = {};
    const intentCounts = {};
    const geneCounts = {};
    const recentOutcomes = [];
    
    for (const file of files) {
      const filePath = path.join(evolutionPath, file);
      const content = fs.readFileSync(filePath, 'utf8');
      
      // Extract signals
      const signalsMatch = content.match(/Context \[Signals\]:\s*\n?\s*\[([^\]]+)\]/);
      if (signalsMatch) {
        const signals = signalsMatch[1].split(',').map(s => s.trim().replace(/"/g, ''));
        signals.forEach(signal => {
          signalCounts[signal] = (signalCounts[signal] || 0) + 1;
        });
      }
      
      // Extract intent
      const intentMatch = content.match(/Intent:\s*(\w+)/);
      if (intentMatch) {
        intentCounts[intentMatch[1]] = (intentCounts[intentMatch[1]] || 0) + 1;
      }
      
      // Extract gene used
      const geneMatch = content.match(/Selected Gene "([^"]+)"/);
      if (geneMatch) {
        geneCounts[geneMatch[1]] = (geneCounts[geneMatch[1]] || 0) + 1;
      }
      
      // Check outcome
      recentOutcomes.push(content.includes('SOLIDIFY] SUCCESS'));
    }
    
    // Calculate metrics
    const successCount = recentOutcomes.filter(o => o).length;
    result.metrics.recentSuccessRate = recentOutcomes.length > 0 
      ? Math.round((successCount / recentOutcomes.length) * 100) 
      : 0;
    
    // Calculate stagnation level
    const stagnationSignals = ['empty_cycle_loop_detected', 'stable_success_plateau', 
                               'evolution_saturation', 'force_steady_state'];
    let stagnationCount = 0;
    for (const signal of stagnationSignals) {
      if (signalCounts[signal]) stagnationCount += signalCounts[signal];
    }
    result.metrics.stagnationLevel = Math.min(100, Math.round((stagnationCount / files.length) * 25));
    
    // Calculate innovation gap
    const innovateCount = intentCounts['innovate'] || 0;
    const totalIntents = Object.values(intentCounts).reduce((a, b) => a + b, 0);
    result.metrics.innovationGap = totalIntents > 0 
      ? 100 - Math.round((innovateCount / totalIntents) * 100) 
      : 100;
    
    // Generate prediction
    if (result.metrics.stagnationLevel > 60) {
      result.prediction = {
        action: 'force_innovate',
        category: 'break_stagnation',
        priority: 'critical',
        description: 'Force innovation to break stagnation cycle',
        suggestedSkills: [
          'Create a novel skill that addresses an unmet need',
          'Implement cross-skill orchestration',
          'Add predictive capabilities'
        ]
      };
      result.confidence = 0.85;
      result.reasoning.push(`Stagnation level is high (${result.metrics.stagnationLevel}%)`);
      result.reasoning.push('Repeated signals indicate need for novel innovation');
    } else if (result.metrics.innovationGap > 70) {
      result.prediction = {
        action: 'prioritize_innovate',
        category: 'innovation',
        priority: 'high',
        description: 'Increase innovation rate to fill capability gaps',
        suggestedSkills: [
          'Analyze existing skills for enhancement opportunities',
          'Create complementary skills to existing ones',
          'Address user feature requests'
        ]
      };
      result.confidence = 0.75;
      result.reasoning.push(`Innovation gap is ${result.metrics.innovationGap}%`);
      result.reasoning.push('System has been optimizing/repairing more than innovating');
    } else if (result.metrics.recentSuccessRate > 90) {
      result.prediction = {
        action: 'explore_new_domains',
        category: 'expansion',
        priority: 'medium',
        description: 'System is stable, explore new capability domains',
        suggestedSkills: [
          'Create skills for new use cases',
          'Add integration capabilities',
          'Improve user experience'
        ]
      };
      result.confidence = 0.70;
      result.reasoning.push(`Success rate is high (${result.metrics.recentSuccessRate}%)`);
      result.reasoning.push('System is ready for expansion');
    } else {
      result.prediction = {
        action: 'stabilize',
        category: 'maintenance',
        priority: 'normal',
        description: 'Continue current evolution pattern',
        suggestedSkills: [
          'Monitor for emerging patterns',
          'Optimize existing skills',
          'Fix any remaining issues'
        ]
      };
      result.confidence = 0.65;
      result.reasoning.push('System is in normal operation mode');
    }
    
    // Generate alternatives
    const topGenes = Object.entries(geneCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3);
    
    for (const [gene, count] of topGenes) {
      if (gene !== (result.prediction.action === 'force_innovate' ? 'gene_gep_repair_from_errors' : gene)) {
        result.alternatives.push({
          gene,
          usageCount: count,
          reason: `Used ${count} times recently`
        });
      }
    }
    
  } catch (error) {
    result.error = error.message;
    result.prediction = {
      action: 'error_recovery',
      category: 'repair',
      priority: 'high',
      description: 'Error occurred during prediction, default to safe action'
    };
  }
  
  return result;
}

/**
 * Get recommended skill to create
 * @returns {Object} Skill recommendation
 */
function getRecommendedSkill() {
  const prediction = predictNextAction();
  
  const skillSuggestions = {
    force_innovate: [
      { name: 'cross-skill-orchestrator', description: 'Orchestrate multiple skills for complex tasks' },
      { name: 'pattern-learning-engine', description: 'Learn from successful operations' },
      { name: 'auto-recovery-system', description: 'Auto-recover from common failures' }
    ],
    prioritize_innovate: [
      { name: 'resource-optimizer', description: 'Optimize token and memory usage' },
      { name: 'context-compressor', description: 'Compress context for efficiency' },
      { name: 'skill-synthesizer', description: 'Synthesize new skills from patterns' }
    ],
    explore_new_domains: [
      { name: 'integration-bridge', description: 'Bridge to external services' },
      { name: 'user-feedback-analyzer', description: 'Analyze user feedback for improvements' },
      { name: 'proactive-suggestion-engine', description: 'Proactively suggest actions' }
    ],
    stabilize: [
      { name: 'health-check-runner', description: 'Run periodic health checks' },
      { name: 'log-aggregator', description: 'Aggregate and analyze logs' }
    ]
  };
  
  const suggestions = skillSuggestions[prediction.prediction.action] || skillSuggestions.stabilize;
  const selected = suggestions[Math.floor(Math.random() * suggestions.length)];
  
  return {
    ...selected,
    confidence: prediction.confidence,
    reasoning: prediction.reasoning
  };
}

/**
 * Format prediction report
 * @param {Object} prediction - Prediction result
 * @returns {string} Formatted report
 */
function formatReport(prediction) {
  const lines = [];
  
  lines.push('🔮 Evolution Prediction');
  lines.push('━'.repeat(50));
  lines.push(`Timestamp: ${prediction.timestamp}`);
  lines.push('');
  
  lines.push('📊 Metrics:');
  lines.push(`  Success Rate: ${prediction.metrics.recentSuccessRate}%`);
  lines.push(`  Stagnation Level: ${prediction.metrics.stagnationLevel}%`);
  lines.push(`  Innovation Gap: ${prediction.metrics.innovationGap}%`);
  lines.push('');
  
  if (prediction.prediction) {
    lines.push('🎯 Prediction:');
    lines.push(`  Action: ${prediction.prediction.action}`);
    lines.push(`  Category: ${prediction.prediction.category}`);
    lines.push(`  Priority: ${prediction.prediction.priority}`);
    lines.push(`  Description: ${prediction.prediction.description}`);
    lines.push(`  Confidence: ${Math.round(prediction.confidence * 100)}%`);
    lines.push('');
    
    if (prediction.prediction.suggestedSkills) {
      lines.push('💡 Suggested Skills:');
      prediction.prediction.suggestedSkills.forEach((s, i) => {
        lines.push(`  ${i + 1}. ${s}`);
      });
    }
  }
  
  if (prediction.reasoning.length > 0) {
    lines.push('');
    lines.push('📝 Reasoning:');
    prediction.reasoning.forEach(r => {
      lines.push(`  • ${r}`);
    });
  }
  
  return lines.join('\n');
}

/**
 * Main entry point
 */
async function main() {
  console.log('🔮 Evolution Predictor');
  console.log('======================\n');
  
  const prediction = predictNextAction();
  console.log(formatReport(prediction));
  
  console.log('\n📌 Recommended Skill:');
  const skill = getRecommendedSkill();
  console.log(`  Name: ${skill.name}`);
  console.log(`  Description: ${skill.description}`);
  
  return prediction;
}

module.exports = {
  predictNextAction,
  getRecommendedSkill,
  formatReport,
  main
};
