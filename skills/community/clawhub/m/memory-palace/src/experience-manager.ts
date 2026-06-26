/**
 * Memory Palace - Experience Manager
 * 
 * Manages experience accumulation and application for AI agents.
 * Enables agents to learn from past experiences like humans.
 */

import { v4 as uuidv4 } from 'uuid';
import type {
  Memory,
  RecordExperienceOptions,
  GetExperiencesOptions,
  VerifyExperienceOptions,
  ExperienceCategory,
  GetRelevantParams,
  VerifiedExperienceResult,
} from './types.js';
import { MemoryPalaceManager } from './manager.js';
import { ExperienceExtractor, defaultExtractor } from './llm/experience-extractor.js';
import type { ExtractedExperience } from './llm/types.js';
import { FileStorage } from './storage.js';

/**
 * ExperienceManager - Manages experience accumulation lifecycle
 * 
 * Features:
 * - Record new experiences with category and applicability
 * - Get relevant experiences based on context
 * - Verify experience effectiveness
 * - Extract experiences from existing memories using LLM
 */
export class ExperienceManager {
  private manager: MemoryPalaceManager;
  private extractor: ExperienceExtractor;
  private storage: FileStorage;

  constructor(manager: MemoryPalaceManager, extractor?: ExperienceExtractor) {
    this.manager = manager;
    this.extractor = extractor ?? defaultExtractor;
    this.storage = new FileStorage(manager.getStoragePath());
  }

  /**
   * Record a new experience
   * 
   * @param options Experience recording options
   * @returns The created memory with experience metadata
   */
  async recordExperience(options: RecordExperienceOptions): Promise<Memory> {
    const now = new Date();
    const category = options.category || 'general';
    
    // Ensure 'experience' tag is included
    const tags = [...new Set(['experience', ...(options.tags || [])])];
    
    // Create memory with experience metadata
    const memory = await this.manager.store({
      content: options.content,
      location: options.location || 'experiences',
      tags,
      importance: options.importance ?? 0.7, // Default higher importance for experiences
      type: 'experience',
      experienceMeta: {
        category,
        applicability: options.applicability,
        source: options.source,
        verified: false,
        verifiedCount: 0,
        effectivenessScore: 0.1, // Initialize to minimum score
        usageCount: 0,
      },
    });

    return memory;
  }

  /**
   * Get experiences matching criteria
   * 
   * @param options Filter options
   * @returns Array of matching experience memories
   */
  async getExperiences(options: GetExperiencesOptions = {}): Promise<Memory[]> {
    const { category, applicability, verified, limit = 10, sortByVerified } = options;

    // List all experiences
    const memories = await this.manager.list({
      location: 'experiences',
      limit: 1000, // Get all first, filter later
    });

    // Filter by type='experience'
    let experiences = memories.filter(m => m.type === 'experience');

    // Filter by category
    if (category) {
      const categoryStr = String(category).toLowerCase();
      experiences = experiences.filter(m => 
        String(m.experienceMeta?.category).toLowerCase() === categoryStr
      );
    }

    // Filter by applicability (partial match)
    if (applicability) {
      const lowerApplicability = applicability.toLowerCase();
      experiences = experiences.filter(m => 
        m.experienceMeta?.applicability.toLowerCase().includes(lowerApplicability) ||
        m.content.toLowerCase().includes(lowerApplicability)
      );
    }

    // Filter by verified status
    if (verified !== undefined) {
      experiences = experiences.filter(m => 
        m.experienceMeta?.verified === verified
      );
    }

    // Sort by effectivenessScore (default), or by verification count if requested
    if (sortByVerified) {
      experiences.sort((a, b) => 
        (b.experienceMeta?.verifiedCount || 0) - (a.experienceMeta?.verifiedCount || 0)
      );
    } else {
      // Default: sort by effectivenessScore descending
      experiences.sort((a, b) => 
        (b.experienceMeta?.effectivenessScore || 0) - (a.experienceMeta?.effectivenessScore || 0)
      );
    }
    
    // Increment usageCount and update lastUsedAt for queried experiences
    const now = new Date();
    for (const exp of experiences) {
      if (exp.experienceMeta) {
        exp.experienceMeta.usageCount = (exp.experienceMeta.usageCount || 0) + 1;
        exp.experienceMeta.lastUsedAt = now;
        // Update effectivenessScore
        exp.experienceMeta.effectivenessScore = Math.min(1, 
          (exp.experienceMeta.verifiedCount || 0) * 0.3 + 
          exp.experienceMeta.usageCount * 0.1
        );
        // Save the update asynchronously
        this.storage.save(exp).catch(() => {});
      }
    }

    return experiences.slice(0, limit);
  }

