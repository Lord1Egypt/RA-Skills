import type { LanguageOption, TaskStatus, SrtSegment } from '../types';

/**
 * Whisper 支持的语言列表。
 */
export const LANGUAGES: LanguageOption[] = [
  { code: 'auto', label: '自动检测' },
  { code: 'ja', label: '日语' },
  { code: 'zh', label: '中文' },
  { code: 'en', label: '英语' },
  { code: 'ko', label: '韩语' },
  { code: 'fr', label: '法语' },
  { code: 'de', label: '德语' },
  { code: 'es', label: '西班牙语' },
  { code: 'ru', label: '俄语' },
  { code: 'pt', label: '葡萄牙语' },
  { code: 'it', label: '意大利语' },
  { code: 'ar', label: '阿拉伯语' },
  { code: 'hi', label: '印地语' },
  { code: 'th', label: '泰语' },
  { code: 'vi', label: '越南语' },
  { code: 'nl', label: '荷兰语' },
  { code: 'pl', label: '波兰语' },
  { code: 'sv', label: '瑞典语' },
  { code: 'tr', label: '土耳其语' },
];

/**
 * 获取语言代码对应的友好名称。
 */
export function getLanguageLabel(code: string): string {
  const lang = LANGUAGES.find((l) => l.code === code);
  return lang ? lang.label : code.toUpperCase();
}

/**
 * 支持的音频扩展名列表。
 */
export function getAudioExtensions(): string[] {
  return ['.m4a', '.wav', '.mp3', '.flac', '.ogg', '.aac', '.wma'];
}

/**
 * react-dropzone 使用的 accept 配置。
 */
export const AUDIO_ACCEPT: Record<string, string[]> = {
  'audio/*': ['.m4a', '.wav', '.mp3', '.flac', '.ogg', '.aac', '.wma'],
};

/**
 * 从文件名中提取扩展名。
 */
export function extractExtension(fileName: string): string | null {
  const ext = fileName.split('.').pop()?.toLowerCase();
  if (ext && getAudioExtensions().includes(`.${ext}`)) {
    return ext;
  }
  return null;
}

/**
 * 格式化文件大小为人类可读字符串。
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  const k = 1024;
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  const size = bytes / Math.pow(k, i);
  return `${size.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
}

/**
 * 格式化音频时长。
 */
export function formatDuration(seconds: number): string {
  if (!seconds || seconds <= 0) return '--';
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);

  const parts: string[] = [];
  if (h > 0) parts.push(`${h}h`);
  if (m > 0 || h > 0) parts.push(`${m}m`);
  parts.push(`${s}s`);
  return parts.join(' ');
}

/**
 * 格式化短时长（用于预估剩余时间）。
 */
export function formatEstimatedTime(seconds: number): string {
  if (!seconds || seconds <= 0) return '--';
  const h = Math.floor(seconds / 3600);
  const m = Math.ceil((seconds % 3600) / 60);

  if (h > 0) return `约 ${h} 小时 ${m} 分`;
  return `约 ${m} 分钟`;
}

/**
 * 预估转录时间。
 */
export function estimateTime(
  chunkSec: number,
  totalChunks: number,
  overlapSec: number,
): number {
  if (totalChunks <= 0) return 0;
  const effectiveChunkDuration = chunkSec - overlapSec;
  const processingTimePerChunk = chunkSec * 0.15;
  return totalChunks * Math.max(processingTimePerChunk, effectiveChunkDuration * 0.1);
}

/**
 * 根据音频时长和分段参数计算总 chunk 数。
 */
export function calculateTotalChunks(
  duration: number,
  chunkSec: number,
  overlapSec: number,
): number {
  if (duration <= 0 || chunkSec <= 0) return 1;
  const effectiveChunk = chunkSec - overlapSec;
  return Math.ceil(duration / Math.max(effectiveChunk, 1));
}

/**
 * 生成唯一 ID。
 */
export function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}

/**
 * 获取状态对应的颜色。
 */
export function getStatusColor(status: TaskStatus): string {
  const colorMap: Record<TaskStatus, string> = {
    queued: '#9EA3B8',
    loading: '#2196F3',
    transcribing: '#FF9800',
    completed: '#4CAF50',
    failed: '#F44336',
    cancelled: '#5A6180',
  };
  return colorMap[status];
}

/**
 * 获取状态对应的中文标签。
 */
export function getStatusLabel(status: TaskStatus): string {
  const labelMap: Record<TaskStatus, string> = {
    queued: '等待中',
    loading: '转录中',
    transcribing: '转录中',
    completed: '已完成',
    failed: '失败',
    cancelled: '已取消',
  };
  return labelMap[status];
}

/**
 * 从模型路径中提取短名称。
 */
export function getShortModelName(modelPath: string): string {
  const parts = modelPath.split('/');
  return parts[parts.length - 1] || modelPath;
}

// ─── API 客户端 ──────────────────────────────────────

/**
 * 调用后端启动转录任务。
 */
