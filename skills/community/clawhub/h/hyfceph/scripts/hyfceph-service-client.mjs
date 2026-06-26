#!/usr/bin/env node

import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import { parseArgs } from 'node:util';
import { generateHyfcephPdfReport } from './hyfceph-report-pdf.mjs';
import { qrcode } from './vendor/qrcode.mjs';

const DEFAULT_PORTAL_BASE_URL = 'https://hyfceph.52ortho.com/';
const LAST_RESULT_STATE_PATH = path.join(os.homedir(), '.codex/state/hyfceph-last-result.json');
const AUTH_STATE_PATH = path.join(os.homedir(), '.codex/state/hyfceph-auth.json');

function ensureTrailingSlash(value) {
  return value.endsWith('/') ? value : `${value}/`;
}

function timestampSlug() {
  return new Date().toISOString().replace(/[:.]/g, '-');
}

function defaultBaseName(mode) {
  return `hyfceph-${mode}-${timestampSlug()}`;
}

function nowIso() {
  return new Date().toISOString();
}

function printHelp() {
  console.log(`Usage:
  node scripts/hyfceph-service-client.mjs --image /path/to/ceph.png [options]
  node scripts/hyfceph-service-client.mjs --image /path/to/base.png --compare-image /path/to/compare.png [options]
  node scripts/hyfceph-service-client.mjs --pdf-input /path/to/result.json [options]
  node scripts/hyfceph-service-client.mjs --latest-pdf [options]
  node scripts/hyfceph-service-client.mjs --auth-status
  node scripts/hyfceph-service-client.mjs --clear-saved-api-key

Required:
  --api-key <key>                HYFCeph API Key (optional after first successful save)

Options:
  --portal-base-url <url>        HYFCeph portal URL, default: ${DEFAULT_PORTAL_BASE_URL}
  --auth-status                  Show whether a saved HYFCeph API Key exists and is valid
  --clear-saved-api-key          Remove the locally saved HYFCeph API Key
  --image <file>                 Upload a local ceph image and measure it on the server
  --compare-image <file>         Upload a second ceph image and generate an overlap PNG
  --align-mode <SN|FH>           Overlap alignment mode, default: SN
  --patient-name <name>          Optional patient name for the local PDF report
  --output <file>                Output JSON path
  --annotated-png-output <file>  Output PNG path
  --annotated-svg-output <file>  Output SVG path
  --contour-png-output <file>    Output contour PNG path
  --contour-svg-output <file>    Output contour SVG path
  --no-report                    Do not request the server-side HTML report link
  --generate-pdf                 Generate a local PDF after the current measurement run
  --pdf-output <file>            Output PDF path
  --pdf-input <file>             Generate a PDF from an existing HYFCeph result JSON
  --latest-pdf                   Generate a PDF from the latest locally recorded HYFCeph result
  --no-pdf-upload                Do not upload generated PDF to the portal OSS bridge
`);
}

async function requestJson(url, {
  method = 'GET',
  headers = {},
  body,
} = {}) {
  const finalHeaders = { ...headers };
  let payload = body;
  if (body && typeof body !== 'string') {
    payload = JSON.stringify(body);
    finalHeaders['Content-Type'] ??= 'application/json';
  }

  const response = await fetch(url, {
    method,
    headers: finalHeaders,
    body: method === 'GET' || method === 'HEAD' ? undefined : payload,
  });

  const text = await response.text();
  let data = {};
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(`Expected JSON but got: ${text.slice(0, 500)}`);
  }

  if (!response.ok) {
    throw new Error(data?.error || `HTTP ${response.status} ${response.statusText}`);
  }

  return data;
}

async function writeText(filePath, content) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, content, 'utf8');
  return path.resolve(filePath);
}

async function writeJson(filePath, value) {
  return writeText(filePath, JSON.stringify(value, null, 2));
}

async function writeBase64(filePath, base64) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, Buffer.from(base64, 'base64'));
  return path.resolve(filePath);
}

async function writeBuffer(filePath, buffer) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, buffer);
  return path.resolve(filePath);
}

