import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const FAILURE_RULES = [
  { failureClass: 'NetworkPolicyBlocked', severity: 'high', patterns: [/网络策略/, /network policy/i, /blocked by current network/i], nextAction: 'Route through an approved provider/network path or mark the provider unavailable before retrying.' },
  { failureClass: 'GatewayUnavailable', severity: 'high', patterns: [/ECONNREFUSED/i, /Gateway unreachable/i, /gateway.*timeout/i, /websocket closed:\s*1006/i], nextAction: 'Check LaunchAgent, gateway logs, and local port readiness before blaming the channel.' },
  { failureClass: 'SessionContextRot', severity: 'medium', patterns: [/stale .*session/i, /skillsSnapshot/i, /记不得自己的身份/, /identity regression/i], nextAction: 'Start a new session or archive stale sessions after skill, config, or identity changes.' },
  { failureClass: 'SkillMissing', severity: 'medium', patterns: [/skill.*not found/i, /no .* in skillsSnapshot/i, /missing skill/i], nextAction: 'Verify skill install path, snapshot freshness, and whether the target channel loaded the updated catalog.' },
  { failureClass: 'ToolInvalidArguments', severity: 'medium', patterns: [/InvalidArguments/i, /invalid arguments/i, /oldText/i, /Edit:.*failed/i, /edit.*failed/i], nextAction: 'Record the bad tool call shape and add a guardrail or example to the relevant skill.' },
  { failureClass: 'ProviderError', severity: 'medium', patterns: [/ProviderError/i, /rate limit/i, /429\b/, /5\d\d .*provider/i, /model .*not available/i], nextAction: 'Switch provider/model only after recording the provider, model, and failure response.' },
  { failureClass: 'ExternalPlatformBlocked', severity: 'high', patterns: [/X API.*unavailable/i, /cannot use api/i, /login required/i, /captcha/i, /visibility proof/i], nextAction: 'Use browser/ACP fallback or classify as externally blocked with proof URL requirements.' },
  { failureClass: 'HumanApprovalRequired', severity: 'low', patterns: [/approval required/i, /ask Ray/i, /explicit authorization/i, /production deploy/i], nextAction: 'Surface the exact approval boundary and the smallest safe next action.' },
];

export function classifyFailureText(text, source = 'inline') {
  const body = String(text || '');
  if (!body.trim()) return [];
  const events = [];
  for (const line of body.split(/\r?\n/).filter(Boolean)) {
    for (const rule of FAILURE_RULES) {
      if (!rule.patterns.some((pattern) => pattern.test(line))) continue;
      events.push({
        failureClass: rule.failureClass,
        severity: rule.severity,
        source,
        evidence: line.trim().slice(0, 500),
        nextAction: rule.nextAction,
      });
      break;
    }
  }
  return dedupeEvents(events);
}

export function summarizeFailureEvents(events) {
  const byClass = {};
  for (const event of events) {
    const key = event.failureClass || 'Unknown';
    byClass[key] ??= { failureClass: key, count: 0, severity: event.severity || 'unknown', examples: [], nextAction: event.nextAction || null };
    byClass[key].count += 1;
    if (byClass[key].examples.length < 5) byClass[key].examples.push({ source: event.source, evidence: event.evidence });
  }
  return {
    total: events.length,
    byClass,
    topClasses: Object.values(byClass).sort((a, b) => b.count - a.count || a.failureClass.localeCompare(b.failureClass)),
  };
}

export function readRecentText(path, maxBytes = 250_000) {
  if (!existsSync(path)) return '';
  const text = readFileSync(path, 'utf8');
  const size = statSync(path).size;
  return size <= maxBytes ? text : text.slice(-maxBytes);
}

export function scanFailureSources(paths) {
  const events = [];
  for (const path of paths) events.push(...classifyFailureText(readRecentText(path), path));
  return { generatedAt: new Date().toISOString(), sources: paths, events, summary: summarizeFailureEvents(events) };
}

export function readJsonSafe(path, fallback = null) {
  try {
    if (!existsSync(path)) return fallback;
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

export function readAgentSessions(openclawHome, agents) {
  const result = {};
  for (const agent of agents) {
    const sessionsPath = resolve(openclawHome, 'agents', agent, 'sessions', 'sessions.json');
    const sessionsJson = readJsonSafe(sessionsPath, {});
    result[agent] = Object.entries(sessionsJson || {}).map(([key, value]) => ({
      key,
      updatedAt: value?.updatedAt || null,
      model: value?.model || value?.authProfileOverride || null,
      channel: value?.lastChannel || value?.deliveryContext?.channel || value?.origin?.provider || null,
      sessionFile: value?.sessionFile || null,
    })).sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0));
  }
  return result;
}

