import { existsSync, readFileSync } from "fs";
import { homedir } from "os";
import { join } from "path";
const LENDING_CONFIG_FILE = join(homedir(), ".agent-wallet", "lending-config.json");
const DEFAULT_EVM_RPCS = {
    "eip155:1": [
        "https://eth.llamarpc.com",
        "https://cloudflare-eth.com",
        "https://rpc.ankr.com/eth",
    ],
    "eip155:56": [
        "https://bsc-dataseed.binance.org",
        "https://bsc-dataseed1.binance.org",
        "https://bsc-dataseed2.binance.org",
    ],
};
function loadSharedRpcOverrides() {
    try {
        if (!existsSync(LENDING_CONFIG_FILE))
            return {};
        const raw = readFileSync(LENDING_CONFIG_FILE, "utf8");
        const parsed = JSON.parse(raw);
        if (!parsed || typeof parsed !== "object" || !parsed.rpcUrls) {
            return {};
        }
        return parsed.rpcUrls;
    }
    catch {
        return {};
    }
}
export function getRpcCandidatesForChain(chainId) {
    const overrides = loadSharedRpcOverrides();
    const override = overrides[chainId];
    const candidates = [];
    const seen = new Set();
    if (typeof override === "string" && override.trim().length > 0) {
        const normalized = override.trim();
        if (!seen.has(normalized)) {
            seen.add(normalized);
            candidates.push({ rpcUrl: normalized, source: "shared_config" });
        }
    }
    for (const rpcUrl of DEFAULT_EVM_RPCS[chainId]) {
        const normalized = rpcUrl.trim();
        if (!normalized || seen.has(normalized))
            continue;
        seen.add(normalized);
        candidates.push({ rpcUrl: normalized, source: "default" });
    }
    return candidates;
}
export function getRpcForChain(chainId) {
    const candidates = getRpcCandidatesForChain(chainId);
    return candidates[0];
}
