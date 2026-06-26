/**
 * 构造 DG-Lab 协议要求的 URL 字符串
 */
export declare function buildQrCodeString(wsUrl: string, clientId: string): string;
/**
 * 生成二维码 PNG 文件并保存到本地
 * @param wsUrl WebSocket 服务器公网地址
 * @param clientId 动态生成的控制端 ID
 * @param outputDir 图片保存的目录
 * @returns 完整的图片绝对路径
 */
export declare function generateQrCodeImage(wsUrl: string, clientId: string, outputDir: string): Promise<string>;
//# sourceMappingURL=qrcode.d.ts.map