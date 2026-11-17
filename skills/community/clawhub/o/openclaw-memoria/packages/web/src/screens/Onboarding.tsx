/**
 * Onboarding — premier lancement (spec §13), ton « tout est local ».
 * Étapes : bienvenue → stockage → MOTEUR D'INTELLIGENCE (obligatoire) →
 * connecter un 1er agent. L'étape moteur est LE rempart anti-mort-silencieuse :
 * on ne termine pas sans moteur d'extraction prêt, SAUF choix explicite du
 * mode dégradé (encart rouge qui dit ce que ça implique).
 */
import { useCallback, useEffect, useState } from 'react'
import { Wizard, type WizardStep } from '../components/Wizard'
import { useT } from '../i18n'
import {
  ApiError,
  copyOpenClawKey,
  getDoctor,
  getLlmHealth,
  getOllamaPullStatus,
  pairAgent,
  setExtractionProvider,
  startOllamaPull,
  type AgentType,
  type DoctorReport,
  type LlmHealth,
  type LlmProviderName,
  type OllamaPullStatus,
  type PairResult,
} from '../api'

const AGENT_TYPES: Array<{ id: AgentType; label: string }> = [
  { id: 'claude-code', label: 'Claude Code' },
  { id: 'codex', label: 'Codex' },
  { id: 'openclaw', label: 'OpenClaw' },
  { id: 'generic', label: 'Autre (MCP)' },
]

type EngineChoice = LlmProviderName | 'openclaw'

/** Modèle conseillé par provider (lmstudio = premier modèle chargé). */
const DEFAULT_MODELS: Partial<Record<LlmProviderName, string>> = {
  ollama: 'qwen2.5:3b',
  openai: 'gpt-4o-mini',
  anthropic: 'claude-haiku-4-5-20251001',
  openrouter: 'openai/gpt-4o-mini',
}

type EngineState = 'ready' | 'config' | 'off'

function StateBadge({ state }: { state: EngineState }) {
  const { t } = useT()
  if (state === 'ready') return <span className="badge badge-ok">{t('onboarding.badge.ready')}</span>
  if (state === 'config') return <span className="badge badge-warn">{t('onboarding.badge.config')}</span>
  return <span className="badge badge-muted">{t('onboarding.badge.off')}</span>
}

