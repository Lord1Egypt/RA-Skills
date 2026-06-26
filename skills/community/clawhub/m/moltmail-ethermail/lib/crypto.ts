import crypto from "crypto";

const ALGO = "aes-256-gcm";
const KEY_LEN = 32; // 256 bits
const IV_LEN = 12;  // recommended for GCM
const SALT_LEN = 16;

export type EncryptedPayload = {
    salt: string;
    iv: string;
    authTag: string;
    ciphertext: string;
};

function deriveKey(passphrase: string, salt: Buffer): Promise<Buffer> {
    return new Promise((resolve, reject) => {
        crypto.scrypt(passphrase, salt, KEY_LEN, (err, key) => {
            if (err) reject(err);
            else resolve(key);
        });
    });
}

export async function encrypt(
    plaintext: string,
    passphrase: string
): Promise<EncryptedPayload> {
    const salt = crypto.randomBytes(SALT_LEN);
    const iv = crypto.randomBytes(IV_LEN);
    const key = await deriveKey(passphrase, salt);

    const cipher = crypto.createCipheriv(ALGO, key, iv);
    const encrypted = Buffer.concat([
        cipher.update(plaintext, "utf8"),
        cipher.final()
    ]);

    const authTag = cipher.getAuthTag();

    return {
        salt: salt.toString("base64"),
        iv: iv.toString("base64"),
        authTag: authTag.toString("base64"),
        ciphertext: encrypted.toString("base64")
    };
}

export async function decrypt(
    payload: EncryptedPayload,
    passphrase: string
): Promise<string> {
    const salt = Buffer.from(payload.salt, "base64");
    const iv = Buffer.from(payload.iv, "base64");
    const authTag = Buffer.from(payload.authTag, "base64");
    const ciphertext = Buffer.from(payload.ciphertext, "base64");

    const key = await deriveKey(passphrase, salt);

    const decipher = crypto.createDecipheriv(ALGO, key, iv);
    decipher.setAuthTag(authTag);

    const decrypted = Buffer.concat([
        decipher.update(ciphertext),
        decipher.final()
    ]);

    return decrypted.toString("utf8");
}
