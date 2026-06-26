"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getOption = getOption;
exports.requireOption = requireOption;
exports.parseOutputFormat = parseOutputFormat;
function getOption(argv, name) {
    const flag = `--${name}`;
    const index = argv.indexOf(flag);
    if (index === -1) {
        return undefined;
    }
    return argv[index + 1];
}
function requireOption(argv, name) {
    const value = getOption(argv, name);
    if (!value) {
        throw new Error(`missing required option: --${name}`);
    }
    return value;
}
function parseOutputFormat(argv, defaultFormat = "md") {
    const value = (getOption(argv, "format") || defaultFormat).trim();
    if (value === "json" || value === "text" || value === "md") {
        return value;
    }
    throw new Error(`unsupported format: ${value}`);
}
