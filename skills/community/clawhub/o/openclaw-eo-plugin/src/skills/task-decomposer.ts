/**
 * Task Decomposer - Breaks down tasks into最小可执行单元
 * 
 * 核心原则：每个最小任务应该在 3-5分钟 内完成
 * 
 * 最小任务单元定义：
 * - 单一文件创建/修改
 * - 单一函数实现
 * - 单个测试用例
 * - 单次API调用
 * - 单一配置更新
 */

export interface DecomposedTask {
  id: string
  name: string
  description: string
  estimatedMinutes: number  // 1-5 分钟
  expertType: 'frontend' | 'backend' | 'qa' | 'devops' | 'security' | 'architect' | 'planner'
  dependencies: string[]  // task IDs that must complete first
  parallelizable: boolean
  codeLocation?: string  // File or module path
}

export interface TaskDecomposition {
  originalTask: string
  totalTasks: number
  estimatedTotalMinutes: number
  tasks: DecomposedTask[]
  parallelGroups: string[][]  // Tasks that can run in parallel
  criticalPath: string[]  // Task IDs in execution order
}

/**
 * Task Decomposer class
 */
export class TaskDecomposer {
  private static readonly MAX_TASK_MINUTES = 5
  private static readonly MIN_TASK_MINUTES = 1

  /**
   * Decompose a task into最小可执行单元
   * 
   * @param taskDescription - Original task description
   * @param context - Optional context (codebase, language, framework)
   * @returns TaskDecomposition with broken down tasks
   */
  decompose(taskDescription: string, context?: {
    language?: string
    framework?: string
    codebasePath?: string
  }): TaskDecomposition {
    const tasks: DecomposedTask[] = []
    const taskDesc = taskDescription.toLowerCase()

    // Strategy: Parse task type and decompose accordingly
    if (this.isFeatureDevelopment(taskDesc)) {
      this.decomposeFeature(taskDescription, tasks, context)
    } else if (this.isBugFix(taskDesc)) {
      this.decomposeBugFix(taskDescription, tasks, context)
    } else if (this.isRefactoring(taskDesc)) {
      this.decomposeRefactoring(taskDescription, tasks, context)
    } else if (this.isTesting(taskDesc)) {
      this.decomposeTesting(taskDescription, tasks, context)
    } else if (this.isDeployment(taskDesc)) {
      this.decomposeDeployment(taskDescription, tasks, context)
    } else {
      // Generic decomposition
      this.decomposeGeneric(taskDescription, tasks, context)
    }

    // Calculate parallel groups
    const parallelGroups = this.calculateParallelGroups(tasks)

    // Calculate critical path
    const criticalPath = this.calculateCriticalPath(tasks)

    // Calculate totals
    const totalTasks = tasks.length
    const estimatedTotalMinutes = tasks.reduce((sum, t) => sum + t.estimatedMinutes, 0)

    return {
      originalTask: taskDescription,
      totalTasks,
      estimatedTotalMinutes,
      tasks,
      parallelGroups,
      criticalPath,
    }
  }

  /**
   * Check if task is feature development
   */
  private isFeatureDevelopment(task: string): boolean {
    const keywords = ['implement', 'add', 'create', 'build', 'develop', 'new', '功能', '开发', '实现']
    return keywords.some(k => task.includes(k))
  }

  /**
   * Check if task is bug fix
   */
  private isBugFix(task: string): boolean {
    const keywords = ['fix', 'bug', 'error', 'issue', '修复', '错误', '问题']
    return keywords.some(k => task.includes(k))
  }

  /**
   * Check if task is refactoring
   */
  private isRefactoring(task: string): boolean {
    const keywords = ['refactor', 'restructure', 'optimize', 'improve', '重构', '优化', '整理']
    return keywords.some(k => task.includes(k))
  }

  /**
   * Check if task is testing
   */
  private isTesting(task: string): boolean {
    const keywords = ['test', 'testing', 'spec', '验证', '测试']
    return keywords.some(k => task.includes(k))
  }

