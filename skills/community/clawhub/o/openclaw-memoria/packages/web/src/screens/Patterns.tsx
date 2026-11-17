/**
 * Récurrences — « Memoria a remarqué que… ». Les choses que tu dis/fais de
 * façon récurrente, repérées et regroupées. Tu confirmes (Memoria en fait un
 * souvenir consolidé) ou tu écartes. Rien n'est appliqué sans ton accord.
 */
import { useCallback, useEffect, useState } from 'react'
import { ApiError, getAgents, getPatterns, decidePattern, type AgentEntry, type Pattern } from '../api'
import { useT } from '../i18n'

type Translate = (key: string, vars?: Record<string, string | number>) => string

const KIND_KEY: Record<string, string> = {
  preference: 'patterns.kind_preference',
  habit: 'patterns.kind_habit',
  convention: 'patterns.kind_convention',
  fact: 'patterns.kind_fact',
}

/** Libellé traduit du type de récurrence (repli sur « Récurrence »). */
function kindLabel(t: Translate, kind: string): string {
  return t(KIND_KEY[kind] ?? 'patterns.kind_default')
}

export function Patterns() {
  const { t } = useT()
  const [agents, setAgents] = useState<AgentEntry[]>([])
  const [instance, setInstance] = useState('')
  const [patterns, setPatterns] = useState<Pattern[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    getAgents()
      .then(a => {
        const real = a.filter(x => x.assistant_type !== 'generic' && !x.instance.revoked_at)
        setAgents(real)
        if (real[0]) setInstance(real[0].instance.id)
      })
      .catch(() => setError(t('patterns.service_unavailable')))
  }, [t])

  const load = useCallback(async (inst: string) => {
    setPatterns(null)
    try {
      setPatterns(await getPatterns(inst))
    } catch (err) {
      setPatterns([])
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
        await decidePattern(instance, id, decision)
        await load(instance)
      } catch (err) {
        setError(err instanceof ApiError ? err.message : t('patterns.action_failed'))
      } finally {
        setBusy(false)
      }
    },
    [instance, load, t],
  )

  return (
    <section>
      <header className="screen-head">
        <div>
          <h1>{t('patterns.title')}</h1>
          <p className="muted">{t('patterns.lead')}</p>
        </div>
        {agents.length > 0 && (
          <select className="agent-select" value={instance} onChange={e => setInstance(e.target.value)}>
            {agents.map(a => <option key={a.instance.id} value={a.instance.id}>{a.assistant_type}</option>)}
          </select>
        )}
      </header>

      {error && <div className="error-banner">{error}</div>}

      {patterns === null ? (
        <div className="spinner-row"><span className="spinner" aria-hidden /> {t('patterns.analyzing')}</div>
      ) : patterns.length === 0 ? (
        <div className="empty-state">
          <p>{t('patterns.empty_title')}</p>
          <p className="muted">{t('patterns.empty_body')}</p>
        </div>
      ) : (
        <ul className="pattern-list">
          {patterns.map(p => (
            <li key={p.id} className="pattern-card">
              <div className="pattern-head">
                <span className="badge badge-accent">{kindLabel(t, p.kind)}</span>
                <span className="muted">{t('patterns.seen_times', { count: p.occurrences })}</span>
              </div>
              <p className="pattern-label">{p.label}</p>
              <p className="pattern-canonical muted">« {p.canonical_fact} »</p>
              <div className="pattern-actions">
                <button type="button" className="btn btn-primary" disabled={busy} onClick={() => void decide(p.id, 'accept')}>
                  {t('patterns.consolidate')}
                </button>
                <button type="button" className="btn btn-ghost" disabled={busy} onClick={() => void decide(p.id, 'dismiss')}>
                  {t('patterns.dismiss')}
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
