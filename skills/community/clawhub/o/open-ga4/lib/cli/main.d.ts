import { type Ga4Runtime } from "../runtime.js";
import { type ParsedArgs } from "./args.js";
import type { Streams } from "./render.js";
/**
 * A string literal, not a read of package.json at runtime: package.json is
 * not shipped inside the skill bundle, so a runtime read would work in this
 * checkout and fail after install. src/cli/main.test.ts asserts this equals
 * package.json's version, so the two cannot silently drift apart.
 */
export declare const VERSION = "0.2.1";
export declare function main(argv: string[], env: NodeJS.ProcessEnv, streams: Streams): Promise<number>;
/** The "command" branch of ParsedArgs, narrowed once so every reader below can use it directly. */
export type CommandArgs = Extract<ParsedArgs, {
    kind: "command";
}>;
/**
 * Converts each command's flags into the operation's own parameter object and
 * returns its markdown, or with `--json`, its structured details instead.
 * Kept in this file, not split out: this mapping is what a reviewer most
 * needs to see in one place.
 */
export declare function dispatch(runtime: Ga4Runtime, parsed: CommandArgs): Promise<string>;
