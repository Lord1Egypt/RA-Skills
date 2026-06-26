"use strict";
/**
 * DG-Lab Socket & Bluetooth Protocol Definitions
 * Based on official documentation for Coyote V3.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DGLabWSType = exports.MAX_PULSE_PER_SEND = exports.MAX_MESSAGE_LENGTH = void 0;
exports.strengthCmd = strengthCmd;
exports.clearQueueCmd = clearQueueCmd;
exports.pulseCmd = pulseCmd;
exports.compressFrequency = compressFrequency;
exports.decompressFrequency = decompressFrequency;
exports.generateWaveformHex = generateWaveformHex;
// ─── 协议常量 ───
/** APP 收信 JSON 最大字符长度 */
exports.MAX_MESSAGE_LENGTH = 1950;
/** 单次波形数组最大条数 (官方100条=10s，我们限制70条=7s 留余量) */
exports.MAX_PULSE_PER_SEND = 70;
// 1. WebSocket Layer Protocol
var DGLabWSType;
(function (DGLabWSType) {
    DGLabWSType["HEARTBEAT"] = "heartbeat";
    DGLabWSType["BIND"] = "bind";
    DGLabWSType["MSG"] = "msg";
    DGLabWSType["BREAK"] = "break";
    DGLabWSType["ERROR"] = "error";
})(DGLabWSType || (exports.DGLabWSType = DGLabWSType = {}));
// 2. Message Payload Protocol
function strengthCmd(channel, mode, value) {
    return `strength-${channel}+${mode}+${value}`;
}
function clearQueueCmd(channel) {
    return `clear-${channel}`;
}
/**
 * 创建波形指令，自动按 MAX_PULSE_PER_SEND 截断
 */
function pulseCmd(channel, waveformHexArray) {
    const capped = waveformHexArray.slice(0, exports.MAX_PULSE_PER_SEND);
    const payload = JSON.stringify(capped);
    const cmd = `pulse-${channel}:${payload}`;
    // 安全检查：整条消息(含JSON包装)不能超过1950字符
    if (cmd.length > exports.MAX_MESSAGE_LENGTH) {
        console.warn(`[DG-Lab Protocol] pulse command length ${cmd.length} exceeds ${exports.MAX_MESSAGE_LENGTH}, truncating`);
        // 逐步减少直到合法
        let arr = capped;
        while (arr.length > 1) {
            arr = arr.slice(0, arr.length - 1);
            const shortened = `pulse-${channel}:${JSON.stringify(arr)}`;
            if (shortened.length <= exports.MAX_MESSAGE_LENGTH)
                return shortened;
        }
    }
    return cmd;
}
// 3. Frequency Compression (官方 V3 协议转化公式)
// 输入: 用户友好的波形频率值 (10-1000ms, 对应脉冲频率 1Hz-100Hz)
// 输出: 协议实际发送值 (10-240)
/**
 * 将波形频率(10-1000ms)压缩为协议发送值(10-240)
 * 根据官方 V3 文档的转化公式
 */
function compressFrequency(input) {
    const v = Math.max(10, Math.min(1000, Math.round(input)));
    if (v <= 100) {
        return v;
    }
    else if (v <= 600) {
        return Math.round((v - 100) / 5 + 100);
    }
    else {
        return Math.round((v - 600) / 10 + 200);
    }
}
/**
 * 将协议发送值(10-240)解压为波形频率(10-1000ms)
 * compressFrequency 的逆函数
 */
function decompressFrequency(encoded) {
    if (encoded <= 100) {
        return encoded;
    }
    else if (encoded <= 200) {
        return (encoded - 100) * 5 + 100;
    }
    else {
        return (encoded - 200) * 10 + 600;
    }
}
function generateWaveformHex(points) {
    let hex = '';
    // 前4字节: 频率 (压缩后)
    for (const point of points) {
        hex += compressFrequency(point.freq).toString(16).padStart(2, '0');
    }
    // 后4字节: 波形强度
    for (const point of points) {
        const l = Math.max(0, Math.min(100, Math.round(point.level)));
        hex += l.toString(16).padStart(2, '0');
    }
    return hex;
}
//# sourceMappingURL=protocol.js.map