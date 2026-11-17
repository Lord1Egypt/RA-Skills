/**
 * Redaction par regex (spec §9, D2 — gate dur) : détecte les secrets connus
 * AVANT storeFact et les remplace par `[secret:<name>]`. La valeur part au
 * coffre, jamais dans facts/.md/logs/audit/projection.
 *
 * Ordre des patterns = du plus spécifique au plus générique (le générique ne
 * doit jamais re-capturer un placeholder déjà posé).
 */
import { sha256Hex } from '../util.js'
import type { DetectedSecret, RedactionResult, Redactor } from './types.js'

interface SecretPattern {
  kind: string
  /** DOIT porter les flags `g` et `d` (indices de groupes). */
  regex: RegExp
  /** Si défini, seul ce groupe de capture est redacté (le contexte est gardé). */
  group?: number
}

/**
 * NB faux positifs : un hash git fait 40 hex — le pattern aws-secret exige donc
 * un contexte `aws…secret/key/token…=` ; le token générique exige un mot-clé
 * (`password|token|secret|api key`) suivi de `:`/`=`.
 */
const PATTERNS: ReadonlyArray<SecretPattern> = [
  // Blocs PEM en premier : ils contiennent du base64 qui matcherait JWT/générique.
  {
    kind: 'pem-private-key',
    regex: /-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----/gd,
  },
  { kind: 'anthropic', regex: /\bsk-ant-[A-Za-z0-9_-]{20,}/gd },
  { kind: 'openai', regex: /\bsk-proj-[A-Za-z0-9_-]{20,}/gd },
  { kind: 'openai', regex: /\bsk-[A-Za-z0-9]{20,}\b/gd },
  { kind: 'aws-access-key', regex: /\bAKIA[0-9A-Z]{16}\b/gd },
  {
    kind: 'aws-secret-key',
    regex: /\baws[\w -]{0,32}(?:secret|access|key|token)[\w -]{0,16}["']?\s*[:=]\s*["']?([A-Za-z0-9/+]{40})(?![A-Za-z0-9/+=])/gid,
    group: 1,
  },
  { kind: 'github', regex: /\b(?:gh[opsu]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})/gd },
  { kind: 'google', regex: /\bAIza[0-9A-Za-z_-]{35}(?![0-9A-Za-z_-])/gd },
  { kind: 'google-oauth', regex: /\bya29\.[A-Za-z0-9_-]{20,}/gd },
  { kind: 'slack', regex: /\bxox[baprs]-[A-Za-z0-9-]{10,}(?![A-Za-z0-9-])/gd },
  { kind: 'slack-webhook', regex: /\bhttps:\/\/hooks\.slack\.com\/services\/[A-Za-z0-9/]{20,}/gd },
  // Stripe (écosystème Primo) : clés secrètes/restreintes/webhook + sessions live.
  { kind: 'stripe', regex: /\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}/gd },
  { kind: 'stripe-webhook', regex: /\bwhsec_[A-Za-z0-9]{20,}/gd },
  { kind: 'stripe-session', regex: /\bcs_(?:live|test)_[A-Za-z0-9]{20,}/gd },
  // Chaîne de connexion avec credentials : proto://user:pass@host
  { kind: 'connection-string', regex: /\b[a-z][a-z0-9+.-]*:\/\/[^\s:/@]+:([^\s:/@]{3,})@[^\s/]+/gid, group: 1 },
  {
    kind: 'jwt',
    regex: /\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}(?![A-Za-z0-9_.-])/gd,
  },
  {
    kind: 'generic-token',
    // (?<!\[) : ne pas re-matcher le mot `secret` d'un placeholder `[secret:…]`
    // déjà posé ; (?!\[secret:) : ne pas capturer un placeholder comme valeur.
    regex: /(?<!\[)\b(?:password|passwd|pwd|token|secret|api[_-]?key|apikey)["']?\s*[:=]\s*["']?(?!\[secret:)([^\s"'`]{12,})/gid,
    group: 1,
  },
]

export class RegexRedactor implements Redactor {
  redact(text: string): RedactionResult {
    const found: DetectedSecret[] = []
    // Nom STABLE PAR VALEUR (hash court) : la même clé vue dans deux captures
    // différentes garde le même nom — deux clés distinctes du même kind ne se
    // disputent jamais la même entrée du coffre (anti-écrasement silencieux).
    const byValue = new Map<string, string>()

    const nameFor = (kind: string, value: string): string => {
      const existing = byValue.get(value)
      if (existing) return existing
      const name = `${kind}-${sha256Hex(value).slice(0, 8)}`
      byValue.set(value, name)
      found.push({ name, kind, value })
      return name
    }

    let out = text
    for (const pattern of PATTERNS) {
      out = applyPattern(out, pattern, nameFor)
    }
    return { text: out, found }
  }
}

function applyPattern(
  text: string,
  pattern: SecretPattern,
  nameFor: (kind: string, value: string) => string,
): string {
  let result = ''
  let last = 0
  for (const m of text.matchAll(pattern.regex)) {
    const span = m.indices?.[pattern.group ?? 0]
    if (!span) continue // groupe optionnel non matché — rien à redacter ici
    const [start, end] = span
    const value = text.slice(start, end)
    result += text.slice(last, start) + `[secret:${nameFor(pattern.kind, value)}]`
    last = end
  }
  return result + text.slice(last)
}