  /**
   * Verify an experience's effectiveness
   * 
   * @param options Verification options
   * @returns Updated memory or null if not found
   */
  async verifyExperience(options: VerifyExperienceOptions): Promise<VerifiedExperienceResult | null> {
    const { id, effective } = options;

    // Get the experience
    const memory = await this.manager.get(id);
    if (!memory || memory.type !== 'experience' || !memory.experienceMeta) {
      return null;
    }

    // Update verification status
    const newVerifiedCount = (memory.experienceMeta.verifiedCount || 0) + 1;
    const newVerified = effective 
      ? memory.experienceMeta.verified || newVerifiedCount >= 2 // Require at least 2 verifications
      : memory.experienceMeta.verified;

    // Update importance based on effectiveness
    const newImportance = effective 
      ? Math.min(1, memory.importance + 0.05) // Boost importance if effective
      : Math.max(0.3, memory.importance - 0.1); // Reduce if not effective

    // Calculate new effectivenessScore: Math.min(1, verifiedCount * 0.3 + usageCount * 0.1)
    const newEffectivenessScore = Math.min(1, 
      newVerifiedCount * 0.3 + 
      (memory.experienceMeta?.usageCount || 0) * 0.1
    );

    // Update the memory
    const updatedMemory: Memory = {
      ...memory,
      importance: newImportance,
      updatedAt: new Date(),
      experienceMeta: {
        ...memory.experienceMeta,
        verified: newVerified,
        verifiedCount: newVerifiedCount,
        lastVerifiedAt: new Date(),
        effectivenessScore: newEffectivenessScore,
      },
    };

    // Save directly to storage
    await this.storage.save(updatedMemory);

    // Return with shortcut fields for convenience
    return {
      ...updatedMemory,
      verified: updatedMemory.experienceMeta?.verified ?? false,
      verifiedCount: updatedMemory.experienceMeta?.verifiedCount ?? 0,
      verifiedAt: updatedMemory.experienceMeta?.lastVerifiedAt,
    };
  }

  /**
   * Extract experiences from existing memories using LLM
   * 
   * @param memories Memories to analyze
   * @param options Extraction options
   * @returns Array of newly created experience memories
   */
  async extractFromMemories(
    memories: Memory[],
    options?: { category?: ExperienceCategory | string; source?: string }
  ): Promise<Memory[]> {
    if (memories.length === 0) {
      return [];
    }

    // Use LLM to extract experiences
    const result = await this.extractor.extract(memories);

    if (!result.success || !result.data || result.data.length === 0) {
      return [];
    }

    // Convert extracted experiences to memories
    const createdExperiences: Memory[] = [];
    
    for (const extracted of result.data) {
      try {
        const memory = await this.recordExperience({
          content: extracted.experience,
          category: options?.category || this.inferCategory(extracted),
          applicability: extracted.context,
          source: options?.source || 'extracted',
          tags: extracted.relatedTopics,
        });
        createdExperiences.push(memory);
      } catch (error) {
        // Continue on individual failures
        console.error('Failed to create experience from extracted:', error);
      }
    }

    return createdExperiences;
  }