export function buildAgentScorecard({ date, progressReport, sessions = {} }) {
  const agents = {};
  for (const [laneName, lane] of Object.entries(progressReport?.lanes || {})) {
    const agent = lane.agent || 'unassigned';
    agents[agent] ??= { agent, delivered: 0, blocked: 0, failed: 0, inProgress: 0, lanes: [], lastSessionKey: null, lastSessionAt: null };
    const stateText = String(lane.agentStatus || lane.state || '').toUpperCase();
    if (stateText.includes('DELIVERED') || stateText.includes('PROOF_VERIFIED')) agents[agent].delivered += 1;
    else if (stateText.includes('BLOCK')) agents[agent].blocked += 1;
    else if (stateText.includes('FAIL')) agents[agent].failed += 1;
    else agents[agent].inProgress += 1;
    const row = {
      lane: laneName,
      state: lane.state || null,
      agentStatus: lane.agentStatus || null,
      summary: lane.agentSummary || null,
      blocker: lane.blocker || null,
      missing: lane.missing_receipts || lane.todayBlockedOrMissing || [],
      evidence: lane.evidenceLinks || lane.receipts || [],
      nextHandoff: lane.nextHandoff || null,
    };
    const repair = classifyLaneRepair(row, { date: date || progressReport?.date, agent, lane: laneName, history: arguments[0]?.history || [] });
    if (repair) row.repair = repair;
    agents[agent].lanes.push(row);
  }
  for (const [agent, rows] of Object.entries(sessions)) {
    agents[agent] ??= { agent, delivered: 0, blocked: 0, failed: 0, inProgress: 0, lanes: [], lastSessionKey: null, lastSessionAt: null };
    const latest = rows?.[0];
    if (!latest) continue;
    agents[agent].lastSessionKey = latest.key;
    agents[agent].lastSessionAt = latest.updatedAt ? new Date(latest.updatedAt).toISOString() : null;
    agents[agent].lastSession = latest;
  }
  return {
    date: date || progressReport?.date || new Date().toLocaleDateString('sv-SE', { timeZone: 'Asia/Shanghai' }),
    generatedAt: new Date().toISOString(),
    status: progressReport?.status || null,
    summary: progressReport?.summary || null,
    agents,
  };
}

export function classifyLaneRepair(lane, { date, agent, lane: laneName, history = [] } = {}) {
  const stateText = String(lane.agentStatus || lane.state || '').toUpperCase();
  const isFailure = stateText.includes('FAIL') || stateText.includes('BLOCK') || stateText.includes('PENDING');
  if (!isFailure) return null;

  const text = [
    lane.blocker,
    lane.summary,
    lane.nextHandoff,
    ...(Array.isArray(lane.missing) ? lane.missing : []),
  ].filter(Boolean).join('\n');
  const failureClass = inferLaneFailureClass(text);
  const repeatCount7d = 1 + countRecentRepeats(history, { date, agent, lane: laneName, failureClass });
  const repairState = repairStateForFailure(failureClass, repeatCount7d);

  return {
    repairState,
    failureClass,
    nextAction: nextActionForFailure(failureClass, lane),
    repeatCount7d,
    escalation: repeatCount7d >= 2 ? 'Create a self-improvement experiment before another blind retry.' : null,
  };
}

export function buildRepairTickets(scorecard) {
  const tickets = [];
  for (const agent of Object.values(scorecard.agents || {})) {
    for (const lane of agent.lanes || []) {
      if (!lane.repair) continue;
      const laneId = lane.lane.startsWith(`${agent.agent}-`) ? lane.lane : `${agent.agent}-${lane.lane}`;
      tickets.push({
        ticket_id: `rt-${scorecard.date}-${laneId}-harness-repair`,
        date: scorecard.date,
        owner: agent.agent,
        agent: agent.agent,
        lane: lane.lane,
        failureClass: lane.repair.failureClass,
        repairState: lane.repair.repairState,
        blocker: lane.blocker,
        missingProof: lane.missing || [],
        evidence: lane.evidence || [],
        nextAction: lane.repair.nextAction,
        repeatCount7d: lane.repair.repeatCount7d,
        escalation: lane.repair.escalation,
        retryPolicy: retryPolicyForFailure(lane.repair.failureClass),
        status: lane.repair.repairState === 'EXPERIMENT_REQUIRED' ? 'NEEDS_EXPERIMENT' : 'OPEN',
        generatedAt: new Date().toISOString(),
      });
    }
  }
  return tickets;
}

export function writeRepairTickets(tickets, rootDir) {
  const written = [];
  for (const ticket of tickets) {
    const dir = resolve(rootDir, ticket.date);
    mkdirSync(dir, { recursive: true });
    const path = resolve(dir, `${ticket.ticket_id}.json`);
    writeFileSync(path, `${JSON.stringify(ticket, null, 2)}\n`);
    written.push(path);
  }
  return written;
}

