import crypto from "node:crypto";

/**
 * 微信服务号消息加解密 (WXBizMsgCrypt)
 *
 * 与企业微信的核心差异：
 * - 签名算法相同：sha1(sort(token, timestamp, nonce, encrypt))
 * - AES 加解密相同：AES-256-CBC + PKCS#7(block=32)
 * - 协议包相同：[16B random][4B msg_len][msg][appid/receiveId]
 * - ReceiveId 对 MP 来说是 appId（企微是 corpId），但都是尾部字符串匹配
 */

/**
 * **decodeEncodingAESKey (解码 AES Key)**
 *
 * 微信后台的 EncodingAESKey 是 43 字符 base64（不含尾部 `=`）。
 * 补齐后 base64 解码得到 32 字节 AES Key。
 */
export function decodeEncodingAESKey(encodingAESKey: string): Buffer {
  const trimmed = encodingAESKey.trim();
  if (!trimmed) throw new Error("encodingAESKey missing");
  const withPadding = trimmed.endsWith("=") ? trimmed : `${trimmed}=`;
  const key = Buffer.from(withPadding, "base64");
  if (key.length !== 32) {
    throw new Error(
      `invalid encodingAESKey (expected 32 bytes after base64 decode, got ${key.length})`,
    );
  }
  return key;
}

export const WECHAT_PKCS7_BLOCK_SIZE = 32;

function pkcs7Pad(buf: Buffer, blockSize: number): Buffer {
  const mod = buf.length % blockSize;
  const pad = mod === 0 ? blockSize : blockSize - mod;
  const padByte = Buffer.from([pad]);
  return Buffer.concat([buf, Buffer.alloc(pad, padByte[0]!)]);
}

export function pkcs7Unpad(buf: Buffer, blockSize: number): Buffer {
  if (buf.length === 0) throw new Error("invalid pkcs7 payload");
  const pad = buf[buf.length - 1]!;
  if (pad < 1 || pad > blockSize) {
    throw new Error("invalid pkcs7 padding");
  }
  if (pad > buf.length) {
    throw new Error("invalid pkcs7 payload");
  }
  for (let i = 0; i < pad; i += 1) {
    if (buf[buf.length - 1 - i] !== pad) {
      throw new Error("invalid pkcs7 padding");
    }
  }
  return buf.subarray(0, buf.length - pad);
}

function sha1Hex(input: string): string {
  return crypto.createHash("sha1").update(input).digest("hex");
}

/**
 * **computeMsgSignature (计算消息签名)**
 *
 * msg_signature = sha1(sort(token, timestamp, nonce, encrypt).join(""))
 * 用于安全模式/兼容模式下验证回调请求。
 */
export function computeMsgSignature(params: {
  token: string;
  timestamp: string;
  nonce: string;
  encrypt: string;
}): string {
  const parts = [params.token, params.timestamp, params.nonce, params.encrypt]
    .map((v) => String(v ?? ""))
    .sort();
  return sha1Hex(parts.join(""));
}

/**
 * **computeServerVerifySignature (计算服务器校验签名)**
 *
 * 服务器 URL 校验（明文模式 GET）使用：
 * signature = sha1(sort(token, timestamp, nonce).join(""))
 * 注意比 msg_signature 少了 encrypt 字段。
 */
export function computeServerVerifySignature(params: {
  token: string;
  timestamp: string;
  nonce: string;
}): string {
  const parts = [params.token, params.timestamp, params.nonce]
    .map((v) => String(v ?? ""))
    .sort();
  return sha1Hex(parts.join(""));
}

export function verifyMsgSignature(params: {
  token: string;
  timestamp: string;
  nonce: string;
  encrypt: string;
  signature: string;
}): boolean {
  if (!params.signature) return false;
  const expected = computeMsgSignature({
    token: params.token,
    timestamp: params.timestamp,
    nonce: params.nonce,
    encrypt: params.encrypt,
  });
  return timingSafeEqualStr(expected, params.signature);
}

export function verifyServerSignature(params: {
  token: string;
  timestamp: string;
  nonce: string;
  signature: string;
}): boolean {
  if (!params.signature) return false;
  const expected = computeServerVerifySignature({
    token: params.token,
    timestamp: params.timestamp,
    nonce: params.nonce,
  });
  return timingSafeEqualStr(expected, params.signature);
}

function timingSafeEqualStr(a: string, b: string): boolean {
  const ab = Buffer.from(a, "utf8");
  const bb = Buffer.from(b, "utf8");
  if (ab.length !== bb.length) return false;
  return crypto.timingSafeEqual(ab, bb);
}

/**
 * **decryptEncrypted (解密密文)**
 *
 * 将回调包中的 Encrypt 字段解密为明文 XML。
 * 协议：`[16B random][4B BE msgLen][msg UTF8][appId UTF8]`。
 * 如果传入 receiveId（即 appId）会校验尾部匹配。
 */
export function decryptEncrypted(params: {
  encodingAESKey: string;
  receiveId?: string;
  encrypt: string;
}): string {
  const aesKey = decodeEncodingAESKey(params.encodingAESKey);
  const iv = aesKey.subarray(0, 16);
  const decipher = crypto.createDecipheriv("aes-256-cbc", aesKey, iv);
  decipher.setAutoPadding(false);
  const decryptedPadded = Buffer.concat([
    decipher.update(Buffer.from(params.encrypt, "base64")),
    decipher.final(),
  ]);
  const decrypted = pkcs7Unpad(decryptedPadded, WECHAT_PKCS7_BLOCK_SIZE);

  if (decrypted.length < 20) {
    throw new Error(
      `invalid decrypted payload (expected at least 20 bytes, got ${decrypted.length})`,
    );
  }

  const msgLen = decrypted.readUInt32BE(16);
  const msgStart = 20;
  const msgEnd = msgStart + msgLen;
  if (msgEnd > decrypted.length) {
    throw new Error(
      `invalid decrypted msg length (msgEnd=${msgEnd}, payloadLength=${decrypted.length})`,
    );
  }
  const msg = decrypted.subarray(msgStart, msgEnd).toString("utf8");

  const receiveId = params.receiveId ?? "";
  if (receiveId) {
    const trailing = decrypted.subarray(msgEnd).toString("utf8");
    if (trailing !== receiveId) {
      throw new Error(
        `receiveId mismatch (expected "${receiveId}", got "${trailing}")`,
      );
    }
  }

  return msg;
}

/**
 * **encryptPlaintext (加密明文)**
 *
 * 将要回复的明文 XML 打包加密。
 */
export function encryptPlaintext(params: {
  encodingAESKey: string;
  receiveId?: string;
  plaintext: string;
}): string {
  const aesKey = decodeEncodingAESKey(params.encodingAESKey);
  const iv = aesKey.subarray(0, 16);
  const random16 = crypto.randomBytes(16);
  const msg = Buffer.from(params.plaintext ?? "", "utf8");
  const msgLen = Buffer.alloc(4);
  msgLen.writeUInt32BE(msg.length, 0);
  const receiveId = Buffer.from(params.receiveId ?? "", "utf8");

  const raw = Buffer.concat([random16, msgLen, msg, receiveId]);
  const padded = pkcs7Pad(raw, WECHAT_PKCS7_BLOCK_SIZE);
  const cipher = crypto.createCipheriv("aes-256-cbc", aesKey, iv);
  cipher.setAutoPadding(false);
  const encrypted = Buffer.concat([cipher.update(padded), cipher.final()]);
  return encrypted.toString("base64");
}
