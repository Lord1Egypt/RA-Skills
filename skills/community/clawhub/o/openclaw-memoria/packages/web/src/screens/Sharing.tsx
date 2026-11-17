/**
 * Partage (spec §11) : deux outils.
 *  1. Matrice « qui peut lire quoi » : pour chaque scope partagé, coche les
 *     agents autorisés en lecture.
 *  2. Faits sur toi à partager : pour chaque agent, Memoria propose les faits
 *     qui parlent de l'utilisateur (identité/préférences) ; tu choisis ceux à
 *     remonter vers la mémoire partagée « user » (tous les agents y accèdent).
 * Rien n'est partagé sans ton clic — Memoria propose, tu décides.
 */
import { useCallback, useEffect, useState } from 'react'
import {
  ApiError,
  getAgents,
  getIdentityCandidates,
  getScopeFacts,
  getScopes,
  setPolicy,
  shareFacts,
  type AdminFact,
  type AgentEntry,
  type AssistantInfo,
  type IdentityCandidate,
  type ScopeAccess,
} from '../api'
import { useT } from '../i18n'

type Translate = (key: string, vars?: Record<string, string | number>) => string

export function Sharing() {
  const { t } = useT()
  const [scopes, setScopes] = useState<ScopeAccess[] | null>(null)
  const [assistants, setAssistants] = useState<AssistantInfo[]>([])
  const [agents, setAgents] = useState<AgentEntry[]>([])
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [exploring, setExploring] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    try {
      const [s, a] = await Promise.all([getScopes(), getAgents()])
      setScopes(s.scopes.filter(sc => sc.type !== 'private' && sc.type !== 'legacy_to_review'))
      setAssistants(s.assistants)
      setAgents(a)
      setError(null)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t('sharing.error_service'))
    }
  }, [t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const toggle = useCallback(
    async (assistantId: string, scope: ScopeAccess, next: boolean) => {
      setBusy(true)
      try {
        await setPolicy(assistantId, scope.id, { can_read: next })
        await refresh()
      } catch (err) {
        setError(err instanceof ApiError ? err.message : t('sharing.error_toggle'))
      } finally {
        setBusy(false)
      }
    },
    [refresh, t],
  )

  return (
    <section>
      <header className="screen-head">
        <div>
          <h1>{t('sharing.title')}</h1>
          <p className="muted">
            {t('sharing.lead')}
          </p>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <div className="settings-block">
        <h2>{t('sharing.matrix_title')}</h2>
        {scopes === null ? (
          <div className="spinner-row"><span className="spinner" aria-hidden /> {t('common.loading')}</div>
        ) : scopes.length === 0 ? (
          <p className="muted">{t('sharing.matrix_empty')}</p>
        ) : (
          <table className="share-matrix">
            <thead>
              <tr>
                <th>{t('sharing.col_scope')}</th>
                <th>{t('sharing.col_facts')}</th>
                {assistants.map(a => (
                  <th key={a.id} title={a.type}>{a.display_name}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {scopes.map(scope => (
                <tr key={scope.id}>
                  <td>
                    <button type="button" className="scope-link" onClick={() => setExploring(exploring === scope.id ? null : scope.id)}>
                      {scopeLabel(t, scope)} <span className="muted">{exploring === scope.id ? '▾' : '▸'}</span>
                    </button>
                  </td>
                  <td className="muted">{scope.facts}</td>
                  {assistants.map(a => {
                    const allowed = scope.readers.includes(a.id)
                    return (
                      <td key={a.id} className="share-cell">
                        <input
                          type="checkbox"
                          checked={allowed}
                          disabled={busy}
                          aria-label={t('sharing.reader_aria', { agent: a.display_name, scope: scopeLabel(t, scope) })}
                          onChange={e => void toggle(a.id, scope, e.target.checked)}
                        />
                      </td>
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {exploring && <ScopeContent scopeId={exploring} onError={setError} />}
      </div>

      <div className="settings-block">
        <h2>{t('sharing.identity_title')}</h2>
        <p className="muted">
          {t('sharing.identity_lead')}
        </p>
        {agents.filter(a => a.assistant_type !== 'generic').map(a => (
          <IdentityPanel key={a.instance.id} agent={a} onShared={() => void refresh()} onError={setError} />
        ))}
      </div>
    </section>
  )
}

/** Contenu d'un scope partagé (les souvenirs dans « Sur vous », « Entreprise »…). */
function ScopeContent({ scopeId, onError }: { scopeId: string; onError: (m: string) => void }) {
  const { t } = useT()
  const [facts, setFacts] = useState<AdminFact[] | null>(null)
  useEffect(() => {
    getScopeFacts(scopeId)
      .then(setFacts)
      .catch(err => onError(err instanceof ApiError ? err.message : t('sharing.error_load')))
  }, [scopeId, onError, t])
  if (facts === null) return <div className="spinner-row"><span className="spinner" aria-hidden /> …</div>
  if (facts.length === 0) return <p className="muted scope-content">{t('sharing.scope_empty')}</p>
  return (
    <ul className="fact-list scope-content">
      {facts.map(f => (
        <li key={f.id} className="fact-card"><p className="fact-content">{f.fact}</p></li>
      ))}
    </ul>
  )
}

function IdentityPanel({
  agent,
  onShared,
  onError,
}: {
  agent: AgentEntry
  onShared: () => void
  onError: (m: string) => void
}) {
  const { t } = useT()
  const [candidates, setCandidates] = useState<IdentityCandidate[] | null>(null)
  const [selected, setSelected] = useState<Set<string>>(new Set())
  const [open, setOpen] = useState(false)
  const [busy, setBusy] = useState(false)

  const load = useCallback(async () => {
    try {
      const c = await getIdentityCandidates(agent.instance.id)
      setCandidates(c)
    } catch (err) {
      onError(err instanceof ApiError ? err.message : t('sharing.error_load'))
    }
  }, [agent.instance.id, onError, t])

  const share = useCallback(async () => {
    if (selected.size === 0) return
    setBusy(true)
    try {
      await shareFacts([...selected], 'user')
      setSelected(new Set())
      await load()
      onShared()
    } catch (err) {
      onError(err instanceof ApiError ? err.message : t('sharing.error_share'))
    } finally {
      setBusy(false)
    }
  }, [selected, load, onShared, onError, t])

  return (
    <div className="identity-panel">
      <button
        type="button"
        className="btn btn-ghost"
        onClick={() => {
          setOpen(o => !o)
          if (!open && candidates === null) void load()
        }}
      >
        {open ? '▾' : '▸'} {t('sharing.identity_panel_label', { agent: agent.assistant_type })}
      </button>
      {open && (
        candidates === null ? (
          <div className="spinner-row"><span className="spinner" aria-hidden /> {t('sharing.analyzing')}</div>
        ) : candidates.length === 0 ? (
          <p className="muted">{t('sharing.identity_empty')}</p>
        ) : (
          <>
            <ul className="fact-list">
              {candidates.map(c => (
                <li key={c.id} className="fact-card identity-card">
                  <label>
                    <input
                      type="checkbox"
                      checked={selected.has(c.id)}
                      onChange={e => {
                        const next = new Set(selected)
                        if (e.target.checked) next.add(c.id)
                        else next.delete(c.id)
                        setSelected(next)
                      }}
                    />
                    <span>{c.content}</span>
                  </label>
                </li>
              ))}
            </ul>
            <button type="button" className="btn btn-primary" disabled={busy || selected.size === 0} onClick={() => void share()}>
              {selected.size > 0 ? t('sharing.share_button_count', { count: selected.size }) : t('sharing.share_button')}
            </button>
          </>
        )
      )}
    </div>
  )
}

function scopeLabel(t: Translate, scope: ScopeAccess): string {
  switch (scope.type) {
    case 'user':
      return t('sharing.scope_user')
    case 'org':
      return t('sharing.scope_org')
    case 'client':
      return t('sharing.scope_client', { name: scope.name })
    case 'project':
      return t('sharing.scope_project', { name: scope.name })
    case 'shared_topic':
      return t('sharing.scope_topic', { name: scope.name })
    default:
      return scope.name
  }
}
