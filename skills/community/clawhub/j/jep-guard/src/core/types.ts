/**
 * JEP Core Types
 * Aligned with:
 * - draft-wang-jep-judgment-event-protocol-04
 * - draft-wang-jac-01
 * - draft-wang-hjs-accountability-04
 */

export type JEPVerb = 'J' | 'D' | 'T' | 'V';

export interface JEPPayload {
  action?: string;
  target?: string;
  context?: Record<string, unknown>;
  [key: string]: unknown;
}

export interface JEPExtensions {
  [uri: string]: unknown;
}

/**
 * JEP Event — wire format
 * Matches IETF draft exactly
 */
export interface JPEvent {
  jep: '1';
  verb: JEPVerb;
  who: string;           // DID / URI / pubkey hash
  when: number;          // Unix timestamp (seconds)
  what: string | null;   // multihash or null
  nonce: string;         // UUIDv4
  aud?: string;          // intended recipient
  ref: string | null;    // parent event hash (HJS chain)
  task_based_on?: string | null; // JAC: parent judgment hash
  extensions?: JEPExtensions;
  sig?: string;          // JWS (RFC 7515)
}

/**
 * Internal metadata (not serialized to wire)
 */
export interface JEPMetadata {
  event_id: string;      // internal UUID
  status: 'pending' | 'granted' | 'denied' | 'expired' | 'completed';
  local_timestamp: number; // ms
}

export interface SkillIdentity {
  skill_id: string;
  name: string;
  version: string;
  pubkey: string;        // base64 Ed25519 pubkey
  capabilities: string[];
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  installed_at: number;
  last_seen: number;
  extensions: string[];
  metadata: {
    author?: string;
    source?: string;
    tee_attestation?: string;
  };
}

export interface ExecutionRequest {
  requester: string;
  action: string;
  target: string;
  type: 'system_call' | 'skill_delegate' | 'api_call' | 'model_inference';
  context?: Record<string, unknown>;
}

export interface GateResult {
  action: 'allow' | 'block' | 'review';
  reason: string;
  event?: JPEvent;
  capabilityToken?: string;
  requiredVerifiers?: string[];
}

export interface PolicyRule {
  id: string;
  match: {
    action?: string;
    target?: string;
    skill?: string;
    risk_level?: string;
  };
  decision: 'allow' | 'deny' | 'review';
  required_verifiers?: string[];
  rate_limit?: { max: number; window: number };
}

export interface PolicyResult {
  decision: 'allow' | 'deny' | 'review';
  rule_matched?: string;
  required_verifiers?: string[];
}

export interface RouteRequest {
  from: string;
  to: string;
  scope: string[];
  payload: unknown;
  timeout?: number;
}

export interface RouteResult {
  success: boolean;
  event?: JPEvent;
  output?: unknown;
  error?: string;
}

export interface ReputationScore {
  skill_id: string;
  total_judgments: number;
  completed: number;
  terminated: number;
  completionRate: number;
  violationRate: number;
  avg_latency_ms: number;
  last_updated: number;
}

export interface Extension {
  name: string;
  version: string;
  init(context: GuardContext): Promise<void>;
  evaluate?(request: ExecutionRequest): Promise<ExtensionResult>;
  onEvent?(event: JPEvent): Promise<void>;
}

export interface ExtensionResult {
  action: 'allow' | 'block' | 'review';
  rule_matched?: string;
  metadata?: Record<string, unknown>;
}

export interface GuardContext {
  core: JEPCoreService;
  registry: SkillRegistry;
  policy: PolicyEngine;
  reputation: ReputationEngine;
  audit: AuditStream;
}

export interface JEPCoreService {
  createJudge(payload: unknown, agent: string, predecessors?: string[]): JPEvent;
  createDelegate(payload: unknown, agent: string, predecessors: string[]): JPEvent;
  createVerify(payload: unknown, agent: string, predecessors: string[]): JPEvent;
  createTerminate(payload: unknown, agent: string, predecessors: string[]): JPEvent;
  updateStatus(eventId: string, status: JPEvent['status']): void;
  getActiveDelegations(agent: string): JPEvent[];
  dag: CausalDAG;
}

export interface SkillRegistry {
  get(skillId: string): SkillIdentity | undefined;
  list(): SkillIdentity[];
}

export interface PolicyEngine {
  evaluate(req: ExecutionRequest, skill: SkillIdentity): Promise<PolicyResult>;
}

export interface ReputationEngine {
  get(skillId: string): ReputationScore;
}

export interface AuditStream {
  emit(event: JPEvent): Promise<void>;
  query(filter: AuditFilter): Promise<JPEvent[]>;
}

export interface AuditFilter {
  since?: Date;
  agent?: string;
  verb?: JEPVerb;
}

/**
 * Causal DAG — in-memory graph of events
 */
export class CausalDAG {
  private nodes = new Map<string, JPEvent>();
  private edges = new Map<string, Set<string>>();

  add(event: JPEvent): void {
    this.nodes.set(event.nonce, event);

    for (const pred of [event.ref, event.task_based_on].filter(Boolean)) {
      if (!this.edges.has(pred!)) this.edges.set(pred!, new Set());
      this.edges.get(pred!)!.add(event.nonce);
    }
  }

  get(id: string): JPEvent | undefined {
    return this.nodes.get(id);
  }

  hasCycle(from: string, to: string): boolean {
    const ancestors = this.ancestors(to);
    return ancestors.some(e => e.nonce === from || e.who === from);
  }

  ancestors(eventId: string): JPEvent[] {
    const result: JPEvent[] = [];
    const visited = new Set<string>();
    const stack: string[] = [];

    const start = this.nodes.get(eventId);
    if (start?.ref) stack.push(start.ref);
    if (start?.task_based_on) stack.push(start.task_based_on);

    while (stack.length) {
      const id = stack.pop()!;
      if (visited.has(id)) continue;
      visited.add(id);

      const node = this.nodes.get(id);
      if (node) {
        result.push(node);
        if (node.ref) stack.push(node.ref);
        if (node.task_based_on) stack.push(node.task_based_on);
      }
    }
    return result;
  }

  serialize(): string {
    return JSON.stringify({ events: Array.from(this.nodes.values()) }, null, 2);
  }
}