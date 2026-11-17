import { ReputationScore, JPEvent } from '../core/types';
export declare class ReputationEngineService {
    private scores;
    recordEvent(skillId: string, event: JPEvent, latencyMs?: number): void;
    get(skillId: string): ReputationScore;
    list(): ReputationScore[];
}
