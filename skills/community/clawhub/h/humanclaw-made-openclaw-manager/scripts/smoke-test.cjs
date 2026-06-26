const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');

const stateRoot = path.join(os.tmpdir(), `openclaw-manager-smoke-${Date.now()}`);
process.env.OPENCLAW_MANAGER_STATE_ROOT = stateRoot;

const { bootstrapManagerRuntime } = require('../dist/skill/bootstrap.js');
const { buildNormalizedInbound } = require('../dist/connectors/base.js');
const { telegramConnector } = require('../dist/connectors/telegram.js');

const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

const readShadows = async (runtime) => runtime.store.readJson(runtime.store.threadShadowsFile, []);

const writeShadows = async (runtime, shadows) => runtime.store.writeJson(runtime.store.threadShadowsFile, shadows);

const threadBase = (label) => ({
  source_type: 'chat',
  source_thread_key: `${label}:${Date.now()}`,
  message_type: 'user_message',
  attachments: [],
});

(async () => {
  await fs.rm(stateRoot, { recursive: true, force: true });

  const runtime = await bootstrapManagerRuntime();

  const greetingThread = threadBase('greeting');
  const greetings = ['你好', '收到', '好的'];
  const greetingResults = [];
  for (const content of greetings) {
    greetingResults.push(
      await runtime.shadowService.handleInbound(
        buildNormalizedInbound({
          ...greetingThread,
          content,
        })
      )
    );
  }
  assert(greetingResults.every((item) => item.mode === 'shadowed'), 'Three greetings should stay shadowed.');

  const taskThread = threadBase('task');
  const taskIntent = await runtime.shadowService.handleInbound(
    buildNormalizedInbound({
      ...taskThread,
      content: '帮我整理一下这份采访纪要，并给出可执行的大纲。',
    })
  );
  const taskContext = await runtime.shadowService.handleInbound(
    buildNormalizedInbound({
      ...taskThread,
      content: '参考链接在这里：https://example.com/brief ，另外附件里有背景资料。',
      attachments: [{ kind: 'brief', url: 'https://example.com/brief' }],
    })
  );
  assert(taskIntent.mode === 'shadowed', 'Task intent alone should not promote.');
  assert(taskContext.mode === 'promoted', 'Task intent + context payload should promote.');

  const ackThread = threadBase('ack');
  const ackIntent = await runtime.shadowService.handleInbound(
    buildNormalizedInbound({
      ...ackThread,
      content: '继续帮我分析这份数据，看看趋势。',
    })
  );
  const ackNoise = await runtime.shadowService.handleInbound(
    buildNormalizedInbound({
      ...ackThread,
      content: '好的',
    })
  );
  assert(ackIntent.mode === 'shadowed', 'Single task intent should stay shadowed.');
  assert(ackNoise.mode === 'shadowed', 'Task intent plus acknowledgement should stay shadowed.');

  const toolThread = threadBase('tool');
  const toolResult = await runtime.shadowService.handleInbound(
    buildNormalizedInbound({
      ...toolThread,
      content: '调用工具抓取最新资料。',
      message_type: 'tool_called',
      metadata: { tool_called: true },
    })
  );
  assert(toolResult.mode === 'promoted', 'tool_called should promote immediately.');

  const blockedThread = threadBase('blocked');
  const blockedResult = await runtime.shadowService.handleInbound(
    buildNormalizedInbound({
      ...blockedThread,
      content: '我现在卡住了，需要你决定先走哪个方案。',
      message_type: 'waiting_human',
      metadata: { current_state: 'waiting_human' },
    })
  );
  assert(blockedResult.mode === 'promoted', 'waiting_human should promote immediately.');

  const manual = await runtime.shadowService.manualAdopt({
    title: 'Manual Promotion Smoke',
    objective: 'Verify manual shadow promotion.',
    initial_message: 'Manual adoption should promote a synthetic shadow.',
    source_type: 'chat',
    source_thread_key: `manual:${Date.now()}`,
  });
  assert(Boolean(manual.session.session_id), 'Manual adopt should create a session.');

  const promoteThread = threadBase('promote');
  const promoteSeed = await runtime.shadowService.handleInbound(
    buildNormalizedInbound({
      ...promoteThread,
      content: '这里先记录一个待观察线程。',
    })
  );
  const promotedManually = await runtime.shadowService.promoteShadow(promoteSeed.shadow_id, {
    title: 'Manual Promote Smoke',
    objective: 'Verify promoteShadow.',
  });
  assert(Boolean(promotedManually.session.session_id), 'Manual promote should create a session.');

  const connectorPayload = telegramConnector.normalize({
    message: {
      chat: { id: 12345, title: 'Smoke Chat' },
      from: { id: 'agent-smoke', username: 'agent_smoke' },
      text: 'Please keep an eye on this thread.',
      message_id: 'msg-1',
      date: Math.floor(Date.now() / 1000),
    },
  });
  connectorPayload.metadata.requires_followup = true;
  const connectorResult = await runtime.shadowService.handleInbound(connectorPayload);
  assert(connectorResult.mode === 'shadowed', 'Connector follow-up alone should not promote.');

  const candidateShadows = await runtime.shadowService.listShadows();
  const connectorShadow = candidateShadows.find((item) => item.shadow_id === connectorResult.shadow_id);
  assert(Boolean(connectorShadow), 'Connector shadow should exist.');
  assert(connectorShadow.state === 'candidate', 'Connector follow-up should become a candidate shadow.');
  assert(connectorShadow.promotion_score === 1, 'Connector follow-up should add one promotion point.');

  let shadows = await readShadows(runtime);
  const noiseShadow = shadows.find((item) => item.shadow_id === greetingResults[0].shadow_id);
  const staleCandidate = shadows.find((item) => item.shadow_id === connectorResult.shadow_id);
  noiseShadow.updated_at = new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString();
  staleCandidate.last_effective_at = new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString();
  staleCandidate.state = 'candidate';
  await writeShadows(runtime, shadows);

  const archivedSweep = await runtime.shadowService.listShadows();
  const archivedNoise = archivedSweep.find((item) => item.shadow_id === greetingResults[0].shadow_id);
  const archivedCandidate = archivedSweep.find((item) => item.shadow_id === connectorResult.shadow_id);
  assert(archivedNoise.state === 'archived', 'Observed zero-score shadows should archive after seven days.');
  assert(archivedCandidate.state === 'archived', 'Candidate shadows should archive after fourteen idle days.');

  const resumed = await runtime.sessionService.resume(
    taskContext.session_id,
    'Resume from latest checkpoint'
  );
  await runtime.sessionService.checkpoint(resumed.session_id, {
    blockers: ['Need external confirmation'],
    summary: 'Waiting on an external update to continue.',
    next_machine_actions: ['Watch for inbound update.'],
  });

  await runtime.skillTraceService.wrap(
    {
      session_id: resumed.session_id,
      run_id: resumed.active_run_id,
      skill_name: 'smoke-skill',
      role: 'primary',
      input_summary: 'Resume and complete the test task.',
    },
    async () => ({
      output_summary: 'Completed the simulated smoke task.',
      outcome: 'advanced',
      value: { ok: true },
    })
  );

  const snapshot = await runtime.shareService.createSnapshot(resumed, 'run_evidence', {
    related_run_id: resumed.active_run_id,
  });
  const closed = await runtime.sessionService.close(resumed.session_id, {
    closure_type: 'completed',
    notes: 'Smoke test completed.',
    outcome: 'completed',
    reusable_skill_name: 'smoke-skill',
  });
  const fact = await runtime.capabilityFactService.createFromClosure(closed, {
    closure_type: 'completed',
    reusable_skill_name: 'smoke-skill',
  });
  const graph = await runtime.capabilityFactService.graphSummary();
  const digest = await runtime.commands['/digest']();
  const focus = await runtime.commands['/focus']();
  const threads = await runtime.commands['/threads']();

  const ackShadow = threads.find((item) => item.shadow_id === ackNoise.shadow_id);
  const digestObservation = digest.thread_observations.find((item) => item.shadow_id === ackNoise.shadow_id);

  assert(Boolean(ackShadow), 'Ack thread shadow should still be tracked.');
  assert(ackShadow.promotion_score === 2, 'Task intent should keep score even after a noise reply.');
  assert(ackShadow.effective_turn_count === 1, 'Ack thread should only count one effective turn.');
  assert(Boolean(digestObservation?.pending_reason), 'Digest should explain why a shadow is not yet promoted.');

  process.stdout.write(
    `${JSON.stringify(
      {
        greeting_modes: greetingResults.map((item) => item.mode),
        task_promotion: [taskIntent.mode, taskContext.mode],
        ack_promotion: [ackIntent.mode, ackNoise.mode],
        tool_mode: toolResult.mode,
        blocked_mode: blockedResult.mode,
        connector_mode: connectorResult.mode,
        archived_noise_state: archivedNoise.state,
        archived_candidate_state: archivedCandidate.state,
        snapshot_kind: snapshot.snapshot_kind,
        graph_nodes: graph.nodes.length,
        digest_sessions: digest.session_map.length,
        focus_candidates: focus.candidate_shadows.length,
        thread_count: threads.length,
        fact_id: fact.fact_id,
      },
      null,
      2
    )}\n`
  );
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
