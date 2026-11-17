import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { test } from 'node:test'
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { basename, dirname, join, resolve } from 'node:path'
import { Context } from '@deepseek-ai/cordis'
import SystemPrompt, { renderPrompt } from '@deepseek-ai/dsh-system-prompt'
import ToolRuntime from '@deepseek-ai/dsh-tools'
import * as WritingPlugin from '../index.js'
import { agentCapabilitiesTool, longFormGuidanceTool } from '../adapter.js'

test('official Cordis + MCP mounts, assembles writing guidance, calls tools, and unloads', {timeout: 20000}, async () => {
  const ctx = new Context()
  try {
    await ctx.plugin(SystemPrompt)
    await ctx.plugin(ToolRuntime)
    const plugin = ctx.plugin(WritingPlugin, {serverName: 'writing-integration'})
    await plugin
    const name = 'mcp__writing-integration__compile_generation_prompt'
    const guidanceName = longFormGuidanceTool('writing-integration')
    assert.ok(ctx.tools.get(name), 'MCP tool is discovered through the official client')
    const capabilitiesName = agentCapabilitiesTool('writing-integration')
    const capabilities = await ctx.tools.execute({signal: new AbortController().signal,
      callId: 'capabilities-test', name: capabilitiesName, arguments: {}})
    assert.equal(capabilities.isError, false)
    assert.equal(JSON.parse(capabilities.content[0].text).available, false)
    const prompt = renderPrompt(await ctx.systemPrompt.assemble({}))
    assert.match(prompt, /Human Writing for DSH/)
    assert.ok(prompt.includes(guidanceName))
    assert.doesNotMatch(prompt, /Map that child ID/)
    const guidance = await ctx.tools.execute({
      signal: new AbortController().signal, callId: 'writing-guidance', name: guidanceName, arguments: {},
    })
    assert.equal(guidance.isError, false)
    assert.match(guidance.content[0].text, /subagent with description and prompt/)
    assert.match(guidance.content[0].text, /not independent agents/)
    assert.match(guidance.content[0].text, /result_schema, and claim_token unchanged/)
    assert.match(guidance.content[0].text, /Reject stale child results/)
    for (const tool of ['plan_long_form_writing', 'list_writing_tasks', 'claim_writing_task',
      'submit_writing_result', 'verify_writing_project', 'assemble_writing_project']) {
      assert.ok(ctx.tools.get(`mcp__writing-integration__${tool}`), `real MCP exposes ${tool}`)
    }
    const planning = ctx.tools.get('mcp__writing-integration__plan_long_form_writing')
    assert.deepEqual(planning.parameters.properties.length_unit.enum, ['characters', 'words'])
    assert.deepEqual(planning.parameters.properties.execution_mode.enum, ['sequential', 'contract'])
    const submission = ctx.tools.get('mcp__writing-integration__submit_writing_result')
    assert.equal(submission.parameters.properties.result.type, 'object')
    assert.ok(submission.parameters.required.includes('agent_id'))
    const result = await ctx.tools.execute({
      signal: new AbortController().signal, callId: 'writing-test-1', name,
      arguments: {style: 'academic-paper', task: 'Describe the supplied results without inventing citations.'},
    })
    assert.equal(result.isError, false)
    assert.match(result.content[0].text, /generation-quality/)
    await plugin.dispose()
    assert.equal(ctx.tools.get(name), undefined)
    assert.equal(ctx.tools.get(guidanceName), undefined)
    assert.equal(ctx.tools.get(capabilitiesName), undefined)
    assert.doesNotMatch(renderPrompt(await ctx.systemPrompt.assemble({})), /Human Writing for DSH/)
  } finally {
    await ctx.fiber.dispose()
  }
})

test('tools-only mode retains on-demand guidance without a prompt section', {timeout: 20000}, async () => {
  const ctx = new Context()
  try {
    await ctx.plugin(SystemPrompt)
    await ctx.plugin(ToolRuntime)
    const plugin = ctx.plugin(WritingPlugin, {serverName: 'tools-only', generationGuidance: false})
    await plugin
    assert.ok(ctx.tools.get(longFormGuidanceTool('tools-only')))
    assert.doesNotMatch(renderPrompt(await ctx.systemPrompt.assemble({})), /Human Writing for DSH/)
    await plugin.dispose()
    assert.equal(ctx.tools.get(longFormGuidanceTool('tools-only')), undefined)
  } finally {
    await ctx.fiber.dispose()
  }
})

