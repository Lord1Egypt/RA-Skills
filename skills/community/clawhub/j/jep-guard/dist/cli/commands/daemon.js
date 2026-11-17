"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.daemonCommand = void 0;
const commander_1 = require("commander");
const server_1 = require("../../daemon/server");
exports.daemonCommand = new commander_1.Command('daemon')
    .description('Start JEP Guard daemon')
    .option('--mode <mode>', 'daemon mode', 'full')
    .option('--port <port>', 'IPC port (default: unix socket)')
    .action(async (options) => {
    const daemon = new server_1.GuardDaemon(options.mode);
    // Graceful shutdown
    process.on('SIGINT', () => {
        console.log('\n🛑 Shutting down JEP Guard...');
        daemon.stop();
        process.exit(0);
    });
    process.on('SIGTERM', () => {
        daemon.stop();
        process.exit(0);
    });
    await daemon.start();
    console.log(`🚀 JEP Guard v3.0.0 daemon running in ${options.mode} mode`);
    console.log(`   IPC Socket: ${daemon.socketPath}`);
    console.log(`   PID: ${process.pid}`);
    console.log('\nPress Ctrl+C to stop\n');
});
//# sourceMappingURL=daemon.js.map