// ============================================================================
// EO Session Archiver - 读取、索引、分析历史会话
// ============================================================================

import * as fs from 'fs'
import * as path from 'path'
import { logger } from '../utils/logger.js'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface SessionArchive {
  sessionKey: string
  workspace: string
  lastMessageAt: number
  messageCount: number
  messages: SessionMessage[]
  summary?: string
  tags: string[]
}

export interface SessionMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: number
  tools?: string[]
}

export interface ArchiveIndex {
  lastIndexedAt: number
  sessionCount: number
  totalMessages: number
  topics: Map<string, TopicEntry>
  decisions: Decision[]
  patterns: Pattern[]
}

export interface TopicEntry {
  topic: string
  sessionKeys: string[]
  lastDiscussedAt: number
  messageCount: number
}

export interface Decision {
  id: string
  content: string
  sessionKey: string
  timestamp: number
  confirmed: boolean
}

export interface Pattern {
  id: string
  type: 'workflow' | 'command' | 'expert' | 'topic'
  description: string
  occurrences: number
  lastSeenAt: number
  sessions: string[]
}

// ---------------------------------------------------------------------------
// Session Archiver
// ---------------------------------------------------------------------------

export class SessionArchiver {
  private workspaceRoot: string
  private archiveDir: string
  private indexPath: string
  private archiveIndex: ArchiveIndex

  constructor(workspaceRoot: string) {
    this.workspaceRoot = workspaceRoot
    this.archiveDir = path.join(workspaceRoot, '.eo-sessions')
    this.indexPath = path.join(this.archiveDir, 'index.json')
    this.archiveIndex = this.loadIndex()
  }

  // ---------------------------------------------------------------------------
  // Index Management
  // ---------------------------------------------------------------------------

  private loadIndex(): ArchiveIndex {
    try {
      if (fs.existsSync(this.indexPath)) {
        const data = fs.readFileSync(this.indexPath, 'utf-8')
        const parsed = JSON.parse(data)
        // Reconstruct Map from array
        parsed.topics = new Map(parsed.topics)
        return parsed
      }
    } catch (e) {
      console.error('[SessionArchiver] Failed to load index:', e)
    }
    return {
      lastIndexedAt: 0,
      sessionCount: 0,
      totalMessages: 0,
      topics: new Map(),
      decisions: [],
      patterns: [],
    }
  }

  private saveIndex(): void {
    try {
      fs.mkdirSync(this.archiveDir, { recursive: true })
      const data = {
        ...this.archiveIndex,
        topics: Array.from(this.archiveIndex.topics.entries()),
      }
      fs.writeFileSync(this.indexPath, JSON.stringify(data, null, 2))
    } catch (e) {
      console.error('[SessionArchiver] Failed to save index:', e)
    }
  }

  // ---------------------------------------------------------------------------
  // Session Reading
  // ---------------------------------------------------------------------------

  /**
   * Read session messages from OpenClaw session storage
   * Assumes OpenClaw stores sessions in ~/.openclaw/sessions/ or workspace
   */
  async readSession(sessionKey: string): Promise<SessionArchive | null> {
    // Try to find session in OpenClaw's session storage
    const possiblePaths = [
      path.join(process.env.HOME || '/home/zzy', '.openclaw', 'sessions', `${sessionKey}.json`),
      path.join(this.workspaceRoot, '.openclaw', 'sessions', `${sessionKey}.json`),
      path.join(this.workspaceRoot, 'memory', `${sessionKey}.json`),
    ]

    for (const sessionPath of possiblePaths) {
      if (fs.existsSync(sessionPath)) {
        try {
          const data = fs.readFileSync(sessionPath, 'utf-8')
          const session = JSON.parse(data)
          return this.normalizeSession(session, sessionKey, sessionPath)
        } catch (e) {
          console.warn(`[SessionArchiver] Failed to read session from ${sessionPath}:`, e)
        }
      }
    }

    // No session file found - return null
    return null
  }