export function Onboarding({ onDone }: { onDone: () => void }) {
  const { t } = useT()
  const [step, setStep] = useState(0)
  const [doctor, setDoctor] = useState<DoctorReport | null>(null)
  const [type, setType] = useState<AgentType>('claude-code')
  const [pair, setPair] = useState<PairResult | null>(null)
  const [copied, setCopied] = useState(false)

  // --- état de l'étape moteur
  const [health, setHealth] = useState<LlmHealth | null>(null)
  const [healthUnavailable, setHealthUnavailable] = useState(false)
  const [checking, setChecking] = useState(false)
  const [selected, setSelected] = useState<EngineChoice | null>(null)
  const [chosenNote, setChosenNote] = useState<string | null>(null)
  const [engineError, setEngineError] = useState<string | null>(null)
  const [degraded, setDegraded] = useState(false)
  const [testResult, setTestResult] = useState<LlmHealth | null>(null)
  // téléchargement Ollama en cours (polling 1 s)
  const [pulling, setPulling] = useState<string | null>(null)
  const [pullStatus, setPullStatus] = useState<OllamaPullStatus | null>(null)

  useEffect(() => {
    getDoctor().then(setDoctor).catch(() => setDoctor(null))
  }, [])

  const refreshHealth = useCallback(async (): Promise<LlmHealth | null> => {
    setChecking(true)
    try {
      const h = await getLlmHealth()
      setHealth(h)
      setHealthUnavailable(false)
      return h
    } catch {
      // route absente (vieux service) : on n'affiche pas l'étape en bloquant
      setHealthUnavailable(true)
      return null
    } finally {
      setChecking(false)
    }
  }, [])

  useEffect(() => {
    if (step === 2 && health === null && !healthUnavailable) void refreshHealth()
  }, [step, health, healthUnavailable, refreshHealth])

  /** Persiste le moteur choisi via POST /v1/admin/llm_extraction. */
  const persistChoice = useCallback(async (engine: LlmProviderName, h: LlmHealth | null): Promise<void> => {
    const model = engine === 'lmstudio' ? h?.options.lmstudio.models[0] : DEFAULT_MODELS[engine]
    try {
      await setExtractionProvider(engine, model)
      setChosenNote(t('onboarding.engine.saved', { engine, suffix: model ? ` / ${model}` : '' }))
      setEngineError(null)
    } catch (err) {
      setEngineError(err instanceof ApiError ? err.message : t('onboarding.engine.saveError'))
    }
  }, [t])

  // polling du téléchargement Ollama (barres de progression)
  useEffect(() => {
    if (!pulling) return
    const timer = setInterval(() => {
      getOllamaPullStatus()
        .then(s => {
          setPullStatus(s)
          if (!s.running) {
            setPulling(null)
            if (s.error) setEngineError(t('onboarding.pull.failed', { model: s.model ?? t('onboarding.pull.modelFallback'), error: s.error }))
            void refreshHealth().then(h => {
              // une fois Ollama complet, on persiste le choix automatiquement
              if (h?.options.ollama.available) void persistChoice('ollama', h)
            })
          }
        })
        .catch(() => setPulling(null))
    }, 1000)
    return () => clearInterval(timer)
  }, [pulling, refreshHealth, persistChoice, t])

  const choose = useCallback(
    async (engine: EngineChoice) => {
      setSelected(engine)
      setTestResult(null)
      setChosenNote(null)
      if (!health) return
      const o = health.options
      if (engine === 'openclaw') {
        // copie la clé OpenClaw vers ~/.<provider>/api_key puis bascule dessus
        const provider = o.openclaw.provider
        if (!provider) return
        try {
          await copyOpenClawKey(provider)
          const h = await refreshHealth()
          await persistChoice(provider, h)
        } catch (err) {
          setEngineError(err instanceof ApiError ? err.message : t('onboarding.engine.copyError'))
        }
        return
      }
      const ready =
        engine === 'ollama' ? o.ollama.available
        : engine === 'lmstudio' ? o.lmstudio.available && o.lmstudio.models.length > 0
        : o[engine].available
      if (ready) await persistChoice(engine, health)
    },
    [health, persistChoice, refreshHealth, t],
  )

  const startPull = useCallback((model: string) => {
    setEngineError(null)
    setPullStatus({ running: true, model, percent: null, status: t('onboarding.pull.starting'), error: null })
    startOllamaPull(model)
      .then(() => setPulling(model))
      .catch(err => {
        setPullStatus(null)
        setEngineError(err instanceof ApiError ? err.message : t('onboarding.pull.error'))
      })
  }, [t])

  const reverify = useCallback(async () => {
    setTestResult(null)
    const h = await refreshHealth()
    if (h && selected && selected !== 'openclaw') {
      const o = h.options
      const ready =
        selected === 'ollama' ? o.ollama.available
        : selected === 'lmstudio' ? o.lmstudio.available && o.lmstudio.models.length > 0
        : o[selected].available
      if (ready && !h.extraction.available) await persistChoice(selected, h)
      else if (ready) setChosenNote(t('onboarding.engine.ready', { provider: h.extraction.provider ?? '', model: h.extraction.model ?? '' }))
    }
  }, [refreshHealth, selected, persistChoice, t])

  const runTest = useCallback(async () => {
    const h = await refreshHealth()
    setTestResult(h)
  }, [refreshHealth])

  const startPairing = async () => {
    try {
      setPair(await pairAgent(type))
    } catch (err) {
      setPair(null)
      console.warn('pairing onboarding échoué', err instanceof ApiError ? err.message : err)
    }
  }

  const engineOk = health?.extraction.available === true
  const engineGateOpen = engineOk || degraded || healthUnavailable

  const steps: WizardStep[] = [
    {
      id: 'welcome',
      title: t('onboarding.welcome.title'),
      render: () => (
        <div className="ob-step">
          <p className="ob-lead">{t('onboarding.welcome.lead')}</p>
          <p>
            {t('onboarding.welcome.body')} <strong>{t('onboarding.welcome.bodyStrong')}</strong>
          </p>
          <p className="muted">{t('onboarding.welcome.duration')}</p>
        </div>
      ),
    },
    {
      id: 'storage',
      title: t('onboarding.storage.title'),
      render: () => (
        <div className="ob-step">
          <p>{t('onboarding.storage.lead')}</p>
          <pre className="command">{doctor?.storage_root ?? '~/.memoria/data'}</pre>
          <p className="muted">{t('onboarding.storage.note')}</p>
        </div>
      ),
    },
    {
      id: 'engine',
      title: t('onboarding.engine.title'),
      render: () => (
        <EngineStep
          health={health}
          healthUnavailable={healthUnavailable}
          checking={checking}
          selected={selected}
          chosenNote={chosenNote}
          engineError={engineError}
          testResult={testResult}
          pullStatus={pullStatus}
          pulling={pulling}
          degraded={degraded}
          onChoose={engine => void choose(engine)}
          onPull={startPull}
          onReverify={() => void reverify()}
          onTest={() => void runTest()}
          onDegraded={() => {
            setDegraded(true)
            setStep(3)
          }}
        />
      ),
    },
    {
      id: 'agent',
      title: t('onboarding.agent.title'),
      render: () => (
        <div className="ob-step">
          {degraded && (
            <p className="provider-missing">
              {t('onboarding.agent.degraded')}
            </p>
          )}
          {!pair ? (
            <>
              <p>{t('onboarding.agent.question')}</p>
              <div className="ob-types">
                {AGENT_TYPES.map(at => (
                  <button key={at.id} type="button" className={`capture-option${type === at.id ? ' capture-active' : ''}`} onClick={() => setType(at.id)}>
                    {at.id === 'generic' ? t('onboarding.agent.typeGeneric') : at.label}
                  </button>
                ))}
              </div>
              <button type="button" className="btn btn-primary" onClick={() => void startPairing()}>{t('onboarding.agent.generate')}</button>
            </>
          ) : (
            <>
              <p>{t('onboarding.agent.pasteCommand')}</p>
              <pre className="command">{pair.command}</pre>
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => { void navigator.clipboard.writeText(pair.command); setCopied(true) }}
              >
                {copied ? t('onboarding.agent.copied') : t('onboarding.agent.copy')}
              </button>
              <p className="muted">{t('onboarding.agent.codeLabel')}<strong>{pair.pairing_code}</strong>{t('onboarding.agent.codeValidity')}</p>
            </>
          )}
        </div>
      ),
    },
  ]

  return (
    <div className="welcome">
      <div className="welcome-card ob-card">
        <div className="brand">Memo<span style={{ color: 'var(--accent)' }}>ria</span></div>
        <Wizard
          steps={steps}
          current={step}
          onBack={() => setStep(s => Math.max(0, s - 1))}
          onNext={() => setStep(s => Math.min(steps.length - 1, s + 1))}
          onFinish={onDone}
          nextLabel={step === steps.length - 1 ? t('onboarding.wizard.finish') : t('onboarding.wizard.continue')}
          nextDisabled={step === 2 && !engineGateOpen}
        />
      </div>
    </div>
  )
}

