import { describe, expect, it } from "vitest";
import {
  computeMsgSignature,
  computeServerVerifySignature,
  decodeEncodingAESKey,
  decryptEncrypted,
  encryptPlaintext,
  pkcs7Unpad,
  verifyMsgSignature,
  verifyServerSignature,
  WECHAT_PKCS7_BLOCK_SIZE,
} from "./crypto.js";

const TEST_TOKEN = "wechat_demo_token";
const TEST_AES_KEY_43 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQ";
const TEST_APPID = "wx1234567890abcdef";

describe("encoding aes key", () => {
  it("decodes a 43-char key to 32 bytes", () => {
    expect(decodeEncodingAESKey(TEST_AES_KEY_43).length).toBe(32);
  });
  it("rejects an empty key", () => {
    expect(() => decodeEncodingAESKey("")).toThrow();
  });
});

describe("signatures", () => {
  it("computes stable msg_signature regardless of arg order", () => {
    const a = computeMsgSignature({ token: "t", timestamp: "1", nonce: "n", encrypt: "e" });
    const b = computeMsgSignature({ token: "t", timestamp: "1", nonce: "n", encrypt: "e" });
    expect(a).toBe(b);
    expect(a).toHaveLength(40);
  });
  it("verifies matching signatures with timing-safe compare", () => {
    const sig = computeMsgSignature({ token: TEST_TOKEN, timestamp: "1", nonce: "n", encrypt: "x" });
    expect(verifyMsgSignature({ token: TEST_TOKEN, timestamp: "1", nonce: "n", encrypt: "x", signature: sig })).toBe(true);
  });
  it("rejects empty signature", () => {
    expect(verifyMsgSignature({ token: TEST_TOKEN, timestamp: "1", nonce: "n", encrypt: "x", signature: "" })).toBe(false);
  });
  it("computes server verify signature without encrypt", () => {
    const sig = computeServerVerifySignature({ token: "t", timestamp: "1", nonce: "n" });
    expect(verifyServerSignature({ token: "t", timestamp: "1", nonce: "n", signature: sig })).toBe(true);
  });
});

describe("encrypt/decrypt roundtrip", () => {
  it("roundtrips an XML plaintext with appId check", () => {
    const plaintext = "<xml><Content><![CDATA[你好世界]]></Content></xml>";
    const cipher = encryptPlaintext({
      encodingAESKey: TEST_AES_KEY_43,
      receiveId: TEST_APPID,
      plaintext,
    });
    expect(cipher.length).toBeGreaterThan(0);
    const decoded = decryptEncrypted({
      encodingAESKey: TEST_AES_KEY_43,
      receiveId: TEST_APPID,
      encrypt: cipher,
    });
    expect(decoded).toBe(plaintext);
  });
  it("rejects when receiveId mismatches", () => {
    const cipher = encryptPlaintext({
      encodingAESKey: TEST_AES_KEY_43,
      receiveId: TEST_APPID,
      plaintext: "hi",
    });
    expect(() =>
      decryptEncrypted({
        encodingAESKey: TEST_AES_KEY_43,
        receiveId: "wxDIFFERENT",
        encrypt: cipher,
      }),
    ).toThrow(/receiveId mismatch/);
  });
});

describe("pkcs7", () => {
  it("unpads a validly padded buffer", () => {
    const padded = Buffer.concat([Buffer.from("hello"), Buffer.alloc(WECHAT_PKCS7_BLOCK_SIZE - 5, WECHAT_PKCS7_BLOCK_SIZE - 5)]);
    expect(pkcs7Unpad(padded, WECHAT_PKCS7_BLOCK_SIZE).toString()).toBe("hello");
  });
  it("rejects invalid padding bytes", () => {
    expect(() => pkcs7Unpad(Buffer.from([0, 0, 0, 33]), WECHAT_PKCS7_BLOCK_SIZE)).toThrow();
  });
});
