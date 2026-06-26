import express from 'express'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const app  = express()
const PORT = 3721
const HOME = process.env.HOME || process.env.USERPROFILE || ''
const OC   = path.join(HOME, '.openclaw')

// In production serve the Vite build; in dev Vite handles the frontend
app.use(express.static(path.join(__dirname, 'dist')))
app.use((req, res, next) => { res.setHeader('Cache-Control', 'no-store'); next() })

// ─── Cache ───────────────────────────────────────────────────────────────────
const _cache = {}
function cached(key, ttlMs, fn) {
  const now = Date.now()
  if (_cache[key] && now - _cache[key].t < ttlMs) return _cache[key].v
  const v = fn()
  _cache[key] = { v, t: now }
  return v
}

// ─── Helpers ─────────────────────────────────────────────────────────────────
function readJSON(p)  { try { return JSON.parse(fs.readFileSync(p, 'utf8')) } catch { return null } }
function readText(p)  { try { return fs.readFileSync(p, 'utf8') } catch { return null } }

// ─── Context window helper ────────────────────────────────────────────────────
// Model context windows (tokens)
const CTX_WINDOWS = {
  'claude-opus-4-6': 1000000,
  'claude-sonnet-4-6': 1000000,
  'claude-sonnet-4-5-20250514': 1000000,
  'claude-haiku-4-5-20251001': 1000000,
  'anthropic/claude-opus-4-6': 1000000,
  'anthropic/claude-sonnet-4-6': 1000000,
  'anthropic/claude-sonnet-4-5-20250514': 1000000,
  'anthropic/claude-haiku-4-5-20251001': 1000000,
  default: 1000000,
}
function getCtxMax(model) {
  if (!model) return CTX_WINDOWS.default
  const key = typeof model === 'string' ? model : (model.primary || '')
  return CTX_WINDOWS[key] || CTX_WINDOWS.default
}
function getContextUsage(agentDir, model) {
  try {
    const sessDir = path.join(agentDir, 'sessions')
    const files = fs.readdirSync(sessDir)
      .filter(f => f.endsWith('.jsonl') && !f.includes('.deleted'))
      .map(f => ({ f, mt: fs.statSync(path.join(sessDir, f)).mtimeMs }))
      .sort((a, b) => b.mt - a.mt)
    if (!files.length) return null
    const latest = path.join(sessDir, files[0].f)
    const lines = fs.readFileSync(latest, 'utf8').split('\n').filter(Boolean)
    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        const ev = JSON.parse(lines[i])
        if (ev.type === 'message' && ev.message?.role === 'assistant') {
          const u = ev.message.usage
          if (u?.totalTokens) {
            const ctx = (u.input || 0) + (u.cacheRead || 0) + (u.cacheWrite || 0)
            const maxCtx = getCtxMax(model)
            return { used: ctx, max: maxCtx, pct: Math.round(ctx / maxCtx * 100) }
          }
        }
      } catch {}
    }
  } catch {}
  return null
}

// ─── Agent ID discovery ─────────────────────────────────────────────────────
function getAgentIds() {
  const config = readJSON(path.join(OC, 'openclaw.json'))
  return (config?.agents?.list || []).map(a => a.id)
}

