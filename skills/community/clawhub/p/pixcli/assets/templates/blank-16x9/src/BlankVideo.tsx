import React from "react";
import {AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig} from "remotion";

export const BlankVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  const scale = spring({
    frame,
    fps,
    config: {damping: 200, stiffness: 100},
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
          color: "#ffffff",
          fontSize: 48,
          fontWeight: 700,
          fontFamily: "sans-serif",
        }}
      >
        Your Video Starts Here
      </div>
    </AbsoluteFill>
  );
};
