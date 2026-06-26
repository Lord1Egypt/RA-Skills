import type { SolanaCluster } from './genesis-clusters.js';

export function transactionExplorerUrl(signature: string, cluster: SolanaCluster): string {
  const base = `https://solscan.io/tx/${signature}`;
  if (cluster === 'mainnet-beta' || cluster === 'custom') return base;
  return `${base}?cluster=${cluster}`;
}
