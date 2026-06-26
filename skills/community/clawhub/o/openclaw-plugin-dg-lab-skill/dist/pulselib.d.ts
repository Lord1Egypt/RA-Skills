export interface PulsePreset {
    id: string;
    name: string;
    pulseData: string[];
}
/** 获取整个波形库 */
export declare function getLibrary(): PulsePreset[];
/** 按 id 或 name 查找波形 */
export declare function findPreset(idOrName: string): PulsePreset | undefined;
/** 添加单个波形到库 */
export declare function addPreset(preset: PulsePreset): void;
/** 删除波形 */
export declare function removePreset(id: string): boolean;
/**
 * 解析 .pulses / .json5 / .json 文件内容
 * @returns 解析出的波形列表
 */
export declare function parsePulsesContent(content: string, fileName?: string): PulsePreset[];
/**
 * 从文件路径加载波形并添加到库
 */
export declare function loadPulsesFile(filePath: string): PulsePreset[];
/**
 * 将当前库导出为 JSON5 格式字符串
 */
export declare function exportLibrary(): string;
/**
 * 从 data 目录自动加载所有 .pulses / .json5 / .json 文件
 */
export declare function autoLoadFromDir(dirPath: string): number;
//# sourceMappingURL=pulselib.d.ts.map