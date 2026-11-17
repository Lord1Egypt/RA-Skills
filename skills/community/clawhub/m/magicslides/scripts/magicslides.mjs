#!/usr/bin/env node
// MagicSlides CLI for agents. Zero dependencies, Node 18+.
// Calls the hosted MagicSlides MCP server over HTTP with your API key, so any agent
// that can run a shell command can make decks, docs, sheets and reels.
//
//   export MAGICSLIDES_API_KEY=ms-api-...   (get one: https://www.magicslides.app/dashboard/settings/api)
//   or: node magicslides.mjs login ms-api-...  (saves it to ~/.config/magicslides/api-key, for
//       agents like Codex whose sandbox strips *KEY* env vars from shell commands)
//   node magicslides.mjs tools                       # list tools + their arguments
//   node magicslides.mjs <tool> '<json args>'        # call a tool
//   node magicslides.mjs <tool> @args.json           # args from a file
//   echo '<json>' | node magicslides.mjs <tool> -    # args from stdin

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'

const ENDPOINT = process.env.MAGICSLIDES_MCP_URL || 'https://www.magicslides.app/api/mcp/mcp'
const REF = process.env.MAGICSLIDES_REF || 'agent-skill'

const KEY_FILE = join(process.env.XDG_CONFIG_HOME || join(homedir(), '.config'), 'magicslides', 'api-key')

const die = (msg, code = 1) => {
  process.stderr.write(msg.endsWith('\n') ? msg : msg + '\n')
  process.exit(code)
}

if (process.argv[2] === 'login') {
  const key = (process.argv[3] || '').trim()
  if (!key.startsWith('ms-api-')) die('Usage: magicslides.mjs login ms-api-...   (key from https://www.magicslides.app/dashboard/settings/api)')
  mkdirSync(join(KEY_FILE, '..'), { recursive: true })
  writeFileSync(KEY_FILE, key + '\n', { mode: 0o600 })
  console.log(`Saved to ${KEY_FILE}`)
  process.exit(0)
}

let KEY = (process.env.MAGICSLIDES_API_KEY || '').trim()
if (!KEY) {
  try {
    KEY = readFileSync(KEY_FILE, 'utf8').trim()
  } catch {
    /* no saved key */
  }
}

if (!KEY) {
  die(
    'MAGICSLIDES_API_KEY is not set.\n' +
      `Get a free key: https://www.magicslides.app/dashboard/settings/api?ref=${REF}\n` +
      'Then: export MAGICSLIDES_API_KEY=ms-api-...  or  node magicslides.mjs login ms-api-...'
  )
}

let rpcId = 0
async function rpc(method, params) {
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      accept: 'application/json, text/event-stream',
      'x-api-key': KEY,
      'user-agent': `magicslides-agent-skill/1.0 (${REF})`,
    },
    body: JSON.stringify({ jsonrpc: '2.0', id: ++rpcId, method, params }),
  })
  const text = await res.text()
  if (res.status === 401) die('MagicSlides rejected the API key (401). Create a new one at https://www.magicslides.app/dashboard/settings/api')
  if (!res.ok) die(`MagicSlides HTTP ${res.status}: ${text.slice(0, 500)}`)
  // Streamable HTTP answers either plain JSON or an SSE stream of `data:` lines.
  const payloads = text.trim().startsWith('{')
    ? [text]
    : text.split('\n').filter((l) => l.startsWith('data:')).map((l) => l.slice(5).trim())
  for (const p of payloads) {
    const msg = JSON.parse(p)
    if (msg.id !== rpcId) continue
    if (msg.error) die(`MagicSlides error: ${msg.error.message || JSON.stringify(msg.error)}`)
    return msg.result
  }
  die(`Unexpected response from MagicSlides: ${text.slice(0, 500)}`)
}

async function readArgs(raw) {
  if (raw === undefined) return {}
  if (raw === '-') {
    let s = ''
    for await (const chunk of process.stdin) s += chunk
    raw = s
  } else if (raw.startsWith('@')) {
    raw = readFileSync(raw.slice(1), 'utf8')
  }
  try {
    return JSON.parse(raw)
  } catch (e) {
    die(`Arguments must be JSON: ${e.message}`)
  }
}

const [cmd, rawArgs] = process.argv.slice(2)

if (!cmd || cmd === '-h' || cmd === '--help') {
  console.log(
    'Usage: magicslides.mjs tools | <tool> [\'{"json":"args"}\' | @file.json | -]\n' +
      'Common: whoami, list_templates, get_template_schema, create_presentation_from_slots,\n' +
      '        create_presentation, get_presentation, update_presentation, create_doc, create_sheet'
  )
  process.exit(0)
}

if (cmd === 'tools') {
  const { tools } = await rpc('tools/list', {})
  for (const t of tools) {
    const props = Object.keys(t.inputSchema?.properties || {})
    const req = new Set(t.inputSchema?.required || [])
    console.log(`${t.name}(${props.map((p) => (req.has(p) ? p : p + '?')).join(', ')})`)
    console.log(`  ${t.description.split('\n')[0]}`)
  }
  process.exit(0)
}

const result = await rpc('tools/call', { name: cmd, arguments: await readArgs(rawArgs) })
for (const c of result.content || []) {
  if (c.type === 'text') console.log(c.text)
}
// structuredContent carries the machine-readable fields (ids, URLs); print it last.
if (result.structuredContent) {
  const sc = { ...result.structuredContent }
  delete sc.picker // large widget payload for MCP Apps hosts, useless in a terminal
  console.log('\n--- structured ---\n' + JSON.stringify(sc, null, 2))
}
if (result.isError) process.exit(2)
