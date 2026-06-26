import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { ReactNode } from "react";

/**
 * 过渡类型
 */
export type TransitionType = "fade" | "slide" | "wipe" | "none";

/**
 * 滑动方向
 */
export type SlideDirection = "from-left" | "from-right" | "from-top" | "from-bottom";

/**
 * 擦除方向
 */
export type WipeDirection = "from-left" | "from-right" | "from-top" | "from-bottom";

export interface TransitionSceneProps {
  /**
   * 进入场景的内容
   */
  children: ReactNode;
  /**
   * 过渡类型
   */
  transition?: TransitionType;
  /**
   * 过渡持续时间（帧数）
   */
  duration?: number;
  /**
   * 滑动方向（仅 slide 类型有效）
   */
  slideDirection?: SlideDirection;
  /**
   * 擦除方向（仅 wipe 类型有效）
   */
  wipeDirection?: WipeDirection;
  /**
   * 样式
   */
  style?: React.CSSProperties;
}

/**
 * TransitionScene 组件 - 场景过渡效果
 *
 * 用于在场景之间添加过渡动画，支持淡入淡出、滑动、擦除等效果。
 *
 * @example
 * // 淡入场景
 * <TransitionScene transition="fade" duration={30}>
 *   <Text>Hello World</Text>
 * </TransitionScene>
 *
 * @example
 * // 从右侧滑入
 * <TransitionScene transition="slide" slideDirection="from-right" duration={20}>
 *   <Rect fill="blue" />
 * </TransitionScene>
 */
export const TransitionScene: React.FC<TransitionSceneProps> = ({
  children,
  transition = "fade",
  duration = 30,
  slideDirection = "from-left",
  wipeDirection = "from-left",
  style,
}) => {
  const frame = useCurrentFrame();

  if (transition === "none") {
    return <AbsoluteFill style={style}>{children}</AbsoluteFill>;
  }

  const progress = interpolate(
    frame,
    [0, duration],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.bezier(0, 0, 0.58, 1),
    }
  );

  const transitionStyles = getTransitionStyles(transition, progress, slideDirection, wipeDirection);

  return (
    <AbsoluteFill style={{ ...style, ...transitionStyles }}>
      {children}
    </AbsoluteFill>
  );
};

/**
 * 获取过渡样式
 */
function getTransitionStyles(
  type: TransitionType,
  progress: number,
  slideDirection?: SlideDirection,
  wipeDirection?: WipeDirection
): React.CSSProperties {
  switch (type) {
    case "fade":
      return {
        opacity: progress,
      };
    case "slide": {
      const offset = (1 - progress) * 100;
      switch (slideDirection) {
        case "from-right":
          return { opacity: 1, transform: `translateX(${offset}%)` };
        case "from-left":
          return { opacity: 1, transform: `translateX(-${offset}%)` };
        case "from-bottom":
          return { opacity: 1, transform: `translateY(${offset}%)` };
        case "from-top":
          return { opacity: 1, transform: `translateY(-${offset}%)` };
        default:
          return { opacity: 1, transform: `translateX(-${offset}%)` };
      }
    }
    case "wipe": {
      const clipProgress = progress * 100;
      let clipPath: string;
      switch (wipeDirection) {
        case "from-right":
          clipPath = `inset(0 0 0 ${clipProgress}%)`;
          break;
        case "from-left":
          clipPath = `inset(0 ${100 - clipProgress}% 0 0)`;
          break;
        case "from-bottom":
          clipPath = `inset(${clipProgress}% 0 0 0)`;
          break;
        case "from-top":
          clipPath = `inset(0 0 ${100 - clipProgress}% 0)`;
          break;
        default:
          clipPath = `inset(0 ${100 - clipProgress}% 0 0)`;
      }
      return { opacity: 1, clipPath };
    }
    default:
      return { opacity: 1 };
  }
}

export default TransitionScene;
