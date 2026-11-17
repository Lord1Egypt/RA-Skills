import fs from 'node:fs/promises';
import path from 'node:path';
import { SkillError } from './errors.mjs';
import { fileDescriptor } from './multipart.mjs';
import { materializeInteractionChoices, plainText } from './interaction-normalizer.mjs';
import { currentTaskEvidencePolicy } from './evidence-policy.mjs';

const DIRECT_TEXT_EXTENSIONS = new Set(['.txt', '.md', '.csv', '.json', '.html', '.htm', '.xml']);
const HOST_EXTRACT_EXTENSIONS = new Set([
  '.pdf', '.doc', '.docx', '.rtf', '.xls', '.xlsx', '.jpg', '.jpeg', '.png'
]);
const MAX_FILE_COUNT = 20;
const MAX_FILE_BYTES = 10 * 1024 * 1024;
const MAX_CHARS_PER_FILE = 120_000;
const MAX_TOTAL_CHARS = 300_000;

function uniquePaths(values = []) {
  return [...new Set(values.filter(Boolean).map(value => path.resolve(String(value))))];
}

function extractedTextMap(input = {}) {
  const source = input.extractedTexts || input.fileTexts || [];
  const entries = Array.isArray(source)
    ? source.map(item => [item?.filePath || item?.path || item?.name, item?.text || item?.content])
    : Object.entries(source || {});
  const result = new Map();
  for (const [key, value] of entries) {
    if (!key || typeof value !== 'string' || !value.trim()) continue;
    const raw = String(key);
    result.set(raw, value);
    result.set(path.basename(raw), value);
    result.set(path.resolve(raw), value);
  }
  return result;
}

function normalizedText(value, extension = '') {
  let text = String(value || '').replace(/\u0000/g, '').replace(/\r\n?/g, '\n').trim();
  if (['.html', '.htm', '.xml'].includes(extension)) text = plainText(text);
  return text;
}

function limitedText(value, remaining, warnings, name) {
  const limit = Math.max(0, Math.min(MAX_CHARS_PER_FILE, remaining));
  if (value.length <= limit) return value;
  warnings.push(`材料“${name}”内容较长，仅保留前 ${limit} 个字符用于案情识别。`);
  return value.slice(0, limit);
}

function materialSection(name, text) {
  return `【案件材料：${name}】\n${text}`;
}

export function publicCaseContext(context) {
  if (!context?.text) return null;
  return {
    scope: 'current_task_only',
    evidencePolicy: currentTaskEvidencePolicy(),
    text: context.text,
    files: (context.files || []).map(file => ({
      name: file.name,
      extension: file.extension,
      size: file.size,
      source: file.source,
      charCount: file.charCount || 0
    })),
    warnings: context.warnings || []
  };
}

export function attachCaseContext(interaction, context) {
  const visible = publicCaseContext(context);
  if (!interaction) return interaction;
  const rendered = materializeInteractionChoices(interaction, visible?.text || '');
  if (!visible) return rendered;
  return {
    ...rendered,
    caseContext: {
      ...visible,
      useBeforePresenting: true,
      displayToUser: false,
      instruction: '这是仅从当前任务中用户上传或粘贴的材料及当前任务原始问题提取的内容。只可用它回答当前字段；禁止读取或混入全局记忆、其他任务、其他线程、旧案例、示例、评测、交接文档、测试记录或日志。当前任务材料无法确定时向用户提问，不要复述材料全文。'
    }
  };
}

export function materialExtractionRequired({ capability, unresolvedFiles, sessionId = null }) {
  return {
    ok: true,
    capability,
    stage: 'needs_material_extraction',
    ...(sessionId ? { sessionId } : {}),
    prompt: '这些案件材料不能由本地脚本直接提取。请先使用当前宿主真实可用的文件阅读、PDF、文档或图像识别工具忠实提取内容，再把结果放入 extractedTexts 重试原命令；宿主没有相应能力时，才请用户提供可复制文字或转换后的文件。',
    data: {
      unresolvedFiles,
      expectedInput: {
        extractedTexts: [{ filePath: '/绝对路径/案件材料.pdf', text: '从材料中忠实提取的文字' }]
      }
    }
  };
}

