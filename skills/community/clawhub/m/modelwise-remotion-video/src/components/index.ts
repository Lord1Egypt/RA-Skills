/**
 * 基础动画组件库
 * 导出所有动画组件
 */

export { FadeIn, type FadeInProps, type FadeDirection } from "./FadeIn";
export { SlideIn, type SlideInProps, type SlideDirection } from "./SlideIn";
export { ScaleIn, type ScaleInProps } from "./ScaleIn";
export { Typewriter, type TypewriterProps } from "./Typewriter";
export { WordHighlight, type WordHighlightProps } from "./WordHighlight";

// 场景过渡组件
export {
  TransitionScene,
  type TransitionSceneProps,
  type TransitionType,
  type SlideDirection as TransitionSlideDirection,
  type WipeDirection,
} from "./TransitionScene";
