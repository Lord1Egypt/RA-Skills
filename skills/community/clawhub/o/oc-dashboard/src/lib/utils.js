export function fmt$(n) {
  if (!n || n === 0) return '$0.00'
  if (n < 0.01) return '<$0.01'
  if (n < 1) return '$' + n.toFixed(3)
  return '$' + n.toFixed(2)
}

export function fmtTok(n) {
  if (!n) return '0'
  if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(0) + 'k'
  return String(n)
}

export function timeAgo(ms) {
  if (!ms) return '—'
  const diff = Date.now() - ms
  const s = Math.floor(diff / 1000)
  const m = Math.floor(s / 60)
  const h = Math.floor(m / 60)
  const d = Math.floor(h / 24)
  if (d > 0) return d + 'd ago'
  if (h > 0) return h + 'h ago'
  if (m > 0) return m + 'm ago'
  if (s > 5) return s + 's ago'
  return 'just now'
}

export function countdown(ms) {
  if (!ms) return '—'
  const diff = ms - Date.now()
  if (diff < 0) return 'overdue'
  const m = Math.floor(diff / 60000)
  const h = Math.floor(m / 60)
  if (h > 0) return `in ${h}h ${m % 60}m`
  return `in ${m}m`
}

export function fmtDur(ms) {
  if (!ms) return ''
  if (ms < 1000) return ms + 'ms'
  return (ms / 1000).toFixed(1) + 's'
}

export function fmtTime(isoOrMs) {
  if (!isoOrMs) return ''
  const d = new Date(isoOrMs)
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })
}

export function cronHuman(sched) {
  if (!sched) return ''
  if (sched.kind === 'every') {
    const h = Math.floor(sched.everyMs / 3600000)
    const m = Math.floor((sched.everyMs % 3600000) / 60000)
    if (h && m) return `every ${h}h ${m}m`
    if (h) return `every ${h}h`
    return `every ${m}m`
  }
  const map = {
    '30 5 * * *':   '05:30 daily',
    '0 7 * * *':    '07:00 daily',
    '0 8 * * 1-5':  '08:00 weekdays',
    '0 21 * * *':   '21:00 daily',
    '30 22 * * *':  '22:30 daily',
    '0 4 * * *':    '04:00 daily',
    '0 20 * * 0':   'Sun 20:00',
    '0 12 1 * *':   '1st/month 12:00',
  }
  return map[sched.expr] || sched.expr || ''
}

export function modelShort(m) {
  if (!m) return ''
  const str = typeof m === 'object' ? (m.primary || m.id || Object.values(m)[0] || '') : String(m)
  return str.replace('anthropic/', '').replace('claude-', '').replace(/-\d{8}$/, '')
}

export const TOOL_ICONS = {
  read:    '📖',
  write:   '✍️',
  edit:    '📝',
  exec:    '💻',
  bash:    '💻',
  browser: '🌐',
  search:  '🔍',
  memory:  '🧠',
  subagent:'🤖',
  glob:    '🗂️',
  grep:    '🔎',
  default: '🔧',
}

export function toolIcon(name) {
  if (!name) return TOOL_ICONS.default
  const key = Object.keys(TOOL_ICONS).find(k => name.toLowerCase().includes(k))
  return key ? TOOL_ICONS[key] : TOOL_ICONS.default
}
