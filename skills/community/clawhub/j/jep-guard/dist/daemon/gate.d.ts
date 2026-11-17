import { ExecutionRequest, GateResult } from '../core/types';
import { JEPCore } from '../core/jep-core';
import { SkillRegistryService } from './registry';
import { PolicyEngineService } from './policy';
import { ExtensionLoaderService } from '../extensions/loader';
export declare class CausalGateService {
    private core;
    private registry;
    private policy;
    private extensions;
    constructor(core: JEPCore, registry: SkillRegistryService, policy: PolicyEngineService, extensions: ExtensionLoaderService);
    process(req: ExecutionRequest): Promise<GateResult>;
    private issueCapabilityToken;
}
