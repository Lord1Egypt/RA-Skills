import { existsSync, readFileSync, realpathSync } from 'node:fs'
import { createRequire } from 'node:module'
import { homedir } from 'node:os'
import { dirname, join, resolve, sep } from 'node:path'

export const playwrightVersion = '1.57.0'
export class ExportRuntimeError extends Error {
  constructor(code, message, details = {}) {
    super(message)
    this.result = { ok: false, code, message, nextActions: [{ label: code === 'EXPORT_MODULE_LOAD_FAILED' ? 'Repair the reported installed host module; it was not replaced automatically.' : 'Run /miao-viewer setup in Pi, or the bundled setup-export.mjs after approval.', safeToRetry: true }], ...details }
  }
}

export function exportRoots({ env = process.env, cwd = process.cwd(), home = homedir(), host, hostRoot } = {}) {
  const roots = []
  const add = (root, source) => { if (root && !roots.some(item => item.root === resolve(root))) roots.push({ root: resolve(root), source }) }
  const explicitRoot = hostRoot || env.MIAO_VIZ_PLAYWRIGHT_ROOT
  add(explicitRoot, explicitRoot && resolve(explicitRoot) === resolve(home, '.miao-vision/playwright') ? 'shared' : 'host')
  if (host === 'claude-code') {
    add(join(cwd, '.claude'), 'host')
    add(join(home, '.claude'), 'host')
  }
  add(join(home, '.miao-vision/playwright'), 'shared')
  add(cwd, 'workspace')
  return roots
}

export function resolvePlaywright(options = {}) {
  for (const candidate of exportRoots(options)) {
    const require = createRequire(join(candidate.root, 'package.json'))
    for (const name of ['playwright', 'playwright-core', '@playwright/test']) {
      let entry
      try {
        entry = require.resolve(name)
        const canonicalRoot = existsSync(candidate.root) ? realpathSync(candidate.root) : candidate.root
        const nested = canonicalRoot.lastIndexOf(`${sep}node_modules${sep}`)
        const boundary = nested >= 0 ? canonicalRoot.slice(0, nested + `${sep}node_modules`.length) : join(canonicalRoot, 'node_modules')
        const moduleBoundary = existsSync(boundary) ? realpathSync(boundary) : boundary
        if (!entry.startsWith(moduleBoundary + sep)) continue
      } catch (error) {
        if (error.code === 'MODULE_NOT_FOUND') {
          let installed = false
          try { installed = Boolean(require.resolve(`${name}/package.json`)) } catch {}
          if (!installed) continue
        }
        throw new ExportRuntimeError('EXPORT_MODULE_LOAD_FAILED', `Cannot resolve ${name}.`, { source: candidate.source, root: candidate.root, detail: error.message })
      }
      try {
        const module = require(entry)
        if (!module.chromium?.launch) throw new Error('Chromium API is unavailable.')
        const manifestPath = require.resolve(`${name}/package.json`)
        const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'))
        const packageRoot = dirname(manifestPath)
        return { ...candidate, module, name, version: manifest.version, entry, cli: join(packageRoot, 'cli.js') }
      } catch (error) {
        throw new ExportRuntimeError('EXPORT_MODULE_LOAD_FAILED', `Installed ${name} could not be loaded.`, { source: candidate.source, root: candidate.root, detail: error.message })
      }
    }
  }
  throw new ExportRuntimeError('EXPORT_PLAYWRIGHT_MISSING', 'Playwright is not installed in the host, shared directory, or workspace.', {
    nextActions: [{ label: 'In Pi run /miao-viewer setup; otherwise run the bundled setup-export.mjs after approval.', safeToRetry: true }]
  })
}

export function exportRuntimeStatus(options = {}) {
  try {
    const runtime = resolvePlaywright(options)
    const browserPath = runtime.module.chromium.executablePath()
    const ready = existsSync(browserPath)
    return { ok: ready, source: runtime.source, root: runtime.root, version: runtime.version, browserPath,
      ...(!ready ? { code: 'EXPORT_BROWSER_MISSING', message: 'Matching Chromium is missing. Run export setup after approval.' } : {}) }
  } catch (error) { return error.result ?? { ok: false, code: 'EXPORT_MODULE_LOAD_FAILED', message: error.message } }
}

export async function launchExportBrowser(options = {}) {
  const runtime = resolvePlaywright(options)
  try { return await runtime.module.chromium.launch({ timeout: 30_000 }) }
  catch (error) {
    const missing = /Executable doesn't exist|executable.*not.*exist/i.test(error.message)
    throw new ExportRuntimeError(missing ? 'EXPORT_BROWSER_MISSING' : 'EXPORT_BROWSER_LAUNCH_FAILED',
      missing ? 'Matching Chromium is missing. Run export setup after approval.' : 'Chromium could not be launched.',
      { source: runtime.source, root: runtime.root, version: runtime.version, detail: error.message,
        nextActions: [{ label: missing ? 'Run /miao-viewer setup, or the bundled setup-export.mjs.' : 'Check browser permissions and operating system dependencies.', safeToRetry: true }] })
  }
}
