export function transactionExplorerUrl(signature, cluster) {
    const base = `https://solscan.io/tx/${signature}`;
    if (cluster === 'mainnet-beta' || cluster === 'custom')
        return base;
    return `${base}?cluster=${cluster}`;
}
