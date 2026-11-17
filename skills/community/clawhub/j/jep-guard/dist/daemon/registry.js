"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.SkillRegistryService = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const os_1 = __importDefault(require("os"));
const crypto_1 = require("../core/crypto");
class SkillRegistryService {
    skills = new Map();
    constructor(configDir) {
        const dir = configDir || path_1.default.join(os_1.default.homedir(), '.jep-guard');
        const { secureDir, readPrivate, validId } = require('../../transport');
        secureDir(dir);
        const file = path_1.default.join(dir, 'allowed-skills.json');
        if (fs_1.default.existsSync(file)) {
            const entries = JSON.parse(readPrivate(file));
            if (!Array.isArray(entries) || entries.length > 128)
                throw new Error('Invalid skill allowlist');
            for (const entry of entries) {
                if (!validId(entry.name) || typeof entry.pubkey !== 'string' || Buffer.from(entry.pubkey, 'base64').length !== 32 || !Array.isArray(entry.capabilities) || entry.capabilities.some((c) => typeof c !== 'string'))
                    throw new Error('Invalid trusted skill');
                if (this.skills.has(entry.name))
                    throw new Error('Duplicate skill identity');
                const identity = { skill_id: entry.name, name: entry.name, version: entry.version || '1', pubkey: entry.pubkey, capabilities: entry.capabilities, risk_level: 'high', installed_at: Date.now(), last_seen: Date.now(), extensions: [], metadata: { source: 'operator-allowlist' } };
                this.skills.set(entry.name, identity);
            }
        }
    }
    register(manifest) {
        const existing = this.get(manifest.name);
        if (!existing || (manifest.pubkey && manifest.pubkey !== existing.pubkey) || manifest.version !== existing.version || JSON.stringify(manifest.capabilities || []) !== JSON.stringify(existing.capabilities))
            throw new Error('Operator approval required for registration changes');
        return existing;
    }
    get(skillId) { const entry = this.skills.get(skillId); return entry ? JSON.parse(JSON.stringify(entry)) : undefined; }
    list() { return [...this.skills.keys()].map(k => this.get(k)); }
    verifySignature(skillId, message, signature) {
        const entry = this.skills.get(skillId);
        return !!entry && crypto_1.JEPCrypto.verify(message, signature, entry.pubkey);
    }
}
exports.SkillRegistryService = SkillRegistryService;
//# sourceMappingURL=registry.js.map