export function queryWithCaseContext(query, context) {
  const base = String(query || '').trim();
  const material = String(context?.text || '').slice(0, 4_000).trim();
  return [base, material].filter(Boolean).join('\n');
}

export async function prepareCaseMaterials(input = {}, options = {}) {
  const deferredExtensions = new Set(options.deferredExtensions || []);
  const paths = uniquePaths([
    ...(Array.isArray(input.filePaths) ? input.filePaths : input.filePath ? [input.filePath] : []),
    ...(Array.isArray(input.imagePaths) ? input.imagePaths : input.imagePath ? [input.imagePath] : [])
  ]);
  if (paths.length > MAX_FILE_COUNT) {
    throw new SkillError('TOO_MANY_CASE_MATERIALS', `案件材料最多提交 ${MAX_FILE_COUNT} 个文件`);
  }

  const overrides = extractedTextMap(input);
  const descriptors = await Promise.all(paths.map(fileDescriptor));
  const warnings = [];
  const unresolvedFiles = [];
  const deferredFiles = [];
  const files = [];
  const sections = [];
  let remaining = MAX_TOTAL_CHARS;

  const combinedSource = input.materialText
    || (input.caseContext && typeof input.caseContext === 'object' ? input.caseContext.text : input.caseContext)
    || '';
  const combinedText = normalizedText(combinedSource);
  if (combinedText) {
    const text = limitedText(combinedText, remaining, warnings, '用户提供的材料文字');
    if (text) {
      sections.push(materialSection('用户提供的材料文字', text));
      remaining -= text.length;
    }
  }

  for (const descriptor of descriptors) {
    if (descriptor.size > MAX_FILE_BYTES) {
      throw new SkillError('FILE_TOO_LARGE', `案件材料 ${descriptor.name} 超过 10MB`);
    }
    if (!DIRECT_TEXT_EXTENSIONS.has(descriptor.extension) && !HOST_EXTRACT_EXTENSIONS.has(descriptor.extension)) {
      throw new SkillError('UNSUPPORTED_CASE_MATERIAL_TYPE', `不支持案件材料格式：${descriptor.extension || '未知'}`);
    }

    if (deferredExtensions.has(descriptor.extension)) deferredFiles.push(descriptor);
    const override = overrides.get(descriptor.path) || overrides.get(descriptor.name);
    let rawText = override || '';
    let source = override ? 'host_extracted' : '';
    if (!rawText && DIRECT_TEXT_EXTENSIONS.has(descriptor.extension)) {
      rawText = await fs.readFile(descriptor.path, 'utf8');
      source = 'local_text';
    }

    const text = limitedText(normalizedText(rawText, descriptor.extension), remaining, warnings, descriptor.name);
    if (text) {
      sections.push(materialSection(descriptor.name, text));
      remaining -= text.length;
    } else if (!deferredExtensions.has(descriptor.extension)) {
      unresolvedFiles.push({
        filePath: descriptor.path,
        name: descriptor.name,
        extension: descriptor.extension,
        size: descriptor.size,
        requiredToolKind: ['.jpg', '.jpeg', '.png'].includes(descriptor.extension)
          ? 'image_or_ocr'
          : 'document_or_pdf'
      });
    }

    files.push({
      name: descriptor.name,
      extension: descriptor.extension,
      size: descriptor.size,
      source: text ? source : deferredExtensions.has(descriptor.extension) ? 'backend_image' : 'pending_host_extraction',
      charCount: text.length
    });
  }

  return {
    text: sections.join('\n\n'),
    files,
    warnings,
    unresolvedFiles,
    deferredFiles
  };
}
