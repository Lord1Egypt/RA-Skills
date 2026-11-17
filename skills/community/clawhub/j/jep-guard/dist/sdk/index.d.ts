export declare class JEPGuardSDK {
    private socketPath;
    private skillId;
    constructor(skillId: string, socketPath?: string);
    private call;
    judge(decision: {
        action: string;
        target?: string;
        context?: unknown;
    }): Promise<any>;
    delegate(target: string, scope: string[], payload?: unknown): Promise<any>;
    verify(targetEvent: string, verdict: 'approved' | 'rejected', evidence?: string[]): Promise<any>;
    terminate(targetEvent: string, reason: string): Promise<any>;
}
export declare function init(skillId: string): JEPGuardSDK;
