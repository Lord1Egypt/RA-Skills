import {Composition} from "remotion";
import script from "../script.json";
import {PaperCollageVideo} from "./video";

const durationInFrames = script.scenes.reduce((total, scene) => total + scene.durationInFrames, 0);

export const RemotionRoot = () => <Composition id="PaperCollageVideo" component={PaperCollageVideo} durationInFrames={durationInFrames} fps={script.composition.fps} width={script.composition.width} height={script.composition.height}/>;
