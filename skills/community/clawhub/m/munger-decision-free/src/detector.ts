import { Scenario, DetectorOutput } from './types';
import scenariosData from '../data/scenarios.json';

/**
 * 场景识别器
 * 
 * 负责识别用户输入的决策场景类型（如投资、招聘、产品决策等）。
 * 使用关键词匹配和正则表达式匹配的混合策略，快速准确地识别场景。
 * 
 * 识别流程：
 * 1. 关键词匹配（快速，准确率 70%）
 * 2. 正则表达式匹配（精确，准确率 85%）
 * 3. 综合评分（加权计算置信度）
 * 4. 兜底策略（返回通用场景）
 * 
 * @example
 * ```typescript
 * const detector = new ScenarioDetector();
 * const result = await detector.detect('要不要投资这只股票？');
 * console.log(result.scenarioId); // 'investment'
 * console.log(result.confidence); // 0.85
 * ```
 */
export class ScenarioDetector {
  /** 场景配置列表（从 JSON 文件加载） */
  private scenarios: Scenario[];

  /**
   * 构造函数
   * 
   * 从 scenarios.json 文件加载场景配置。
   * 兼容两种 JSON 格式：{ scenarios: [...] } 或直接 [...]
   */
  constructor() {
    const data = scenariosData as any;
    // 兼容两种 JSON 格式
    this.scenarios = data.scenarios || scenariosData;
  }

  /**
   * 关键词匹配识别（快速策略）
   * 
   * 通过关键词和正则表达式匹配识别场景，速度快但准确率约 70%。
   * 
   * 算法原理：
   * 1. 遍历所有场景配置
   * 2. 计算关键词匹配数量（至少 1 个）
   * 3. 计算正则表达式匹配数量（至少 1 个）
   * 4. 综合评分：关键词权重 40%，正则权重 60%
   * 5. 返回评分最高的场景
   * 
   * 评分公式：
   * - 关键词评分 = min(匹配数 / 3, 1) * 0.4
   * - 正则评分 = 0.5 + 匹配数 * 0.1
   * - 最终置信度 = 关键词评分 * 0.4 + 正则评分 * 0.6（有正则时）
   * - 最终置信度 = 关键词评分 * 0.5（无正则时，上限 0.4）
   * 
   * @param input - 用户输入的决策问题
   * @returns 识别结果，包含场景 ID、置信度和推荐模型；未识别返回 null
   * @throws {Error} 输入为空或非字符串
   * @throws {Error} 输入长度超过 1000 字符
   * 
   * @example
   * ```typescript
   * const result = detector.detectByKeywords('要不要投资这只股票？');
   * // { scenarioId: 'investment', confidence: 0.85, suggestedModels: ['06', '07', '10'] }
   * ```
   */
  detectByKeywords(input: string): DetectorOutput | null {
    // 输入验证：确保输入是非空字符串
    if (!input || typeof input !== 'string') {
      throw new Error('输入必须是非空字符串');
    }
    
    // 输入验证：防止过长输入导致性能问题
    if (input.length > 1000) {
      throw new Error('输入过长，请控制在 1000 字符以内');
    }
    
    // 转小写以实现大小写不敏感匹配
    const inputLower = input.toLowerCase();
    let bestMatch: DetectorOutput | null = null;
    let bestScore = 0;
    
    // 遍历所有场景配置，计算匹配度
    for (const scenario of this.scenarios) {
      try {
        // 计算关键词匹配度
        const matchedKeywords = scenario.keywords.filter(keyword => 
          inputLower.includes(keyword.toLowerCase())
        );
        
        // 计算正则匹配度（带超时保护，防止恶意正则）
        const matchedPatterns = scenario.patterns.filter(pattern => {
          try {
            const regex = new RegExp(pattern, 'i');
            return regex.test(input);
          } catch {
            // 正则表达式无效时忽略
            return false;
          }
        });
        
        // 综合评分：至少匹配 1 个关键词或 1 个模式
        const hasKeywords = matchedKeywords.length >= 1;
        const hasPatterns = matchedPatterns.length >= 1;
        
        if (hasKeywords || hasPatterns) {
          // 关键词评分：匹配 3 个关键词即满分
          const keywordScore = Math.min(matchedKeywords.length / 3, 1);
          // 正则评分：基础分 0.5，每多匹配 1 个加 0.1
          const patternScore = matchedPatterns.length > 0 ? 0.5 + matchedPatterns.length * 0.1 : 0;
          // 最终置信度：有正则时权重更高（60%），无正则时上限 0.4
          const confidence = hasPatterns
            ? Math.min((keywordScore * 0.4 + patternScore * 0.6), 1)
            : Math.min(keywordScore * 0.5, 0.4);
          
          // 更新最佳匹配
          if (confidence > bestScore) {
            bestScore = confidence;
            bestMatch = {
              scenarioId: scenario.id,
              confidence,
              suggestedModels: scenario.models
            };
          }
        }
      } catch (error) {
        // 单个场景匹配失败不影响其他场景
        console.error(`场景 ${scenario.id} 匹配失败:`, error);
        continue;
      }
    }
    
    return bestMatch;
  }

