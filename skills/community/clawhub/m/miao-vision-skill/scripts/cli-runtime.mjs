import { accessSync, constants, existsSync, readFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const scriptDir = dirname(fileURLToPath(import.meta.url))
export const skillRoot = resolve(scriptDir, '..')
export const compatibilityPath = resolve(skillRoot, 'cli-compatibility.json')

export function readCompatibility(path = compatibilityPath) {
  return JSON.parse(readFileSync(path, 'utf8'))
}

export function executableName(platform = process.platform) {
  return platform === 'win32' ? 'miao-viz.exe' : 'miao-viz'
}

export function defaultMiaoVisionHome(env = process.env, home = homedir()) {
  return env.MIAO_VISION_HOME ? resolve(env.MIAO_VISION_HOME) : resolve(home, '.miao-vision')
}

export function cliCandidates({ env = process.env, platform = process.platform } = {}) {
  const key = Object.keys(env).find(key => key.toLowerCase() === 'path')
  const paths = (env[key] ?? '').split(platform === 'win32' ? ';' : ':').filter(Boolean)
  const names = platform === 'win32' ? ['miao-viz.exe', 'miao-viz.cmd', 'miao-viz.bat'] : ['miao-viz']
  for (const directory of paths) {
    for (const name of names) {
      const candidate = resolve(directory, name)
      try {
        accessSync(candidate, platform === 'win32' ? constants.F_OK : constants.X_OK)
        return [candidate]
      } catch {}
    }
  }
  return []
}

// Resolve npm's Windows shim to its JS entry without spawning a shell.
export function cliInvocation(executable, args = [], platform = process.platform) {
  if (platform === 'win32' && /\.(cmd|bat)$/i.test(executable)) {
    const entry = resolve(dirname(executable), 'node_modules/@miao-vision/cli/dist/cli.cjs')
    if (!existsSync(entry)) throw new Error('Global npm miao-viz entry was not found. Reinstall @miao-vision/cli.')
    return { command: process.execPath, args: [entry, ...args] }
  }
  return { command: executable, args }
}

export function parseVersion(value) {
  const match = String(value).trim().match(/^v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?$/)
  return match ? match.slice(1).map(Number) : null
}

export function compareVersions(left, right) {
  const a = parseVersion(left)
  const b = parseVersion(right)
  if (!a || !b) return null
  for (let index = 0; index < 3; index += 1) {
    if (a[index] !== b[index]) return a[index] < b[index] ? -1 : 1
  }
  return 0
}

export function isCompatibleVersion(version, compatibility) {
  const minimum = compareVersions(version, compatibility.minimumCliVersion)
  const maximum = compareVersions(version, compatibility.maximumCliVersionExclusive)
  return minimum !== null && maximum !== null && minimum >= 0 && maximum < 0
}

export function isRecommendedVersion(version, compatibility) {
  return compareVersions(version, compatibility.recommendedCliVersion) === 0
}

export function selectPreferredCandidate(candidates, compatibility) {
  return candidates.find((candidate) => isRecommendedVersion(candidate.version, compatibility)) ?? candidates[0]
}

export function existingCandidates(options) {
  return cliCandidates(options)
}
