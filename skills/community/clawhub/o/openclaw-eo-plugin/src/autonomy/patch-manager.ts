/**
 * Patch Manager - Manages automatic patch application
 * 
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve
 * 
 * Handles:
 * - Low-risk patches: auto-apply
 * - Medium-risk patches: review queue
 * - High-risk patches: manual approval required
 */

import { effectTracker } from '../autonomy/index.js'
import { patchLogger } from '../utils/logger.js'
import fs from 'fs/promises'
import path from 'path'

export type PatchRisk = 'low' | 'medium' | 'high'
export type PatchStatus = 'pending' | 'approved' | 'rejected' | 'applied' | 'rolled_back'

export interface Patch {
  id: string
  name: string
  description: string
  risk: PatchRisk
  status: PatchStatus
  createdAt: number
  appliedAt?: number
  rollbackAt?: number
  content: string // The actual patch content
  target: string // File or module to patch
  score?: number // EffectScore that triggered this patch
  autoApply: boolean // Can be auto-applied?
}

export interface PatchResult {
  success: boolean
  patchId?: string
  message: string
  error?: string
}

const PATCH_DIR = path.join(process.cwd(), '.eo-patches')

/**
 * Patch Manager - Manages evolution patches
 */
export class PatchManager {
  private patches: Map<string, Patch> = new Map()
  private reviewQueue: string[] = [] // Patches waiting for review

  constructor() {
    this.loadPatches()
  }

  /**
   * Load patches from disk
   */
  private async loadPatches(): Promise<void> {
    try {
      const files = await fs.readdir(PATCH_DIR)
      for (const file of files) {
        if (file.endsWith('.json')) {
          const content = await fs.readFile(path.join(PATCH_DIR, file), 'utf-8')
          const patch = JSON.parse(content) as Patch
          this.patches.set(patch.id, patch)
          if (patch.status === 'pending' && patch.risk !== 'low') {
            this.reviewQueue.push(patch.id)
          }
        }
      }
      patchLogger.info(`Loaded ${this.patches.size} patches`);
    } catch {
      // Directory doesn't exist yet
      patchLogger.info('No patches directory found, starting fresh');
    }
  }

  /**
   * Save a patch to disk
   */
  private async savePatch(patch: Patch): Promise<void> {
    await fs.mkdir(PATCH_DIR, { recursive: true })
    await fs.writeFile(
      path.join(PATCH_DIR, `${patch.id}.json`),
      JSON.stringify(patch, null, 2),
      'utf-8'
    )
  }

