import { Extension, ExtensionResult, ExecutionRequest, GuardContext } from '../core/types';
export declare class ExtensionLoaderService {
    private extensions;
    private context;
    constructor(ctx: GuardContext);
    loadBuiltins(): Promise<void>;
    evaluateAll(request: ExecutionRequest): Promise<ExtensionResult[]>;
    get(name: string): Extension | undefined;
    getReputation(skillId: string): import("../core/types").ReputationScore;
}