// ------------------------------------------------------- étape moteur (A4)

function EngineStep({
  health,
  healthUnavailable,
  checking,
  selected,
  chosenNote,
  engineError,
  testResult,
  pullStatus,
  pulling,
  degraded,
  onChoose,
  onPull,
  onReverify,
  onTest,
  onDegraded,
}: {
  health: LlmHealth | null
  healthUnavailable: boolean
  checking: boolean
  selected: EngineChoice | null
  chosenNote: string | null
  engineError: string | null
  testResult: LlmHealth | null
  pullStatus: OllamaPullStatus | null
  pulling: string | null
  degraded: boolean
  onChoose: (engine: EngineChoice) => void
  onPull: (model: string) => void
  onReverify: () => void
  onTest: () => void
  onDegraded: () => void
}) {
  const { t } = useT()
  if (healthUnavailable) {
    return (
      <div className="ob-step">
        <p className="muted">
          {t('onboarding.engine.unavailable')}
        </p>
      </div>
    )
  }
  if (!health) {
    return (
      <div className="ob-step">
        <div className="spinner-row"><span className="spinner" aria-hidden /> {t('onboarding.engine.detecting')}</div>
      </div>
    )
  }

  const o = health.options
  const cards: Array<{ id: EngineChoice; icon: string; label: string; hint: string; state: EngineState }> = [
    {
      id: 'ollama',
      icon: '🦙',
      label: 'Ollama',
      hint: t('onboarding.engine.ollamaHint'),
      state: o.ollama.available ? 'ready' : o.ollama.serverUp || o.ollama.binaryInPath ? 'config' : 'off',
    },
    {
      id: 'lmstudio',
      icon: '🖥️',
      label: 'LM Studio',
      hint: t('onboarding.engine.lmstudioHint'),
      state: o.lmstudio.available && o.lmstudio.models.length > 0 ? 'ready' : o.lmstudio.available ? 'config' : 'off',
    },
    { id: 'openai', icon: '🔑', label: 'OpenAI', hint: t('onboarding.engine.apiKeyHint'), state: o.openai.available ? 'ready' : 'config' },
    { id: 'openrouter', icon: '🔑', label: 'OpenRouter', hint: t('onboarding.engine.apiKeyHint'), state: o.openrouter.available ? 'ready' : 'config' },
    { id: 'anthropic', icon: '🔑', label: 'Anthropic', hint: t('onboarding.engine.apiKeyHint'), state: o.anthropic.available ? 'ready' : 'config' },
  ]
  if (o.openclaw.available && o.openclaw.reusable && o.openclaw.provider) {
    cards.push({
      id: 'openclaw',
      icon: '🔁',
      label: t('onboarding.engine.openclawLabel'),
      hint: t('onboarding.engine.openclawHint', { provider: o.openclaw.provider }),
      state: 'ready',
    })
  }

  return (
    <div className="ob-step">
      <p className="muted">
        {t('onboarding.engine.lead')} <strong>{t('onboarding.engine.leadStrong')}</strong>.
      </p>

      <div className="engine-grid">
        {cards.map(c => (
          <button
            key={c.id}
            type="button"
            className={`engine-card${selected === c.id ? ' engine-active' : ''}`}
            onClick={() => onChoose(c.id)}
          >
            <span className="engine-head">
              <span>{c.icon} <strong>{c.label}</strong></span>
              <StateBadge state={c.state} />
            </span>
            <span className="muted engine-hint">{c.hint}</span>
          </button>
        ))}
      </div>

      {engineError && <div className="error-banner">{engineError}</div>}
      {chosenNote && <p className="engine-note">{chosenNote}</p>}

      {selected === 'ollama' && <OllamaGuide o={o.ollama} pulling={pulling} pullStatus={pullStatus} onPull={onPull} onReverify={onReverify} checking={checking} />}
      {selected === 'lmstudio' && <LmStudioGuide o={o.lmstudio} onReverify={onReverify} checking={checking} />}
      {(selected === 'openai' || selected === 'openrouter' || selected === 'anthropic') && (
        <ApiKeyGuide provider={selected} available={o[selected].available} onReverify={onReverify} checking={checking} />
      )}

      <div className="engine-test">
        <button type="button" className="btn btn-ghost" disabled={checking} onClick={onTest}>
          {checking ? t('onboarding.engine.checking') : t('onboarding.engine.test')}
        </button>
        {testResult && (
          <ul className="engine-results">
            <li className={testResult.extraction.available ? 'ok' : 'ko'}>
              {testResult.extraction.available
                ? t('onboarding.engine.extractionReady', { provider: testResult.extraction.provider ?? '', model: testResult.extraction.model ?? '' })
                : t('onboarding.engine.extractionFail', { reason: testResult.extraction.reason ?? t('onboarding.engine.reasonUnknown') })}
            </li>
            <li className={testResult.embeddings.available ? 'ok' : 'ko'}>
              {testResult.embeddings.available
                ? t('onboarding.engine.embeddingsReady', { provider: testResult.embeddings.provider ?? '', model: testResult.embeddings.model ?? '' })
                : t('onboarding.engine.embeddingsWarn', { reason: testResult.embeddings.reason ?? t('onboarding.engine.embeddingsUnavailable') })}
            </li>
          </ul>
        )}
      </div>

      {!health.extraction.available && !degraded && (
        <div className="degraded-box">
          <p>
            <strong>{t('onboarding.engine.degradedWarnStrong')}</strong> {t('onboarding.engine.degradedWarnBody')}
          </p>
          <button type="button" className="btn btn-danger" onClick={onDegraded}>
            {t('onboarding.engine.continueDegraded')}
          </button>
        </div>
      )}
    </div>
  )
}

