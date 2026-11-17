export declare class GuardDaemon {
    private mode;
    socketPath: string;
    private server?;
    private core;
    private registry;
    private audit;
    private gate;
    private grants;
    private connections;
    private listening;
    constructor(mode: string);
    start(): Promise<void>;
    stop(): void;
    private handleRequest;
}
