/**
 * UTF-8 Base64 编解码工具
 * 魔方网表 bq 查询中的文本值需要 Base64 编码，格式为 _Base64(原文)
 */
export declare function encodeBase64(input: string): string;
export declare function decodeBase64(input: string): string;
/**
 * 将文本编码为 bq 中使用的值格式: _Base64(text)
 */
export declare function encodeBqTextValue(text: string): string;
//# sourceMappingURL=base64.d.ts.map