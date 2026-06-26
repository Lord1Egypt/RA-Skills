import { loadWallet } from "../lib/wallet.ts";
import { completeOnboarding } from "../lib/ethermail.ts";

const main = async () => {
    const wallet = await loadWallet();

    return await completeOnboarding(wallet.address);
}

main().then(() => {
    console.log("\n✨ EtherMail onboarding completed!");
}).catch(err => {
    console.error("\n❌ Error completing onboarding");
    console.error(err instanceof Error ? err.message : err);
    process.exit(1);
})