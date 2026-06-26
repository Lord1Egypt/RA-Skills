import os from 'node:os';

export function detectOS() {
  const platform = os.platform();
  if (platform === 'win32') return 'windows';
  if (platform === 'darwin') return 'macos';
  if (platform === 'linux') return 'linux';
  return 'unknown';
}

export function getOSLabel(osType = detectOS()) {
  const labels = {
    windows: 'Windows',
    macos: 'macOS',
    linux: 'Linux',
    unknown: os.platform(),
  };
  return labels[osType] || osType;
}

export function getHomeDir() {
  return os.homedir();
}

export function formatDisplayPath(absolutePath, osType = detectOS()) {
  const home = getHomeDir();
  if (!absolutePath.startsWith(home)) {
    return absolutePath;
  }

  const relative = absolutePath.slice(home.length).replace(/\\/g, '/');
  if (osType === 'windows') {
    return `%USERPROFILE%${relative.replace(/\//g, '\\')}`;
  }
  return `~${relative}`;
}
