export interface DaemonConfig {
    binaryPath?: string;
    port?: number;
    dataDir?: string;
}
export declare class DaemonManager {
    private config;
    private process;
    private port;
    private url;
    private pid;
    private pidFile;
    private dataDir;
    private startPromise;
    constructor(config?: DaemonConfig);
    ensureRunning(): Promise<string>;
    private doStart;
    isHealthy(): Promise<boolean>;
    private findAvailablePort;
    private isPortAvailable;
    private startDaemon;
    private findBinary;
    private waitForHealthy;
    private safeUnlinkPidFile;
    private isMemoryGardenProcess;
    private cleanupOrphan;
    shutdown(): Promise<void>;
    getUrl(): string;
    getPort(): number;
}
//# sourceMappingURL=daemon-manager.d.ts.map