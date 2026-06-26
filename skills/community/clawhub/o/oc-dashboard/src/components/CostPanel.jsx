import { fmt$, fmtTok, modelShort } from '../lib/utils.js'

export default function CostPanel({ costs }) {
  const { byModel = {}, byDay = {} } = costs

  const models   = Object.entries(byModel).sort((a, b) => b[1].cost - a[1].cost)
  const today    = new Date().toISOString().slice(0, 10)
  const days     = Array.from({ length: 14 }, (_, i) => {
    const d = new Date(); d.setDate(d.getDate() - (13 - i))
    return d.toISOString().slice(0, 10)
  }).filter(d => byDay[d]?.cost)
  const maxCost  = Math.max(...days.map(d => byDay[d]?.cost || 0), 0.001)

  return (
    <div className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden">
      <div className="px-4 py-2.5 border-b border-oc-border">
        <span className="text-[10px] uppercase tracking-widest text-oc-muted font-semibold">Token & Cost Breakdown</span>
      </div>
      <div className="p-4 grid grid-cols-2 gap-6">

        {/* By model */}
        <div>
          <div className="text-[10px] uppercase tracking-wider text-oc-muted mb-3">By Model (30d)</div>
          {models.length === 0 ? (
            <div className="text-oc-muted text-[12px] text-center py-4">No data</div>
          ) : (
            <div className="space-y-1.5">
              {models.map(([model, v]) => (
                <div key={model} className="flex items-center justify-between bg-oc-s2 px-3 py-2 rounded text-[12px]">
                  <span className="text-oc-muted">{modelShort(model)}</span>
                  <div className="text-right">
                    <div className="text-cyan-400 font-semibold">{fmt$(v.cost)}</div>
                    <div className="text-[10px] text-oc-muted">{fmtTok(v.tokens)}tok</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* By day */}
        <div>
          <div className="text-[10px] uppercase tracking-wider text-oc-muted mb-3">Daily Spend (14d)</div>
          {days.length === 0 ? (
            <div className="text-oc-muted text-[12px] text-center py-4">No data</div>
          ) : (
            <div className="space-y-2">
              {days.map(d => {
                const v    = byDay[d] || { cost: 0 }
                const pct  = Math.round((v.cost / maxCost) * 100)
                const label = d === today ? 'Today' : d.slice(5)
                return (
                  <div key={d}>
                    <div className="flex justify-between text-[11px] mb-0.5">
                      <span className="text-oc-muted">{label}</span>
                      <span className="text-cyan-400">{fmt$(v.cost)}</span>
                    </div>
                    <div className="h-1.5 bg-oc-s3 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-violet-600 rounded-full transition-all duration-500"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
