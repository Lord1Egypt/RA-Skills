import { useEffect, useState } from 'react'
import { Line } from 'react-chartjs-2'

const TOOLTIP_OPTS = {
  backgroundColor: '#1c1c1c',
  borderColor: '#2e2e2e',
  borderWidth: 1,
  titleColor: '#e0e0e0',
  bodyColor: '#a0a0a0',
  padding: 8,
  callbacks: {
    label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y} turns`,
  },
}

const SCALE_OPTS = {
  x: {
    grid: { color: '#1a1a1a' },
    ticks: { color: '#505050', maxTicksLimit: 8, font: { size: 10 } },
  },
  y: {
    grid: { color: '#1a1a1a' },
    ticks: { color: '#505050', precision: 0, font: { size: 10 } },
    beginAtZero: true,
  },
}

export default function ActivityPulse() {
  const [data, setData] = useState(null)

  useEffect(() => {
    const load = () =>
      fetch('/api/activity').then(r => r.json()).then(setData).catch(() => {})
    load()
    const t = setInterval(load, 60000)
    return () => clearInterval(t)
  }, [])

  const agentEntries = data ? Object.entries(data.agents || {}) : []
  const isEmpty = !data || agentEntries.every(([, vals]) => vals.every(v => v === 0))

  const COLORS = [
    { border: '#a855f7', bg: 'rgba(168,85,247,0.08)' },
    { border: '#06b6d4', bg: 'rgba(6,182,212,0.08)' },
    { border: '#f59e0b', bg: 'rgba(245,158,11,0.08)' },
    { border: '#10b981', bg: 'rgba(16,185,129,0.08)' },
  ]

  const chartData = {
    labels: data?.labels || [],
    datasets: agentEntries.map(([name, values], i) => ({
      label: name,
      data: values,
      borderColor: COLORS[i % COLORS.length].border,
      backgroundColor: COLORS[i % COLORS.length].bg,
      fill: true, tension: 0.4, pointRadius: 0,
      borderWidth: 1.5,
    })),
  }

  return (
    <div className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-oc-border">
        <span className="text-[10px] uppercase tracking-widest text-oc-muted font-semibold">
          Activity Pulse <span className="text-oc-muted/50 normal-case tracking-normal font-normal">(LLM turns / hour, 24h)</span>
        </span>
        {data && (
          <span className="text-[10px] text-oc-muted">
            {agentEntries.reduce((sum, [, vals]) => sum + vals.reduce((a, b) => a + b, 0), 0)} turns today
          </span>
        )}
      </div>
      <div className="p-4 h-40">
        {!data && (
          <div className="h-full flex items-center justify-center text-oc-muted text-xs animate-pulse">Loading…</div>
        )}
        {data && isEmpty && (
          <div className="h-full flex items-center justify-center text-oc-muted text-xs">No activity in last 24h</div>
        )}
        {data && !isEmpty && (
          <Line
            data={chartData}
            options={{
              responsive: true, maintainAspectRatio: false, animation: false,
              plugins: { legend: { labels: { color: '#606060', boxWidth: 10, padding: 12 } }, tooltip: TOOLTIP_OPTS },
              scales: SCALE_OPTS,
            }}
          />
        )}
      </div>
    </div>
  )
}
