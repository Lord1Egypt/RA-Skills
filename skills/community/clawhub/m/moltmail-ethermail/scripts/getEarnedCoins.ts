import { loadAuth, getEarnedCoins } from "../lib/ethermail.ts";

const main = async () => {
    await loadAuth();

    const emcAvailable = await getEarnedCoins();
    console.log(JSON.stringify({ success: true, emc_available: emcAvailable }, null, 2));
};

main().catch(err => {
    console.error("\n❌ Error getting earned coins");
    console.error(err instanceof Error ? err.message : err);
    process.exit(1);
});
