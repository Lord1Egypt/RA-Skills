import { ClaudeMemorySystem } from '../core/claude-memory';
import { VerificationAgent, VerificationCheck } from './verification';
import { SafetyGatePipeline } from './safety';

export class ClaudeCoordinator {
  private memory: ClaudeMemorySystem;
  private verifier: VerificationAgent;
  private safety: SafetyGatePipeline;

  constructor(memory?: ClaudeMemorySystem) {
    this.memory = memory || new ClaudeMemorySystem();
    this.verifier = new VerificationAgent();
    this.safety = new SafetyGatePipeline();
  }

  buildRun(request: string) {
    return {
      request,
      retrievedMemory: this.memory.formatRetrievedContext(request, 5),
      tasks: [
        { role: 'coordinator', objective: 'Split request into a task graph.', evidenceRequired: true },
        { role: 'explorer', objective: 'Return evidence only.', evidenceRequired: true },
        { role: 'planner', objective: 'Turn evidence into an execution plan.', evidenceRequired: true },
        { role: 'implementer', objective: 'Apply scoped changes.', evidenceRequired: true },
        { role: 'verifier', objective: 'Demand runnable proof.', evidenceRequired: true },
        { role: 'reviewer', objective: 'Surface residual risk.', evidenceRequired: true }
      ]
    };
  }

  auditCommand(command: string) {
    return this.safety.audit(command);
  }

  verify(checks: VerificationCheck[]) {
    return this.verifier.verify(checks);
  }
}

export default ClaudeCoordinator;
