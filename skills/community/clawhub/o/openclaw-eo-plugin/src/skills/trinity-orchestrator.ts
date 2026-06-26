// ============================================================================
// EO Trinity Orchestrator - Phase 5.2: Technical Fusion
//
// Integrates three major systems:
// - OpenClaw: Control layer (session management, routing, tools)
// - Hermes: Execution layer (auto-skill generation, organic growth)
// - Claude Code: Coding execution (code generation, refactoring, execution)
//
// Creates a unified "super agent" architecture.
// ============================================================================

import { AgentCoordinator } from '../autonomy/agent-coordinator.js'
import { skillGenerator, SkillGenerator } from './skill-generator.js'

// ============================================================================
// Types
// ============================================================================

export type TrinityLayer = 'openclaw' | 'hermes' | 'claude_code'

export interface TrinityConfig {
  enableOpenClaw: boolean
  enableHermes: boolean
  enableClaudeCode: boolean
  defaultLayer: TrinityLayer
  layerRouting: 'auto' | 'manual' | 'hybrid'
  maxConcurrentLayers: number
}

export interface TrinityTask {
  id: string
  description: string
  type: 'planning' | 'coding' | 'review' | 'research' | 'management' | 'general'
  preferredLayer?: TrinityLayer
  requiredCapabilities: string[]
  context: any
}

export interface TrinityResult {
  taskId: string
  success: boolean
  primaryLayer: TrinityLayer
  layerResults: Map<TrinityLayer, LayerResult>
  fusedOutput: string
  confidence: number
  executionTimeMs: number
}

export interface LayerResult {
  layer: TrinityLayer
  success: boolean
  output?: string
  error?: string
  confidence: number
  capabilities: string[]
  metadata?: Record<string, any>
}

export interface RoutingDecision {
  recommendedLayer: TrinityLayer
  reasoning: string
  alternativeLayers: TrinityLayer[]
  confidence: number
}

// ============================================================================
// Capability Registry
// ============================================================================

class CapabilityRegistry {
  private capabilities: Map<TrinityLayer, Set<string>> = new Map([
    ['openclaw', new Set(['session_management', 'tool_routing', 'memory', 'multi_agent', 'hooks', 'skills'])],
    ['hermes', new Set(['auto_skill_gen', 'organic_growth', 'user_interaction', 'multi_platform', 'learning'])],
    ['claude_code', new Set(['code_generation', 'refactoring', 'execution', 'debugging', 'file_ops', 'git_ops'])],
  ])
  
  private layerStrengths: Map<TrinityLayer, Map<string, number>> = new Map([
    ['openclaw', new Map([
      ['multi_agent', 0.95],
      ['memory', 0.9],
      ['session_management', 0.95],
      ['tool_routing', 0.85],
    ])],
    ['hermes', new Map([
      ['auto_skill_gen', 0.9],
      ['organic_growth', 0.85],
      ['user_interaction', 0.9],
    ])],
    ['claude_code', new Map([
      ['code_generation', 0.98],
      ['refactoring', 0.95],
      ['execution', 0.95],
      ['debugging', 0.9],
    ])],
  ])
  
  /**
   * Check if a layer has a specific capability.
   */
  hasCapability(layer: TrinityLayer, capability: string): boolean {
    return this.capabilities.get(layer)?.has(capability) ?? false
  }
  
  /**
   * Get all capabilities of a layer.
   */
  getCapabilities(layer: TrinityLayer): string[] {
    return Array.from(this.capabilities.get(layer) || [])
  }
  
  /**
   * Get all capabilities from all layers.
   */
  getAllCapabilitiesMap(): Map<TrinityLayer, Set<string>> {
    return this.capabilities
  }
  
  /**
   * Get the strength of a layer for a specific capability.
   */
  getStrength(layer: TrinityLayer, capability: string): number {
    return this.layerStrengths.get(layer)?.get(capability) ?? 0.5
  }
  
  /**
   * Find the best layer for a set of required capabilities.
   */
  findBestLayer(requiredCapabilities: string[]): { layer: TrinityLayer; score: number } {
    const scores: Map<TrinityLayer, number> = new Map()
    
    for (const layer of ['openclaw', 'hermes', 'claude_code'] as TrinityLayer[]) {
      let totalScore = 0
      let capabilityCount = 0
      
      for (const cap of requiredCapabilities) {
        if (this.hasCapability(layer, cap)) {
          totalScore += this.getStrength(layer, cap)
          capabilityCount++
        }
      }
      
      // Normalize by required capabilities
      scores.set(layer, capabilityCount > 0 ? totalScore / requiredCapabilities.length : 0)
    }
    
    // Find best
    let bestLayer: TrinityLayer = 'openclaw'
    let bestScore = 0
    
    scores.forEach((score, layer) => {
      if (score > bestScore) {
        bestScore = score
        bestLayer = layer
      }
    })
    
    return { layer: bestLayer, score: bestScore }
  }
}

