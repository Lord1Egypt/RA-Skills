const CHAIN_LABELS: Record<string, string> = {
  "eip155:1": "Ethereum",
  "eip155:56": "BSC",
};

export function getChainLabel(chainId: string): string {
  return CHAIN_LABELS[chainId] || chainId;
}

export function formatChainDisplay(chainId: string): string {
  return getChainLabel(chainId);
}
