import { loadAuth, getConfiguredAddress, getEmailFromWallet, sendEmail } from "../lib/ethermail.ts";

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
    if (!toAddress || !subject || !html) throw new Error("Usage: npm run send-email -- <toAddress> <subject> <htmlBody> [--from <alias>]");

    const { userId } = await loadAuth();
    const walletAddress = await getConfiguredAddress();
    const fromEmail = fromAlias || getEmailFromWallet(walletAddress);

    return await sendEmail(userId, {
        from: { name: "", address: fromEmail },
        to: [{ name: "", address: toAddress }],
        subject,
        html,
    });
};

main().then(result => {
    console.log(JSON.stringify(result, null, 2));
}).catch(err => {
    console.error(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }));
    process.exit(1);
});
