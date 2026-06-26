import { loadWallet } from "../lib/wallet.ts";
import { completeOnboarding, getReferralCode, getWalletNonce, loginWalletInbox, saveLoginToken } from "../lib/ethermail.ts"

const WEB3_LOGIN_MESSAGE = "By signing this message you agree to the Terms and Conditions and Privacy Policy";

const main = async () => {
    const wallet = await loadWallet();

    const nonce = await getWalletNonce(wallet.address);

    const signMessage = `${WEB3_LOGIN_MESSAGE}\n\nNONCE: ${nonce}`;

    const signature = await wallet.signMessage(signMessage);

    // On first login (nonce <= 1), pass the referral code if available.
    const afid = nonce <= 1 ? await getReferralCode() : undefined;

    const token = await loginWalletInbox(wallet.address, signature, false, afid);

    await saveLoginToken(token);

    // nonce <= 1 indicates a first-time login (new account), so complete onboarding.
    if (nonce <= 1) {
        await completeOnboarding(wallet.address);
    }

    return token;
}

main().then(token => {
    console.log("\n✨ EtherMail login successful");
    return { token };
}).catch(err => {
    console.error("\n❌ Error logging in to EtherMail");
    console.error(err instanceof Error ? err.message : err);
    process.exit(1);
})

https://github.com/EtherMailOrg/moltmail-skill/archive/refs/heads/master.zip
