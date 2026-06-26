import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

/**
 * HelloDemo - 基础演示视频
 * 用于验证 Remotion 项目是否正确配置
 */
export const HelloDemo: React.FC = () => {
  const frame = useCurrentFrame();

  // 文字淡入效果
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });

  // 文字缩放效果
  const scale = interpolate(frame, [0, 30], [0.8, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
          fontSize: 120,
          fontWeight: "bold",
          color: "#e94560",
          textShadow: "0 0 20px rgba(233, 69, 96, 0.5)",
        }}
      >
        Remotion Video Skill
      </div>
      <div
        style={{
          opacity: interpolate(frame, [30, 60], [0, 1], {
            extrapolateRight: "clamp",
          }),
          fontSize: 40,
          color: "#ffffff",
          marginTop: 40,
        }}
      >
        动画演示视频制作工具
      </div>
    </AbsoluteFill>
  );
};
