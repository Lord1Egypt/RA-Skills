import { useEffect, useState } from 'react'
import { fmt$, fmtTok, timeAgo } from '../lib/utils.js'

function projectLabel(cwd) {
  if (!cwd) return '—'
  const parts = cwd.split('/')
  return parts[parts.length - 1] || cwd
}

function modelShortLocal(m) {
  return (m || '').replace('claude-', '').replace(/-\d{8}$/, '')
}

export default function ClaudeCodeUsage() {
  const [data, setData] = useState(null)

  useEffect(() => {
    const load = () =>
      fetch('/api/claude-code-sessions').then(r => r.json()).then(setData).catch(() => {})
    load()
    const t = setInterval(load, 30000)
    return () => clearInterval(t)
  }, [])

  const sessions = data?.sessions || []
  const totalCost = data?.totalCost || 0

  return (
    <div className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-oc-border">
        <span className="text-[10px] uppercase tracking-widest text-oc-muted font-semibold">
          Claude Code Sessions
          <span className="text-oc-muted/50 normal-case tracking-normal font-normal ml-1">(my own usage)</span>
        </span>
        <div className="flex items-center gap-3 text-[11px]">
          {data && (
            <>
              <span className="text-oc-muted">{data.total} sessions</span>
              <span className="text-violet-400 font-semibold">{fmt$(totalCost)} total</span>
            </>
          )}
        </div>
      </div>

      {!data && (
        <div className="p-6 text-center text-oc-muted text-xs animate-pulse">Loading…</div>
      )}

      {data && sessions.length === 0 && (
        <div className="p-6 text-center text-oc-muted text-xs">
          No sessions recorded yet. Session data is written when a Claude Code session ends.
        </div>
      )}

      {data && sessions.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-[11px]">
            <thead>
              <tr className="border-b border-oc-border text-oc-muted text-[10px] uppercase tracking-wider">
                <th className="text-left px-4 py-2 font-normal">Session</th>
                <th className="text-left px-4 py-2 font-normal hidden sm:table-cell">Project</th>
                <th className="text-right px-4 py-2 font-normal">Turns</th>
                <th className="text-right px-4 py-2 font-normal">Tokens</th>
                <th className="text-right px-4 py-2 font-normal">Cost</th>
                <th className="text-right px-4 py-2 font-normal hidden md:table-cell">When</th>
              </tr>
            </thead>
            <tbody>
              {sessions.map(s => {
                const totalTok = (s.input_tokens || 0) + (s.output_tokens || 0) +
                                 (s.cache_creation_input_tokens || 0) + (s.cache_read_input_tokens || 0)
                return (
                  <tr key={s.session_id} className="border-b border-oc-border/50 hover:bg-oc-s3/30 transition-colors">
                    <td className="px-4 py-2">
                      <div className="flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-violet-500 flex-shrink-0" />
                        <span className="text-oc-text truncate max-w-[140px]" title={s.slug || s.session_id}>
                          {s.slug || s.session_id.slice(0, 8)}
                        </span>
                      </div>
                      <div className="text-[9px] text-oc-muted/60 pl-3.5">{modelShortLocal(s.model)}</div>
                    </td>
                    <td className="px-4 py-2 hidden sm:table-cell">
                      <span className="text-oc-muted truncate max-w-[100px] block" title={s.cwd}>
                        {projectLabel(s.cwd)}
                      </span>
                    </td>
                    <td className="px-4 py-2 text-right text-zinc-300">{s.turns}</td>
                    <td className="px-4 py-2 text-right">
                      <span className="text-zinc-300">{fmtTok(totalTok)}</span>
                      {s.cache_read_input_tokens > 0 && (
                        <div className="text-[9px] text-emerald-600/70">
                          {fmtTok(s.cache_read_input_tokens)} cached
                        </div>
                      )}
                    </td>
                    <td className="px-4 py-2 text-right">
                      <span className={`font-semibold ${s.cost > 5 ? 'text-red-400' : s.cost > 1 ? 'text-amber-400' : 'text-emerald-400'}`}>
                        {fmt$(s.cost)}
                      </span>
                    </td>
                    <td className="px-4 py-2 text-right text-oc-muted hidden md:table-cell">
                      {timeAgo(s.ts)}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
