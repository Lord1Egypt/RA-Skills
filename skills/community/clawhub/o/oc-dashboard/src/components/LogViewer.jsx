import { useState, useEffect, useRef } from 'react'

function lineClass(line) {
  if (line.includes('[discord]'))                      return 'text-blue-400'
  if (line.includes('[ws]'))                           return 'text-emerald-400'
  if (line.includes('[warn]'))                         return 'text-amber-400'
  if (line.includes('[error]') || /error/i.test(line)) return 'text-red-400'
  if (line.includes('[browser'))                       return 'text-purple-400'
  if (line.includes('[gateway]'))                      return 'text-cyan-400'
  return 'text-zinc-500'
}

export default function LogViewer() {
  const [lines, setLines]     = useState([])
  const [filter, setFilter]   = useState('')
  const [sseOk, setSseOk]     = useState(true)
  const [pinned, setPinned]   = useState(true)
  const containerRef          = useRef(null)

  // Initial load
  useEffect(() => {
    fetch('/api/log').then(r => r.json()).then(data => {
      setLines(data.slice(-200))
    }).catch(() => {})
  }, [])

  // SSE live tail
  useEffect(() => {
    const es = new EventSource('/api/events')
    es.onmessage = e => {
      const line = JSON.parse(e.data)
      setLines(prev => {
        const next = [...prev, line]
        return next.length > 500 ? next.slice(-500) : next
      })
    }
    es.onerror = () => setSseOk(false)
    return () => es.close()
  }, [])

  // Auto-scroll
  useEffect(() => {
    if (pinned && containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [lines, pinned])

  const filtered = filter
    ? lines.filter(l => l.toLowerCase().includes(filter.toLowerCase()))
    : lines

  return (
    <div className="bg-[#080808] border border-oc-border rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 bg-oc-surface border-b border-oc-border">
        <div className="flex items-center gap-2">
          <span className="text-[10px] uppercase tracking-widest text-oc-muted font-semibold">Live Gateway Log</span>
          <span className={`w-1.5 h-1.5 rounded-full ${sseOk ? 'bg-emerald-400 animate-pulse-dot' : 'bg-red-400'}`} />
        </div>
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="filter…"
            value={filter}
            onChange={e => setFilter(e.target.value)}
            className="bg-oc-s2 border border-oc-border text-oc-text text-[11px] px-2 py-1 rounded w-44 outline-none focus:border-violet-700 font-mono"
          />
          <button
            onClick={() => setPinned(p => !p)}
            className={`text-[10px] px-2 py-1 rounded border transition-colors ${
              pinned
                ? 'text-violet-400 bg-violet-950 border-violet-800'
                : 'text-oc-muted bg-oc-s2 border-oc-border hover:border-oc-muted'
            }`}
          >
            {pinned ? '⬇ auto' : '⏸ paused'}
          </button>
        </div>
      </div>
      <div ref={containerRef} className="h-64 overflow-y-auto p-3 space-y-0.5">
        {filtered.map((line, i) => (
          <div key={i} className={`text-[11.5px] font-mono whitespace-pre-wrap break-all leading-5 ${lineClass(line)}`}>
            {line}
          </div>
        ))}
      </div>
    </div>
  )
}
