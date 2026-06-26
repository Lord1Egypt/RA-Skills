/**
 * Shared interfaces for lista-wallet-connect-skill.
 */

export interface Session {
  accounts: string[];
  chains?: string[];
  peerName: string;
  authenticated?: boolean;
  authAddress?: string;
  authNonce?: string;
  authSignature?: string;
  authTimestamp?: string;
  createdAt: string;
  updatedAt?: string;
}

export type Sessions = Record<string, Session>;

export interface ParsedArgs {
  topic?: string;
  address?: string;
  message?: string;
  chain?: string;
  chains?: string;
  to?: string;
  data?: string;
  value?: string;
  gas?: string;
  gasPrice?: string;
  all?: boolean;
  clean?: boolean;
  help?: boolean;
  open?: boolean;
  noSimulate?: boolean;
}

export interface Eip712TypeEntry {
  name: string;
  type: string;
}

export interface TypedData {
  domain: Record<string, unknown>;
  types: Record<string, Eip712TypeEntry[]>;
  message: Record<string, unknown>;
  primaryType?: string;
}
