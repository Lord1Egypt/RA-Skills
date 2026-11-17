/**
 * Audit — journal d'activité neutre (jamais de contenu, voir audit_log core).
 * Le daemon renvoie les 200 dernières entrées, pagination locale.
 */
import { useState } from 'react'
import { getAudit, type AuditEntry } from '../api'
import { EmptyState, ErrorBanner, Spinner, formatDate, useLoad } from '../components/ui'
import { useT } from '../i18n'

const PAGE_SIZE = 25

// Actions techniques → clé i18n audit.action.<action> (repli : l'action brute).
const KNOWN_ACTIONS = new Set([
  'pair_assistant', 'complete_pairing', 'revoke_instance', 'store_fact', 'recall', 'forget', 'person_autocreate',
])

export function Audit() {
  const { t } = useT()
  const { state, reload } = useLoad(getAudit)
  const [page, setPage] = useState(0)

  return (
    <section>
      <header className="screen-head">
        <h1>{t('audit.title')}</h1>
        <button type="button" className="btn btn-ghost" onClick={() => { setPage(0); reload() }}>
          {t('common.refresh')}
        </button>
      </header>
      <p className="muted">{t('audit.lead')}</p>

      {state.status === 'loading' && <Spinner />}
      {state.status === 'error' && <ErrorBanner message={state.message} onRetry={reload} />}
      {state.status === 'ready' &&
        (state.data.length === 0 ? (
          <EmptyState title={t('audit.empty.title')} body={t('audit.empty.body')} />
        ) : (
          <AuditTable entries={state.data} page={page} setPage={setPage} />
        ))}
    </section>
  )
}

type SortKey = 'ts' | 'actor' | 'action' | 'scope'
type SortDir = 'asc' | 'desc'

type Translate = (key: string, vars?: Record<string, string | number>) => string

/** Libellé traduit d'une action (repli sur l'action brute si non connue). */
function actionLabel(t: Translate, action: string): string {
  return KNOWN_ACTIONS.has(action) ? t(`audit.action.${action}`) : action
}

/** Valeur de tri (texte comparable) pour une colonne donnée. */
function sortValue(t: Translate, e: AuditEntry, key: SortKey): string {
  switch (key) {
    case 'ts':
      return e.ts
    case 'actor':
      return `${t(`audit.actor.${e.actor_type}`)} ${e.actor_id}`
    case 'action':
      return actionLabel(t, e.action)
    case 'scope':
      return e.scope_id ?? ''
  }
}

function AuditTable({ entries, page, setPage }: { entries: AuditEntry[]; page: number; setPage: (p: number) => void }) {
  const { t } = useT()
  // Tri par défaut : Date décroissante (le plus récent d'abord).
  const [sortKey, setSortKey] = useState<SortKey>('ts')
  const [sortDir, setSortDir] = useState<SortDir>('desc')

  function toggleSort(key: SortKey) {
    if (key === sortKey) {
      setSortDir(d => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortKey(key)
      setSortDir(key === 'ts' ? 'desc' : 'asc') // date : récent d'abord ; texte : A→Z
    }
    setPage(0)
  }

  const sorted = [...entries].sort((a, b) => {
    const cmp = sortValue(t, a, sortKey).localeCompare(sortValue(t, b, sortKey), undefined, { numeric: true })
    return sortDir === 'asc' ? cmp : -cmp
  })

  const pageCount = Math.max(1, Math.ceil(sorted.length / PAGE_SIZE))
  const current = Math.min(page, pageCount - 1)
  const slice = sorted.slice(current * PAGE_SIZE, (current + 1) * PAGE_SIZE)

  const columns: Array<{ key: SortKey; label: string }> = [
    { key: 'ts', label: t('audit.col.date') },
    { key: 'actor', label: t('audit.col.actor') },
    { key: 'action', label: t('audit.col.action') },
    { key: 'scope', label: t('audit.col.scope') },
  ]
  const arrow = (key: SortKey) => (key === sortKey ? (sortDir === 'asc' ? ' ↑' : ' ↓') : ' ↕')

  return (
    <>
      <table className="table">
        <thead>
          <tr>
            {columns.map(col => (
              <th
                key={col.key}
                className="sortable"
                aria-sort={col.key === sortKey ? (sortDir === 'asc' ? 'ascending' : 'descending') : 'none'}
                onClick={() => toggleSort(col.key)}
              >
                {col.label}
                <span className="sort-arrow muted">{arrow(col.key)}</span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {slice.map(entry => (
            <tr key={entry.id}>
              <td className="nowrap">{formatDate(entry.ts)}</td>
              <td>
                {t(`audit.actor.${entry.actor_type}`)}
                {entry.actor_type === 'assistant' && (
                  <code className="path"> {entry.actor_id.slice(0, 8)}</code>
                )}
              </td>
              <td>
                {actionLabel(t, entry.action)}
                {entry.reason && <span className="muted"> · {entry.reason}</span>}
              </td>
              <td>{entry.scope_id ? <code className="path">{entry.scope_id.slice(0, 8)}</code> : '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <footer className="pager">
        <button type="button" className="btn btn-ghost" disabled={current === 0} onClick={() => setPage(current - 1)}>
          {t('common.prev')}
        </button>
        <span className="muted">
          {t('common.page', { current: current + 1, total: pageCount })}
        </span>
        <button
          type="button"
          className="btn btn-ghost"
          disabled={current >= pageCount - 1}
          onClick={() => setPage(current + 1)}
        >
          {t('common.next')}
        </button>
      </footer>
    </>
  )
}
