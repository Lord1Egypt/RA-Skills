import { fmt$, fmtTok, countdown } from '../lib/utils.js'

function Stat({ label, value, sub, valueClass = 'text-zinc-100' }) {
  return (
    <div className="bg-oc-surface px-4 py-3 flex flex-col gap-1">
      <div className="text-[10px] text-oc-muted uppercase tracking-widest">{label}</div>
      <div className={`text-2xl font-bold leading-none ${valueClass}`}>{value}</div>
      {sub && <div className="text-[11px] text-oc-muted">{sub}</div>}
    </div>
  )
}

export default function StatBar({ data }) {
  const { agents = [], subagents = {}, crons = [], costs = {} } = data
  const activeAgents = agents.filter(a => a.status === 'active').length
  const activeSA     = (subagents.active || []).length
  const recentSA     = (subagents.recent || []).length
  const errCrons     = crons.filter(c => c.consecutiveErrors > 0).length
  const upcoming     = crons.filter(c => c.enabled && c.nextRunAtMs).sort((a, b) => a.nextRunAtMs - b.nextRunAtMs)[0]

  return (
    <div className="grid grid-cols-3 lg:grid-cols-6 border-b border-oc-border" style={{ gap: '1px', background: 'var(--tw-border-color, #2e2e2e)' }}>
      <Stat
        label="Agents"
        value={agents.length}
        sub={activeAgents ? `${activeAgents} active` : 'all idle'}
        valueClass="text-violet-400"
      />
      <Stat
        label="Sub-agents"
        value={activeSA}
        sub={`${recentSA} in 48h`}
        valueClass="text-cyan-400"
      />
      <Stat
        label="Cron Jobs"
        value={crons.length}
        sub={errCrons ? `⚠ ${errCrons} errors` : 'all OK'}
        valueClass={errCrons ? 'text-amber-400' : 'text-blue-400'}
      />
      <Stat
        label="Cost Today"
        value={fmt$(costs.today?.cost)}
        sub={fmtTok(costs.today?.tokens) + ' tokens'}
        valueClass="text-emerald-400"
      />
      <Stat
        label="Cost (30d)"
        value={fmt$(costs.total?.cost)}
        sub={fmtTok(costs.total?.tokens) + ' tokens'}
        valueClass="text-amber-400"
      />
      <Stat
        label="Next Cron"
        value={upcoming ? countdown(upcoming.nextRunAtMs) : '—'}
        sub={upcoming?.name || ''}
        valueClass="text-blue-400"
      />
    </div>
  )
}
