"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AuditStreamService = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const os_1 = __importDefault(require("os"));
class AuditStreamService {
    streamPath;
    events = [];
    maxMemoryEvents = 10000;
    constructor(configDir) {
        const dir = configDir || path_1.default.join(os_1.default.homedir(), '.jep-guard');
        if (!fs_1.default.existsSync(dir))
            fs_1.default.mkdirSync(dir, { recursive: true, mode: 0o700 });
        this.streamPath = path_1.default.join(dir, 'audit-stream.jep');
        this.load();
    }
    async emit(event) {
        this.events.push(JSON.parse(JSON.stringify(event)));
        // Rotate if too many in memory
        if (this.events.length > this.maxMemoryEvents) {
            this.events = this.events.slice(-this.maxMemoryEvents / 2);
        }
        const line = JSON.stringify(event) + '\n';
        const fd = fs_1.default.openSync(this.streamPath, fs_1.default.constants.O_WRONLY | fs_1.default.constants.O_APPEND | fs_1.default.constants.O_CREAT | fs_1.default.constants.O_NOFOLLOW, 0o600);
        try {
            if (fs_1.default.fstatSync(fd).size + Buffer.byteLength(line) > 16777216)
                throw new Error('Archive audit log before continuing');
            fs_1.default.writeSync(fd, line);
        }
        finally {
            fs_1.default.closeSync(fd);
        }
    }
    async query(filter) {
        return this.events.filter(e => {
            if (filter.since && e.when * 1000 < filter.since.getTime())
                return false;
            if (filter.agent && e.who !== filter.agent)
                return false;
            if (filter.verb && e.verb !== filter.verb)
                return false;
            return true;
        });
    }
    export(format = 'jep', events = this.events) {
        if (format === 'jep') {
            return JSON.stringify({ events }, null, 2);
        }
        return JSON.stringify(events, null, 2);
    }
    stats() {
        const byVerb = {};
        for (const e of this.events) {
            byVerb[e.verb] = (byVerb[e.verb] || 0) + 1;
        }
        return {
            total: this.events.length,
            byVerb,
            sizeBytes: fs_1.default.existsSync(this.streamPath) ? fs_1.default.statSync(this.streamPath).size : 0
        };
    }
    load() {
        if (!fs_1.default.existsSync(this.streamPath))
            return;
        const stat = fs_1.default.lstatSync(this.streamPath);
        if (stat.isSymbolicLink() || (stat.mode & 0o077) || stat.size > 16777216)
            throw new Error('Audit file needs secure archival before startup');
        const lines = fs_1.default.readFileSync(this.streamPath, 'utf-8').split('\n').filter(Boolean);
        // Only load last N events to memory
        const recent = lines.slice(-this.maxMemoryEvents);
        for (const line of recent) {
            try {
                this.events.push(JSON.parse(line));
            }
            catch { }
        }
    }
}
exports.AuditStreamService = AuditStreamService;
//# sourceMappingURL=audit.js.map