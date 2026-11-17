/**
 * Secrets (spec §9, décision D2) — GATE DUR :
 * la valeur d'un secret ne touche JAMAIS facts/.md/logs/audit/projection.
 * `SecretProvider` = coffre (Keychain macOS / Credential Manager / libsecret /
 * fallback AES-256-GCM). `Redactor` = détection+remplacement AVANT storeFact.
 */

export interface SecretProvider {
  /** `keychain-macos` | `credential-manager` | `libsecret` | `aes-vault` */
  readonly kind: string
  isAvailable(): boolean
  set(name: string, value: string): void
  /** null si absent. */
  get(name: string): string | null
  delete(name: string): void
  /** Référence opaque stockable (ex. `keychain:memoria/<name>`). */
  locationFor(name: string): string
}

export interface DetectedSecret {
  /** Nom proposé pour la référence (ex. `anthropic-api-key-1`). */
  name: string
  /** Type détecté (`anthropic`, `openai`, `aws`, `jwt`, `generic-token`…). */
  kind: string
  /** La valeur détectée — à mettre au coffre, jamais ailleurs. */
  value: string
}

export interface RedactionResult {
  /** Texte où chaque secret est remplacé par `[secret:<name>]`. */
  text: string
  found: DetectedSecret[]
}

export interface Redactor {
  redact(text: string): RedactionResult
}