// ─── Agents ──────────────────────────────────────────────────────────────────
function getAgentData() {
  const config = readJSON(path.join(OC, 'openclaw.json'))
  if (!config) return []

  return (config.agents?.list || []).map(agent => {
    const agentDir   = path.join(OC, 'agents', agent.id)
    const sessions   = readJSON(path.join(agentDir, 'sessions', 'sessions.json')) || {}
    const auth       = readJSON(path.join(agentDir, 'agent', 'auth-profiles.json'))
    const sessionList = Object.values(sessions)
    const lastActivity = sessionList.reduce((max, s) => Math.max(max, s.updatedAt || 0), 0)
    const isActive   = lastActivity > 0 && Date.now() - lastActivity < 5 * 60 * 1000
    const authErrorCount = auth?.usageStats
      ? Object.values(auth.usageStats).reduce((s, u) => s + (u.errorCount || 0), 0) : 0

    const workspaceDir = agent.workspace || path.join(OC, 'workspace')
    const today = new Date().toISOString().slice(0, 10)

    let recentSessions = 0
    try {
      const sessDir = path.join(agentDir, 'sessions')
      recentSessions = fs.readdirSync(sessDir)
        .filter(f => f.endsWith('.jsonl') && !f.includes('.deleted'))
        .filter(f => { try { return Date.now() - fs.statSync(path.join(sessDir, f)).mtimeMs < 3600000 } catch { return false } })
        .length
    } catch {}

    return {
      id: agent.id, name: agent.identity?.name || agent.id, emoji: agent.identity?.emoji || '🤖',
      model: agent.model || config.agents?.defaults?.model,
      lastActivity, sessionCount: sessionList.length, recentSessions,
      status: isActive ? 'active' : 'idle', authErrorCount,
      contextUsage: getContextUsage(agentDir, agent.model || config.agents?.defaults?.model),
      soul:     readText(path.join(workspaceDir, 'SOUL.md')),
      identity: readText(path.join(workspaceDir, 'IDENTITY.md')),
      memory:   readText(path.join(workspaceDir, 'MEMORY.md')),
      dailyLog: readText(path.join(workspaceDir, 'memory', 'daily', `${today}.md`)),
    }
  })
}

// ─── Sub-agents ───────────────────────────────────────────────────────────────
// Reads first user message from a session JSONL as the task description
function readSessionTask(filePath) {
  try {
    const lines = fs.readFileSync(filePath, 'utf8').split('\n').filter(Boolean)
    for (const line of lines) {
      try {
        const ev = JSON.parse(line)
        if (ev.type === 'message' && ev.message?.role === 'user') {
          const text = (ev.message.content || []).filter(c => c.type === 'text').map(c => c.text).join(' ')
          return text.slice(0, 200)
        }
      } catch {}
    }
  } catch {}
  return ''
}

function getSubagentData() {
  const now = Date.now()
  const active = []
  const recent = []

  // Primary source: subagents/runs.json (formally dispatched runs)
  const runsData = readJSON(path.join(OC, 'subagents', 'runs.json'))
  for (const r of Object.values(runsData?.runs || {})) {
    if (!r.endedAt) {
      active.push({ runId: r.runId, label: r.label || '(unlabelled)',
        task: (r.task || '').slice(0, 200), model: r.model,
        createdAt: r.createdAt, startedAt: r.startedAt, source: 'runs' })
    } else if (r.endedAt > now - 48 * 3600000) {
      recent.push({ runId: r.runId, label: r.label || '(unlabelled)',
        task: (r.task || '').slice(0, 200),
        status: r.outcome?.status || 'unknown', endedReason: r.endedReason,
        createdAt: r.createdAt, endedAt: r.endedAt,
        durationMs: r.endedAt - r.startedAt, model: r.model,
        result: r.frozenResultText ? r.frozenResultText.slice(0, 500) : null,
        source: 'runs' })
    }
  }

  // Secondary source: sessions.json — sessions with 'subagent' in the key
  for (const agentId of getAgentIds()) {
    const sessPath = path.join(OC, 'agents', agentId, 'sessions', 'sessions.json')
    const sessions = readJSON(sessPath) || {}
    for (const [key, s] of Object.entries(sessions)) {
      if (!key.includes('subagent')) continue
      const updatedAt  = s.updatedAt || 0
      const sessionFile = s.sessionFile || path.join(OC, 'agents', agentId, 'sessions', `${s.sessionId}.jsonl`)
      const task = readSessionTask(sessionFile)
      const runId = s.sessionId || key
      const isAlreadyCovered = active.some(r => r.runId === runId) || recent.some(r => r.runId === runId)
      if (isAlreadyCovered) continue

      if (updatedAt > now - 30 * 60 * 1000) {
        // Updated in last 10 min → treat as active
        active.push({ runId, label: key.split(':').pop().slice(0, 16),
          task, model: null, createdAt: updatedAt, startedAt: updatedAt, source: 'session' })
      } else if (updatedAt > now - 48 * 3600000) {
        recent.push({ runId, label: key.split(':').pop().slice(0, 16),
          task, status: s.abortedLastRun ? 'error' : 'ok',
          createdAt: updatedAt, endedAt: updatedAt,
          durationMs: 0, model: null, source: 'session' })
      }
    }
  }

  recent.sort((a, b) => (b.endedAt || 0) - (a.endedAt || 0))
  return { active, recent: recent.slice(0, 20) }
}

