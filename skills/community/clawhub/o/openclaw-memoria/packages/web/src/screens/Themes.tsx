/**
 * Thèmes — la « carte » de ce que sait Memoria, agent par agent, rangé par
 * SUJET. Chaque thème est une tuile dont la taille reflète son importance
 * (plus l'agent en sait, plus c'est gros). Cliquer un thème montre ses
 * souvenirs : on voit OÙ chaque chose est rangée. C'est la puissance de
 * Memoria, d'un coup d'œil.
 */
import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  ApiError,
  getAgents,
  getTopics,
  getTopicFacts,
  getTopicRelations,
  refineTopics,
  type AdminFact,
  type AgentEntry,
  type Topic,
  type TopicGraph,
} from '../api'
import { useT } from '../i18n'

export function Themes() {
  const { t: tr } = useT()
  const [agents, setAgents] = useState<AgentEntry[]>([])
  const [instance, setInstance] = useState<string>('')
  const [topics, setTopics] = useState<Topic[] | null>(null)
  const [active, setActive] = useState<Topic | null>(null)
  const [facts, setFacts] = useState<AdminFact[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [refining, setRefining] = useState(false)
  const [view, setView] = useState<'tiles' | 'graph'>('tiles')

  useEffect(() => {
    getAgents()
      .then(a => {
        const real = a.filter(x => x.assistant_type !== 'generic' && !x.instance.revoked_at)
        setAgents(real)
        if (real.length > 0 && real[0]) setInstance(real[0].instance.id)
      })
      .catch(() => setError(tr('themes.error_service')))
  }, [tr])

  useEffect(() => {
    if (!instance) return
    setTopics(null)
    setActive(null)
    setFacts(null)
    // On met en avant les thèmes consistants (≥2 souvenirs) ; les thèmes à 1
    // souvenir forment une longue queue qu'on n'affiche pas par défaut.
    getTopics(instance, 2)
      .then(setTopics)
      .catch(err => {
        setTopics([])
        if (err instanceof ApiError && err.status !== 404) setError(err.message)
      })
  }, [instance])

  const openTopic = useCallback(
    async (t: Topic) => {
      setActive(t)
      setFacts(null)
      try {
        setFacts(await getTopicFacts(instance, t.id))
      } catch (err) {
        setError(err instanceof ApiError ? err.message : tr('themes.error_load'))
      }
    },
    [instance, tr],
  )

  const maxImportance = useMemo(() => Math.max(1, ...(topics ?? []).map(t => t.importance_score)), [topics])

  return (
    <section>
      <header className="screen-head">
        <div>
          <h1>{tr('themes.title')}</h1>
          <p className="muted">{tr('themes.lead')}</p>
        </div>
        <div className="theme-toolbar">
          <div className="view-switch" role="tablist" aria-label={tr('themes.view_aria')}>
            <button type="button" role="tab" aria-selected={view === 'tiles'} className={`view-tab${view === 'tiles' ? ' view-tab-active' : ''}`} onClick={() => setView('tiles')}>
              {tr('themes.view_tiles')}
            </button>
            <button type="button" role="tab" aria-selected={view === 'graph'} className={`view-tab${view === 'graph' ? ' view-tab-active' : ''}`} onClick={() => setView('graph')}>
              {tr('themes.view_relations')}
            </button>
          </div>
          <button
            type="button"
            className="btn btn-ghost"
            disabled={refining || !instance}
            title={tr('themes.refine_title')}
            onClick={async () => {
              setRefining(true)
              try {
                const n = await refineTopics(instance)
                if (n > 0) setTopics(await getTopics(instance, 2))
                else setError(tr('themes.error_no_ai'))
              } catch (err) {
                setError(err instanceof ApiError ? err.message : tr('themes.error_refine'))
              } finally {
                setRefining(false)
              }
            }}
          >
            {refining ? tr('themes.refining') : tr('themes.refine_button')}
          </button>
          {agents.length > 0 && (
            <select className="agent-select" value={instance} onChange={e => setInstance(e.target.value)}>
              {agents.map(a => (
                <option key={a.instance.id} value={a.instance.id}>
                  {a.assistant_type}
                </option>
              ))}
            </select>
          )}
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      {topics === null ? (
        <div className="spinner-row"><span className="spinner" aria-hidden /> {tr('common.loading')}</div>
      ) : topics.length === 0 ? (
        <div className="empty-state">
          <p>{tr('themes.empty_title')}</p>
          <p className="muted">{tr('themes.empty_body')}</p>
        </div>
      ) : view === 'graph' ? (
        <ThemeRelations instance={instance} onOpen={t => void openTopic(t)} onError={setError} />
      ) : (
        <div className="theme-cloud">
          {topics.map(t => {
            const scale = 0.85 + (t.importance_score / maxImportance) * 0.6
            return (
              <button
                key={t.id}
                type="button"
                className={`theme-tile${active?.id === t.id ? ' theme-active' : ''}`}
                style={{ fontSize: `${scale}rem` }}
                onClick={() => void openTopic(t)}
              >
                <span className="theme-name">{t.name}</span>
                <span className="theme-count">{t.fact_count}</span>
              </button>
            )
          })}
        </div>
      )}

      {view === 'tiles' && active && (
        <div className="theme-detail">
          <h2>{active.name} <span className="muted">{tr('themes.detail_count', { count: active.fact_count })}</span></h2>
          {active.keywords.length > 0 && (
            <div className="theme-keywords">{active.keywords.slice(0, 8).map(k => <span key={k} className="badge badge-muted">{k}</span>)}</div>
          )}
          {facts === null ? (
            <div className="spinner-row"><span className="spinner" aria-hidden /> …</div>
          ) : (
            <ul className="fact-list">
              {facts.map(f => (
                <li key={f.id} className="fact-card">
                  <p className="fact-content">{f.fact}</p>
                  <div className="fact-meta"><span className="badge badge-muted">{f.category}</span></div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </section>
  )
}

/**
 * Carte des relations entre thèmes : graphe circulaire SANS dépendance (SVG pur).
 * Deux thèmes reliés par une arête s'ils partagent des souvenirs ou des entités
 * (Néto, un client, un projet…). Épaisseur de l'arête = force du lien. Survol
 * d'un thème → ses liens ressortent ; clic → ouvre ses souvenirs (vue Tuiles).
 */
function ThemeRelations({ instance, onOpen, onError }: { instance: string; onOpen: (t: Topic) => void; onError: (m: string) => void }) {
  const { t: tr } = useT()
  const [graph, setGraph] = useState<TopicGraph | null>(null)
  const [hover, setHover] = useState<string | null>(null)

  useEffect(() => {
    if (!instance) return
    setGraph(null)
    getTopicRelations(instance, 2)
      .then(setGraph)
      .catch(err => {
        setGraph({ nodes: [], edges: [] })
        if (err instanceof ApiError && err.status !== 404) onError(err.message)
      })
  }, [instance, onError])

  const layout = useMemo(() => {
    if (!graph) return null
    const n = graph.nodes.length
    const size = 560
    const cx = size / 2
    const cy = size / 2
    const R = size / 2 - 90
    const maxImp = Math.max(1, ...graph.nodes.map(t => t.importance_score))
    const pos = new Map<string, { x: number; y: number; r: number; t: Topic; angle: number }>()
    graph.nodes.forEach((t, i) => {
      const angle = (i / Math.max(1, n)) * Math.PI * 2 - Math.PI / 2
      pos.set(t.id, {
        x: cx + R * Math.cos(angle),
        y: cy + R * Math.sin(angle),
        r: 7 + (t.importance_score / maxImp) * 13,
        t,
        angle,
      })
    })
    const maxW = Math.max(1, ...graph.edges.map(e => e.weight))
    return { size, pos, maxW }
  }, [graph])

  if (graph === null) return <div className="spinner-row"><span className="spinner" aria-hidden /> {tr('themes.loading_relations')}</div>
  if (graph.edges.length === 0)
    return (
      <div className="empty-state">
        <p>{tr('themes.relations_empty_title')}</p>
        <p className="muted">{tr('themes.relations_empty_body')}</p>
      </div>
    )

  const { size, pos, maxW } = layout!
  const strongest = [...graph.edges].slice(0, 8)

  return (
    <div className="theme-graph-wrap">
      <svg className="theme-graph" viewBox={`0 0 ${size} ${size}`} role="img" aria-label={tr('themes.graph_aria')}>
        {graph.edges.map(e => {
          const pa = pos.get(e.a)
          const pb = pos.get(e.b)
          if (!pa || !pb) return null
          const active = hover === null || hover === e.a || hover === e.b
          return (
            <line
              key={`${e.a}-${e.b}`}
              x1={pa.x} y1={pa.y} x2={pb.x} y2={pb.y}
              stroke="var(--accent)"
              strokeWidth={1 + (e.weight / maxW) * 5}
              strokeOpacity={active ? 0.55 : 0.08}
              strokeLinecap="round"
            >
              <title>{e.via.length > 0 ? tr('themes.edge_linked_by', { via: e.via.join(', ') }) : tr('themes.edge_shared_facts', { count: e.shared_facts })}</title>
            </line>
          )
        })}
        {[...pos.values()].map(({ x, y, r, t, angle }) => {
          const dim = hover !== null && hover !== t.id && !graph.edges.some(e => (e.a === hover && e.b === t.id) || (e.b === hover && e.a === t.id))
          const right = Math.cos(angle) >= 0
          return (
            <g
              key={t.id}
              className="theme-node"
              opacity={dim ? 0.25 : 1}
              onMouseEnter={() => setHover(t.id)}
              onMouseLeave={() => setHover(null)}
              onClick={() => onOpen(t)}
              style={{ cursor: 'pointer' }}
            >
              <circle cx={x} cy={y} r={r} fill="var(--accent)" fillOpacity={0.85} />
              <text x={x + (right ? r + 5 : -(r + 5))} y={y + 4} textAnchor={right ? 'start' : 'end'} className="theme-node-label">
                {t.name.length > 22 ? t.name.slice(0, 20) + '…' : t.name}
              </text>
            </g>
          )
        })}
      </svg>
      <div className="theme-graph-legend">
        <h3>{tr('themes.strongest_links')}</h3>
        <ul>
          {strongest.map(e => {
            const na = pos.get(e.a)?.t.name ?? '?'
            const nb = pos.get(e.b)?.t.name ?? '?'
            return (
              <li key={`${e.a}-${e.b}`}>
                <strong>{na}</strong> ↔ <strong>{nb}</strong>
                <span className="muted">
                  {e.via.length > 0 ? tr('themes.legend_via', { via: e.via.join(', ') }) : e.shared_facts > 0 ? tr('themes.legend_shared', { count: e.shared_facts }) : ''}
                </span>
              </li>
            )
          })}
        </ul>
      </div>
    </div>
  )
}