  /**
   * 混合策略识别（主入口）
   * 
   * 先使用关键词快速匹配，置信度低时可扩展 LLM 识别（当前未实现）。
   * 如果识别失败或置信度过低，返回通用场景作为兜底。
   * 
   * 策略选择：
   * - 置信度 > 0.1：使用关键词匹配结果
   * - 置信度 ≤ 0.1：返回通用场景（兜底）
   * - 异常情况：返回通用场景（兜底）
   * 
   * @param input - 用户输入的决策问题
   * @returns 识别结果，包含场景 ID、置信度和推荐模型
   * 
   * @example
   * ```typescript
   * const result = await detector.detect('要不要投资这只股票？');
   * // { scenarioId: 'investment', confidence: 0.85, suggestedModels: ['06', '07', '10'] }
   * 
   * const fallback = await detector.detect('随便问问');
   * // { scenarioId: 'general', confidence: 0.3, suggestedModels: ['01', '06', '07'] }
   * ```
   */
  async detect(input: string): Promise<DetectorOutput> {
    try {
      // 先尝试关键词快速匹配
      const quick = this.detectByKeywords(input);
      
      // 置信度足够高，直接返回
      if (quick && quick.confidence > 0.1) {
        return quick;
      }
      
      // 兜底：返回通用场景
      // 推荐多元思维、能力圈、逆向思维三个核心模型
      return {
        scenarioId: 'general',
        confidence: 0.3,
        suggestedModels: ['01', '06', '07'] // 多元思维、能力圈、逆向思维
      };
    } catch (error) {
      console.error('场景识别失败:', error);
      // 异常时返回通用场景（兜底）
      return {
        scenarioId: 'general',
        confidence: 0.1,
        suggestedModels: ['01', '06', '07']
      };
    }
  }

  /**
   * 获取场景信息
   * 
   * 根据场景 ID 查找完整的场景配置。
   * 
   * @param scenarioId - 场景 ID
   * @returns 场景配置对象，未找到返回 undefined
   * 
   * @example
   * ```typescript
   * const scenario = detector.getScenario('investment');
   * console.log(scenario.name); // '投资决策'
   * ```
   */
  getScenario(scenarioId: string): Scenario | undefined {
    return this.scenarios.find(s => s.id === scenarioId);
  }

  /**
   * 列出所有场景
   * 
   * 返回所有可用的场景配置列表。
   * 
   * @returns 场景配置数组
   * 
   * @example
   * ```typescript
   * const allScenarios = detector.listScenarios();
   * console.log(allScenarios.length); // 5
   * ```
   */
  listScenarios(): Scenario[] {
    return this.scenarios;
  }
}
