/**
 * Knowledge Graph Engine - 知识图谱引擎
 * 
 * 基于 HippoRAG + ZEP + Ontology 最佳实践
 * 支持实体管理、关系管理、图遍历、自动构建
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.2.0
 */

import * as fs from 'fs';
import * as path from 'path';

// ============ 实体类型定义 ============

export type EntityType = 
  | 'Person'      // 人物
  | 'Project'     // 项目
  | 'Task'        // 任务
  | 'Skill'       // 技能
  | 'Memory'      // 记忆
  | 'Event'       // 事件
  | 'Concept';    // 概念

export interface GraphEntity {
  id: string;
  type: EntityType;
  name: string;
  attributes: Record<string, any>;
  createdAt: number;
  updatedAt: number;
}

// ============ 关系类型定义 ============

export type RelationType =
  | 'works_on'        // 工作于
  | 'knows'           // 知道
  | 'created'         // 创建
  | 'has_task'        // 有任务
  | 'uses_skill'      // 使用技能
  | 'owned_by'        // 属于
  | 'assigned_to'     // 分配给
  | 'part_of'         // 属于（部分）
  | 'depends_on'      // 依赖于
  | 'related_to'      // 相关
  | 'attended_by'     // 参与者
  | 'about'           // 关于
  | 'references';     // 引用

export interface GraphRelation {
  id: string;
  from: string;       // 源实体 ID
  to: string;         // 目标实体 ID
  type: RelationType;
  description: string;
  weight: number;     // 权重 0-1
  createdAt: number;
}

// ============ 图遍历 ============

export interface GraphPath {
  start: string;
  end: string;
  nodes: string[];    // 路径上的实体 ID
  relations: string[]; // 路径上的关系 ID
  length: number;
}

export interface TraverseOptions {
  maxDepth?: number;
  relationTypes?: RelationType[];
  direction?: 'forward' | 'backward' | 'both';
}

export interface NeighborQuery {
  entityId: string;
  relationType?: RelationType;
  direction?: 'in' | 'out' | 'both';
  limit?: number;
}

export interface NeighborResult {
  entityId: string;
  neighbors: Array<{
    entityId: string;
    relationType: RelationType;
    direction: 'in' | 'out';
    relationId: string;
  }>;
}

// ============ 配置 ============

export interface GraphConfig {
  basePath?: string;
  autoSave?: boolean;
  autoSaveInterval?: number; // 毫秒
}

// ============ 知识图谱引擎 ============

export class KnowledgeGraph {
  private config: Required<GraphConfig>;
  private entities: Map<string, GraphEntity>;
  private relations: Map<string, GraphRelation>;
  private adjacencyList: Map<string, Set<string>>; // 邻接表
  private reverseIndex: Map<string, Set<string>>;  // 反向索引
  private saveTimer?: NodeJS.Timeout;

  constructor(config: GraphConfig = {}) {
    this.config = {
      basePath: config.basePath ?? 'memory/knowledge-graph',
      autoSave: config.autoSave ?? true,
      autoSaveInterval: config.autoSaveInterval ?? 5 * 60 * 1000, // 5 分钟
    };

    this.entities = new Map();
    this.relations = new Map();
    this.adjacencyList = new Map();
    this.reverseIndex = new Map();

    // 初始化
    this.init();
  }

  /**
   * 初始化图谱
   */
  private async init(): Promise<void> {
    try {
      // 确保目录存在
      if (!fs.existsSync(this.config.basePath)) {
        fs.mkdirSync(this.config.basePath, { recursive: true });
      }

      // 加载数据
      await this.load();

      // 启动自动保存
      if (this.config.autoSave) {
        this.startAutoSave();
      }

      console.log(`[KnowledgeGraph] 初始化完成，加载了 ${this.entities.size} 个实体，${this.relations.size} 个关系`);
    } catch (error) {
      console.warn('[KnowledgeGraph] 初始化失败:', error);
    }
  }

