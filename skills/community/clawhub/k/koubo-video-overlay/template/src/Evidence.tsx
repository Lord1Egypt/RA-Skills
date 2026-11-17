import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";

const clamp = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

// 单张证据图卡片：侧边淡入淡出 + 轻微滑入，白色圆角边框。
// 时长固定 150 帧（5 秒 @30fps）：0-12 淡入，12-138 停留，138-150 淡出。
// w/h 按图片原始比例算（objectFit:cover 不裁切）；x/y 是卡片左上角在画布中的像素坐标。
const EvidenceCard: React.FC<{
  src: string;
  w: number;
  h: number;
  x: number;
  y: number;
}> = ({ src, w, h, x, y }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 12, 138, 150], [0, 1, 1, 0], clamp);
  const slide = interpolate(frame, [0, 14], [26, 0], clamp);
  return (
    <AbsoluteFill style={{ backgroundColor: "transparent" }}>
      <div
        style={{
          position: "absolute",
          left: x,
          top: y,
          width: w,
          height: h,
          opacity,
          transform: `translateX(${slide}px)`,
          backgroundColor: "#ffffff",
          borderRadius: 14,
          padding: 6,
          boxShadow: "0 8px 28px rgba(0,0,0,0.35)",
          boxSizing: "border-box",
        }}
      >
        <Img
          src={staticFile(src)}
          style={{ width: "100%", height: "100%", objectFit: "cover", borderRadius: 9, display: "block" }}
        />
      </div>
    </AbsoluteFill>
  );
};

// 每张证据图一个合成。按口播内容增删 EvN，并在 Root.tsx 注册、pipeline.ps1 加对应渲染+叠加。
// 尺寸针对 544x960 竖屏；换画布尺寸要重算 w/h/x/y。
//
// 摆放两种模式（按用户偏好选）：
// ① 居中盖脸（默认，口播时图是主体）：水平居中 x=(544-w)/2，垂直中心约 y=420 盖住中上部人脸，图放大。
// ② 侧边不挡脸：图缩小放右侧（x≈210-300, y≈250-300, w≈230-320），人脸保留为主体。
// 下面用模式①。要模式②就把 w/h 缩小、x 移到右侧。
export const Ev1: React.FC = () => <EvidenceCard src="img1.png" w={360} h={562} x={92} y={139} />;
export const Ev2: React.FC = () => <EvidenceCard src="img2.png" w={510} h={329} x={17} y={150} />;
export const Ev3: React.FC = () => <EvidenceCard src="img3.png" w={500} h={289} x={22} y={276} />;