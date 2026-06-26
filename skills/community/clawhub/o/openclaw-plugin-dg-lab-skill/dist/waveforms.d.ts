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
/**
 * 惩罚波形: 高频持续刺激
 * 不限制长度，由 sendPulseWithContinuity() 自动分段发送
 */
export declare function punishWave(durationMs?: number): string[];
/**
 * 轻柔安抚波形: 低频呼吸式
 * 不限制长度，由 sendPulseWithContinuity() 自动分段发送
 */
export declare function teaseWave(durationMs?: number): string[];
/**
 * 测试波形: 中频短促 (0.5秒)
 */
export declare function testWave(): string[];
//# sourceMappingURL=waveforms.d.ts.map