import { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'

function FileIcon({ name }) {
  if (name.includes('daily') || /\d{4}-\d{2}-\d{2}/.test(name)) return <span>📅</span>
  if (name.includes('soul') || name.includes('SOUL')) return <span>✨</span>
  if (name.includes('memory') || name.includes('MEMORY')) return <span>🧠</span>
  if (name.includes('lesson') || name.includes('learning')) return <span>📚</span>
  if (name.includes('decision')) return <span>⚖️</span>
  if (name.includes('project') || name.includes('task')) return <span>🗂️</span>
  if (name.includes('life') || name.includes('routine')) return <span>🌱</span>
  return <span>📄</span>
}

function DirIcon({ name }) {
  const icons = { daily: '📅', learning: '📚', agents: '🤖', projects: '🗂️', system: '⚙️', archive: '🗃️' }
  return <span>{icons[name] || '📁'}</span>
}

function FileTree({ nodes, selected, onSelect, depth = 0 }) {
  const [open, setOpen] = useState(() => new Set(nodes.filter(n => n.type === 'dir').map(n => n.name)))

  return (
    <div>
      {nodes.map(node => (
        <div key={node.name}>
          {node.type === 'dir' ? (
            <>
              <button
                onClick={() => setOpen(s => { const n = new Set(s); n.has(node.name) ? n.delete(node.name) : n.add(node.name); return n })}
                className="flex items-center gap-1.5 w-full text-left px-2 py-1 hover:bg-oc-s3 rounded text-[11px] text-oc-muted"
                style={{ paddingLeft: `${8 + depth * 12}px` }}
              >
                <span className="text-[9px]">{open.has(node.name) ? '▾' : '▸'}</span>
                <DirIcon name={node.name} />
                <span className="truncate">{node.name}</span>
              </button>
              {open.has(node.name) && node.children?.length > 0 && (
                <FileTree nodes={node.children} selected={selected} onSelect={onSelect} depth={depth + 1} />
              )}
            </>
          ) : (
            <button
              onClick={() => onSelect(node)}
              className={`flex items-center gap-1.5 w-full text-left px-2 py-1 rounded text-[11px] transition-colors ${
                selected?.path === node.path
                  ? 'bg-violet-900/40 text-violet-300'
                  : 'text-oc-muted hover:bg-oc-s3 hover:text-oc-text'
              }`}
              style={{ paddingLeft: `${8 + depth * 12}px` }}
            >
              <FileIcon name={node.name} />
              <span className="truncate">{node.name.replace('.md', '').replace('.txt', '')}</span>
            </button>
          )}
        </div>
      ))}
    </div>
  )
}

export default function MemoryBrowser() {
  const [tree, setTree] = useState([])
  const [selected, setSelected] = useState(null)
  const [content, setContent] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetch('/api/memory').then(r => r.json()).then(d => setTree(d.tree || []))
  }, [])

  async function handleSelect(node) {
    setSelected(node)
    setContent(null)
    setLoading(true)
    try {
      const r = await fetch(`/api/memory/file?path=${encodeURIComponent(node.path)}`)
      const d = await r.json()
      setContent(d.content || '')
    } catch {
      setContent('Error loading file.')
    }
    setLoading(false)
  }

  return (
    <div className="bg-oc-surface border border-oc-border rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-oc-border">
        <span className="text-[10px] uppercase tracking-widest text-oc-muted font-semibold">
          Memory Browser
          <span className="text-oc-muted/50 normal-case tracking-normal font-normal ml-1">(workspace/memory)</span>
        </span>
        {selected && (
          <span className="text-[10px] text-violet-400">{selected.path}</span>
        )}
      </div>

      <div className="flex" style={{ minHeight: '320px', maxHeight: '480px' }}>
        {/* Sidebar */}
        <div className="w-52 flex-shrink-0 border-r border-oc-border overflow-y-auto py-1">
          {tree.length === 0 ? (
            <div className="p-3 text-[11px] text-oc-muted animate-pulse">Loading…</div>
          ) : (
            <FileTree nodes={tree} selected={selected} onSelect={handleSelect} />
          )}
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {!selected && (
            <div className="h-full flex items-center justify-center text-oc-muted text-xs">
              ← Select a file to view its contents
            </div>
          )}
          {selected && loading && (
            <div className="text-oc-muted text-xs animate-pulse">Loading…</div>
          )}
          {selected && !loading && content !== null && (
            <div className="prose prose-invert prose-sm max-w-none text-[12px] text-zinc-300 leading-relaxed
              [&_h1]:text-zinc-100 [&_h1]:text-sm [&_h2]:text-zinc-100 [&_h2]:text-xs [&_h2]:uppercase [&_h2]:tracking-wider [&_h2]:mt-3
              [&_h3]:text-zinc-200 [&_h3]:text-xs [&_p]:mb-1.5 [&_ul]:pl-4 [&_li]:mb-0.5
              [&_code]:bg-oc-s3 [&_code]:px-1 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-[11px]
              [&_strong]:text-zinc-100 [&_hr]:border-oc-border [&_a]:text-violet-400">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
