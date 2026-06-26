import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { TransitionScene } from "../components/TransitionScene";
import { FadeIn } from "../components/FadeIn";
import { SlideIn } from "../components/SlideIn";

/**
 * 场景1 - 欢迎场景
 */
const WelcomeScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <FadeIn duration={20}>
        <h1
          style={{
            fontSize: 80,
            color: "#e94560",
            fontFamily: "Arial, sans-serif",
            margin: 0,
          }}
        >
          Welcome
        </h1>
      </FadeIn>
    </AbsoluteFill>
  );
};

/**
 * 场景2 - 过渡展示场景
 */
const TransitionIntroScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#16213e",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <SlideIn direction="left" duration={25}>
        <h2
          style={{
            fontSize: 60,
            color: "#0f3460",
            fontFamily: "Arial, sans-serif",
            margin: 0,
            backgroundColor: "#e94560",
            padding: "20px 40px",
            borderRadius: 10,
          }}
        >
          Transition Effects
        </h2>
      </SlideIn>
    </AbsoluteFill>
  );
};

/**
 * 场景3 - Fade 过渡演示
 */
const FadeDemoScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0f3460",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <FadeIn duration={15}>
        <div style={{ textAlign: "center" }}>
          <h2
            style={{
              fontSize: 70,
              color: "#e94560",
              fontFamily: "Arial, sans-serif",
              margin: 0,
            }}
          >
            Fade Transition
          </h2>
          <p
            style={{
              fontSize: 30,
              color: "#ffffff",
              fontFamily: "Arial, sans-serif",
              marginTop: 20,
            }}
          >
            Smooth opacity animation
          </p>
        </div>
      </FadeIn>
    </AbsoluteFill>
  );
};

/**
 * 场景4 - Slide 过渡演示
 */
const SlideDemoScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#533483",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <SlideIn direction="right" duration={20}>
        <div style={{ textAlign: "center" }}>
          <h2
            style={{
              fontSize: 70,
              color: "#e94560",
              fontFamily: "Arial, sans-serif",
              margin: 0,
            }}
          >
            Slide Transition
          </h2>
          <p
            style={{
              fontSize: 30,
              color: "#ffffff",
              fontFamily: "Arial, sans-serif",
              marginTop: 20,
            }}
          >
            Sliding from different directions
          </p>
        </div>
      </SlideIn>
    </AbsoluteFill>
  );
};

/**
 * 场景5 - Wipe 过渡演示
 */
const WipeDemoScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#e94560",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <FadeIn duration={15}>
        <div style={{ textAlign: "center" }}>
          <h2
            style={{
              fontSize: 70,
              color: "#ffffff",
              fontFamily: "Arial, sans-serif",
              margin: 0,
            }}
          >
            Wipe Transition
          </h2>
          <p
            style={{
              fontSize: 30,
              color: "#1a1a2e",
              fontFamily: "Arial, sans-serif",
              marginTop: 20,
            }}
          >
            Clip-path reveal effect
          </p>
        </div>
      </FadeIn>
    </AbsoluteFill>
  );
};

/**
 * 场景6 - 结束场景
 */
const EndScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <FadeIn duration={20}>
        <h1
          style={{
            fontSize: 80,
            color: "#e94560",
            fontFamily: "Arial, sans-serif",
            margin: 0,
          }}
        >
          Thanks for Watching!
        </h1>
      </FadeIn>
    </AbsoluteFill>
  );
};

/**
 * TransitionDemo - 场景过渡效果演示视频
 *
 * 展示如何使用 TransitionScene 组件在多个场景之间添加过渡动画。
 * 包含 fade、slide、wipe 三种过渡效果的演示。
 */
export const TransitionDemo: React.FC = () => {
  const { fps } = useVideoConfig();

  // 每个场景的持续时间（秒）
  const sceneDuration = 3;
  const sceneFrames = sceneDuration * fps;

  // 过渡动画持续时间（帧）
  const transitionDuration = 30;

  return (
    <AbsoluteFill>
      {/* 场景1: 欢迎场景 */}
      <Sequence from={0} durationInFrames={sceneFrames}>
        <TransitionScene transition="fade" duration={transitionDuration}>
          <WelcomeScene />
        </TransitionScene>
      </Sequence>

      {/* 场景2: 过渡介绍 */}
      <Sequence from={sceneFrames} durationInFrames={sceneFrames}>
        <TransitionScene
          transition="slide"
          slideDirection="from-left"
          duration={transitionDuration}
        >
          <TransitionIntroScene />
        </TransitionScene>
      </Sequence>

      {/* 场景3: Fade 演示 */}
      <Sequence from={sceneFrames * 2} durationInFrames={sceneFrames}>
        <TransitionScene transition="fade" duration={transitionDuration}>
          <FadeDemoScene />
        </TransitionScene>
      </Sequence>

      {/* 场景4: Slide 演示 */}
      <Sequence from={sceneFrames * 3} durationInFrames={sceneFrames}>
        <TransitionScene
          transition="slide"
          slideDirection="from-right"
          duration={transitionDuration}
        >
          <SlideDemoScene />
        </TransitionScene>
      </Sequence>

      {/* 场景5: Wipe 演示 */}
      <Sequence from={sceneFrames * 4} durationInFrames={sceneFrames}>
        <TransitionScene
          transition="wipe"
          wipeDirection="from-left"
          duration={transitionDuration}
        >
          <WipeDemoScene />
        </TransitionScene>
      </Sequence>

      {/* 场景6: 结束场景 */}
      <Sequence from={sceneFrames * 5} durationInFrames={sceneFrames}>
        <TransitionScene transition="fade" duration={transitionDuration}>
          <EndScene />
        </TransitionScene>
      </Sequence>
    </AbsoluteFill>
  );
};

export default TransitionDemo;
