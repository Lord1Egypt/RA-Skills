import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";
import { useMemo } from "react";

export interface WordHighlightProps {
  /**
   * 要显示的文字
   */
  text: string;
  /**
   * 要高亮的关键词列表
   */
  highlightWords?: string[];
  /**
   * 动画开始帧
   */
  startFrame?: number;
  /**
   * 每个词的动画持续时间（帧数）
   */
  wordDuration?: number;
  /**
   * 词之间的延迟（帧数）
   */
  wordDelay?: number;
  /**
   * 默认文字颜色
   */
  defaultColor?: string;
  /**
   * 高亮文字颜色
   */
  highlightColor?: string;
  /**
   * 高亮背景颜色
   */
  highlightBgColor?: string;
  /**
   * 是否使用 spring 动画
   */
  useSpring?: boolean;
  /**
   * 文字样式
   */
  textStyle?: React.CSSProperties;
  /**
   * 容器样式
   */
  style?: React.CSSProperties;
}

/**
 * WordHighlight 组件 - 文字逐词高亮动画
 *
 * @example
 * // 基础高亮效果
 * <WordHighlight
 *   text="The quick brown fox jumps"
 *   highlightWords={["quick", "fox"]}
 * />
 *
 * @example
 * // 自定义颜色和样式
 * <WordHighlight
 *   text="Hello World from Remotion"
 *   highlightWords={["World", "Remotion"]}
 *   highlightColor="#fff"
 *   highlightBgColor="#e94560"
 *   textStyle={{ fontSize: 48 }}
 * />
 */
export const WordHighlight: React.FC<WordHighlightProps> = ({
  text,
  highlightWords = [],
  startFrame = 0,
  wordDuration = 10,
  wordDelay = 5,
  defaultColor = "#888888",
  highlightColor = "#ffffff",
  highlightBgColor = "#e94560",
  useSpring = true,
  textStyle,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 分词
  const words = useMemo(() => text.split(/(\s+)/), [text]);

  // 检查是否是高亮词
  const isHighlightWord = (word: string) => {
    return highlightWords.some(
      (hw) => hw.toLowerCase() === word.toLowerCase()
    );
  };

  // 计算每个词的动画状态
  const getWordAnimation = (wordIndex: number, isHighlight: boolean) => {
    const wordStartFrame = startFrame + wordIndex * (wordDuration + wordDelay);
    const wordEndFrame = wordStartFrame + wordDuration;

    let progress: number;

    if (useSpring) {
      progress = spring({
        frame: frame - wordStartFrame,
        fps,
        config: {
          damping: 15,
          stiffness: 50,
          mass: 1,
        },
      });
    } else {
      progress = interpolate(frame, [wordStartFrame, wordEndFrame], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
    }

    if (isHighlight) {
      return {
        color: highlightColor,
        backgroundColor: `rgba(233, 69, 96, ${progress * 0.3})`,
        padding: "0 8px",
        borderRadius: "4px",
        transform: `scale(${1 + progress * 0.05})`,
        opacity: interpolate(frame, [wordStartFrame, wordStartFrame + 5], [0.5, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }),
      };
    }

    return {
      color: defaultColor,
      opacity: interpolate(frame, [wordStartFrame, wordStartFrame + 5], [0.3, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      }),
    };
  };

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "row",
        flexWrap: "wrap",
        ...style,
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          ...textStyle,
        }}
      >
        {words.map((word, index) => {
          const isHighlight = isHighlightWord(word.trim());
          const animStyle = getWordAnimation(index, isHighlight);

          if (/^\s+$/.test(word)) {
            // 保留空格
            return <span key={index}>{word}</span>;
          }

          return (
            <span
              key={index}
              style={{
                display: "inline-block",
                transition: "all 0.1s ease",
                ...animStyle,
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export default WordHighlight;
