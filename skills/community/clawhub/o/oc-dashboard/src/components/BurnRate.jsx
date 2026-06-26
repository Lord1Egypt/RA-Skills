import { useEffect, useState } from 'react'
import { Line } from 'react-chartjs-2'
import { fmt$, fmtTok } from '../lib/utils.js'

export default function BurnRate() {
  const [data, setData] = useState(null)

  useEffect(() => {
    const load = () =>
      fetch('/api/burn-rate').then(r => r.json()).then(setData).catch(() => {})
    load()
    const t = setInterval(load, 60000)
    return () => clearInterval(t)
  }, [])

  const points  = data?.points || []
  const rate    = data?.ratePerHour || 0
  const total   = data?.totalCost  || 0
  const dailyEst = rate * 24

  // Downsample to max 60 points for chart clarity
  const step    = Math.max(1, Math.floor(points.length / 60))
  const sampled = points.filter((_, i) => i % step === 0 || i === points.length - 1)

  const chartData = {
    labels: sampled.map(p => {
      const d = new Date(p.ts)
      return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
    }),
    datasets: [{
      label: 'Cumulative cost',
      data: sampled.map(p => p.cumCost),
      borderColor: '#f59e0b',
      backgroundColor: 'rgba(245,158,11,0.07)',
      fill: true, tension: 0.3, pointRadius: 0, borderWidth: 1.5,
    }],
  }

  return (
    <div className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-oc-border">
        <span className="text-[10px] uppercase tracking-widest text-oc-muted font-semibold">
          Token Burn Rate <span className="text-oc-muted/50 normal-case tracking-normal font-normal">(24h)</span>
        </span>
        <div className="flex items-center gap-3 text-[11px]">
          {rate > 0 && (
            <span className="text-amber-400 font-semibold">{fmt$(rate)}<span className="text-oc-muted font-normal">/hr</span></span>
          )}
          {dailyEst > 0 && (
            <span className="text-oc-muted">~{fmt$(dailyEst)}/day</span>
          )}
        </div>
      </div>

      {/* Mini stat row */}
      <div className="grid grid-cols-3 border-b border-oc-border text-center">
        <div className="py-2 border-r border-oc-border">
          <div className="text-[10px] text-oc-muted">24h total</div>
          <div className="text-sm font-bold text-amber-400">{fmt$(total)}</div>
        </div>
        <div className="py-2 border-r border-oc-border">
          <div className="text-[10px] text-oc-muted">rate now</div>
          <div className="text-sm font-bold text-amber-300">{rate > 0 ? fmt$(rate) + '/hr' : '—'}</div>
        </div>
        <div className="py-2">
          <div className="text-[10px] text-oc-muted">turns</div>
          <div className="text-sm font-bold text-zinc-300">{points.length}</div>
        </div>
      </div>

      <div className="p-4 h-32">
        {!data && (
          <div className="h-full flex items-center justify-center text-oc-muted text-xs animate-pulse">Loading…</div>
        )}
        {data && points.length === 0 && (
          <div className="h-full flex items-center justify-center text-oc-muted text-xs">No cost data in last 24h</div>
        )}
        {data && points.length > 0 && (
          <Line
            data={chartData}
            options={{
              responsive: true, maintainAspectRatio: false, animation: false,
              plugins: {
                legend: { display: false },
                tooltip: {
                  backgroundColor: '#1c1c1c', borderColor: '#2e2e2e', borderWidth: 1,
                  titleColor: '#e0e0e0', bodyColor: '#a0a0a0', padding: 8,
                  callbacks: { label: ctx => ` cumulative: ${fmt$(ctx.parsed.y)}` },
                },
              },
              scales: {
                x: { grid: { color: '#1a1a1a' }, ticks: { color: '#505050', maxTicksLimit: 6, font: { size: 10 } } },
                y: {
                  grid: { color: '#1a1a1a' }, ticks: { color: '#505050', font: { size: 10 },
                    callback: v => fmt$(v),
                  },
                  beginAtZero: true,
                },
              },
            }}
          />
        )}
      </div>
    </div>
  )
}