// ─── Cron jobs ───────────────────────────────────────────────────────────────
function getCronData() {
  const data = readJSON(path.join(OC, 'cron', 'jobs.json'))
  if (!data) return []
  const runsDir = path.join(OC, 'cron', 'runs')
  return (data.jobs || []).map(job => {
    let recentRuns = []
    try {
      const lines = fs.readFileSync(path.join(runsDir, `${job.id}.jsonl`), 'utf8')
        .trim().split('\n').filter(Boolean)
      recentRuns = lines.slice(-5).map(l => JSON.parse(l)).reverse()
    } catch {}
    return {
      id: job.id, name: job.name, enabled: job.enabled,
      schedule: job.schedule, agentId: job.agentId,
      nextRunAtMs:       job.state?.nextRunAtMs,
      lastRunAtMs:       job.state?.lastRunAtMs,
      lastStatus:        job.state?.lastStatus,
      lastError:         job.state?.lastError,
      consecutiveErrors: job.state?.consecutiveErrors || 0,
      lastDurationMs:    job.state?.lastDurationMs,
      recentRuns,
    }
  })
}

// ─── Token costs ─────────────────────────────────────────────────────────────
function getTokenCosts() {
  const now  = Date.now()
  const todayStart   = (() => { const d = new Date(); d.setHours(0,0,0,0); return d.getTime() })()
  const thirtyDaysAgo = now - 30 * 86400000
  const total = { cost: 0, tokens: 0, input: 0, output: 0 }
  const today = { cost: 0, tokens: 0, input: 0, output: 0 }
  const byModel = {}, byDay = {}

  for (const agentId of getAgentIds()) {
    const sessDir = path.join(OC, 'agents', agentId, 'sessions')
    let files
    try {
      files = fs.readdirSync(sessDir)
        .filter(f => f.endsWith('.jsonl') && !f.includes('.deleted'))
        .filter(f => { try { return fs.statSync(path.join(sessDir, f)).mtimeMs > thirtyDaysAgo } catch { return false } })
    } catch { continue }

    for (const file of files) {
      const fp = path.join(sessDir, file)
      const isToday = (() => { try { return fs.statSync(fp).mtimeMs > todayStart } catch { return false } })()
      let content
      try { content = fs.readFileSync(fp, 'utf8') } catch { continue }

      for (const line of content.split('\n')) {
        if (!line.trim()) continue
        try {
          const ev = JSON.parse(line)
          if (ev.type !== 'message' || ev.message?.role !== 'assistant') continue
          if (ev.message?.model === 'delivery-mirror') continue
          const u = ev.message.usage
          if (!u?.cost) continue
          const cost = u.cost.total || 0, tokens = u.totalTokens || 0
          const ts = ev.timestamp ? new Date(ev.timestamp).getTime() : (isToday ? Date.now() : 0)
          const model = ev.message.model || 'unknown'

          total.cost   += cost;  total.tokens += tokens
          total.input  += u.input || 0; total.output += u.output || 0
          if (ts >= todayStart) { today.cost += cost; today.tokens += tokens }

          if (!byModel[model]) byModel[model] = { cost: 0, tokens: 0 }
          byModel[model].cost += cost; byModel[model].tokens += tokens

          const day = new Date(ts || Date.now()).toISOString().slice(0, 10)
          if (!byDay[day]) byDay[day] = { cost: 0, tokens: 0 }
          byDay[day].cost += cost; byDay[day].tokens += tokens
        } catch {}
      }
    }
  }
  return { total, today, byModel, byDay }
}

