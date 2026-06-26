import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";
import type {ExplainerPlan, ExplainerScene, ExplainerStage} from "./scene-types";

const STAGE_COLORS: Record<ExplainerStage, string> = {
  context: "#1a1a2e",
  problem: "#16213e",
  mechanism: "#0f3460",
  benefits: "#0a2647",
  "next-step": "#1a1a2e",
};

const STAGE_ACCENTS: Record<ExplainerStage, string> = {
  context: "#4cc9f0",
  problem: "#f72585",
  mechanism: "#7209b7",
  benefits: "#4361ee",
  "next-step": "#4cc9f0",
};

const SceneCard: React.FC<{scene: ExplainerScene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: {damping: 200, stiffness: 120},
  });

  const fadeOut = interpolate(
    frame,
    [scene.durationInFrames - 15, scene.durationInFrames],
    [1, 0],
    {extrapolateLeft: "clamp", extrapolateRight: "clamp"},
  );

  const accent = STAGE_ACCENTS[scene.stage];

  return (
    <AbsoluteFill
      style={{
        backgroundColor: STAGE_COLORS[scene.stage],
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeOut,
      }}
    >
      {/* Accent bar */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 4,
          background: `linear-gradient(90deg, transparent, ${accent}, transparent)`,
          transform: `scaleX(${entrance})`,
        }}
      />

      {/* Stage label */}
      <div
        style={{
          position: "absolute",
          top: 60,
          left: 80,
          fontSize: 14,
          fontWeight: 600,
          letterSpacing: 3,
          textTransform: "uppercase",
          color: accent,
          opacity: entrance,
          fontFamily: "sans-serif",
        }}
      >
        {scene.stage.replace("-", " ")}
      </div>

      {/* Content */}
      <div
        style={{
          maxWidth: 1200,
          padding: "0 80px",
          transform: `translateY(${interpolate(entrance, [0, 1], [40, 0])}px)`,
          opacity: entrance,
        }}
      >
        <h1
          style={{
            fontSize: 64,
            fontWeight: 800,
            color: "#ffffff",
            lineHeight: 1.1,
            margin: 0,
            fontFamily: "sans-serif",
          }}
        >
          {scene.headline}
        </h1>

        {scene.subheadline && (
          <p
            style={{
              fontSize: 28,
              color: accent,
              marginTop: 20,
              fontWeight: 500,
              fontFamily: "sans-serif",
            }}
          >
            {scene.subheadline}
          </p>
        )}

        <p
          style={{
            fontSize: 20,
            color: "rgba(255,255,255,0.6)",
            marginTop: 24,
            lineHeight: 1.6,
            fontFamily: "sans-serif",
          }}
        >
          {scene.voiceover}
        </p>
      </div>

      {/* CTA for next-step stage */}
      {scene.stage === "next-step" && (
        <div
          style={{
            position: "absolute",
            bottom: 120,
            left: "50%",
            transform: `translateX(-50%) scale(${entrance})`,
            backgroundColor: accent,
            color: "#ffffff",
            fontSize: 28,
            fontWeight: 700,
            padding: "18px 48px",
            borderRadius: 12,
            fontFamily: "sans-serif",
          }}
        >
          {scene.headline}
        </div>
      )}
    </AbsoluteFill>
  );
};

export const ExplainerVideo: React.FC<{plan: ExplainerPlan}> = ({plan}) => {
  let currentFrame = 0;

  return (
    <AbsoluteFill style={{backgroundColor: "#0a0a0a"}}>
      {/* Background music */}
      {plan.musicFile && (
        <Audio src={staticFile(plan.musicFile)} volume={0.2} />
      )}

      {/* Scenes */}
      {plan.scenes.map((scene) => {
        const from = currentFrame;
        currentFrame += scene.durationInFrames;

        return (
          <Sequence
            key={scene.id}
            from={from}
            durationInFrames={scene.durationInFrames}
          >
            <SceneCard scene={scene} />

            {/* Per-scene voiceover */}
            {scene.voiceoverFile && (
              <Audio src={staticFile(scene.voiceoverFile)} volume={1} />
            )}

            {/* Per-scene SFX */}
            {scene.sfxFile && (
              <Audio src={staticFile(scene.sfxFile)} volume={0.35} />
            )}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
