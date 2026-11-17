import {AbsoluteFill, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame} from "remotion";
import script from "../script.json";

type Role = "primary" | "secondary" | "tertiary" | "foreground";
type Layer = {src: string; role: Role; x: number; y: number; width: number; delay: number; z: number; from: "left" | "right" | "bottom"};

const motion = {primary: {distance: 78, rise: 55, scale: .86}, secondary: {distance: 58, rise: 38, scale: .9}, tertiary: {distance: 38, rise: 22, scale: .95}, foreground: {distance: 50, rise: 30, scale: .92}};
const filter = "drop-shadow(4px 0 #f5eedc) drop-shadow(-4px 0 #f5eedc) drop-shadow(0 4px #f5eedc) drop-shadow(0 18px 9px rgba(20,15,12,.32))";

const Cutout = ({layer}: {layer: Layer}) => {
  const frame = useCurrentFrame();
  const local = frame - layer.delay;
  const enter = interpolate(local, [0, 14], [0, 1], {easing: Easing.bezier(.16, 1, .3, 1), extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const setting = motion[layer.role];
  const side = layer.from === "left" ? -1 : layer.from === "right" ? 1 : 0;
  const bob = local > 14 ? Math.sin((local - 14) / 11) * 3 : 0;
  return <Img src={staticFile(layer.src)} style={{position: "absolute", left: layer.x, top: layer.y, width: layer.width, zIndex: layer.z, opacity: enter, scale: interpolate(enter, [0, 1], [setting.scale, 1]), translate: `${side * (1 - enter) * setting.distance}px ${layer.from === "bottom" ? (1 - enter) * setting.rise + bob : bob}px`, filter}}/>;
};

const Scene = ({scene}: {scene: typeof script.scenes[number]}) => {
  const frame = useCurrentFrame();
  const push = interpolate(frame, [0, scene.durationInFrames], [1, 1.012], {extrapolateRight: "clamp"});
  return <AbsoluteFill style={{overflow: "hidden", background: "#201510"}}>
    <Img src={staticFile(scene.background)} style={{width: "100%", height: "100%", objectFit: "cover", scale: push}}/>
    {scene.layers.map((layer) => <Cutout key={`${layer.src}-${layer.x}-${layer.y}`} layer={layer as Layer}/>) }
    <div style={{position: "absolute", zIndex: 20, bottom: 32, left: 75, right: 75, padding: "13px 28px", textAlign: "center", color: "#fbf1db", background: "rgba(74,22,18,.68)", borderRadius: 16, fontFamily: "serif", textShadow: "0 3px 0 #5c1d1c"}}><div style={{fontSize: 52, fontWeight: 800}}>{scene.caption.title}</div><div style={{fontSize: 25, marginTop: 6}}>{scene.caption.subtitle}</div></div>
  </AbsoluteFill>;
};

export const PaperCollageVideo = () => {
  let offset = 0;
  const scenes = script.scenes.map((scene) => {
    const from = offset;
    offset += scene.durationInFrames;
    return <Sequence key={scene.id} from={from} durationInFrames={scene.durationInFrames}><Scene scene={scene}/></Sequence>;
  });
  return <AbsoluteFill>{scenes}</AbsoluteFill>;
};
