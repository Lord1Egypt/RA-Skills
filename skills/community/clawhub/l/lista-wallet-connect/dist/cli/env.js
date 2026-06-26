import { existsSync, readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
export function loadLocalEnv() {
    const envPath = resolve(dirname(fileURLToPath(import.meta.url)), "../../.env");
    if (!existsSync(envPath))
        return;
    const content = readFileSync(envPath, "utf8");
    for (const rawLine of content.split(/\r?\n/)) {
        const line = rawLine.trim();
        if (!line || line.startsWith("#"))
            continue;
        const normalized = line.startsWith("export ")
            ? line.slice("export ".length).trim()
            : line;
        const sep = normalized.indexOf("=");
        if (sep <= 0)
            continue;
        const key = normalized.slice(0, sep).trim();
        if (!key || process.env[key] !== undefined)
            continue;
        let value = normalized.slice(sep + 1).trim();
        if ((value.startsWith('"') && value.endsWith('"')) ||
            (value.startsWith("'") && value.endsWith("'"))) {
            value = value.slice(1, -1);
        }
        process.env[key] = value;
    }
}
