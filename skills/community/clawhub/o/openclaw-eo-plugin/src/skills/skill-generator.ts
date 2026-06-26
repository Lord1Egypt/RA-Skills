// ============================================================================
// EO Skill Generator - Phase 5.1: Capability Fusion
//
// Integrates Hermes-style auto-skill generation with EO's expert system.
// Enables organic skill growth while maintaining structured collaboration.
// ============================================================================

import { AgentKnowledgeGraph, knowledgeGraph, Experience, experienceTracker } from '../collaboration/knowledge-graph.js'
import { AgentCoordinator } from '../autonomy/agent-coordinator.js'
import { logger } from '../utils/logger.js'

// ============================================================================
// Types
// ============================================================================

export interface SkillTemplate {
  id: string
  name: string
  description: string
  category: string
  triggerPatterns: string[]          // patterns that suggest this skill is needed
  requiredExpertRoles: string[]      // which experts to involve
  steps: SkillStep[]
  examples: string[]                 // example use cases
  confidence: number                  // 0-1, how well it works
  usageCount: number
  successRate: number
  createdAt: number
  source: 'manual' | 'generated' | 'learned'
}

export interface SkillStep {
  order: number
  action: 'analyze' | 'plan' | 'execute' | 'review' | 'coordinate' | 'synthesize'
  description: string
  expertRole?: string               // which expert handles this step
  timeout?: number                  // ms
  requiredOutput?: string           // what's expected from this step
}

export interface GeneratedSkill extends Omit<SkillTemplate, 'id' | 'createdAt'> {
  id: string
  createdAt: number
  generationReason: string          // why this skill was generated
  parentSkillId?: string            // if derived from another skill
  trainingData: TrainingExample[]   // examples used to generate
}

export interface TrainingExample {
  input: string
  output: string
  quality: number                   // 0-1
  source: 'experience' | 'expert' | 'user_feedback'
}

export interface SkillGenerationRequest {
  taskType: string
  context: string
  expertOutputs?: Map<string, string>
  similarSkills?: SkillTemplate[]
  targetDomain?: string
}

export interface SkillFusionResult {
  originalEO: {
    expertCount: number
    experts: string[]
    confidence: number
  }
  generatedHermes: {
    skillId: string
    skillName: string
    triggerPatterns: string[]
    confidence: number
  }
  fused: {
    bestOfBoth: SkillTemplate
    recommendations: string[]
  }
}

// ============================================================================
// Pattern Analyzer
// ============================================================================

class PatternAnalyzer {
  private patterns: Map<string, RegExp[]> = new Map()
  
  constructor() {
    this.initializeDefaultPatterns()
  }
  
  private initializeDefaultPatterns(): void {
    // Common task type patterns
    this.patterns.set('planning', [
      /计划|规划|安排/i,
      /plan|schedule/i,
      /wbs|任务分解/i,
    ])
    
    this.patterns.set('coding', [
      /代码|开发|实现/i,
      /code|implement|build/i,
      /function|class|module/i,
    ])
    
    this.patterns.set('review', [
      /审查|评审|检查/i,
      /review|check|audit/i,
      /code review|pr review/i,
    ])
    
    this.patterns.set('architecture', [
      /架构|设计|方案/i,
      /architecture|design|system/i,
      /structure|pattern/i,
    ])
    
    this.patterns.set('debugging', [
      /调试|修复|问题/i,
      /debug|fix|issue|bug/i,
      /error|exception/i,
    ])
    
    this.patterns.set('deployment', [
      /部署|发布|上线/i,
      /deploy|release|publish/i,
      /ci\/cd|pipeline/i,
    ])
  }
  
