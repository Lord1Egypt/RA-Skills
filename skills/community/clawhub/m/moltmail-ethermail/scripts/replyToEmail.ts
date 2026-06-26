import { loadAuth, getConfiguredAddress, getEmailFromWallet, replyToEmail } from "../lib/ethermail.ts";

const main = async () => {
    const args = process.argv.slice(2);
    const fromIndex = args.indexOf("--from");
    let fromAlias: string | undefined;
    if (fromIndex !== -1) {
        fromAlias = args[fromIndex + 1];
        args.splice(fromIndex, 2);
    }

    const toAddress = args[0];
    const subject = args[1];
    const html = args[2];
    const originalMessageId = args[3];
    const mailboxId = args[4];
    if (!toAddress || !subject || !html || !originalMessageId || !mailboxId) {
        throw new Error("Usage: npm run reply-email -- <toAddress> <subject> <htmlBody> <originalMessageId> <mailboxId> [--from <alias>]");
    }

    const { userId } = await loadAuth();
    const walletAddress = await getConfiguredAddress();
    const fromEmail = fromAlias || getEmailFromWallet(walletAddress);

    return await replyToEmail(userId, {
        from: { name: "", address: fromEmail },
        to: [{ name: "", address: toAddress }],
        subject,
        html,
        reference: {
            action: "reply",
            id: originalMessageId,
            mailbox: mailboxId,
        },
    });
};

main().then(result => {
    console.log(JSON.stringify(result, null, 2));
}).catch(err => {
    console.error(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }));
    process.exit(1);
});
