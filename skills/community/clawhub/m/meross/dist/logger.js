"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createLogger = createLogger;
const node_util_1 = require("node:util");
const LEVEL_ORDER = {
    error: 0,
    info: 1,
    debug: 2
};
function serializeMeta(meta) {
    if (meta === undefined) {
        return '';
    }
    return ` ${(0, node_util_1.inspect)(meta, { depth: 4, breakLength: 120 })}`;
}
function createLogger(scope, minLevel = 'error') {
    // minLevel is provided explicitly; no env lookups here.
    const log = (level, message, meta) => {
        if (LEVEL_ORDER[level] > LEVEL_ORDER[minLevel]) {
            return;
        }
        const stamp = new Date().toISOString();
        process.stderr.write(`[${stamp}] [${level}] [${scope}] ${message}${serializeMeta(meta)}\n`);
    };
    return {
        error(message, meta) {
            log('error', message, meta);
        },
        info(message, meta) {
            log('info', message, meta);
        },
        debug(message, meta) {
            log('debug', message, meta);
        }
    };
}
