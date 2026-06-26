"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SkillError = void 0;
exports.isRecord = isRecord;
exports.normalizeWhitespace = normalizeWhitespace;
exports.toErrorPayload = toErrorPayload;
class SkillError extends Error {
    constructor(code, message, cause = undefined) {
        super(message);
        this.code = code;
        this.cause = cause;
        this.name = 'SkillError';
    }
}
exports.SkillError = SkillError;
function isRecord(value) {
    return typeof value === 'object' && value !== null;
}
function normalizeWhitespace(value) {
    return value.trim().replace(/\s+/g, ' ');
}
function toErrorPayload(error) {
    if (error instanceof SkillError) {
        return {
            ok: false,
            error: {
                code: error.code,
                message: error.message
            }
        };
    }
    if (error instanceof Error) {
        return {
            ok: false,
            error: {
                code: 'INTERNAL_ERROR',
                message: error.message
            }
        };
    }
    return {
        ok: false,
        error: {
            code: 'INTERNAL_ERROR',
            message: 'Unknown internal error.'
        }
    };
}
