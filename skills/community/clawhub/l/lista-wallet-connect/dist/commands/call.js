/**
 * Raw contract call command -- send arbitrary transactions with custom calldata.
 */
import { getClient } from "../client.js";
import { loadSessions } from "../storage.js";
import { getRpcCandidatesForChain, } from "../rpc.js";
import { requireSession, requireAccount, parseAccount, resolveAddress, requestWithTimeout, } from "../helpers.js";
import { printErrorJson, printJson, stringifyJson } from "../output.js";
import { EXPLORER_URLS } from "./call/constants.js";
import { buildCallTransaction } from "./call/parse.js";
import { simulateTransaction } from "./call/simulate.js";
function resolveSupportedChain(chain) {
    if (chain === "eip155:1" || chain === "eip155:56") {
        return chain;
    }
    return null;
}
export async function cmdCall(args) {
    if (!args.topic) {
        printErrorJson({ error: "--topic required" });
        process.exit(1);
    }
    if (!args.to) {
        printErrorJson({ error: "--to (contract address) required" });
        process.exit(1);
    }
    const evmChain = resolveSupportedChain(args.chain || "eip155:56");
    if (!evmChain) {
        printErrorJson({
            error: `Unsupported chain: ${args.chain}. Only eip155:1 (ETH) and eip155:56 (BSC) are supported.`,
        });
        process.exit(1);
    }
    const client = await getClient();
    const sessionData = requireSession(loadSessions(), args.topic);
    const accountStr = requireAccount(sessionData, evmChain, "EVM");
    const { address: from } = parseAccount(accountStr);
    const resolvedTo = await resolveAddress(args.to);
    if (resolvedTo !== args.to) {
        printErrorJson({ ens: args.to, resolved: resolvedTo });
    }
    const tx = buildCallTransaction(from, resolvedTo, args);
    process.stderr.write(`${stringifyJson({
        action: "sending_raw_tx",
        chain: evmChain,
        from,
        to: resolvedTo,
        data: tx.data ? `${tx.data.slice(0, 10)}...` : undefined,
        value: tx.value,
        gas: tx.gas,
    })}\n`);
    if (!args.noSimulate) {
        const rpcCandidates = getRpcCandidatesForChain(evmChain);
        process.stderr.write(`${stringifyJson({
            action: "simulating_tx",
            rpcCandidates: rpcCandidates.map((candidate) => ({
                rpcUrl: candidate.rpcUrl,
                rpcSource: candidate.source,
            })),
        })}\n`);
        const simResult = await simulateTransaction(evmChain, { from, to: resolvedTo, data: tx.data, value: tx.value }, rpcCandidates);
        if (!simResult.success) {
            printJson({
                status: "simulation_failed",
                error: simResult.error,
                revertReason: simResult.revertReason,
                revertData: simResult.revertData,
                revertSelector: simResult.revertSelector,
                attempts: simResult.attempts,
                hint: "Transaction would revert on-chain. Use --no-simulate to force send (not recommended).",
            });
            await client.core.relayer.transportClose().catch(() => { });
            process.exit(1);
        }
        process.stderr.write(`${stringifyJson({
            action: "simulation_passed",
            rpcUrl: simResult.rpcUrl,
            rpcSource: simResult.rpcSource,
        })}\n`);
    }
    try {
        const txHash = await requestWithTimeout(client, {
            topic: args.topic,
            chainId: evmChain,
            request: {
                method: "eth_sendTransaction",
                params: [tx],
            },
        }, {
            phase: "call",
            context: {
                command: "call",
                topic: args.topic,
                chain: evmChain,
                from,
                to: resolvedTo,
            },
        });
        const explorerUrl = EXPLORER_URLS[evmChain] || "";
        printJson({
            status: "sent",
            txHash,
            chain: evmChain,
            from,
            to: resolvedTo,
            ...(resolvedTo !== args.to ? { ens: args.to } : {}),
            data: tx.data,
            value: tx.value,
            explorer: explorerUrl ? `${explorerUrl}${txHash}` : undefined,
        });
    }
    catch (err) {
        printJson({ status: "rejected", error: err.message });
    }
    await client.core.relayer.transportClose().catch(() => { });
    process.exit(0);
}
