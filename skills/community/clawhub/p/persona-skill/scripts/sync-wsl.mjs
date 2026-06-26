import { execSync } from 'child_process';
import os from 'os';

const isWSL = os.release().toLowerCase().includes('microsoft');
const isWindows = os.platform() === 'win32';
const targetDir = '~/.openclaw/workspace/skills/persona-skill';

let cmd = '';

if (isWSL || !isWindows) {
    console.log(`📡 Detected Native/WSL environment. Syncing to ${targetDir}...`);
    cmd = `mkdir -p ${targetDir} && rsync -av --exclude 'node_modules' --exclude '.git' ./ ${targetDir}/`;
} else if (isWindows) {
    console.log(`📡 Detected Windows environment. Calling WSL rsync to sync to ${targetDir}...`);
    try {
        const cwd = process.cwd().replace(/\\/g, '/');
        // Retrieve the accurate WSL path of the current Windows directory
        const wslPathStr = execSync(`wsl wslpath -u "${cwd}"`).toString().trim();
        cmd = `wsl bash -c "mkdir -p ${targetDir} && rsync -av --exclude 'node_modules' --exclude '.git' ${wslPathStr}/ ${targetDir}/"`;
    } catch (e) {
        console.error('❌ Failed to construct WSL command. Are you sure WSL is installed and running?');
        process.exit(1);
    }
}

try {
    execSync(cmd, { stdio: 'inherit' });
    console.log('✅ Successfully synced persona-skill files to your local OpenClaw workspace!');
} catch (e) {
    console.error('❌ Sync failed:', e.message);
    process.exit(1);
}
