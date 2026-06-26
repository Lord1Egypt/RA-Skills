import { PublicKey, SystemProgram, Transaction, sendAndConfirmTransaction, } from '@solana/web3.js';
export async function sendNativeTransfer(connection, { signer, recipient, lamports, commitment = 'confirmed', }) {
    const balance = await connection.getBalance(signer.publicKey);
    if (balance < lamports) {
        const err = Object.assign(new Error('Insufficient balance for transfer (plus fees).'), {
            code: 'insufficient_balance',
            details: {
                balanceLamports: balance,
                requiredLamports: lamports,
                signer: signer.publicKey.toBase58(),
            },
        });
        throw err;
    }
    const tx = new Transaction().add(SystemProgram.transfer({
        fromPubkey: signer.publicKey,
        toPubkey: recipient,
        lamports,
    }));
    const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash(commitment);
    tx.recentBlockhash = blockhash;
    tx.feePayer = signer.publicKey;
    const signature = await sendAndConfirmTransaction(connection, tx, [signer], {
        commitment,
    });
    return { signature, lastValidBlockHeight };
}
export function publicKeyFromBase58(addressBase58) {
    try {
        return new PublicKey(addressBase58);
    }
    catch {
        const err = Object.assign(new Error('Invalid recipient address'), {
            code: 'invalid_address',
        });
        throw err;
    }
}
