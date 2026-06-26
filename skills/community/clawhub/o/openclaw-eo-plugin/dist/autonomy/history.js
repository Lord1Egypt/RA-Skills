/**
 * Decision History
 */
export class DecisionHistory {
    history = new Map();
    maxSize = 500;
    add(decision, outcome) {
        this.history.set(decision.id, { decision, outcome, createdAt: Date.now() });
        if (this.history.size > this.maxSize)
            this.prune();
    }
    get(id) { return this.history.get(id); }
    getRecent(limit = 50) {
        return Array.from(this.history.values()).sort((a, b) => b.createdAt - a.createdAt).slice(0, limit);
    }
    prune() {
        const entries = Array.from(this.history.entries()).sort((a, b) => a[1].createdAt - b[1].createdAt);
        const toRemove = entries.slice(0, Math.floor(this.maxSize * 0.2));
        toRemove.forEach(([id]) => this.history.delete(id));
    }
    size() { return this.history.size; }
    clear() { this.history.clear(); }
}
export const decisionHistory = new DecisionHistory();
//# sourceMappingURL=history.js.map