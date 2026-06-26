import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  spring,
  useVideoConfig,
  Easing,
} from "remotion";
import { ReactNode } from "react";

export type SlideDirection = "left" | "right" | "top" | "bottom";

export interface SlideInProps {
  children: ReactNode;
  /**
   * 动画开始帧
   */
  startFrame?: number;
  /**
   * 动画持续时间（帧数），仅在非 spring 模式下使用
   */
  duration?: number;
  /**
   * 滑动方向
   */
  direction?: SlideDirection;
  /**
   * 滑动距离（像素），默认为视频尺寸的 100%
   */
  distance?: number;
  /**
   * 是否使用 spring 动画
   */
  useSpring?: boolean;
  /**
   * Spring 预设配置
   */
  springPreset?: "snappy" | "gentle" | "bouncy" | "smooth" | "stiff";
  /**
   * 缓动函数（非 spring 模式）
   */
  easing?: "linear" | "ease" | "ease-in" | "ease-out" | "ease-in-out";
  /**
   * 样式
   */
  style?: React.CSSProperties;
}

/**
 * SlideIn 组件 - 滑动入场动画
 *
 * @example
 * // 从左侧滑入
 * <SlideIn direction="left" startFrame={0}>
 *   <Text>Hello World</Text>
 * </SlideIn>
 *
 * @example
 * // 从顶部滑入，使用 spring 效果
 * <SlideIn direction="top" useSpring springPreset="bouncy">
 *   <Text>Bouncy entrance</Text>
 * </SlideIn>
 */
export const SlideIn: React.FC<SlideInProps> = ({
  children,
  startFrame = 0,
  duration = 30,
  direction = "left",
  distance,
  useSpring = false,
  springPreset = "gentle",
  easing = "ease-out",
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // 计算默认滑动距离
  const getDistance = () => {
    if (distance !== undefined) return distance;
    switch (direction) {
      case "left":
      case "right":
        return width;
      case "top":
      case "bottom":
        return height;
    }
  };

  const slideDistance = getDistance();

  // 获取初始位置
  const getInitialOffset = () => {
    switch (direction) {
      case "left":
        return { x: -slideDistance, y: 0 };
      case "right":
        return { x: slideDistance, y: 0 };
      case "top":
        return { x: 0, y: -slideDistance };
      case "bottom":
        return { x: 0, y: slideDistance };
    }
  };

  const initialOffset = getInitialOffset();

  const getEasingFunction = () => {
    switch (easing) {
      case "linear":
        return Easing.linear;
      case "ease":
      case "ease-in-out":
        return Easing.bezier(0.42, 0, 0.58, 1);
      case "ease-in":
        return Easing.bezier(0.42, 0, 1, 1);
      case "ease-out":
      default:
        return Easing.bezier(0, 0, 0.58, 1);
    }
  };

  // Spring 配置
  const springConfigs = {
    snappy: { damping: 20, stiffness: 100, mass: 0.5 },
    gentle: { damping: 15, stiffness: 50, mass: 1 },
    bouncy: { damping: 10, stiffness: 100, mass: 0.5 },
    smooth: { damping: 20, stiffness: 30, mass: 1 },
    stiff: { damping: 30, stiffness: 200, mass: 1 },
  };

  let translateX: number;
  let translateY: number;

  if (useSpring) {
    const progress = spring({
      frame: frame - startFrame,
      fps,
      config: springConfigs[springPreset],
    });

    translateX = interpolate(progress, [0, 1], [initialOffset.x, 0]);
    translateY = interpolate(progress, [0, 1], [initialOffset.y, 0]);
  } else {
    translateX = interpolate(
      frame,
      [startFrame, startFrame + duration],
      [initialOffset.x, 0],
      {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
        easing: getEasingFunction(),
      }
    );
    translateY = interpolate(
      frame,
      [startFrame, startFrame + duration],
      [initialOffset.y, 0],
      {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
        easing: getEasingFunction(),
      }
    );
  }

  return (
    <AbsoluteFill
      style={{
        ...style,
        transform: `translate(${translateX}px, ${translateY}px)`,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export default SlideIn;
