import { timeAgo, fmtDur } from '../lib/utils.js'

function SubagentItem({ run, isActive }) {
  const statusColor = run.status === 'ok' ? 'text-emerald-400' : run.status === 'error' ? 'text-red-400' : 'text-zinc-400'
  const icon = isActive ? '🟢' : run.status === 'ok' ? '✓' : run.status === 'error' ? '✗' : '?'

  return (
    <div className={`p-3 rounded-md bg-oc-s2 text-[12px] ${isActive ? 'border-l-2 border-emerald-500' : ''}`}>
      <div className="font-medium mb-1">
        <span className={statusColor}>{icon}</span>{' '}
        {run.label}
      </div>
      {run.task && (
        <div className="text-oc-muted truncate mb-1.5">{run.task}</div>
      )}
      <div className="flex gap-3 text-[11px] text-oc-muted flex-wrap">
        {run.model && <span>model: {run.model}</span>}
        {isActive
          ? <span>started {timeAgo(run.startedAt)}</span>
          : <span>{timeAgo(run.endedAt)}</span>
        }
        {run.durationMs > 0 && <span>{fmtDur(run.durationMs)}</span>}
      </div>
    </div>
  )
}

export default function SubagentPanel({ subagents }) {
  const { active = [], recent = [] } = subagents

  return (
    <div className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden flex flex-col">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-oc-border">
        <span className="text-[10px] uppercase tracking-widest text-oc-muted font-semibold">Sub-agents</span>
        {active.length > 0 && (
          <span className="flex items-center gap-1.5 text-[10px] text-emerald-400 bg-emerald-950 border border-emerald-800 px-2 py-0.5 rounded">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse-dot" />
            {active.length} running
          </span>
        )}
      </div>
      <div className="p-3 flex flex-col gap-2 overflow-y-auto max-h-64">
        {active.length === 0 && recent.length === 0 ? (
          <div className="text-center text-oc-muted text-[12px] py-6">No sub-agents in the last 48h</div>
        ) : (
          <>
            {active.map(r => <SubagentItem key={r.runId} run={r} isActive />)}
            {recent.map(r => <SubagentItem key={r.runId} run={r} isActive={false} />)}
          </>
        )}
      </div>
    </div>
  )
}
