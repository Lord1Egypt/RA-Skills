"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cli_1 = require("../lib/cli");
const productSearch_1 = require("../productSearch");
async function main() {
    const argv = process.argv.slice(2);
    return await (0, productSearch_1.emitResponse)((0, cli_1.requireOption)(argv, "raw-message"), (0, cli_1.parseOutputFormat)(argv, "md"));
}
main().then((code) => process.exit(code), (error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
});
