import { existsSync, readFileSync, statSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..')

export const longFormGuidanceTool = serverName => `writing__${serverName}__longform_guidance`
export const agentCapabilitiesTool = serverName => `writing__${serverName}__agent_capabilities`

export function agentCapabilities(ctx, toolName, agent) {
  const definition = ctx.tools.get(toolName, agent)
  return {
    delegation_tool: toolName,
    available: Boolean(definition),
    mode: definition ? 'native-tool-visible' : 'sequential-role-passes',
    parameters: definition?.parameters ?? null,
    runtime_verified: false,
    note: definition
      ? 'Tool is visible in the calling agent scope. Startup, provider, depth, permissions and completion still require runtime checks. Use only its advertised parameters; do not change model or preset without authorization.'
      : 'No visible configured delegation tool. Recheck after provider changes; disclose sequential role passes, not independent agents.',
  }
}

export function longFormWritingGuidance(serverName = 'human-writing') {
  const tool = name => `mcp__${serverName}__${name}`
  return `# Long-form writing orchestration
Use for requested output >=10,000 characters or words, or explicit multi-agent long-form writing,
not merely a long input or an ordinary long-form audit. Preserve the requested length unit.
First call ${agentCapabilitiesTool(serverName)} to inspect the configured delegation tool in
the current agent scope. Tool visibility is not proof of an operational provider or completed work.
Save the agreed outline through normal workspace tools; do not invent missing user facts.
Call ${tool('plan_long_form_writing')}(outline_path, output_dir, style, target_length,
chunk_size=5000, length_unit='characters'|'words', execution_mode='sequential', max_parallel=4,
context_paths?, source_paths?, reference_paths?). Context is project truth, sources are factual
evidence, references are voice only. All paths stay inside the configured writing root.

Order: outline checker -> chunk planner -> writer per chunk -> separate editor per chunk ->
final continuity reviewer -> assemble. IDs: outline-check -> chunk-plan -> write-0001 /
review-0001 pairs -> continuity. Call ${tool('list_writing_tasks')}(package_dir);
claim only ready tasks via ${tool('claim_writing_task')}(package_dir, task_id, agent_id).
The claim returns content (complete role-specific prompt) and result_schema: forward both
unchanged, never substitute a generic role prompt. Keep the claim's agent_id through
${tool('submit_writing_result')}(package_dir, task_id, result: object, agent_id).
Forward the full content, result_schema, and claim_token unchanged to the assigned role.
The submitted result.claim_token must copy the current claim_token, also supplied in
result_schema.claim_token. Track child ID, task ID, agent_id, and claim_token together.
Claims include lease_seconds. Before expiry, the same coordinator may renew by claiming
the same task with the same agent_id; an active renewal keeps the token. After expiry or
reissue never reuse old child output: cancel/settle it before starting a new assignment.
Large assignments may be file pointers: paginate the entire referenced material, not just previews.
An active same-agent resume keeps its token; a reclaim or revision attempt gets a new token.
Reject stale child results from an earlier attempt; never relabel them with a new token.
Use distinct writer/editor identities; retain each identity on bounded revision attempts.
The final reviewer must differ from all chunk writers.

If the host exposes a native delegation tool, use its advertised schema (DSH normally uses
subagent with description and prompt; toolName is configurable, and DSH 0.2.2+ supports
optional provider/model/reasoning_effort and agent_preset routing). DSH requires dsh-subagent,
a configured provider such as dsh-subagent-spawn-in-process, and dsh-tool-subagent; the service
or MCP alone is not an agent runner. A native start returns a child ID, NOT completed prose.
Map that child ID to the claimed agent_id, wait for its completion notice, then submit the
actual structured result unchanged. Never fabricate receipts or count a start as approval.
Do not assume a fresh child inherits conversation; forward the full claim and schema.
If delegation is absent, denied, or fails, disclose the limitation. Use honest sequential
distinct role passes, with role-pass identities rather than invented child IDs; explicitly
say they are not independent agents. Do not silently reassign an already claimed task.

After each submission, re-list readiness. Fix requests permit only the bounded revisions
allowed by the returned protocol. Stop and report exhausted or blocked work; do not bypass
approval or edit package state. Later tasks stay blocked until their predecessor is approved.
Parallel work is permitted ONLY in execution_mode='contract' with approved explicit independent
block entry/exit contracts, and only for ready tasks up to max_parallel and host capacity.
max_parallel bounds simultaneous claims, not guaranteed agent processes. 60000/5000 means
12 writing jobs plus their review jobs, not 12 guaranteed concurrent agents.
Otherwise run sequentially, even if the host suggests parallel independent delegation.
After all required approvals, call ${tool('verify_writing_project')}(package_dir), then
${tool('assemble_writing_project')}(package_dir, output_path). Never claim completion on
failed verification or assembly, and never publish externally without user instruction.`
}

export function probePython(configured) {
  if (configured !== undefined) {
    if (typeof configured !== 'string' || !configured.trim()) {
      throw new Error('pythonCommand must be an executable path.')
    }
    return configured.trim()
  }
  if (process.env.PYTHON && process.env.PYTHON.trim()) return process.env.PYTHON.trim()
  if (process.env.VIRTUAL_ENV) {
    const venvPy = process.platform === 'win32'
      ? resolve(process.env.VIRTUAL_ENV, 'Scripts/python.exe')
      : resolve(process.env.VIRTUAL_ENV, 'bin/python')
    if (existsSync(venvPy)) return venvPy
  }
  if (process.platform === 'win32') {
    const userProfile = process.env.USERPROFILE || ''
    const cwdCandidates = [
      resolve(process.cwd(), '.venv/Scripts/python.exe'),
      resolve(process.cwd(), 'venv/Scripts/python.exe'),
      resolve(userProfile, '.venv-html-to-docx/Scripts/python.exe'),
    ]
    for (const cand of cwdCandidates) {
      if (cand && existsSync(cand)) return cand
    }
  }
  return 'python'
}

export function resolveServerConfig(config = {}) {
  const root = resolve(config.root ?? process.cwd())
  if (!existsSync(resolve(packageRoot, 'humanwriting/mcp_server.py'))) {
    throw new Error('Writing runtime is missing. Install the repository-root bundle or the published release tarball.')
  }
  const command = probePython(config.pythonCommand)
  const serverName = config.serverName ?? 'human-writing'
  if (!/^[A-Za-z0-9_-]{1,32}$/.test(serverName)) throw new Error('serverName must contain 1–32 letters, numbers, underscores, or hyphens.')
  const timeout = config.toolCallTimeoutMs ?? 60000
  const delegationToolName = config.delegationToolName ?? 'subagent'
  if (typeof delegationToolName !== 'string' || !/^[A-Za-z0-9_-]{1,100}$/.test(delegationToolName)) {
    throw new Error('delegationToolName must be a tool identifier of at most 100 characters.')
  }
  if (!Number.isSafeInteger(timeout) || timeout < 1000) throw new Error('toolCallTimeoutMs must be an integer of at least 1000.')
  if (!existsSync(root)) throw new Error('Writing workspace does not exist.')
  if (!statSync(root).isDirectory()) throw new Error('Writing workspace must be a directory.')
  return {
    transport: 'stdio', serverName, command,
    // -I ignores user-site and PYTHONPATH. Import only the bundled runtime before
    // considering the writing workspace, which may itself contain Python files.
    args: ['-I', '-X', 'utf8', '-c',
      'import runpy,sys; sys.path.insert(0,sys.argv.pop(1)); runpy.run_module("humanwriting.mcp_server",run_name="__main__")',
      packageRoot, '--root', root],
    env: {}, cwd: root, toolCallTimeoutMs: timeout, failOnStartupError: true,
  }
}

export function writingGuidance(serverName = 'human-writing') {
  const tool = name => `mcp__${serverName}__${name}`
  return `# Human Writing for DSH\n\nApply only to requested authored prose, rewriting, or editorial review, not code or ordinary answers.
For novels use fiction/webnovel; for papers academic-paper; for reports formal-document;
for news news-report; for essays argumentative; for posts self-media. Respect the user's language.
For requested output >=10,000 characters or words, or explicit multi-agent long-form writing,
first call ${longFormGuidanceTool(serverName)} and follow its plan/claim/submit workflow.
This threshold concerns requested output, not input length. Load that protocol only on demand.
Before substantive writing, call ${tool('compile_generation_prompt')} with the task, style,
supplied context, and source_paths/reference_paths when available. Apply its instructions
while composing. For supplied-draft cleanup use ${tool('compile_humanize_prompt')}.
Use ${tool('compile_critique_prompt')} when the user wants advice rather than replacement text.
Keep factual evidence separate from voice references; never invent a citation, result,
personal experience, or source-backed detail. When necessary evidence is missing, narrow
the claim or identify missing input. Maintain fiction ledgers across chapters.
Before delivering substantial prose, use ${tool('lint_text')} as an editorial lead, not a
mandatory rewrite gate. Repair only evidenced defects. For rewrites check ${tool('verify_fidelity')}
and ${tool('verify_protected_content')}; unchanged numbers do not establish unchanged meaning.
Use focused audits when needed, not every audit on every paragraph. Long-form reviews
use the plan/claim/receipt/coverage tools. Do not claim naturalness or publish externally
solely because a lint score improved. Write or save content through DSH's normal output
tools when requested; publishing to an external destination needs that user's instruction.
\n${readFileSync(resolve(packageRoot, 'skills/generation-quality.md'), 'utf8')}`
}

export async function mountWritingPlugin(ctx, config, mountMcp) {
  const serverConfig = resolveServerConfig(config)
  await mountMcp(ctx, serverConfig)
  ctx.tools.register({
    name: agentCapabilitiesTool(serverConfig.serverName),
    description: 'Inspect the configured native delegation tool in the calling agent scope. Does not start agents or prove provider readiness.',
    parameters: {type: 'object', properties: {}, additionalProperties: false},
    output: {schema: {type: 'object'}, render: (_args, value) => [{type: 'text', text: JSON.stringify(value)}]},
    async execute(_args, exec) { return agentCapabilities(ctx, config.delegationToolName ?? 'subagent', exec.agent) },
  })
  ctx.tools.register({
    name: longFormGuidanceTool(serverConfig.serverName),
    description: 'Load the long-form drafting protocol only for >=10,000 requested output characters/words or explicit multi-agent long-form writing. Does not start agents.',
    parameters: {type: 'object', properties: {}, additionalProperties: false},
    output: {schema: {type: 'string'}, render: (_args, value) => [{type: 'text', text: value}]},
    async execute() { return longFormWritingGuidance(serverConfig.serverName) },
  })
  if (config.generationGuidance !== false) {
    ctx.systemPrompt.section({
      name: `human-writing:${serverConfig.serverName}`, order: 7500,
      interpolate: false, text: writingGuidance(serverConfig.serverName),
    })
  }
}
