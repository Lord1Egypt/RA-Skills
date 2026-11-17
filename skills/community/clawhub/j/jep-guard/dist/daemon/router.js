"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CausalRouterService = void 0;
class CausalRouterService {
    core;
    gate;
    constructor(core, gate) {
        this.core = core;
        this.gate = gate;
    }
    async route(req) {
        return { success: false, error: 'Cross-skill execution requires a separately authenticated receiver; legacy /tmp routing is disabled' };
    }
}
exports.CausalRouterService = CausalRouterService;
//# sourceMappingURL=router.js.map