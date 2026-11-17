/**
 * App — coquille de navigation (5 écrans) + sélecteur de mode de capture
 * toujours visible (pause = exigence spec §13) + écran d'accueil quand
 * aucun token admin n'est présent (l'UI s'ouvre normalement via le CLI
 * `memoria`, qui passe le token dans l'URL).
 */
import { useCallback, useEffect, useState } from 'react'
import { getAgents, getCaptureMode, getVersion, hasToken, setCaptureMode, type CaptureMode } from './api'
import { useT, LANGS, type Lang } from './i18n'
import { Dashboard } from './screens/Dashboard'
import { Agents } from './screens/Agents'
import { Memory } from './screens/Memory'
import { Review } from './screens/Review'
import { Themes } from './screens/Themes'
import { Patterns } from './screens/Patterns'
import { Procedures } from './screens/Procedures'
import { Revisions } from './screens/Revisions'
import { Sharing } from './screens/Sharing'
import { Persons } from './screens/Persons'
import { Vault } from './screens/Vault'
import { System } from './screens/System'
import { Audit } from './screens/Audit'
import { Onboarding } from './screens/Onboarding'
import { Settings } from './screens/Settings'
import { Docs } from './screens/Docs'

type ScreenId =
  | 'dashboard' | 'agents' | 'memory' | 'themes' | 'patterns' | 'procedures'
  | 'review' | 'revisions' | 'sharing' | 'persons' | 'vault' | 'system' | 'audit' | 'settings' | 'docs'

// Les libellés viennent de l'i18n : nav.<id> (cf. messages/fr.ts).
const NAV_IDS: ScreenId[] = [
  'dashboard', 'agents', 'memory', 'themes', 'patterns', 'procedures',
  'review', 'revisions', 'sharing', 'persons', 'vault', 'system', 'audit', 'settings', 'docs',
]

// clés i18n : capture.<key> (label) + capture.hint.<key>
const MODES: Array<{ id: CaptureMode; key: 'auto' | 'review' | 'pause' }> = [
  { id: 'auto-private', key: 'auto' },
  { id: 'review-first', key: 'review' },
  { id: 'incognito', key: 'pause' },
]

export function App() {
  const { t } = useT()
  // Le token est adopté avant le rendu (main.tsx) ; sa présence ne change plus ensuite.
  const [authed] = useState(hasToken)
  const [screen, setScreen] = useState<ScreenId>('dashboard')
  // null = on ne sait pas encore (chargement) ; true = 0 agent → onboarding.
  const [onboarding, setOnboarding] = useState<boolean | null>(null)

  useEffect(() => {
    if (!authed) return
    getAgents()
      .then(agents => setOnboarding(agents.length === 0))
      .catch(() => setOnboarding(false))
  }, [authed])

  if (!authed) return <Welcome />
  if (onboarding === null) return <div className="welcome"><div className="spinner" aria-hidden /></div>
  if (onboarding) return <Onboarding onDone={() => setOnboarding(false)} />

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          Memoria
          <span className="brand-sub">{t('brand.sub')}</span>
        </div>
        <LangSwitch />
        <nav className="nav" aria-label="Navigation principale">
          {NAV_IDS.map(id => (
            <button
              key={id}
              type="button"
              className={`nav-item${screen === id ? ' nav-active' : ''}`}
              onClick={() => setScreen(id)}
            >
              {t(`nav.${id}`)}
            </button>
          ))}
        </nav>
        <CaptureModeSwitch />
        <div className="sidebar-foot muted">
          {t('foot.local')}
          <VersionFoot />
        </div>
      </aside>
      <main className="content">
        {screen === 'dashboard' && <Dashboard onConnect={() => setScreen('agents')} onConfigure={() => setScreen('settings')} />}
        {screen === 'agents' && <Agents onOpenReview={() => setScreen('review')} />}
        {screen === 'memory' && <Memory />}
        {screen === 'themes' && <Themes />}
        {screen === 'patterns' && <Patterns />}
        {screen === 'procedures' && <Procedures />}
        {screen === 'review' && <Review />}
        {screen === 'revisions' && <Revisions />}
        {screen === 'sharing' && <Sharing />}
        {screen === 'persons' && <Persons />}
        {screen === 'vault' && <Vault />}
        {screen === 'system' && <System />}
        {screen === 'audit' && <Audit />}
        {screen === 'settings' && <Settings />}
        {screen === 'docs' && <Docs />}
      </main>
    </div>
  )
}

/** Pause/capture toujours accessible, quel que soit l'écran (spec §13). */
function CaptureModeSwitch() {
  const { t } = useT()
  const [mode, setMode] = useState<CaptureMode | null>(null)

  useEffect(() => {
    getCaptureMode()
      .then(setMode)
      .catch(() => setMode(null))
  }, [])

  const change = useCallback((next: CaptureMode) => {
    setMode(next) // optimiste — l'échec remet l'état réel
    setCaptureMode(next).catch(() => {
      getCaptureMode()
        .then(setMode)
        .catch(() => setMode(null))
    })
  }, [])

  if (mode === null) return null

  const current = MODES.find(m => m.id === mode)
  return (
    <div className="capture-switch">
      <span className="field-label">{t('capture.title')}</span>
      <div className="capture-options" role="radiogroup" aria-label={t('capture.title')}>
        {MODES.map(m => (
          <button
            key={m.id}
            type="button"
            role="radio"
            aria-checked={mode === m.id}
            title={t(`capture.hint.${m.key}`)}
            className={`capture-option${mode === m.id ? ' capture-active' : ''}${m.id === 'incognito' && mode === m.id ? ' capture-paused' : ''}`}
            onClick={() => change(m.id)}
          >
            {t(`capture.${m.key}`)}
          </button>
        ))}
      </div>
      {current && <p className="muted capture-hint">{t(`capture.hint.${current.key}`)}</p>}
    </div>
  )
}

/** Sélecteur de langue de l'interface (barre latérale). */
function LangSwitch() {
  const { t, lang, setLang } = useT()
  return (
    <div className="lang-switch">
      <label className="field-label" htmlFor="lang-select">{t('lang.title')}</label>
      <select
        id="lang-select"
        className="lang-select"
        value={lang}
        onChange={e => setLang(e.target.value as Lang)}
      >
        {LANGS.map(l => (
          <option key={l.code} value={l.code}>
            {l.flag} {l.label}
          </option>
        ))}
      </select>
    </div>
  )
}

/** Version installée, affichée discrètement en pied de barre latérale. */
function VersionFoot() {
  const [label, setLabel] = useState<string | null>(null)
  useEffect(() => {
    getVersion()
      .then(v => setLabel(v.sha ? `v${v.version} · ${v.sha}` : `v${v.version}`))
      .catch(() => setLabel(null))
  }, [])
  if (!label) return null
  return <div className="sidebar-version">{label}</div>
}

function Welcome() {
  return (
    <div className="welcome">
      <div className="welcome-card">
        <div className="brand">Memoria</div>
        <h1>Votre mémoire locale vous attend</h1>
        <p>
          Pour ouvrir ce tableau de bord en toute sécurité, lancez la commande suivante dans votre
          terminal — elle ouvre cette page avec votre clé d’accès personnelle :
        </p>
        <pre className="command">memoria</pre>
        <p className="muted">
          Tout reste sur votre machine : cette interface ne parle qu’au service Memoria qui tourne en
          local.
        </p>
      </div>
    </div>
  )
}
