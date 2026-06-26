import { cmdPair } from "../commands/pair.js";
import { cmdAuth } from "../commands/auth.js";
import { cmdSign } from "../commands/sign.js";
import { cmdSignTypedData } from "../commands/sign-typed-data.js";
import { cmdCall } from "../commands/call.js";
import { cmdHealth } from "../commands/health.js";
import { cmdStatus, cmdSessions, cmdListSessions, cmdWhoami, cmdDeleteSession, } from "../commands/sessions.js";
import { loadSessions } from "../storage.js";
import { findSessionByAddress } from "../client.js";
import { printErrorJson, printJson } from "../output.js";
function resolveAddress(args) {
    if (args.address && !args.topic) {
        const sessions = loadSessions();
        const match = findSessionByAddress(sessions, args.address);
        if (!match) {
            printErrorJson({ error: "No session found for address", address: args.address });
            process.exit(1);
        }
        args.topic = match.topic;
    }
    return args;
}
export async function runCommand(command, args, meta) {
    const commands = {
        pair: cmdPair,
        status: cmdStatus,
        auth: (a) => cmdAuth(resolveAddress(a)),
        sign: (a) => cmdSign(resolveAddress(a)),
        "sign-typed-data": (a) => cmdSignTypedData(resolveAddress(a)),
        call: (a) => cmdCall(resolveAddress(a)),
        sessions: cmdSessions,
        "list-sessions": cmdListSessions,
        whoami: cmdWhoami,
        "delete-session": cmdDeleteSession,
        health: cmdHealth,
        version: async () => {
            printJson({
                skill: meta.skillName,
                version: meta.skillVersion,
                hint: "If version mismatch, run: npm install && npm run build",
            });
        },
    };
    if (!commands[command]) {
        console.error(`Unknown command: ${command}`);
        process.exit(1);
    }
    await commands[command](args);
}
