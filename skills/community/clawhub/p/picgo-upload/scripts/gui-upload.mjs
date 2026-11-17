#!/usr/bin/env node
// gui-upload.mjs — upload files (or the clipboard image) through a running PicGo
// GUI app's local HTTP server and print a normalized JSON array of results.
//
// Why this exists: when the PicGo desktop app is running it exposes an upload
// server (default http://127.0.0.1:36677). Using it means zero install, zero
// login, and it reuses whatever image hosting the user already configured in the GUI.
// This script wraps the heartbeat probe + POST /upload + response normalization
// so the agent can get a hosted URL with a single command.
//
// Zero dependencies. Requires Node >= 22 (uses global fetch / FormData / Blob
// and process.loadEnvFile). No `npm install` needed.
//
// Usage:
//   node gui-upload.mjs <path1> [path2 ...]   Upload one or more local files.
//   node gui-upload.mjs --clipboard           Upload the current clipboard image.
//   node gui-upload.mjs --port 36678 <path>   Target a non-default port.
//   node gui-upload.mjs --secret <s> <path>   Provide the server auth secret.
//
// Output (stdout): a JSON array, one entry per uploaded item, shaped to match
// `picgo upload --format json` so callers can treat both paths identically:
//   [{ "imgUrl": "...", "fileName": "...", "type": "github", "size": 12345, ... }]
//
// Exit codes:
//   0  success — at least one item uploaded, JSON array on stdout
//   1  usage error (bad/missing arguments)
//   2  GUI server not reachable (caller should fall back to the picgo CLI)
//   3  auth required / failed (server has a secret; pass --secret)
//   4  upload failed (server reachable but the upload itself errored)

import { existsSync, statSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const DEFAULT_PORT = 36677
const DEFAULT_HOST = '127.0.0.1'
const HEARTBEAT_TIMEOUT_MS = 1500
const UPLOAD_TIMEOUT_MS = 120000

const EXIT = {
  OK: 0,
  USAGE: 1,
  NO_SERVER: 2,
  AUTH: 3,
  UPLOAD_FAILED: 4
}

function fail (code, message) {
  process.stderr.write(message.endsWith('\n') ? message : message + '\n')
  process.exit(code)
}

// --- Argument parsing -------------------------------------------------------

function parseArgs (argv) {
  const opts = {
    files: [],
    clipboard: false,
    port: DEFAULT_PORT,
    host: DEFAULT_HOST,
    secret: undefined
  }

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i]
    switch (arg) {
      case '--clipboard':
        opts.clipboard = true
        break
      case '--port':
        opts.port = Number(argv[++i])
        if (!Number.isInteger(opts.port) || opts.port <= 0) {
          fail(EXIT.USAGE, `Invalid --port value: ${argv[i]}`)
        }
        break
      case '--host':
        opts.host = argv[++i]
        if (!opts.host) fail(EXIT.USAGE, 'Missing value for --host')
        break
      case '--secret':
        opts.secret = argv[++i]
        if (opts.secret === undefined) fail(EXIT.USAGE, 'Missing value for --secret')
        break
      case '--help':
      case '-h':
        printHelpAndExit()
        break
      default:
        if (arg.startsWith('--')) {
          fail(EXIT.USAGE, `Unknown option: ${arg}`)
        }
        opts.files.push(arg)
    }
  }

  return opts
}

function printHelpAndExit () {
  process.stdout.write(
    'Usage:\n' +
    '  node gui-upload.mjs <path1> [path2 ...]   Upload local files\n' +
    '  node gui-upload.mjs --clipboard           Upload the clipboard image\n' +
    '  node gui-upload.mjs --port <n> <path>     Target a non-default port (default 36677)\n' +
    '  node gui-upload.mjs --secret <s> <path>   Provide the server auth secret\n'
  )
  process.exit(EXIT.OK)
}

// --- Secret resolution ------------------------------------------------------
// Priority: --secret flag > .env next to this script > PICGO_SERVER_SECRET env.

function resolveSecret (flagSecret) {
  if (flagSecret) return flagSecret

  const scriptDir = path.dirname(fileURLToPath(import.meta.url))
  const envPath = path.join(scriptDir, '.env')
  if (existsSync(envPath)) {
    try {
      // Node 22 builtin; loads KEY=VALUE pairs into process.env. Zero-dependency.
      process.loadEnvFile(envPath)
    } catch {
      // A malformed .env should not crash the upload — fall through to env var.
    }
  }

  const fromEnv = process.env.PICGO_SERVER_SECRET
  return fromEnv && fromEnv.trim() !== '' ? fromEnv.trim() : undefined
}

// --- HTTP helpers -----------------------------------------------------------

