import { AbsoluteFill, Sequence, useCurrentFrame } from "remotion";
import {
  FadeIn,
  SlideIn,
  ScaleIn,
  Typewriter,
  WordHighlight,
} from "../components";

/**
 * AnimationDemo - 动画组件演示视频
 * 展示所有基础动画组件的效果
 */
export const AnimationDemo: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0f0f23",
        fontFamily: "Arial, sans-serif",
      }}
    >
      {/* 场景 1: FadeIn 演示 */}
      <Sequence from={0} durationInFrames={90}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <FadeIn startFrame={0} duration={30}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 60, color: "#e94560", fontWeight: "bold" }}>
                FadeIn 效果
              </div>
              <div style={{ fontSize: 30, color: "#ffffff", marginTop: 20 }}>
                淡入动画演示
              </div>
            </div>
          </FadeIn>
        </AbsoluteFill>
      </Sequence>

      {/* 场景 2: SlideIn 演示 */}
      <Sequence from={90} durationInFrames={120}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: 40 }}>
            <SlideIn direction="left" startFrame={0} useSpring springPreset="bouncy">
              <div style={{ fontSize: 48, color: "#00d9ff" }}>← 从左侧滑入</div>
            </SlideIn>
            <SlideIn direction="right" startFrame={15} useSpring springPreset="bouncy">
              <div style={{ fontSize: 48, color: "#ff6b6b" }}>从右侧滑入 →</div>
            </SlideIn>
            <SlideIn direction="top" startFrame={30} useSpring springPreset="gentle">
              <div style={{ fontSize: 48, color: "#4ecdc4" }}>↑ 从顶部滑入</div>
            </SlideIn>
            <SlideIn direction="bottom" startFrame={45} useSpring springPreset="gentle">
              <div style={{ fontSize: 48, color: "#ffe66d" }}>↓ 从底部滑入</div>
            </SlideIn>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* 场景 3: ScaleIn 演示 */}
      <Sequence from={210} durationInFrames={90}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div style={{ display: "flex", gap: 60 }}>
            <ScaleIn startFrame={0} useSpring springPreset="bouncy">
              <div
                style={{
                  width: 150,
                  height: 150,
                  backgroundColor: "#e94560",
                  borderRadius: 20,
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  fontSize: 24,
                  color: "#fff",
                }}
              >
                Bouncy
              </div>
            </ScaleIn>
            <ScaleIn startFrame={15} useSpring springPreset="gentle">
              <div
                style={{
                  width: 150,
                  height: 150,
                  backgroundColor: "#4ecdc4",
                  borderRadius: 20,
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  fontSize: 24,
                  color: "#fff",
                }}
              >
                Gentle
              </div>
            </ScaleIn>
            <ScaleIn startFrame={30} useSpring springPreset="snappy">
              <div
                style={{
                  width: 150,
                  height: 150,
                  backgroundColor: "#ffe66d",
                  borderRadius: 20,
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  fontSize: 24,
                  color: "#333",
                }}
              >
                Snappy
              </div>
            </ScaleIn>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* 场景 4: Typewriter 演示 */}
      <Sequence from={300} durationInFrames={150}>
        <AbsoluteFill
          style={{
            backgroundColor: "#1a1a2e",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div style={{ textAlign: "center" }}>
            <Typewriter
              text="Hello, Remotion Video Skill!"
              startFrame={0}
              charsPerFrame={0.8}
              showCursor
              cursorChar="|"
              cursorBlinkRate={15}
              textStyle={{
                fontSize: 56,
                color: "#00ff88",
                fontFamily: "monospace",
              }}
              cursorStyle={{ color: "#00ff88" }}
            />
            <div style={{ marginTop: 60 }}>
              <Typewriter
                text="Create amazing animations with ease..."
                startFrame={60}
                charsPerFrame={1}
                showCursor
                cursorChar="▌"
                cursorBlinkRate={12}
                textStyle={{
                  fontSize: 36,
                  color: "#888",
                  fontFamily: "monospace",
                }}
              />
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* 场景 5: WordHighlight 演示 */}
      <Sequence from={450} durationInFrames={120}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div style={{ textAlign: "center" }}>
            <WordHighlight
              text="The quick brown fox jumps over the lazy dog"
              highlightWords={["quick", "fox", "lazy"]}
              startFrame={0}
              wordDuration={8}
              wordDelay={4}
              defaultColor="#666"
              highlightColor="#fff"
              highlightBgColor="#e94560"
              textStyle={{ fontSize: 42 }}
            />
            <div style={{ marginTop: 60 }}>
              <WordHighlight
                text="Remotion makes video creation fun and easy"
                highlightWords={["Remotion", "video", "fun"]}
                startFrame={60}
                wordDuration={6}
                wordDelay={3}
                defaultColor="#888"
                highlightColor="#fff"
                highlightBgColor="#4ecdc4"
                textStyle={{ fontSize: 36 }}
              />
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* 结束场景 */}
      <Sequence from={570} durationInFrames={90}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <FadeIn startFrame={0} duration={20}>
            <ScaleIn startFrame={0} useSpring springPreset="bouncy">
              <div style={{ textAlign: "center" }}>
                <div
                  style={{
                    fontSize: 72,
                    fontWeight: "bold",
                    background: "linear-gradient(90deg, #e94560, #4ecdc4)",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                  }}
                >
                  Remotion Video Skill
                </div>
                <div style={{ fontSize: 32, color: "#888", marginTop: 20 }}>
                  基础动画组件库演示完成
                </div>
              </div>
            </ScaleIn>
          </FadeIn>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};

export default AnimationDemo;
