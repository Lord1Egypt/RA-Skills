"use strict";
/**
 * SSH 连接池
 * 管理连接生命周期，支持并发控制和连接复用
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConnectionPool = void 0;
const events_1 = require("events");
class ConnectionPool extends events_1.EventEmitter {
    constructor(client, options = {}) {
        super();
        this.activeConnections = new Map();
        this.waitingQueue = [];
        this.cleaningInterval = null;
        this.client = client;
        this.options = {
            maxConnections: 10,
            idleTimeout: 5 * 60 * 1000, // 5分钟
            maxLifetime: 30 * 60 * 1000, // 30分钟
            validateConnection: async (conn) => {
                try {
                    await new Promise((resolve, reject) => {
                        conn.exec('echo 1', (err) => {
                            if (err)
                                reject(err);
                            else
                                resolve(undefined);
                        });
                    });
                    return true;
                }
                catch {
                    return false;
                }
            }
        };
    }
    /**
     * 启动连接池
     */
    start() {
        this.cleaningInterval = setInterval(() => {
            this.cleanIdleConnections();
        }, 60 * 1000); // 每分钟清理一次
    }
    /**
     * 停止连接池
     */
    stop() {
        if (this.cleaningInterval) {
            clearInterval(this.cleaningInterval);
            this.cleaningInterval = null;
        }
        // 关闭所有连接
        for (const [key, { conn }] of this.activeConnections) {
            try {
                conn.end();
            }
            catch {
                // 忽略关闭错误
            }
        }
        this.activeConnections.clear();
        this.waitingQueue = [];
    }
    /**
     * 获取连接（支持等待）
     */
    async acquire(server, timeout = 30000) {
        const key = server.getKey();
        // 1. 检查是否有可用连接
        const existing = this.activeConnections.get(key);
        if (existing && await this.options.validateConnection(existing.conn)) {
            existing.lastUsed = Date.now();
            return existing.conn;
        }
        // 2. 检查是否已达到最大连接数
        if (this.activeConnections.size >= this.options.maxConnections) {
            // 进入等待队列
            return new Promise((resolve, reject) => {
                const timeoutId = setTimeout(() => {
                    const idx = this.waitingQueue.findIndex(item => item.server.getKey() === key);
                    if (idx >= 0) {
                        this.waitingQueue.splice(idx, 1);
                    }
                    reject(new Error('获取连接超时：连接池已满'));
                }, timeout);
                this.waitingQueue.push({
                    server,
                    resolve: (conn) => {
                        clearTimeout(timeoutId);
                        resolve(conn);
                    },
                    reject: (err) => {
                        clearTimeout(timeoutId);
                        reject(err);
                    }
                });
                // 尝试处理等待队列
                setTimeout(() => this.processWaitingQueue(), 0);
            });
        }
        // 3. 创建新连接
        try {
            const conn = await this.client.connect(server);
            this.activeConnections.set(key, {
                conn,
                createdAt: Date.now(),
                lastUsed: Date.now()
            });
            return conn;
        }
        catch (error) {
            throw new Error(`连接池创建连接失败: ${error.message}`);
        }
    }
    /**
     * 释放连接（归还到池中）
     */
    release(server, conn) {
        const key = server.getKey();
        const entry = this.activeConnections.get(key);
        if (entry) {
            entry.lastUsed = Date.now();
        }
    }
    /**
     * 执行命令（使用连接池）
     */
    async execute(server, command, timeout = 30000) {
        const conn = await this.acquire(server, timeout);
        try {
            const result = await this.client.execute(server, command, timeout);
            this.release(server, conn);
            return result;
        }
        catch (error) {
            // 命令执行失败，关闭连接
            this.closeConnection(server);
            throw error;
        }
    }
    /**
     * 清理空闲连接
     */
    cleanIdleConnections() {
        const now = Date.now();
        const toRemove = [];
        for (const [key, { conn, createdAt, lastUsed }] of this.activeConnections) {
            // 检查是否超过最大存活时间
            if (now - createdAt > this.options.maxLifetime) {
                toRemove.push(key);
                try {
                    conn.end();
                }
                catch { }
                continue;
            }
            // 检查是否空闲超时
            if (now - lastUsed > this.options.idleTimeout) {
                toRemove.push(key);
                try {
                    conn.end();
                }
                catch { }
            }
        }
        for (const key of toRemove) {
            this.activeConnections.delete(key);
        }
    }
    /**
     * 处理等待队列
     */
    async processWaitingQueue() {
        if (this.waitingQueue.length === 0)
            return;
        // 按优先级排序（这里简单按入队顺序）
        const next = this.waitingQueue.shift();
        if (!next)
            return;
        try {
            const conn = await this.acquire(next.server, 5000);
            next.resolve(conn);
        }
        catch (error) {
            next.reject(error);
        }
    }
    /**
     * 关闭指定连接
     */
    async closeConnection(server) {
        const key = server.getKey();
        const entry = this.activeConnections.get(key);
        if (entry) {
            try {
                await new Promise((resolve, reject) => {
                    entry.conn.end((err) => {
                        if (err)
                            reject(err);
                        else
                            resolve();
                    });
                });
            }
            catch {
                // 忽略关闭错误
            }
            this.activeConnections.delete(key);
        }
    }
    /**
     * 获取统计信息
     */
    getStats() {
        return {
            active: this.activeConnections.size,
            queued: this.waitingQueue.length
        };
    }
    /**
     * 是否正在运行
     */
    isRunning() {
        return this.cleaningInterval !== null;
    }
}
exports.ConnectionPool = ConnectionPool;
//# sourceMappingURL=ConnectionPool.js.map