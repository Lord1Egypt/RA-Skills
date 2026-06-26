import { loadAuth } from "../lib/ethermail.ts";

const main = async () => {
    const { userId } = await loadAuth();

    console.log(JSON.stringify({ success: true, referralCode: userId }, null, 2));
};

main().catch(err => {
    console.error("\n❌ Error getting referral code");
    console.error(err instanceof Error ? err.message : err);
    process.exit(1);
});
