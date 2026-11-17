/**
 * Credentials d'instance — DÉPLACÉS dans @memoria/core (mission B2) : le daemon
 * les écrit lui-même lors de la connexion 1 clic (POST /v1/admin/agents_connect).
 * Ce module ré-exporte l'API à l'identique pour les consommateurs de @memoria/mcp.
 */
export {
  credentialsPath,
  defaultCredentialsDir,
  deleteCredentials,
  listCredentials,
  loadCredentials,
  saveCredentials,
} from '@memoria/core'
export type { InstanceCredentials } from '@memoria/core'