  /**
   * 加载数据
   */
  private async load(): Promise<void> {
    const entitiesPath = path.join(this.config.basePath, 'entities.json');
    const relationsPath = path.join(this.config.basePath, 'relations.json');

    if (fs.existsSync(entitiesPath)) {
      const data = fs.readFileSync(entitiesPath, 'utf-8');
      const entities = JSON.parse(data);
      this.entities = new Map(Object.entries(entities));
    }

    if (fs.existsSync(relationsPath)) {
      const data = fs.readFileSync(relationsPath, 'utf-8');
      const relations = JSON.parse(data);
      this.relations = new Map(Object.entries(relations));
    }

    // 重建索引
    this.rebuildIndex();
  }

  /**
   * 保存数据
   */
  private async save(): Promise<void> {
    try {
      // 确保目录存在
      if (!fs.existsSync(this.config.basePath)) {
        fs.mkdirSync(this.config.basePath, { recursive: true });
      }

      // 保存实体
      const entitiesPath = path.join(this.config.basePath, 'entities.json');
      fs.writeFileSync(
        entitiesPath,
        JSON.stringify(Object.fromEntries(this.entities), null, 2),
        'utf-8'
      );

      // 保存关系
      const relationsPath = path.join(this.config.basePath, 'relations.json');
      fs.writeFileSync(
        relationsPath,
        JSON.stringify(Object.fromEntries(this.relations), null, 2),
        'utf-8'
      );

      console.log(`[KnowledgeGraph] 保存完成：${this.entities.size} 实体，${this.relations.size} 关系`);
    } catch (error) {
      console.error('[KnowledgeGraph] 保存失败:', error);
    }
  }

  /**
   * 启动自动保存
   */
  private startAutoSave(): void {
    this.saveTimer = setInterval(() => {
      this.save();
    }, this.config.autoSaveInterval);
  }

  /**
   * 重建索引
   */
  private rebuildIndex(): void {
    this.adjacencyList.clear();
    this.reverseIndex.clear();

    for (const relation of this.relations.values()) {
      // 正向索引
      if (!this.adjacencyList.has(relation.from)) {
        this.adjacencyList.set(relation.from, new Set());
      }
      this.adjacencyList.get(relation.from)!.add(relation.to);

      // 反向索引
      if (!this.reverseIndex.has(relation.to)) {
        this.reverseIndex.set(relation.to, new Set());
      }
      this.reverseIndex.get(relation.to)!.add(relation.from);
    }
  }

  // ============ 实体操作 ============

  /**
   * 添加实体
   */
  async addEntity(entity: Omit<GraphEntity, 'createdAt' | 'updatedAt'>): Promise<string> {
    const id = entity.id || `entity_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const now = Date.now();

    const fullEntity: GraphEntity = {
      ...entity,
      id,
      createdAt: now,
      updatedAt: now,
    };

    this.entities.set(id, fullEntity);

    // 初始化邻接表
    if (!this.adjacencyList.has(id)) {
      this.adjacencyList.set(id, new Set());
    }
    if (!this.reverseIndex.has(id)) {
      this.reverseIndex.set(id, new Set());
    }

    if (this.config.autoSave) {
      await this.save();
    }

    console.log(`[KnowledgeGraph] 添加实体：${id} (${entity.type}:${entity.name})`);
    return id;
  }

  /**
   * 获取实体
   */
  async getEntity(id: string): Promise<GraphEntity | null> {
    return this.entities.get(id) || null;
  }

  /**
   * 更新实体
   */
  async updateEntity(id: string, updates: Partial<GraphEntity>): Promise<void> {
    const entity = this.entities.get(id);
    if (!entity) {
      throw new Error(`Entity ${id} not found`);
    }

    const updated = {
      ...entity,
      ...updates,
      updatedAt: Date.now(),
    };

    this.entities.set(id, updated);

    if (this.config.autoSave) {
      await this.save();
    }
  }

  /**
   * 删除实体
   */
  async deleteEntity(id: string): Promise<void> {
    // 删除相关关系
    const relationsToDelete = Array.from(this.relations.values())
      .filter(r => r.from === id || r.to === id);

    for (const relation of relationsToDelete) {
      await this.deleteRelation(relation.id);
    }

    // 删除实体
    this.entities.delete(id);
    this.adjacencyList.delete(id);
    this.reverseIndex.delete(id);

    if (this.config.autoSave) {
      await this.save();
    }
  }

  /**
   * 查询实体（按类型）
   */
  async queryEntitiesByType(type: EntityType): Promise<GraphEntity[]> {
    return Array.from(this.entities.values()).filter(e => e.type === type);
  }

  /**
   * 搜索实体（按名称）
   */
  async searchEntities(query: string, limit: number = 20): Promise<GraphEntity[]> {
    const queryLower = query.toLowerCase();
    const results: Array<{ entity: GraphEntity; score: number }> = [];

    for (const entity of this.entities.values()) {
      let score = 0;

      // 名称匹配
      if (entity.name.toLowerCase().includes(queryLower)) {
        score += 10;
      }

      // 属性匹配
      for (const value of Object.values(entity.attributes)) {
        if (String(value).toLowerCase().includes(queryLower)) {
          score += 5;
          break;
        }
      }

      if (score > 0) {
        results.push({ entity, score });
      }
    }

    // 按评分排序
    results.sort((a, b) => b.score - a.score);

    return results.slice(0, limit).map(r => r.entity);
  }

  // ============ 关系操作 ============

  /**
   * 添加关系
   */
  async addRelation(relation: Omit<GraphRelation, 'id' | 'createdAt'>): Promise<string> {
    const id = `rel_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const now = Date.now();

    const fullRelation: GraphRelation = {
      ...relation,
      id,
      createdAt: now,
    };

    this.relations.set(id, fullRelation);

    // 更新索引
    if (!this.adjacencyList.has(relation.from)) {
      this.adjacencyList.set(relation.from, new Set());
    }
    this.adjacencyList.get(relation.from)!.add(relation.to);

    if (!this.reverseIndex.has(relation.to)) {
      this.reverseIndex.set(relation.to, new Set());
    }
    this.reverseIndex.get(relation.to)!.add(relation.from);

    if (this.config.autoSave) {
      await this.save();
    }

    console.log(`[KnowledgeGraph] 添加关系：${relation.from} -[${relation.type}]-> ${relation.to}`);
    return id;
  }

