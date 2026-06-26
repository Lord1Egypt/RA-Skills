import { Command } from 'commander';
import { GuardDaemon } from '../../daemon/server';

export const daemonCommand = new Command('daemon')
  .description('Start JEP Guard daemon')
  .option('--mode <mode>', 'daemon mode', 'skill_os')
  .option('--port <port>', 'IPC port (default: unix socket)')
  .action(async (options) => {
    const daemon = new GuardDaemon(options.mode);

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
    console.log(`🚀 JEP Guard v2.0.4 daemon running in ${options.mode} mode`);
    console.log(`   IPC Socket: ${daemon.socketPath}`);
    console.log(`   PID: ${process.pid}`);
    console.log('\nPress Ctrl+C to stop\n');
  });