  /**
   * Create a new patch from optimization result
   */
  async createPatch(params: {
    name: string
    description: string
    content: string
    target: string
    risk?: PatchRisk
    score?: number
  }): Promise<PatchResult> {
    const { name, description, content, target, risk = 'medium', score } = params

    // Auto-apply low-risk patches
    const autoApply = risk === 'low'

    const patch: Patch = {
      id: `patch_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      name,
      description,
      risk,
      status: autoApply ? 'pending' : 'pending',
      createdAt: Date.now(),
      content,
      target,
      score,
      autoApply,
    }

    this.patches.set(patch.id, patch)
    await this.savePatch(patch)

    if (autoApply) {
      // Immediately apply low-risk patches
      return this.applyPatch(patch.id)
    } else {
      // Add to review queue
      this.reviewQueue.push(patch.id)
      return {
        success: true,
        patchId: patch.id,
        message: `Patch created: ${name} (${risk} risk) - added to review queue`,
      }
    }
  }

  /**
   * Apply a patch
   */
  async applyPatch(patchId: string): Promise<PatchResult> {
    const patch = this.patches.get(patchId)
    if (!patch) {
      return { success: false, message: `Patch not found: ${patchId}` }
    }

    if (patch.status === 'applied') {
      return { success: false, patchId, message: 'Patch already applied' }
    }

    try {
      // In a real implementation, this would apply the patch
      // For now, just mark as applied
      patch.status = 'applied'
      patch.appliedAt = Date.now()
      await this.savePatch(patch)

      patchLogger.info(`Applied patch: ${patch.name}`);
      return {
        success: true,
        patchId,
        message: `Patch applied: ${patch.name}`,
      }
    } catch (error) {
      return {
        success: false,
        patchId,
        message: 'Failed to apply patch',
        error: error instanceof Error ? error.message : String(error),
      }
    }
  }

  /**
   * Reject a patch
   */
  async rejectPatch(patchId: string, reason?: string): Promise<PatchResult> {
    const patch = this.patches.get(patchId)
    if (!patch) {
      return { success: false, message: `Patch not found: ${patchId}` }
    }

    patch.status = 'rejected'
    await this.savePatch(patch)

    // Remove from review queue
    this.reviewQueue = this.reviewQueue.filter(id => id !== patchId)

    return {
      success: true,
      patchId,
      message: `Patch rejected: ${patch.name}${reason ? ` (${reason})` : ''}`,
    }
  }

  /**
   * Rollback a patch
   */
  async rollbackPatch(patchId: string): Promise<PatchResult> {
    const patch = this.patches.get(patchId)
    if (!patch) {
      return { success: false, message: `Patch not found: ${patchId}` }
    }

    if (patch.status !== 'applied') {
      return { success: false, patchId, message: 'Cannot rollback non-applied patch' }
    }

    patch.status = 'rolled_back'
    patch.rollbackAt = Date.now()
    await this.savePatch(patch)

    return {
      success: true,
      patchId,
      message: `Patch rolled back: ${patch.name}`,
    }
  }

  /**
   * Get patches by status
   */
  getByStatus(status: PatchStatus): Patch[] {
    return Array.from(this.patches.values()).filter(p => p.status === status)
  }

  /**
   * Get patches by risk level
   */
  getByRisk(risk: PatchRisk): Patch[] {
    return Array.from(this.patches.values()).filter(p => p.risk === risk)
  }

  /**
   * Get review queue
   */
  getReviewQueue(): Patch[] {
    return this.reviewQueue.map(id => this.patches.get(id)!).filter(Boolean)
  }

  /**
   * Get all patches
   */
  getAllPatches(): Patch[] {
    return Array.from(this.patches.values())
  }

  /**
   * Get statistics
   */
  getStats(): {
    total: number
    byStatus: Record<PatchStatus, number>
    byRisk: Record<PatchRisk, number>
    reviewQueueSize: number
  } {
    const patches = Array.from(this.patches.values())
    return {
      total: patches.length,
      byStatus: {
        pending: patches.filter(p => p.status === 'pending').length,
        approved: patches.filter(p => p.status === 'approved').length,
        rejected: patches.filter(p => p.status === 'rejected').length,
        applied: patches.filter(p => p.status === 'applied').length,
        rolled_back: patches.filter(p => p.status === 'rolled_back').length,
      },
      byRisk: {
        low: patches.filter(p => p.risk === 'low').length,
        medium: patches.filter(p => p.risk === 'medium').length,
        high: patches.filter(p => p.risk === 'high').length,
      },
      reviewQueueSize: this.reviewQueue.length,
    }
  }

  /**
   * Auto-generate patches from EffectTracker's low scores
   */
  async generatePatchesFromLowScores(): Promise<PatchResult[]> {
    const results: PatchResult[] = []
    const stats = effectTracker.stats()

    // If average score is low, generate optimization patches
    if (stats.avgScore < 70) {
      const patch = await this.createPatch({
        name: 'Strategy Optimization',
        description: `Average score is ${stats.avgScore.toFixed(1)}, below threshold. Consider strategy adjustment.`,
        content: JSON.stringify({ strategy: 'conservative' }),
        target: 'optimizer',
        risk: stats.avgScore < 50 ? 'high' : 'medium',
        score: stats.avgScore,
      })
      results.push(patch)
    }

    // Check for declining trend
    if (stats.trend === 'declining') {
      const patch = await this.createPatch({
        name: 'Investigate Decline',
        description: 'Score trend is declining. Root cause analysis recommended.',
        content: JSON.stringify({ action: 'investigate' }),
        target: 'trend-analysis',
        risk: 'medium',
      })
      results.push(patch)
    }

    return results
  }
}

// Export singleton
export const patchManager = new PatchManager()
