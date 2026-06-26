"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const common_1 = require("../common");
const cli_1 = require("../lib/cli");
const recognizePlatformLink_1 = require("../recognizePlatformLink");
function main() {
    const argv = process.argv.slice(2);
    (0, common_1.printJson)((0, recognizePlatformLink_1.recognizeRawMessage)((0, cli_1.requireOption)(argv, "raw-message")));
    return 0;
}
process.exit(main());
