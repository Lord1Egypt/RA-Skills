import { timeAgo } from '../lib/utils.js'

export default function Header({ gateway, lastFetch, onRefresh, page, onNav }) {
  const statusColor = {
    online:  'text-emerald-400 bg-emerald-950 border-emerald-800',
    stale:   'text-amber-400 bg-amber-950 border-amber-800',
    offline: 'text-red-400 bg-red-950 border-red-800',
  }[gateway?.status || 'offline'] || 'text-zinc-400 bg-zinc-900 border-zinc-700'

  return (
    <header className="sticky top-0 z-50 flex items-center justify-between px-4 py-2.5 bg-oc-surface border-b border-oc-border">
      <div className="flex items-center gap-3">
        <span className="text-sm font-semibold tracking-wide">
          🦞 <span className="text-violet-400">OpenClaw</span> Control Tower
        </span>
        {gateway?.version && (
          <span className="text-[10px] text-violet-400 bg-violet-950 border border-violet-800 px-1.5 py-0.5 rounded">
            v{gateway.version}
          </span>
        )}
      </div>

      <nav className="flex items-center gap-1">
        <button
          onClick={() => onNav('dashboard')}
          className={`text-[11px] px-3 py-1 rounded transition-colors ${
            page === 'dashboard'
              ? 'bg-violet-900 text-violet-200 border border-violet-700'
              : 'text-oc-muted hover:text-oc-text hover:bg-oc-s2'
          }`}
        >
          Dashboard
        </button>
        <button
          onClick={() => onNav('replay')}
          className={`text-[11px] px-3 py-1 rounded transition-colors ${
            page === 'replay'
              ? 'bg-violet-900 text-violet-200 border border-violet-700'
              : 'text-oc-muted hover:text-oc-text hover:bg-oc-s2'
          }`}
        >
          Session Replay
        </button>
      </nav>

      <div className="flex items-center gap-3 text-[11px]">
        {gateway?.status && (
          <span className={`flex items-center gap-1.5 px-2 py-0.5 rounded border text-[10px] font-medium ${statusColor}`}>
            <span className={`w-1.5 h-1.5 rounded-full bg-current ${gateway.status === 'online' ? 'animate-pulse-dot' : ''}`} />
            {gateway.status.charAt(0).toUpperCase() + gateway.status.slice(1)}
          </span>
        )}
        {lastFetch && (
          <span className="text-oc-muted">{timeAgo(lastFetch)}</span>
        )}
        <button
          onClick={onRefresh}
          className="text-oc-muted hover:text-oc-text transition-colors px-1.5 py-0.5 rounded hover:bg-oc-s2"
          title="Refresh"
        >
          ↻
        </button>
      </div>
    </header>
  )
}
