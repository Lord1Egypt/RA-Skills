/**
 * Révisions — le « ménage » de la mémoire. Memoria repère les souvenirs qui se
 * contredisent ou font doublon, et PROPOSE de les ranger : garder le plus
 * récent, écarter l'ancien. Rien n'est modifié sans ta validation.
 */
import { useCallback, useEffect, useState } from 'react'
import {
  ApiError,
  decideRevision,
  getAgents,
  getRevisions,
  proposeRevisions,
  type AgentEntry,
  type RevisionProposal,
} from '../api'
import { useT } from '../i18n'

type Translate = (key: string, vars?: Record<string, string | number>) => string

const KNOWN_KINDS = new Set(['contradicted', 'duplicate', 'obsolete'])

/** Libellé traduit d'un type de révision (repli sur le type brut si inconnu). */
function kindLabel(t: Translate, kind: string): string {
  return KNOWN_KINDS.has(kind) ? t(`revisions.kind_${kind}`) : kind
}

export function Revisions() {
  const { t } = useT()
  const [agents, setAgents] = useState<AgentEntry[]>([])
  const [instance, setInstance] = useState('')
  const [items, setItems] = useState<RevisionProposal[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    getAgents()
      .then(a => {
        const real = a.filter(x => x.assistant_type !== 'generic' && !x.instance.revoked_at)
        setAgents(real)
        if (real[0]) setInstance(real[0].instance.id)
      })
      .catch(() => setError(t('revisions.error_service')))
  }, [t])

  const load = useCallback(async (inst: string) => {
    setItems(null)
    try {
      // déclenche une analyse fraîche puis liste
      await proposeRevisions(inst).catch(() => 0)
      setItems(await getRevisions(inst))
    } catch (err) {
      setItems([])
      if (err instanceof ApiError && err.status !== 404) setError(err.message)
    }
  }, [])

  useEffect(() => {
    if (instance) void load(instance)
  }, [instance, load])

  const decide = useCallback(
    async (id: string, decision: 'accept' | 'dismiss') => {
      setBusy(true)
      try {
        await decideRevision(instance, id, decision)
        setItems(prev => (prev ? prev.filter(i => i.id !== id) : prev))
      } catch (err) {
        setError(err instanceof ApiError ? err.message : t('revisions.error_action'))
      } finally {
        setBusy(false)
      }
    },
    [instance, t],
  )

  return (
    <section>
      <header className="screen-head">
        <div>
          <h1>{t('revisions.title')}</h1>
          <p className="muted">{t('revisions.lead')}</p>
        </div>
        {agents.length > 0 && (
          <select className="agent-select" value={instance} onChange={e => setInstance(e.target.value)}>
            {agents.map(a => <option key={a.instance.id} value={a.instance.id}>{a.assistant_type}</option>)}
          </select>
        )}
      </header>

      {error && <div className="error-banner">{error}</div>}

      {items === null ? (
        <div className="spinner-row"><span className="spinner" aria-hidden /> {t('revisions.analyzing')}</div>
      ) : items.length === 0 ? (
        <div className="empty-state">
          <p>{t('revisions.empty_title')}</p>
          <p className="muted">{t('revisions.empty_body')}</p>
        </div>
      ) : (
        <ul className="pattern-list">
          {items.map(r => (
            <li key={r.id} className="pattern-card">
              <div className="pattern-head">
                <span className="badge badge-accent">{kindLabel(t, r.kind)}</span>
              </div>
              <p className="pattern-canonical muted">{r.reason}</p>
              <div className="pattern-actions">
                <button type="button" className="btn btn-primary" disabled={busy} onClick={() => void decide(r.id, 'accept')}>
                  {t('revisions.action_accept')}
                </button>
                <button type="button" className="btn btn-ghost" disabled={busy} onClick={() => void decide(r.id, 'dismiss')}>
                  {t('revisions.action_dismiss')}
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
