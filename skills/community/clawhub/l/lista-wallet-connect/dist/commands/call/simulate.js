import { createPublicClient, http } from "viem";
import { CHAIN_CONFIG } from "./constants.js";
const FOURBYTE_API = "https://www.4byte.directory/api/v1/signatures/";
const selectorSignatureCache = new Map();
function toMessage(value) {
    if (value instanceof Error) {
        const errLike = value;
        return errLike.message || errLike.shortMessage || errLike.details || String(value);
    }
    if (typeof value === "string")
        return value;
    return String(value);
}
function extractRevertData(message) {
    const patterns = [
        /Execution reverted with reason:\s*[^\n]*?(0x[0-9a-fA-F]{8,})/i,
        /execution reverted:?\s*[^\n]*?(0x[0-9a-fA-F]{8,})/i,
    ];
    for (const pattern of patterns) {
        const match = message.match(pattern);
        const candidate = match?.[1];
        if (!candidate)
            continue;
        if (candidate.length < 10)
            continue;
        if (candidate.length % 2 !== 0)
            continue;
        return candidate.toLowerCase();
    }
    return undefined;
}
function extractTextReason(message) {
    const normalize = (value) => {
        const cleaned = value.trim().replace(/\.+$/, "");
        if (/^0x$/i.test(cleaned))
            return undefined;
        return cleaned || undefined;
    };
    const withReasonMatch = message.match(/Execution reverted with reason:\s*([^\n]+)/i);
    if (withReasonMatch?.[1]) {
        const reason = withReasonMatch[1].replace(/:\s*0x[0-9a-fA-F]{8,}\.?$/i, "");
        return normalize(reason);
    }
    const revertedMatch = message.match(/execution reverted:?\s*([^\n]+)/i);
    if (revertedMatch?.[1]) {
        const reason = revertedMatch[1].replace(/:\s*0x[0-9a-fA-F]{8,}\.?$/i, "");
        return normalize(reason);
    }
    return undefined;
}
function extractSelectorFromReason(reason) {
    if (!reason)
        return undefined;
    const cleaned = reason.trim().replace(/\.+$/, "");
    if (!/^0x[0-9a-fA-F]{8}$/.test(cleaned))
        return undefined;
    return cleaned.toLowerCase();
}
async function lookupSelectorSignature(selector) {
    const normalized = selector.toLowerCase();
    if (selectorSignatureCache.has(normalized)) {
        return selectorSignatureCache.get(normalized);
    }
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 2500);
    try {
        const url = `${FOURBYTE_API}?hex_signature=${encodeURIComponent(normalized)}`;
        const response = await fetch(url, {
            method: "GET",
            signal: controller.signal,
            headers: { accept: "application/json" },
        });
        if (!response.ok) {
            selectorSignatureCache.set(normalized, undefined);
            return undefined;
        }
        const payload = (await response.json());
        const signature = payload.results?.[0]?.text_signature;
        if (typeof signature === "string" && signature.length > 0) {
            selectorSignatureCache.set(normalized, signature);
            return signature;
        }
        selectorSignatureCache.set(normalized, undefined);
        return undefined;
    }
    catch {
        return undefined;
    }
    finally {
        clearTimeout(timeout);
    }
}
export async function simulateTransaction(chainId, tx, rpcCandidates) {
    const config = CHAIN_CONFIG[chainId];
    const attempts = [];
    for (const candidate of rpcCandidates) {
        const client = createPublicClient({
            chain: config.chain,
            transport: http(candidate.rpcUrl),
        });
        try {
            await client.call({
                account: tx.from,
                to: tx.to,
                data: tx.data,
                value: tx.value ? BigInt(tx.value) : undefined,
            });
            return {
                success: true,
                rpcUrl: candidate.rpcUrl,
                rpcSource: candidate.source,
            };
        }
        catch (err) {
            const message = toMessage(err);
            const isRevert = /revert/i.test(message);
            const revertData = extractRevertData(message);
            const textReason = extractTextReason(message);
            const selectorFromReason = extractSelectorFromReason(textReason);
            const revertSelector = revertData
                ? revertData.slice(0, 10)
                : selectorFromReason;
            const signature = revertSelector ? await lookupSelectorSignature(revertSelector) : undefined;
            attempts.push({
                rpcUrl: candidate.rpcUrl,
                source: candidate.source,
                error: message,
            });
            if (isRevert || revertData) {
                return {
                    success: false,
                    error: message,
                    revertReason: signature || textReason || "Contract execution reverted",
                    revertData,
                    revertSelector,
                    attempts,
                };
            }
        }
    }
    return {
        success: false,
        error: attempts.length > 0
            ? attempts.map((a) => `[${a.source}] ${a.rpcUrl}: ${a.error}`).join(" | ")
            : "Simulation failed with no RPC candidates",
        attempts,
    };
}
