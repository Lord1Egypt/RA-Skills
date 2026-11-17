/**
 * Job de téléchargement de modèle Ollama (POST /v1/admin/ollama_pull) :
 * un SEUL téléchargement à la fois, progression suivie en mémoire via le
 * stream NDJSON de POST {ollama}/api/pull, interrogeable par
 * GET /v1/admin/ollama_pull_status (polling UI pendant l'onboarding).
 *
 * Machine à états : idle → running → (idle + percent 100) | (idle + error).
 * Tout échec est CONSERVÉ dans l'état (et loggé) — jamais une fin muette.
 */
import { DEFAULT_OLLAMA_BASE_URL } from '@memoria/core'

export interface OllamaPullStatus {
  running: boolean
  /** Modèle en cours (ou dernier) de téléchargement. */
  model: string | null
  /** 0-100, null tant que la taille totale n'est pas connue. */
  percent: number | null
  /** Dernier statut envoyé par Ollama (pulling…, verifying…, success). */
  status: string | null
  /** Message d'échec du DERNIER téléchargement (null si OK/en cours). */
  error: string | null
}

interface PullLine {
  status?: string
  total?: number
  completed?: number
  error?: string
}

export class OllamaPullJob {
  private readonly baseUrl: string
  private state: OllamaPullStatus = { running: false, model: null, percent: null, status: null, error: null }

  constructor(baseUrl: string = DEFAULT_OLLAMA_BASE_URL) {
    this.baseUrl = baseUrl.replace(/\/$/, '')
  }

  status(): OllamaPullStatus {
    return { ...this.state }
  }

  /** Démarre le téléchargement (refus EXPLICITE si un job tourne déjà). */
  start(model: string): void {
    if (this.state.running) {
      throw new Error(`un téléchargement est déjà en cours (${this.state.model ?? '?'})`)
    }
    this.state = { running: true, model, percent: null, status: 'démarrage', error: null }
    void this.run(model).then(
      () => {
        this.state = { running: false, model, percent: 100, status: 'terminé', error: null }
        console.log(`[memoria-daemon] modèle Ollama « ${model} » téléchargé`)
      },
      (err: unknown) => {
        const message = (err as Error).message ?? String(err)
        this.state = { running: false, model, percent: this.state.percent, status: 'erreur', error: message }
        console.warn(`[memoria-daemon] téléchargement Ollama « ${model} » en échec : ${message}`)
      },
    )
  }

  private async run(model: string): Promise<void> {
    const res = await fetch(`${this.baseUrl}/api/pull`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: model, stream: true }),
    })
    if (!res.ok) {
      const detail = await res.text().catch(() => '')
      throw new Error(`ollama /api/pull HTTP ${res.status} : ${detail.slice(0, 200)}`)
    }
    if (!res.body) throw new Error('ollama /api/pull : corps de réponse absent (stream attendu)')

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    for (;;) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      let nl: number
      while ((nl = buffer.indexOf('\n')) >= 0) {
        const line = buffer.slice(0, nl).trim()
        buffer = buffer.slice(nl + 1)
        if (line) this.applyLine(line, model)
      }
    }
    if (buffer.trim()) this.applyLine(buffer.trim(), model)
  }

  private applyLine(line: string, model: string): void {
    let parsed: PullLine
    try {
      parsed = JSON.parse(line) as PullLine
    } catch {
      // ligne NDJSON tronquée/illisible : on la signale mais on continue le stream
      console.warn(`[memoria-daemon] ligne /api/pull illisible (modèle ${model}) : ${line.slice(0, 120)}`)
      return
    }
    // Ollama signale ses erreurs DANS le stream ({"error": "..."}).
    if (parsed.error) throw new Error(parsed.error)
    if (parsed.status) this.state.status = parsed.status
    if (typeof parsed.total === 'number' && parsed.total > 0 && typeof parsed.completed === 'number') {
      this.state.percent = Math.min(100, Math.round((parsed.completed / parsed.total) * 100))
    }
    if (parsed.status === 'success') this.state.percent = 100
  }
}