// ─── Gateway status ───────────────────────────────────────────────────────────
function getGatewayStatus() {
  try {
    const stat   = fs.statSync(path.join(OC, 'logs', 'gateway.log'))
    const update = readJSON(path.join(OC, 'update-check.json'))
    return {
      status:      Date.now() - stat.mtimeMs < 300000 ? 'online' : 'stale',
      version:     update?.currentVersion || null,
      logModified: stat.mtimeMs,
    }
  } catch { return { status: 'offline', version: null } }
}

// ─── Session list ─────────────────────────────────────────────────────────────
app.get('/api/sessions/:agentId', (req, res) => {
  const { agentId } = req.params
  const sessDir = path.join(OC, 'agents', agentId, 'sessions')
  const index   = readJSON(path.join(sessDir, 'sessions.json')) || {}

  // Current active sessions from index
  const current = Object.entries(index).map(([key, s]) => ({
    key,
    sessionId:   s.sessionId,
    file:        path.basename(s.sessionFile || ''),
    updatedAt:   s.updatedAt,
    channel:     s.deliveryContext?.channel || s.lastChannel,
    chatType:    s.chatType,
    origin:      s.origin,
    displayName: s.displayName || s.origin?.label || key,
  })).sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0))

  // All historical files sorted by mtime
  let history = []
  try {
    history = fs.readdirSync(sessDir)
      .filter(f => f.endsWith('.jsonl') && !f.includes('.deleted'))
      .map(f => {
        const stat = fs.statSync(path.join(sessDir, f))
        return { file: f, mtime: stat.mtimeMs, size: stat.size }
      })
      .sort((a, b) => b.mtime - a.mtime)
  } catch {}

  res.json({ current, history })
})

// ─── Session events ───────────────────────────────────────────────────────────
app.get('/api/session/:agentId/:file', (req, res) => {
  const { agentId, file } = req.params
  // Security: only allow .jsonl files, no path traversal
  if (!file.endsWith('.jsonl') || file.includes('/') || file.includes('..')) {
    return res.status(400).json({ error: 'Invalid file' })
  }
  const filePath = path.join(OC, 'agents', agentId, 'sessions', file)
  let events = []
  try {
    const content = fs.readFileSync(filePath, 'utf8')
    events = content.split('\n')
      .filter(l => l.trim())
      .map(l => { try { return JSON.parse(l) } catch { return null } })
      .filter(Boolean)
      .filter(e => !(e.type === 'message' && e.message?.model === 'delivery-mirror'))
  } catch (err) {
    return res.status(404).json({ error: err.message })
  }
  res.json(events)
})

