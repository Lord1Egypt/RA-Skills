"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.GuardDaemon = void 0;
const net_1 = __importDefault(require("net"));
const path_1 = __importDefault(require("path"));
const fs_1 = __importDefault(require("fs"));
const crypto_1 = require("crypto");
const jep_core_1 = require("../core/jep-core");
const canonical_1 = require("../core/canonical");
const registry_1 = require("./registry");
const policy_1 = require("./policy");
const gate_1 = require("./gate");
const reputation_1 = require("./reputation");
const audit_1 = require("./audit");
const loader_1 = require("../extensions/loader");
class GuardDaemon {
    mode;
    socketPath;
    server;
    core;
    registry;
    audit;
    gate;
    grants = new Map();
    connections = new Set();
    listening = false;
    constructor(mode) {
        this.mode = mode;
        if (mode !== 'full')
            throw new Error('Daemon requires explicit full mode');
        const { dir, secureDir, readPrivate } = require('../../transport');
        const folder = dir();
        secureDir(folder);
        this.socketPath = path_1.default.join(folder, 'guard.sock');
        const keyfile = path_1.default.join(folder, 'daemon-seed');
        if (!fs_1.default.existsSync(keyfile))
            fs_1.default.writeFileSync(keyfile, (0, crypto_1.randomBytes)(32).toString('base64'), { mode: 0o600, flag: 'wx' });
        const seed = Buffer.from(readPrivate(keyfile).trim(), 'base64');
        this.core = new jep_core_1.JEPCore('jep-guard-daemon', seed);
        const publicfile = path_1.default.join(folder, 'daemon-publickey');
        if (fs_1.default.existsSync(publicfile)) {
            if (readPrivate(publicfile).trim() !== this.core.publicKey)
                throw new Error('Daemon key pin mismatch');
        }
        else
            fs_1.default.writeFileSync(publicfile, this.core.publicKey, { mode: 0o600, flag: 'wx' });
        this.registry = new registry_1.SkillRegistryService(folder);
        this.audit = new audit_1.AuditStreamService(folder);
        const policy = new policy_1.PolicyEngineService(path_1.default.join(folder, 'policy.json'));
        const extensions = new loader_1.ExtensionLoaderService({ core: this.core, registry: this.registry, policy, reputation: new reputation_1.ReputationEngineService(), audit: this.audit });
        this.gate = new gate_1.CausalGateService(this.core, this.registry, policy, extensions);
    }
    async start() {
        // Never unlink someone else's/live socket automatically. Operator removes stale sockets explicitly.
        if (fs_1.default.existsSync(this.socketPath))
            throw new Error('Socket already exists; check for a running daemon');
        this.server = net_1.default.createServer(socket => {
            if (this.connections.size >= 64) {
                socket.destroy();
                return;
            }
            this.connections.add(socket);
            socket.on('close', () => this.connections.delete(socket));
            socket.on('error', () => socket.destroy());
            socket.setTimeout(5000, () => socket.destroy());
            const challenge = (0, crypto_1.randomBytes)(32).toString('hex');
            socket.write(JSON.stringify({ challenge }) + '\n');
            let buffer = Buffer.alloc(0), handled = false;
            socket.on('data', async (chunk) => {
                if (handled)
                    return;
                buffer = Buffer.concat([buffer, chunk]);
                if (buffer.length > 65536) {
                    handled = true;
                    socket.destroy();
                    return;
                }
                const newline = buffer.indexOf(10);
                if (newline < 0)
                    return;
                handled = true;
                try {
                    if (newline !== buffer.length - 1)
                        throw new Error('One request per connection');
                    const { sig, ...req } = JSON.parse(buffer.subarray(0, newline).toString('utf8'));
                    if (req.challenge !== challenge || !req.payload || typeof req.payload !== 'object' || Array.isArray(req.payload) || !this.registry.verifySignature(req.skill, (0, canonical_1.canonicalize)(req), sig))
                        throw new Error('Unauthenticated request');
                    const result = await this.handleRequest(req);
                    socket.end(JSON.stringify(result) + '\n');
                }
                catch (err) {
                    socket.end(JSON.stringify({ error: err instanceof Error ? err.message : 'Request rejected' }) + '\n');
                }
            });
        });
        await new Promise((resolve, reject) => {
            this.server.once('error', reject);
            this.server.listen(this.socketPath, () => {
                try {
                    fs_1.default.chmodSync(this.socketPath, 0o600);
                    this.listening = true;
                    resolve();
                }
                catch (e) {
                    this.server.close();
                    reject(e);
                }
            });
        });
    }
    stop() {
        for (const socket of this.connections)
            socket.destroy();
        this.server?.close();
        if (this.listening && fs_1.default.existsSync(this.socketPath))
            fs_1.default.unlinkSync(this.socketPath);
        this.listening = false;
    }
    async handleRequest(req) {
        switch (req.method) {
            case 'REGISTER_SKILL':
                if (req.payload.name !== req.skill)
                    throw new Error('Identity mismatch');
                return { success: true, skill_id: this.registry.register(req.payload).skill_id };
            case 'JUDGE': {
                if (typeof req.payload.action !== 'string' || typeof req.payload.target !== 'string')
                    throw new Error('Action and target are required');
                const identity = this.registry.get(req.skill);
                if (!identity.capabilities.includes(req.payload.action))
                    throw new Error('Action is outside assigned capabilities');
                const result = await this.gate.process({ requester: req.skill, action: req.payload.action, target: req.payload.target, type: 'system_call', context: req.payload.context });
                if (result.event)
                    await this.audit.emit(result.event);
                if (result.action === 'allow')
                    this.grants.set(result.event.nonce, req.skill);
                return result;
            }
            case 'VERIFY':
            case 'TERMINATE': {
                const target = req.payload.target_event;
                if (typeof target !== 'string' || this.grants.get(target) !== req.skill)
                    throw new Error('No active owned grant');
                // Consume before asynchronous audit to prevent duplicate completion races.
                this.grants.delete(target);
                const payload = { ...req.payload, requester: req.skill, source: 'authenticated_client_report' };
                const event = req.method === 'VERIFY' ? this.core.createVerify(payload, undefined, [target]) : this.core.createTerminate(payload, undefined, [target]);
                await this.audit.emit(event);
                this.core.updateStatus(target, 'completed');
                return { success: true, event };
            }
            case 'DELEGATE': throw new Error('Authenticated receiver transport is required; legacy cross-skill routing is disabled');
            default: throw new Error('Unknown method');
        }
    }
}
exports.GuardDaemon = GuardDaemon;
//# sourceMappingURL=server.js.map