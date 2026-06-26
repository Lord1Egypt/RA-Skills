import {
  PublicKey,
  SystemProgram,
  Transaction,
  sendAndConfirmTransaction,
  type Commitment,
  type Connection,
  type Keypair,
} from '@solana/web3.js';

type InsufficientBalanceError = Error & {
  code: 'insufficient_balance';
  details: {
    balanceLamports: number;
    requiredLamports: number;
    signer: string;
  };
};

export async function sendNativeTransfer(
  connection: Connection,
  {
    signer,
    recipient,
    lamports,
    commitment = 'confirmed',
  }: {
    signer: Keypair;
    recipient: PublicKey;
    lamports: number;
    commitment?: Commitment;
  },
): Promise<{ signature: string; lastValidBlockHeight: number }> {
  const balance = await connection.getBalance(signer.publicKey);
  if (balance < lamports) {
    const err: InsufficientBalanceError = Object.assign(
      new Error('Insufficient balance for transfer (plus fees).'),
      {
        code: 'insufficient_balance' as const,
        details: {
          balanceLamports: balance,
          requiredLamports: lamports,
          signer: signer.publicKey.toBase58(),
        },
      },
    );
    throw err;
  }

  const tx = new Transaction().add(
    SystemProgram.transfer({
      fromPubkey: signer.publicKey,
      toPubkey: recipient,
      lamports,
    }),
  );

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash(commitment);
  tx.recentBlockhash = blockhash;
  tx.feePayer = signer.publicKey;

  const signature = await sendAndConfirmTransaction(connection, tx, [signer], {
    commitment,
  });

  return { signature, lastValidBlockHeight };
}

export function publicKeyFromBase58(addressBase58: string): PublicKey {
  try {
    return new PublicKey(addressBase58);
  } catch {
    const err = Object.assign(new Error('Invalid recipient address'), {
      code: 'invalid_address' as const,
    });
    throw err;
  }
}
