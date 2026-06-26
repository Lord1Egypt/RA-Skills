import { timeAgo, fmtDur, cronHuman, countdown } from '../lib/utils.js'

export default function CronTable({ crons }) {
  const errCount = crons.filter(c => c.consecutiveErrors > 0).length

  return (
    <div className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-oc-border">
        <span className="text-[10px] uppercase tracking-widest text-oc-muted font-semibold">Scheduled Jobs</span>
        {errCount > 0 && (
          <span className="text-[11px] text-amber-400">⚠ {errCount} job{errCount > 1 ? 's' : ''} with errors</span>
        )}
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-[12px]">
          <thead>
            <tr className="border-b border-oc-border">
              {['Job', 'Schedule', 'Last Run', 'Status', 'Next Run', 'Errors'].map(h => (
                <th key={h} className="text-left px-3 py-2 text-[10px] uppercase tracking-wider text-oc-muted font-medium">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {crons.map(job => (
              <tr
                key={job.id}
                className={`border-b border-oc-border/50 hover:bg-oc-s2 transition-colors ${!job.enabled ? 'opacity-40' : ''}`}
              >
                <td className="px-3 py-2.5">
                  <div className="font-medium">{job.name}</div>
                  {job.consecutiveErrors > 0 && job.lastError && (
                    <div className="text-red-400 text-[10px] mt-0.5 truncate max-w-xs" title={job.lastError}>
                      {job.lastError.slice(0, 70)}
                    </div>
                  )}
                </td>
                <td className="px-3 py-2.5 text-oc-muted">{cronHuman(job.schedule)}</td>
                <td className="px-3 py-2.5 text-oc-muted">
                  {job.lastRunAtMs ? timeAgo(job.lastRunAtMs) : '—'}
                  {job.lastDurationMs ? (
                    <span className="text-[10px] ml-1 opacity-60">({fmtDur(job.lastDurationMs)})</span>
                  ) : null}
                </td>
                <td className="px-3 py-2.5">
                  {!job.lastStatus ? (
                    <span className="text-oc-muted">—</span>
                  ) : job.lastStatus === 'ok' ? (
                    <span className="text-[10px] text-emerald-400 bg-emerald-950 border border-emerald-800 px-1.5 py-0.5 rounded">OK</span>
                  ) : (
                    <span className="text-[10px] text-red-400 bg-red-950 border border-red-800 px-1.5 py-0.5 rounded">ERR</span>
                  )}
                </td>
                <td className="px-3 py-2.5 text-blue-400">
                  {job.enabled ? countdown(job.nextRunAtMs) : <span className="text-oc-muted">disabled</span>}
                </td>
                <td className="px-3 py-2.5">
                  {job.consecutiveErrors > 0 ? (
                    <span className="text-red-400 font-bold">{job.consecutiveErrors}</span>
                  ) : ''}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
