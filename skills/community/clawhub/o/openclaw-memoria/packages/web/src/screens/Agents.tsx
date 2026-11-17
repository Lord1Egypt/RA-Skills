/**
 * Agents — détection des assistants de la machine + connexion 1 clic + import
 * des souvenirs avec progression (missions B1/B2/B3/B4), connexion par code de
 * pairing (TTL 10 min, voir PAIRING_TTL_MS côté core) et révocation.
 */
import { useEffect, useState, type ReactNode } from 'react'
import {
  connectAgent,
  deleteAgent,
  deriveSelf,
  detectMachineAgents,
  getAgents,
  getExpertise,
  getImportStatus,
  getSelfObservations,
  pairAgent,
  revokeAgent,
  startImport,
  type AgentEntry,
  type AgentType,
  type ConnectAgentResult,
  type DetectedAgent,
  type ExpertiseDomain,
  type ImportJobStatus,
  type PairResult,
  type SelfObservation,
} from '../api'
import {
  ConfirmButton,
  CopyButton,
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

const PAIRING_TTL_SECONDS = 10 * 60 // miroir de PAIRING_TTL_MS (registry.ts)

const AGENT_CHOICES: Array<{ type: AgentType; labelKey: string; hintKey: string }> = [
  { type: 'claude-code', labelKey: 'agents.choice.claudeCode.label', hintKey: 'agents.choice.claudeCode.hint' },
  { type: 'codex', labelKey: 'agents.choice.codex.label', hintKey: 'agents.choice.codex.hint' },
  { type: 'openclaw', labelKey: 'agents.choice.openclaw.label', hintKey: 'agents.choice.openclaw.hint' },
  { type: 'generic', labelKey: 'agents.choice.generic.label', hintKey: 'agents.choice.generic.hint' },
]

type PairFlow =
  | { step: 'closed' }
  | { step: 'choose'; busy: AgentType | null; error: string | null }
  | { step: 'code'; type: AgentType; result: PairResult }

export function Agents({ onOpenReview }: { onOpenReview?: () => void }) {
  const { t } = useT()
  const { state, reload } = useLoad(getAgents)
  const [flow, setFlow] = useState<PairFlow>({ step: 'closed' })
  const [actionError, setActionError] = useState<string | null>(null)

  const startPairing = (type: AgentType) => {
    setFlow({ step: 'choose', busy: type, error: null })
    pairAgent(type).then(
      result => setFlow({ step: 'code', type, result }),
      (err: unknown) => {
        console.warn('memoria-ui : pairing échoué', err)
        setFlow({ step: 'choose', busy: null, error: humanError(err) })
      },
    )
  }

  const closeFlow = () => {
    setFlow({ step: 'closed' })
    reload()
  }

  const revoke = (instanceId: string) => {
    setActionError(null)
    revokeAgent(instanceId).then(
      () => reload(),
      (err: unknown) => {
        console.warn('memoria-ui : révocation échouée', err)
        setActionError(humanError(err))
      },
    )
  }

  const remove = (instanceId: string) => {
    setActionError(null)
    deleteAgent(instanceId).then(
      () => reload(),
      (err: unknown) => {
        console.warn('memoria-ui : suppression échouée', err)
        setActionError(humanError(err))
      },
    )
  }

  return (
    <section>
      <header className="screen-head">
        <h1>{t('agents.title')}</h1>
        {state.status === 'ready' && state.data.length > 0 && (
          <button type="button" className="btn btn-primary" onClick={() => setFlow({ step: 'choose', busy: null, error: null })}>
            {t('agents.connect')}
          </button>
        )}
      </header>

      <MachineAgents onChanged={reload} onOpenReview={onOpenReview} />

      {actionError && <ErrorBanner message={actionError} />}

      {state.status === 'loading' && <Spinner />}
      {state.status === 'error' && <ErrorBanner message={state.message} onRetry={reload} />}
      {state.status === 'ready' &&
        (state.data.length === 0 && flow.step === 'closed' ? (
          <EmptyState
            title={t('agents.empty.title')}
            body={t('agents.empty.body')}
            action={
              <button
                type="button"
                className="btn btn-primary btn-big"
                onClick={() => setFlow({ step: 'choose', busy: null, error: null })}
              >
                {t('agents.empty.action')}
              </button>
            }
          />
        ) : (
          <AgentList agents={state.data} onRevoke={revoke} onDelete={remove} />
        ))}

      {flow.step === 'choose' && (
        <Modal title={t('agents.choose.title')} onClose={() => setFlow({ step: 'closed' })}>
          {flow.error && <ErrorBanner message={flow.error} />}
          <div className="choice-grid">
            {AGENT_CHOICES.map(choice => (
              <button
                key={choice.type}
                type="button"
                className="choice-card"
                disabled={flow.busy !== null}
                onClick={() => startPairing(choice.type)}
              >
                <strong>{t(choice.labelKey)}</strong>
                <span className="muted">{flow.busy === choice.type ? t('agents.choose.preparing') : t(choice.hintKey)}</span>
              </button>
            ))}
          </div>
        </Modal>
      )}

      {flow.step === 'code' && (
        <Modal title={t('agents.code.title', { agent: agentTypeLabel(flow.type) })} onClose={closeFlow}>
          <PairingCode result={flow.result} onRegenerate={() => startPairing(flow.type)} />
          <div className="modal-foot">
            <button type="button" className="btn btn-primary" onClick={closeFlow}>
              {t('agents.code.done')}
            </button>
          </div>
        </Modal>
      )}
    </section>
  )
}

// ------------------------------------------------------------ Sur cette machine

const START_FRESH_KEY = 'memoria.start_fresh'

/** Choix « Démarrer de zéro » mémorisé localement (pas d'action serveur). */
function loadStartFresh(): Set<string> {
  try {
    const raw = localStorage.getItem(START_FRESH_KEY)
    const parsed: unknown = raw ? JSON.parse(raw) : []
    return new Set(Array.isArray(parsed) ? (parsed as string[]) : [])
  } catch (err) {
    console.warn('memoria-ui : choix « démarrer de zéro » illisible', err)
    return new Set()
  }
}

function saveStartFresh(kinds: Set<string>): void {
  try {
    localStorage.setItem(START_FRESH_KEY, JSON.stringify([...kinds]))
  } catch (err) {
    console.warn('memoria-ui : choix « démarrer de zéro » non sauvegardé', err)
  }
}

type ImportFlow =
  | { step: 'closed' }
  | { step: 'confirm'; agent: DetectedAgent }
  | { step: 'running'; agent: DetectedAgent; status: ImportJobStatus | null }
  | { step: 'done'; agent: DetectedAgent; status: ImportJobStatus }
  | { step: 'failed'; agent: DetectedAgent; message: string }

/** Section « Sur cette machine » : détection, connexion 1 clic, import des souvenirs. */
function MachineAgents({ onChanged, onOpenReview }: { onChanged: () => void; onOpenReview?: () => void }) {
  const { t } = useT()
  const [detected, setDetected] = useState<DetectedAgent[] | null>(null)
  const [detecting, setDetecting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [connectBusy, setConnectBusy] = useState<string | null>(null)
  const [connectResults, setConnectResults] = useState<Record<string, ConnectAgentResult>>({})
  const [startFresh, setStartFresh] = useState<Set<string>>(loadStartFresh)
  const [flow, setFlow] = useState<ImportFlow>({ step: 'closed' })

  const detect = () => {
    setDetecting(true)
    setError(null)
    detectMachineAgents().then(
      agents => {
        setDetected(agents)
        setDetecting(false)
      },
      (err: unknown) => {
        console.warn('memoria-ui : détection des agents échouée', err)
        setError(humanError(err))
        setDetecting(false)
      },
    )
  }

  const connect = (agent: DetectedAgent) => {
    setConnectBusy(agent.kind)
    setError(null)
    connectAgent(agent.kind).then(
      result => {
        setConnectResults(prev => ({ ...prev, [agent.kind]: result }))
        setConnectBusy(null)
        onChanged()
        detect() // rafraîchit already_connected
      },
      (err: unknown) => {
        console.warn('memoria-ui : connexion 1 clic échouée', err)
        setError(humanError(err))
        setConnectBusy(null)
      },
    )
  }

  const dismissImport = (agent: DetectedAgent) => {
    const next = new Set(startFresh)
    next.add(agent.kind)
    setStartFresh(next)
    saveStartFresh(next)
  }

  const undoDismiss = (agent: DetectedAgent) => {
    const next = new Set(startFresh)
    next.delete(agent.kind)
    setStartFresh(next)
    saveStartFresh(next)
  }

  const launchImport = (agent: DetectedAgent) => {
    const isLegacy = agent.kind === 'openclaw'
    startImport({
      instance_id: agent.already_connected!,
      kind: isLegacy ? 'legacy' : 'transcripts',
      ...(isLegacy && agent.data_found.legacy_db ? { legacy_path: agent.data_found.legacy_db.path } : {}),
    }).then(
      status => setFlow({ step: 'running', agent, status }),
      (err: unknown) => {
        console.warn('memoria-ui : démarrage de l’import échoué', err)
        setFlow({ step: 'failed', agent, message: humanError(err) })
      },
    )
  }

  // Polling du job (1 s) tant que la modale est en étape « running ».
  useEffect(() => {
    if (flow.step !== 'running') return
    const agent = flow.agent
    const id = window.setInterval(() => {
      getImportStatus().then(
        status => {
          if (status.state === 'done') setFlow({ step: 'done', agent, status })
          else if (status.state === 'error') setFlow({ step: 'failed', agent, message: status.error ?? t('agents.import.unknownError') })
          else setFlow({ step: 'running', agent, status })
        },
        (err: unknown) => {
          // erreur de polling : visible en console, on retentera au tick suivant
          console.warn('memoria-ui : statut d’import illisible', err)
        },
      )
    }, 1000)
    return () => window.clearInterval(id)
  }, [flow])

  return (
    <div className="machine-agents">
      <div className="machine-head">
        <h2>{t('agents.machine.title')}</h2>
        <button type="button" className="btn" onClick={detect} disabled={detecting}>
          {detecting ? t('agents.machine.detecting') : t('agents.machine.detect')}
        </button>
      </div>
      {error && <ErrorBanner message={error} />}
      {detected !== null && detected.length === 0 && (
        <p className="muted">{t('agents.machine.none')}</p>
      )}
      {detected !== null && detected.length > 0 && (
        <div className="machine-grid">
          {detected.map(agent => (
            <MachineAgentCard
              key={agent.kind}
              agent={agent}
              busy={connectBusy === agent.kind}
              connectResult={connectResults[agent.kind]}
              dismissed={startFresh.has(agent.kind)}
              onConnect={() => connect(agent)}
              onImport={() => setFlow({ step: 'confirm', agent })}
              onDismiss={() => dismissImport(agent)}
              onUndoDismiss={() => undoDismiss(agent)}
            />
          ))}
        </div>
      )}

      {flow.step !== 'closed' && (
        <Modal
          title={t('agents.import.title', { name: flow.agent.name })}
          onClose={() => {
            // pendant le run on laisse le job finir côté daemon ; on ferme juste la fenêtre
            setFlow({ step: 'closed' })
            if (flow.step === 'done') onChanged()
          }}
        >
          {flow.step === 'confirm' && (
            <ImportConfirm agent={flow.agent} onConfirm={() => launchImport(flow.agent)} onCancel={() => setFlow({ step: 'closed' })} />
          )}
          {flow.step === 'running' && <ImportProgress status={flow.status} />}
          {flow.step === 'done' && (
            <ImportDone agent={flow.agent} status={flow.status} onOpenReview={onOpenReview} onClose={() => { setFlow({ step: 'closed' }); onChanged() }} />
          )}
          {flow.step === 'failed' && <ErrorBanner message={flow.message} />}
        </Modal>
      )}
    </div>
  )
}

function MachineAgentCard({
  agent,
  busy,
  connectResult,
  dismissed,
  onConnect,
  onImport,
  onDismiss,
  onUndoDismiss,
}: {
  agent: DetectedAgent
  busy: boolean
  connectResult: ConnectAgentResult | undefined
  dismissed: boolean
  onConnect: () => void
  onImport: () => void
  onDismiss: () => void
  onUndoDismiss: () => void
}) {
  const { t } = useT()
  const connected = agent.already_connected !== null
  const dataLabel = describeData(t, agent)
  return (
    <div className="machine-card">
      <div className="machine-card-head">
        <strong>{agentIcon(agent.kind)} {agent.name}</strong>
        {connected ? <span className="badge badge-ok">{t('agents.card.connected')}</span> : <span className="badge badge-muted">{t('agents.card.notConnected')}</span>}
      </div>
      <div className="machine-card-meta muted">
        {agent.installed ? t('agents.card.cliInstalled') : t('agents.card.cliAbsent')}
        {dataLabel && <> · {dataLabel}</>}
      </div>
      {connectResult && (
        <p className={connectResult.registered.registered ? 'machine-connect-ok' : 'machine-connect-warn'}>
          {connectResult.registered.registered
            ? t('agents.card.connectOk', { hint: connectResult.restart_hint ?? '' })
            : t('agents.card.connectWarn', { detail: connectResult.registered.detail })}
        </p>
      )}
      <div className="machine-card-actions">
        {!connected && (
          <button type="button" className="btn btn-primary" onClick={onConnect} disabled={busy}>
            {busy ? t('agents.card.connecting') : t('agents.card.connect')}
          </button>
        )}
        {connected && dataLabel && !dismissed && (
          <>
            <button type="button" className="btn btn-primary" onClick={onImport}>
              {t('agents.card.import')}
            </button>
            <button type="button" className="btn btn-ghost" onClick={onDismiss}>
              {t('agents.card.startFresh')}
            </button>
          </>
        )}
        {connected && dataLabel && dismissed && (
          <span className="muted">
            {t('agents.card.startFreshNote')}{' '}
            <button type="button" className="btn-link" onClick={onUndoDismiss}>
              {t('agents.card.undoDismiss')}
            </button>
          </span>
        )}
      </div>
    </div>
  )
}

function agentIcon(kind: DetectedAgent['kind']): string {
  if (kind === 'claude-code') return '🤖'
  if (kind === 'codex') return '🧠'
  if (kind === 'openclaw') return '🦞'
  return '🖱️'
}

/** « 122 conversations trouvées » / « Mémoire OpenClaw : 3 573 souvenirs ». */
function describeData(t: Translate, agent: DetectedAgent): string | null {
  if (agent.data_found.transcript_files !== undefined) {
    const n = agent.data_found.transcript_files
    const key = n > 1 ? 'agents.data.conversations.plural' : 'agents.data.conversations.one'
    return t(key, { n: n.toLocaleString('fr-FR') })
  }
  if (agent.data_found.legacy_db) {
    return t('agents.data.legacy', { n: agent.data_found.legacy_db.fact_count.toLocaleString('fr-FR') })
  }
  return null
}

function ImportConfirm({ agent, onConfirm, onCancel }: { agent: DetectedAgent; onConfirm: () => void; onCancel: () => void }) {
  const { t } = useT()
  const isLegacy = agent.kind === 'openclaw'
  return (
    <div className="import-confirm">
      <p>
        <strong>{t('agents.confirm.source')}</strong>
        {describeData(t, agent)}
        {isLegacy && agent.data_found.legacy_db && <span className="muted"> ({agent.data_found.legacy_db.path})</span>}
      </p>
      {isLegacy ? (
        <p className="muted">
          {t('agents.confirm.legacyBody')}
        </p>
      ) : (
        <p className="muted">
          {t('agents.confirm.transcriptsBefore')}<strong>{t('agents.confirm.transcriptsDormant')}</strong>{t('agents.confirm.transcriptsAfter')}
        </p>
      )}
      <div className="modal-foot">
        <button type="button" className="btn btn-ghost" onClick={onCancel}>
          {t('agents.confirm.cancel')}
        </button>
        <button type="button" className="btn btn-primary" onClick={onConfirm}>
          {t('agents.confirm.launch')}
        </button>
      </div>
    </div>
  )
}

function ImportProgress({ status }: { status: ImportJobStatus | null }) {
  const { t } = useT()
  const p = status?.progress
  const total = p && p.files_total > 0 ? p.files_total : 1
  const done = p ? Math.min(p.files_done, total) : 0
  const percent = Math.round((done / total) * 100)
  return (
    <div className="import-progress">
      <p>{t('agents.progress.running')}</p>
      <div className="progress-track" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={percent}>
        <div className="progress-fill" style={{ width: `${percent}%` }} />
      </div>
      <p className="muted">
        {p ? t('agents.progress.detail', { done: p.files_done, total: p.files_total, facts: p.facts_imported.toLocaleString('fr-FR') }) : t('agents.progress.starting')}
      </p>
    </div>
  )
}

function ImportDone({
  agent,
  status,
  onOpenReview,
  onClose,
}: {
  agent: DetectedAgent
  status: ImportJobStatus
  onOpenReview?: () => void
  onClose: () => void
}) {
  const { t } = useT()
  const n = status.progress.facts_imported
  const isLegacy = agent.kind === 'openclaw'
  return (
    <div className="import-done">
      {isLegacy ? (
        <p>
          ✓ <strong>{t('agents.done.legacyStrong', { n: n.toLocaleString('fr-FR') })}</strong>{t('agents.done.legacyAfter')}
        </p>
      ) : (
        <p>
          ✓ <strong>{t(n > 1 ? 'agents.done.transcriptsStrong.plural' : 'agents.done.transcriptsStrong.one', { n: n.toLocaleString('fr-FR') })}</strong>{t('agents.done.transcriptsAfter')}
        </p>
      )}
      {status.errors.length > 0 && (
        <details className="import-errors">
          <summary>{t('agents.done.errorsSummary', { n: status.errors.length })}</summary>
          <ul>
            {status.errors.slice(0, 10).map((e, i) => (
              <li key={i} className="muted">{e}</li>
            ))}
          </ul>
        </details>
      )}
      <div className="modal-foot">
        <button type="button" className="btn btn-ghost" onClick={onClose}>
          {t('agents.done.close')}
        </button>
        {!isLegacy && onOpenReview && (
          <button type="button" className="btn btn-primary" onClick={onOpenReview}>
            {t('agents.done.openReview')}
          </button>
        )}
      </div>
    </div>
  )
}

function AgentList({ agents, onRevoke, onDelete }: { agents: AgentEntry[]; onRevoke: (id: string) => void; onDelete: (id: string) => void }) {
  const { t } = useT()
  if (agents.length === 0) return null
  return (
    <ul className="agent-list">
      {agents.map(({ instance, assistant_type }) => {
        const revoked = instance.revoked_at !== null
        const pending = !revoked && instance.last_seen_at === null
        return (
          <li key={instance.id} className={`agent-row${revoked ? ' agent-revoked' : ''}`}>
            <div className="agent-id">
              <strong>{agentTypeLabel(assistant_type)}</strong>
              <span className="muted">{t('agents.list.on', { machine: instance.machine_id })}</span>
            </div>
            <div className="agent-meta">
              {revoked ? (
                <span className="badge badge-muted">{t('agents.list.revoked')}</span>
              ) : pending ? (
                <span className="badge badge-warn">{t('agents.list.pending')}</span>
              ) : (
                <span className="badge badge-ok">{t('agents.list.connected')}</span>
              )}
              <span className="muted">
                {instance.last_seen_at ? t('agents.list.seenAt', { date: formatDate(instance.last_seen_at) }) : t('agents.list.addedAt', { date: formatDate(instance.created_at) })}
              </span>
            </div>
            {!revoked && !pending && <AgentExpertise instanceId={instance.id} />}
            <div className="agent-actions">
              {!revoked && (
                <ConfirmButton label={t('agents.list.revoke')} confirmLabel={t('agents.list.revokeConfirm')} onConfirm={() => onRevoke(instance.id)} />
              )}
              <ConfirmButton
                label={t('agents.list.delete')}
                confirmLabel={t('agents.list.deleteConfirm')}
                onConfirm={() => onDelete(instance.id)}
              />
            </div>
          </li>
        )
      })}
    </ul>
  )
}

/** Domaines de maîtrise + forces/faiblesses de l'agent (couches 8 + 19). */
function AgentExpertise({ instanceId }: { instanceId: string }) {
  const { t } = useT()
  const [domains, setDomains] = useState<ExpertiseDomain[]>([])
  const [self, setSelf] = useState<SelfObservation[]>([])
  useEffect(() => {
    getExpertise(instanceId)
      .then(d => setDomains(d.slice(0, 4)))
      .catch(() => setDomains([]))
    // analyse fraîche du comportement puis lecture
    deriveSelf(instanceId)
      .catch(() => 0)
      .then(() => getSelfObservations(instanceId))
      .then(o => setSelf(o.slice(0, 3)))
      .catch(() => setSelf([]))
  }, [instanceId])
  if (domains.length === 0 && self.length === 0) return null
  return (
    <div className="agent-insights">
      {domains.length > 0 && (
        <div className="agent-expertise" title={t('agents.expertise.title')}>
          <span className="muted">{t('agents.expertise.label')}</span>
          {domains.map(d => <span key={d.domain} className="badge badge-theme">{d.domain}</span>)}
        </div>
      )}
      {self.length > 0 && (
        <div className="agent-self">
          {self.map(o => (
            <span key={o.id} className={`badge ${o.kind === 'weakness' ? 'badge-warn' : 'badge-muted'}`} title={o.kind}>
              {o.kind === 'strength' ? '✓ ' : o.kind === 'weakness' ? '⚠ ' : '• '}
              {o.observation.length > 60 ? o.observation.slice(0, 57) + '…' : o.observation}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

function PairingCode({ result, onRegenerate }: { result: PairResult; onRegenerate: () => void }) {
  const { t } = useT()
  const [secondsLeft, setSecondsLeft] = useState(PAIRING_TTL_SECONDS)

  useEffect(() => {
    setSecondsLeft(PAIRING_TTL_SECONDS)
    const id = window.setInterval(() => setSecondsLeft(s => Math.max(0, s - 1)), 1000)
    return () => window.clearInterval(id)
  }, [result.pairing_code])

  const expired = secondsLeft === 0
  const mm = Math.floor(secondsLeft / 60)
  const ss = String(secondsLeft % 60).padStart(2, '0')

  return (
    <div className="pairing">
      <p>
        {t('agents.pairing.instructions')}
      </p>
      <div className="pairing-code" aria-label={t('agents.pairing.codeLabel')}>
        {result.pairing_code}
      </div>
      <div className="command-row">
        <code className="command">{result.command}</code>
        <CopyButton text={result.command} label={t('agents.pairing.copy')} />
      </div>
      {expired ? (
        <div className="pairing-expired">
          <span>{t('agents.pairing.expired')}</span>
          <button type="button" className="btn btn-primary" onClick={onRegenerate}>
            {t('agents.pairing.regenerate')}
          </button>
        </div>
      ) : (
        <p className="muted">
          {t('agents.pairing.expiresBefore')}<strong>{mm}:{ss}</strong>{t('agents.pairing.expiresAfter')}
        </p>
      )}
    </div>
  )
}

function Modal({ title, children, onClose }: { title: string; children: ReactNode; onClose: () => void }) {
  const { t } = useT()
  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true" aria-label={title}>
      <div className="modal">
        <header className="modal-head">
          <h2>{title}</h2>
          <button type="button" className="btn btn-ghost" onClick={onClose} aria-label={t('agents.modal.close')}>
            ✕
          </button>
        </header>
        {children}
      </div>
    </div>
  )
}
