"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.JEPGuardSDK = void 0;
exports.init = init;
const path_1 = __importDefault(require("path"));
const os_1 = __importDefault(require("os"));
class JEPGuardSDK {
    socketPath;
    skillId;
    constructor(skillId, socketPath) {
        if (socketPath)
            throw new Error("Custom socket paths are not trusted");
        this.skillId = skillId;
        this.socketPath = socketPath || path_1.default.join(os_1.default.tmpdir(), 'jep-guard.sock');
    }
    async call(method, payload) {
        return require('../../transport').guardCall(method, this.skillId, payload);
    }
    async judge(decision) {
        return this.call('JUDGE', { ...decision, target: decision.target || '' });
    }
    async delegate(target, scope, payload) {
        return this.call('DELEGATE', { target, scope, payload });
    }
    async verify(targetEvent, verdict, evidence) {
        return this.call('VERIFY', { target_event: targetEvent, verdict, evidence });
    }
    async terminate(targetEvent, reason) {
        return this.call('TERMINATE', { target_event: targetEvent, reason });
    }
}
exports.JEPGuardSDK = JEPGuardSDK;
function init(skillId) {
    return new JEPGuardSDK(skillId);
}
//# sourceMappingURL=index.js.map