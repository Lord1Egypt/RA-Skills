#!/usr/bin/env node
/**
 * Parallel Tasks Executor for OpenClaw
 * 
 * Executes multiple tasks in parallel using sessions_spawn with:
 * - Configurable timeout per task
 * - Error isolation (one failure doesn't block others)
 * - Aggregated results summary
 * 
 * Usage:
 *   node executor.ts --task "Research X" --task "Research Y" --timeout 300
 *   node executor.ts --tasks-file tasks.txt --timeout 600
 */

import * as fs from 'fs'
import * as path from 'path'

// Types
interface Task {
  name: string
  description: string
  timeout?: number
}

interface TaskResult {
  name: string
  status: 'fulfilled' | 'rejected' | 'timeout' | 'cancelled' | 'no_reply'
  duration?: number
  value?: string
  error?: string
}

interface ParallelOptions {
  timeout: number
  stopOnError: boolean
  reportProgress: boolean
  maxConcurrent: number
}

// ANSI colors for terminal output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  gray: '\x1b[90m'
}

function colorize(color: string, text: string): string {
  return `${colors[color as keyof typeof colors] || ''}${text}${colors.reset}`
}

/**
 * Parse command line arguments
 */
function parseArgs(): { tasks: Task[], options: Partial<ParallelOptions> } {
  const args = process.argv.slice(2)
  const tasks: Task[] = []
  const options: Partial<ParallelOptions> = {
    timeout: 300,
    stopOnError: false,
    reportProgress: true,
    maxConcurrent: 5
  }

  let currentTask: string | null = null
  let i = 0

  while (i < args.length) {
    const arg = args[i]

    if (arg === '--task' || arg === '-t') {
      if (currentTask) {
        tasks.push({ name: `task-${tasks.length + 1}`, description: currentTask })
      }
      currentTask = args[++i]
    } else if (arg === '--timeout' || arg === '-to') {
      options.timeout = parseInt(args[++i]) || 300
    } else if (arg === '--max-concurrent' || arg === '-m') {
      options.maxConcurrent = parseInt(args[++i]) || 5
    } else if (arg === '--stop-on-error') {
      options.stopOnError = true
    } else if (arg === '--no-progress') {
      options.reportProgress = false
    } else if (arg === '--tasks-file' || arg === '-f') {
      const filePath = args[++i]
      if (filePath && fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf-8')
        const fileTasks = parseTaskInput(content)
        tasks.push(...fileTasks)
      }
    } else if (arg === '--help' || arg === '-h') {
      printHelp()
      process.exit(0)
    } else if (arg === '--parse') {
      // Parse mode: read tasks from stdin and print parsed output
      const stdin = fs.readFileSync('/dev/stdin', 'utf-8')
      const parsed = parseTaskInput(stdin)
      console.log(JSON.stringify(parsed, null, 2))
      process.exit(0)
    } else if (!arg.startsWith('-')) {
      // Positional argument treated as task description
      if (currentTask) {
        tasks.push({ name: `task-${tasks.length + 1}`, description: currentTask })
      }
      currentTask = arg
    }
    i++
  }

  // Don't forget the last task
  if (currentTask) {
    tasks.push({ name: `task-${tasks.length + 1}`, description: currentTask })
  }

  return { tasks, options }
}

/**
 * Parse task input from various formats
 */
function parseTaskInput(input: string): Task[] {
  const lines = input.split('\n').filter(line => line.trim())
  const tasks: Task[] = []

  for (const line of lines) {
    const trimmed = line.trim()

    // Skip empty lines and comments
    if (!trimmed || trimmed.startsWith('#')) continue

    // Named task: [name] description
    const namedMatch = trimmed.match(/^\[([^\]]+)\]\s*(.+)$/)
    if (namedMatch) {
      tasks.push({
        name: namedMatch[1],
        description: namedMatch[2]
      })
      continue
    }

    // Bullet list or numbered: - task or 1. task
    const listMatch = trimmed.match(/^[-*\d.]\s*(.+)$/)
    if (listMatch) {
      tasks.push({
        name: `task-${tasks.length + 1}`,
        description: listMatch[1]
      })
      continue
    }

    // Plain text: treat as description
    if (trimmed.length > 0) {
      tasks.push({
        name: `task-${tasks.length + 1}`,
        description: trimmed
      })
    }
  }

  return tasks
}

/**
 * Execute a single task via sessions_spawn ACP command
 */