  /**
   * Analyze text to detect task type.
   */
  analyzeTaskType(text: string): { type: string; confidence: number; matchedPatterns: string[] } {
    const matchedPatterns: string[] = []
    let bestMatch: string = 'general'
    let bestConfidence = 0
    
    this.patterns.forEach((regexes, type) => {
      let matchCount = 0
      regexes.forEach(regex => {
        if (regex.test(text)) matchCount++
      })
      
      if (matchCount > 0) {
        const confidence = Math.min(1, matchCount / regexes.length)
        matchedPatterns.push(type)
        
        if (confidence > bestConfidence) {
          bestConfidence = confidence
          bestMatch = type
        }
      }
    })
    
    return { type: bestMatch, confidence: bestConfidence, matchedPatterns }
  }
  
  /**
   * Extract key phrases from text.
   */
  extractKeyPhrases(text: string, maxPhrases = 10): string[] {
    // Simple extraction - in production would use NLP
    const words = text.split(/\s+/)
      .filter(w => w.length > 3)
      .filter(w => !this.isStopWord(w))
    
    // Count frequency
    const freq = new Map<string, number>()
    words.forEach(w => {
      const normalized = w.toLowerCase().replace(/[^a-z\u4e00-\u9fa5]/g, '')
      freq.set(normalized, (freq.get(normalized) || 0) + 1)
    })
    
    // Sort by frequency
    return Array.from(freq.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, maxPhrases)
      .map(([word]) => word)
  }
  
  private isStopWord(word: string): boolean {
    const stops = ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'this', 'that', '的', '是', '在', '了', '和']
    return stops.includes(word.toLowerCase())
  }
}

// ============================================================================
// Skill Generator
// ============================================================================

export class SkillGenerator {
  private knowledgeGraph: AgentKnowledgeGraph
  private coordinator: AgentCoordinator
  private patternAnalyzer: PatternAnalyzer
  private generatedSkills: Map<string, GeneratedSkill> = new Map()
  
  constructor(
    knowledgeGraph: AgentKnowledgeGraph,
    coordinator: AgentCoordinator
  ) {
    this.knowledgeGraph = knowledgeGraph
    this.coordinator = coordinator
    this.patternAnalyzer = new PatternAnalyzer()
  }
  
  // ============================================================================
  // Skill Generation from Experience
  // ============================================================================
  
  /**
   * Generate a new skill from accumulated experience.
   */
  generateFromExperience(request: SkillGenerationRequest): GeneratedSkill | null {
    // Analyze task type
    const analysis = this.patternAnalyzer.analyzeTaskType(request.context)
    
    if (analysis.confidence < 0.3) {
      logger.warn('Task type unclear, cannot generate skill')
      return null
    }
    
    // Find similar existing skills
    const similarSkills = this.findSimilarSkills(request.taskType, analysis.type)
    
    // Extract key phrases for trigger patterns
    const triggerPatterns = this.patternAnalyzer.extractKeyPhrases(request.context, 5)
    
    // Build skill steps based on task type
    const steps = this.generateSteps(analysis.type, request.expertOutputs)
    
    // Calculate confidence based on similar skills
    let confidence = 0.5
    if (similarSkills.length > 0) {
      confidence = Math.min(0.9, 0.5 + similarSkills.length * 0.1)
    }
    
    // Create the generated skill
    const skill: GeneratedSkill = {
      id: 'skill-gen-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6),
      name: this.generateSkillName(analysis.type, request.taskType),
      description: this.generateDescription(request.context, analysis.type),
      category: analysis.type,
      triggerPatterns: triggerPatterns.map(p => `.*${p}.*`),
      requiredExpertRoles: this.determineRequiredExperts(analysis.type),
      steps,
      examples: this.generateExamples(analysis.type),
      confidence,
      usageCount: 0,
      successRate: 0,
      createdAt: Date.now(),
      source: 'generated',
      generationReason: `Detected ${analysis.type} pattern from ${similarSkills.length} similar skills`,
      trainingData: this.aggregateTrainingData(similarSkills),
    }
    
    this.generatedSkills.set(skill.id, skill)
    return skill
  }
  
