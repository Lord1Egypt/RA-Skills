import nacl from 'tweetnacl';
import { createHash, randomBytes } from 'crypto';

/**
 * JEP Cryptography
 * Ed25519 signatures + SHA-256 hashing
 */
export class JEPCrypto {
  private keyPair: nacl.SignKeyPair;

  constructor(seed?: Uint8Array) {
    if (seed) {
      this.keyPair = nacl.sign.keyPair.fromSeed(seed.slice(0, 32));
    } else {
      this.keyPair = nacl.sign.keyPair();
    }
  }

  get publicKey(): string {
    return Buffer.from(this.keyPair.publicKey).toString('base64');
  }

  sign(message: string): string {
    const msgBytes = Buffer.from(message, 'utf-8');
    const sig = nacl.sign.detached(msgBytes, this.keyPair.secretKey);
    return Buffer.from(sig).toString('base64');
  }

  static verify(message: string, signature: string, publicKey: string): boolean {
    const msgBytes = Buffer.from(message, 'utf-8');
    const sigBytes = Buffer.from(signature, 'base64');
    const pubBytes = Buffer.from(publicKey, 'base64');
    return nacl.sign.detached.verify(msgBytes, sigBytes, pubBytes);
  }

  static sha256(input: string): string {
    return createHash('sha256').update(input).digest('hex');
  }

  static uuidv4(): string {
    const bytes = randomBytes(16);
    bytes[6] = (bytes[6] & 0x0f) | 0x40;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;
    return [
      bytes.toString('hex', 0, 4),
      bytes.toString('hex', 4, 6),
      bytes.toString('hex', 6, 8),
      bytes.toString('hex', 8, 10),
      bytes.toString('hex', 10, 16)
    ].join('-');
  }
}