  /**
   * Check if task is deployment
   */
  private isDeployment(task: string): boolean {
    const keywords = ['deploy', 'release', 'publish', 'build', '发布', '部署']
    return keywords.some(k => task.includes(k))
  }

  /**
   * Decompose feature development task
   */
  private decomposeFeature(task: string, tasks: DecomposedTask[], context?: { language?: string; framework?: string }): void {
    let taskId = 1

    // 1. 分析需求 → 1-2分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Analyze requirements',
      description: `分析"${task}"的功能需求，确定输入输出、边界条件`,
      estimatedMinutes: 2,
      expertType: 'planner',
      dependencies: [],
      parallelizable: false,
    })

    // 2. 设计接口/数据结构 → 2-3分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Design interface/schema',
      description: '设计API接口或数据结构，定义函数签名',
      estimatedMinutes: 3,
      expertType: 'architect',
      dependencies: ['task_1'],
      parallelizable: false,
    })

    // 3. 创建/修改文件 → 2-3分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Create/modify files',
      description: '创建新文件或修改现有文件，实现基础结构',
      estimatedMinutes: 3,
      expertType: context?.language === 'typescript' || context?.language === 'javascript' ? 'frontend' : 'backend',
      dependencies: ['task_2'],
      parallelizable: false,
      codeLocation: this.guessFileLocation(task, context),
    })

    // 4. 实现核心逻辑 → 3-5分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Implement core logic',
      description: '实现核心业务逻辑',
      estimatedMinutes: 5,
      expertType: context?.language === 'typescript' || context?.language === 'javascript' ? 'frontend' : 'backend',
      dependencies: ['task_3'],
      parallelizable: false,
    })

    // 5. 编写测试 → 2-3分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Write tests',
      description: '编写单元测试或集成测试',
      estimatedMinutes: 3,
      expertType: 'qa',
      dependencies: ['task_4'],
      parallelizable: false,
    })

    // 6. 代码审查 → 1-2分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Code review',
      description: '检查代码质量、规范、安全性',
      estimatedMinutes: 2,
      expertType: 'security',
      dependencies: ['task_5'],
      parallelizable: false,
    })
  }

  /**
   * Decompose bug fix task
   */
  private decomposeBugFix(task: string, tasks: DecomposedTask[], context?: { codebasePath?: string }): void {
    let taskId = 1

    // 1. 复现问题 → 2-3分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Reproduce bug',
      description: '复现并确认bug，收集错误日志',
      estimatedMinutes: 3,
      expertType: 'qa',
      dependencies: [],
      parallelizable: false,
    })

    // 2. 定位问题 → 2-3分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Locate bug',
      description: '通过日志、调试定位问题根源',
      estimatedMinutes: 3,
      expertType: 'backend',
      dependencies: ['task_1'],
      parallelizable: false,
    })

    // 3. 修复问题 → 1-2分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Fix bug',
      description: '实施修复',
      estimatedMinutes: 2,
      expertType: 'backend',
      dependencies: ['task_2'],
      parallelizable: false,
    })

    // 4. 验证修复 → 1-2分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Verify fix',
      description: '确认bug已修复，原有功能正常',
      estimatedMinutes: 2,
      expertType: 'qa',
      dependencies: ['task_3'],
      parallelizable: false,
    })
  }

  /**
   * Decompose refactoring task
   */
  private decomposeRefactoring(task: string, tasks: DecomposedTask[], context?: { codebasePath?: string }): void {
    let taskId = 1

    // 1. 分析待重构代码 → 2分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Analyze code to refactor',
      description: '分析待重构代码，理解依赖关系',
      estimatedMinutes: 2,
      expertType: 'architect',
      dependencies: [],
      parallelizable: false,
    })

    // 2. 规划重构步骤 → 1-2分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Plan refactoring steps',
      description: '规划重构顺序，最小化风险',
      estimatedMinutes: 2,
      expertType: 'planner',
      dependencies: ['task_1'],
      parallelizable: false,
    })

    // 3. 逐个文件重构 → 每文件2-3分钟
    // This would be broken down further based on actual files
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Refactor files',
      description: '按计划重构文件，保持功能不变',
      estimatedMinutes: 5,
      expertType: 'backend',
      dependencies: ['task_2'],
      parallelizable: true, // Can parallelize if multiple files
    })

    // 4. 更新测试 → 2分钟
    tasks.push({
      id: `task_${taskId++}`,
      name: 'Update tests',
      description: '更新因重构受影响的测试',
      estimatedMinutes: 2,
      expertType: 'qa',
      dependencies: ['task_3'],
      parallelizable: false,
    })
  }

  /**
   * Decompose testing task
   */
  private decomposeTesting(task: string, tasks: DecomposedTask[], context?: { codebasePath?: string }): void {
    let taskId = 1

    tasks.push({
      id: `task_${taskId++}`,
      name: 'Identify test scenarios',
      description: '识别需要测试的场景和边界条件',
      estimatedMinutes: 2,
      expertType: 'qa',
      dependencies: [],
      parallelizable: false,
    })

    tasks.push({
      id: `task_${taskId++}`,
      name: 'Write test cases',
      description: '编写测试用例',
      estimatedMinutes: 3,
      expertType: 'qa',
      dependencies: ['task_1'],
      parallelizable: false,
    })

    tasks.push({
      id: `task_${taskId++}`,
      name: 'Execute tests',
      description: '执行测试并记录结果',
      estimatedMinutes: 2,
      expertType: 'qa',
      dependencies: ['task_2'],
      parallelizable: false,
    })
  }

  /**
   * Decompose deployment task
   */
  private decomposeDeployment(task: string, tasks: DecomposedTask[], context?: { codebasePath?: string }): void {
    let taskId = 1

    tasks.push({
      id: `task_${taskId++}`,
      name: 'Prepare deployment',
      description: '检查构建、版本、环境配置',
      estimatedMinutes: 2,
      expertType: 'devops',
      dependencies: [],
      parallelizable: false,
    })

    tasks.push({
      id: `task_${taskId++}`,
      name: 'Deploy to staging',
      description: '部署到预发布环境',
      estimatedMinutes: 2,
      expertType: 'devops',
      dependencies: ['task_1'],
      parallelizable: false,
    })

    tasks.push({
      id: `task_${taskId++}`,
      name: 'Verify deployment',
      description: '验证部署结果',
      estimatedMinutes: 2,
      expertType: 'qa',
      dependencies: ['task_2'],
      parallelizable: false,
    })

    tasks.push({
      id: `task_${taskId++}`,
      name: 'Deploy to production',
      description: '部署到生产环境',
      estimatedMinutes: 2,
      expertType: 'devops',
      dependencies: ['task_3'],
      parallelizable: false,
    })
  }

  /**
   * Generic decomposition for unknown task types
   */
  private decomposeGeneric(task: string, tasks: DecomposedTask[], context?: { language?: string }): void {
    // For generic tasks, create a simple 3-step decomposition
    tasks.push({
      id: 'task_1',
      name: 'Analyze task',
      description: `分析"${task}"的目标和范围`,
      estimatedMinutes: 2,
      expertType: 'planner',
      dependencies: [],
      parallelizable: false,
    })

    tasks.push({
      id: 'task_2',
      name: 'Execute task',
      description: '执行任务',
      estimatedMinutes: 5,
      expertType: context?.language === 'typescript' || context?.language === 'javascript' ? 'frontend' : 'backend',
      dependencies: ['task_1'],
      parallelizable: false,
    })

    tasks.push({
      id: 'task_3',
      name: 'Verify result',
      description: '验证任务完成情况',
      estimatedMinutes: 2,
      expertType: 'qa',
      dependencies: ['task_2'],
      parallelizable: false,
    })
  }

  /**
   * Calculate parallel groups based on dependencies
   */
  private calculateParallelGroups(tasks: DecomposedTask[]): string[][] {
    const groups: string[][] = []
    const assigned = new Set<string>()

    // First pass: tasks with no dependencies can run in parallel
    const noDeps = tasks.filter(t => t.dependencies.length === 0 && t.parallelizable)
    if (noDeps.length > 0) {
      groups.push(noDeps.map(t => t.id))
      noDeps.forEach(t => assigned.add(t.id))
    }

    // Second pass: remaining tasks
    const remaining = tasks.filter(t => !assigned.has(t.id))
    if (remaining.length > 0) {
      groups.push(remaining.map(t => t.id))
    }

    return groups
  }

  /**
   * Calculate critical path (longest path through dependencies)
   */
  private calculateCriticalPath(tasks: DecomposedTask[]): string[] {
    const path: string[] = []
    const taskMap = new Map(tasks.map(t => [t.id, t]))

    // Find entry tasks (no dependencies)
    let currentTasks = tasks.filter(t => t.dependencies.length === 0)

    while (currentTasks.length > 0) {
      // Add the longest task to path
      const longest = currentTasks.reduce((a, b) =>
        a.estimatedMinutes > b.estimatedMinutes ? a : b
      )
      path.push(longest.id)

      // Find next tasks (dependencies satisfied)
      const nextIds = new Set(longest.id)
      currentTasks = tasks.filter(t =>
        t.dependencies.every(dep => nextIds.has(dep)) && !path.includes(t.id)
      )
    }

    return path
  }

  /**
   * Guess file location from task description
   */
  private guessFileLocation(task: string, context?: { framework?: string }): string | undefined {
    const lower = task.toLowerCase()

    if (lower.includes('component') || lower.includes('ui') || lower.includes('页面')) {
      if (context?.framework === 'react') return 'src/components/'
      if (context?.framework === 'vue') return 'src/components/'
      return 'src/components/'
    }

    if (lower.includes('api') || lower.includes('接口')) {
      return 'src/api/'
    }

    if (lower.includes('service') || lower.includes('服务')) {
      return 'src/services/'
    }

    if (lower.includes('util') || lower.includes('工具')) {
      return 'src/utils/'
    }

    return undefined
  }

  /**
   * Format decomposition as markdown for display
   */
  formatAsMarkdown(decomposition: TaskDecomposition): string {
    const lines: string[] = [
      `# Task Decomposition: ${decomposition.originalTask}`,
      '',
      `**Total Tasks:** ${decomposition.totalTasks} | **Estimated:** ${decomposition.estimatedTotalMinutes} min`,
      '',
      '## Execution Plan',
      '',
    ]

    // Show critical path first
    if (decomposition.criticalPath.length > 0) {
      lines.push('### Critical Path (Sequential)')
      lines.push('')
      for (const taskId of decomposition.criticalPath) {
        const task = decomposition.tasks.find(t => t.id === taskId)
        if (task) {
          lines.push(`${task.estimatedMinutes}min | ${task.expertType} | ${task.name}`)
        }
      }
      lines.push('')
    }

    // Show parallel groups
    if (decomposition.parallelGroups.length > 0) {
      lines.push('### Parallel Execution')
      lines.push('')
      for (let i = 0; i < decomposition.parallelGroups.length; i++) {
        const group = decomposition.parallelGroups[i]
        const groupTasks = group.map(id => decomposition.tasks.find(t => t.id === id)!).filter(Boolean)
        const maxTime = Math.max(...groupTasks.map(t => t.estimatedMinutes))
        lines.push(`**Group ${i + 1}** (${maxTime}min): ${groupTasks.map(t => t.name).join(', ')}`)
      }
      lines.push('')
    }

    // Show detailed task list
    lines.push('### All Tasks')
    lines.push('')
    lines.push('| # | Task | Expert | Time | Dependencies |')
    lines.push('|---|------|--------|------|--------------|')

    decomposition.tasks.forEach((task, idx) => {
      const deps = task.dependencies.length > 0 ? task.dependencies.join(', ') : '-'
      lines.push(`| ${idx + 1} | ${task.name} | ${task.expertType} | ${task.estimatedMinutes}min | ${deps} |`)
    })

    lines.push('')
    lines.push('---')
    lines.push(`*Generated at ${new Date().toISOString()}*`)

    return lines.join('\n')
  }
}

// Export singleton
export const taskDecomposer = new TaskDecomposer()