function baseUrl (opts) {
  return `http://${opts.host}:${opts.port}`
}

function authHeaders (secret) {
  return secret ? { Authorization: `Bearer ${secret}` } : {}
}

async function isServerAlive (opts) {
  try {
    const res = await fetch(`${baseUrl(opts)}/heartbeat`, {
      method: 'POST',
      signal: AbortSignal.timeout(HEARTBEAT_TIMEOUT_MS)
    })
    if (!res.ok) return false
    const data = await res.json().catch(() => null)
    return data?.success === true && data?.result === 'alive'
  } catch {
    return false
  }
}

// --- Response normalization -------------------------------------------------
// The GUI returns { success, result: [urls], items: [{imgUrl, ...}] }.
// `items` (newer GUI) already matches the CLI's JSON shape, so prefer it.
// Older GUIs only return `result` (a URL array) — build minimal items from it.

function normalizeResponse (data) {
  if (Array.isArray(data?.items) && data.items.length > 0) {
    return data.items
  }
  if (Array.isArray(data?.result)) {
    return data.result
      .filter((url) => typeof url === 'string' && url !== '')
      .map((imgUrl) => ({ imgUrl }))
  }
  return []
}

// --- Upload modes -----------------------------------------------------------

// Validate inputs up front (before any network I/O) so a bad path produces a
// precise "file does not exist" error instead of a misleading server probe.
function resolveInputPaths (files) {
  return files.map((file) => {
    const abs = path.resolve(file)
    if (!existsSync(abs)) {
      fail(EXIT.USAGE, `File does not exist: ${file}`)
    }
    if (!statSync(abs).isFile()) {
      fail(EXIT.USAGE, `Not a file: ${file}`)
    }
    return abs
  })
}

async function uploadPaths (opts, absPaths) {
  // The GUI's path-based upload reads files server-side from the given absolute
  // paths. This is the most faithful path (preserves original file metadata).
  return postUpload(opts, {
    headers: { 'Content-Type': 'application/json', ...authHeaders(opts.secret) },
    body: JSON.stringify({ list: absPaths })
  })
}

async function uploadClipboard (opts) {
  // Empty body => the GUI uploads the current clipboard image.
  return postUpload(opts, {
    headers: { ...authHeaders(opts.secret) },
    body: undefined
  })
}

async function postUpload (opts, init) {
  let res
  try {
    res = await fetch(`${baseUrl(opts)}/upload`, {
      method: 'POST',
      signal: AbortSignal.timeout(UPLOAD_TIMEOUT_MS),
      ...init
    })
  } catch (e) {
    fail(EXIT.NO_SERVER, `Failed to reach PicGo GUI server at ${baseUrl(opts)}: ${e.message}`)
  }

  if (res.status === 401) {
    fail(
      EXIT.AUTH,
      'PicGo GUI server requires authentication (401). The server has a secret set. ' +
      'Pass --secret <value>, put PICGO_SERVER_SECRET in a .env beside this script, ' +
      'or set the PICGO_SERVER_SECRET environment variable.'
    )
  }

  const data = await res.json().catch(() => null)

  if (!res.ok || !data || data.success !== true) {
    const message = data?.message || `HTTP ${res.status}`
    fail(EXIT.UPLOAD_FAILED, `Upload failed: ${message}`)
  }

  const items = normalizeResponse(data)
  if (items.length === 0) {
    fail(EXIT.UPLOAD_FAILED, 'Upload reported success but returned no URLs.')
  }
  return items
}

// --- Main -------------------------------------------------------------------

async function main () {
  const opts = parseArgs(process.argv.slice(2))

  if (opts.clipboard && opts.files.length > 0) {
    fail(EXIT.USAGE, 'Use either --clipboard or file paths, not both.')
  }
  if (!opts.clipboard && opts.files.length === 0) {
    fail(EXIT.USAGE, 'Nothing to upload. Provide file paths or --clipboard. Use --help for usage.')
  }

  // Validate local files before touching the network, so path errors are exact.
  const absPaths = opts.clipboard ? [] : resolveInputPaths(opts.files)

  opts.secret = resolveSecret(opts.secret)

  if (!(await isServerAlive(opts))) {
    fail(
      EXIT.NO_SERVER,
      `PicGo GUI server is not running at ${baseUrl(opts)}. ` +
      'Start the PicGo desktop app, or fall back to the picgo CLI.'
    )
  }

  const items = opts.clipboard ? await uploadClipboard(opts) : await uploadPaths(opts, absPaths)
  process.stdout.write(JSON.stringify(items) + '\n')
  process.exit(EXIT.OK)
}

main().catch((e) => {
  fail(EXIT.UPLOAD_FAILED, `Unexpected error: ${e?.stack || e?.message || String(e)}`)
})
