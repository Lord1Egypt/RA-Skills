import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
  useCurrentFrame,
  interpolate,
  Easing,
  spring,
} from "remotion";
import { FadeIn } from "../components/FadeIn";
import { SlideIn } from "../components/SlideIn";
import { ScaleIn } from "../components/ScaleIn";

/**
 * 标题序列样式预设
 */
type TitleStyle = "cinematic" | "minimal" | "playful" | "corporate";

interface TitleSequenceProps {
  title?: string;
  subtitle?: string;
  style?: TitleStyle;
}

/**
 * 电影风格标题场景
 */
const CinematicTitle: React.FC<{ title: string; subtitle: string }> = ({
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 主标题动画
  const titleY = interpolate(
    frame,
    [0, 30],
    [100, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    }
  );

  const titleOpacity = interpolate(
    frame,
    [0, 20],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // 字幕动画
  const subtitleOpacity = interpolate(
    frame,
    [30, 50],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // 背景光效
  const lightX = interpolate(
    frame,
    [0, 150],
    [-200, 200],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%)",
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {/* 光效背景 */}
      <div
        style={{
          position: "absolute",
          width: 400,
          height: 400,
          background:
            "radial-gradient(circle, rgba(255,215,0,0.3) 0%, transparent 70%)",
          transform: `translateX(${lightX}px)`,
          top: "30%",
        }}
      />

      {/* 主标题 */}
      <div
        style={{
          transform: `translateY(${titleY}px)`,
          opacity: titleOpacity,
          textAlign: "center",
        }}
      >
        <h1
          style={{
            fontSize: 120,
            color: "#ffd700",
            fontFamily: "Georgia, serif",
            margin: 0,
            textShadow: "0 4px 20px rgba(255, 215, 0, 0.5)",
            letterSpacing: 10,
          }}
        >
          {title}
        </h1>
      </div>

      {/* 字幕 */}
      <div
        style={{
          opacity: subtitleOpacity,
          marginTop: 40,
          textAlign: "center",
        }}
      >
        <p
          style={{
            fontSize: 40,
            color: "#ffffff",
            fontFamily: "Arial, sans-serif",
            margin: 0,
            letterSpacing: 5,
            textTransform: "uppercase",
          }}
        >
          {subtitle}
        </p>
      </div>

      {/* 底部装饰线 */}
      <div
        style={{
          position: "absolute",
          bottom: 100,
          width: interpolate(frame, [50, 100], [0, 600], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
          height: 2,
          background: "linear-gradient(90deg, transparent, #ffd700, transparent)",
        }}
      />
    </AbsoluteFill>
  );
};

/**
 * 极简风格标题场景
 */
const MinimalTitle: React.FC<{ title: string; subtitle: string }> = ({
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 20, stiffness: 100, mass: 0.5 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#ffffff",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1
          style={{
            fontSize: 100,
            color: "#000000",
            fontFamily: "Helvetica, sans-serif",
            margin: 0,
            fontWeight: 300,
            transform: `translateY(${(1 - progress) * 50}px)`,
            opacity: progress,
          }}
        >
          {title}
        </h1>
        <p
          style={{
            fontSize: 30,
            color: "#666666",
            fontFamily: "Helvetica, sans-serif",
            margin: "30px 0 0",
            fontWeight: 300,
            opacity: interpolate(frame, [30, 60], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          {subtitle}
        </p>
      </div>
    </AbsoluteFill>
  );
};

/**
 * 活泼风格标题场景
 */
const PlayfulTitle: React.FC<{ title: string; subtitle: string }> = ({
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const colors = ["#ff6b6b", "#4ecdc4", "#ffe66d", "#95e1d3"];
  const letters = title.split("");

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1
          style={{
            fontSize: 100,
            fontFamily: "Arial Black, sans-serif",
            margin: 0,
            display: "flex",
            justifyContent: "center",
          }}
        >
          {letters.map((letter, index) => {
            const delay = index * 3;
            const letterProgress = spring({
              frame: frame - delay,
              fps,
              config: { damping: 10, stiffness: 100, mass: 0.5 },
            });

            const rotation = interpolate(letterProgress, [0, 1], [-180, 0]);
            const scale = letterProgress;
            const color = colors[index % colors.length];

            return (
              <span
                key={index}
                style={{
                  display: "inline-block",
                  color,
                  transform: `rotate(${rotation}deg) scale(${scale})`,
                  textShadow: `0 0 20px ${color}`,
                }}
              >
                {letter === " " ? "\u00A0" : letter}
              </span>
            );
          })}
        </h1>
        <SlideIn direction="top" duration={20} startFrame={40}>
          <p
            style={{
              fontSize: 36,
              color: "#ffffff",
              fontFamily: "Arial, sans-serif",
              margin: "40px 0 0",
            }}
          >
            {subtitle}
          </p>
        </SlideIn>
      </div>
    </AbsoluteFill>
  );
};

/**
 * 企业风格标题场景
 */
const CorporateTitle: React.FC<{ title: string; subtitle: string }> = ({
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const lineProgress = interpolate(frame, [0, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* 左侧装饰线 */}
      <div
        style={{
          position: "absolute",
          left: 100,
          top: "50%",
          transform: "translateY(-50%)",
          width: 4,
          height: lineProgress * 200,
          backgroundColor: "#ffffff",
        }}
      />

      <div style={{ textAlign: "center", marginLeft: 50 }}>
        <FadeIn duration={30}>
          <h1
            style={{
              fontSize: 90,
              color: "#ffffff",
              fontFamily: "Georgia, serif",
              margin: 0,
              fontWeight: "bold",
            }}
          >
            {title}
          </h1>
        </FadeIn>
        <FadeIn duration={20} startFrame={20}>
          <p
            style={{
              fontSize: 32,
              color: "rgba(255,255,255,0.8)",
              fontFamily: "Arial, sans-serif",
              margin: "30px 0 0",
              letterSpacing: 3,
            }}
          >
            {subtitle}
          </p>
        </FadeIn>
      </div>

      {/* 右下角装饰 */}
      <div
        style={{
          position: "absolute",
          right: 60,
          bottom: 60,
          width: 80,
          height: 80,
          borderTop: "3px solid rgba(255,255,255,0.5)",
          borderRight: "3px solid rgba(255,255,255,0.5)",
          opacity: interpolate(frame, [40, 60], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      />
    </AbsoluteFill>
  );
};

/**
 * TitleSequence - 标题动画模板
 *
 * 提供多种风格的标题动画效果：
 * - cinematic: 电影风格，金色标题配光效
 * - minimal: 极简风格，黑白配色
 * - playful: 活泼风格，彩色字母逐个弹跳
 * - corporate: 企业风格，蓝色渐变背景
 */
export const TitleSequence: React.FC<TitleSequenceProps> = ({
  title = "Title",
  subtitle = "Subtitle",
  style = "cinematic",
}) => {
  const TitleComponent = {
    cinematic: CinematicTitle,
    minimal: MinimalTitle,
    playful: PlayfulTitle,
    corporate: CorporateTitle,
  }[style];

  return <TitleComponent title={title} subtitle={subtitle} />;
};

export default TitleSequence;
