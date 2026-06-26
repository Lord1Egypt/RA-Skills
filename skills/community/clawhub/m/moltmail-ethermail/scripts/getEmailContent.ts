import { loadAuth, getEmailContent, markEmailAsRead } from "../lib/ethermail.ts";

const main = async () => {
    const args = process.argv.slice(2);
    const mailboxId = args[0];
    const messageId = args[1];
    if (!mailboxId || !messageId) throw new Error("Usage: npm run get-email -- <mailboxId> <messageId>");

    const { userId } = await loadAuth();
    const email = await getEmailContent(userId, mailboxId, messageId);

    // Automatically mark as read when content is fetched
    await markEmailAsRead(userId, mailboxId, messageId);

    return email;
};

main().then(result => {
    console.log(JSON.stringify(result, null, 2));
}).catch(err => {
    console.error(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }));
    process.exit(1);
});
