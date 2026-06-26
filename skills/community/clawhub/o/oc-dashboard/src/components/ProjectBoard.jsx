import { useState, useEffect } from 'react'

const COLUMNS = [
  { key: 'active',  label: 'Active',  icon: '🔥' },
  { key: 'blocked', label: 'Blocked', icon: '🔴' },
  { key: 'paused',  label: 'Paused',  icon: '⏸' },
  { key: 'done',    label: 'Done',    icon: '✅' },
]

function timeAgoISO(iso) {
  if (!iso) return '—'
  const diff = Date.now() - new Date(iso).getTime()
  const s = Math.floor(diff / 1000)
  const m = Math.floor(s / 60)
  const h = Math.floor(m / 60)
  const d = Math.floor(h / 24)
  if (d > 0) return d + 'd ago'
  if (h > 0) return h + 'h ago'
  if (m > 0) return m + 'm ago'
  return 'just now'
}

function Stars({ count }) {
  return (
    <span className="text-amber-400 text-[10px] tracking-tight">
      {'★'.repeat(count)}
      <span className="text-oc-muted">{'★'.repeat(5 - count)}</span>
    </span>
  )
}

function ProjectCard({ project }) {
  return (
    <div className="bg-oc-s2 border border-oc-border rounded-lg p-3 hover:border-violet-800 transition-colors">
      <div className="flex items-start justify-between gap-2 mb-1.5">
        <span className="text-sm font-semibold text-oc-text leading-tight">
          {project.emoji} {project.name}
        </span>
        <Stars count={project.priority} />
      </div>

      <p className="text-[11px] text-zinc-400 mb-1.5 leading-snug">{project.stage}</p>

      <div className="flex items-start gap-1.5 mb-2">
        <span className="text-[10px] text-cyan-500 shrink-0 mt-px">Next →</span>
        <span className="text-[11px] text-zinc-300 leading-snug">{project.nextAction}</span>
      </div>

      <div className="flex items-center justify-between text-[10px] text-oc-muted">
        <span>{timeAgoISO(project.updatedAt)}</span>
        {project.notes && (
          <span className="truncate max-w-[60%] text-right" title={project.notes}>
            {project.notes}
          </span>
        )}
      </div>
    </div>
  )
}

export default function ProjectBoard() {
  const [projects, setProjects] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/projects')
      .then(r => r.json())
      .then(data => { setProjects(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  const filtered = projects.filter(p => {
    if (!search) return true
    const q = search.toLowerCase()
    return p.name.toLowerCase().includes(q)
      || p.stage.toLowerCase().includes(q)
      || p.nextAction.toLowerCase().includes(q)
      || (p.notes || '').toLowerCase().includes(q)
  })

  const grouped = {}
  for (const col of COLUMNS) grouped[col.key] = []
  for (const p of filtered) {
    if (grouped[p.status]) grouped[p.status].push(p)
  }
  // Sort active by priority desc
  grouped.active.sort((a, b) => b.priority - a.priority)

  if (loading) {
    return (
      <section>
        <div className="text-[10px] text-oc-muted uppercase tracking-widest mb-3 px-0.5">Project Board</div>
        <div className="bg-oc-surface border border-oc-border rounded-lg p-6 text-center text-oc-muted text-xs">
          Loading...
        </div>
      </section>
    )
  }

  return (
    <section>
      <div className="flex items-center justify-between mb-3 px-0.5">
        <div className="text-[10px] text-oc-muted uppercase tracking-widest">Project Board</div>
        <input
          type="text"
          placeholder="Search projects..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="bg-oc-s2 border border-oc-border rounded px-2 py-1 text-[11px] text-oc-text placeholder:text-oc-muted focus:outline-none focus:border-violet-700 w-48 font-mono"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        {COLUMNS.map(col => {
          const items = grouped[col.key]
          return (
            <div key={col.key} className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden">
              <div className="flex items-center justify-between px-3 py-2 bg-oc-s2 border-b border-oc-border">
                <span className="text-[11px] font-semibold text-oc-text">
                  {col.icon} {col.label}
                </span>
                <span className="text-[10px] text-oc-muted">{items.length}</span>
              </div>
              <div className="p-2 flex flex-col gap-2 min-h-[80px]">
                {items.length === 0 ? (
                  <div className="text-[11px] text-oc-muted italic text-center py-4">No projects</div>
                ) : (
                  items.map(p => <ProjectCard key={p.id} project={p} />)
                )}
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}
