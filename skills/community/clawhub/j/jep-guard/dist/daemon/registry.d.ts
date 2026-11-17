import { SkillIdentity } from '../core/types';
export declare class SkillRegistryService {
    private skills;
    constructor(configDir?: string);
    register(manifest: Partial<SkillIdentity> & {
        name: string;
        version: string;
    }): SkillIdentity;
    get(skillId: string): SkillIdentity | undefined;
    list(): SkillIdentity[];
    verifySignature(skillId: string, message: string, signature: string): boolean;
}