export function markdownScorecard(scorecard) {
  const lines = [`# Agent Harness Scorecard — ${scorecard.date}`, '', `Generated: ${scorecard.generatedAt}`, `Status: ${scorecard.status || 'unknown'}`, '', scorecard.summary || 'No summary available.', ''];
  for (const agent of Object.values(scorecard.agents).sort((a, b) => a.agent.localeCompare(b.agent))) {
    lines.push(`## ${agent.agent}`, `- Delivered: ${agent.delivered}`, `- Blocked: ${agent.blocked}`, `- Failed: ${agent.failed}`, `- In progress/unknown: ${agent.inProgress}`);
    if (agent.lastSessionKey) lines.push(`- Last session: ${agent.lastSessionKey} (${agent.lastSessionAt || 'unknown time'})`);
    for (const lane of agent.lanes) {
      lines.push(`- Lane ${lane.lane}: ${lane.agentStatus || lane.state || 'unknown'}${lane.blocker ? ` — ${lane.blocker}` : ''}`);
      if (lane.repair) lines.push(`- Repair ${lane.lane}: ${lane.repair.repairState} / ${lane.repair.failureClass} / repeat7d=${lane.repair.repeatCount7d}`);
    }
    lines.push('');
  }
  return `${lines.join('\n').trim()}\n`;
}

function inferLaneFailureClass(text) {
  const body = String(text || '');
  if (/proof|receipt|live URL|visibility|验真|证据/i.test(body)) return 'ProofMissing';
  if (/upstream|waiting for|等待/i.test(body)) return 'UpstreamMissing';
  const classified = classifyFailureText(body);
  return classified[0]?.failureClass || 'UnknownFailure';
}

function countRecentRepeats(history, { date, agent, lane, failureClass }) {
  const now = date ? Date.parse(`${date}T00:00:00Z`) : Date.now();
  const sevenDays = 7 * 24 * 60 * 60 * 1000;
  return (history || []).filter((item) => {
    if (item.agent !== agent || item.lane !== lane || item.failureClass !== failureClass) return false;
    const t = Date.parse(`${item.date}T00:00:00Z`);
    return Number.isFinite(t) && now - t > 0 && now - t <= sevenDays;
  }).length;
}

function repairStateForFailure(failureClass, repeatCount7d) {
  if (repeatCount7d >= 2) return 'EXPERIMENT_REQUIRED';
  if (failureClass === 'HumanApprovalRequired') return 'HUMAN_APPROVAL_REQUIRED';
  if (failureClass === 'UpstreamMissing') return 'BLOCKED_UPSTREAM';
  return 'TICKET_CREATED';
}

function nextActionForFailure(failureClass, lane) {
  if (failureClass === 'ProofMissing') return 'Find or produce missing proof/receipt before retrying the agent.';
  if (failureClass === 'UpstreamMissing') return 'Repair upstream owner/lane before asking downstream to retry.';
  if (failureClass === 'ToolInvalidArguments') return 'Add a tool-call guardrail or example, then rerun the smallest failing step.';
  if (failureClass === 'SessionContextRot') return 'Archive stale session or start a fresh session so updated skills/config load.';
  if (failureClass === 'ExternalPlatformBlocked') return 'Use browser/ACP fallback or record explicit platform blocker proof.';
  if (failureClass === 'GatewayUnavailable') return 'Fix gateway/LaunchAgent/port readiness before retrying channel work.';
  return lane.nextHandoff || 'Create a concrete repair action with evidence and owner.';
}

function retryPolicyForFailure(failureClass) {
  if (['ProofMissing', 'UpstreamMissing', 'HumanApprovalRequired'].includes(failureClass)) return 'do_not_retry_until_unblocked';
  if (['GatewayUnavailable', 'SessionContextRot', 'ToolInvalidArguments'].includes(failureClass)) return 'repair_then_single_retry';
  return 'single_retry_with_evidence';
}

export function defaultFailureSources(openclawHome, workspace) {
  const sources = [resolve(openclawHome, 'logs', 'gateway.log'), resolve(openclawHome, 'logs', 'gateway.err.log'), resolve(workspace, 'progress-log.md')];
  const elonLogDir = resolve(openclawHome, 'workspace-elon', 'logs');
  if (existsSync(elonLogDir)) {
    sources.push(...readdirSync(elonLogDir).filter((file) => file.endsWith('.log')).sort().slice(-20).map((file) => resolve(elonLogDir, file)));
  }
  return sources.filter((path) => existsSync(path));
}

function dedupeEvents(events) {
  const seen = new Set();
  return events.filter((event) => {
    const key = `${event.failureClass}:${event.source}:${event.evidence}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}