  /**
   * Generate skill steps based on task type.
   */
  private generateSteps(taskType: string, expertOutputs?: Map<string, string>): SkillStep[] {
    const baseSteps: SkillStep[] = [
      { order: 1, action: 'analyze', description: 'Analyze task requirements' }
    ]
    
    switch (taskType) {
      case 'planning':
        return [
          ...baseSteps,
          { order: 2, action: 'coordinate', description: 'Involve Planner expert', expertRole: 'planner' },
          { order: 3, action: 'plan', description: 'Create project plan' },
          { order: 4, action: 'review', description: 'Review plan with Architect', expertRole: 'architect' },
        ]
        
      case 'coding':
        return [
          ...baseSteps,
          { order: 2, action: 'coordinate', description: 'Assign Frontend/Backend experts', expertRole: 'frontend' },
          { order: 3, action: 'execute', description: 'Implement code' },
          { order: 4, action: 'review', description: 'Code review', expertRole: 'qa' },
        ]
        
      case 'architecture':
        return [
          ...baseSteps,
          { order: 2, action: 'coordinate', description: 'Involve Architect expert', expertRole: 'architect' },
          { order: 3, action: 'plan', description: 'Design system architecture' },
          { order: 4, action: 'synthesize', description: 'Create architecture document' },
        ]
        
      case 'review':
        return [
          ...baseSteps,
          { order: 2, action: 'review', description: 'Multi-expert review', expertRole: 'qa' },
          { order: 3, action: 'synthesize', description: 'Aggregate review findings' },
        ]
        
      case 'debugging':
        return [
          ...baseSteps,
          { order: 2, action: 'analyze', description: 'Analyze error patterns' },
          { order: 3, action: 'execute', description: 'Identify root cause' },
          { order: 4, action: 'review', description: 'Verify fix with QA', expertRole: 'qa' },
        ]
        
      case 'deployment':
        return [
          ...baseSteps,
          { order: 2, action: 'coordinate', description: 'Involve DevOps expert', expertRole: 'devops' },
          { order: 3, action: 'execute', description: 'Execute deployment' },
          { order: 4, action: 'review', description: 'Verify deployment', expertRole: 'qa' },
        ]
        
      default:
        return [
          ...baseSteps,
          { order: 2, action: 'execute', description: 'Execute task' },
          { order: 3, action: 'review', description: 'Review outcome' },
        ]
    }
  }
  
  /**
   * Determine required experts for a task type.
   */
  private determineRequiredExperts(taskType: string): string[] {
    const expertMap: Record<string, string[]> = {
      planning: ['planner', 'architect'],
      coding: ['frontend', 'backend', 'qa'],
      architecture: ['architect'],
      review: ['qa', 'architect'],
      debugging: ['backend', 'qa'],
      deployment: ['devops', 'qa'],
      general: ['planner'],
    }
    return expertMap[taskType] || ['planner']
  }
  
  /**
   * Generate a skill name.
   */
  private generateSkillName(taskType: string, context: string): string {
    const prefix = {
      planning: '智能规划',
      coding: '代码开发',
      architecture: '架构设计',
      review: '评审审查',
      debugging: '问题诊断',
      deployment: '部署发布',
      general: '任务执行',
    }[taskType] || '任务处理'
    
    return `${prefix}-${Date.now().toString(36).slice(-4).toUpperCase()}`
  }
  
  /**
   * Generate a skill description.
   */
  private generateDescription(context: string, taskType: string): string {
    const keyPhrases = this.patternAnalyzer.extractKeyPhrases(context, 3)
    return `自动生成的${taskType}技能，用于处理${keyPhrases.join('、')}相关的任务`
  }
  
  /**
   * Generate example use cases.
   */
  private generateExamples(taskType: string): string[] {
    const examples: Record<string, string[]> = {
      planning: ['创建项目计划', '分解复杂任务', '制定里程碑'],
      coding: ['实现新功能', '重构现有代码', '添加单元测试'],
      architecture: ['设计系统架构', '评审技术方案', '优化系统结构'],
      review: ['代码审查', 'PR评审', '文档检查'],
      debugging: ['定位Bug', '分析崩溃', '修复问题'],
      deployment: ['部署到测试环境', '发布新版本', '回滚操作'],
      general: ['执行常规任务', '处理用户请求', '协调多专家工作'],
    }
    return examples[taskType] || ['执行任务']
  }
  
