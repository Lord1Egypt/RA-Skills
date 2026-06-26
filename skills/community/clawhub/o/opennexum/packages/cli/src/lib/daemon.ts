import { access, mkdir, unlink, writeFile } from 'node:fs/promises';
import { execFile } from 'node:child_process';
import path from 'node:path';
import os from 'node:os';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);

export type DaemonStatus = 'running' | 'stopped' | 'not_installed' | 'unsupported';

const PLIST_LABEL = 'com.nexum.watch';
const PLIST_PATH = path.join(
  os.homedir(),
  'Library',
  'LaunchAgents',
  `${PLIST_LABEL}.plist`
);
const SYSTEMD_SERVICE = 'nexum-watch.service';
const SYSTEMD_PATH = path.join(
  os.homedir(),
  '.config',
  'systemd',
  'user',
  SYSTEMD_SERVICE
);
const NEXUM_LOG = path.join(os.homedir(), '.nexum', 'watch.log');
const NEXUM_ERR_LOG = path.join(os.homedir(), '.nexum', 'watch.err.log');

type Platform = 'macos' | 'linux' | 'other';

function getPlatform(): Platform {
  if (process.platform === 'darwin') return 'macos';
  if (process.platform === 'linux') return 'linux';
  return 'other';
}

async function whichNexum(): Promise<string> {
  try {
    const { stdout } = await execFileAsync('which', ['nexum']);
    return stdout.trim() || 'nexum';
  } catch {
    return 'nexum';
  }
}

function makePlist(nexumBin: string): string {
  return `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${PLIST_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${nexumBin}</string>
    <string>watch</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${NEXUM_LOG}</string>
  <key>StandardErrorPath</key>
  <string>${NEXUM_ERR_LOG}</string>
</dict>
</plist>
`;
}

function makeSystemdService(nexumBin: string): string {
  return `[Unit]
Description=Nexum Watch Daemon
After=network.target

[Service]
ExecStart=${nexumBin} watch
Restart=on-failure
StandardOutput=append:${NEXUM_LOG}
StandardError=append:${NEXUM_ERR_LOG}

[Install]
WantedBy=default.target
`;
}

export async function installDaemon(): Promise<void> {
  const platform = getPlatform();
  const nexumBin = await whichNexum();

  if (platform === 'macos') {
    await mkdir(path.dirname(PLIST_PATH), { recursive: true });
    await mkdir(path.dirname(NEXUM_LOG), { recursive: true });
    await writeFile(PLIST_PATH, makePlist(nexumBin), 'utf8');
    try {
      await execFileAsync('launchctl', ['load', PLIST_PATH]);
    } catch {
      // Already loaded or not running — ignore
    }
    console.log(`✓ LaunchAgent installed: ${PLIST_PATH}`);
    console.log('  nexum watch will start automatically on login.');
  } else if (platform === 'linux') {
    await mkdir(path.dirname(SYSTEMD_PATH), { recursive: true });
    await mkdir(path.dirname(NEXUM_LOG), { recursive: true });
    await writeFile(SYSTEMD_PATH, makeSystemdService(nexumBin), 'utf8');
    try {
      await execFileAsync('systemctl', ['--user', 'daemon-reload']);
      await execFileAsync('systemctl', ['--user', 'enable', '--now', SYSTEMD_SERVICE]);
    } catch (err) {
      console.warn(
        `警告: systemctl 调用失败，service 文件已写入但可能未激活: ${err instanceof Error ? err.message : err}`
      );
    }
    console.log(`✓ systemd user service installed: ${SYSTEMD_PATH}`);
  } else {
    console.log('当前操作系统不支持自动安装守护进程。');
    console.log('请手动运行: nexum watch');
  }
}

export async function uninstallDaemon(): Promise<void> {
  const platform = getPlatform();

  if (platform === 'macos') {
    try {
      await execFileAsync('launchctl', ['unload', PLIST_PATH]);
    } catch {
      // Not loaded — ignore
    }
    try {
      await unlink(PLIST_PATH);
    } catch {
      // Already removed — ignore
    }
    console.log('✓ LaunchAgent removed.');
  } else if (platform === 'linux') {
    try {
      await execFileAsync('systemctl', ['--user', 'disable', '--now', SYSTEMD_SERVICE]);
    } catch {
      // Not installed — ignore
    }
    try {
      await unlink(SYSTEMD_PATH);
      await execFileAsync('systemctl', ['--user', 'daemon-reload']);
    } catch {
      // Already removed — ignore
    }
    console.log('✓ systemd user service removed.');
  } else {
    console.log('当前操作系统不支持自动卸载守护进程。');
  }
}

export async function getDaemonStatus(): Promise<DaemonStatus> {
  const platform = getPlatform();

  if (platform === 'macos') {
    try {
      await access(PLIST_PATH);
    } catch {
      return 'not_installed';
    }
    try {
      const { stdout } = await execFileAsync('launchctl', ['list', PLIST_LABEL]);
      // launchctl list <label> returns plist-style "key" = value; format, not JSON
      // Check for PID field which is only present when the process is running
      const pidMatch = stdout.match(/"PID"\s*=\s*(\d+)/);
      return pidMatch ? 'running' : 'stopped';
    } catch {
      return 'stopped';
    }
  } else if (platform === 'linux') {
    try {
      await access(SYSTEMD_PATH);
    } catch {
      return 'not_installed';
    }
    try {
      const { stdout } = await execFileAsync('systemctl', [
        '--user',
        'is-active',
        SYSTEMD_SERVICE,
      ]);
      return stdout.trim() === 'active' ? 'running' : 'stopped';
    } catch {
      return 'stopped';
    }
  }

  return 'unsupported';
}
