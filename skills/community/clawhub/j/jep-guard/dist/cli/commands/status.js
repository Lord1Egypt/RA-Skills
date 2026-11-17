"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.statusCommand = void 0;
const commander_1 = require("commander");
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const os_1 = __importDefault(require("os"));
exports.statusCommand = new commander_1.Command('status')
    .description('Show JEP Guard status')
    .action(async () => {
    const configDir = path_1.default.join(os_1.default.homedir(), '.jep-guard');
    const socketPath = path_1.default.join(configDir, 'guard.sock');
    console.log('\n🛡️  JEP Guard v3.0.0 Status\n');
    // Config
    const configPath = path_1.default.join(configDir, 'config.json');
    if (fs_1.default.existsSync(configPath)) {
        const config = JSON.parse(fs_1.default.readFileSync(configPath, 'utf-8'));
        console.log(`Mode:      ${config.mode}`);
        console.log(`Version:   ${config.version}`);
        console.log(`Daemon:    ${fs_1.default.existsSync(socketPath) ? 'Socket exists; liveness unverified' : 'No socket'}`);
    }
    else {
        console.log('❌ Not initialized. Run: claw run jep-guard init');
        return;
    }
    // Stats
    const auditPath = path_1.default.join(configDir, 'audit-stream.jep');
    if (fs_1.default.existsSync(auditPath)) {
        const stats = fs_1.default.statSync(auditPath);
        console.log(`Audit Log: ${(stats.size / 1024).toFixed(1)} KB`);
    }
    console.log('\nQuick commands:');
    console.log('  claw run jep-guard daemon          Start daemon');
    console.log('  claw run jep-guard log --last     View recent events');
    console.log('  claw run jep-guard dashboard      Interactive dashboard');
});
//# sourceMappingURL=status.js.map