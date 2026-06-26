/** 转录任务状态 */
export type TaskStatus =
  | 'queued'
  | 'loading'
  | 'transcribing'
  | 'completed'
  | 'failed'
  | 'cancelled';

/** Whisper 支持的语言代码 */
export type LanguageCode =
  | 'auto'
  | 'ja'
  | 'zh'
  | 'en'
  | 'ko'
  | 'fr'
  | 'de'
  | 'es'
  | 'ru'
  | 'pt'
  | 'it'
  | 'ar'
  | 'hi'
  | 'th'
  | 'vi'
  | 'nl'
  | 'pl'
  | 'sv'
  | 'tr';

/** 单条 SRT 字幕段 */
export interface SrtSegment {
  /** 序号（1-based） */
  index: number;
  /** 开始时间（秒） */
  startTime: number;
  /** 结束时间（秒） */
  endTime: number;
  /** 原始文本 */
  text: string;
  /** 翻译文本（可选） */
  translatedText?: string;
}

/** 转录任务 */
export interface TranscriptionTask {
  /** 唯一标识 */
  id: string;
  /** 文件名 */
  fileName: string;
  /** 文件大小（字节） */
  fileSize: number;
  /** 原始音频文件路径 */
  filePath: string;
  /** 后端任务 ID（用于查询进度） */
  backendTaskId?: string;
  /** 语言代码 */
  language: string;
  /** 模型名称 */
  model: string;
  /** 分段秒数 */
  chunkSec: number;
  /** 重叠秒数 */
  overlapSec: number;
  /** 当前状态 */
  status: TaskStatus;
  /** 转录进度（0-100） */
  progress: number;
  /** 当前处理到第几个 chunk */
  currentChunk: number;
  /** 总 chunk 数 */
  totalChunks: number;
  /** 已跳过的 chunk 数（推理异常等） */
  skippedChunks: number;
  /** 跳过的 chunk 编号列表 */
  skippedChunkIndexes: number[];
  /** 转录结果段列表 */
  segments: SrtSegment[];
  /** 翻译结果段列表 */
  translatedSegments: SrtSegment[];
  /** 翻译状态：idle / translating / done */
  translationStatus: 'idle' | 'translating' | 'done';
  /** 输出 SRT 路径 */
  outputSrtPath?: string;
  /** 音频时长（秒） */
  duration?: number;
  /** 错误信息 */
  error?: string;
  /** 创建时间戳 */
  createdAt: number;
  /** 完成时间戳 */
  completedAt?: number;
}

/** 全局应用设置 */
export interface AppSettings {
  /** MLX Whisper 模型路径 */
  modelPath: string;
  /** 默认语言 */
  defaultLanguage: string;
  /** 默认分段秒数 */
  defaultChunkSec: number;
  /** 默认重叠秒数 */
  defaultOverlapSec: number;
  /** 输出目录 */
  outputDir: string;
  /** 最大并发数 */
  maxConcurrent: number;
  /** 后端 API 地址 */
  apiBaseUrl: string;
  /** 翻译模型 ID */
  translateModel: string;
}

/** 队列统计信息 */
export interface QueueStats {
  total: number;
  queued: number;
  loading: number;
  transcribing: number;
  completed: number;
  failed: number;
  cancelled: number;
}

/** 文件列表筛选标签 */
export type FilterTab = 'all' | 'transcribing' | 'completed' | 'failed';

/** 页面名称 */
export type PageName = 'transcribe' | 'translate';

/** SRT 翻译页面状态 */
export interface SrtTranslateState {
  /** 当前页面 */
  currentPage: PageName;
  /** 源语言 */
  sourceLanguage: string;
  /** 目标语言 */
  targetLanguage: string;
  /** 翻译模型（留空用默认） */
  translateModel: string;
  /** 已加载的 SRT segments */
  segments: SrtSegment[];
  /** 翻译后的 segments */
  translatedSegments: SrtSegment[];
  /** 翻译状态 */
  translateStatus: 'idle' | 'translating' | 'done' | 'error';
  /** 错误信息 */
  error?: string;
}

/** 语言选项 */
export interface LanguageOption {
  code: LanguageCode;
  label: string;
}
