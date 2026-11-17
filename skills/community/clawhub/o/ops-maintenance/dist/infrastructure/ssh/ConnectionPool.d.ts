/**
 * SSH 连接池
 * 管理连接生命周期，支持并发控制和连接复用
 */
import { EventEmitter } from 'events';
import type { Server } from '../../config/schemas';
import { SSHClient } from './SSHClient';
export interface PoolOptions {
    /** 最大连接数 */
    maxConnections?: number;
    /** 连接空闲超时（ms） */
    idleTimeout?: number;
    /** 连接最大存活时间（ms） */
    maxLifetime?: number;
    /** 验证连接是否可用 */
    validateConnection?: (conn: any) => Promise<boolean>;
}
export declare class ConnectionPool extends EventEmitter {
    private client;
    private options;
    private activeConnections;
    private waitingQueue;
    private cleaningInterval;
    constructor(client: SSHClient, options?: PoolOptions);
    /**
     * 启动连接池
     */
    start(): void;
    /**
     * 停止连接池
     */
    stop(): void;
    /**
     * 获取连接（支持等待）
     */
    acquire(server: Server, timeout?: number): Promise<any>;
    /**
     * 释放连接（归还到池中）
     */
    release(server: Server, conn: any): void;
    /**
     * 执行命令（使用连接池）
     */
    execute(server: Server, command: string, timeout?: number): Promise<string>;
    /**
     * 清理空闲连接
     */
    private cleanIdleConnections;
    /**
     * 处理等待队列
     */
    private processWaitingQueue;
    /**
     * 关闭指定连接
     */
    closeConnection(server: Server): Promise<void>;
    /**
     * 获取统计信息
     */
    getStats(): {
        active: number;
        queued: number;
    };
    /**
     * 是否正在运行
     */
    isRunning(): boolean;
}
//# sourceMappingURL=ConnectionPool.d.ts.map