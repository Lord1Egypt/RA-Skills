import { Connection, type Commitment } from '@solana/web3.js';
import { GENESIS_HASH_TO_CLUSTER, type SolanaCluster } from './genesis-clusters.js';

export function createConnection(rpcUrl: string, commitment: Commitment = 'confirmed'): Connection {
  return new Connection(rpcUrl, commitment);
}

export async function inferCluster(connection: Connection): Promise<SolanaCluster> {
  try {
    const genesis = await connection.getGenesisHash();
    return GENESIS_HASH_TO_CLUSTER[genesis as keyof typeof GENESIS_HASH_TO_CLUSTER] ?? 'custom';
  } catch {
    return 'custom';
  }
}
