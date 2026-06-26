/**
 * 时间计算工具函数
 */

/**
 * 将秒数转换为帧数
 * @param seconds 秒数
 * @param fps 帧率（默认 30）
 */
export const secondsToFrames = (seconds: number, fps = 30): number => {
  return Math.round(seconds * fps);
};

/**
 * 将帧数转换为秒数
 * @param frames 帧数
 * @param fps 帧率（默认 30）
 */
export const framesToSeconds = (frames: number, fps = 30): number => {
  return frames / fps;
};

/**
 * 将毫秒转换为帧数
 * @param ms 毫秒
 * @param fps 帧率（默认 30）
 */
export const msToFrames = (ms: number, fps = 30): number => {
  return Math.round((ms / 1000) * fps);
};

/**
 * 计算视频时长（秒）
 * @param frames 总帧数
 * @param fps 帧率（默认 30）
 */
export const getDuration = (frames: number, fps = 30): string => {
  const totalSeconds = frames / fps;
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = Math.floor(totalSeconds % 60);
  const remainingFrames = frames % fps;

  if (minutes > 0) {
    return `${minutes}m ${seconds}s ${remainingFrames}f`;
  }
  return `${seconds}s ${remainingFrames}f`;
};
