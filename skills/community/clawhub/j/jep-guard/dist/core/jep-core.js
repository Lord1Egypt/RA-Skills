"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.JEPCore = void 0;
const types_1 = require("./types");
const crypto_1 = require("./crypto");
const canonical_1 = require("./canonical");
class JEPCore {
    agentId;
    dag = new types_1.CausalDAG();
    eventStore = new Map();
    statusMap = new Map();
    crypto;
    constructor(agentId, seed) {
        this.agentId = agentId;
        this.crypto = new crypto_1.JEPCrypto(seed);
    }
    signPayload(payload) { return this.crypto.sign((0, canonical_1.canonicalize)(payload)); }
    get publicKey() {
        return this.crypto.publicKey;
    }
    createEvent(verb, payload, predecessors = []) {
        if (this.eventStore.size >= 10000)
            throw new Error("Event capacity exceeded; archive and restart");
        const canonical = (0, canonical_1.canonicalize)({ verb, who: this.agentId, payload });
        const what = crypto_1.JEPCrypto.sha256(canonical);
        const nonce = crypto_1.JEPCrypto.uuidv4();
        const now = Math.floor(Date.now() / 1000);
        const event = {
            jep: '1',
            verb,
            who: this.agentId,
            when: now,
            what,
            nonce,
            ref: predecessors[0] || null,
            task_based_on: predecessors[1] || null,
            extensions: payload && typeof payload === "object" && "requester" in payload ? { "https://jep.local/requester": payload.requester } : {}
        };
        // Sign the canonical form (excluding sig itself)
        const toSign = (0, canonical_1.canonicalize)(event);
        event.sig = this.crypto.sign(toSign);
        Object.freeze(event.extensions);
        Object.freeze(event);
        this.dag.add(event);
        this.eventStore.set(nonce, event);
        this.statusMap.set(nonce, verb === 'J' ? 'pending' : 'completed');
        return event;
    }
    createJudge(payload, agent, predecessors) {
        if (agent && agent !== this.agentId)
            throw new Error('Agent mismatch');
        return this.createEvent('J', payload, predecessors);
    }
    createDelegate(payload, agent, predecessors) {
        if (agent && agent !== this.agentId)
            throw new Error('Agent mismatch');
        return this.createEvent('D', payload, predecessors || []);
    }
    createVerify(payload, agent, predecessors) {
        if (agent && agent !== this.agentId)
            throw new Error('Agent mismatch');
        return this.createEvent('V', payload, predecessors || []);
    }
    createTerminate(payload, agent, predecessors) {
        if (agent && agent !== this.agentId)
            throw new Error('Agent mismatch');
        return this.createEvent('T', payload, predecessors || []);
    }
    updateStatus(eventId, status) {
        this.statusMap.set(eventId, status);
    }
    getStatus(eventId) {
        return this.statusMap.get(eventId);
    }
    getActiveDelegations(agent) {
        return Array.from(this.eventStore.values()).filter(e => e.verb === 'D' && e.who === agent && this.statusMap.get(e.nonce) !== 'completed');
    }
    getEvent(nonce) {
        return this.eventStore.get(nonce);
    }
    verifySignature(event) {
        if (!event.sig)
            return false;
        const { sig, ...body } = event;
        return event.who === this.agentId && crypto_1.JEPCrypto.verify((0, canonical_1.canonicalize)(body), sig, this.publicKey);
    }
}
exports.JEPCore = JEPCore;
//# sourceMappingURL=jep-core.js.map