  /**
   * Infer category from extracted experience
   */
  private inferCategory(extracted: ExtractedExperience): string {
    const text = `${extracted.experience} ${extracted.relatedTopics.join(' ')}`.toLowerCase();
    
    if (text.includes('代码') || text.includes('开发') || text.includes('编程') || 
        text.includes('typescript') || text.includes('python') || text.includes('rust')) {
      return 'development';
    }
    if (text.includes('运维') || text.includes('部署') || text.includes('服务器') ||
        text.includes('docker') || text.includes('k8s')) {
      return 'operations';
    }
    if (text.includes('产品') || text.includes('用户') || text.includes('需求') ||
        text.includes('功能') || text.includes('设计')) {
      return 'product';
    }
    if (text.includes('沟通') || text.includes('会议') || text.includes('协作') ||
        text.includes('团队')) {
      return 'communication';
    }
    
    return 'general';
  }

  /**
   * Get relevant experiences for a given context
   * 
   * @param params - Object-style: { context, limit? } or legacy (context, limit)
   * @returns Relevant experiences sorted by relevance
   * @deprecated Use getRelevantExperiences({ context, limit }) for object-style API
   */
  async getRelevantExperiences(
    contextOrParams: string | GetRelevantParams,
    limit?: number
  ): Promise<Memory[]> {
    // Handle backward compatibility - accept string or object
    const context = typeof contextOrParams === 'string' ? contextOrParams : contextOrParams.context;
    // For object style, use limit from object or fallback to parameter
    const limitNum = typeof contextOrParams === 'string' 
      ? (limit ?? 5) 
      : (contextOrParams.limit ?? limit ?? 5);
    
    // Search experiences matching the context
    const results = await this.manager.recall(context, {
      location: 'experiences',
      topK: limitNum * 2,
    });

    // Filter to only experience type
    const experiences = results
      .filter(r => r.memory.type === 'experience')
      .map(r => r.memory);

    // Update usage metrics for these experiences
    const now = new Date();
    for (const exp of experiences) {
      if (exp.experienceMeta) {
        exp.experienceMeta.usageCount = (exp.experienceMeta.usageCount || 0) + 1;
        exp.experienceMeta.lastUsedAt = now;
        // Update effectivenessScore
        exp.experienceMeta.effectivenessScore = Math.min(1, 
          (exp.experienceMeta.verifiedCount || 0) * 0.3 + 
          exp.experienceMeta.usageCount * 0.1
        );
        // Save the update asynchronously
        this.storage.save(exp).catch(() => {});
      }
    }

    // Boost verified experiences
    experiences.sort((a, b) => {
      const aScore = (a.experienceMeta?.verified ? 1 : 0) + (a.experienceMeta?.verifiedCount || 0) * 0.1;
      const bScore = (b.experienceMeta?.verified ? 1 : 0) + (b.experienceMeta?.verifiedCount || 0) * 0.1;
      return bScore - aScore;
    });

    return experiences.slice(0, limit);
  }

  /**
   * Get statistics about experiences
   */
  async getExperienceStats(): Promise<{
    total: number;
    byCategory: Record<string, number>;
    verified: number;
    avgVerifiedCount: number;
  }> {
    const experiences = await this.getExperiences({ limit: 1000 });
    
    const byCategory: Record<string, number> = {};
    let verified = 0;
    let totalVerifiedCount = 0;

    for (const exp of experiences) {
      if (exp.experienceMeta) {
        const cat = exp.experienceMeta.category;
        byCategory[cat] = (byCategory[cat] || 0) + 1;
        
        if (exp.experienceMeta.verified) {
          verified++;
        }
        totalVerifiedCount += exp.experienceMeta.verifiedCount || 0;
      }
    }

    return {
      total: experiences.length,
      byCategory,
      verified,
      avgVerifiedCount: experiences.length > 0 ? totalVerifiedCount / experiences.length : 0,
    };
  }
}

/**
 * Create an ExperienceManager instance
 */
export function createExperienceManager(
  manager: MemoryPalaceManager,
  extractor?: ExperienceExtractor
): ExperienceManager {
  return new ExperienceManager(manager, extractor);
}