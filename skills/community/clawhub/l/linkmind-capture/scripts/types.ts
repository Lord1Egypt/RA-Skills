export interface CapturedContent {
  platform: "weibo" | "xiaohongshu" | "wechat" | "xiaoyuzhou";
  title: string;
  author: string;
  authorAvatar?: string;
  date: string;
  text: string;
  images: string[];
  videoUrl: string | null;
  originalUrl: string;
  fetchedAt: string;
  /** Platform-specific metadata */
  extra?: Record<string, unknown>;
}

export interface WeiboContent extends CapturedContent {
  platform: "weibo";
  repostOf: { author: string; text: string } | null;
  stats: {
    reposts: number;
    comments: number;
    likes: number;
  };
}

export interface XiaohongshuContent extends CapturedContent {
  platform: "xiaohongshu";
  tags: string[];
  stats: {
    likes: number;
    collects: number;
    comments: number;
  };
}

export type ErrorCode =
  | "NETWORK"
  | "AUTH"
  | "RATE_LIMIT"
  | "NOT_FOUND"
  | "PARSE"
  | "DEPENDENCY"
  | "UNKNOWN";

export interface HandlerError {
  error: string;
  code?: ErrorCode;
  url?: string;
  details?: string;
}

export type HandlerResult = CapturedContent | HandlerError;

export interface WechatContent extends CapturedContent {
  platform: "wechat";
  accountName: string;
  digest: string;
  coverImage: string | null;
  readCount: number | null;
  likeCount: number | null;
  inLookCount: number | null;
  /**
   * Markdown with inline images (e.g. `![](url)`) interleaved with text,
   * preserving the original author's image placement in the article body.
   * Use this field instead of `text` when rendering WeChat notes.
   */
  richContent?: string;
}

export interface XiaoyuzhouContent extends CapturedContent {
  platform: "xiaoyuzhou";
  episodeId: string;
  podcast: string;                  // 节目名称（如"42章经"）
  durationSeconds: number;          // 音频总时长（秒）
  timestampSeconds: number | null;  // 分享时打点的时间（秒），无则 null
  subtitleUrl: string | null;       // 平台提供的字幕文件 URL，无则 null
  description: string;              // 节目 shownotes / 简介
  audioUrl: string;                 // 音频文件直链（用于下载音频或 ASR 提取）
}

export function isError(result: HandlerResult): result is HandlerError {
  return "error" in result;
}
