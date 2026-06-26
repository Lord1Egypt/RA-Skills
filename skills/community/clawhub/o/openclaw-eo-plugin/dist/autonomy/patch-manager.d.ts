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
export type PatchRisk = 'low' | 'medium' | 'high';
export type PatchStatus = 'pending' | 'approved' | 'rejected' | 'applied' | 'rolled_back';
export interface Patch {
    id: string;
    name: string;
    description: string;
    risk: PatchRisk;
    status: PatchStatus;
    createdAt: number;
    appliedAt?: number;
    rollbackAt?: number;
    content: string;
    target: string;
    score?: number;
    autoApply: boolean;
}
export interface PatchResult {
    success: boolean;
    patchId?: string;
    message: string;
    error?: string;
}
/**
 * Patch Manager - Manages evolution patches
 */
export declare class PatchManager {
    private patches;
    private reviewQueue;
    constructor();
    /**
     * Load patches from disk
     */
    private loadPatches;
    /**
     * Save a patch to disk
     */
    private savePatch;
    /**
     * Create a new patch from optimization result
     */
    createPatch(params: {
        name: string;
        description: string;
        content: string;
        target: string;
        risk?: PatchRisk;
        score?: number;
    }): Promise<PatchResult>;
    /**
     * Apply a patch
     */
    applyPatch(patchId: string): Promise<PatchResult>;
    /**
     * Reject a patch
     */
    rejectPatch(patchId: string, reason?: string): Promise<PatchResult>;
    /**
     * Rollback a patch
     */
    rollbackPatch(patchId: string): Promise<PatchResult>;
    /**
     * Get patches by status
     */
    getByStatus(status: PatchStatus): Patch[];
    /**
     * Get patches by risk level
     */
    getByRisk(risk: PatchRisk): Patch[];
    /**
     * Get review queue
     */
    getReviewQueue(): Patch[];
    /**
     * Get all patches
     */
    getAllPatches(): Patch[];
    /**
     * Get statistics
     */
    getStats(): {
        total: number;
        byStatus: Record<PatchStatus, number>;
        byRisk: Record<PatchRisk, number>;
        reviewQueueSize: number;
    };
    /**
     * Auto-generate patches from EffectTracker's low scores
     */
    generatePatchesFromLowScores(): Promise<PatchResult[]>;
}
export declare const patchManager: PatchManager;
//# sourceMappingURL=patch-manager.d.ts.map