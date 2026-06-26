#!/usr/bin/env node

/**
 * Fetches an authorization code and secret from the current breo backend integration,
 * then generates a QR code image for the user to scan.
 *
 * 1. Calls GET /api/auth/code/ge to obtain { code, secret }
 * 2. Builds the scan URL with { code, secret } query parameters
 * 3. Saves a QR code PNG to local workspace path
 *
 * Usage: node generate-qrcode.js
 * Output: JSON to stdout  { qrPath, code, expiresAt }
 */

import QRCode from "qrcode";
import { writeFileSync, mkdirSync } from "fs";
import { join } from "path";
import {
  getAuthApiUrl,
  getWorkspaceDir,
  BREO_QR_BASE_URL,
  CODE_EXPIRY_MS,
  jsonOutput,
  errorExit,
} from "./utils.js";

const QR_IMAGE_SIZE = 400;

/**
 * Resolve writable workspace directory for generated PNG.
 */
const WORKSPACE_DIR = getWorkspaceDir();

async function fetchAuthCode(baseUrl) {
  const resp = await fetch(`${baseUrl}/api/auth/code/ge`, {
    signal: AbortSignal.timeout(10000),
  });

  if (!resp.ok) {
    const body = await resp.text().catch(() => "");
    throw Object.assign(
      new Error(`授权服务返回错误 (HTTP ${resp.status}): ${body || "未知错误"}`),
      { httpStatus: resp.status }
    );
  }

  const json = await resp.json();
  const { code, secret } = json.data || {};
  if (!code || !secret) {
    throw new Error("后端返回数据不完整：缺少 code 或 secret");
  }
  return { code, secret };
}

function buildAuthUrl(code, secret) {
  const params = new URLSearchParams({ code, secret });
  return `${BREO_QR_BASE_URL}?${params.toString()}`;
}

async function generateQRFile(authUrl, code) {
  const qrDataUrl = await QRCode.toDataURL(authUrl, {
    type: "image/png",
    width: QR_IMAGE_SIZE,
    margin: 2,
    color: { dark: "#000000", light: "#FFFFFF" },
  });

  const base64Data = qrDataUrl.replace(/^data:image\/png;base64,/, "");
  const buffer = Buffer.from(base64Data, "base64");
  const filename = `breo-qr-${code.slice(0, 8)}.png`;

  mkdirSync(WORKSPACE_DIR, { recursive: true });
  const qrPath = join(WORKSPACE_DIR, filename);
  writeFileSync(qrPath, buffer);
  return { qrPath };
}

async function main() {
  try {
    const baseUrl = getAuthApiUrl();
    const { code, secret } = await fetchAuthCode(baseUrl);
    const authUrl = buildAuthUrl(code, secret);
    const expiresAt = new Date(Date.now() + CODE_EXPIRY_MS).toISOString();

    const { qrPath } = await generateQRFile(authUrl, code);

    jsonOutput({ qrPath, code, expiresAt });
  } catch (err) {
    if (err.cause?.code === "ECONNREFUSED" || err.cause?.code === "ENOTFOUND") {
      errorExit("无法连接到倍轻松授权服务，请检查网络连接。");
    }
    errorExit(err.message);
  }
}

main();
