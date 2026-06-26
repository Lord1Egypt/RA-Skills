import { useEffect, useState } from 'react'

const DAYS = 35  // ~5 weeks

function getDateGrid() {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return Array.from({ length: DAYS }, (_, i) => {
    const d = new Date(today)
    d.setDate(d.getDate() - (DAYS - 1 - i))
    return d.toISOString().slice(0, 10)
  })
}

function buildDayMap(runs) {
  // {date: {status: 'ok'|'error', count: N}}
  const map = {}
  for (const r of runs) {
    if (!r.ts) continue
    const day = new Date(r.ts).toISOString().slice(0, 10)
    if (!map[day]) map[day] = { status: r.status, count: 0 }
    map[day].count++
    if (r.status === 'error') map[day].status = 'error' // any error taints the day
  }
  return map
}

function Cell({ day, entry, jobName }) {
  const today = new Date().toISOString().slice(0, 10)
  const isToday = day === today
  let bg = 'bg-oc-s3'
  let title = `${day}: no run`
  if (entry) {
    bg = entry.status === 'ok' ? 'bg-emerald-700' : 'bg-red-700'
    title = `${day}: ${entry.count} run${entry.count > 1 ? 's' : ''} — ${entry.status}`
    if (entry.status === 'error') bg = 'bg-red-600'
    else if (entry.count >= 3) bg = 'bg-emerald-500'
  }

  return (
    <div
      className={`w-3 h-3 rounded-sm ${bg} ${isToday ? 'ring-1 ring-violet-500' : ''} transition-all`}
      title={title}
    />
  )
}

export default function CronHeatmap({ crons }) {
  const [history, setHistory] = useState({})
  const [expanded, setExpanded] = useState(false)

  useEffect(() => {
    fetch('/api/cron-history')
      .then(r => r.json())
      .then(setHistory)
      .catch(() => {})
  }, [])

  const dateGrid = getDateGrid()
  // Show week labels (Mon of each week)
  const weekLabels = dateGrid.filter((_, i) => {
    const d = new Date(_ + 'T00:00:00')
    return d.getDay() === 1 || i === 0
  })

  const visibleCrons = expanded ? crons : crons.slice(0, 6)

  return (
    <div className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-oc-border">
        <span className="text-[10px] uppercase tracking-widest text-oc-muted font-semibold">
          Cron Run History <span className="text-oc-muted/50 normal-case tracking-normal font-normal">(35 days)</span>
        </span>
        <div className="flex items-center gap-3 text-[10px] text-oc-muted">
          <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-sm bg-emerald-600 inline-block" /> ok</span>
          <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-sm bg-red-600 inline-block" /> error</span>
          <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-sm bg-oc-s3 inline-block" /> no run</span>
        </div>
      </div>

      <div className="px-4 pt-3 pb-1 overflow-x-auto">
        {/* Date axis */}
        <div className="flex items-center mb-2 pl-36">
          <div className="flex gap-1">
            {dateGrid.map((day, i) => {
              const d = new Date(day + 'T00:00:00')
              const isMonday = d.getDay() === 1
              return (
                <div key={day} className="w-3 text-center">
                  {isMonday && (
                    <span className="text-[8px] text-oc-muted leading-none">
                      {d.getMonth() + 1}/{d.getDate()}
                    </span>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Job rows */}
        <div className="space-y-1.5">
          {visibleCrons.map(job => {
            const runs   = history[job.id] || []
            const dayMap = buildDayMap(runs)
            const errDays = Object.values(dayMap).filter(d => d.status === 'error').length
            const okDays  = Object.values(dayMap).filter(d => d.status === 'ok').length

            return (
              <div key={job.id} className="flex items-center gap-2">
                {/* Job name */}
                <div className="w-36 flex-shrink-0 flex items-center gap-1.5">
                  <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${
                    job.consecutiveErrors > 0 ? 'bg-red-500' : job.lastStatus === 'ok' ? 'bg-emerald-500' : 'bg-oc-muted'
                  }`} />
                  <span className="text-[10px] text-oc-muted truncate" title={job.name}>{job.name}</span>
                </div>
                {/* Cells */}
                <div className="flex gap-1">
                  {dateGrid.map(day => (
                    <Cell key={day} day={day} entry={dayMap[day]} jobName={job.name} />
                  ))}
                </div>
                {/* Stats */}
                <div className="text-[10px] text-oc-muted ml-1 flex-shrink-0">
                  {okDays > 0 && <span className="text-emerald-600">{okDays}✓</span>}
                  {errDays > 0 && <span className="text-red-500 ml-1">{errDays}✗</span>}
                </div>
              </div>
            )
          })}
        </div>

        {/* Show more */}
        {crons.length > 6 && (
          <button
            onClick={() => setExpanded(e => !e)}
            className="mt-3 text-[10px] text-oc-muted hover:text-oc-text transition-colors"
          >
            {expanded ? '▲ Show less' : `▼ Show all ${crons.length} jobs`}
          </button>
        )}
      </div>
      <div className="h-3" />
    </div>
  )
}
