import assert from 'node:assert/strict'
import { spawn } from 'node:child_process'
import { once } from 'node:events'
import { mkdtempSync, readFileSync, writeFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { basename, dirname, join, resolve } from 'node:path'
import { createInterface } from 'node:readline'
import { test } from 'node:test'
import { agentCapabilities, agentCapabilitiesTool, longFormGuidanceTool, longFormWritingGuidance, mountWritingPlugin, resolveServerConfig, writingGuidance } from '../adapter.js'

test('mounts MCP before registering scoped literal generation guidance', async () => {
  const sections = [], events = []
  const ctx = { tools: { register: () => events.push('tool') }, systemPrompt: { section: value => { sections.push(value); events.push('section') } } }
  await mountWritingPlugin(ctx, {serverName: 'custom-writing'}, async (_ctx, config) => {
    assert.equal(config.serverName, 'custom-writing')
    assert.equal(config.failOnStartupError, true)
    events.push('ready')
  })
  assert.deepEqual(events, ['ready', 'tool', 'tool', 'section'])
  assert.equal(sections[0].interpolate, false)
  assert.match(sections[0].text, /mcp__custom-writing__compile_generation_prompt/)
  assert.match(sections[0].text, /not code or ordinary answers/)
})

test('delegation discovery respects caller scope, custom names, and reloads without starting agents', async () => {
  const agent = {id: 'restricted-child'}, definitions = []
  let visible = false
  const parameters = {type: 'object', properties: {prompt: {type: 'string'}}}
  const ctx = {tools: {
    get(name, scope) {
      assert.equal(name, 'delegate_writer')
      assert.equal(scope, agent)
      return visible ? {parameters} : undefined
    },
    register(definition) { definitions.push(definition) },
  }}
  await mountWritingPlugin(ctx, {generationGuidance: false, delegationToolName: 'delegate_writer'}, async () => {})
  const tool = definitions.find(item => item.name === agentCapabilitiesTool('human-writing'))
  assert.equal((await tool.execute({}, {agent})).available, false)
  visible = true
  const discovered = await tool.execute({}, {agent})
  assert.equal(discovered.available, true)
  assert.equal(discovered.runtime_verified, false)
  assert.deepEqual(discovered.parameters, parameters)
  visible = false
  assert.equal(agentCapabilities(ctx, 'delegate_writer', agent).mode, 'sequential-role-passes')
  assert.throws(() => resolveServerConfig({delegationToolName: 'bad tool name'}), /delegationToolName/)
})

test('disabled generation guidance retains tools, failed startup contributes no section', async () => {
  let mounted = false
  await mountWritingPlugin({tools: {register() {}}}, {generationGuidance: false}, async () => { mounted = true })
  assert.equal(mounted, true)
  let registered = false
  await assert.rejects(mountWritingPlugin({systemPrompt: {section: () => {registered = true}}}, {}, async () => {
    throw new Error('startup failed')
  }), /startup failed/)
  assert.equal(registered, false)
  assert.throws(() => resolveServerConfig({serverName: 'bad name'}), /serverName/)
  assert.throws(() => resolveServerConfig({toolCallTimeoutMs: -1}), /toolCallTimeoutMs/)
})

test('long-form protocol is on demand, namespaced, and honest about delegation', () => {
  const prompt = writingGuidance('custom-writing')
  assert.match(prompt, />=10,000 characters or words/)
  assert.match(prompt, /explicit multi-agent long-form writing/)
  assert.match(prompt, /requested output, not input length/)
  assert.ok(prompt.includes(longFormGuidanceTool('custom-writing')))
  assert.doesNotMatch(prompt, /Map that child ID/)
  const protocol = longFormWritingGuidance('custom-writing')
  for (const name of ['plan_long_form_writing', 'list_writing_tasks', 'claim_writing_task',
    'submit_writing_result', 'verify_writing_project', 'assemble_writing_project']) {
    assert.ok(protocol.includes(`mcp__custom-writing__${name}`))
    assert.ok(!protocol.includes(`mcp__human-writing__${name}`))
  }
  assert.match(protocol, /forward both\nunchanged/)
  assert.match(protocol, /result: object, agent_id/)
  assert.match(protocol, /child ID, NOT completed prose/)
  assert.match(protocol, /not independent agents/)
  assert.match(protocol, /ONLY in execution_mode='contract'/)
  assert.match(protocol, /predecessor is approved/)
  assert.match(protocol, /bounded revisions/)
  assert.match(protocol, /content \(complete role-specific prompt\) and result_schema/)
  assert.match(protocol, /final reviewer must differ from all chunk writers/)
  assert.match(protocol, /12 writing jobs plus their review jobs, not 12 guaranteed concurrent agents/)
  assert.match(protocol, /full content, result_schema, and claim_token unchanged/)
  assert.match(protocol, /result\.claim_token must copy the current claim_token/)
  assert.match(protocol, /Reject stale child results from an earlier attempt; never relabel them with a new token/)
})

test('bundled Python server negotiates, compiles genres, verifies facts, and blocks escapes', {timeout: 20000}, async () => {
  const root = mkdtempSync(join(tmpdir(), 'human-writing-dsh-'))
  writeFileSync(join(root, 'humanwriting.py'), 'raise RuntimeError("workspace shadowed runtime")')
  writeFileSync(join(root, 'sources.md'), 'Observed test: the device lasted six hours.', 'utf8')
  assert.throws(() => resolveServerConfig({root: join(root, 'sources.md')}), /must be a directory/)
  const config = resolveServerConfig({root})
  const child = spawn(config.command, config.args, {cwd: config.cwd, stdio: ['pipe', 'pipe', 'pipe']})
  const responses = new Map()
  let stderr = ''
  child.stderr.on('data', data => {stderr += data})
  const lines = createInterface({input: child.stdout})
  lines.on('line', line => {
    const value = JSON.parse(line)
    const pending = responses.get(value.id)
    if (pending) {responses.delete(value.id); pending.resolve(value)}
  })
  child.on('error', error => { for (const pending of responses.values()) pending.reject(error) })
  child.on('exit', code => { for (const pending of responses.values()) pending.reject(new Error(`Server exited ${code}: ${stderr}`)) })
  let id = 0
  const request = (method, params = {}) => new Promise((resolve, reject) => {
    responses.set(++id, {resolve, reject})
    child.stdin.write(JSON.stringify({jsonrpc: '2.0', id, method, params}) + '\n')
  })
  const call = (name, args) => request('tools/call', {name, arguments: args})
  try {
    const initialized = await request('initialize', {protocolVersion: '2025-03-26', capabilities: {}, clientInfo: {name: 'dsh-test', version: '1'}})
    const runtimeVersion = readFileSync(new URL('../../../humanwriting/__init__.py', import.meta.url), 'utf8')
      .match(/__version__\s*=\s*"([^"]+)"/)[1]
    assert.equal(initialized.result.serverInfo.version, runtimeVersion)
    const listed = await request('tools/list')
    assert.ok(listed.result.tools.some(tool => tool.name === 'compile_generation_prompt'))
    for (const style of ['fiction', 'academic-paper', 'formal-document']) {
      const compiled = await call('compile_generation_prompt', {style, task: 'Write the requested passage.'})
      assert.equal(compiled.result.isError, undefined)
      assert.match(compiled.result.content[0].text, /generation-quality/)
    }
    const report = await call('compile_generation_prompt', {style: 'self-media', task: 'Explain the test.', source_paths: ['sources.md']})
    assert.match(report.result.content[0].text, /device lasted six hours/)
    const escaped = await call('compile_generation_prompt', {style: 'self-media', task: 'Write.', source_paths: ['../outside.md']})
    assert.equal(escaped.result.isError, true)
    const fidelity = await call('verify_fidelity', {source_text: 'The effect may be 20%.', candidate_text: 'The effect is 20%.'})
    assert.equal(JSON.parse(fidelity.result.content[0].text).status, 'needs-review')
  } finally {
    const closed = once(child, 'close')
    child.stdin.end()
    child.kill()
    await closed
    lines.close()
    assert.equal(dirname(resolve(root)), resolve(tmpdir()))
    assert.ok(basename(root).startsWith('human-writing-dsh-'))
    rmSync(root, {recursive: true, force: true})
  }
})
