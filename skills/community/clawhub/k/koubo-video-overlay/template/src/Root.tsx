import React from "react";
import { Composition } from "remotion";
import { Ev1, Ev2, Ev3 } from "./Evidence";

// 画布尺寸/帧率必须与原片一致（ffprobe 查）。每张图一个合成，durationInFrames=150（5秒@30fps）。
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="Ev1" component={Ev1} durationInFrames={150} fps={30} width={544} height={960} />
      <Composition id="Ev2" component={Ev2} durationInFrames={150} fps={30} width={544} height={960} />
      <Composition id="Ev3" component={Ev3} durationInFrames={150} fps={30} width={544} height={960} />
    </>
  );
};