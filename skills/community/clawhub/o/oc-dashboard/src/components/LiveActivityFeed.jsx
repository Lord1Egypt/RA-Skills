import { useEffect, useState } from 'react'
import { timeAgo } from '../lib/utils.js'

const TYPE_LABELS = {
  discord:  '💬 discord',
  cron:     '⏰ cron',
  subagent: '🤖 subagent',
  main:     '🌐 webchat',
  other:    '📡 session',
}

export default function LiveActivityFeed() {
  const [items, setItems] = useState(null)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    const load = () =>
      fetch('/api/activity-feed').then(r => r.json()).then(setItems).catch(() => {})
    load()
    const t = setInterval(load, 15000)
    return () => clearInterval(t)
  }, [])

  const allItems = items || []
  const agents = [...new Set(allItems.map(i => i.agentId))]
  const filtered = filter === 'all' ? allItems : allItems.filter(i => i.agentId === filter)

  return (
    <section>
      <div className="flex items-center justify-between mb-3 px-0.5">
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-oc-muted uppercase tracking-widest">
            Live Activity Feed
          </span>
          {items && (
            <span className="text-[10px] text-oc-muted/60">{filtered.length} items</span>
          )}
        </div>
        {agents.length > 1 && (
          <select
            value={filter}
            onChange={e => setFilter(e.target.value)}
            className="bg-oc-s2 border border-oc-border rounded px-2 py-1 text-[11px] text-oc-text focus:outline-none focus:border-violet-700 font-mono"
          >
            <option value="all">All agents</option>
            {agents.map(id => {
              const item = allItems.find(i => i.agentId === id)
              return (
                <option key={id} value={id}>
                  {item?.agentEmoji} {item?.agentName || id}
                </option>
              )
            })}
          </select>
        )}
      </div>

      <div className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden">
        {!items && (
          <div className="p-6 text-center text-oc-muted text-xs animate-pulse">Loading…</div>
        )}

        {items && filtered.length === 0 && (
          <div className="p-6 text-center text-oc-muted text-xs">
            No activity in the last 2 hours
          </div>
        )}

        {items && filtered.length > 0 && (
          <div className="divide-y divide-oc-border/50">
            {filtered.map((item, idx) => (
              <div
                key={item.sessionKey + idx}
                className="px-4 py-2.5 hover:bg-oc-s3/30 transition-colors"
              >
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2 text-[12px] min-w-0">
                    <span className="flex-shrink-0">{item.agentEmoji}</span>
                    <span className="font-semibold text-oc-text truncate">{item.agentName}</span>
                    <span className="text-oc-muted">·</span>
                    <span className="text-oc-muted truncate text-[11px]">
                      {TYPE_LABELS[item.type] || item.type}:{item.channel}
                    </span>
                    <span className="text-oc-muted">·</span>
                    <span className="text-oc-muted text-[11px] flex-shrink-0">{timeAgo(item.updatedAt)}</span>
                  </div>
                  <span className="flex-shrink-0 ml-2">
                    {item.isActive ? (
                      <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block animate-pulse-dot" />
                    ) : (
                      <span className="w-2 h-2 rounded-full bg-zinc-600 inline-block" />
                    )}
                  </span>
                </div>
                {item.lastMessage && (
                  <p className="text-[11px] text-zinc-400 truncate pl-6">
                    "{item.lastMessage}"
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}
