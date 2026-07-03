#!/usr/bin/env node
/**
 * open-url.js — 用系统默认浏览器打开指定 URL
 *
 * 域名白名单：只允许 BeautsGO 平台域名
 *
 * 用法：
 *   node api/browser/open-url.js <url>
 */

const { exec } = require('child_process')
const { promisify } = require('util')
const execAsync = promisify(exec)

/** 允许打开的域名白名单 */
const ALLOWED_HOSTS = ['i.beautsgo.com']

function isAllowedUrl(url) {
  try {
    const { hostname, protocol } = new URL(url)
    if (protocol !== 'https:') return false
    return ALLOWED_HOSTS.some(host => hostname === host || hostname.endsWith('.' + host))
  } catch {
    return false
  }
}

async function openUrl(url) {
  if (!url) throw new Error('URL is required')
  if (!isAllowedUrl(url)) throw new Error(`URL not allowed: ${url}`)

  if (process.platform === 'darwin') {
    await execAsync(`open "${url}"`)
  } else if (process.platform === 'win32') {
    await execAsync(`start "" "${url}"`)
  } else {
    await execAsync(`xdg-open "${url}"`)
  }
}

if (require.main === module) {
  openUrl(process.argv[2])
    .then(() => { console.log(`✅ Opened: ${process.argv[2]}`); process.exit(0) })
    .catch(err => { console.error(`❌ ${err.message}`); process.exit(1) })
}

module.exports = { openUrl }