test('real Cordis/MCP plans, claims, submits, and enforces writing approval gates', {timeout: 20000}, async () => {
  const root = mkdtempSync(join(tmpdir(), 'writing-cordis-'))
  writeFileSync(join(root, 'outline.md'), 'A courier arrives.', 'utf8')
  const ctx = new Context()
  let callId = 0
  const call = (name, args) => ctx.tools.execute({
    signal: new AbortController().signal, callId: `workflow-${++callId}`,
    name: `mcp__writing-workflow__${name}`, arguments: args,
  })
  const value = result => {
    assert.equal(result.isError, false, JSON.stringify(result.content))
    return JSON.parse(result.content[0].text)
  }
  try {
    await ctx.plugin(SystemPrompt)
    await ctx.plugin(ToolRuntime)
    await ctx.plugin(WritingPlugin, {root, serverName: 'writing-workflow'})
    const plan = value(await call('plan_long_form_writing', {
      outline_path: 'outline.md', output_dir: 'project', style: 'fiction',
      target_length: 10000, chunk_size: 5000, length_unit: 'words', execution_mode: 'sequential',
    }))
    assert.equal(plan.length_unit, 'words')
    assert.equal(plan.chunk_count, 2)
    const packageArgs = {package_dir: 'project'}
    const listed = value(await call('list_writing_tasks', packageArgs))
    assert.deepEqual(listed.tasks.filter(task => task.ready).map(task => task.task_id), ['outline-check'])
    const blocked = await call('claim_writing_task', {...packageArgs, task_id: 'chunk-plan', agent_id: 'planner-pass'})
    assert.equal(blocked.isError, true)
    const identity = {...packageArgs, task_id: 'outline-check', agent_id: 'outline-pass'}
    const claim = value(await call('claim_writing_task', identity))
    assert.equal(claim.agent_id, identity.agent_id)
    assert.match(claim.content, /A courier arrives/)
    assert.ok(claim.result_schema)
    assert.equal(typeof claim.claim_token, 'string')
    assert.ok(claim.claim_token.length > 0)
    assert.equal(claim.result_schema.claim_token, claim.claim_token)
    const resumed = value(await call('claim_writing_task', identity))
    assert.equal(resumed.claim_token, claim.claim_token)
    assert.deepEqual(resumed.result_schema, claim.result_schema)
    const receipt = {decision: 'pass', coverage: [{id: 'O0001', quote: 'A courier arrives.', note: 'No conflicting prerequisites.'}], issues: []}
    assert.equal((await call('submit_writing_result', {...identity, result: receipt})).isError, true)
    const result = {...receipt, claim_token: claim.claim_token}
    assert.equal((await call('submit_writing_result', {...identity, result: {...result, claim_token: 'stale-token'}})).isError, true)
    assert.equal((await call('submit_writing_result', {...identity, agent_id: 'wrong-pass', result})).isError, true)
    value(await call('submit_writing_result', {...identity, result}))
    const next = value(await call('list_writing_tasks', packageArgs))
    assert.ok(next.tasks.some(task => task.task_id === 'chunk-plan' && task.ready))
    assert.equal(value(await call('verify_writing_project', packageArgs)).ready_for_assembly, false)
    assert.equal((await call('assemble_writing_project', {...packageArgs, output_path: 'manuscript.md'})).isError, true)

    const planner = {...packageArgs, task_id: 'chunk-plan', agent_id: 'planner-pass'}
    const planClaim = value(await call('claim_writing_task', planner))
    value(await call('submit_writing_result', {...planner, result: {
      claim_token: planClaim.claim_token, style_contract: 'Plain English fixture prose.',
      chunks: [1, 2].map(index => ({
        id: `chunk-000${index}`, title: 'Arrival', brief: 'Establish the courier arrival.',
        outline_ids: ['O0001'], entry_state: 'Courier approaching.', exit_state: 'Courier present.',
        source_ids: [], reference_ids: [], depends_on: [], independent: false,
      })),
    }}))
    const writer = {...packageArgs, task_id: 'write-0001', agent_id: 'writer-pass'}
    const firstAttempt = value(await call('claim_writing_task', writer))
    // Repeated fixture text tests protocol transport and length checks, not prose quality.
    const text = 'courier '.repeat(5000).trim()
    const draft = {
      claim_token: firstAttempt.claim_token, text, covered_outline_ids: ['O0001'],
      state: {}, state_changes: [], pending_threads: [], handoff: 'Courier has arrived.',
    }
    value(await call('submit_writing_result', {...writer, result: draft}))
    const editor = {...packageArgs, task_id: 'review-0001', agent_id: 'editor-pass'}
    const editClaim = value(await call('claim_writing_task', editor))
    value(await call('submit_writing_result', {...editor, result: {
      claim_token: editClaim.claim_token, decision: 'revise',
      text_sha256: createHash('sha256').update(text).digest('hex'),
      coverage: [{id: 'P0001', quote: 'courier courier', note: 'Repeated fixture needs revision.'}],
      checks: Object.fromEntries(['outline', 'continuity', 'voice', 'naturalness'].map(key =>
        [key, {status: key === 'naturalness' ? 'issue' : 'pass', note: 'Protocol fixture assessment.'}])),
      issues: [{paragraph_id: 'P0001', quote: 'courier', reason: 'Repeated wording.', suggestion: 'Vary the prose.'}],
    }}))
    const revision = value(await call('claim_writing_task', writer))
    assert.notEqual(revision.claim_token, firstAttempt.claim_token)
    assert.equal(revision.result_schema.claim_token, revision.claim_token)
    assert.equal(value(await call('claim_writing_task', writer)).claim_token, revision.claim_token)
    const stale = await call('submit_writing_result', {...writer, result: draft})
    assert.equal(stale.isError, true, 'old child output cannot complete the new revision attempt')
    assert.match(JSON.stringify(stale.content), /claim.token|stale|attempt/i)
    const stillClaimed = value(await call('list_writing_tasks', packageArgs))
    assert.equal(stillClaimed.tasks.find(task => task.task_id === writer.task_id).status, 'claimed')
  } finally {
    await ctx.fiber.dispose()
    assert.equal(dirname(root), resolve(tmpdir()))
    assert.ok(basename(root).startsWith('writing-cordis-'))
    rmSync(root, {recursive: true, force: true})
  }
})