export async function apiStartTranscription(
  apiBaseUrl: string,
  filePath: string,
  model?: string,
  language: string = 'auto',
  chunkSec: number = 150,
  overlapSec: number = 20,
): Promise<{ task_id: string }> {
  const body: Record<string, unknown> = {
    file_path: filePath,
    language,
    chunk_sec: chunkSec,
    overlap_sec: overlapSec,
  };
  if (model) body.model = model;
  const res = await fetch(`${apiBaseUrl}/api/transcribe`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

/**
 * 查询后端任务状态。
 */
export async function apiGetTaskStatus(
  apiBaseUrl: string,
  taskId: string,
): Promise<{
  id: string;
  file_name: string;
  model: string;
  language: string;
  chunk_sec: number;
  overlap_sec: number;
  status: string;
  progress: number;
  current_chunk: number;
  total_chunks: number;
  skipped_chunks: number;
  skipped_chunk_indexes: number[];
  segments: SrtSegment[];
  duration: number;
  error: string | null;
  completed_at: number | null;
}> {
  const res = await fetch(`${apiBaseUrl}/api/tasks/${taskId}`);
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return res.json();
}

/**
 * 取消后端任务。
 */
export async function apiCancelTask(
  apiBaseUrl: string,
  taskId: string,
): Promise<void> {
  await fetch(`${apiBaseUrl}/api/tasks/${taskId}/cancel`, { method: 'POST' });
}

/**
 * 调用后端翻译接口。
 */
export async function apiTranslate(
  apiBaseUrl: string,
  segments: SrtSegment[],
  sourceLanguage: string,
  targetLanguage: string = 'zh',
  translateModel?: string,
): Promise<SrtSegment[]> {
  const body: Record<string, unknown> = {
    segments,
    source_language: sourceLanguage,
    target_language: targetLanguage,
  };
  if (translateModel) body.model = translateModel;
  const res = await fetch(`${apiBaseUrl}/api/translate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  const data = await res.json();
  return data.translated_segments;
}

/**
 * 上传文件到后端。
 */
export async function apiUploadFile(
  apiBaseUrl: string,
  file: File,
): Promise<{ file_path: string; file_name: string; file_size: number }> {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${apiBaseUrl}/api/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    throw new Error(`Upload failed: HTTP ${res.status}`);
  }
  return res.json();
}

/**
 * 检查后端健康状态。
 */
export async function apiHealthCheck(
  apiBaseUrl: string,
): Promise<{ status: string; whisper_model: string; translate_model_loaded: boolean; translate_model: string | null }> {
  const res = await fetch(`${apiBaseUrl}/api/health`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * 获取可用翻译模型列表。
 */
export async function apiGetModels(
  apiBaseUrl: string,
): Promise<{ models: Array<{ id: string; name: string; size: string }> }> {
  const res = await fetch(`${apiBaseUrl}/api/models`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ─── SRT 导出 ──────────────────────────────────────

/**
 * 格式化秒数为 SRT 时间格式 HH:MM:SS,mmm。
 */
export function formatSrtTime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const ms = Math.round((seconds % 1) * 1000);
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms).padStart(3, '0')}`;
}

/**
 * 将段列表导出为 SRT 格式字符串。
 */
export function exportSegmentsToSrt(segments: SrtSegment[], useTranslation: boolean): string {
  return segments
    .map((seg) => {
      const text = useTranslation && seg.translatedText ? seg.translatedText : seg.text;
      return [
        seg.index,
        `${formatSrtTime(seg.startTime)} --> ${formatSrtTime(seg.endTime)}`,
        text,
      ].join('\n');
    })
    .join('\n\n');
}

/**
 * 触发浏览器下载 SRT 文件。
 */
export function downloadSrt(content: string, filename: string): void {
  const blob = new Blob([content], { type: 'text/srt; charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/**
 * 解析 SRT 格式字符串为 SrtSegment[]。
 */
export function parseSrt(srtContent: string): SrtSegment[] {
  const blocks = srtContent.trim().split(/\n\n+/);
  const segments: SrtSegment[] = [];

  for (const block of blocks) {
    const lines = block.trim().split('\n');
    if (lines.length < 2) continue;

    // 第一行是序号，第二行是时间轴
    const timeLine = lines[1];
    const timeMatch = timeLine.match(
      /(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,.]\d{3})/
    );
    if (!timeMatch) continue;

    const startTime = parseSrtTimeToSeconds(timeMatch[1]);
    const endTime = parseSrtTimeToSeconds(timeMatch[2]);
    const text = lines.slice(2).join('\n').trim();

    segments.push({
      index: segments.length + 1,
      startTime,
      endTime,
      text,
    });
  }

  return segments;
}

/**
 * 将 SRT 时间格式 (HH:MM:SS,mmm) 转换为秒数。
 */
function parseSrtTimeToSeconds(timeStr: string): number {
  const [h, m, sMs] = timeStr.split(':');
  const [s, ms] = (sMs || '0,000').split(/[,.]/);
  return parseInt(h) * 3600 + parseInt(m) * 60 + parseInt(s) + parseInt(ms) / 1000;
}
