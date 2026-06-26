// ============================================================================
// EO Context Loader - Load relevant historical context on session start
//
// When a new session starts, this module loads relevant historical context
// from past sessions so the agent isn't "amnesiac" about previous work.
// ============================================================================

import * as fs from 'fs'
import * as path from 'path'
import { logger } from '../utils/logger.js'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ContextLoadResult {
  sessionKey: string
  loaded: boolean
  contextItems: ContextItem[]
  memoryHints: string[]
  suggestions: string[]
}

export interface ContextItem {
  type: 'decision' | 'pattern' | 'recent_work' | 'preference'
  content: string
  sourceSession: string
  timestamp: number
  relevance: number
}

export interface ContextLoaderConfig {
  /** Maximum context items to load */
  maxItems: number
  /** Maximum age of context (ms) - older items won't be loaded */
  maxAgeMs: number
  /** Workspace root */
  workspaceRoot: string
  /** Memory file path */
  memoryPath: string
}

const DEFAULT_CONFIG: ContextLoaderConfig = {
  maxItems: 10,
  maxAgeMs: 30 * 24 * 60 * 60 * 1000, // 30 days
  workspaceRoot: process.cwd(),
  memoryPath: '.eo-dream/memory.json',
}

// ---------------------------------------------------------------------------
// Context Loader
// ---------------------------------------------------------------------------

export class ContextLoader {
  private config: ContextLoaderConfig

