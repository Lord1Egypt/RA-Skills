import fs from "fs/promises";
import path from "path";
import { Wallet } from "ethers";
import { decrypt, type EncryptedPayload } from "./crypto.ts";
import pkg from "enquirer";
const { prompt } = pkg;

const CONFIG_PATH = path.resolve(
    process.cwd(),
    "state",
    "config.enc.json"
);

type WalletConfig = {
    address: string;
    encryptedPrivateKey: EncryptedPayload;
};

export async function promptPassphrase(): Promise<string> {
    if (process.env.ETHERMAIL_PASSPHRASE) {
        return process.env.ETHERMAIL_PASSPHRASE;
    }

    const { passphrase } = await prompt<{ passphrase: string }>({
        type: "password",
        name: "passphrase",
        message: "Enter wallet passphrase",
        mask: "*"
    });

    return passphrase;
}

export async function loadWallet(): Promise<Wallet> {
    const raw = await fs.readFile(CONFIG_PATH, "utf8");
    const config: WalletConfig = JSON.parse(raw);

    const passphrase = await promptPassphrase();
    if (!passphrase) {
        throw new Error("Passphrase is required to unlock wallet");
    }

    let privateKey: string;
    try {
        privateKey = await decrypt(
            config.encryptedPrivateKey,
            passphrase
        );
    } catch {
        throw new Error("Failed to decrypt wallet (wrong passphrase?)");
    }

    const wallet = new Wallet(privateKey);

    if (wallet.address.toLowerCase() !== config.address.toLowerCase()) {
        throw new Error("Decrypted wallet does not match stored address");
    }

    return wallet;
}
