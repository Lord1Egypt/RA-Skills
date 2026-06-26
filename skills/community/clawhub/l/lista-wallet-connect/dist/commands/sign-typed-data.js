/**
 * sign-typed-data command — sign EIP-712 typed data (EVM only).
 */
import { readFileSync } from "fs";
import { getClient } from "../client.js";
import { loadSessions } from "../storage.js";
import { requireSession, findAccount, parseAccount, requestWithTimeout } from "../helpers.js";
import { printErrorJson, printJson } from "../output.js";
/**
 * Parse and validate typed data from a JSON string or @file path.
 */
export function parseTypedData(raw) {
    let json;
    if (raw.startsWith("@")) {
        const filePath = raw.slice(1);
        try {
            json = JSON.parse(readFileSync(filePath, "utf8"));
        }
        catch (err) {
            throw new Error(`Failed to read typed data from file "${filePath}": ${err.message}`);
        }
    }
    else {
        try {
            json = JSON.parse(raw);
        }
        catch {
            throw new Error("--data must be valid JSON or a @file path");
        }
    }
    if (!json || typeof json !== "object" || Array.isArray(json)) {
        throw new Error("Typed data must be a JSON object");
    }
    const obj = json;
    const missing = ["domain", "types", "message"].filter((k) => !(k in obj));
    if (missing.length > 0) {
        throw new Error(`Typed data missing required field(s): ${missing.join(", ")}`);
    }
    if (typeof obj.types !== "object" || Array.isArray(obj.types)) {
        throw new Error("Typed data 'types' must be an object");
    }
    return obj;
}
/**
 * Infer primaryType from the types object.
 * Returns the first key that isn't "EIP712Domain".
 */
export function inferPrimaryType(types) {
    const candidates = Object.keys(types).filter((k) => k !== "EIP712Domain");
    if (candidates.length === 0) {
        throw new Error("Cannot infer primaryType: no types defined besides EIP712Domain — provide it explicitly");
    }
    return candidates[0];
}
export async function cmdSignTypedData(args) {
    if (!args.topic || !args.data) {
        printErrorJson({ error: "--topic (or --address) and --data required" });
        process.exit(1);
    }
    let typedData;
    try {
        typedData = parseTypedData(args.data);
    }
    catch (err) {
        printErrorJson({ error: err.message });
        process.exit(1);
    }
    const primaryType = typedData.primaryType ??
        (() => {
            try {
                return inferPrimaryType(typedData.types);
            }
            catch (err) {
                printErrorJson({ error: err.message });
                process.exit(1);
            }
        })();
    const client = await getClient();
    const sessionData = requireSession(loadSessions(), args.topic);
    // EIP-712 is EVM-only — require an eip155 account
    const account = findAccount(sessionData.accounts, args.chain?.startsWith("eip155") ? args.chain : "eip155");
    if (!account) {
        printErrorJson({
            error: "No EVM (eip155) account found in session — EIP-712 is EVM-only",
        });
        process.exit(1);
    }
    const { chainId, address } = parseAccount(account);
    const payload = { ...typedData, primaryType };
    const signature = await requestWithTimeout(client, {
        topic: args.topic,
        chainId,
        request: {
            method: "eth_signTypedData_v4",
            params: [address, JSON.stringify(payload)],
        },
    }, {
        phase: "sign_typed_data",
        context: {
            command: "sign-typed-data",
            topic: args.topic,
            chainId,
            address,
            primaryType,
        },
    });
    printJson({ status: "signed", address, signature, chain: chainId, primaryType });
    await client.core.relayer.transportClose().catch(() => { });
    process.exit(0);
}
