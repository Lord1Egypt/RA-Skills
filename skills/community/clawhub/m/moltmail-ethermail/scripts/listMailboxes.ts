import { loadAuth, listMailboxes } from "../lib/ethermail.ts";

const main = async () => {
    const { userId } = await loadAuth();
    return await listMailboxes(userId);
};

main().then(result => {
    console.log(JSON.stringify(result, null, 2));
}).catch(err => {
    console.error(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }));
    process.exit(1);
});
