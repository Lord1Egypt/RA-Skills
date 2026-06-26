export const DEFAULT_RPC_URL = 'https://api.devnet.solana.com';
export function resolveRpcUrl(env, flagRpc) {
    return flagRpc || env.SOLANA_RPC_URL || DEFAULT_RPC_URL;
}
