import { LAMPORTS_PER_SOL } from '@solana/web3.js';

function normalizeSolString(raw: string): string {
  const [wholePart, fracPart = ''] = raw.split('.');
  const whole = wholePart.replace(/^0+(?=\d)/, '') || '0';
  const fracTrimmed = fracPart.replace(/0+$/, '');
  return fracTrimmed.length > 0 ? `${whole}.${fracTrimmed}` : whole;
}

export function lamportsToSolString(lamports: number): string {
  const lamportsBig = BigInt(lamports);
  const whole = lamportsBig / BigInt(LAMPORTS_PER_SOL);
  const frac = lamportsBig % BigInt(LAMPORTS_PER_SOL);
  const fracText = frac.toString().padStart(9, '0').replace(/0+$/, '');
  return fracText.length > 0 ? `${whole.toString()}.${fracText}` : whole.toString();
}

export function parsePositiveSolToLamports(
  solInput: string | number,
): { lamports: number; solExact: string } {
  const raw = String(solInput).trim();
  if (!/^\d+(\.\d+)?$/.test(raw)) {
    throw new Error('Amount must be a positive number');
  }

  const [wholePart, fracPart = ''] = raw.split('.');
  if (fracPart.length > 9) {
    throw new Error('Amount supports at most 9 decimal places (lamports precision)');
  }
  const lamportsPerSol = BigInt(LAMPORTS_PER_SOL);
  const wholeLamports = BigInt(wholePart) * lamportsPerSol;
  const fracPadded = fracPart.padEnd(9, '0').slice(0, 9);
  const fracLamports = BigInt(fracPadded || '0');
  const lamportsBig = wholeLamports + fracLamports;

  if (lamportsBig <= 0n) {
    throw new Error('Amount too small after converting to lamports');
  }
  if (lamportsBig > BigInt(Number.MAX_SAFE_INTEGER)) {
    throw new Error('Amount is too large');
  }

  return {
    lamports: Number(lamportsBig),
    solExact: normalizeSolString(raw),
  };
}
