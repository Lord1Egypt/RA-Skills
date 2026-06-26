import { loadAuth, searchEmails } from "../lib/ethermail.ts";

const main = async () => {
    const args = process.argv.slice(2);
    const mailboxId = args[0];
    if (!mailboxId) throw new Error("Usage: npm run search-emails -- <mailboxId> [page] [limit] [nextCursor]");

    const page = args[1] ? parseInt(args[1], 10) : 1;
    const limit = args[2] ? parseInt(args[2], 10) : 10;
    const next = args[3] || undefined;

    const { userId } = await loadAuth();
    return await searchEmails(userId, mailboxId, page, limit, next);
};

main().then(result => {
    console.log(JSON.stringify(result, null, 2));
}).catch(err => {
    console.error(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }));
    process.exit(1);
});
