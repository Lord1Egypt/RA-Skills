import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';

export const resolveServerCommand = async () => {
  const distServer = path.resolve(process.cwd(), 'dist', 'api', 'server.js');
  try {
    await fs.access(distServer);
    return [process.execPath, [distServer]] as const;
  } catch {
    const tsxCli = path.resolve(process.cwd(), 'node_modules', 'tsx', 'dist', 'cli.mjs');
    return [process.execPath, [tsxCli, path.resolve(process.cwd(), 'src', 'api', 'server.ts')]] as const;
  }
};

export const launchSidecarProcess = async () => {
  const [command, args] = await resolveServerCommand();
  const child = spawn(command, args, {
    cwd: process.cwd(),
    detached: true,
    stdio: 'ignore',
    shell: false,
    env: {
      ...process.env,
      OPENCLAW_MANAGER_SERVER_PROCESS: '1',
    },
  });

  child.unref();

  return {
    pid: child.pid ?? null,
    command,
    args,
  };
};
