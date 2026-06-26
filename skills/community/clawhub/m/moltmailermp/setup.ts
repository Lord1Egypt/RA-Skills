import { HDNodeWallet, Wallet } from "ethers";
import pkg from "enquirer";
import fs from "fs/promises";
import path from "path";
import { encrypt } from "./lib/crypto.ts";

const { prompt } = pkg;

const STATE_DIR = path.resolve(process.cwd(), "state");
const CONFIG_PATH = path.join(STATE_DIR, "config.enc.json");

type ExistingConfig = {
    address: string;
};

async function configExists(): Promise<boolean> {
    try {
        await fs.access(CONFIG_PATH);
        return true;
    } catch {
        return false;
    }
}

async function main() {
    if (await configExists()) {
        const raw = await fs.readFile(CONFIG_PATH, "utf8");
        const existing: ExistingConfig = JSON.parse(raw);

        console.log("\n🔎 Existing EtherMail setup detected");
        console.log("Address:", existing.address);

        const { action } = await prompt<{ action: string }>({
            type: "select",
            name: "action",
            message: "This account is already set up. What do you want to do?",
            choices: [
                { name: "Keep existing wallet", value: "keep" },
                { name: "Set up a new wallet", value: "replace" }
            ]
        });

        if (action.toLowerCase().includes("keep")) {
            console.log("\n✅ Keeping existing EtherMail wallet. No changes made.");
            return;
        }

        console.log("\n⚠️ Existing wallet will be replaced\n");
    }

    const { mode } = await prompt<{ mode: string }>({
        type: "select",
        name: "mode",
        message: "How do you want to set up EtherMail?",
        choices: ["New wallet", "Import existing wallet"]
    });

    let wallet: Wallet | HDNodeWallet;

    if (mode === "New wallet") {
        wallet = Wallet.createRandom();
        console.log("\n✅ New wallet created");
        console.log("Address:", wallet.address);
    } else {
        const { pk } = await prompt<{ pk: string }>({
            type: "password",
            name: "pk",
            message: "Enter your EtherMail account wallet private key"
        });

        wallet = new Wallet(pk);
        console.log("\n✅ Wallet imported");
        console.log("Address:", wallet.address);
    }

    const { passphrase } = await prompt<{ passphrase: string }>({
        type: "password",
        name: "passphrase",
        message: "Create a passphrase to encrypt this wallet"
    });

    const { confirm } = await prompt<{ confirm: string }>({
        type: "password",
        name: "confirm",
        message: "Confirm passphrase"
    });

    if (passphrase !== confirm) {
        throw new Error("Passphrases do not match");
    }

    const { referralCode } = await prompt<{ referralCode: string }>({
        type: "input",
        name: "referralCode",
        message: "Enter a referral code (leave empty to skip)",
        initial: ""
    });

    const encryptedPrivateKey = await encrypt(
        wallet.privateKey,
        passphrase
    );

    await fs.mkdir(STATE_DIR, { recursive: true });

    const configData: Record<string, any> = {
        address: wallet.address,
        encryptedPrivateKey,
        createdAt: new Date().toISOString()
    };

    if (referralCode.trim()) {
        configData.referralCode = referralCode.trim();
    }

    await fs.writeFile(
        CONFIG_PATH,
        JSON.stringify(configData, null, 2),
        { mode: 0o600 }
    );

    console.log("\n🔐 Wallet encrypted and saved successfully");
    console.log("Config path:", CONFIG_PATH);
}

main()
    .then(() => {
        console.log("\n✨ EtherMail skill setup completed");
    })
    .catch((err) => {
        console.error("\n❌ Error setting up EtherMail skill");
        console.error(err instanceof Error ? err.message : err);
        process.exit(1);
    });