// ============================================================================
// Trinity Orchestrator (Main Class)
// ============================================================================

export class TrinityOrchestrator {
  private config: TrinityConfig
  private capabilityRegistry: CapabilityRegistry
  private skillGenerator: SkillGenerator
  private coordinator: AgentCoordinator
  private executionHistory: Map<string, TrinityResult> = new Map()
  
  constructor(
    config?: Partial<TrinityConfig>
  ) {
    this.config = {
      enableOpenClaw: true,
      enableHermes: true,
      enableClaudeCode: true,
      defaultLayer: 'openclaw',
      layerRouting: 'auto',
      maxConcurrentLayers: 3,
      ...config,
    }
    
    this.capabilityRegistry = new CapabilityRegistry()
    this.skillGenerator = skillGenerator
    this.coordinator = new AgentCoordinator()
  }
  
  // ============================================================================
  // Routing Logic
  // ============================================================================
  
  /**
   * Route a task to the appropriate layer(s).
   */
  route(task: TrinityTask): RoutingDecision {
    // If user specified preferred layer, respect it
    if (task.preferredLayer && this.isLayerEnabled(task.preferredLayer)) {
      return {
        recommendedLayer: task.preferredLayer,
        reasoning: `User specified ${task.preferredLayer} as preferred`,
        alternativeLayers: this.getAlternativeLayers(task.preferredLayer, task.requiredCapabilities),
        confidence: 0.9,
      }
    }
    
    // Auto-route based on capabilities
    if (this.config.layerRouting === 'auto') {
      return this.autoRoute(task)
    }
    
    // Hybrid routing - consider all factors
    return this.hybridRoute(task)
  }
  
  /**
   * Automatic layer routing based on task analysis.
   */
  private autoRoute(task: TrinityTask): RoutingDecision {
    const { layer, score } = this.capabilityRegistry.findBestLayer(task.requiredCapabilities)
    
    // Task type based routing
    let typeBasedLayer: TrinityLayer = this.config.defaultLayer
    
    switch (task.type) {
      case 'coding':
        typeBasedLayer = 'claude_code'
        break
      case 'planning':
      case 'management':
        typeBasedLayer = 'openclaw'
        break
      case 'research':
        typeBasedLayer = 'hermes'
        break
      case 'review':
        // Reviews benefit from multiple perspectives
        typeBasedLayer = 'openclaw'
        break
    }
    
    // Combine capability match with task type
    let finalLayer: TrinityLayer
    if (score > 0.7) {
      finalLayer = layer // Trust capability matching
    } else {
      finalLayer = typeBasedLayer // Fall back to task type
    }
    
    return {
      recommendedLayer: finalLayer,
      reasoning: `Task type '${task.type}' matched with ${finalLayer} (capability score: ${(score * 100).toFixed(0)}%)`,
      alternativeLayers: this.getAlternativeLayers(finalLayer, task.requiredCapabilities),
      confidence: score,
    }
  }
  
  /**
   * Hybrid routing considering multiple factors.
   */
  private hybridRoute(task: TrinityTask): RoutingDecision {
    // Consider capability match
    const capabilityMatch = this.capabilityRegistry.findBestLayer(task.requiredCapabilities)
    
    // Consider task type
    const typeRouting: Record<string, TrinityLayer> = {
      planning: 'openclaw',
      coding: 'claude_code',
      review: 'openclaw',
      research: 'hermes',
      management: 'openclaw',
      general: this.config.defaultLayer,
    }
    
    const typeLayer = typeRouting[task.type] || 'openclaw'
    
    // If capability match is strong, use it
    if (capabilityMatch.score > 0.8) {
      return {
        recommendedLayer: capabilityMatch.layer,
        reasoning: `Strong capability match (${(capabilityMatch.score * 100).toFixed(0)}%) for ${task.requiredCapabilities.join(', ')}`,
        alternativeLayers: this.getAlternativeLayers(capabilityMatch.layer, task.requiredCapabilities),
        confidence: capabilityMatch.score,
      }
    }
    
    // Otherwise use task type
    return {
      recommendedLayer: typeLayer,
      reasoning: `Task type '${task.type}' routing to ${typeLayer}`,
      alternativeLayers: this.getAlternativeLayers(typeLayer, task.requiredCapabilities),
      confidence: 0.6,
    }
  }
  
