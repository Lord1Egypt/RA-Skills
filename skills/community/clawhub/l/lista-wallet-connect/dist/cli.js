#!/usr/bin/env tsx
import { parseCliInput } from "./cli/args.js";
import { loadLocalEnv } from "./cli/env.js";
import { renderHelp } from "./cli/help.js";
import { loadCliMeta } from "./cli/meta.js";
import { runCommand } from "./cli/router.js";
import { setupDebugLogFile } from "./cli/debug-log.js";
import { printErrorJson } from "./output.js";
const parsed = parseCliInput();
setupDebugLogFile("@lista-dao/lista-wallet-connect-skill", parsed.debugLogFile);
loadLocalEnv();
const meta = loadCliMeta();
export const SKILL_VERSION = meta.skillVersion;
export const SKILL_NAME = meta.skillName;
if (!parsed.command || parsed.help) {
    console.log(renderHelp(meta));
    process.exit(0);
}
runCommand(parsed.command, parsed.args, meta).catch((err) => {
    printErrorJson({ error: err.message });
    process.exit(1);
});
