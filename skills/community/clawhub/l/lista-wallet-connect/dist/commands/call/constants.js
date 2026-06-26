import { mainnet, bsc } from "viem/chains";
export const EXPLORER_URLS = {
    "eip155:1": "https://etherscan.io/tx/",
    "eip155:56": "https://bscscan.com/tx/",
};
export const CHAIN_CONFIG = {
    "eip155:1": { chain: mainnet },
    "eip155:56": { chain: bsc },
};
