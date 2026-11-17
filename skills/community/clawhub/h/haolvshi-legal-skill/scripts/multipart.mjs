import fs from 'node:fs/promises';
import path from 'node:path';
import { SkillError } from './errors.mjs';

const MIME_TYPES = {
  '.pdf': 'application/pdf',
  '.doc': 'application/msword',
  '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png'
};

export async function fileDescriptor(filePath) {
  const absolutePath = path.resolve(String(filePath));
  const stat = await fs.stat(absolutePath).catch(() => null);
  if (!stat?.isFile()) {
    throw new SkillError('FILE_NOT_FOUND', `没有找到文件：${absolutePath}`);
  }
  const extension = path.extname(absolutePath).toLowerCase();
  return {
    path: absolutePath,
    name: path.basename(absolutePath),
    extension,
    size: stat.size,
    mimeType: MIME_TYPES[extension] || 'application/octet-stream'
  };
}

export async function createFileFormData(fieldName, descriptor, extra = {}) {
  const bytes = await fs.readFile(descriptor.path);
  const form = new FormData();
  for (const [key, value] of Object.entries(extra)) {
    if (value !== undefined && value !== null) form.append(key, String(value));
  }
  form.append(fieldName, new Blob([bytes], { type: descriptor.mimeType }), descriptor.name);
  return form;
}

export function validateContractFiles(descriptors) {
  if (!descriptors.length) {
    throw new SkillError('CONTRACT_FILE_REQUIRED', '请提供需要审核的合同文件');
  }
  const maxBytes = 10 * 1024 * 1024;
  for (const file of descriptors) {
    if (file.size > maxBytes) {
      throw new SkillError('FILE_TOO_LARGE', `文件 ${file.name} 超过 10MB`);
    }
    if (!MIME_TYPES[file.extension]) {
      throw new SkillError('UNSUPPORTED_FILE_TYPE', `不支持文件格式：${file.extension || '未知'}`);
    }
  }

  const documents = descriptors.filter(file => ['.pdf', '.doc', '.docx'].includes(file.extension));
  const images = descriptors.filter(file => ['.jpg', '.jpeg', '.png'].includes(file.extension));
  if (documents.length && images.length) {
    throw new SkillError('MIXED_FILE_TYPES', '合同正文和合同图片请分开提交');
  }
  if (documents.length > 1) {
    throw new SkillError('TOO_MANY_DOCUMENTS', '合同正文每次只能提交一个文件');
  }
  if (images.length > 10) {
    throw new SkillError('TOO_MANY_IMAGES', '合同图片最多提交十张');
  }
  return { doc: documents.length > 0, files: descriptors };
}

export function validatePleadingImage(descriptor) {
  if (!['.jpg', '.jpeg', '.png'].includes(descriptor.extension)) {
    throw new SkillError('PLEADING_IMAGE_TYPE', '文书材料图片仅支持 JPG、JPEG、PNG');
  }
  if (descriptor.size > 10 * 1024 * 1024) {
    throw new SkillError('FILE_TOO_LARGE', `图片 ${descriptor.name} 超过 10MB`);
  }
}

