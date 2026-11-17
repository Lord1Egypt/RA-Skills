const { execFile, spawn } = require('child_process');
const os = require('os');
const fs = require('fs');
const { promisify } = require('util');
const execFilePromise = promisify(execFile);

const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i++) {
  if (!args[i].startsWith('--')) continue;
  params[args[i].slice(2)] = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
}
const { action, value, app } = params;
const ALLOWED_APPS = new Set(['firefox','chrome','google-chrome','chromium','edge','microsoft-edge','code','vlc','spotify','calculator','gnome-calculator','notepad','gedit','nautilus','files','terminal','gnome-terminal']);
let platform = os.platform();
let isWsl = false;
let powershellPath = 'powershell.exe'; let cmdPath = 'cmd.exe'; let taskkillPath = 'taskkill.exe';
if (platform === 'linux') {
  try { const release = fs.readFileSync('/proc/version', 'utf8').toLowerCase(); if (release.includes('microsoft') || release.includes('wsl')) { isWsl = true; platform = 'wsl'; powershellPath = '/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'; cmdPath = '/mnt/c/Windows/System32/cmd.exe'; taskkillPath = '/mnt/c/Windows/System32/taskkill.exe'; } } catch {}
}

function numberInRange(raw, min, max, name) {
  if (!/^-?\d+(?:\.\d+)?$/.test(String(raw))) throw new Error(`${name} must be a number`);
  const n = Number(raw); if (!Number.isFinite(n) || n < min || n > max) throw new Error(`${name} must be between ${min} and ${max}`); return n;
}
function appName(raw) {
  if (typeof raw !== 'string' || !raw.trim() || raw.length > 128 || !/^[a-zA-Z0-9 _\-.]+$/.test(raw.trim())) throw new Error('app must be a simple executable name (letters, numbers, spaces, dots, dashes, underscores)');
  const base = raw.trim().split(/[\\/]/).pop();
  const normalized = base.replace(/\.exe$/i, '').toLowerCase();
  if (!ALLOWED_APPS.has(normalized)) throw new Error(`app is not in the safe allowlist: ${[...ALLOWED_APPS].join(', ')}`);
  return base.replace(/\.exe$/i, '');
}
function executable(name) { return process.platform === 'win32' ? `${name}.exe` : name; }
async function setVolume(raw) {
  const v = numberInRange(raw, 0, 100, 'volume');
  if (platform === 'linux') { try { await execFilePromise('pactl', ['set-sink-volume', '@DEFAULT_SINK@', `${v}%`]); } catch { await execFilePromise('amixer', ['sset', 'Master', `${v}%`]); } }
  else if (platform === 'darwin') await execFilePromise('osascript', ['-e', `set volume output volume ${v}`]);
  else if (platform === 'win32' || platform === 'wsl') await execFilePromise(isWsl ? cmdPath : 'nircmd.exe', isWsl ? ['/c', 'nircmd.exe', 'setsysvolume', String(Math.floor(65535 * v / 100))] : ['setsysvolume', String(Math.floor(65535 * v / 100))]);
  else throw new Error(`Unsupported platform: ${platform}`);
}
async function changeVolume(raw) {
  const d = numberInRange(raw, -100, 100, 'delta'); let current = 50;
  if (platform === 'linux') { try { const r = await execFilePromise('pactl', ['get-sink-volume', '@DEFAULT_SINK@']); current = Number(r.stdout.match(/(\d+)%/)?.[1] || 50); } catch { try { const r = await execFilePromise('amixer', ['get', 'Master']); current = Number(r.stdout.match(/(\d+)%/)?.[1] || 50); } catch {} } }
  else if (platform === 'darwin') { const r = await execFilePromise('osascript', ['-e', 'output volume of (get volume settings)']); current = Number.parseInt(r.stdout, 10) || 50; }
  const next = Math.max(0, Math.min(100, current + d)); await setVolume(next); console.log(`Volume changed from ${current}% to ${next}%`);
}
async function setBrightness(raw) {
  const v = numberInRange(raw, 0, 100, 'brightness');
  if (platform === 'linux' && !isWsl) await execFilePromise('brightnessctl', ['set', `${v}%`]);
  else if (platform === 'win32' || platform === 'wsl') { const ps = `(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, ${v})`; await execFilePromise(isWsl ? powershellPath : 'powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', ps]); }
  else throw new Error('Brightness control is unavailable on this platform without a supported utility');
}
async function openApp(raw) {
  const name = appName(raw); const exe = executable(name);
  if (platform === 'linux') { const child = spawn(exe, [], {detached: true, stdio: 'ignore'}); child.unref(); }
  else if (platform === 'darwin') await execFilePromise('open', ['-a', name]);
  else if (platform === 'win32') await execFilePromise('cmd.exe', ['/c', 'start', '', exe]);
  else if (platform === 'wsl') await execFilePromise(cmdPath, ['/c', 'start', '', exe]);
  else throw new Error(`Unsupported platform: ${platform}`);
}
async function closeApp(raw) {
  const name = appName(raw); const exe = executable(name);
  if (platform === 'linux' || platform === 'darwin') await execFilePromise('pkill', ['-x', name]);
  else if (platform === 'win32') await execFilePromise('taskkill.exe', ['/IM', exe, '/F']);
  else if (platform === 'wsl') await execFilePromise(taskkillPath, ['/IM', exe, '/F']);
  else throw new Error(`Unsupported platform: ${platform}`);
}

(async () => {
  try {
    if (!['set_volume','change_volume','set_brightness','open_app','close_app'].includes(action)) throw new Error('unknown or missing action');
    if (action === 'set_volume') await setVolume(value);
    if (action === 'change_volume') await changeVolume(value);
    if (action === 'set_brightness') await setBrightness(value);
    if (action === 'open_app') await openApp(app);
    if (action === 'close_app') await closeApp(app);
    console.log(`Action ${action} completed successfully.`);
  } catch (e) { console.error(`Error executing ${action || 'request'}: ${e.message}`); process.exitCode = 1; }
})();
