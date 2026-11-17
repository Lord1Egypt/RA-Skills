/**
 * 类型定义统一导出
 */
export interface SSHConfig {
    host: string;
    port?: number;
    user?: string;
    password?: string;
    keyFile?: string;
    name?: string;
    tags?: string[];
}
export type ServerStatus = 'healthy' | 'warning' | 'offline' | 'unknown';
export declare class Server {
    readonly id: string;
    readonly host: string;
    readonly port: number;
    readonly user: string;
    readonly name?: string | undefined;
    readonly tags: string[];
    constructor(id: string, host: string, port: number, user: string, name?: string | undefined, tags?: string[]);
    static fromSSHConfig(config: SSHConfig, idx?: number): Server;
    getKey(): string;
    hasTag(tag: string): boolean;
    getDisplayName(): string;
}
export interface HealthMetrics {
    uptime: string;
    loadAverage: [number, number, number];
    memory: {
        total: number;
        used: number;
        free: number;
        available: number;
        swapTotal: number;
        swapUsed: number;
    };
    disk: {
        mountPoint: string;
        total: number;
        used: number;
        available: number;
        usagePercent: number;
    };
}
export interface ServiceStatus {
    name: string;
    running: boolean;
}
export declare class ServerHealth {
    readonly server: Server;
    readonly status: ServerStatus;
    readonly metrics?: HealthMetrics | undefined;
    readonly services?: ServiceStatus[] | undefined;
    readonly checkedAt: Date;
    readonly error?: string | undefined;
    constructor(server: Server, status: ServerStatus, metrics?: HealthMetrics | undefined, services?: ServiceStatus[] | undefined, checkedAt?: Date, error?: string | undefined);
    static healthy(server: Server, metrics: HealthMetrics, services: ServiceStatus[]): ServerHealth;
    static warning(server: Server, metrics: HealthMetrics, services: ServiceStatus[], reason?: string): ServerHealth;
    static offline(server: Server, error: string): ServerHealth;
    getDiskUsagePercent(): number;
    getMemoryUsagePercent(): number;
    getSwapUsagePercent(): number;
}
export interface ClusterHealthReport {
    totalServers: number;
    healthy: number;
    warning: number;
    offline: number;
    serverHealth: ServerHealth[];
    generatedAt: Date;
}
export declare class ConfigValidationError extends Error {
    readonly field?: string | undefined;
    readonly value?: any | undefined;
    constructor(message: string, field?: string | undefined, value?: any | undefined);
}
export interface ConfigManagerOptions {
    configPath?: string;
    watch?: boolean;
    pollInterval?: number;
}
export interface IServerRepository {
    findAll(): Promise<Server[]>;
    findByTags(tags: string[]): Promise<Server[]>;
    findById(id: string): Promise<Server | null>;
    add(server: Server): Promise<void>;
    update(server: Server): Promise<void>;
    remove(host: string): Promise<void>;
    onChange?(callback: () => void): void;
}
export interface ICacheRepository {
    get<T>(key: string): Promise<T | null>;
    set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>;
    delete(key: string): Promise<void>;
    clear(): Promise<void>;
}
export interface ISSHClient {
    execute(server: Server, command: string, timeout?: number): Promise<string>;
    testConnection(server: Server): Promise<boolean>;
    disconnect(server: Server): Promise<void>;
    setCredentialsProvider(provider: ICredentialsProvider): void;
}
export interface IHealthCheckStrategy {
    name: string;
    priority: number;
    check(server: Server, ssh: ISSHClient): Promise<any>;
    isCritical(): boolean;
}
export interface IReportFormatter {
    formatClusterReport(report: ClusterHealthReport): string;
    formatServerHealth(health: ServerHealth): string;
    formatPasswordReport(data: any): string;
}
export interface INotifier {
    notify(title: string, message: string, level: 'info' | 'warning' | 'critical'): Promise<void>;
}
export interface ICredentialsProvider {
    getCredentials(server: Server): Promise<{
        password?: string;
        keyFile?: string;
        keyContent?: string;
    } | null>;
    setCredentials(server: Server, credentials: any): Promise<void>;
}
export type OpsAction = 'health' | 'logs' | 'perf' | 'ports' | 'process' | 'disk' | 'password' | 'passwd' | 'expire';
export interface PasswordUserInfo {
    user: string;
    lastChanged: string;
    expires: string;
    maxDays: string;
    status: string;
    daysLeft?: number;
}
export interface ThresholdConfig {
    diskWarning: number;
    diskCritical: number;
    memoryWarning: number;
    memoryCritical: number;
    swapWarning: number;
    swapCritical: number;
    loadWarningMultiplier: number;
    loadCriticalMultiplier: number;
}
export interface ContainerOptions {
    configPath?: string;
    useConnectionPool?: boolean;
    cacheTTL?: number;
    logLevel?: string;
    environment?: string;
}
export interface AppConfig {
    configPath?: string;
    useConnectionPool?: boolean;
    cacheTTL?: number;
    logLevel?: string;
    environment?: string;
}
export interface LegacyAdapterConfig {
    configPath?: string;
    useConnectionPool?: boolean;
    cacheTTL?: number;
    environment?: string;
}
//# sourceMappingURL=types.d.ts.map