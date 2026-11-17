#!/usr/bin/env node
//
// 文件上传到云存储，获取公网可访问 URL
//
// ⚠️ 安全警告：
//   - 本脚本会将本地文件上传到远程云存储
//   - 请勿上传包含敏感内容的文件（如身份证、私人视频、受版权保护素材等）
//
// 用法：
//   node upload.mjs <文件绝对路径>
//   echo '{"error":"need_upload",...}' | node upload.mjs
//
// 依赖：
//   - mcporter（已配置 ClawAgent 服务）
//   - Node.js ≥ 20（内置 fetch + fs.createReadStream，无需 curl/file/ali-oss SDK）
//
// 输出：
//   IMPORT_READY
//   FILE_URL:<url>
//   FILE_SIZE:<size>
//

import { createReadStream, statSync, accessSync, readSync } from 'node:fs';
const R_OK = 4; // fs.constants.R_OK
import { resolve, basename } from 'node:path';
import { spawnSync } from 'node:child_process';

// ── 扩展名 → MIME 映射 ────────────────────────────────────────────────
const MIME_MAP = {
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png':  'image/png',
  '.gif':  'image/gif',
  '.webp': 'image/webp',
  '.bmp':  'image/bmp',
  '.svg':  'image/svg+xml',
  '.mp4':  'video/mp4',
  '.mov':  'video/quicktime',
  '.avi':  'video/x-msvideo',
  '.mkv':  'video/x-matroska',
  '.mp3':  'audio/mpeg',
  '.wav':  'audio/wav',
  '.pdf':  'application/pdf',
  '.zip':  'application/zip',
};

function getMimeType(filePath) {
  const ext = filePath.slice(filePath.lastIndexOf('.')).toLowerCase();
  return MIME_MAP[ext] ?? 'application/octet-stream';
}

