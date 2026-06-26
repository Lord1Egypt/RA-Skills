export const DEFAULT_RPC_URL = 'https://api.devnet.solana.com';

export type RpcEnv = {
  SOLANA_RPC_URL?: string;
};

export function resolveRpcUrl(env: RpcEnv, flagRpc?: string | null): string {
  return flagRpc || env.SOLANA_RPC_URL || DEFAULT_RPC_URL;
}