  /**
   * 获取关系
   */
  async getRelation(id: string): Promise<GraphRelation | null> {
    return this.relations.get(id) || null;
  }

  /**
   * 删除关系
   */
  async deleteRelation(id: string): Promise<void> {
    const relation = this.relations.get(id);
    if (!relation) {
      return;
    }

    this.relations.delete(id);

    // 更新索引
    const targets = this.adjacencyList.get(relation.from);
    if (targets) {
      targets.delete(relation.to);
    }

    const sources = this.reverseIndex.get(relation.to);
    if (sources) {
      sources.delete(relation.from);
    }

    if (this.config.autoSave) {
      await this.save();
    }
  }

  /**
   * 获取实体的关系
   */
  async getEntityRelations(entityId: string, type?: RelationType): Promise<GraphRelation[]> {
    return Array.from(this.relations.values()).filter(r => {
      const matchesEntity = r.from === entityId || r.to === entityId;
      const matchesType = !type || r.type === type;
      return matchesEntity && matchesType;
    });
  }

  // ============ 图遍历 ============

  /**
   * 获取邻居
   */
  async getNeighbors(options: NeighborQuery): Promise<NeighborResult> {
    const { entityId, relationType, direction = 'both', limit = 50 } = options;

    const neighbors: NeighborResult['neighbors'] = [];

    // 出边
    if (direction === 'out' || direction === 'both') {
      const targets = this.adjacencyList.get(entityId);
      if (targets) {
        for (const relation of this.relations.values()) {
          if (relation.from === entityId) {
            if (!relationType || relation.type === relationType) {
              neighbors.push({
                entityId: relation.to,
                relationType: relation.type,
                direction: 'out',
                relationId: relation.id,
              });
            }
          }
        }
      }
    }

    // 入边
    if (direction === 'in' || direction === 'both') {
      const sources = this.reverseIndex.get(entityId);
      if (sources) {
        for (const relation of this.relations.values()) {
          if (relation.to === entityId) {
            if (!relationType || relation.type === relationType) {
              neighbors.push({
                entityId: relation.from,
                relationType: relation.type,
                direction: 'in',
                relationId: relation.id,
              });
            }
          }
        }
      }
    }

    return {
      entityId,
      neighbors: neighbors.slice(0, limit),
    };
  }

