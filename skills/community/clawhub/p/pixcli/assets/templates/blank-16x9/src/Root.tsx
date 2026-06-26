import React from "react";
import {Composition} from "remotion";
import {BlankVideo} from "./BlankVideo";

export const Root: React.FC = () => {
  return (
    <Composition
      id="BlankVideo"
      component={BlankVideo}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
