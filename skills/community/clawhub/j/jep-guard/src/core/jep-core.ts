import { JPEvent, JEPVerb, JEPCoreService, CausalDAG, JEPMetadata } from './types';
import { JEPCrypto } from './crypto';
import { canonicalize } from './canonical';

export class JEPCore implements JEPCoreService {
  public dag = new CausalDAG();
  private eventStore = new Map<string, JPEvent>();
  private statusMap = new Map<string, JEPMetadata['status']>();
  private crypto: JEPCrypto;

  constructor(private agentId: string, seed?: Uint8Array) {
    this.crypto = new JEPCrypto(seed);
  }

  signPayload(payload: unknown): string { return this.crypto.sign(canonicalize(payload)); }

  get publicKey(): string {
    return this.crypto.publicKey;
  }

  private createEvent(verb: JEPVerb, payload: unknown, predecessors: string[] = []): JPEvent {
    if (this.eventStore.size >= 10000) throw new Error("Event capacity exceeded; archive and restart");
    const canonical = canonicalize({ verb, who: this.agentId, payload });
    const what = JEPCrypto.sha256(canonical);
    const nonce = JEPCrypto.uuidv4();
    const now = Math.floor(Date.now() / 1000);

    const event: JPEvent = {
      jep: '1',
      verb,
      who: this.agentId,
      when: now,
      what,
      nonce,
      ref: predecessors[0] || null,
      task_based_on: predecessors[1] || null,
      extensions: payload && typeof payload === "object" && "requester" in payload ? {"https://jep.local/requester": (payload as any).requester} : {}
    };

    // Sign the canonical form (excluding sig itself)
    const toSign = canonicalize(event);
    event.sig = this.crypto.sign(toSign);

    Object.freeze(event.extensions);
    Object.freeze(event);
    this.dag.add(event);
    this.eventStore.set(nonce, event);
    this.statusMap.set(nonce, verb === 'J' ? 'pending' : 'completed');

    return event;
  }

  createJudge(payload: unknown, agent?: string, predecessors?: string[]): JPEvent {
    if (agent && agent !== this.agentId) throw new Error('Agent mismatch');
    return this.createEvent('J', payload, predecessors);
  }

  createDelegate(payload: unknown, agent?: string, predecessors?: string[]): JPEvent {
    if (agent && agent !== this.agentId) throw new Error('Agent mismatch');
    return this.createEvent('D', payload, predecessors || []);
  }

  createVerify(payload: unknown, agent?: string, predecessors?: string[]): JPEvent {
    if (agent && agent !== this.agentId) throw new Error('Agent mismatch');
    return this.createEvent('V', payload, predecessors || []);
  }

  createTerminate(payload: unknown, agent?: string, predecessors?: string[]): JPEvent {
    if (agent && agent !== this.agentId) throw new Error('Agent mismatch');
    return this.createEvent('T', payload, predecessors || []);
  }

  updateStatus(eventId: string, status: JEPMetadata['status']): void {
    this.statusMap.set(eventId, status);
  }

  getStatus(eventId: string): JEPMetadata['status'] | undefined {
    return this.statusMap.get(eventId);
  }

  getActiveDelegations(agent: string): JPEvent[] {
    return Array.from(this.eventStore.values()).filter(
      e => e.verb === 'D' && e.who === agent && this.statusMap.get(e.nonce) !== 'completed'
    );
  }

  getEvent(nonce: string): JPEvent | undefined {
    return this.eventStore.get(nonce);
  }

  verifySignature(event: JPEvent): boolean {
    if (!event.sig) return false;
    const {sig,...body}=event;
    return event.who === this.agentId && JEPCrypto.verify(canonicalize(body),sig!,this.publicKey);
  }
}