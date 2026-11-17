/**
 * Petits composants partagés + helpers d'affichage.
 * Volontairement légers : pas de framework UI, juste du CSS maison.
 */
import { useEffect, useRef, useState, type ReactNode } from 'react'
import { ApiError } from '../api'

// ------------------------------------------------------------------- helpers

const dateFmt = new Intl.DateTimeFormat('fr-FR', { dateStyle: 'medium', timeStyle: 'short' })

export function formatDate(iso: string | null | undefined): string {
  if (!iso) return '—'
  const d = new Date(iso)
  return Number.isNaN(d.getTime()) ? iso : dateFmt.format(d)
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} o`
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} Ko`
  return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`
}

const AGENT_TYPE_LABELS: Record<string, string> = {
  'claude-code': 'Claude Code',
  codex: 'Codex',
  openclaw: 'OpenClaw',
  cursor: 'Cursor',
  robot: 'Robot',
  generic: 'Autre agent',
}

export function agentTypeLabel(type: string): string {
  return AGENT_TYPE_LABELS[type] ?? type
}

/** Traduit une erreur technique en message lisible — jamais de jargon brut. */
export function humanError(err: unknown): string {
  if (err instanceof ApiError) {
    if (err.status === 401) return 'Session expirée ou clé invalide — relancez `memoria` depuis votre terminal.'
    if (err.status === 404) return 'Cette fonction n’est pas encore disponible dans votre version du service Memoria.'
    return err.message
  }
  if (err instanceof TypeError) {
    return 'Le service Memoria ne répond pas. Vérifiez qu’il tourne (commande `memoria`).'
  }
  return err instanceof Error ? err.message : String(err)
}

// ---------------------------------------------------------------- chargement

export type LoadState<T> =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; data: T }

/**
 * Hook de chargement standard : loading → ready | error (+ reload).
 * Toute erreur est loggée ET affichée — pas de mort silencieuse.
 */
export function useLoad<T>(loader: () => Promise<T>, deps: readonly unknown[] = []): {
  state: LoadState<T>
  reload: () => void
} {
  const [state, setState] = useState<LoadState<T>>({ status: 'loading' })
  const [tick, setTick] = useState(0)
  const loaderRef = useRef(loader)
  loaderRef.current = loader

  useEffect(() => {
    let cancelled = false
    setState({ status: 'loading' })
    loaderRef.current().then(
      data => {
        if (!cancelled) setState({ status: 'ready', data })
      },
      (err: unknown) => {
        if (cancelled) return
        console.warn('memoria-ui : chargement échoué', err)
        setState({ status: 'error', message: humanError(err) })
      },
    )
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- deps maîtrisées par l'appelant
  }, [tick, ...deps])

  return { state, reload: () => setTick(t => t + 1) }
}

// --------------------------------------------------------------- composants

export function Spinner({ label = 'Chargement…' }: { label?: string }) {
  return (
    <div className="spinner-row" role="status">
      <span className="spinner" aria-hidden="true" />
      <span className="muted">{label}</span>
    </div>
  )
}

export function ErrorBanner({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="error-banner" role="alert">
      <span>{message}</span>
      {onRetry && (
        <button type="button" className="btn btn-ghost" onClick={onRetry}>
          Réessayer
        </button>
      )}
    </div>
  )
}

export function EmptyState({ title, body, action }: { title: string; body?: string; action?: ReactNode }) {
  return (
    <div className="empty-state">
      <h2>{title}</h2>
      {body && <p className="muted">{body}</p>}
      {action}
    </div>
  )
}

/** Copie dans le presse-papiers avec retour visuel ; l'échec est visible aussi. */
export function CopyButton({ text, label = 'Copier' }: { text: string; label?: string }) {
  const [feedback, setFeedback] = useState<'idle' | 'done' | 'failed'>('idle')

  const copy = () => {
    navigator.clipboard.writeText(text).then(
      () => setFeedback('done'),
      (err: unknown) => {
        console.warn('memoria-ui : copie presse-papiers refusée', err)
        setFeedback('failed')
      },
    )
    window.setTimeout(() => setFeedback('idle'), 2000)
  }

  return (
    <button type="button" className="btn btn-ghost" onClick={copy}>
      {feedback === 'done' ? 'Copié !' : feedback === 'failed' ? 'Échec de copie' : label}
    </button>
  )
}

/**
 * Bouton à confirmation en deux temps (pas de window.confirm) :
 * 1er clic = armé pendant 4 s, 2e clic = action.
 */
export function ConfirmButton({
  label,
  confirmLabel = 'Confirmer ?',
  onConfirm,
  disabled = false,
}: {
  label: string
  confirmLabel?: string
  onConfirm: () => void
  disabled?: boolean
}) {
  const [armed, setArmed] = useState(false)
  const timer = useRef<number | null>(null)

  useEffect(
    () => () => {
      if (timer.current !== null) window.clearTimeout(timer.current)
    },
    [],
  )

  const click = () => {
    if (!armed) {
      setArmed(true)
      timer.current = window.setTimeout(() => setArmed(false), 4000)
      return
    }
    if (timer.current !== null) window.clearTimeout(timer.current)
    setArmed(false)
    onConfirm()
  }

  return (
    <button type="button" className={`btn ${armed ? 'btn-danger' : 'btn-ghost'}`} onClick={click} disabled={disabled}>
      {armed ? confirmLabel : label}
    </button>
  )
}
