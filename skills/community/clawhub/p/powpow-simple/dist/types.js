/**
 * POWPOW Simple Skill - 类型定义
 */
// 错误类型
export class PowpowError extends Error {
    constructor(message, code, statusCode) {
        super(message);
        this.code = code;
        this.statusCode = statusCode;
        this.name = 'PowpowError';
    }
}
//# sourceMappingURL=types.js.map