import { Composition } from "remotion";
import { HelloDemo } from "./compositions/HelloDemo";
import { AnimationDemo } from "./compositions/AnimationDemo";
import { TransitionDemo } from "./compositions/TransitionDemo";
import { ProductDemo } from "./compositions/ProductDemo";
import { TitleSequence } from "./compositions/TitleSequence";
import { DataVisualization } from "./compositions/DataVisualization";

/**
 * Remotion Root - 所有视频组合的入口文件
 */
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="HelloDemo"
        component={HelloDemo}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="AnimationDemo"
        component={AnimationDemo}
        durationInFrames={660}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="TransitionDemo"
        component={TransitionDemo}
        durationInFrames={540}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ProductDemo"
        component={ProductDemo}
        durationInFrames={720}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="TitleSequence"
        component={TitleSequence}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="DataVisualization"
        component={DataVisualization}
        durationInFrames={480}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