function OllamaGuide({
  o,
  pulling,
  pullStatus,
  onPull,
  onReverify,
  checking,
}: {
  o: LlmHealth['options']['ollama']
  pulling: string | null
  pullStatus: OllamaPullStatus | null
  onPull: (model: string) => void
  onReverify: () => void
  checking: boolean
}) {
  const { t } = useT()
  if (!o.serverUp) {
    return (
      <div className="engine-guide">
        <p>
          {t('onboarding.ollama.step1')} <a href="https://ollama.com/download" target="_blank" rel="noreferrer">ollama.com/download</a>
        </p>
        <p>{t('onboarding.ollama.step2')}</p>
        <button type="button" className="btn btn-primary" disabled={checking} onClick={onReverify}>
          {t('onboarding.ollama.recheck')}
        </button>
      </div>
    )
  }
  const missing: Array<{ model: string; label: string }> = []
  if (!o.hasExtractModel) missing.push({ model: 'qwen2.5:3b', label: t('onboarding.ollama.pullExtract') })
  if (!o.hasEmbedModel) missing.push({ model: 'nomic-embed-text', label: t('onboarding.ollama.pullEmbed') })
  if (missing.length === 0) {
    return <div className="engine-guide"><p className="engine-note">{t('onboarding.ollama.ready', { count: o.models.length })}</p></div>
  }
  return (
    <div className="engine-guide">
      <p>{t('onboarding.ollama.missingIntro', { what: missing.length === 1 ? t('onboarding.ollama.missingOne') : t('onboarding.ollama.missingTwo') })}</p>
      {missing.map(m => {
        const isPullingThis = pullStatus?.model === m.model && (pullStatus.running || pulling === m.model)
        return (
          <div key={m.model} className="pull-row">
            <button
              type="button"
              className="btn btn-primary"
              disabled={pulling !== null || pullStatus?.running === true}
              onClick={() => onPull(m.model)}
            >
              {m.label}
            </button>
            {isPullingThis && (
              <div className="progress" role="progressbar" aria-valuenow={pullStatus?.percent ?? undefined}>
                <div className="progress-fill" style={{ width: `${pullStatus?.percent ?? 2}%` }} />
                <span className="progress-label">
                  {pullStatus?.percent !== null && pullStatus?.percent !== undefined ? `${pullStatus.percent} %` : pullStatus?.status ?? '…'}
                </span>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

function LmStudioGuide({ o, onReverify, checking }: { o: LlmHealth['options']['lmstudio']; onReverify: () => void; checking: boolean }) {
  const { t } = useT()
  return (
    <div className="engine-guide">
      {!o.available ? (
        <>
          <p>{t('onboarding.lmstudio.step1')} <a href="https://lmstudio.ai" target="_blank" rel="noreferrer">lmstudio.ai</a></p>
          <p>{t('onboarding.lmstudio.step2')}</p>
          <p>{t('onboarding.lmstudio.step3a')}<strong>Developer</strong>{t('onboarding.lmstudio.step3b')}</p>
        </>
      ) : o.models.length === 0 ? (
        <p>{t('onboarding.lmstudio.noModel')}</p>
      ) : (
        <p className="engine-note">{t('onboarding.lmstudio.ready', { model: o.models[0] ?? '' })}</p>
      )}
      <button type="button" className="btn btn-primary" disabled={checking} onClick={onReverify}>
        {t('onboarding.lmstudio.recheck')}
      </button>
    </div>
  )
}

function ApiKeyGuide({
  provider,
  available,
  onReverify,
  checking,
}: {
  provider: 'openai' | 'openrouter' | 'anthropic'
  available: boolean
  onReverify: () => void
  checking: boolean
}) {
  const { t } = useT()
  const command = `echo 'TA_CLÉ' > ~/.${provider}/api_key && chmod 600 ~/.${provider}/api_key`
  const providerName = provider === 'openai' ? 'OpenAI' : provider === 'openrouter' ? 'OpenRouter' : 'Anthropic'
  return (
    <div className="engine-guide">
      {available ? (
        <p className="engine-note">{t('onboarding.apikey.detected', { provider })}</p>
      ) : (
        <>
          <p>
            {t('onboarding.apikey.instructions', { provider: providerName })}
          </p>
          <pre className="command">mkdir -p ~/.{provider} && {command}</pre>
          <p className="muted">{t('onboarding.apikey.note')}</p>
        </>
      )}
      <button type="button" className="btn btn-primary" disabled={checking} onClick={onReverify}>
        {t('onboarding.apikey.recheck')}
      </button>
    </div>
  )
}
