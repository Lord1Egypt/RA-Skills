import fs from 'fs';
import path from 'path';
import { baseError } from '../errors.js';

function inferMimeType(filename = '') {
  const lower = String(filename).toLowerCase();
  if (lower.endsWith('.png')) return 'image/png';
  if (lower.endsWith('.jpg') || lower.endsWith('.jpeg')) return 'image/jpeg';
  if (lower.endsWith('.gif')) return 'image/gif';
  if (lower.endsWith('.webp')) return 'image/webp';
  if (lower.endsWith('.pdf')) return 'application/pdf';
  if (lower.endsWith('.txt')) return 'text/plain';
  if (lower.endsWith('.csv')) return 'text/csv';
  if (lower.endsWith('.xlsx')) return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
  if (lower.endsWith('.xls')) return 'application/vnd.ms-excel';
  if (lower.endsWith('.docx')) return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
  if (lower.endsWith('.doc')) return 'application/msword';
  return 'application/octet-stream';
}

function inferKind(filename = '', mimeType = '') {
  const lower = String(filename).toLowerCase();
  const mime = String(mimeType).toLowerCase();
  if (mime.startsWith('image/') || /\.(png|jpe?g|gif|webp|bmp|svg)$/.test(lower)) return 'media';
  return 'file';
}

function normalizeAttachmentObject(fileToken, meta = {}) {
  return {
    file_token: fileToken,
    name: meta.name,
    type: meta.type,
    size: meta.size,
    url: meta.url,
    tmp_url: meta.tmp_url,
  };
}

async function readableToBuffer(readable) {
  const chunks = [];
  for await (const chunk of readable) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks);
}

function isFeishuMediaDownloadUrl(raw = '') {
  return /\/open-apis\/drive\/v1\/medias\/[^/]+\/download(?:\?|$)/.test(String(raw));
}

function isFeishuMediaTmpUrlEndpoint(raw = '') {
  return /\/open-apis\/drive\/v1\/medias\/batch_get_tmp_download_url(?:\?|$)/.test(String(raw));
}

