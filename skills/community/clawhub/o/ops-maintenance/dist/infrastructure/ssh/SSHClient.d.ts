/**
 * SSH 客户端 - 简化可运行版本
 */
import type { Server, ISSHClient, ICredentialsProvider } from '../config/schemas';
export declare class SSHClient implements ISSHClient {
    private connections;
    private credentialsProvider?;
    setCredentialsProvider(provider: ICredentialsProvider): void;
    execute(server: Server, command: string, timeout?: number): Promise<string>;
    testConnection(server: Server): Promise<boolean>;
    private getConnection;
    private connect;
    private isAlive;
    disconnect(server: Server): Promise<void>;
    disconnectAll(): Promise<void>;
    getActiveConnectionsCount(): number;
}
//# sourceMappingURL=SSHClient.d.ts.map