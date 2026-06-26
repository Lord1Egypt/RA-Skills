import { Model } from './types';
import modelsData from '../data/models.json';

/**
 * 模型推荐引擎
 * 
 * 负责根据场景推荐相关的芒格思维模型。
 * 提供模型查询、过滤和分类功能。
 * 
 * 数据来源：从 models.json 文件加载模型配置。
 * 
 * @example
 * ```typescript
 * const recommender = new ModelRecommender();
 * const models = recommender.recommend(['06', '07', '10']);
 * console.log(models.map(m => m.name)); // ['能力圈', '逆向思维', '安全边际']
 * ```
 */
export class ModelRecommender {
  /** 思维模型配置列表（从 JSON 文件加载） */
  private models: Model[];

  /**
   * 构造函数
   * 
   * 从 models.json 文件加载思维模型配置。
   * 兼容两种 JSON 格式：{ models: [...] } 或直接 [...]
   */
  constructor() {
    this.models = (modelsData as any).models || modelsData;
  }

  /**
   * 根据模型 ID 列表推荐模型
   * 
   * 根据提供的模型 ID 列表，查找并返回对应的模型配置。
   * 自动过滤不存在的模型 ID。
   * 
   * @param modelIds - 模型 ID 列表
   * @returns 模型配置数组（保持输入顺序）
   * 
   * @example
   * ```typescript
   * const models = recommender.recommend(['06', '07', '99']);
   * // 返回 2 个模型（'99' 不存在被过滤）
   * console.log(models.length); // 2
   * ```
   */
  recommend(modelIds: string[]): Model[] {
    return modelIds
      .map(id => this.models.find(m => m.id === id))
      .filter((m): m is Model => m !== undefined); // 类型守卫，过滤 undefined
  }

  /**
   * 获取单个模型
   * 
   * 根据模型 ID 查找单个模型配置。
   * 
   * @param modelId - 模型 ID
   * @returns 模型配置对象，未找到返回 undefined
   * 
   * @example
   * ```typescript
   * const model = recommender.getModel('06');
   * console.log(model?.name); // '能力圈'
   * ```
   */
  getModel(modelId: string): Model | undefined {
    return this.models.find(m => m.id === modelId);
  }

  /**
   * 列出所有模型
   * 
   * 返回所有可用的思维模型配置列表。
   * 
   * @returns 模型配置数组
   * 
   * @example
   * ```typescript
   * const allModels = recommender.listModels();
   * console.log(allModels.length); // 30+
   * ```
   */
  listModels(): Model[] {
    return this.models;
  }

  /**
   * 按分类列出模型
   * 
   * 根据分类（如认知心理学、商业模型等）过滤模型。
   * 
   * @param category - 模型分类
   * @returns 该分类下的模型配置数组
   * 
   * @example
   * ```typescript
   * const psychologyModels = recommender.listByCategory('认知心理学');
   * console.log(psychologyModels.map(m => m.name)); // ['能力圈', '逆向思维', ...]
   * ```
   */
  listByCategory(category: string): Model[] {
    return this.models.filter(m => m.category === category);
  }
}
