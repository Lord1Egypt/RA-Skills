import { mainnet, bsc, type Chain } from "viem/chains";
import type { SupportedEvmChainId } from "../../rpc.js";

export const EXPLORER_URLS: Record<string, string> = {
  "eip155:1": "https://etherscan.io/tx/",
  "eip155:56": "https://bscscan.com/tx/",
};

export const CHAIN_CONFIG: Record<SupportedEvmChainId, { chain: Chain }> = {
  "eip155:1": { chain: mainnet },
  "eip155:56": { chain: bsc },
};