async function executeTaskViaSpawn(
  task: Task,
  timeoutSeconds: number
): Promise<TaskResult> {
  const startTime = Date.now()
  const taskId = `parallel-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`

  return new Promise((resolve) => {
    // Build the ACP spawn command
    const spawnCmd = [
      'sessions_spawn',
      '--task', `"${task.description}"`,
      '--label', `"${task.name}"`,
      '--timeout', String(timeoutSeconds),
      '--session-id', taskId
    ].join(' ')

    if (process.env.DEBUG) {
      console.error(`[DEBUG] Spawning: ${spawnCmd}`)
    }

    // Use Hermes CLI to spawn session
    const { spawn } = require('child_process')
    const proc = spawn('hermes', ['cli', '--', ...spawnCmd.split(' ').filter(Boolean)], {
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env }
    })

    let stdout = ''
    let stderr = ''

    proc.stdout?.on('data', (data: Buffer) => {
      stdout += data.toString()
    })

    proc.stderr?.on('data', (data: Buffer) => {
      stderr += data.toString()
    })

    // Set up timeout
    const timeoutId = setTimeout(() => {
      try {
        proc.kill('SIGTERM')
      } catch (e) {
        // Ignore
      }
      resolve({
        name: task.name,
        status: 'timeout',
        duration: Date.now() - startTime,
        error: `Exceeded ${timeoutSeconds}s timeout`
      })
    }, timeoutSeconds * 1000)

    proc.on('close', (code: number | null, signal: string | null) => {
      clearTimeout(timeoutId)

      if (signal === 'SIGTERM') {
        resolve({
          name: task.name,
          status: 'timeout',
          duration: Date.now() - startTime,
          error: `Exceeded ${timeoutSeconds}s timeout`
        })
        return
      }

      if (code === 0) {
        resolve({
          name: task.name,
          status: 'fulfilled',
          duration: Date.now() - startTime,
          value: stdout.trim() || 'Task completed successfully'
        })
      } else {
        resolve({
          name: task.name,
          status: 'rejected',
          duration: Date.now() - startTime,
          error: stderr.trim() || `Process exited with code ${code}`
        })
      }
    })

    proc.on('error', (err: Error) => {
      clearTimeout(timeoutId)
      resolve({
        name: task.name,
        status: 'rejected',
        duration: Date.now() - startTime,
        error: err.message
      })
    })
  })
}

/**
 * Execute multiple tasks with concurrency control
 */
async function executeParallel(
  tasks: Task[],
  options: Partial<ParallelOptions> = {}
): Promise<TaskResult[]> {
  const opts: ParallelOptions = {
    timeout: options.timeout || 300,
    stopOnError: options.stopOnError || false,
    reportProgress: options.reportProgress !== false,
    maxConcurrent: options.maxConcurrent || 5
  }

  console.log(colorize('cyan', `\n🚀 Starting ${tasks.length} tasks in parallel (max ${opts.maxConcurrent} concurrent)...\n`))

  const results: TaskResult[] = []
  const executing: Promise<void>[] = []
  let completed = 0

  // Use semaphore pattern for concurrency control
  async function runTask(task: Task): Promise<TaskResult> {
    const timeout = (task.timeout || opts.timeout)!

    if (opts.reportProgress) {
      console.log(colorize('blue', `🔄 [${task.name}] Starting (timeout: ${timeout}s)...`))
    }

    const result = await executeTaskViaSpawn(task, timeout)
    
    completed++
    const progress = `[${completed}/${tasks.length}]`
    
    if (result.status === 'fulfilled') {
      if (opts.reportProgress) {
        const duration = result.duration ? `(${(result.duration / 1000).toFixed(1)}s)` : ''
        console.log(colorize('green', `✅ ${progress} [${task.name}] Complete ${duration}`))
      }
    } else if (result.status === 'timeout') {
      console.log(colorize('yellow', `⏱️  ${progress} [${task.name}] Timeout after ${timeout}s`))
    } else {
      console.log(colorize('red', `❌ ${progress} [${task.name}] Failed: ${result.error}`))
    }

    return result
  }

  // Process tasks with concurrency limit
  for (let i = 0; i < tasks.length; i++) {
    const task = tasks[i]
    
    if (opts.stopOnError && results.some(r => r.status !== 'fulfilled')) {
      // Stop remaining tasks if stopOnError is enabled and a task failed
      while (executing.length > 0) {
        await Promise.race(executing)
      }
      break
    }

    const promise = runTask(task).then(result => {
      results.push(result)
      // Remove from executing list
      const idx = executing.indexOf(promise)
      if (idx > -1) executing.splice(idx, 1)
    })

    executing.push(promise)

    // If we've hit max concurrent, wait for one to complete
    if (executing.length >= opts.maxConcurrent) {
      await Promise.race(executing)
    }
  }

  // Wait for all remaining tasks
  await Promise.all(executing)

  return results
}

/**
 * Format results as a summary table
 */