  /**
   * Get alternative layers when primary doesn't have all capabilities.
   */
  private getAlternativeLayers(primary: TrinityLayer, required: string[]): TrinityLayer[] {
    const alternatives: TrinityLayer[] = []
    
    for (const layer of ['openclaw', 'hermes', 'claude_code'] as TrinityLayer[]) {
      if (layer === primary) continue
      
      const hasExtra = required.some(cap => 
        this.capabilityRegistry.hasCapability(layer, cap) && 
        !this.capabilityRegistry.hasCapability(primary, cap)
      )
      
      if (hasExtra) alternatives.push(layer)
    }
    
    return alternatives.slice(0, 2)
  }
  
  /**
   * Check if a layer is enabled.
   */
  private isLayerEnabled(layer: TrinityLayer): boolean {
    switch (layer) {
      case 'openclaw': return this.config.enableOpenClaw
      case 'hermes': return this.config.enableHermes
      case 'claude_code': return this.config.enableClaudeCode
    }
  }
  
  // ============================================================================
  // Execution
  // ============================================================================
  
  /**
   * Execute a task using the recommended layer(s).
   */
  async execute(task: TrinityTask): Promise<TrinityResult> {
    const routing = this.route(task)
    const startTime = Date.now()
    
    const layerResults = new Map<TrinityLayer, LayerResult>()
    
    // Execute on primary layer
    const primaryResult = await this.executeOnLayer(routing.recommendedLayer, task)
    layerResults.set(routing.recommendedLayer, primaryResult)
    
    // Optionally execute on alternatives for comparison/fusion
    if (routing.alternativeLayers.length > 0 && this.config.layerRouting === 'hybrid') {
      // For hybrid mode, try alternative layers in parallel for best results
      const altPromises = routing.alternativeLayers.map(layer => 
        this.executeOnLayer(layer, task)
      )
      
      const altResults = await Promise.all(altPromises)
      altResults.forEach((result, idx) => {
        layerResults.set(routing.alternativeLayers[idx], result)
      })
    }
    
    // Fuse outputs from multiple layers
    const fusedOutput = this.fuseOutputs(layerResults, task)
    
    const result: TrinityResult = {
      taskId: task.id,
      success: primaryResult.success,
      primaryLayer: routing.recommendedLayer,
      layerResults,
      fusedOutput,
      confidence: this.calculateConfidence(layerResults, routing),
      executionTimeMs: Date.now() - startTime,
    }
    
    // Store in history
    this.executionHistory.set(task.id, result)
    
    return result
  }
  
  /**
   * Execute task on a specific layer.
   */
  private async executeOnLayer(layer: TrinityLayer, task: TrinityTask): Promise<LayerResult> {
    switch (layer) {
      case 'openclaw':
        return this.executeOpenClaw(task)
      case 'hermes':
        return this.executeHermes(task)
      case 'claude_code':
        return this.executeClaudeCode(task)
    }
  }
  
  /**
   * Execute using OpenClaw capabilities.
   */
  private async executeOpenClaw(task: TrinityTask): Promise<LayerResult> {
    try {
      // Use EO's multi-expert orchestration
      const fused = await this.skillGenerator.fuseWithEO({
        taskType: task.type,
        context: task.description,
      })
      
      return {
        layer: 'openclaw',
        success: true,
        output: fused.fused.bestOfBoth.description,
        confidence: fused.originalEO.confidence,
        capabilities: ['multi_agent', 'expert_coordination', 'structured_execution'],
        metadata: {
          expertCount: fused.originalEO.expertCount,
          experts: fused.originalEO.experts,
        },
      }
    } catch (error) {
      return {
        layer: 'openclaw',
        success: false,
        error: error instanceof Error ? error.message : String(error),
        confidence: 0,
        capabilities: ['multi_agent', 'expert_coordination', 'structured_execution'],
      }
    }
  }
  
  /**
   * Execute using Hermes-style auto-generation.
   */
  private async executeHermes(task: TrinityTask): Promise<LayerResult> {
    try {
      // Use Hermes-style skill generation and organic learning
      const skill = this.skillGenerator.generateFromExperience({
        taskType: task.type,
        context: task.description,
      })
      
      if (skill) {
        return {
          layer: 'hermes',
          success: true,
          output: `Generated skill: ${skill.name}\n${skill.description}`,
          confidence: skill.confidence,
          capabilities: ['auto_skill_gen', 'organic_growth', 'pattern_learning'],
          metadata: {
            skillId: skill.id,
            triggerPatterns: skill.triggerPatterns.slice(0, 3),
          },
        }
      }
      
      return {
        layer: 'hermes',
        success: false,
        error: 'Could not generate skill for this task',
        confidence: 0.3,
        capabilities: ['auto_skill_gen', 'organic_growth'],
      }
    } catch (error) {
      return {
        layer: 'hermes',
        success: false,
        error: error instanceof Error ? error.message : String(error),
        confidence: 0,
        capabilities: ['auto_skill_gen', 'organic_growth'],
      }
    }
  }
  
