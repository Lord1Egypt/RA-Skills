"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.canonicalize = canonicalize;
const canonicalize_1 = __importDefault(require("canonicalize"));
function canonicalize(obj) {
    const result = (0, canonicalize_1.default)(obj);
    if (typeof result !== 'string' || Buffer.byteLength(result) > 262144)
        throw new Error('Invalid or oversized canonical JSON');
    return result;
}
//# sourceMappingURL=canonical.js.map