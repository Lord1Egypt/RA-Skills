/**
 * Preset Workflow Templates
 * Pre-defined workflows for common scenarios
 */

import type { PresetWorkflowTemplate, Workflow, WorkflowStep } from './types.js'

/**
 * Generate unique ID
 */
function generateId(prefix: string): string {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`
}

/**
 * Create workflow steps from template
 */
function createSteps(steps: Omit<WorkflowStep, 'id'>[]): WorkflowStep[] {
  return steps.map((step, index) => ({
    ...step,
    id: `step_${index + 1}`,
  }))
}

/**
 * Preset Workflow Templates
 */
export const PRESET_WORKFLOWS: PresetWorkflowTemplate[] = [
  {
    id: 'new-project',
    name: 'New Project Launch',
    description: 'Complete workflow for starting a new project: intent detection, expert planning, architecture design, verification',
    steps: [
      {
        name: 'Intent Detection',
        type: 'condition',
        config: { condition: 'detect_project_intent' },
      },
      {
        name: 'Expert Planning',
        type: 'expert',
        config: { expertRole: 'planner', prompt: 'Plan the new project with WBS and milestones' },
      },
      {
        name: 'Architecture Design',
        type: 'expert',
        config: { expertRole: 'architect', prompt: 'Design system architecture' },
      },
      {
        name: 'Verification',
        type: 'tool',
        config: { toolName: 'eo_verify', toolParams: { checkpoint: 'milestone1' } },
      },
    ],
    trigger: {
      type: 'message',
      keywords: ['new project', 'start project', 'create project', '新项目', '项目启动'],
    },
  },
  {
    id: 'code-review',
    name: 'Code Review',
    description: 'Comprehensive code review: security scan, performance analysis, quality check, report generation',
    steps: [
      {
        name: 'Security Scan',
        type: 'expert',
        config: { expertRole: 'security', prompt: 'Scan for security vulnerabilities' },
      },
      {
        name: 'Performance Analysis',
        type: 'expert',
        config: { expertRole: 'performance', prompt: 'Analyze performance issues' },
      },
      {
        name: 'Quality Check',
        type: 'tool',
        config: { toolName: 'eo_code_review', toolParams: { depth: 'standard' } },
      },
      {
        name: 'Report Generation',
        type: 'output',
        config: { prompt: 'Generate review summary report' },
      },
    ],
    trigger: {
      type: 'message',
      keywords: ['code review', 'review code', 'check code', '代码审查', '代码检查'],
    },
  },
  {
    id: 'task-analysis',
    name: 'Task Analysis',
    description: 'Intelligent task analysis: intent detection, expert consultation, suggestion generation',
    steps: [
      {
        name: 'Intent Detection',
        type: 'condition',
        config: { condition: 'analyze_intent' },
      },
      {
        name: 'Expert Consultation',
        type: 'expert',
        config: { expertRole: 'analyst', prompt: 'Analyze task requirements' },
      },
      {
        name: 'Suggestion Generation',
        type: 'output',
        config: { prompt: 'Generate actionable suggestions' },
      },
    ],
    trigger: {
      type: 'message',
      keywords: ['analyze', 'analysis', '分析', '任务分析'],
    },
  },
  {
    id: 'debug-assist',
    name: 'Debug Assistant',
    description: 'Debug workflow: error analysis, root cause, fix suggestions, verification',
    steps: [
      {
        name: 'Error Analysis',
        type: 'condition',
        config: { condition: 'analyze_error' },
      },
      {
        name: 'Root Cause',
        type: 'expert',
        config: { expertRole: 'debugger', prompt: 'Find root cause' },
      },
      {
        name: 'Fix Suggestions',
        type: 'expert',
        config: { expertRole: 'developer', prompt: 'Suggest fixes' },
      },
      {
        name: 'Verification',
        type: 'tool',
        config: { toolName: 'eo_verify', toolParams: { type: 'code' } },
      },
    ],
    trigger: {
      type: 'message',
      keywords: ['bug', 'error', 'fix', 'debug', '错误', '调试', '修复'],
    },
  },
  {
    id: 'performance-optimize',
    name: 'Performance Optimization',
    description: 'Performance optimization: profiling, bottleneck identification, optimization, verification',
    steps: [
      {
        name: 'Profiling',
        type: 'expert',
        config: { expertRole: 'performance', prompt: 'Profile system performance' },
      },
      {
        name: 'Bottleneck ID',
        type: 'expert',
        config: { expertRole: 'architect', prompt: 'Identify bottlenecks' },
      },
      {
        name: 'Optimization',
        type: 'expert',
        config: { expertRole: 'developer', prompt: 'Apply optimizations' },
      },
      {
        name: 'Verification',
        type: 'tool',
        config: { toolName: 'eo_verify', toolParams: { type: 'performance' } },
      },
    ],
    trigger: {
      type: 'message',
      keywords: ['performance', 'optimize', 'slow', '优化', '性能'],
    },
  },
]

/**
 * Create a workflow instance from a preset template
 */
export function createWorkflowFromPreset(
  presetId: string,
  context: Record<string, any> = {}
): Workflow | null {
  const preset = PRESET_WORKFLOWS.find(p => p.id === presetId)
  if (!preset) return null

  return {
    id: generateId(preset.id),
    name: preset.name,
    description: preset.description,
    steps: createSteps(preset.steps),
    trigger: preset.trigger,
    context,
    status: 'idle',
    createdAt: Date.now(),
    currentStepIndex: 0,
  }
}

/**
 * Get all preset workflow IDs
 */
export function getPresetIds(): string[] {
  return PRESET_WORKFLOWS.map(p => p.id)
}

/**
 * Get preset by ID
 */
export function getPresetById(id: string): PresetWorkflowTemplate | undefined {
  return PRESET_WORKFLOWS.find(p => p.id === id)
}
