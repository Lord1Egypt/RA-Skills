"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.JEPCrypto = void 0;
const tweetnacl_1 = __importDefault(require("tweetnacl"));
const crypto_1 = require("crypto");
/**
 * JEP Cryptography
 * Ed25519 signatures + SHA-256 hashing
 */
class JEPCrypto {
    keyPair;
    constructor(seed) {
        if (seed) {
            if (seed.length !== 32)
                throw new Error("Seed must be exactly 32 bytes");
            this.keyPair = tweetnacl_1.default.sign.keyPair.fromSeed(seed);
        }
        else {
            this.keyPair = tweetnacl_1.default.sign.keyPair();
        }
    }
    get publicKey() {
        return Buffer.from(this.keyPair.publicKey).toString('base64');
    }
    sign(message) {
        const msgBytes = Buffer.from(message, 'utf-8');
        const sig = tweetnacl_1.default.sign.detached(msgBytes, this.keyPair.secretKey);
        return Buffer.from(sig).toString('base64');
    }
    static verify(message, signature, publicKey) {
        try {
            const msgBytes = Buffer.from(message, 'utf-8');
            const sigBytes = Buffer.from(signature, 'base64');
            const pubBytes = Buffer.from(publicKey, 'base64');
            return sigBytes.length === 64 && pubBytes.length === 32 && tweetnacl_1.default.sign.detached.verify(msgBytes, sigBytes, pubBytes);
        }
        catch {
            return false;
        }
    }
    static sha256(input) {
        return (0, crypto_1.createHash)('sha256').update(input).digest('hex');
    }
    static uuidv4() {
        const bytes = (0, crypto_1.randomBytes)(16);
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
exports.JEPCrypto = JEPCrypto;
//# sourceMappingURL=crypto.js.map