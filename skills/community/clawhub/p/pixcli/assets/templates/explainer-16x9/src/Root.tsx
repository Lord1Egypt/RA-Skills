import React from "react";
import {Composition} from "remotion";
import {ExplainerVideo} from "./ExplainerVideo";
import {samplePlan} from "./sample-plan";

export const Root: React.FC = () => {
  const totalFrames = samplePlan.scenes.reduce(
    (sum, s) => sum + s.durationInFrames,
    0,
  );

  return (
    <Composition
      id="ExplainerVideo"
      component={ExplainerVideo}
      durationInFrames={totalFrames}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{plan: samplePlan}}
    />
  );
};