// ─── Live Activity Feed ──────────────────────────────────────────────────────
function getActivityFeed() {
  const now = Date.now()
  const twoHoursAgo = now - 2 * 3600000
  const tenMinAgo = now - 10 * 60 * 1000
  const config = readJSON(path.join(OC, 'openclaw.json'))
  const agentList = config?.agents?.list || []
  const results = []

  for (const agent of agentList) {
    const agentDir = path.join(OC, 'agents', agent.id)
    const sessions = readJSON(path.join(agentDir, 'sessions', 'sessions.json')) || {}

    for (const [key, s] of Object.entries(sessions)) {
      const updatedAt = s.updatedAt || 0
      if (updatedAt < twoHoursAgo) continue

      // Parse session type from key
      let type = 'other'
      if (key.includes('discord:channel:')) type = 'discord'
      else if (key.includes('cron:')) type = 'cron'
      else if (key.includes('subagent')) type = 'subagent'
      else if (key === `agent:${agent.id}:main`) type = 'main'

      // Extract channel / label from key
      const parts = key.split(':')
      const channel = parts[parts.length - 1] || key

      // Read last assistant message from session JSONL (only last 20 lines)
      let lastMessage = ''
      const sessionFile = s.sessionFile || path.join(agentDir, 'sessions', `${s.sessionId}.jsonl`)
      try {
        const content = fs.readFileSync(sessionFile, 'utf8')
        const lines = content.split('\n').filter(Boolean)
        const tail = lines.slice(-20)
        for (let i = tail.length - 1; i >= 0; i--) {
          try {
            const ev = JSON.parse(tail[i])
            if (ev.type === 'message' && ev.message?.role === 'assistant') {
              const textParts = (ev.message.content || []).filter(c => c.type === 'text').map(c => c.text)
              lastMessage = textParts.join(' ').slice(0, 200)
              break
            }
          } catch {}
        }
      } catch {}

      results.push({
        agentId: agent.id,
        agentName: agent.identity?.name || agent.id,
        agentEmoji: agent.identity?.emoji || '🤖',
        sessionKey: key,
        channel,
        type,
        lastMessage,
        updatedAt,
        isActive: updatedAt > tenMinAgo,
      })
    }
  }

  results.sort((a, b) => b.updatedAt - a.updatedAt)
  return results.slice(0, 20)
}

app.get('/api/activity-feed', (_req, res) => {
  res.json(cached('activity-feed', 15000, getActivityFeed))
})

// ─── Main dashboard data ──────────────────────────────────────────────────────
app.get('/api/data', (req, res) => {
  res.json({
    agents:    cached('agents',    15000, getAgentData),
    subagents: cached('subagents', 10000, getSubagentData),
    crons:     cached('crons',     15000, getCronData),
    costs:     cached('costs',    120000, getTokenCosts),
    gateway:   cached('gateway',   30000, getGatewayStatus),
    ts: Date.now(),
  })
})

// ─── Activity pulse (hourly LLM calls per agent, last 24h) ───────────────────
app.get('/api/activity', (_req, res) => {
  res.json(cached('activity', 120000, () => {
    const hours = 24
    const now   = Date.now()
    const since = now - hours * 3600000
    const result = {}

    for (const agentId of getAgentIds()) {
      const sessDir = path.join(OC, 'agents', agentId, 'sessions')
      const counts  = new Array(hours).fill(0)
      let files
      try {
        files = fs.readdirSync(sessDir)
          .filter(f => f.endsWith('.jsonl') && !f.includes('.deleted'))
          .filter(f => { try { return fs.statSync(path.join(sessDir, f)).mtimeMs > since } catch { return false } })
      } catch { result[agentId] = counts; continue }

      for (const file of files) {
        let content
        try { content = fs.readFileSync(path.join(sessDir, file), 'utf8') } catch { continue }
        for (const line of content.split('\n')) {
          if (!line.trim()) continue
          try {
            const ev = JSON.parse(line)
            if (ev.type !== 'message' || ev.message?.role !== 'assistant') continue
            if (ev.message?.model === 'delivery-mirror') continue
            const ts = ev.timestamp ? new Date(ev.timestamp).getTime() : 0
            if (!ts || ts < since) continue
            const idx = Math.floor((ts - since) / 3600000)
            if (idx >= 0 && idx < hours) counts[idx]++
          } catch {}
        }
      }
      result[agentId] = counts
    }

    const labels = Array.from({ length: hours }, (_, i) => {
      const d = new Date(since + i * 3600000)
      return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
    })
    return { labels, agents: result, since }
  }))
})

