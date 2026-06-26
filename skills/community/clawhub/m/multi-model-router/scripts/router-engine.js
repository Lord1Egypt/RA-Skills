class RouterEngine {
  constructor(config) {
    this.config = config || this.getDefaultConfig();
  }

  getDefaultConfig() {
    return {
      models: {
        high_context: {
          alias: "xinliu/qwen3-max",
          context_window: 256000,
          privacy_level: "cloud",
          cost_per_1k_input: 0,
          cost_per_1k_output: 0,
          priority: 1
        },
        balanced: {
          alias: "xinliu/kimi-k2-0905",
          context_window: 256000,
          privacy_level: "cloud", 
          cost_per_1k_input: 0,
          cost_per_1k_output: 0,
          priority: 2
        },
        offline: {
          alias: "ollama/qwen35-32k",
          context_window: 32768,
          privacy_level: "local",
          cost_per_1k_input: 0,
          cost_per_1k_output: 0,
          priority: 3
        }
      },
      routing_rules: {
        privacy_sensitive: ["offline"],
        context_length_gt_32k: ["high_context", "balanced"],
        context_length_le_32k: ["offline", "high_context", "balanced"],
        cost_optimization: ["offline", "balanced", "high_context"],
        performance_critical: ["high_context", "balanced", "offline"]
      },
      fallback_strategy: "high_context"
    };
  }

  selectModel(analysis, userPreferences = {}) {
    let candidates = Object.keys(this.config.models);
    
    // Apply privacy rules first (highest priority)
    if (analysis.privacyLevel === 'high') {
      candidates = this.applyPrivacyFilter(candidates);
    }
    
    // Apply context length rules
    if (analysis.contextLength > 32768) {
      candidates = this.applyContextFilter(candidates, analysis.contextLength);
    }
    
    // Apply cost optimization if requested
    if (analysis.costSensitivity || userPreferences.costSensitive) {
      candidates = this.applyCostOptimization(candidates);
    }
    
    // Apply performance priority if requested  
    if (analysis.performanceCritical || userPreferences.performanceCritical) {
      candidates = this.applyPerformancePriority(candidates);
    }
    
    // Return the best candidate based on priority
    return this.selectBestCandidate(candidates);
  }
  
  applyPrivacyFilter(candidates) {
    return candidates.filter(model => 
      this.config.models[model].privacy_level === 'local'
    );
  }
  
  applyContextFilter(candidates, requiredContextLength) {
    return candidates.filter(model => 
      this.config.models[model].context_window >= requiredContextLength
    );
  }
  
  applyCostOptimization(candidates) {
    // Sort by cost (local models first, then by configured cost)
    return candidates.sort((a, b) => {
      const modelA = this.config.models[a];
      const modelB = this.config.models[b];
      
      // Local models are always cheaper
      if (modelA.privacy_level === 'local' && modelB.privacy_level !== 'local') {
        return -1;
      }
      if (modelA.privacy_level !== 'local' && modelB.privacy_level === 'local') {
        return 1;
      }
      
      // Compare costs
      const costA = modelA.cost_per_1k_input + modelA.cost_per_1k_output;
      const costB = modelB.cost_per_1k_input + modelB.cost_per_1k_output;
      
      if (costA === costB) {
        return modelA.priority - modelB.priority; // Use priority as tiebreaker
      }
      return costA - costB;
    });
  }
  
  applyPerformancePriority(candidates) {
    // Sort by priority (lower number = higher priority)
    return candidates.sort((a, b) => 
      this.config.models[a].priority - this.config.models[b].priority
    );
  }
  
  selectBestCandidate(candidates) {
    if (candidates.length === 0) {
      console.warn("No suitable models found, using fallback");
      return this.config.fallback_strategy;
    }
    return candidates[0]; // Return highest priority candidate
  }
}

module.exports = RouterEngine;