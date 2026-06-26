import { EventEmitter } from 'events';
export declare const serverEvents: EventEmitter<any>;
/**
 * Generates a dynamic control ID that is authorized to be bound.
 */
export declare function generateControlId(): string;
export declare function startDGLabServer(port: number): void;
export declare function stopDGLabServer(): Promise<void>;
/**
 * Send a command to all bound Apps.
 * Automatically checks message length limit (1950 chars).
 */
export declare function sendCommandToApps(commandStr: string): void;
/**
 * 获取当前连接状态
 */
export declare function getConnectionStatus(): {
    clients: number;
    bindings: number;
    controlIds: number;
};
//# sourceMappingURL=server.d.ts.map