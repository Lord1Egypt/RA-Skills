import { loadAuth, markEmailAsRead } from "../lib/ethermail.ts";

const main = async () => {
    const args = process.argv.slice(2);
    const mailboxId = args[0];
    const messageId = args[1];
    if (!mailboxId || !messageId) throw new Error("Usage: npm run mark-read -- <mailboxId> <messageId>");

    const { userId } = await loadAuth();
    return await markEmailAsRead(userId, mailboxId, messageId);
};

main().then(result => {
    console.log(JSON.stringify(result, null, 2));
}).catch(err => {
    console.error(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }));
    process.exit(1);
});
