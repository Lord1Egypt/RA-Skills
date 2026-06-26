/**
 * Memory-Master 技能自进化模块
 *
 * 基于 AutoSkill / SkillRL 论文
 * - 从错误中学习
 * - 技能蒸馏
 * - 经验驱动的终身学习
 */
/**
 * 技能条目
 */
export interface Skill {
    id: string;
    name: string;
    description: string;
    pattern: string;
    action: string;
    successCount: number;
    failureCount: number;
    lastUsed?: number;
    createdAt: number;
    updatedAt: number;
}
/**
 * 经验记录
 */
export interface Experience {
    id: string;
    skillId?: string;
    context: string;
    action: string;
    result: 'success' | 'failure';
    feedback?: string;
    timestamp: number;
    lessons?: string[];
}
/**
 * 技能进化配置
 */
export interface SkillEvolutionConfig {
    minSuccesses: number;
    minFailures: number;
    retentionDays: number;
}
/**
 * 技能进化器
 */
export declare class SkillEvolver {
    private config;
    private skillsFile;
    private experiencesFile;
    constructor(memoryDir?: string, config?: Partial<SkillEvolutionConfig>);
    /**
     * 初始化文件
     */
    private initFiles;
    /**
     * 记录经验
     */
    recordExperience(context: string, action: string, result: 'success' | 'failure', feedback?: string, skillId?: string): Promise<Experience>;
    /**
     * 从失败中学习
     */
    private learnFromFailure;
    /**
     * 技能蒸馏（从成功经验中提取）
     */
    distillSkills(): Promise<Skill[]>;
    /**
     * 提取触发模式
     */
    private extractPattern;
    /**
     * 查找共同词汇
     */
    private findCommonWords;
    /**
     * 更新技能统计
     */
    private updateSkillStats;
    /**
     * 获取技能建议
     */
    getSkillSuggestions(context: string): Skill[];
    /**
     * 清理旧经验
     */
    cleanupOldExperiences(): void;
    /**
     * 加载技能
     */
    private loadSkills;
    /**
     * 保存技能
     */
    private saveSkills;
    /**
     * 加载经验
     */
    private loadExperiences;
    /**
     * 保存经验
     */
    private saveExperiences;
    /**
     * 生成 ID
     */
    private generateId;
    /**
     * 获取统计信息
     */
    getStats(): {
        totalSkills: number;
        totalExperiences: number;
        successRate: number;
    };
}
export default SkillEvolver;
