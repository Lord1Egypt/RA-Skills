/**
 * Parsers de transcripts d'agents → tours de conversation normalisés (spec §7.2).
 *
 * Quatre formats RÉELS supportés (vérifiés sur disque) :
 *  - Claude Code   : ~/.claude/projects/<slug>/<uuid>.jsonl (une ligne JSON/événement) ;
 *  - Codex rollout : ~/.codex/sessions/.../rollout-*.jsonl + archived_sessions/ ;
 *  - Codex history : ~/.codex/history.jsonl (prompts user seuls) ;
 *  - Markdown      : fichier .md découpé en sections de titre `##`.
 *
 * Robustesse (règle du projet « aucun mort silencieux ») :
 *  - une ligne JSON invalide est IGNORÉE (jamais de throw qui ferait perdre tout
 *    le fichier) — mais signalée via console.warn pour rester visible ;
 *  - les blocs/tours vides sont filtrés ;
 *  - le texte d'un tour est tronqué à MAX_TURN_CHARS (borne le coût LLM) ;
 *  - AUCUN catch muet : toute erreur inattendue passe par console.warn.
 */

/** Tour de conversation normalisé — la sortie commune de tous les parsers. */
export interface Turn {
  role: 'user' | 'assistant'
  text: string
  /** Timestamp ISO si la source en porte un (sert au filtre sinceDate). */
  ts?: string
}

export type TranscriptFormat = 'claude-code' | 'codex-rollout' | 'codex-history' | 'markdown' | 'unknown'

/** Plafond de caractères par tour — borne le coût d'extraction (jamais silencieux : on log la troncature). */
const MAX_TURN_CHARS = 20_000

/** Texte tronqué à MAX_TURN_CHARS, avec marqueur visible (pas de coupe muette). */
function truncate(text: string, where: string): string {
  if (text.length <= MAX_TURN_CHARS) return text
  console.warn(`[memoria] transcript : tour tronqué (${text.length} → ${MAX_TURN_CHARS} chars) [${where}]`)
  return `${text.slice(0, MAX_TURN_CHARS)}…[tronqué]`
}

/** Découpe un contenu JSONL en lignes non vides (CRLF/LF tolérés). */
function jsonlLines(content: string): string[] {
  return content.split(/\r?\n/).filter(line => line.trim().length > 0)
}