function formatResults(results: TaskResult[]): string {
  const succeeded = results.filter(r => r.status === 'fulfilled').length
  const failed = results.filter(r => r.status !== 'fulfilled').length
  const totalDuration = results.reduce((sum, r) => sum + (r.duration || 0), 0)

  let output = '\n'
  output += colorize('green', '✅ Parallel Execution Complete') + '\n'
  output += `   ${results.length} tasks: ${colorize('green', `${succeeded} succeeded`)}, ${colorize('red', `${failed} failed`)}`
  if (totalDuration > 0) {
    output += ` (${(totalDuration / 1000).toFixed(1)}s total)`
  }
  output += '\n\n'

  // Table header
  const col1 = 'Task'
  const col2 = 'Status'
  const col3 = 'Duration'
  
  output += '┌' + '─'.repeat(21) + '┬' + '─'.repeat(12) + '┬' + '─'.repeat(12) + '┐\n'
  output += `│ ${col1.padEnd(19)} │ ${col2.padEnd(10)} │ ${col3.padEnd(10)} │\n`
  output += '├' + '─'.repeat(21) + '┼' + '─'.repeat(12) + '┼' + '─'.repeat(12) + '┤\n'

  for (const result of results) {
    const statusIcon = result.status === 'fulfilled' ? '✅' : 
                      result.status === 'timeout' ? '⏱️' : '❌'
    const statusColor = result.status === 'fulfilled' ? 'green' : 
                        result.status === 'timeout' ? 'yellow' : 'red'
    const duration = result.duration ? `${(result.status === 'timeout' ? result.duration / 1000 : result.duration / 1000).toFixed(1)}s` : '-'
    
    const name = result.name.slice(0, 19).padEnd(19)
    const status = `${statusIcon} ${result.status}`.padEnd(10)
    
    output += `│ ${colorize(statusColor as any, name)} │ ${colorize(statusColor as any, status)} │ ${duration.padStart(10)} │\n`
  }

  output += '└' + '─'.repeat(21) + '┴' + '─'.repeat(12) + '┴' + '─'.repeat(12) + '┘\n'

  // Error details
  const errors = results.filter(r => r.status !== 'fulfilled')
  if (errors.length > 0) {
    output += `\n${colorize('red', '❌ Failed Tasks:')}\n`
    for (const error of errors) {
      const errorMsg = error.error || 'Unknown error'
      output += `   • ${error.name}: ${errorMsg.slice(0, 100)}\n`
    }
  }

  return output
}

/**
 * Print help message
 */
function printHelp(): void {
  console.log(`
${colorize('cyan', '📋 Parallel Tasks Executor for OpenClaw')}

${colorize('yellow', 'Usage:')}
  node executor.ts [options] --task "Task 1" --task "Task 2" ...
  node executor.ts [options] "Task 1" "Task 2" "Task 3"

${colorize('yellow', 'Options:')}
  --task, -t <desc>      Task description (can be specified multiple times)
  --timeout, -to <sec>   Timeout per task in seconds (default: 300)
  --max-concurrent, -m   Maximum concurrent tasks (default: 5)
  --stop-on-error        Stop all tasks if one fails
  --no-progress          Suppress progress output
  --tasks-file, -f <file> Read tasks from file (one per line)
  --parse                Parse tasks from stdin and print JSON
  --help, -h            Show this help message

${colorize('yellow', 'Task Input Formats:')}
  Named:     [my-task] This is my task description
  Bullet:    - This is my task description
  Numbered:  1. This is my task description
  Plain:     This is my task description (auto-named as task-1, task-2, ...)

${colorize('yellow', 'Examples:')}
  # Simple usage
  node executor.ts "Research AI trends" "Research market analysis"

  # Named tasks with custom timeout
  node executor.ts --timeout 600 \\
    --task "[research] Research AI trends" \\
    --task "[implement] Build the feature"

  # Read from file
  node executor.ts --tasks-file my-tasks.txt --max-concurrent 3

${colorize('yellow', 'Environment Variables:')}
  DEBUG=true    Enable debug output

${colorize('yellow', 'Exit Codes:')}
  0   All tasks succeeded
  1   Some tasks failed or timed out
`)
}

// Main entry point
async function main() {
  try {
    const { tasks, options } = parseArgs()

    if (tasks.length === 0) {
      console.error(colorize('red', 'Error: No tasks specified. Use --help for usage information.'))
      process.exit(1)
    }

    if (process.env.DEBUG) {
      console.error(`[DEBUG] Parsed ${tasks.length} tasks`)
      console.error(`[DEBUG] Options:`, JSON.stringify(options, null, 2))
    }

    const results = await executeParallel(tasks, options)
    const failedCount = results.filter(r => r.status !== 'fulfilled').length

    console.log(formatResults(results))

    if (failedCount > 0) {
      console.log(colorize('yellow', `\n⚠️  ${failedCount} task(s) failed or timed out\n`))
      process.exit(1)
    } else {
      console.log(colorize('green', '\n✨ All tasks completed successfully!\n'))
      process.exit(0)
    }
  } catch (error) {
    console.error(colorize('red', `\nFatal error: ${error instanceof Error ? error.message : String(error)}\n`))
    if (process.env.DEBUG) {
      console.error(error)
    }
    process.exit(1)
  }
}

main()
