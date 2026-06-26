import { AbsoluteFill, Sequence, useVideoConfig, interpolate, useCurrentFrame, Easing } from "remotion";
import { FadeIn } from "../components/FadeIn";
import { SlideIn } from "../components/SlideIn";
import { ScaleIn } from "../components/ScaleIn";
import { Typewriter } from "../components/Typewriter";
import { WordHighlight } from "../components/WordHighlight";

/**
 * 产品特性数据
 */
interface ProductFeature {
  title: string;
  description: string;
  icon: string;
}

const features: ProductFeature[] = [
  { title: "Fast", description: "Lightning fast performance", icon: "⚡" },
  { title: "Secure", description: "Enterprise-grade security", icon: "🔒" },
  { title: "Scalable", description: "Grow without limits", icon: "📈" },
];

/**
 * Logo 场景
 */
const LogoScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <ScaleIn duration={30} useSpring springPreset="bouncy">
        <div
          style={{
            width: 200,
            height: 200,
            borderRadius: 40,
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <span style={{ fontSize: 100 }}>P</span>
        </div>
      </ScaleIn>
    </AbsoluteFill>
  );
};

/**
 * 标题场景
 */
const TitleScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <FadeIn duration={20}>
        <h1
          style={{
            fontSize: 100,
            color: "#ffffff",
            fontFamily: "Arial, sans-serif",
            margin: 0,
            textAlign: "center",
          }}
        >
          <WordHighlight
            text="Product Name"
            highlightWords={["Product"]}
            highlightColor="#667eea"
            startFrame={20}
            wordDuration={30}
          />
        </h1>
      </FadeIn>
      <div style={{ marginTop: 30 }}>
        <FadeIn duration={20} startFrame={15}>
          <p
            style={{
              fontSize: 40,
              color: "#888888",
              fontFamily: "Arial, sans-serif",
              margin: 0,
            }}
          >
            The future of productivity
          </p>
        </FadeIn>
      </div>
    </AbsoluteFill>
  );
};

/**
 * 问题场景
 */
const ProblemScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
      }}
    >
      <FadeIn duration={20}>
        <h2
          style={{
            fontSize: 60,
            color: "#ff6b6b",
            fontFamily: "Arial, sans-serif",
            margin: 0,
            textAlign: "center",
          }}
        >
          The Problem
        </h2>
      </FadeIn>
      <div style={{ marginTop: 40, textAlign: "center" }}>
        <Typewriter
          text="Traditional tools are slow, complicated, and expensive."
          textStyle={{ fontSize: 36, color: "#ffffff" }}
          startFrame={20}
          charsPerFrame={0.5}
        />
      </div>
    </AbsoluteFill>
  );
};

/**
 * 解决方案场景
 */
const SolutionScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
      }}
    >
      <FadeIn duration={20}>
        <h2
          style={{
            fontSize: 60,
            color: "#4ecdc4",
            fontFamily: "Arial, sans-serif",
            margin: 0,
            textAlign: "center",
          }}
        >
          Our Solution
        </h2>
      </FadeIn>
      <div style={{ marginTop: 40, textAlign: "center" }}>
        <Typewriter
          text="Simple. Fast. Powerful. Affordable."
          textStyle={{ fontSize: 36, color: "#ffffff" }}
          startFrame={20}
          charsPerFrame={0.5}
        />
      </div>
    </AbsoluteFill>
  );
};

/**
 * 特性场景
 */
const FeatureScene: React.FC<{ feature: ProductFeature; index: number }> = ({
  feature,
  index,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const startFrame = 10;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <SlideIn direction="left" duration={25} startFrame={startFrame}>
        <div style={{ textAlign: "center" }}>
          <div style={{ fontSize: 120 }}>{feature.icon}</div>
          <h2
            style={{
              fontSize: 80,
              color: "#667eea",
              fontFamily: "Arial, sans-serif",
              margin: "20px 0",
            }}
          >
            {feature.title}
          </h2>
          <p
            style={{
              fontSize: 36,
              color: "#888888",
              fontFamily: "Arial, sans-serif",
              margin: 0,
            }}
          >
            {feature.description}
          </p>
        </div>
      </SlideIn>
    </AbsoluteFill>
  );
};

/**
 * CTA 场景
 */
const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();

  const buttonScale = interpolate(
    frame,
    [20, 40],
    [0.8, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.elastic(1),
    }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <FadeIn duration={20}>
        <h2
          style={{
            fontSize: 60,
            color: "#ffffff",
            fontFamily: "Arial, sans-serif",
            margin: 0,
            textAlign: "center",
          }}
        >
          Get Started Today
        </h2>
      </FadeIn>
      <div style={{ marginTop: 50 }}>
        <ScaleIn duration={20} startFrame={20}>
          <div
            style={{
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              padding: "20px 60px",
              borderRadius: 50,
              transform: `scale(${buttonScale})`,
            }}
          >
            <span
              style={{
                fontSize: 36,
                color: "#ffffff",
                fontFamily: "Arial, sans-serif",
                fontWeight: "bold",
              }}
            >
              Try Free for 30 Days
            </span>
          </div>
        </ScaleIn>
      </div>
    </AbsoluteFill>
  );
};

/**
 * ProductDemo - 产品演示视频模板
 *
 * 一个完整的产品演示视频模板，包含以下场景：
 * 1. Logo 展示
 * 2. 产品名称和标语
 * 3. 问题陈述
 * 4. 解决方案介绍
 * 5. 产品特性展示（多个）
 * 6. 行动号召（CTA）
 */
export const ProductDemo: React.FC = () => {
  const { fps } = useVideoConfig();

  // 每个场景的持续时间（秒）
  const sceneDuration = 3;
  const sceneFrames = sceneDuration * fps;

  // 特性场景的总时间
  const featureSceneCount = features.length;
  const featureTotalFrames = featureSceneCount * sceneFrames;

  return (
    <AbsoluteFill>
      {/* 场景1: Logo */}
      <Sequence from={0} durationInFrames={sceneFrames}>
        <LogoScene />
      </Sequence>

      {/* 场景2: 标题 */}
      <Sequence from={sceneFrames} durationInFrames={sceneFrames}>
        <TitleScene />
      </Sequence>

      {/* 场景3: 问题 */}
      <Sequence from={sceneFrames * 2} durationInFrames={sceneFrames}>
        <ProblemScene />
      </Sequence>

      {/* 场景4: 解决方案 */}
      <Sequence from={sceneFrames * 3} durationInFrames={sceneFrames}>
        <SolutionScene />
      </Sequence>

      {/* 场景5-7: 特性展示 */}
      {features.map((feature, index) => (
        <Sequence
          key={feature.title}
          from={sceneFrames * (4 + index)}
          durationInFrames={sceneFrames}
        >
          <FeatureScene feature={feature} index={index} />
        </Sequence>
      ))}

      {/* 场景8: CTA */}
      <Sequence from={sceneFrames * (4 + featureSceneCount)} durationInFrames={sceneFrames}>
        <CtaScene />
      </Sequence>
    </AbsoluteFill>
  );
};

export default ProductDemo;
