import { spring } from "remotion";

/**
 * Spring 动画预设配置
 */
export const springPresets = {
  // 快速弹性
  snappy: {
    damping: 20,
    stiffness: 100,
    mass: 0.5,
  },
  // 柔和弹性
  gentle: {
    damping: 15,
    stiffness: 50,
    mass: 1,
  },
  // 弹跳效果
  bouncy: {
    damping: 10,
    stiffness: 100,
    mass: 0.5,
  },
  // 平滑过渡
  smooth: {
    damping: 20,
    stiffness: 30,
    mass: 1,
  },
  // 刚性（无弹性）
  stiff: {
    damping: 30,
    stiffness: 200,
    mass: 1,
  },
};

/**
 * Easing 函数集合
 */
export const easingPresets = {
  easeInOut: (t: number) => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t),
  easeIn: (t: number) => t * t,
  easeOut: (t: number) => t * (2 - t),
  easeInCubic: (t: number) => t * t * t,
  easeOutCubic: (t: number) => --t * t * t + 1,
  easeInOutCubic: (t: number) =>
    t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
};

/**
 * 创建 spring 动画值
 * @param frame 当前帧
 * @param config spring 配置
 * @param fps 帧率
 */
export const createSpring = (
  frame: number,
  config: keyof typeof springPresets = "gentle",
  fps = 30
) => {
  return spring({
    frame,
    fps,
    ...springPresets[config],
  });
};
