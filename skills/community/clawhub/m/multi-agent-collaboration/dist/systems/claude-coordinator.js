"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ClaudeCoordinator = void 0;
const verification_1 = require("./verification");
const safety_1 = require("./safety");
const claude_memory_1 = require("../core/claude-memory");
class ClaudeCoordinator {
    constructor(memory) {
        this.memory = memory || new claude_memory_1.ClaudeMemorySystem();
        this.verifier = new verification_1.VerificationAgent();
        this.safety = new safety_1.SafetyGatePipeline();
    }
    buildRun(request) {
        const retrievedMemory = this.memory.formatRetrievedContext(request, 5);
        return {
            request,
            retrievedMemory,
            tasks: [
                { role: 'coordinator', objective: 'Split the request into a managed task graph.', evidenceRequired: true },
                { role: 'explorer', objective: 'Read the code or artifacts and return evidence only.', evidenceRequired: true },
                { role: 'planner', objective: 'Turn evidence into a concrete execution plan.', evidenceRequired: true },
                { role: 'implementer', objective: 'Apply only the scoped change set.', evidenceRequired: true },
                { role: 'verifier', objective: 'Reject unsupported success and demand runnable proof.', evidenceRequired: true },
                { role: 'reviewer', objective: 'Check residual risk and missing tests.', evidenceRequired: true }
            ]
        };
    }
    auditCommand(command) {
        return this.safety.audit(command);
    }
    verify(checks) {
        return this.verifier.verify(checks);
    }
}
exports.ClaudeCoordinator = ClaudeCoordinator;
exports.default = ClaudeCoordinator;
