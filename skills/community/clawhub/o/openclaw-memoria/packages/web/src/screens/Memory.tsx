/**
 * Mémoire — par agent : recherche dans ses souvenirs (GET /v1/admin/facts,
 * route câblée à l'intégration ; q vide = derniers souvenirs) et oubli
 * définitif fait par fait (POST /v1/admin/forget {ids}).
 */
import { useState, type FormEvent } from 'react'
import { forgetFacts, getAgents, searchAll, searchFacts, type AdminFact, type AgentEntry } from '../api'
import {
  ConfirmButton,
  EmptyState,
  ErrorBanner,
  Spinner,
  agentTypeLabel,
  formatDate,
  humanError,
  useLoad,
} from '../components/ui'
import { useT } from '../i18n'

type Translate = (key: string, vars?: Record<string, string | number>) => string

/** Souvenir affiché : optionnellement étiqueté de l'agent (recherche globale). */
type ShownFact = AdminFact & { agent_type?: string }

const ALL = '__all__'

type SearchState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; facts: ShownFact[]; query: string }

export function Memory() {
  const { t } = useT()
  const { state: agentsState, reload: reloadAgents } = useLoad(getAgents)

  return (
    <section>
      <header className="screen-head">
        <h1>{t('memory.title')}</h1>
      </header>

      {agentsState.status === 'loading' && <Spinner />}
      {agentsState.status === 'error' && <ErrorBanner message={agentsState.message} onRetry={reloadAgents} />}
      {agentsState.status === 'ready' &&
        (agentsState.data.length === 0 ? (
          <EmptyState
            title={t('memory.no_agent_title')}
            body={t('memory.no_agent_body')}
          />
        ) : (
          <MemoryBrowser agents={agentsState.data} />
        ))}
    </section>
  )
}

function MemoryBrowser({ agents }: { agents: AgentEntry[] }) {
  const { t } = useT()
  const active = agents.filter(a => a.instance.revoked_at === null)
  const first = active[0] ?? agents[0]
  const [instanceId, setInstanceId] = useState(first ? first.instance.id : '')
  const [query, setQuery] = useState('')
  const [search, setSearch] = useState<SearchState>({ status: 'idle' })

  const runSearch = (q: string) => {
    setSearch({ status: 'loading' })
    const p = instanceId === ALL ? searchAll(q) : searchFacts(instanceId, q)
    p.then(
      facts => setSearch({ status: 'ready', facts, query: q }),
      (err: unknown) => {
        console.warn('memoria-ui : recherche mémoire échouée', err)
        setSearch({ status: 'error', message: humanError(err) })
      },
    )
  }

  const submit = (e: FormEvent) => {
    e.preventDefault()
    runSearch(query.trim())
  }

  const forget = (fact: AdminFact) => {
    forgetFacts([fact.id]).then(
      deleted => {
        if (deleted === 0) {
          console.warn(`memoria-ui : oubli sans effet pour ${fact.id}`)
        }
        setSearch(prev =>
          prev.status === 'ready' ? { ...prev, facts: prev.facts.filter(f => f.id !== fact.id) } : prev,
        )
      },
      (err: unknown) => {
        console.warn('memoria-ui : oubli échoué', err)
        setSearch({ status: 'error', message: humanError(err) })
      },
    )
  }

  return (
    <>
      <form className="memory-controls" onSubmit={submit}>
        <label className="field">
          <span className="field-label">{t('memory.field_agent')}</span>
          <select
            value={instanceId}
            onChange={e => {
              setInstanceId(e.target.value)
              setSearch({ status: 'idle' })
            }}
          >
            <option value={ALL}>{t('memory.all_memories')}</option>
            {agents.map(({ instance, assistant_type }) => (
              <option key={instance.id} value={instance.id}>
                {agentTypeLabel(assistant_type)} — {instance.machine_id}
                {instance.revoked_at !== null ? t('memory.disconnected_suffix') : ''}
              </option>
            ))}
          </select>
        </label>
        <label className="field field-grow">
          <span className="field-label">{instanceId === ALL ? t('memory.search_all_label') : t('memory.search_one_label')}</span>
          <input
            type="search"
            value={query}
            placeholder={t('memory.search_placeholder')}
            onChange={e => setQuery(e.target.value)}
          />
        </label>
        <button type="submit" className="btn btn-primary" disabled={instanceId === ''}>
          {t('memory.search_button')}
        </button>
        <button
          type="button"
          className="btn btn-ghost"
          disabled={instanceId === ''}
          onClick={() => {
            setQuery('')
            runSearch('')
          }}
        >
          {t('memory.show_all')}
        </button>
      </form>

      {search.status === 'idle' && (
        <p className="muted">{t('memory.hint')}</p>
      )}
      {search.status === 'loading' && <Spinner label={t('memory.searching')} />}
      {search.status === 'error' && <ErrorBanner message={search.message} />}
      {search.status === 'ready' &&
        (search.facts.length === 0 ? (
          <EmptyState
            title={t('memory.empty_title')}
            body={
              search.query === ''
                ? t('memory.empty_body_all')
                : t('memory.empty_body_query', { query: search.query })
            }
          />
        ) : (
          <ul className="fact-list">
            {search.facts.map(fact => (
              <li key={fact.id} className="fact-card">
                <p className="fact-content">{fact.fact}</p>
                <div className="fact-meta">
                  {fact.agent_type && (
                    <span className="badge badge-ok" title={t('memory.badge_agent_source')}>{agentTypeLabel(fact.agent_type)}</span>
                  )}
                  {(fact.topics ?? []).map(topic => (
                    <span key={topic} className="badge badge-theme" title={t('memory.badge_topic')}>{topic}</span>
                  ))}
                  <span className="badge badge-muted">{fact.category}</span>
                  <span className="badge badge-muted">{scopeLabel(t, fact)}</span>
                  <span className="muted">{formatDate(fact.created_at)}</span>
                  <span className="fact-actions">
                    <ConfirmButton label={t('memory.forget')} confirmLabel={t('memory.forget_confirm')} onConfirm={() => forget(fact)} />
                  </span>
                </div>
              </li>
            ))}
          </ul>
        ))}
    </>
  )
}

/** Libellé lisible du scope — jamais d'identifiant brut quand on peut l'éviter. */
function scopeLabel(t: Translate, fact: AdminFact): string {
  const name = fact.scope_name ?? fact.scope_id
  if (name.startsWith('private:')) return t('memory.scope_private')
  if (name === 'user') return t('memory.scope_shared')
  return name.length > 24 ? `${name.slice(0, 24)}…` : name
}
