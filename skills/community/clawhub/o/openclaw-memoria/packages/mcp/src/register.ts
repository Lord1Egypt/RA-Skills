/**
 * Enregistrement MCP auprès des hôtes — DÉPLACÉ dans @memoria/core (mission B2)
 * pour que le daemon connecte un agent EN PROCESSUS (1 clic depuis l'UI) sans
 * créer de cycle mcp→daemon→mcp. Ce module ré-exporte l'API à l'identique :
 * rien ne change pour les consommateurs de @memoria/mcp.
 */
export {
  autoRegister,
  autoUnregister,
  cliInstalled,
  installOpenClawHooks,
  registerClaudeCode,
  registerCodex,
  registerOpenClaw,
  serveInvocation,
  unregisterClaudeCode,
  unregisterCodex,
  unregisterOpenClaw,
} from '@memoria/core'
export type { HostKind, RegisterOptions, RegisterResult } from '@memoria/core'