/** Parse JSON tolérant : null si invalide + warn (jamais de throw qui perdrait le fichier entier). */
function safeParseLine(line: string, where: string): unknown {
  try {
    return JSON.parse(line)
  } catch {
    const excerpt = line.length > 80 ? `${line.slice(0, 80)}…` : line
    console.warn(`[memoria] transcript ${where} : ligne JSON invalide ignorée — « ${excerpt} »`)
    return null
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function asRole(value: unknown): 'user' | 'assistant' | null {
  return value === 'user' || value === 'assistant' ? value : null
}

/** Concatène un `content` qui peut être une string ou un tableau de blocs. Filtre le bruit (tool_use/thinking/env). */
function blocksToText(content: unknown, textTypes: ReadonlySet<string>): string {
  if (typeof content === 'string') return content.trim()
  if (!Array.isArray(content)) return ''
  const parts: string[] = []
  for (const block of content) {
    if (!isRecord(block)) continue
    const type = typeof block['type'] === 'string' ? (block['type'] as string) : ''
    if (!textTypes.has(type)) continue // ignore tool_use / tool_result / thinking / image…
    const text = block['text']
    if (typeof text === 'string' && text.trim().length > 0) parts.push(text.trim())
  }
  return parts.join('\n').trim()
}

/** Bruit système Codex à ne jamais extraire (contexte injecté, pas de l'utilisateur). */
function isSystemNoise(text: string): boolean {
  const t = text.trimStart()
  return t.startsWith('<environment_context>') || t.startsWith('<user_instructions>') || t.startsWith('<user_info>')
}

// ---------------------------------------------------------------------------
// 1. Claude Code — ~/.claude/projects/<slug>/<uuid>.jsonl
// ---------------------------------------------------------------------------

const CLAUDE_TEXT_BLOCKS = new Set(['text'])

export function parseClaudeCodeTranscript(content: string): Turn[] {
  const turns: Turn[] = []
  for (const line of jsonlLines(content)) {
    const obj = safeParseLine(line, 'claude-code')
    if (!isRecord(obj)) continue
    const role = asRole(obj['type'])
    if (!role) continue // summary / system / file-history-snapshot…
    const message = obj['message']
    if (!isRecord(message)) continue
    const text = blocksToText(message['content'], CLAUDE_TEXT_BLOCKS)
    if (!text) continue
    const ts = typeof obj['timestamp'] === 'string' ? (obj['timestamp'] as string) : undefined
    turns.push({ role, text: truncate(text, 'claude-code'), ...(ts ? { ts } : {}) })
  }
  return turns
}

// ---------------------------------------------------------------------------
// 2. Codex rollout — ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl + archived
// ---------------------------------------------------------------------------

const CODEX_TEXT_BLOCKS = new Set(['input_text', 'output_text', 'text'])

export function parseCodexRollout(content: string): Turn[] {
  const turns: Turn[] = []
  for (const line of jsonlLines(content)) {
    const obj = safeParseLine(line, 'codex-rollout')
    if (!isRecord(obj)) continue
    if (obj['type'] !== 'response_item') continue
    const payload = obj['payload']
    if (!isRecord(payload)) continue
    if (payload['type'] !== 'message') continue
    const role = asRole(payload['role'])
    if (!role) continue
    const text = blocksToText(payload['content'], CODEX_TEXT_BLOCKS)
    if (!text || isSystemNoise(text)) continue
    const ts = typeof obj['timestamp'] === 'string' ? (obj['timestamp'] as string) : undefined
    turns.push({ role, text: truncate(text, 'codex-rollout'), ...(ts ? { ts } : {}) })
  }
  return turns
}

// ---------------------------------------------------------------------------
// 3. Codex history — ~/.codex/history.jsonl (prompts user seuls)
// ---------------------------------------------------------------------------

export function parseCodexHistory(content: string): Turn[] {
  const turns: Turn[] = []
  for (const line of jsonlLines(content)) {
    const obj = safeParseLine(line, 'codex-history')
    if (!isRecord(obj)) continue
    const text = typeof obj['text'] === 'string' ? (obj['text'] as string).trim() : ''
    if (!text || isSystemNoise(text)) continue
    // ts en epoch SECONDES → ISO (history.jsonl ne porte pas de millisecondes).
    let ts: string | undefined
    const rawTs = obj['ts']
    if (typeof rawTs === 'number' && Number.isFinite(rawTs) && rawTs > 0) {
      const ms = rawTs < 1e11 ? rawTs * 1000 : rawTs
      const d = new Date(ms)
      if (!Number.isNaN(d.getTime())) ts = d.toISOString()
    }
    turns.push({ role: 'user', text: truncate(text, 'codex-history'), ...(ts ? { ts } : {}) })
  }
  return turns
}

// ---------------------------------------------------------------------------
// 4. Markdown générique — sections par titre `##` (role user par défaut)
// ---------------------------------------------------------------------------

export function parseMarkdown(content: string): Turn[] {
  const turns: Turn[] = []
  const lines = content.split(/\r?\n/)
  let buffer: string[] = []

  const flush = () => {
    const text = buffer.join('\n').trim()
    buffer = []
    if (text.length > 0) turns.push({ role: 'user', text: truncate(text, 'markdown') })
  }

  for (const line of lines) {
    // Un titre de niveau 2+ (## …) ouvre une nouvelle section : on clôt la précédente.
    if (/^#{2,6}\s+\S/.test(line)) {
      flush()
      buffer.push(line)
    } else {
      buffer.push(line)
    }
  }
  flush()
  return turns
}

// ---------------------------------------------------------------------------
// Détection de format
// ---------------------------------------------------------------------------

/**
 * Devine le format à partir du chemin ET des premières lignes (les deux pèsent).
 * `firstLines` = quelques lignes du début du fichier (l'appelant lit un échantillon).
 * Renvoie 'unknown' si rien ne correspond — l'importeur SKIP alors le fichier
 * proprement (jamais de parse à l'aveugle qui inventerait des tours).
 */
export function detectTranscriptFormat(path: string, firstLines: string): TranscriptFormat {
  const lower = path.toLowerCase()

  // 1) Indices forts par chemin (les plus fiables).
  if (lower.includes('.codex') && lower.endsWith('history.jsonl')) return 'codex-history'
  if (/rollout-.*\.jsonl$/.test(lower) || lower.includes('/.codex/sessions/') || lower.includes('/archived_sessions/')) {
    return 'codex-rollout'
  }
  if (lower.includes('/.claude/projects/') && lower.endsWith('.jsonl')) return 'claude-code'
  if (lower.endsWith('.md') || lower.endsWith('.markdown')) return 'markdown'

  // 2) Indices par contenu (extension ambiguë comme un .jsonl hors arborescence connue).
  const sample = jsonlLines(firstLines)
  for (const line of sample) {
    const obj = safeParseLine(line, 'detect')
    if (!isRecord(obj)) continue
    // Codex history : {session_id, ts, text}
    if ('session_id' in obj && 'text' in obj && 'ts' in obj && !('type' in obj)) return 'codex-history'
    // Codex rollout : {timestamp, type:'response_item', payload}
    if (obj['type'] === 'response_item' && isRecord(obj['payload'])) return 'codex-rollout'
    if ('timestamp' in obj && 'payload' in obj) return 'codex-rollout'
    // Claude Code : {type:'user'|'assistant', message:{...}}
    if (asRole(obj['type']) && isRecord(obj['message'])) return 'claude-code'
    // Claude Code variantes (summary/system) avec un uuid + sessionId
    if ('sessionId' in obj && 'uuid' in obj) return 'claude-code'
  }

  // 3) Markdown si le début ressemble à du markdown (titres) et pas à du JSON.
  if (firstLines.trimStart().startsWith('#') || /^\s*#{1,6}\s+\S/m.test(firstLines)) return 'markdown'

  return 'unknown'
}

/** Dispatch chemin/format → parser adapté. 'unknown' → tableau vide (jamais de throw). */
export function parseTranscript(format: TranscriptFormat, content: string): Turn[] {
  switch (format) {
    case 'claude-code':
      return parseClaudeCodeTranscript(content)
    case 'codex-rollout':
      return parseCodexRollout(content)
    case 'codex-history':
      return parseCodexHistory(content)
    case 'markdown':
      return parseMarkdown(content)
    case 'unknown':
      return []
  }
}
