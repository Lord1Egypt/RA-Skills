#!/usr/bin/env node
/**
 * open-url.js — 用系统默认浏览器打开指定 URL
 *
 * 用法：
 *   node api/browser/open-url.js <url>
 *
 * 退出码：
 *   0 — 成功
 *   1 — 失败
 */

const { exec } = require('child_process')
const { promisify } = require('util')
const execAsync = promisify(exec)

async function openUrl(url) {
  if (!url) {
    console.error('❌ URL is required')
    process.exit(1)
  }

  try {
    if (process.platform === 'darwin') {
      await execAsync(`open "${url}"`)
    } else if (process.platform === 'win32') {
      await execAsync(`start "" "${url}"`)
    } else {
      await execAsync(`xdg-open "${url}"`)
    }
    console.log(`✅ Opened: ${url}`)
    process.exit(0)
  } catch (err) {
    console.error(`❌ Failed to open: ${err.message}`)
    process.exit(1)
  }
}

// CLI 调用
if (require.main === module) {
  openUrl(process.argv[2])
}

module.exports = { openUrl }