  constructor(config: Partial<ContextLoaderConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config }
  }

  // ---------------------------------------------------------------------------
  // Main Loading Function
  // ---------------------------------------------------------------------------

  /**
   * Load relevant context for a new session
   * 
   * @param currentSessionKey - The session that's starting
   * @param currentMessage - The message that triggered this session (optional)
   * @returns Context items that should be injected into the session
   */
  async loadContext(currentSessionKey: string, currentMessage?: string): Promise<ContextLoadResult> {
    const contextItems: ContextItem[] = []
    const memoryHints: string[] = []
    const suggestions: string[] = []

    logger.debug(`Loading context for session: ${currentSessionKey}`)

    try {
      // Step 1: Load dream memory (learnings from past sessions)
      const dreamMemory = this.loadDreamMemory()
      
      // Step 2: Load workspace memory files
      const workspaceMemory = this.loadWorkspaceMemory()

      // Step 3: Search for related sessions based on current message
      if (currentMessage) {
        const relatedSessions = await this.findRelatedSessions(currentMessage)
        
        for (const session of relatedSessions) {
          contextItems.push({
            type: 'recent_work',
            content: `最近会话 ${session.sessionKey}: ${session.summary || session.messages.slice(0, 3).map(m => m.content).join(' ')}`,
            sourceSession: session.sessionKey,
            timestamp: session.lastMessageAt,
            relevance: session.relevance,
          })
        }
      }

      // Step 4: Add recent decisions
      const recentDecisions = this.loadRecentDecisions()
      for (const decision of recentDecisions.slice(0, 3)) {
        contextItems.push({
          type: 'decision',
          content: `之前决定: ${decision.content}`,
          sourceSession: decision.sessionKey,
          timestamp: decision.timestamp,
          relevance: 0.9,
        })
        memoryHints.push(`决策记录: ${decision.content}`)
      }

      // Step 5: Add pattern-based context
      for (const insight of dreamMemory.slice(0, 5)) {
        if (Date.now() - insight.createdAt < this.config.maxAgeMs) {
          contextItems.push({
            type: 'pattern',
            content: `学习到: ${insight.content}`,
            sourceSession: 'dream-memory',
            timestamp: insight.createdAt,
            relevance: insight.confidence,
          })
        }
      }

      // Step 6: Generate suggestions based on patterns
      const patternCounts = this.countPatterns(dreamMemory)
      if (patternCounts.workflow > 5) {
        suggestions.push('你最近常用工作流模式，建议继续使用类似流程')
      }
      if (patternCounts.expert > 3) {
        suggestions.push('你经常使用多专家协作，这是一个好习惯')
      }

      // Limit context items
      const limitedItems = contextItems
        .sort((a, b) => b.relevance - a.relevance)
        .slice(0, this.config.maxItems)

      logger.debug(`Loaded ${limitedItems.length} context items`)

      return {
        sessionKey: currentSessionKey,
        loaded: true,
        contextItems: limitedItems,
        memoryHints,
        suggestions,
      }

    } catch (err) {
      console.error('[ContextLoader] Failed to load context:', err)
      return {
        sessionKey: currentSessionKey,
        loaded: false,
        contextItems: [],
        memoryHints: [],
        suggestions: [],
      }
    }
  }

  // ---------------------------------------------------------------------------
  // Helper Methods
  // ---------------------------------------------------------------------------

  private loadDreamMemory(): any[] {
    try {
      const memoryFile = path.join(this.config.workspaceRoot, this.config.memoryPath)
      if (fs.existsSync(memoryFile)) {
        const data = fs.readFileSync(memoryFile, 'utf-8')
        return JSON.parse(data)
      }
    } catch (e) {
      console.warn('[ContextLoader] Failed to load dream memory:', e)
    }
    return []
  }

  private loadWorkspaceMemory(): any {
    try {
      const memoryFiles = [
        path.join(this.config.workspaceRoot, 'MEMORY.md'),
        path.join(this.config.workspaceRoot, 'memory', '*.md'),
      ]

      for (const pattern of memoryFiles) {
        if (pattern.includes('*')) {
          const dir = path.dirname(pattern)
          const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'))
          // Read most recent
          const recent = files
            .map(f => ({ f, mtime: fs.statSync(path.join(dir, f)).mtime.getTime() }))
            .sort((a, b) => b.mtime - a.mtime)
            .slice(0, 3)
          
          if (recent.length > 0) {
            return recent.map(r => fs.readFileSync(path.join(dir, r.f), 'utf-8')).join('\n')
          }
        } else if (fs.existsSync(pattern)) {
          return fs.readFileSync(pattern, 'utf-8')
        }
      }
    } catch (e) {
      console.warn('[ContextLoader] Failed to load workspace memory:', e)
    }
    return ''
  }

  private loadRecentDecisions(): any[] {
    try {
      const archiveDir = path.join(this.config.workspaceRoot, '.eo-sessions')
      if (fs.existsSync(archiveDir)) {
        const indexFile = path.join(archiveDir, 'index.json')
        if (fs.existsSync(indexFile)) {
          const data = fs.readFileSync(indexFile, 'utf-8')
          const index = JSON.parse(data)
          if (Array.isArray(index.decisions)) {
            // Filter by age
            const cutoff = Date.now() - this.config.maxAgeMs
            return index.decisions.filter((d: any) => d.timestamp > cutoff)
          }
        }
      }
    } catch (e) {
      console.warn('[ContextLoader] Failed to load decisions:', e)
    }
    return []
  }

  private async findRelatedSessions(message: string): Promise<Array<{ sessionKey: string; summary?: string; messages: any[]; lastMessageAt: number; relevance: number }>> {
    const results: Array<{ sessionKey: string; summary?: string; messages: any[]; lastMessageAt: number; relevance: number }> = []
    const messageLower = message.toLowerCase()
    const keywords = this.extractKeywords(messageLower)

    try {
      const archiveDir = path.join(this.config.workspaceRoot, '.eo-sessions')
      if (!fs.existsSync(archiveDir)) return results

      const files = fs.readdirSync(archiveDir).filter(f => f.endsWith('.json') && f !== 'index.json')

      for (const file of files.slice(-50)) { // Check last 50 sessions
        try {
          const data = fs.readFileSync(path.join(archiveDir, file), 'utf-8')
          const session = JSON.parse(data)
          
          // Calculate relevance
          let relevance = 0
          const content = (session.summary || '') + ' ' + session.messages?.map((m: any) => m.content).join(' ') || ''
          
          for (const keyword of keywords) {
            if (content.toLowerCase().includes(keyword)) {
              relevance += 1
            }
          }

          // Also check for same session key pattern
          if (messageLower.includes(session.sessionKey?.toLowerCase() || '')) {
            relevance += 5
          }

          if (relevance > 0) {
            results.push({
              sessionKey: session.sessionKey || file.replace('.json', ''),
              summary: session.summary,
              messages: session.messages || [],
              lastMessageAt: session.lastMessageAt || Date.now(),
              relevance,
            })
          }
        } catch (e) {
          // Skip invalid session files
        }
      }
    } catch (e) {
      console.warn('[ContextLoader] Failed to search sessions:', e)
    }

    // Sort by relevance and return top 3
    return results.sort((a, b) => b.relevance - a.relevance).slice(0, 3)
  }

  private extractKeywords(text: string): string[] {
    // Simple keyword extraction - remove stop words
    const stopWords = new Set(['的', '是', '在', '和', '了', '我', '你', '他', '它', '这', '那', '有', '没有', '要', '不要', '一个', '什么', '怎么', '如何', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can'])
    
    return text
      .replace(/[^\w\s\u4e00-\u9fa5]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length > 2 && !stopWords.has(w.toLowerCase()))
      .slice(0, 10)
  }

  private countPatterns(dreamMemory: any[]): { workflow: number; expert: number; topic: number } {
    const counts = { workflow: 0, expert: 0, topic: 0 }
    for (const insight of dreamMemory) {
      if (insight.category === 'workflow') counts.workflow++
      else if (insight.category === 'expert') counts.expert++
      else if (insight.category === 'topic') counts.topic++
    }
    return counts
  }

  /**
   * Load and parse the "🔄 自进化学习" section from MEMORY.md
   * This extracts insights generated by DreamModule and makes them available
   * as historical context for new sessions.
   */
  loadSelfEvolutionLearnings(): ContextItem[] {
    const items: ContextItem[] = []
    
    try {
      const memoryPath = path.join(this.config.workspaceRoot, 'MEMORY.md')
      if (!fs.existsSync(memoryPath)) {
        return items
      }

      const content = fs.readFileSync(memoryPath, 'utf-8')
      
      // Find "🔄 自进化学习" section
      const sectionMatch = content.match(/## 🔄 自进化学习[\s\S]*?(?=\n---|$)/i)
      if (!sectionMatch) {
        return items
      }

      const section = sectionMatch[0]
      
      // Parse table rows: | emoji | content | confidence |
      const rowRegex = /\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|/g
      let match
      
      while ((match = rowRegex.exec(section)) !== null) {
        const emoji = match[1].trim()
        const contentText = match[2].trim()
        const confidence = match[3].trim()
        
        if (contentText && !contentText.includes('类型') && !contentText.includes('洞察')) {
          // Determine category from emoji
          // Map DreamModule categories to ContextItem categories
          let category: ContextItem['type'] = 'pattern'
          if (emoji.includes('⚙️')) category = 'preference'  // workflow learnings → preference
          else if (emoji.includes('📋')) category = 'decision'
          else if (emoji.includes('💡')) category = 'preference'
          else if (emoji.includes('📈')) category = 'pattern'
          
          // Extract timestamp from section header if available
          const timestampMatch = section.match(/(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})/)
          const timestamp = timestampMatch 
            ? new Date(timestampMatch[1]).getTime() 
            : Date.now() - 7 * 24 * 60 * 60 * 1000 // Default to 7 days ago
          
          items.push({
            type: category,
            content: contentText,
            sourceSession: 'MEMORY.md:自进化学习',
            timestamp,
            relevance: parseFloat(confidence.replace('%', '')) / 100 || 0.7,
          })
        }
      }
      
      logger.debug(`Loaded ${items.length} self-evolution learnings from MEMORY.md`)
    } catch (e) {
      console.warn('[ContextLoader] Failed to load self-evolution learnings:', e)
    }
    
    return items
  }
}

// ---------------------------------------------------------------------------
// Session Start Hook Integration
// ---------------------------------------------------------------------------

/**
 * Create a session_start hook that loads context
 */
export function createSessionStartHook(contextLoader: ContextLoader) {
  return {
    id: 'eo_context_loader',
    name: 'EO Context Loader',
    description: 'Loads relevant historical context when session starts',
    handle: async (event: any) => {
      const sessionKey = event.sessionKey || event.context?.sessionKey || 'unknown'
      
      logger.debug(`Session starting: ${sessionKey}`)
      
      const result = await contextLoader.loadContext(
        sessionKey,
        event.message?.content || event.context?.lastMessage
      )

      if (result.loaded && result.contextItems.length > 0) {
        // Inject context into event for downstream hooks/tools to use
        event.context = event.context || {}
        event.context.eoHistoricalContext = result.contextItems
        event.context.eoMemoryHints = result.memoryHints
        event.context.eoSuggestions = result.suggestions

        logger.debug(`Injected ${result.contextItems.length} context items`)
      }

      return event
    },
  }
}

// ---------------------------------------------------------------------------
// Convenience Export
// ---------------------------------------------------------------------------

let globalContextLoader: ContextLoader | null = null

export function getContextLoader(config?: Partial<ContextLoaderConfig>): ContextLoader {
  if (!globalContextLoader) {
    globalContextLoader = new ContextLoader(config)
  }
  return globalContextLoader
}