  /**
   * 图遍历（BFS）
   */
  async traverse(startId: string, options: TraverseOptions = {}): Promise<GraphPath[]> {
    const { maxDepth = 5, relationTypes, direction = 'forward' } = options;

    const paths: GraphPath[] = [];
    const visited = new Set<string>();
    const queue: Array<{ nodeId: string; path: string[]; relations: string[]; depth: number }> = [
      { nodeId: startId, path: [startId], relations: [], depth: 0 },
    ];

    while (queue.length > 0) {
      const { nodeId, path, relations, depth } = queue.shift()!;

      if (depth >= maxDepth) {
        continue;
      }

      // 获取邻居
      const neighborResult = await this.getNeighbors({
        entityId: nodeId,
        relationType: relationTypes?.[0],
        direction: direction === 'forward' ? 'out' : direction === 'backward' ? 'in' : 'both',
      });

      for (const neighbor of neighborResult.neighbors) {
        if (visited.has(neighbor.entityId)) {
          continue;
        }

        const newPath = [...path, neighbor.entityId];
        const newRelations = [...relations, neighbor.relationId];

        // 记录路径
        paths.push({
          start: startId,
          end: neighbor.entityId,
          nodes: newPath,
          relations: newRelations,
          length: newPath.length,
        });

        visited.add(neighbor.entityId);

        // 继续遍历
        queue.push({
          nodeId: neighbor.entityId,
          path: newPath,
          relations: newRelations,
          depth: depth + 1,
        });
      }
    }

    return paths;
  }

  /**
   * 查找最短路径（BFS）
   */
  async findShortestPath(fromId: string, toId: string): Promise<GraphPath | null> {
    if (fromId === toId) {
      return { start: fromId, end: toId, nodes: [fromId], relations: [], length: 0 };
    }

    const visited = new Set<string>();
    const queue: Array<{ nodeId: string; path: string[]; relations: string[] }> = [
      { nodeId: fromId, path: [fromId], relations: [] },
    ];

    while (queue.length > 0) {
      const { nodeId, path, relations } = queue.shift()!;

      const neighborResult = await this.getNeighbors({
        entityId: nodeId,
        direction: 'out',
      });

      for (const neighbor of neighborResult.neighbors) {
        if (neighbor.entityId === toId) {
          return {
            start: fromId,
            end: toId,
            nodes: [...path, toId],
            relations: [...relations, neighbor.relationId],
            length: path.length + 1,
          };
        }

        if (!visited.has(neighbor.entityId)) {
          visited.add(neighbor.entityId);
          queue.push({
            nodeId: neighbor.entityId,
            path: [...path, neighbor.entityId],
            relations: [...relations, neighbor.relationId],
          });
        }
      }
    }

    return null; // 无路径
  }

  // ============ 统计信息 ============

  /**
   * 获取统计信息
   */
  getStats(): {
    totalEntities: number;
    totalRelations: number;
    entitiesByType: Record<EntityType, number>;
    relationsByType: Record<RelationType, number>;
    avgRelationsPerEntity: number;
  } {
    const entitiesByType: Record<string, number> = {};
    const relationsByType: Record<string, number> = {};

    for (const entity of this.entities.values()) {
      entitiesByType[entity.type] = (entitiesByType[entity.type] || 0) + 1;
    }

    for (const relation of this.relations.values()) {
      relationsByType[relation.type] = (relationsByType[relation.type] || 0) + 1;
    }

    return {
      totalEntities: this.entities.size,
      totalRelations: this.relations.size,
      entitiesByType: entitiesByType as Record<EntityType, number>,
      relationsByType: relationsByType as Record<RelationType, number>,
      avgRelationsPerEntity: this.relations.size / Math.max(1, this.entities.size),
    };
  }

  /**
   * 清空图谱
   */
  async clear(): Promise<void> {
    this.entities.clear();
    this.relations.clear();
    this.adjacencyList.clear();
    this.reverseIndex.clear();

    if (this.config.autoSave) {
      await this.save();
    }
  }

  /**
   * 销毁（停止自动保存）
   */
  destroy(): void {
    if (this.saveTimer) {
      clearInterval(this.saveTimer);
    }
    // 最后保存一次
    this.save();
  }
}
