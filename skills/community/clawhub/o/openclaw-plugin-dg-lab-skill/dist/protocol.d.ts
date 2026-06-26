/**
 * DG-Lab Socket & Bluetooth Protocol Definitions
 * Based on official documentation for Coyote V3.
 */
/** APP 收信 JSON 最大字符长度 */
export declare const MAX_MESSAGE_LENGTH = 1950;
/** 单次波形数组最大条数 (官方100条=10s，我们限制70条=7s 留余量) */
export declare const MAX_PULSE_PER_SEND = 70;
export declare enum DGLabWSType {
    HEARTBEAT = "heartbeat",
    BIND = "bind",
    MSG = "msg",
    BREAK = "break",
    ERROR = "error"
}
export interface DGLabWSMessage {
    type: DGLabWSType;
    clientId: string;
    targetId?: string;
    message: string;
}
export declare function strengthCmd(channel: '1' | '2', mode: '0' | '1' | '2', value: number): string;
export declare function clearQueueCmd(channel: '1' | '2'): string;
/**
 * 创建波形指令，自动按 MAX_PULSE_PER_SEND 截断
 */
export declare function pulseCmd(channel: 'A' | 'B', waveformHexArray: string[]): string;
/**
 * 将波形频率(10-1000ms)压缩为协议发送值(10-240)
 * 根据官方 V3 文档的转化公式
 */
export declare function compressFrequency(input: number): number;
/**
 * 将协议发送值(10-240)解压为波形频率(10-1000ms)
 * compressFrequency 的逆函数
 */
export declare function decompressFrequency(encoded: number): number;
export interface WavePoint {
    freq: number;
    level: number;
}
export declare function generateWaveformHex(points: [WavePoint, WavePoint, WavePoint, WavePoint]): string;
//# sourceMappingURL=protocol.d.ts.map