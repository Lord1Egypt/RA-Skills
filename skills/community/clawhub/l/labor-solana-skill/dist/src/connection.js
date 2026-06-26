import { Connection } from '@solana/web3.js';
import { GENESIS_HASH_TO_CLUSTER } from './genesis-clusters.js';
export function createConnection(rpcUrl, commitment = 'confirmed') {
    return new Connection(rpcUrl, commitment);
}
export async function inferCluster(connection) {
    try {
        const genesis = await connection.getGenesisHash();
        return GENESIS_HASH_TO_CLUSTER[genesis] ?? 'custom';
    }
    catch {
        return 'custom';
    }
}