  /**
   * Execute using Claude Code capabilities.
   */
  private async executeClaudeCode(task: TrinityTask): Promise<LayerResult> {
    try {
      // Claude Code is best for coding tasks
      // In a real integration, would spawn a Claude Code session
      
      if (task.type === 'coding') {
        return {
          layer: 'claude_code',
          success: true,
          output: `[Claude Code] Would execute coding task: ${task.description.slice(0, 100)}...`,
          confidence: 0.95,
          capabilities: ['code_generation', 'refactoring', 'execution', 'debugging'],
          metadata: {
            note: 'Requires Claude Code runtime integration',
          },
        }
      }
      
      return {
        layer: 'claude_code',
        success: true,
        output: `[Claude Code] Task routed to coding layer but type is '${task.type}'`,
        confidence: 0.6,
        capabilities: ['code_generation', 'execution'],
      }
    } catch (error) {
      return {
        layer: 'claude_code',
        success: false,
        error: error instanceof Error ? error.message : String(error),
        confidence: 0,
        capabilities: ['code_generation', 'execution'],
      }
    }
  }
  
  // ============================================================================
  // Output Fusion
  // ============================================================================
  
  /**
   * Fuse outputs from multiple layers into a unified result.
   */
  private fuseOutputs(layerResults: Map<TrinityLayer, LayerResult>, task: TrinityTask): string {
    const results = Array.from(layerResults.values())
    const successful = results.filter(r => r.success)
    
    if (successful.length === 1) {
      return successful[0].output || 'No output'
    }
    
    if (successful.length === 0) {
      return 'All layers failed'
    }
    
    // Fusion strategy: combine insights from multiple layers
    const outputs = successful.map(r => {
      const layerEmoji = { openclaw: '🦞', hermes: '🧠', claude_code: '💻' }[r.layer]
      return `${layerEmoji} [${r.layer}] ${r.output}`
    })
    
    return `## Multi-Layer Fusion Result\n\n${outputs.join('\n\n')}\n\n---\n**Best Layer**: ${this.selectBestLayer(successful)}`
  }
  
  /**
   * Select the best performing layer.
   */
  private selectBestLayer(results: LayerResult[]): string {
    const sorted = [...results].sort((a, b) => b.confidence - a.confidence)
    const best = sorted[0]
    return `${best.layer} (${(best.confidence * 100).toFixed(0)}% confidence)`
  }
  
  /**
   * Calculate overall confidence from all layers.
   */
  private calculateConfidence(
    layerResults: Map<TrinityLayer, LayerResult>,
    routing: RoutingDecision
  ): number {
    const results = Array.from(layerResults.values())
    const successCount = results.filter(r => r.success).length
    
    if (successCount === 0) return 0
    
    const avgConfidence = results.reduce((sum, r) => sum + r.confidence, 0) / results.length
    const successRate = successCount / results.length
    
    // Combine: weighted by routing confidence
    return avgConfidence * 0.7 + successRate * 0.3 * routing.confidence
  }
  
  // ============================================================================
  // Status & Analytics
  // ============================================================================
  
  /**
   * Get routing statistics.
   */
  getRoutingStats(): {
    totalTasks: number
    layerDistribution: Record<TrinityLayer, number>
    averageConfidence: number
    successRate: number
  } {
    const results = Array.from(this.executionHistory.values())
    
    const distribution: Record<TrinityLayer, number> = {
      openclaw: 0,
      hermes: 0,
      claude_code: 0,
    }
    
    let totalConfidence = 0
    let successCount = 0
    
    results.forEach(r => {
      distribution[r.primaryLayer]++
      totalConfidence += r.confidence
      if (r.success) successCount++
    })
    
    return {
      totalTasks: results.length,
      layerDistribution: distribution,
      averageConfidence: results.length > 0 ? totalConfidence / results.length : 0,
      successRate: results.length > 0 ? successCount / results.length : 0,
    }
  }
  
  /**
   * Get capability comparison between layers.
   */
  getCapabilityComparison(): Record<string, Record<TrinityLayer, number>> {
    const allCapabilities = new Set<string>()
    
    for (const caps of this.capabilityRegistry.getAllCapabilitiesMap().values()) {
      caps.forEach(c => allCapabilities.add(c))
    }
    
    const comparison: Record<string, Record<TrinityLayer, number>> = {}
    
    allCapabilities.forEach(cap => {
      comparison[cap] = {
        openclaw: this.capabilityRegistry.getStrength('openclaw', cap),
        hermes: this.capabilityRegistry.getStrength('hermes', cap),
        claude_code: this.capabilityRegistry.getStrength('claude_code', cap),
      }
    })
    
    return comparison
  }
}

// ============================================================================
// Global Instance
// ============================================================================

export const trinityOrchestrator = new TrinityOrchestrator()

export default TrinityOrchestrator
