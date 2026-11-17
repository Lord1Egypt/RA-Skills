"use strict";
/**
 * JEP Core Types
 * Aligned with:
 * - draft-wang-jep-judgment-event-protocol-04
 * - draft-wang-jac-01
 * - draft-wang-hjs-accountability-04
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.CausalDAG = void 0;
/**
 * Causal DAG — in-memory graph of events
 */
class CausalDAG {
    nodes = new Map();
    edges = new Map();
    add(event) {
        this.nodes.set(event.nonce, event);
        for (const pred of [event.ref, event.task_based_on].filter(Boolean)) {
            if (!this.edges.has(pred))
                this.edges.set(pred, new Set());
            this.edges.get(pred).add(event.nonce);
        }
    }
    get(id) {
        return this.nodes.get(id);
    }
    hasCycle(from, to) {
        const ancestors = this.ancestors(to);
        return ancestors.some(e => e.nonce === from || e.who === from);
    }
    ancestors(eventId) {
        const result = [];
        const visited = new Set();
        const stack = [];
        const start = this.nodes.get(eventId);
        if (start?.ref)
            stack.push(start.ref);
        if (start?.task_based_on)
            stack.push(start.task_based_on);
        while (stack.length) {
            const id = stack.pop();
            if (visited.has(id))
                continue;
            visited.add(id);
            const node = this.nodes.get(id);
            if (node) {
                result.push(node);
                if (node.ref)
                    stack.push(node.ref);
                if (node.task_based_on)
                    stack.push(node.task_based_on);
            }
        }
        return result;
    }
    serialize() {
        return JSON.stringify({ events: Array.from(this.nodes.values()) }, null, 2);
    }
}
exports.CausalDAG = CausalDAG;
//# sourceMappingURL=types.js.map