  /**
   * Normalize session data from various formats
   * Supports nested format: { type: 'message', message: { role: 'user', content: [{ type: 'text', text: '...' }] } }
   */
  private normalizeSession(raw: any, sessionKey: string, sourcePath: string): SessionArchive {
    const messages: SessionMessage[] = []
    
    // Handle different message formats
    if (Array.isArray(raw.messages)) {
      for (const msg of raw.messages) {
        // Check for nested format: msg.message.role, msg.message.content
        const role = msg.message?.role || msg.role || 'user'
        const content = this.extractContent(msg.message?.content || msg.content || msg.text || msg.message || '')
        
        messages.push({
          role: role as 'user' | 'assistant' | 'system',
          content,
          timestamp: msg.timestamp || Date.now(),
          tools: msg.tools || msg.tool_calls,
        })
      }
    }

    return {
      sessionKey,
      workspace: path.dirname(sourcePath),
      lastMessageAt: raw.lastMessageAt || raw.updatedAt || Date.now(),
      messageCount: messages.length,
      messages,
      summary: raw.summary,
      tags: raw.tags || [],
    }
  }

  /**
   * Extract text content from various content formats
   * Handles Array.isArray(content) format: [{ type: 'text', text: '...' }, ...]
   */
  private extractContent(content: string | any[]): string {
    if (typeof content === 'string') {
      return content
    }
    
    if (Array.isArray(content)) {
      // Extract all text fields from content blocks
      const texts: string[] = []
      for (const block of content) {
        if (block && typeof block === 'object') {
          if (block.type === 'text' && typeof block.text === 'string') {
            texts.push(block.text)
          } else if (typeof block.text === 'string') {
            // Some formats have text directly in the block
            texts.push(block.text)
          } else if (block.content && typeof block.content === 'string') {
            texts.push(block.content)
          }
        }
      }
      if (texts.length > 0) {
        return texts.join('\n')
      }
    }
    
    // Fallback: try to stringify
    if (content && typeof content === 'object') {
      return JSON.stringify(content)
    }
    
    return String(content || '')
  }

  // ---------------------------------------------------------------------------
  // Session Indexing
  // ---------------------------------------------------------------------------

  /**
   * Index a session - extract topics, decisions, patterns
   */
  async indexSession(sessionKey: string): Promise<void> {
    const session = await this.readSession(sessionKey)
    if (!session) {
      console.warn(`[SessionArchiver] No session data found for ${sessionKey}`)
      return
    }

    // Extract topics from messages
    this.extractTopics(session)

    // Extract decisions
    this.extractDecisions(session)

    // Extract patterns
    this.extractPatterns(session)

    // Update stats
    this.archiveIndex.lastIndexedAt = Date.now()
    this.archiveIndex.sessionCount++
    this.archiveIndex.totalMessages += session.messageCount

    this.saveIndex()
    logger.debug(`Indexed session ${sessionKey}: ${session.messageCount} messages`)
  }

  /**
   * Extract topics from session messages
   */
  private extractTopics(session: SessionArchive): void {
    // Simple keyword-based topic extraction
    const topicKeywords = [
      { topic: '代码开发', keywords: ['代码', '开发', 'function', 'class', 'implement'] },
      { topic: '架构设计', keywords: ['架构', '设计', 'architecture', 'system design'] },
      { topic: '论文写作', keywords: ['论文', 'paper', 'writing', 'academic'] },
      { topic: '项目规划', keywords: ['规划', 'plan', 'WBS', '里程碑'] },
      { topic: '多专家协作', keywords: ['专家', 'expert', 'collaboration', '协作'] },
      { topic: '插件配置', keywords: ['插件', 'plugin', '配置', 'config'] },
      { topic: 'Bug修复', keywords: ['bug', '修复', 'fix', 'error'] },
    ]

    const content = session.messages.map(m => m.content).join(' ').toLowerCase()

    for (const { topic, keywords } of topicKeywords) {
      const matches = keywords.filter(kw => content.includes(kw.toLowerCase())).length
      if (matches > 0) {
        const existing = this.archiveIndex.topics.get(topic)
        if (existing) {
          if (!existing.sessionKeys.includes(session.sessionKey)) {
            existing.sessionKeys.push(session.sessionKey)
          }
          existing.messageCount += matches
          existing.lastDiscussedAt = Math.max(existing.lastDiscussedAt, session.lastMessageAt)
        } else {
          this.archiveIndex.topics.set(topic, {
            topic,
            sessionKeys: [session.sessionKey],
            lastDiscussedAt: session.lastMessageAt,
            messageCount: matches,
          })
        }
      }
    }
  }

