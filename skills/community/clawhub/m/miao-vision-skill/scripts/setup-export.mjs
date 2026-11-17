#!/usr/bin/env node
import { mkdirSync, mkdtempSync, renameSync, rmSync, writeFileSync } from 'node:fs'
import { spawn } from 'node:child_process'
import { homedir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { launchExportBrowser, playwrightVersion, resolvePlaywright } from './export-runtime.mjs'

async function execute(command, args, cwd, signal) {
  signal?.throwIfAborted()
  await new Promise((resolve, reject) => {
    const child = spawn(command, args, { cwd, stdio: ['ignore', 'inherit', 'inherit'], detached: process.platform !== 'win32' })
    let childError, forceKill
    const stop = () => {
      childError ??= new Error(signal?.aborted ? 'Export setup cancelled.' : 'Export setup timed out.')
      if (!child.pid) return
      if (process.platform === 'win32') {
        const killer = spawn('taskkill', ['/pid', String(child.pid), '/t', '/f'], { stdio: 'ignore' })
        killer.on('error', () => child.kill())
      } else {
        try { process.kill(-child.pid, 'SIGTERM') } catch { child.kill() }
        forceKill = setTimeout(() => { try { process.kill(-child.pid, 'SIGKILL') } catch {} }, 2000)
        forceKill.unref()
      }
    }
    const timeout = setTimeout(stop, 120_000); timeout.unref()
    signal?.addEventListener('abort', stop, { once: true })
    const cleanup = () => { clearTimeout(timeout); clearTimeout(forceKill); signal?.removeEventListener('abort', stop) }
    child.once('error', error => { childError = error; if (!child.pid) { cleanup(); reject(error) } })
    child.once('close', code => {
      cleanup()
      childError ? reject(childError) : code === 0 ? resolve() : reject(new Error(`Export setup command failed (${code}). Existing dependencies were preserved.`))
    })
  })
}

export async function setupExport(options = {}) {
  const statusOnly = !options.install
  if (statusOnly) {
    const { exportRuntimeStatus } = await import('./export-runtime.mjs')
    return exportRuntimeStatus(options)
  }
  options.signal?.throwIfAborted()
  const sharedRoot = resolve(options.home ?? homedir(), '.miao-vision/playwright')
  mkdirSync(dirname(sharedRoot), { recursive: true })
  const lock = `${sharedRoot}.lock`
  try { mkdirSync(lock) } catch (error) {
    if (error.code === 'EEXIST') throw new Error('Another export setup is running. Retry after it finishes; if interrupted, verify no installer is running before removing the lock.')
    throw error
  }
  let staging
  try {
    let runtime
    let installedShared = false
    try { runtime = resolvePlaywright(options) } catch (error) {
      if (error.result?.code !== 'EXPORT_PLAYWRIGHT_MISSING') throw error
      staging = mkdtempSync(join(dirname(sharedRoot), '.playwright-'))
      writeFileSync(join(staging, 'package.json'), JSON.stringify({ private: true, dependencies: { playwright: playwrightVersion } }))
      const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm'
      // Windows npm is launched by cmd with fixed arguments only.
      const args = ['install', '--ignore-scripts', '--no-audit', '--no-fund']
      if (process.platform === 'win32') await execute(process.env.ComSpec || 'cmd.exe', ['/d', '/s', '/c', npm, ...args], staging, options.signal)
      else await execute(npm, args, staging, options.signal)
      runtime = resolvePlaywright({ ...options, env: { MIAO_VIZ_PLAYWRIGHT_ROOT: staging }, cwd: staging, host: undefined, hostRoot: undefined })
    }
    const selected = { ...options, env: { MIAO_VIZ_PLAYWRIGHT_ROOT: runtime.root }, host: undefined, hostRoot: undefined }
    let browser
    try { browser = await launchExportBrowser(selected) } catch (error) {
      if (error.result?.code !== 'EXPORT_BROWSER_MISSING') throw error
      if (!runtime.cli) throw new Error('Selected Playwright has no browser installer.')
      await execute(process.execPath, [runtime.cli, 'install', 'chromium'], runtime.root, options.signal)
      browser = await launchExportBrowser(selected)
    }
    await browser.close()
    options.signal?.throwIfAborted()
    if (staging) {
      // Only replace an empty shared installation; keep any existing directory intact.
      let backup
      try { backup = `${sharedRoot}.previous-${Date.now()}`; renameSync(sharedRoot, backup) } catch (error) { if (error.code !== 'ENOENT') throw error; backup = undefined }
      try { renameSync(staging, sharedRoot); staging = undefined } catch (error) { if (backup) renameSync(backup, sharedRoot); throw error }
      installedShared = true
      runtime = resolvePlaywright({ ...options, env: { MIAO_VIZ_PLAYWRIGHT_ROOT: sharedRoot }, host: undefined, hostRoot: undefined })
    }
    return { ok: true, source: installedShared ? 'shared' : runtime.source, root: runtime.root, version: runtime.version, browser: 'ready' }
  } finally { if (staging) rmSync(staging, { recursive: true, force: true }); rmSync(lock, { recursive: true, force: true }) }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const hostIndex = process.argv.indexOf('--host')
  const rootIndex = process.argv.indexOf('--host-root')
  setupExport({ install: process.argv.includes('--install'), host: process.argv[hostIndex + 1] && hostIndex >= 0 ? process.argv[hostIndex + 1] : undefined,
    hostRoot: rootIndex >= 0 ? process.argv[rootIndex + 1] : undefined, home: homedir() })
    .then(result => { console.log(JSON.stringify(result)); if (!result.ok) process.exitCode = 1 })
    .catch(error => { console.error(JSON.stringify(error.result ?? { ok: false, code: 'EXPORT_SETUP_FAILED', message: error.message })); process.exitCode = 1 })
}
