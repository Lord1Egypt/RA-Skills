/**
 * 文件处理模块
 * 支持文档解析（docx, pdf, txt 等）和文件上传
 */

import * as fs from 'fs';
import type { DingtalkConfig } from '../../types/index.ts';
import { FILE_MARKER_PATTERN, toLocalPath, uploadMediaToDingTalk, TEXT_FILE_EXTENSIONS } from './common.ts';

/**
 * 解析文档文件，提取文本内容
 */
export async function parseDocumentFile(filePath: string, log?: any): Promise<string | null> {
  try {
    const ext = '.' + filePath.split('.').pop()?.toLowerCase();
    
    if (!TEXT_FILE_EXTENSIONS.has(ext)) {
      log?.warn?.(`[DingTalk][File] 不支持的文件类型：${ext}`);
      return null;
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    log?.info?.(`[DingTalk][File] 解析文件成功：${filePath}, 长度=${content.length}`);
    return content;
  } catch (err: any) {
    log?.error?.(`[DingTalk][File] 解析文件失败：${err.message}`);
    return null;
  }
}

/**
 * 提取文件标记并发送文件消息
 */
export async function processFileMarkers(
  content: string,
  sessionWebhook: string,
  config: DingtalkConfig,
  oapiToken: string | null,
  log?: any,
  useProactiveApi: boolean = false,
  target?: any,
): Promise<string> {
  const logPrefix = useProactiveApi ? '[DingTalk][File][Proactive]' : '[DingTalk][File]';

  if (!oapiToken) {
    log?.warn?.(`${logPrefix} 无 oapiToken，跳过文件处理`);
    return content;
  }

  const matches = [...content.matchAll(FILE_MARKER_PATTERN)];
  if (matches.length === 0) return content;

  log?.info?.(`${logPrefix} 检测到 ${matches.length} 个文件，开始上传...`);

  let result = content;
  for (const match of matches) {
    const full = match[0];
    try {
      const fileData = JSON.parse(match[1]);
      const absPath = toLocalPath(fileData.path);
      const uploadResult = await uploadMediaToDingTalk(absPath, 'file', oapiToken, 20 * 1024 * 1024, log);
      result = result.replace(full, uploadResult ? `[文件已上传：${uploadResult}]` : '⚠️ 文件上传失败');
    } catch {
      log?.warn?.(`${logPrefix} 解析文件标记失败：${match[1]}`);
      result = result.replace(full, '');
    }
  }

  return result;
}
