const CHAIN_LABELS = {
    "eip155:1": "Ethereum",
    "eip155:56": "BSC",
};
export function getChainLabel(chainId) {
    return CHAIN_LABELS[chainId] || chainId;
}
export function formatChainDisplay(chainId) {
    return getChainLabel(chainId);
}