async function readLastResultState() {
  try {
    const raw = await fs.readFile(LAST_RESULT_STATE_PATH, 'utf8');
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}

async function writeLastResultState(state) {
  await writeJson(LAST_RESULT_STATE_PATH, state);
  return LAST_RESULT_STATE_PATH;
}

async function readAuthState() {
  try {
    const raw = await fs.readFile(AUTH_STATE_PATH, 'utf8');
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}

async function writeAuthState(state) {
  await writeJson(AUTH_STATE_PATH, state);
  return AUTH_STATE_PATH;
}

async function clearAuthState() {
  try {
    await fs.rm(AUTH_STATE_PATH, { force: true });
  } catch {
    // ignore
  }
}

function redactApiKey(value) {
  const apiKey = String(value || '').trim();
  if (!apiKey) return null;
  if (apiKey.length <= 12) return `${apiKey.slice(0, 4)}...`;
  return `${apiKey.slice(0, 8)}...${apiKey.slice(-6)}`;
}

async function generateQrPng(url, outputPath) {
  if (!url) return null;
  const qr = qrcode(0, 'M');
  qr.addData(url);
  qr.make();
  const svgText = qr.createSvgTag(10, 20, 'HYFCeph report QR', 'HYFCeph report QR');
  return writeText(outputPath, svgText);
}

async function requestPdfUploadTicket({
  portalBaseUrl,
  apiKey,
  pdfPath,
  patientName,
  reportType,
}) {
  const endpoint = new URL('api/pdf/upload-ticket', portalBaseUrl).toString();
  return requestJson(endpoint, {
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
    },
    body: {
      fileName: path.basename(pdfPath),
      mimeType: 'application/pdf',
      patientName: patientName || '',
      reportType: reportType || 'report',
    },
  });
}

async function uploadPdfToSignedUrl({ upload, pdfPath }) {
  const pdfBuffer = await fs.readFile(pdfPath);
  const response = await fetch(upload.uploadUrl, {
    method: 'PUT',
    headers: upload.uploadHeaders || {
      'Content-Type': 'application/pdf',
    },
    body: pdfBuffer,
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(`PDF 上传失败：HTTP ${response.status} ${response.statusText}${text ? `: ${text.slice(0, 500)}` : ''}`);
  }

  return {
    objectKey: upload.objectKey || null,
    bucket: upload.bucket || null,
    region: upload.region || null,
    accessMode: upload.accessMode || null,
    pdfShareUrl: upload.downloadUrl || upload.publicUrl || null,
    pdfPublicUrl: upload.publicUrl || null,
    pdfShareExpiresAt: upload.downloadExpiresAt || null,
    uploadExpiresAt: upload.uploadExpiresAt || null,
  };
}

async function tryUploadPdfToPortalOss({
  portalBaseUrl,
  explicitApiKey,
  patientName,
  pdfPath,
  reportType,
}) {
  let auth = null;
  try {
    auth = await resolveApiKey({
      explicitApiKey,
      portalBaseUrl,
    });
  } catch (error) {
    return {
      ok: false,
      skipped: true,
      reason: error instanceof Error ? error.message : String(error),
    };
  }

  try {
    const ticketPayload = await requestPdfUploadTicket({
      portalBaseUrl,
      apiKey: auth.apiKey,
      pdfPath,
      patientName,
      reportType,
    });
    const upload = ticketPayload?.upload;
    if (!upload?.uploadUrl) {
      throw new Error('PDF 上传票据返回不完整。');
    }
    const uploaded = await uploadPdfToSignedUrl({
      upload,
      pdfPath,
    });
    return {
      ok: true,
      authSource: auth.authSource,
      ...uploaded,
    };
  } catch (error) {
    return {
      ok: false,
      skipped: false,
      reason: error instanceof Error ? error.message : String(error),
    };
  }
}

async function validateApiKey(portalBaseUrl, apiKey) {
  const endpoint = new URL('api/validate-key', portalBaseUrl).toString();
  return requestJson(endpoint, {
    method: 'POST',
    body: { apiKey },
  });
}

async function resolveApiKey({ explicitApiKey, portalBaseUrl }) {
  const directApiKey = String(explicitApiKey || '').trim();
  if (directApiKey) {
    const validation = await validateApiKey(portalBaseUrl, directApiKey);
    await writeAuthState({
      apiKey: directApiKey,
      portalBaseUrl,
      owner: validation?.owner || null,
      expiresAt: validation?.expiresAt || null,
      validatedAt: nowIso(),
    });
    return {
      apiKey: directApiKey,
      authSource: 'provided',
      validation,
    };
  }

  const savedState = await readAuthState();
  const savedApiKey = String(savedState?.apiKey || '').trim();
  if (!savedApiKey) {
    throw new Error('Missing HYFCeph API Key. Provide --api-key or HYFCEPH_API_KEY.');
  }

  try {
    const validation = await validateApiKey(portalBaseUrl, savedApiKey);
    await writeAuthState({
      ...(savedState || {}),
      apiKey: savedApiKey,
      portalBaseUrl,
      owner: validation?.owner || savedState?.owner || null,
      expiresAt: validation?.expiresAt || null,
      validatedAt: nowIso(),
    });
    return {
      apiKey: savedApiKey,
      authSource: 'saved',
      validation,
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    if (/API Key 无效|API Key 已过期|缺少 API Key/i.test(message)) {
      await clearAuthState();
      throw new Error('已保存的 HYFCeph API Key 无效或已过期，请重新提供新的 API Key。');
    }
    throw error;
  }
}

function mimeTypeFromPath(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.png') return 'image/png';
  if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg';
  if (ext === '.webp') return 'image/webp';
  if (ext === '.bmp') return 'image/bmp';
  if (ext === '.tif' || ext === '.tiff') return 'image/tiff';
  return 'application/octet-stream';
}

async function main() {
  const { values, positionals } = parseArgs({
    options: {
      'api-key': { type: 'string' },
      'portal-base-url': { type: 'string', default: DEFAULT_PORTAL_BASE_URL },
      'auth-status': { type: 'boolean', default: false },
      'clear-saved-api-key': { type: 'boolean', default: false },
      image: { type: 'string' },
      'compare-image': { type: 'string' },
      'align-mode': { type: 'string', default: 'SN' },
      'patient-name': { type: 'string' },
      output: { type: 'string' },
      'annotated-png-output': { type: 'string' },
      'annotated-svg-output': { type: 'string' },
      'contour-png-output': { type: 'string' },
      'contour-svg-output': { type: 'string' },
      'no-report': { type: 'boolean', default: false },
      'generate-pdf': { type: 'boolean', default: false },
      'pdf-output': { type: 'string' },
      'pdf-input': { type: 'string' },
      'latest-pdf': { type: 'boolean', default: false },
      'no-pdf-upload': { type: 'boolean', default: false },
      'share-url': { type: 'string' },
      'current-case': { type: 'boolean', default: false },
      help: { type: 'boolean', short: 'h', default: false },
    },
  });

  if (values.help) {
    printHelp();
    return;
  }

  const pdfInput = String(values['pdf-input'] || '').trim();
  const latestPdf = values['latest-pdf'];
  const pdfOutput = String(values['pdf-output'] || '').trim();
  const patientName = String(values['patient-name'] || '').trim();
  const disablePdfUpload = values['no-pdf-upload'];
  const requestedPortalBaseUrl = String(values['portal-base-url'] || '').trim();
  let portalBaseUrl = ensureTrailingSlash(String(requestedPortalBaseUrl || process.env.HYFCEPH_PORTAL_BASE_URL || DEFAULT_PORTAL_BASE_URL).trim());

  if (values['clear-saved-api-key']) {
    await clearAuthState();
    console.log(JSON.stringify({
      ok: true,
      cleared: true,
      authStatePath: AUTH_STATE_PATH,
    }, null, 2));
    return;
  }

  if (values['auth-status']) {
    const savedState = await readAuthState();
    const savedApiKey = String(savedState?.apiKey || '').trim();
    if (!savedApiKey) {
      console.log(JSON.stringify({
        configured: false,
        portalBaseUrl,
        authStatePath: AUTH_STATE_PATH,
      }, null, 2));
      return;
    }

    try {
      const validation = await validateApiKey(portalBaseUrl, savedApiKey);
      const output = {
        configured: true,
        valid: true,
        authSource: 'saved',
        apiKeyHint: redactApiKey(savedApiKey),
        portalBaseUrl,
        authStatePath: AUTH_STATE_PATH,
        owner: validation?.owner || savedState?.owner || null,
        expiresAt: validation?.expiresAt || savedState?.expiresAt || null,
      };
      await writeAuthState({
        ...(savedState || {}),
        apiKey: savedApiKey,
        portalBaseUrl,
        owner: output.owner,
        expiresAt: output.expiresAt,
        validatedAt: nowIso(),
      });
      console.log(JSON.stringify(output, null, 2));
      return;
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      if (/API Key 无效|API Key 已过期|缺少 API Key/i.test(message)) {
        await clearAuthState();
        console.log(JSON.stringify({
          configured: false,
          valid: false,
          portalBaseUrl,
          authStatePath: AUTH_STATE_PATH,
          reason: 'saved-api-key-invalid',
        }, null, 2));
        return;
      }
      throw error;
    }
  }

  if (pdfInput || latestPdf) {
    const state = await readLastResultState();
    if (!requestedPortalBaseUrl && state?.portalBaseUrl) {
      portalBaseUrl = ensureTrailingSlash(String(state.portalBaseUrl).trim());
    }
    const inputPath = pdfInput
      ? path.resolve(pdfInput)
      : await (async () => {
          const latestResultPath = String(state?.resultJsonPath || '').trim();
          if (!latestResultPath) {
            throw new Error('当前没有可用的最近一次测量结果，无法生成 PDF。请先完成一次测量。');
          }
          return path.resolve(latestResultPath);
        })();

    const pdfPath = await generateHyfcephPdfReport({
      inputPath,
      outputPath: pdfOutput || undefined,
      patientName: patientName || String(state?.patientName || '').trim() || undefined,
    });
    const finalPatientName = patientName || String(state?.patientName || '').trim() || null;
    const reportType = String(state?.mode || 'report').trim() || 'report';
    const pdfUpload = disablePdfUpload
      ? {
          ok: false,
          skipped: true,
          reason: 'pdf-upload-disabled',
        }
      : await tryUploadPdfToPortalOss({
          portalBaseUrl,
          explicitApiKey: String(values['api-key'] || process.env.HYFCEPH_API_KEY || '').trim(),
          patientName: finalPatientName,
          pdfPath,
          reportType,
        });

    await writeLastResultState({
      ...(state || {}),
      resultJsonPath: inputPath,
      portalBaseUrl,
      pdfReportPath: pdfPath,
      pdfUpload,
      patientName: finalPatientName,
      updatedAt: new Date().toISOString(),
    });

    console.log(JSON.stringify({
      inputPath,
      pdfPath,
      pdfUpload,
      patientName: finalPatientName,
    }, null, 2));
    return;
  }

  const imagePath = String(values.image || positionals[0] || '').trim();
  const compareImagePath = String(values['compare-image'] || '').trim();
  const shareUrl = String(values['share-url'] || '').trim();
  const currentCase = values['current-case'] || (!shareUrl && !imagePath);
  const overlapMode = Boolean(imagePath && compareImagePath);
  const shouldGeneratePdf = Boolean(values['generate-pdf']);
  const shouldRequestReport = !values['no-report'];
  const alignMode = String(values['align-mode'] || 'SN').trim().toUpperCase() || 'SN';
  const auth = await resolveApiKey({
    explicitApiKey: String(values['api-key'] || process.env.HYFCEPH_API_KEY || '').trim(),
    portalBaseUrl,
  });
  const apiKey = auth.apiKey;
  const mode = overlapMode ? 'overlap' : (imagePath ? 'image' : (shareUrl ? 'share-url' : 'current-case'));
  const baseName = defaultBaseName(mode);
  const outputPath = path.resolve(values.output || path.join(process.cwd(), `${baseName}.json`));
  const annotatedPngPath = path.resolve(values['annotated-png-output'] || path.join(process.cwd(), `${baseName}.png`));
  const annotatedSvgPath = path.resolve(values['annotated-svg-output'] || path.join(process.cwd(), `${baseName}.svg`));
  const contourPngPath = path.resolve(values['contour-png-output'] || path.join(process.cwd(), `${baseName}.contour.png`));
  const contourSvgPath = path.resolve(values['contour-svg-output'] || path.join(process.cwd(), `${baseName}.contour.svg`));

  const endpoint = new URL(
    overlapMode
      ? 'api/measure/overlap'
      : imagePath
      ? 'api/measure/image'
      : (shareUrl ? 'api/measure/share-url' : 'api/measure/current-case'),
    portalBaseUrl,
  ).toString();

  let payload;
  try {
    const requestBody = overlapMode
      ? await (async () => {
          const resolvedBaseImagePath = path.resolve(imagePath);
          const resolvedCompareImagePath = path.resolve(compareImagePath);
          const [baseImageBuffer, compareImageBuffer] = await Promise.all([
            fs.readFile(resolvedBaseImagePath),
            fs.readFile(resolvedCompareImagePath),
          ]);
          return {
            baseFileName: path.basename(resolvedBaseImagePath),
            baseMimeType: mimeTypeFromPath(resolvedBaseImagePath),
            baseImageBase64: baseImageBuffer.toString('base64'),
            compareFileName: path.basename(resolvedCompareImagePath),
            compareMimeType: mimeTypeFromPath(resolvedCompareImagePath),
            compareImageBase64: compareImageBuffer.toString('base64'),
            alignMode,
            generateReport: shouldRequestReport,
            patientName: patientName || '',
          };
        })()
      : imagePath
        ? await (async () => {
          const resolvedImagePath = path.resolve(imagePath);
          const imageBuffer = await fs.readFile(resolvedImagePath);
          return {
            fileName: path.basename(resolvedImagePath),
            mimeType: mimeTypeFromPath(resolvedImagePath),
            imageBase64: imageBuffer.toString('base64'),
            patientName: patientName || '',
            generateReport: shouldRequestReport,
          };
        })()
        : (shareUrl ? { shareUrl } : {});
    payload = await requestJson(endpoint, {
      method: 'POST',
      headers: {
        'x-api-key': apiKey,
      },
      body: requestBody,
    });
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    if (/服务端远程会话暂不可用/.test(reason)) {
      throw new Error('服务端远程会话暂不可用，请稍后再试。');
    }
    if (!imagePath && !shareUrl && /当前病例|同步|桥接/.test(reason)) {
      throw new Error('服务端当前没有可用病例。请改为直接发送侧位片。');
    }
    throw error;
  }

  const result = payload.result || {};
  const artifacts = result.artifacts || {};
  let resolvedPngPath = null;
  let resolvedSvgPath = null;
  let resolvedContourPngPath = null;
  let resolvedContourSvgPath = null;
  let resolvedReportQrPngPath = null;
  let resolvedPrettyReportQrPngPath = null;

  if (artifacts.annotatedPngBase64) {
    resolvedPngPath = await writeBase64(annotatedPngPath, artifacts.annotatedPngBase64);
  }
  if (artifacts.annotatedSvgBase64) {
    resolvedSvgPath = await writeText(
      annotatedSvgPath,
      Buffer.from(artifacts.annotatedSvgBase64, 'base64').toString('utf8'),
    );
  }
  if (artifacts.contourPngBase64) {
    resolvedContourPngPath = await writeBase64(contourPngPath, artifacts.contourPngBase64);
  }
  if (artifacts.contourSvgBase64) {
    resolvedContourSvgPath = await writeText(
      contourSvgPath,
      Buffer.from(artifacts.contourSvgBase64, 'base64').toString('utf8'),
    );
  }

  const output = {
    ok: payload.ok !== false,
    mode: payload.mode || mode,
    authSource: auth.authSource,
    portalBaseUrl,
    patientName: patientName || null,
    alignMode: result.summary?.alignMode || (overlapMode ? alignMode : null),
    analysis: result.analysis || null,
    analysisError: result.analysisError || null,
    annotationError: result.annotationError || null,
    contourError: result.contourError || null,
    summary: result.summary || null,
    frameworkChoices: result.analysis?.frameworkChoices || result.summary?.frameworkChoices || [],
    metrics: result.metrics || [],
    taskId: result.taskId || null,
    resultUrl: result.resultUrl || null,
    pdfShareUrl: null,
    pdfUpload: null,
    reportShareUrl: result.report?.ok ? result.report.reportShareUrl || null : null,
    reportUpload: result.report || null,
    prettyReportShareUrl: result.prettyReport?.ok ? result.prettyReport.reportShareUrl || null : null,
    prettyReportUpload: result.prettyReport || null,
    feishuDocShareUrl: result.feishuDoc?.ok ? result.feishuDoc.docUrl || null : null,
    feishuDocUpload: result.feishuDoc || null,
    reportQrPngPath: null,
    prettyReportQrPngPath: null,
    feishuDocQrPngPath: null,
    annotatedPngPath: resolvedPngPath,
    annotatedSvgPath: resolvedSvgPath,
    contourPngPath: resolvedContourPngPath,
    contourSvgPath: resolvedContourSvgPath,
  };

  if (output.reportShareUrl) {
    try {
      resolvedReportQrPngPath = await generateQrPng(
        output.reportShareUrl,
        path.join(outputDir, `${baseName}.report-qr.svg`),
      );
      output.reportQrPngPath = resolvedReportQrPngPath;
    } catch {
      output.reportQrPngPath = null;
    }
  }

  if (output.prettyReportShareUrl) {
    try {
      resolvedPrettyReportQrPngPath = await generateQrPng(
        output.prettyReportShareUrl,
        path.join(outputDir, `${baseName}.report-pretty-qr.svg`),
      );
      output.prettyReportQrPngPath = resolvedPrettyReportQrPngPath;
    } catch {
      output.prettyReportQrPngPath = null;
    }
  }

  if (output.feishuDocShareUrl) {
    try {
      output.feishuDocQrPngPath = await generateQrPng(
        output.feishuDocShareUrl,
        path.join(outputDir, `${baseName}.feishu-doc-qr.svg`),
      );
    } catch {
      output.feishuDocQrPngPath = null;
    }
  }

  await writeJson(outputPath, output);

  let pdfReportPath = null;
  let pdfUpload = null;
  if (shouldGeneratePdf) {
    pdfReportPath = await generateHyfcephPdfReport({
      inputPath: outputPath,
      outputPath: pdfOutput || undefined,
      patientName: patientName || undefined,
    });
    output.pdfReportPath = pdfReportPath;
    pdfUpload = disablePdfUpload
      ? {
          ok: false,
          skipped: true,
          reason: 'pdf-upload-disabled',
        }
      : await tryUploadPdfToPortalOss({
          portalBaseUrl,
          explicitApiKey: String(values['api-key'] || process.env.HYFCEPH_API_KEY || '').trim(),
          patientName: patientName || null,
          pdfPath: pdfReportPath,
          reportType: output.mode,
        });
    output.pdfUpload = pdfUpload;
    output.pdfShareUrl = pdfUpload?.ok ? pdfUpload.pdfShareUrl || null : null;
    await writeJson(outputPath, output);
  }

  await writeLastResultState({
    resultJsonPath: outputPath,
    portalBaseUrl,
    annotatedPngPath: resolvedPngPath,
    annotatedSvgPath: resolvedSvgPath,
    contourPngPath: resolvedContourPngPath,
    contourSvgPath: resolvedContourSvgPath,
    reportUpload: output.reportUpload || null,
    reportShareUrl: output.reportShareUrl || null,
    reportQrPngPath: output.reportQrPngPath || null,
    prettyReportUpload: output.prettyReportUpload || null,
    prettyReportShareUrl: output.prettyReportShareUrl || null,
    prettyReportQrPngPath: output.prettyReportQrPngPath || null,
    feishuDocUpload: output.feishuDocUpload || null,
    feishuDocShareUrl: output.feishuDocShareUrl || null,
    feishuDocQrPngPath: output.feishuDocQrPngPath || null,
    pdfReportPath,
    pdfUpload,
    pdfShareUrl: output.pdfShareUrl || null,
    patientName: patientName || null,
    mode: output.mode,
    updatedAt: new Date().toISOString(),
  });

  console.log(JSON.stringify({
    outputPath,
    annotatedPngPath: resolvedPngPath,
    annotatedSvgPath: resolvedSvgPath,
    contourPngPath: resolvedContourPngPath,
    contourSvgPath: resolvedContourSvgPath,
    reportUpload: output.reportUpload || null,
    reportShareUrl: output.reportShareUrl || null,
    reportQrPngPath: output.reportQrPngPath || null,
    prettyReportUpload: output.prettyReportUpload || null,
    prettyReportShareUrl: output.prettyReportShareUrl || null,
    prettyReportQrPngPath: output.prettyReportQrPngPath || null,
    feishuDocUpload: output.feishuDocUpload || null,
    feishuDocShareUrl: output.feishuDocShareUrl || null,
    feishuDocQrPngPath: output.feishuDocQrPngPath || null,
    pdfReportPath,
    pdfUpload,
    pdfShareUrl: output.pdfShareUrl || null,
    patientName: output.patientName,
    summary: output.summary,
    frameworkChoices: output.frameworkChoices,
    metrics: output.metrics,
    analysisError: output.analysisError,
    annotationError: output.annotationError,
    contourError: output.contourError,
  }, null, 2));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
