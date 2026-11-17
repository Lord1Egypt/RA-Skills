"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ExtensionLoaderService = void 0;
class ExtensionLoaderService {
    extensions = new Map();
    context;
    constructor(ctx) {
        this.context = ctx;
    }
    async loadBuiltins() {
        // Optional integrations require explicit, reviewed adapters. No mutable global hooks.
    }
    async evaluateAll(request) {
        const results = [];
        for (const [name, ext] of this.extensions) {
            if (ext.evaluate) {
                const res = await ext.evaluate(request);
                results.push({ ...res, extension: name });
            }
        }
        return results;
    }
    get(name) {
        return this.extensions.get(name);
    }
    getReputation(skillId) {
        return this.context.reputation.get(skillId);
    }
}
exports.ExtensionLoaderService = ExtensionLoaderService;
//# sourceMappingURL=loader.js.map