// ─── Burn rate (cumulative cost timeline, last 24h) ───────────────────────────
app.get('/api/burn-rate', (_req, res) => {
  res.json(cached('burn-rate', 120000, () => {
    const now   = Date.now()
    const since = now - 24 * 3600000
    const points = []

    for (const agentId of getAgentIds()) {
      const sessDir = path.join(OC, 'agents', agentId, 'sessions')
      let files
      try {
        files = fs.readdirSync(sessDir)
          .filter(f => f.endsWith('.jsonl') && !f.includes('.deleted'))
          .filter(f => { try { return fs.statSync(path.join(sessDir, f)).mtimeMs > since } catch { return false } })
      } catch { continue }

      for (const file of files) {
        let content
        try { content = fs.readFileSync(path.join(sessDir, file), 'utf8') } catch { continue }
        for (const line of content.split('\n')) {
          if (!line.trim()) continue
          try {
            const ev = JSON.parse(line)
            if (ev.type !== 'message' || ev.message?.role !== 'assistant') continue
            if (ev.message?.model === 'delivery-mirror') continue
            const u = ev.message?.usage
            if (!u?.cost?.total) continue
            const ts = ev.timestamp ? new Date(ev.timestamp).getTime() : 0
            if (!ts || ts < since) continue
            points.push({ ts, cost: u.cost.total, tokens: u.totalTokens || 0 })
          } catch {}
        }
      }
    }

    points.sort((a, b) => a.ts - b.ts)
    let cum = 0
    const cumPoints = points.map(p => { cum += p.cost; return { ts: p.ts, cost: p.cost, cumCost: cum } })
    const recentCost = points.filter(p => p.ts > now - 2 * 3600000).reduce((s, p) => s + p.cost, 0)
    return { points: cumPoints, ratePerHour: recentCost / 2, totalCost: cum }
  }))
})

// ─── Cron run history (all jobs) ──────────────────────────────────────────────
app.get('/api/cron-history', (_req, res) => {
  res.json(cached('cron-history', 60000, () => {
    const data    = readJSON(path.join(OC, 'cron', 'jobs.json'))
    const runsDir = path.join(OC, 'cron', 'runs')
    const result  = {}
    for (const job of data?.jobs || []) {
      try {
        result[job.id] = fs.readFileSync(path.join(runsDir, `${job.id}.jsonl`), 'utf8')
          .split('\n').filter(Boolean)
          .map(l => { try { const r = JSON.parse(l); return { ts: r.ts || r.runAtMs, status: r.status, durationMs: r.durationMs } } catch { return null } })
          .filter(Boolean)
      } catch { result[job.id] = [] }
    }
    return result
  }))
})

// ─── Log tail ─────────────────────────────────────────────────────────────────
app.get('/api/log', (req, res) => {
  try {
    const content = fs.readFileSync(path.join(OC, 'logs', 'gateway.log'), 'utf8')
    res.json(content.split('\n').filter(Boolean).slice(-300))
  } catch { res.json([]) }
})

// ─── SSE live log ─────────────────────────────────────────────────────────────
app.get('/api/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream')
  res.setHeader('Connection', 'keep-alive')
  res.setHeader('Cache-Control', 'no-cache')
  res.flushHeaders()

  const logPath = path.join(OC, 'logs', 'gateway.log')
  let offset = 0
  try { offset = fs.statSync(logPath).size } catch {}

  const timer = setInterval(() => {
    try {
      const size = fs.statSync(logPath).size
      if (size > offset) {
        const fd  = fs.openSync(logPath, 'r')
        const buf = Buffer.alloc(size - offset)
        fs.readSync(fd, buf, 0, buf.length, offset)
        fs.closeSync(fd)
        offset = size
        buf.toString('utf8').split('\n').filter(Boolean).forEach(line => {
          res.write(`data: ${JSON.stringify(line)}\n\n`)
        })
      }
    } catch {}
  }, 1500)

  req.on('close', () => clearInterval(timer))
})

