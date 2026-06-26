import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  spring,
  useVideoConfig,
  Easing,
} from "remotion";
import { ReactNode } from "react";

export interface ScaleInProps {
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
   * 初始缩放比例
   */
  initialScale?: number;
  /**
   * 最终缩放比例
   */
  finalScale?: number;
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
   * 变换原点
   */
  transformOrigin?: string;
  /**
   * 样式
   */
  style?: React.CSSProperties;
}

/**
 * ScaleIn 组件 - 缩放入场动画
 *
 * @example
 * // 从 0 缩放到 1
 * <ScaleIn startFrame={0}>
 *   <Text>Hello World</Text>
 * </ScaleIn>
 *
 * @example
 * // 使用 bouncy spring 效果
 * <ScaleIn useSpring springPreset="bouncy" initialScale={0.5}>
 *   <Text>Bouncy scale</Text>
 * </ScaleIn>
 *
 * @example
 * // 从 2 缩小到 1
 * <ScaleIn initialScale={2} finalScale={1}>
 *   <Text>Zoom out</Text>
 * </ScaleIn>
 */
export const ScaleIn: React.FC<ScaleInProps> = ({
  children,
  startFrame = 0,
  duration = 30,
  initialScale = 0,
  finalScale = 1,
  useSpring = true,
  springPreset = "gentle",
  easing = "ease-out",
  transformOrigin = "center center",
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

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

  let scale: number;

  if (useSpring) {
    const progress = spring({
      frame: frame - startFrame,
      fps,
      config: springConfigs[springPreset],
    });

    scale = interpolate(progress, [0, 1], [initialScale, finalScale]);
  } else {
    scale = interpolate(
      frame,
      [startFrame, startFrame + duration],
      [initialScale, finalScale],
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
        transform: `scale(${scale})`,
        transformOrigin,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export default ScaleIn;
