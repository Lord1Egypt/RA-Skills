/**
 * 服务器仓库接口（领域层）
 * 定义服务器数据访问的抽象接口
 */
import type { Server, IServerRepository } from '../../config/schemas';
/**
 * 服务器仓库接口
 * 继承基础接口并添加领域特定方法
 */
export interface IServerRepositoryDomain extends IServerRepository {
    /**
     * 通过标签查找服务器（优化版）
     */
    findByTags(tags: string[]): Promise<Server[]>;
    /**
     * 查找所有在线服务器
     */
    findOnline(): Promise<Server[]>;
    /**
     * 批量检查服务器连接状态
     */
    checkConnectivity(servers?: Server[]): Promise<Map<string, boolean>>;
}
//# sourceMappingURL=ServerRepository.d.ts.map