  /**
   * Extract decisions from session
   */
  private extractDecisions(session: SessionArchive): void {
    // Look for decision indicators
    const decisionPatterns = [
      /决定\s*[是为]?\s*(.+)/gi,
      /采用\s*(.+?)\s*方案/gi,
      /用\s*(.+?)\s*来实现/gi,
      /选择\s*(.+?)\s*作为/gi,
    ]

    for (const msg of session.messages) {
      for (const pattern of decisionPatterns) {
        const matches = msg.content.matchAll(pattern)
        for (const match of matches) {
          const decision: Decision = {
            id: `dec-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
            content: match[1] || match[0],
            sessionKey: session.sessionKey,
            timestamp: msg.timestamp,
            confirmed: msg.role === 'assistant',
          }
          this.archiveIndex.decisions.push(decision)
        }
      }
    }
  }

  /**
   * Extract workflow patterns
   */
  private extractPatterns(session: SessionArchive): void {
    // Look for command patterns
    const commandPattern = /\/(\w+)/g
    const toolsUsed = new Set<string>()

    for (const msg of session.messages) {
      if (msg.tools) {
        msg.tools.forEach(t => toolsUsed.add(t))
      }
      const matches = msg.content.matchAll(commandPattern)
      for (const match of matches) {
        const command = match[1]
        this.recordPattern('command', command, session.sessionKey)
      }
    }

    // Record tool usage patterns
    toolsUsed.forEach(tool => {
      this.recordPattern('workflow', `tool:${tool}`, session.sessionKey)
    })
  }

  private recordPattern(type: Pattern['type'], description: string, sessionKey: string): void {
    const existing = this.archiveIndex.patterns.find(
      p => p.type === type && p.description === description
    )
    if (existing) {
      if (!existing.sessions.includes(sessionKey)) {
        existing.sessions.push(sessionKey)
        existing.occurrences++
      }
      existing.lastSeenAt = Date.now()
    } else {
      this.archiveIndex.patterns.push({
        id: `pat-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
        type,
        description,
        occurrences: 1,
        lastSeenAt: Date.now(),
        sessions: [sessionKey],
      })
    }
  }

  // ---------------------------------------------------------------------------
  // Query Methods
  // ---------------------------------------------------------------------------

  /**
   * Get sessions related to a topic
   */
  getSessionsForTopic(topic: string): string[] {
    const entry = this.archiveIndex.topics.get(topic)
    return entry?.sessionKeys || []
  }

  /**
   * Get recent decisions
   */
  getRecentDecisions(limit = 10): Decision[] {
    return this.archiveIndex.decisions
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, limit)
  }

  /**
   * Get top patterns
   */
  getTopPatterns(type?: Pattern['type'], limit = 10): Pattern[] {
    let patterns = this.archiveIndex.patterns
    if (type) {
      patterns = patterns.filter(p => p.type === type)
    }
    return patterns
      .sort((a, b) => b.occurrences - a.occurrences)
      .slice(0, limit)
  }

  /**
   * Get archive statistics
   */
  getStats(): { sessionCount: number; totalMessages: number; topicCount: number; patternCount: number } {
    return {
      sessionCount: this.archiveIndex.sessionCount,
      totalMessages: this.archiveIndex.totalMessages,
      topicCount: this.archiveIndex.topics.size,
      patternCount: this.archiveIndex.patterns.length,
    }
  }

  /**
   * Search sessions by keyword
   */
  async searchSessions(query: string, limit = 10): Promise<SessionArchive[]> {
    const results: SessionArchive[] = []
    const queryLower = query.toLowerCase()

    // Read all session files in archive directory
    if (fs.existsSync(this.archiveDir)) {
      const files = fs.readdirSync(this.archiveDir).filter(f => f.endsWith('.json') && f !== 'index.json')
      
      for (const file of files.slice(0, 100)) { // Limit to 100 files
        try {
          const data = fs.readFileSync(path.join(this.archiveDir, file), 'utf-8')
          const session: SessionArchive = JSON.parse(data)
          
          // Simple keyword search in messages
          const content = session.messages.map(m => m.content).join(' ').toLowerCase()
          if (content.includes(queryLower)) {
            results.push(session)
            if (results.length >= limit) break
          }
        } catch (e) {
          // Skip invalid files
        }
      }
    }

    return results
  }

  /**
   * Get full archive index
   */
  getArchiveIndex(): ArchiveIndex {
    return this.archiveIndex
  }
}

// ---------------------------------------------------------------------------
// Convenience Export
// ---------------------------------------------------------------------------

export function createSessionArchiver(workspaceRoot: string): SessionArchiver {
  return new SessionArchiver(workspaceRoot)
}