  // ============================================================================
  // Skill Similarity & Matching
  // ============================================================================
  
  /**
   * Find similar existing skills.
   */
  private findSimilarSkills(taskType: string, detectedType: string): SkillTemplate[] {
    // Query knowledge graph for related skills
    const knowledge = this.knowledgeGraph.query({
      tags: [taskType, detectedType],
      types: ['pattern', 'solution'],
      minConfidence: 0.5,
      limit: 5,
    })
    
    // Convert to skill format (simplified)
    return knowledge.map(k => ({
      id: k.id,
      name: k.content.slice(0, 50),
      description: k.content,
      category: k.type,
      triggerPatterns: k.tags,
      requiredExpertRoles: [],
      steps: [],
      examples: [],
      confidence: k.confidence,
      usageCount: k.usageCount,
      successRate: k.successRate,
      createdAt: k.createdAt,
      source: 'learned' as const,
    }))
  }
  
  /**
   * Find the best matching skill for a task.
   */
  findBestMatch(taskDescription: string): { skill: GeneratedSkill | null; matchScore: number } {
    const analysis = this.patternAnalyzer.analyzeTaskType(taskDescription)
    const keyPhrases = this.patternAnalyzer.extractKeyPhrases(taskDescription, 5)
    
    let bestMatch: GeneratedSkill | null = null
    let bestScore = 0
    
    for (const skill of this.generatedSkills.values()) {
      let score = 0
      
      // Category match
      if (skill.category === analysis.type) {
        score += 0.4
      }
      
      // Trigger pattern match
      const triggerMatches = skill.triggerPatterns.filter(pattern => {
        try {
          return new RegExp(pattern.slice(2, -2)).test(taskDescription)
        } catch {
          return false
        }
      }).length
      score += (triggerMatches / skill.triggerPatterns.length) * 0.3
      
      // Key phrase match
      const phraseMatches = keyPhrases.filter(phrase => 
        skill.triggerPatterns.some(p => p.includes(phrase))
      ).length
      score += (phraseMatches / keyPhrases.length) * 0.3
      
      if (score > bestScore) {
        bestScore = score
        bestMatch = skill
      }
    }
    
    return { skill: bestMatch, matchScore: bestScore }
  }
  
  // ============================================================================
  // Skill Fusion: EO + Hermes
  // ============================================================================
  
  /**
   * Fuse EO structured approach with Hermes-style generated skills.
   */
  async fuseWithEO(request: SkillGenerationRequest): Promise<SkillFusionResult> {
    // Get EO expert contributions
    const eoExperts = request.expertOutputs 
      ? Array.from(request.expertOutputs.keys()) 
      : this.determineRequiredExperts(request.taskType)
    
    // Generate Hermes-style skill
    const hermesSkill = this.generateFromExperience(request)
    
    if (!hermesSkill) {
      throw new Error('Failed to generate skill from experience')
    }
    
    // Find similar skills
    const similarSkills = this.findSimilarSkills(request.taskType, '')
    
    // Create fused skill
    const fused: SkillTemplate = {
      id: 'fused-' + hermesSkill.id,
      name: `融合: ${hermesSkill.name}`,
      description: `结合EO结构化专家协作与Hermes风格自动生成的技能，综合${eoExperts.length}位专家知识`,
      category: hermesSkill.category,
      triggerPatterns: hermesSkill.triggerPatterns,
      requiredExpertRoles: [...new Set([...eoExperts, ...hermesSkill.requiredExpertRoles])],
      steps: this.mergeSteps(hermesSkill.steps, eoExperts),
      examples: hermesSkill.examples,
      confidence: Math.min(0.95, hermesSkill.confidence + 0.2), // Boost from fusion
      usageCount: 0,
      successRate: 0,
      createdAt: Date.now(),
      source: 'learned',
    }
    
    return {
      originalEO: {
        expertCount: eoExperts.length,
        experts: eoExperts,
        confidence: 0.8,
      },
      generatedHermes: {
        skillId: hermesSkill.id,
        skillName: hermesSkill.name,
        triggerPatterns: hermesSkill.triggerPatterns,
        confidence: hermesSkill.confidence,
      },
      fused: {
        bestOfBoth: fused,
        recommendations: [
          `使用了 ${eoExperts.length} 位专家: ${eoExperts.join(', ')}`,
          `触发词: ${hermesSkill.triggerPatterns.slice(0, 3).join(', ')}`,
          '置信度提升: +20% (从融合中获益)',
        ],
      },
    }
  }
  
