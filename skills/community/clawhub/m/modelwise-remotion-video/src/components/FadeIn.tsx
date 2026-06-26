import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  Easing,
} from "remotion";
import { ReactNode } from "react";

export type FadeDirection = "in" | "out" | "in-out";

export interface FadeInProps {
  children: ReactNode;
  /**
   * 动画开始帧
   */
  startFrame?: number;
  /**
   * 动画持续时间（帧数）
   */
  duration?: number;
  /**
   * 淡入淡出类型
   */
  type?: FadeDirection;
  /**
   * 初始透明度
   */
  initialOpacity?: number;
  /**
   * 最终透明度
   */
  finalOpacity?: number;
  /**
   * 缓动函数
   */
  easing?: "linear" | "ease" | "ease-in" | "ease-out" | "ease-in-out";
  /**
   * 样式
   */
  style?: React.CSSProperties;
}

/**
 * FadeIn 组件 - 淡入淡出动画
 *
 * @example
 * // 淡入效果
 * <FadeIn startFrame={0} duration={30}>
 *   <Text>Hello World</Text>
 * </FadeIn>
 *
 * @example
 * // 淡出效果
 * <FadeIn type="out" startFrame={60} duration={30}>
 *   <Text>Goodbye</Text>
 * </FadeIn>
 *
 * @example
 * // 淡入淡出组合
 * <FadeIn type="in-out" startFrame={0} duration={30} fadeOutStart={90}>
 *   <Text>Appear and disappear</Text>
 * </FadeIn>
 */
export const FadeIn: React.FC<FadeInProps> = ({
  children,
  startFrame = 0,
  duration = 30,
  type = "in",
  initialOpacity = 0,
  finalOpacity = 1,
  easing = "ease-out",
  style,
}) => {
  const frame = useCurrentFrame();

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

  let opacity: number;

  if (type === "in") {
    opacity = interpolate(frame, [startFrame, startFrame + duration], [initialOpacity, finalOpacity], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: getEasingFunction(),
    });
  } else if (type === "out") {
    opacity = interpolate(frame, [startFrame, startFrame + duration], [finalOpacity, initialOpacity], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: getEasingFunction(),
    });
  } else {
    // in-out: 先淡入再淡出
    const fadeInProgress = interpolate(
      frame,
      [startFrame, startFrame + duration],
      [initialOpacity, finalOpacity],
      {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
        easing: getEasingFunction(),
      }
    );
    const fadeOutProgress = interpolate(
      frame,
      [startFrame + duration * 2, startFrame + duration * 3],
      [finalOpacity, initialOpacity],
      {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
        easing: getEasingFunction(),
      }
    );
    opacity = frame < startFrame + duration * 2 ? fadeInProgress : fadeOutProgress;
  }

  return (
    <AbsoluteFill style={{ ...style, opacity }}>
      {children}
    </AbsoluteFill>
  );
};

export default FadeIn;
