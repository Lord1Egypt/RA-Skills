/**
 * 视频尺寸预设
 */
export const videoPresets = {
  // 16:9 横屏 (YouTube, B站)
  landscape: {
    width: 1920,
    height: 1080,
    fps: 30,
    aspectRatio: "16:9" as const,
  },
  // 4K 横屏
  landscape4K: {
    width: 3840,
    height: 2160,
    fps: 30,
    aspectRatio: "16:9" as const,
  },
  // 9:16 竖屏 (抖音, 快手, 视频号)
  portrait: {
    width: 1080,
    height: 1920,
    fps: 30,
    aspectRatio: "9:16" as const,
  },
  // 1:1 正方形 (Instagram)
  square: {
    width: 1080,
    height: 1080,
    fps: 30,
    aspectRatio: "1:1" as const,
  },
  // 4:5 竖版 (Instagram Feed)
  instagramFeed: {
    width: 1080,
    height: 1350,
    fps: 30,
    aspectRatio: "4:5" as const,
  },
};

export type VideoPreset = keyof typeof videoPresets;
export type VideoConfig = (typeof videoPresets)[VideoPreset];

/**
 * 获取视频预设配置
 */
export const getVideoPreset = (preset: VideoPreset): VideoConfig => {
  return videoPresets[preset];
};
