/**
 * JEP Cryptography
 * Ed25519 signatures + SHA-256 hashing
 */
export declare class JEPCrypto {
    private keyPair;
    constructor(seed?: Uint8Array);
    get publicKey(): string;
    sign(message: string): string;
    static verify(message: string, signature: string, publicKey: string): boolean;
    static sha256(input: string): string;
    static uuidv4(): string;
}