function extractFileTokenFromUrl(raw = '') {
  const text = String(raw || '');
  const mediaMatch = text.match(/\/open-apis\/drive\/v1\/medias\/([^/?#]+)\/download/);
  if (mediaMatch?.[1]) return mediaMatch[1];
  try {
    const u = new URL(text);
    const token = u.searchParams.get('file_tokens') || u.searchParams.get('file_token');
    if (token) return token.split(',')[0];
  } catch {}
  return undefined;
}

async function loadFeishuMediaSource(client, input = {}) {
  const source = input.source_attachment || {};
  const token = input.file_token || source.file_token || extractFileTokenFromUrl(input.url) || extractFileTokenFromUrl(source.url) || extractFileTokenFromUrl(source.tmp_url);
  if (!token) return null;

  const filename = input.filename || source.name || `${token}.bin`;
  const mimeType = input.mime_type || source.type || inferMimeType(filename);

  try {
    const download = await client.drive.v1.media.download({
      path: { file_token: token },
    });
    const buffer = await readableToBuffer(download.getReadableStream());
    return {
      buffer,
      filename,
      size: buffer.length,
      mimeType,
      source: { file_token: token, method: 'drive.v1.media.download' },
    };
  } catch (downloadError) {
    try {
      const tmpResp = await client.drive.v1.media.batchGetTmpDownloadUrl({
        params: { file_tokens: [token] },
      });
      const tmpUrl = tmpResp?.data?.tmp_download_urls?.find((item) => item.file_token === token)?.tmp_download_url;
      if (!tmpUrl) throw downloadError;
      const res = await fetch(tmpUrl);
      if (!res.ok) {
        throw baseError('ATTACHMENT_DOWNLOAD_FAILED', `Failed to download Feishu tmp URL: HTTP ${res.status}`, {
          file_token: token,
          status: res.status,
        });
      }
      const arrayBuffer = await res.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);
      return {
        buffer,
        filename,
        size: buffer.length,
        mimeType,
        source: { file_token: token, method: 'drive.v1.media.batchGetTmpDownloadUrl', tmp_url: tmpUrl },
      };
    } catch {
      throw baseError('ATTACHMENT_DOWNLOAD_FAILED', downloadError?.message || 'Failed to download Feishu media attachment', {
        file_token: token,
        url: input.url || source.url,
        tmp_url: source.tmp_url,
      });
    }
  }
}

export async function loadUploadSource(clientOrInput = {}, maybeInput = undefined) {
  const client = maybeInput === undefined ? null : clientOrInput;
  const input = maybeInput === undefined ? clientOrInput : maybeInput;

  if (input.file_path) {
    const filePath = path.resolve(input.file_path);
    const stat = await fs.promises.stat(filePath).catch(() => null);
    if (!stat?.isFile()) {
      throw baseError('FILE_NOT_FOUND', `Local file not found: ${filePath}`, { file_path: input.file_path });
    }
    const buffer = await fs.promises.readFile(filePath);
    return {
      buffer,
      filename: input.filename || path.basename(filePath),
      size: stat.size,
      mimeType: input.mime_type || inferMimeType(input.filename || filePath),
      source: { file_path: filePath },
    };
  }

  if (client && (input.file_token || input.source_attachment?.file_token || isFeishuMediaDownloadUrl(input.url) || isFeishuMediaTmpUrlEndpoint(input.url) || isFeishuMediaDownloadUrl(input.source_attachment?.url) || isFeishuMediaTmpUrlEndpoint(input.source_attachment?.tmp_url))) {
    const feishuLoaded = await loadFeishuMediaSource(client, input);
    if (feishuLoaded) return feishuLoaded;
  }

  if (input.url) {
    const res = await fetch(input.url);
    if (!res.ok) {
      throw baseError('ATTACHMENT_DOWNLOAD_FAILED', `Failed to download URL: HTTP ${res.status}`, {
        url: input.url,
        status: res.status,
      });
    }
    const arrayBuffer = await res.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    const urlName = (() => {
      try {
        const u = new URL(input.url);
        const base = path.basename(u.pathname);
        return base && base !== '/' ? base : 'attachment.bin';
      } catch {
        return 'attachment.bin';
      }
    })();
    const contentType = res.headers.get('content-type') || undefined;
    return {
      buffer,
      filename: input.filename || urlName,
      size: buffer.length,
      mimeType: input.mime_type || contentType || inferMimeType(input.filename || urlName),
      source: { url: input.url },
    };
  }

  throw baseError('INVALID_UPLOAD_SOURCE', 'Attachment upload requires file_path, url, or source attachment with file_token');
}

export async function uploadAttachmentAssetApi(client, input) {
  const loaded = await loadUploadSource(client, input);
  const filename = input.filename || loaded.filename || 'attachment.bin';
  const kind = input.upload_kind || inferKind(filename, loaded.mimeType);

  if (loaded.size > 20 * 1024 * 1024) {
    throw baseError('FILE_TOO_LARGE', 'Attachment upload currently supports files up to 20MB via upload_all', {
      size: loaded.size,
      limit: 20 * 1024 * 1024,
      filename,
    });
  }

  let uploadResponse;
  if (kind === 'media') {
    uploadResponse = await client.drive.v1.media.uploadAll({
      data: {
        file_name: filename,
        parent_type: 'bitable_image',
        parent_node: input.app_token,
        size: loaded.size,
        file: loaded.buffer,
      },
    }).catch((error) => {
      throw baseError('ATTACHMENT_UPLOAD_FAILED', error?.message || 'Failed to upload media attachment', {
        filename,
        size: loaded.size,
        source: loaded.source,
      });
    });
  } else {
    uploadResponse = await client.drive.v1.file.uploadAll({
      data: {
        file_name: filename,
        parent_type: 'bitable_file',
        parent_node: input.app_token,
        size: loaded.size,
        file: loaded.buffer,
      },
    }).catch((error) => {
      throw baseError('ATTACHMENT_UPLOAD_FAILED', error?.message || 'Failed to upload file attachment', {
        filename,
        size: loaded.size,
        source: loaded.source,
      });
    });
  }

  const fileToken = uploadResponse?.file_token;
  if (!fileToken) {
    throw baseError('ATTACHMENT_UPLOAD_FAILED', 'Upload succeeded without returning file_token', {
      filename,
      size: loaded.size,
      source: loaded.source,
      uploadResponse,
    });
  }

  return {
    upload_kind: kind,
    file_token: fileToken,
    attachment: normalizeAttachmentObject(fileToken, {
      name: filename,
      size: loaded.size,
      type: loaded.mimeType,
      url: input.url,
    }),
  };
}

export async function cloneAttachmentAssetApi(client, input) {
  const source = input.source_attachment || {};
  const loaded = await loadUploadSource(client, {
    url: input.url || source.url || source.tmp_url,
    file_token: input.file_token || source.file_token,
    file_path: input.file_path,
    filename: input.filename || source.name,
    mime_type: input.mime_type || source.type,
    source_attachment: source,
  });

  const result = await uploadAttachmentAssetApi(client, {
    ...input,
    filename: input.filename || loaded.filename,
    mime_type: input.mime_type || loaded.mimeType,
    file_path: undefined,
    url: undefined,
  });

  return {
    source_attachment: source,
    ...result,
  };
}

export function normalizeAttachmentsForWrite(input = {}) {
  const attachments = [];
  if (Array.isArray(input.attachments)) {
    for (const item of input.attachments) {
      if (!item) continue;
      if (typeof item === 'string') {
        attachments.push({ file_token: item });
        continue;
      }
      if (typeof item === 'object' && item.file_token) {
        attachments.push(normalizeAttachmentObject(item.file_token, item));
      }
    }
  }
  if (!attachments.length && input.attachment && typeof input.attachment === 'object' && input.attachment.file_token) {
    attachments.push(normalizeAttachmentObject(input.attachment.file_token, input.attachment));
  }
  if (!attachments.length) {
    throw baseError('INVALID_ATTACHMENT_WRITE', 'No attachment/file_token provided to normalize for record write');
  }
  return { attachments };
}
