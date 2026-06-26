"use strict";
/**
 * DG-Lab V3 Waveform Generators
 *
 * 官方协议: pulse-X:["hex1","hex2",...]
 * 每条 hex 是 8 字节(16 字符): 4字节频率(压缩值) + 4字节波形强度
 * 每条代表 100ms 的数据 (4组x25ms)
 * 频率输入范围: 10-1000 (经 compressFrequency 压缩为 10-240)
 * 波形强度范围: 0-100
 *
 * 单次最多发送 70 条 = 7 秒 (留余量给 JSON 包装)
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.punishWave = punishWave;
exports.teaseWave = teaseWave;
exports.testWave = testWave;
const protocol_1 = require("./protocol");
/**
 * 生成单条 8 字节 hex 波形数据
 * @param freqMs 波形频率(ms), 10-1000，会自动压缩
 * @param level 波形强度, 0-100
 */
function waveHex(freqMs, level) {
    const f = (0, protocol_1.compressFrequency)(freqMs);
    const l = Math.max(0, Math.min(100, Math.round(level)));
    const fHex = f.toString(16).padStart(2, '0');
    const lHex = l.toString(16).padStart(2, '0');
    // 4个相同频率 + 4个相同强度 (100ms内4个25ms窗口相同)
    return `${fHex}${fHex}${fHex}${fHex}${lHex}${lHex}${lHex}${lHex}`;
}
/**
 * 惩罚波形: 高频持续刺激
 * 不限制长度，由 sendPulseWithContinuity() 自动分段发送
 */
function punishWave(durationMs = 1000) {
    const count = Math.max(1, Math.floor(durationMs / 100));
    const result = [];
    for (let i = 0; i < count; i++) {
        result.push(waveHex(15, 100));
    }
    return result;
}
/**
 * 轻柔安抚波形: 低频呼吸式
 * 不限制长度，由 sendPulseWithContinuity() 自动分段发送
 */
function teaseWave(durationMs = 1000) {
    const count = Math.max(1, Math.floor(durationMs / 100));
    const result = [];
    for (let i = 0; i < count; i++) {
        const sineValue = (Math.sin(i / 3) + 1) / 2;
        const level = 20 + 60 * sineValue;
        result.push(waveHex(200, level));
    }
    return result;
}
/**
 * 测试波形: 中频短促 (0.5秒)
 */
function testWave() {
    return [
        waveHex(100, 50), // 10Hz 中频
        waveHex(100, 70),
        waveHex(100, 90),
        waveHex(100, 70),
        waveHex(100, 50),
    ];
}
//# sourceMappingURL=waveforms.js.map