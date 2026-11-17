"use strict";
/**
 * SSH 客户端 - 简化可运行版本
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.SSHClient = void 0;
const ssh2_1 = require("ssh2");
const fs_1 = require("fs");
class SSHClient {
    constructor() {
        this.connections = new Map();
    }
    setCredentialsProvider(provider) {
        this.credentialsProvider = provider;
    }
    async execute(server, command, timeout = 30000) {
        const conn = await this.getConnection(server);
        return new Promise((resolve, reject) => {
            conn.exec(command, (err, stream) => {
                if (err) {
                    this.closeConnection(server);
                    return reject(new Error(`SSH 执行失败: ${err.message}`));
                }
                let output = '';
                stream.on('data', (data) => output += data.toString());
                stream.on('close', (code) => {
                    if (code !== 0) {
                        reject(new Error(`退出码 ${code}: ${output.substring(0, 200)}`));
                    }
                    else {
                        resolve(output.trim());
                    }
                });
            });
            setTimeout(() => {
                if (conn.isAuthenticated && conn.isAuthenticated()) {
                    conn.requestForcePseudoTerminal((err) => { if (!err)
                        conn.end(); });
                }
                reject(new Error(`超时: ${command}`));
            }, timeout);
        });
    }
    async testConnection(server) {
        try {
            const conn = await this.connect(server);
            this.connections.set(server.getKey(), conn);
            return true;
        }
        catch {
            return false;
        }
    }
    async getConnection(server) {
        const key = server.getKey();
        let conn = this.connections.get(key);
        if (conn && this.isAlive(conn))
            return conn;
        conn = await this.connect(server);
        this.connections.set(key, conn);
        return conn;
    }
    async connect(server) {
        return new Promise((resolve, reject) => {
            const conn = new ssh2_1.Client();
            const connectOptions = {
                host: server.host,
                port: server.port,
                username: server.user,
                readyTimeout: 30000,
                keepaliveInterval: 10000
            };
            (async () => {
                try {
                    if (this.credentialsProvider) {
                        const credentials = await this.credentialsProvider.getCredentials(server);
                        if (credentials) {
                            if (credentials.keyContent) {
                                connectOptions.privateKey = Buffer.from(credentials.keyContent);
                            }
                            else if (credentials.keyFile) {
                                connectOptions.privateKey = (0, fs_1.readFileSync)(credentials.keyFile);
                            }
                            else if (credentials.password) {
                                connectOptions.password = credentials.password;
                            }
                        }
                    }
                    conn.connect(connectOptions);
                }
                catch (err) {
                    reject(new Error(`连接失败: ${err.message}`));
                }
            })();
            conn.on('ready', () => resolve(conn));
            conn.on('error', (err) => reject(new Error(`SSH错误: ${err.message}`)));
            conn.on('close', () => this.connections.delete(server.getKey()));
        });
    }
    isAlive(conn) {
        return conn.isAuthenticated && conn.isAuthenticated() && !conn.isDestroyed;
    }
    async disconnect(server) {
        const key = server.getKey();
        const conn = this.connections.get(key);
        if (conn) {
            conn.end();
            this.connections.delete(key);
        }
    }
    async disconnectAll() {
        for (const [_, conn] of this.connections)
            conn.end();
        this.connections.clear();
    }
    getActiveConnectionsCount() {
        return this.connections.size;
    }
}
exports.SSHClient = SSHClient;
//# sourceMappingURL=SSHClient.js.map