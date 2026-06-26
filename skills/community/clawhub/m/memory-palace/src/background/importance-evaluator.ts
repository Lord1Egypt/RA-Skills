/**
 * Importance Evaluator
 *
 * Automatically evaluates memory importance based on multiple factors.
 */

/**
 * Keyword weight mapping
 */
const KEYWORD_WEIGHTS: Array<{ patterns: RegExp[]; weight: number }> = [
  // High importance
  { patterns: [/重要|关键|必须|核心|critical|important|must|key/i], weight: 0.3 },
  // Decision-related
  { patterns: [/决策|方案|确定|决定|decision/i], weight: 0.25 },
  // User preference
  { patterns: [/偏好|习惯|喜欢|prefer|like|habit/i], weight: 0.2 },
  // Problem-related
  { patterns: [/bug|错误|问题|error|issue/i], weight: 0.15 },
  // Low importance
  { patterns: [/一般|普通|临时|临时|normal|temp|普通/i], weight: -0.1 },
];

/**
 * Source type weights
 */
const SOURCE_WEIGHTS: Record<string, number> = {
  decision: 0.9,
  preference: 0.8,
  experience: 0.7,
  lesson: 0.6,
  fact: 0.5,
};

/**
 * Evaluation options
 */
export interface ImportanceEvaluationOptions {
  /** Memory type (affects base weight) */
  type?: string;
  /** Memory source */
  source?: string;
}

/**
 * Importance Evaluator
 */
export class ImportanceEvaluator {
  /**
   * Evaluate importance score
   * @param content - Memory content
   * @param options - Evaluation options
   * @returns Importance score (0-1)
   */
  evaluate(content: string, options: ImportanceEvaluationOptions = {}): number {
    // Factor 1: Content length score (0.3 weight)
    const lengthScore = Math.min(1, content.length / 500);

    // Factor 2: Keyword intensity score (0.4 weight)
    const keywordScore = this.calculateKeywordScore(content);

    // Factor 3: Source weight (0.3 weight)
    const sourceWeight = options.source
      ? SOURCE_WEIGHTS[options.source] ?? 0.5
      : 0.5;

    // Combine factors
    const rawScore = lengthScore * 0.3 + keywordScore * 0.4 + sourceWeight * 0.3;

    // Clamp to [0.1, 1.0]
    const score = Math.max(0.1, Math.min(1.0, rawScore));

    // Decision type gets minimum 0.8
    if (options.type === 'decision') {
      return Math.max(0.8, score);
    }

    return Math.round(score * 100) / 100; // Round to 2 decimals
  }

  /**
   * Calculate keyword intensity score
   */
  private calculateKeywordScore(content: string): number {
    let score = 0;

    for (const rule of KEYWORD_WEIGHTS) {
      for (const pattern of rule.patterns) {
        if (pattern.test(content)) {
          score += rule.weight;
          break; // Only count once per rule
        }
      }
    }

    // Clamp to [0, 1]
    return Math.max(0, Math.min(1, score));
  }

  /**
   * Check if user-specified importance should be overridden
   */
  shouldOverride(userImportance: number | undefined, content: string, options: ImportanceEvaluationOptions = {}): boolean {
    // Never override user-specified importance
    return userImportance === undefined;
  }
}

/**
 * Create an ImportanceEvaluator instance
 */
export function createImportanceEvaluator(): ImportanceEvaluator {
  return new ImportanceEvaluator();
}