function formatSize(bytes) {
  if (bytes >= 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB (${bytes} 字节)`;
  if (bytes >= 1024)       return `${(bytes / 1024).toFixed(1)} KB (${bytes} 字节)`;
  return `${bytes} 字节`;
}

// ── stdin 管道检测 ────────────────────────────────────────────────────
function readStdinSync() {
  if (process.stdin.isTTY) return '';
  const chunks = [];
  while (true) {
    const buf = Buffer.alloc(4096);
    try {
      const bytes = readSync(0, buf);
      if (bytes === 0) break;
      chunks.push(buf.subarray(0, bytes));
    } catch {
      break;
    }
  }
  return Buffer.concat(chunks).toString('utf-8');
}

// ── 主流程 ────────────────────────────────────────────────────────────
async function main() {
  const stdinData = readStdinSync().trim();

  let filePath;
  let toolName = null;

  if (stdinData) {
    let needUpload;
    try {
      needUpload = JSON.parse(stdinData);
    } catch {
      console.log('ERROR:invalid_input - 管道输入不是有效的 need_upload 响应');
      console.log('请检查输入格式或提供有效的本地文件路径');
      process.exit(1);
    }

    if (needUpload.error === 'need_upload') {
      filePath = needUpload.local_file_path || '';
      toolName = needUpload.tool_name || null;
    } else {
      console.log('ERROR:invalid_input - 管道输入不是有效的 need_upload 响应');
      console.log('请检查输入格式或提供有效的本地文件路径');
      process.exit(1);
    }
  } else {
    filePath = process.argv[2] || '';
  }

  if (!filePath) {
    console.log('ERROR:missing_argument - 缺少文件路径参数');
    console.log('用法: node upload.mjs <file_path>');
    console.log('  或: echo \'{"error":"need_upload",...}\' | node upload.mjs');
    process.exit(1);
  }

  // ── 参数校验 ────────────────────────────────────────────────────────
  if (filePath.startsWith('@')) {
    console.log(`ERROR:reference_not_supported - 检测到文件引用标记(${filePath})，不支持直接使用`);
    console.log('请提供文件的完整本地路径，例如：/Users/yourname/Downloads/image.jpg');
    process.exit(1);
  }

  if (!filePath.startsWith('/') && !/^[A-Za-z]:[/\\]/.test(filePath)) {
    console.log(`ERROR:relative_path - 请使用完整绝对路径，当前路径: ${filePath}`);
    console.log('示例：/Users/yourname/Downloads/image.jpg');
    process.exit(1);
  }

  const suspicious = /(xxx|yourname|yourusername|example|path\/to)/i;
  if (suspicious.test(filePath)) {
    console.log(`ERROR:suspicious_path - 检测到路径可能为AI编造或示例路径: ${filePath}`);
    console.log('请提供真实的本地文件完整路径');
    process.exit(1);
  }

  // 规范化路径
  filePath = resolve(filePath);

  // 文件存在性和权限
  let fileSize;
  try {
    accessSync(filePath, R_OK);
    fileSize = statSync(filePath).size;
  } catch (e) {
    if (e.code === 'ENOENT') {
      console.log(`ERROR:file_not_found - 文件不存在: ${filePath}`);
      console.log('请检查路径是否正确，或提供文件的实际存储位置');
      process.exit(1);
    }
    if (e.code === 'EACCES') {
      console.log(`ERROR:file_not_readable - 文件无读取权限: ${filePath}`);
      console.log('请检查文件权限或尝试使用 sudo');
      process.exit(1);
    }
    console.log(`ERROR:file_error - ${e.message}`);
    process.exit(1);
  }

  if (fileSize <= 0) {
    console.log(`ERROR:empty_file - 文件为空: ${filePath}`);
    console.log('请检查文件内容或提供有效的文件');
    process.exit(1);
  }

  const maxSize = 100 * 1024 * 1024;
  if (fileSize > maxSize) {
    console.log('ERROR:file_too_large - 文件过大，最大支持 100MB');
    console.log('请压缩文件或选择较小的文件');
    process.exit(1);
  }

  const fileName = basename(filePath);
  const mimeType = getMimeType(filePath);
  console.log(`文件: ${fileName}`);
  console.log(`文件大小: ${formatSize(fileSize)}`);

  // ── Step 1: 获取 OSS 预签名上传 URL ─────────────────────────────────
  console.log('正在获取签名...');

  let signatureData;
  try {
    const result = spawnSync('mcporter', [
      'call', 'ClawAgent', 'signature', '--args', '-',
    ], {
      input: JSON.stringify({ filename: fileName, content_type: mimeType }),
      encoding: 'utf-8',
    });

    // 检查 mcporter 进程退出码和启动错误
    if (result.error) throw result.error;
    if (result.status !== 0) {
      const stderr = (result.stderr || '').trim();
      throw new Error(`mcporter exited with code ${result.status}${stderr ? ': ' + stderr : ''}`);
    }

    const resp = JSON.parse(result.stdout.trim());

    // 检查 API 业务状态码（全局结构: code=0 成功）
    if (resp.code !== 0) {
      console.log(`ERROR:signature_api_error - 签名接口返回异常 (code=${resp.code})`);
      console.log(`服务端消息: ${resp.msg || '未知错误'}`);
      if (resp.code === 403) {
        console.log('提示: Token 鉴权失败，请重新授权（见 references/auth.md）');
      } else if (resp.code === 80000000) {
        console.log('提示: 算力不足，需购买算力');
      }
      process.exit(1);
    }

    signatureData = resp.data ?? {};
  } catch (e) {
    console.log('ERROR:signature_failed - 获取上传签名失败');
    if (e.message && !e.message.startsWith('mcporter')) {
      console.log(`原因: ${e.message}`);
    }
    console.log('请检查网络连接或稍后重试');
    process.exit(1);
  }

  const uploadUrl = signatureData.upload_url || '';
  const fileUrl = signatureData.file_url || '';
  const contentHeader = signatureData.headers?.['Content-Type'] || mimeType;

  if (!uploadUrl) {
    console.log('ERROR:no_upload_url - 未获取到上传链接');
    console.log('请检查服务配置或联系管理员');
    process.exit(1);
  }
  if (!fileUrl) {
    console.log('ERROR:no_file_url - 未获取到文件访问链接');
    console.log('请检查服务配置或联系管理员');
    process.exit(1);
  }

  console.log('✅ 获取上传签名成功');
  console.log('');

  // ── Step 2: 流式 PUT 到 OSS ────────────────────────────────────────
  console.log('正在上传文件到 OSS...');

  let uploadOk = false;
  try {
    const stream = createReadStream(filePath, { highWaterMark: 64 * 1024 });
    const response = await fetch(uploadUrl, {
      method: 'PUT',
      headers: { 'Content-Type': contentHeader },
      body: stream,
      // @ts-ignore — duplex 是标准 fetch 属性但类型声明可能缺失
      duplex: 'half',
    });
    uploadOk = response.ok;
  } catch {
    uploadOk = false;
  }

  if (!uploadOk) {
    console.log('ERROR:upload_failed - OSS 上传失败');
    console.log('请检查网络连接或稍后重试');
    process.exit(1);
  }

  console.log('✅ 文件上传成功');

  // ── 输出 ────────────────────────────────────────────────────────────
  console.log('IMPORT_READY');
  console.log(`FILE_URL:${fileUrl}`);
  console.log(`FILE_SIZE:${fileSize}`);
  if (toolName) console.log(`TOOL_NAME:${toolName}`);
  console.log('');
  console.log('📋 下一步说明：');
  if (toolName) {
    console.log(`文件上传成功，使用上述 FILE_URL 调用工具 ${toolName} 继续操作`);
  } else {
    console.log('文件上传成功，使用上述 FILE_URL 继续后续操作');
  }
}

main().catch((e) => {
  console.log(`ERROR:unexpected - ${e.message}`);
  process.exit(1);
});