  /**
   * Merge steps from Hermes skill with EO expert coordination.
   */
  private mergeSteps(hermesSteps: SkillStep[], eoExperts: string[]): SkillStep[] {
    // Insert expert coordination at key points
    const merged: SkillStep[] = []
    let stepOrder = 1
    
    hermesSteps.forEach(step => {
      merged.push({ ...step, order: stepOrder++ })
      
      // Insert coordination step after planning steps
      if (step.action === 'plan' || step.action === 'analyze') {
        const relevantExperts = eoExperts.filter(e => 
          step.expertRole ? true : true // Simplified - would filter by role
        )
        
        if (relevantExperts.length > 0) {
          merged.push({
            order: stepOrder++,
            action: 'coordinate',
            description: `协调专家: ${relevantExperts.join(', ')}`,
            expertRole: relevantExperts[0],
          })
        }
      }
    })
    
    return merged
  }
  
  // ============================================================================
  // Training Data Aggregation
  // ============================================================================
  
  /**
   * Aggregate training data from similar skills.
   */
  private aggregateTrainingData(similarSkills: SkillTemplate[]): TrainingExample[] {
    const examples: TrainingExample[] = []
    
    similarSkills.forEach(skill => {
      skill.examples.forEach(example => {
        examples.push({
          input: example,
          output: skill.description,
          quality: skill.confidence * skill.successRate,
          source: 'experience',
        })
      })
    })
    
    return examples.slice(0, 20) // Limit to 20 examples
  }
  
  // ============================================================================
  // Skill Management
  // ============================================================================
  
  /**
   * Get all generated skills.
   */
  getAllSkills(): GeneratedSkill[] {
    return Array.from(this.generatedSkills.values())
  }
  
  /**
   * Get skill by ID.
   */
  getSkill(id: string): GeneratedSkill | undefined {
    return this.generatedSkills.get(id)
  }
  
  /**
   * Update skill based on usage feedback.
   */
  updateSkillFeedback(skillId: string, success: boolean): void {
    const skill = this.generatedSkills.get(skillId)
    if (!skill) return
    
    skill.usageCount++
    
    if (skill.usageCount === 1) {
      skill.successRate = success ? 1 : 0
    } else {
      skill.successRate = (skill.successRate * (skill.usageCount - 1) + (success ? 1 : 0)) / skill.usageCount
    }
    
    // Adjust confidence based on success rate
    if (skill.usageCount >= 5) {
      skill.confidence = skill.successRate * 0.9 + 0.1
    }
    
    // Record in knowledge graph
    this.knowledgeGraph.addNode({
      type: 'pattern',
      content: `Skill ${skill.name} used ${skill.usageCount} times with ${(skill.successRate * 100).toFixed(0)}% success`,
      tags: [skill.category, 'skill-performance'],
      confidence: skill.confidence,
      successRate: skill.successRate,
    })
  }
}

// ============================================================================
// Global Instance
// ============================================================================

export const skillGenerator = new SkillGenerator(
  knowledgeGraph,
  new AgentCoordinator()
)

export default SkillGenerator
