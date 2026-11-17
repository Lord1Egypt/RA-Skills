import { JPEvent, JEPCoreService, CausalDAG, JEPMetadata } from './types';
export declare class JEPCore implements JEPCoreService {
    private agentId;
    dag: CausalDAG;
    private eventStore;
    private statusMap;
    private crypto;
    constructor(agentId: string, seed?: Uint8Array);
    signPayload(payload: unknown): string;
    get publicKey(): string;
    private createEvent;
    createJudge(payload: unknown, agent?: string, predecessors?: string[]): JPEvent;
    createDelegate(payload: unknown, agent?: string, predecessors?: string[]): JPEvent;
    createVerify(payload: unknown, agent?: string, predecessors?: string[]): JPEvent;
    createTerminate(payload: unknown, agent?: string, predecessors?: string[]): JPEvent;
    updateStatus(eventId: string, status: JEPMetadata['status']): void;
    getStatus(eventId: string): JEPMetadata['status'] | undefined;
    getActiveDelegations(agent: string): JPEvent[];
    getEvent(nonce: string): JPEvent | undefined;
    verifySignature(event: JPEvent): boolean;
}
