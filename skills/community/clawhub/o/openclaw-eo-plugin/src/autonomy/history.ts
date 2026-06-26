/**
 * Decision History
 */

import type { Decision, Outcome } from './types.js'

interface HistoryEntry { decision: Decision; outcome?: Outcome; createdAt: number }

export class DecisionHistory {
  private history: Map<string, HistoryEntry> = new Map()
  private maxSize = 500

  add(decision: Decision, outcome?: Outcome): void {
    this.history.set(decision.id, { decision, outcome, createdAt: Date.now() })
    if (this.history.size > this.maxSize) this.prune()
  }

  get(id: string): HistoryEntry | undefined { return this.history.get(id) }
  getRecent(limit = 50): HistoryEntry[] {
    return Array.from(this.history.values()).sort((a, b) => b.createdAt - a.createdAt).slice(0, limit)
  }

  private prune(): void {
    const entries = Array.from(this.history.entries()).sort((a, b) => a[1].createdAt - b[1].createdAt)
    const toRemove = entries.slice(0, Math.floor(this.maxSize * 0.2))
    toRemove.forEach(([id]) => this.history.delete(id))
  }

  size(): number { return this.history.size }
  clear(): void { this.history.clear() }
}

export const decisionHistory = new DecisionHistory()
