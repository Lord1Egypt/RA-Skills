import { Keypair } from '@solana/web3.js';
import bs58 from 'bs58';
export function keypairFromSecretRaw(secretRaw) {
    const trimmed = secretRaw.trim();
    if (trimmed.startsWith('[')) {
        const arr = JSON.parse(trimmed);
        if (!Array.isArray(arr)) {
            throw new Error('SOLANA_PRIVATE_KEY JSON must be a byte array');
        }
        if (!arr.every((n) => Number.isInteger(n) && n >= 0 && n <= 255)) {
            throw new Error('SOLANA_PRIVATE_KEY JSON contains invalid byte values');
        }
        return Keypair.fromSecretKey(Uint8Array.from(arr));
    }
    const decoded = bs58.decode(trimmed);
    return Keypair.fromSecretKey(decoded);
}
