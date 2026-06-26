import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);

// 视频配置预设
export const videoConfigs = {
  // 标准 16:9 横屏
  landscape: {
    width: 1920,
    height: 1080,
    fps: 30,
  },
  // 竖屏 9:16 (短视频)
  portrait: {
    width: 1080,
    height: 1920,
    fps: 30,
  },
  // 正方形 1:1
  square: {
    width: 1080,
    height: 1080,
    fps: 30,
  },
};
