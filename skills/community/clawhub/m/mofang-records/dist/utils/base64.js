/**
 * UTF-8 Base64 编解码工具
 * 魔方网表 bq 查询中的文本值需要 Base64 编码，格式为 _Base64(原文)
 */
export function encodeBase64(input) {
    const encoder = new TextEncoder();
    const bytes = encoder.encode(input);
    let binary = '';
    for (const byte of bytes) {
        binary += String.fromCharCode(byte);
    }
    return btoa(binary);
}
export function decodeBase64(input) {
    const binary = atob(input);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }
    const decoder = new TextDecoder();
    return decoder.decode(bytes);
}
/**
 * 将文本编码为 bq 中使用的值格式: _Base64(text)
 */
export function encodeBqTextValue(text) {
    return '_' + encodeBase64(text);
}
//# sourceMappingURL=base64.js.map