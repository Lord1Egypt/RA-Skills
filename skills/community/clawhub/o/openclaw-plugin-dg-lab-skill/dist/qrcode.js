"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildQrCodeString = buildQrCodeString;
exports.generateQrCodeImage = generateQrCodeImage;
const QRCode = __importStar(require("qrcode"));
const path = __importStar(require("path"));
const DG_LAB_URL_BASE = 'https://www.dungeon-lab.com/app-download.php';
const DG_LAB_TAG = 'DGLAB-SOCKET';
/**
 * 构造 DG-Lab 协议要求的 URL 字符串
 */
function buildQrCodeString(wsUrl, clientId) {
    const serverWithClient = `${wsUrl.replace(/\/$/, '')}/${clientId}`;
    return [DG_LAB_URL_BASE, DG_LAB_TAG, serverWithClient].join('#');
}
/**
 * 生成二维码 PNG 文件并保存到本地
 * @param wsUrl WebSocket 服务器公网地址
 * @param clientId 动态生成的控制端 ID
 * @param outputDir 图片保存的目录
 * @returns 完整的图片绝对路径
 */
async function generateQrCodeImage(wsUrl, clientId, outputDir) {
    const content = buildQrCodeString(wsUrl, clientId);
    // 使用时间戳和 ID 确保文件名唯一，避免并发覆盖
    const fileName = `dg_qr_${clientId.substring(0, 6)}_${Date.now()}.png`;
    const filePath = path.join(outputDir, fileName);
    try {
        await QRCode.toFile(filePath, content, {
            errorCorrectionLevel: 'M',
            margin: 2,
            width: 400
        });
        return filePath;
    }
    catch (err) {
        console.error('[DG-Lab] Failed to generate QR Code image:', err);
        throw err;
    }
}
//# sourceMappingURL=qrcode.js.map