// ─── Memory browser ───────────────────────────────────────────────────────────
app.get('/api/memory', (_req, res) => {
  const memRoot = path.join(OC, 'workspace', 'memory')
  if (!fs.existsSync(memRoot)) return res.json({ categories: [] })

  function readDir(dir, maxDepth = 2, depth = 0) {
    const result = []
    try {
      for (const entry of fs.readdirSync(dir).sort()) {
        const full = path.join(dir, entry)
        const stat = fs.statSync(full)
        if (stat.isDirectory() && depth < maxDepth) {
          result.push({ name: entry, type: 'dir', children: readDir(full, maxDepth, depth + 1) })
        } else if (entry.endsWith('.md') || entry.endsWith('.txt')) {
          result.push({ name: entry, type: 'file', path: full.replace(memRoot + '/', ''), size: stat.size, mtime: stat.mtimeMs })
        }
      }
    } catch {}
    return result
  }

  const tree = readDir(memRoot)
  res.json({ tree, root: memRoot })
})

app.get('/api/memory/file', (req, res) => {
  const relPath = req.query.path
  if (!relPath) return res.status(400).json({ error: 'missing path' })
  const memRoot = path.join(OC, 'workspace', 'memory')
  const full = path.join(memRoot, relPath)
  // Safety: ensure we stay within memRoot
  if (!full.startsWith(memRoot)) return res.status(403).json({ error: 'forbidden' })
  const content = readText(full)
  if (content === null) return res.status(404).json({ error: 'not found' })
  res.json({ content, path: relPath })
})

// ─── Claude Code session usage ────────────────────────────────────────────────
app.get('/api/claude-code-sessions', (_req, res) => {
  const logPath = path.join(HOME, '.openclaw', 'claude-code-sessions.jsonl')
  if (!fs.existsSync(logPath)) return res.json({ sessions: [], total: 0, totalCost: 0 })

  const lines = fs.readFileSync(logPath, 'utf8').split('\n').filter(Boolean)
  const sessions = lines.map(l => { try { return JSON.parse(l) } catch { return null } }).filter(Boolean)

  // Deduplicate by session_id (keep last entry — hook may fire multiple times)
  const byId = {}
  for (const s of sessions) byId[s.session_id] = s
  const deduped = Object.values(byId).sort((a, b) => new Date(b.ts) - new Date(a.ts))

  const totalCost = deduped.reduce((sum, s) => sum + (s.cost || 0), 0)
  res.json({ sessions: deduped.slice(0, 50), total: deduped.length, totalCost: Math.round(totalCost * 1e6) / 1e6 })
})

// ─── Projects board ──────────────────────────────────────────────────────────
const PROJECTS_FILE = path.join(OC, 'workspace', 'memory', 'projects', 'projects.json')

const DEFAULT_PROJECTS = [
  { id: 'webapp', name: 'Customer Portal', emoji: '🌐', status: 'active', priority: 5, stage: 'Auth system + API integration', nextAction: 'Wire up OAuth providers', updatedAt: new Date().toISOString(), notes: 'React + Next.js' },
  { id: 'mobile', name: 'Mobile App', emoji: '📱', status: 'active', priority: 4, stage: 'UI design phase', nextAction: 'Finalize navigation flow', updatedAt: new Date().toISOString(), notes: 'React Native' },
  { id: 'openclaw-dashboard', name: 'OpenClaw Dashboard', emoji: '🖥️', status: 'active', priority: 3, stage: 'In development', nextAction: 'Continue iterating', updatedAt: new Date().toISOString(), notes: '' },
]

app.get('/api/projects', (_req, res) => {
  const data = readJSON(PROJECTS_FILE)
  res.json(data || DEFAULT_PROJECTS)
})

// ─── SPA fallback ─────────────────────────────────────────────────────────────
app.get('*', (req, res) => {
  const index = path.join(__dirname, 'dist', 'index.html')
  if (fs.existsSync(index)) res.sendFile(index)
  else res.status(404).send('Run `npm run build` first, or use `npm run dev`')
})

app.listen(PORT, '0.0.0.0', () => {
  console.log(`\n🦞 OpenClaw API → http://localhost:${PORT}`)
  console.log(`   Frontend dev → npm run dev  (http://localhost:5173)\n`)
})
