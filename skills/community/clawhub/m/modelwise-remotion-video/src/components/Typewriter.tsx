import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { useMemo } from "react";

export interface TypewriterProps {
  /**
   * 要显示的文字
   */
  text: string;
  /**
   * 动画开始帧
   */
  startFrame?: number;
  /**
   * 每个字符的显示持续时间（帧数）
   */
  charsPerFrame?: number;
  /**
   * 是否显示光标
   */
  showCursor?: boolean;
  /**
   * 光标字符
   */
  cursorChar?: string;
  /**
   * 光标闪烁速度（帧数）
   */
  cursorBlinkRate?: number;
  /**
   * 文字样式
   */
  textStyle?: React.CSSProperties;
  /**
   * 光标样式
   */
  cursorStyle?: React.CSSProperties;
  /**
   * 容器样式
   */
  style?: React.CSSProperties;
  /**
   * 打字完成后的延迟帧数（用于光标闪烁）
   */
  endDelay?: number;
}

/**
 * Typewriter 组件 - 打字机文字效果
 *
 * @example
 * // 基础打字机效果
 * <Typewriter text="Hello World!" startFrame={0} />
 *
 * @example
 * // 自定义速度和光标
 * <Typewriter
 *   text="Faster typing"
 *   charsPerFrame={2}
 *   cursorChar="|"
 *   cursorBlinkRate={10}
 * />
 *
 * @example
 * // 自定义样式
 * <Typewriter
 *   text="Styled text"
 *   textStyle={{ fontSize: 60, color: '#fff', fontFamily: 'monospace' }}
 *   cursorStyle={{ color: '#00ff00' }}
 * />
 */
export const Typewriter: React.FC<TypewriterProps> = ({
  text,
  startFrame = 0,
  charsPerFrame = 0.5,
  showCursor = true,
  cursorChar = "_",
  cursorBlinkRate = 15,
  textStyle,
  cursorStyle,
  style,
  endDelay = 60,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 计算当前应该显示的字符数
  const totalFrames = text.length / charsPerFrame;
  const currentCharCount = Math.floor(
    interpolate(frame, [startFrame, startFrame + totalFrames], [0, text.length], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  // 当前显示的文字
  const displayedText = useMemo(() => {
    return text.slice(0, currentCharCount);
  }, [text, currentCharCount]);

  // 光标是否可见（闪烁效果）
  const cursorVisible = useMemo(() => {
    if (!showCursor) return false;
    const isTyping = frame >= startFrame && currentCharCount < text.length;
    const isBlinking = Math.floor(frame / cursorBlinkRate) % 2 === 0;
    // 打字过程中光标一直显示，打完后闪烁
    return isTyping || isBlinking;
  }, [frame, showCursor, currentCharCount, text.length, cursorBlinkRate]);

  // 是否完成打字
  const isComplete = currentCharCount >= text.length;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "row",
        ...style,
      }}
    >
      <span style={{ fontFamily: "monospace", whiteSpace: "pre", ...textStyle }}>
        {displayedText}
        {showCursor && (
          <span
            style={{
              opacity: cursorVisible ? 1 : 0,
              transition: "opacity 0.1s",
              ...cursorStyle,
            }}
          >
            {cursorChar}
          </span>
        )}
      </span>
    </AbsoluteFill>
  );
};

export default Typewriter;
