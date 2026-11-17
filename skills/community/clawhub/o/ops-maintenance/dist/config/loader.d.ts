/**
 * 配置管理器 - 简化版
 */
import { Server, SSHConfig } from '../types';
export declare class ConfigManager {
    private servers;
    private configPath;
    private mtime;
    constructor(configPath?: string);
    start(): Promise<void>;
    load(): Promise<void>;
    save(servers?: Server[]): Promise<void>;
    getAll(): Server[];
    getByTags(tags: string[]): Server[];
    getById(id: string): Server | null;
    getByHost(host: string): Server | null;
    add(config: SSHConfig): Promise<Server>;
    update(server: Server): Promise<void>;
    remove(host: string): Promise<boolean>;
    hotReload(): Promise<void>;
    stop(): void;
    getConfigPath(): string;
    get count(): number;
}
//# sourceMappingURL=loader.d.ts.map