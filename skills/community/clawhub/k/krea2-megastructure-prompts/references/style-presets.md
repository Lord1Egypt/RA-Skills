# 风格预设（12 组）

每组给出**可直接拼到提示词末尾的媒介短语** + 适用方向 + 注意事项。
风格短语一般放在 L7 层，紧跟在镜头描述之后。

---

### 1 · 电影概念美术 Cinematic Matte Painting
`cinematic matte painting concept art, epic scale, atmospheric perspective, painterly realism, subtle film grain`
**适用**：通用首选，尤其是建筑与地质巨构。
**注意**：配合 `volumetric haze` 与大气透视效果最佳。

### 2 · 写实摄影 Photorealistic
`photorealistic photograph, shot on a 24mm lens at f/8, natural light, high dynamic range, crisp detail, subtle film grain at ISO 400`
**适用**：自然巨构、机械巨构、需要"可信"的场景。
**注意**：Krea 2 真的理解光圈/焦距/ISO，大胆写具体数值。写 `f/1.4` 会得到浅景深，`85mm` 会长焦压缩，`ISO 3200` 会出高颗粒低照度。

### 3 · 史诗油画 Epic Oil Painting
`epic oil painting, thick impasto brushstrokes, rich glazes, dramatic chiaroscuro, museum-scale canvas, 19th century Romantic landscape tradition`
**适用**：自然巨构、神话题材、崇高感。
**变体**：`Hudson River School influence, sublime scale` / `Caspar David Friedrich mood, solitary figure contemplating the sublime`

### 4 · 3D 渲染 3D Render
`3D render, Octane render, physically based materials, subsurface scattering on the translucent sections, global illumination, crisp ray-traced reflections`
**适用**：生物巨构、机械巨构、需要精确材质的概念设计。
**注意**：可指定 `clay render, untextured grey model` 做纯形体研究。

### 5 · 建筑可视化 Architectural Visualization
`architectural visualization, entourage figures, soft overcast lighting, accurate material rendering, wide-angle corrected perspective, minimal post-processing`
**适用**：建筑巨构的方案表达、体量研究。

### 6 · 废土蓝图 / 工业制图 Wasteland Blueprint
`weathered technical illustration, blueprint linework overlaid on a rendered scene, annotation marks and measurement callouts, grid background, cyan and bone palette, worn paper texture`
**适用**：机械巨构的设定图、世界观资料。

### 7 · 东方水墨 Ink Wash
`traditional East Asian ink wash painting, 水墨, vast negative space, misty voids, sparse brushwork, monochrome with faint mineral pigment, rice paper texture, seal stamp in the corner`
**适用**：自然与超现实巨构。留白本身就是尺度语言——主体只占一角，其余全空。

### 8 · 构成主义海报 Constructivist Poster
`1920s constructivist propaganda poster, bold flat color blocks, hard diagonal composition, geometric sans-serif typography, limited palette of red black and cream, halftone grain`
**适用**：政治/工业巨构的平面化表达。巨构在此风格下会被极端透视夸张。

### 9 · 暗黑奇幻插画 Dark Fantasy Illustration
`dark fantasy illustration, desaturated palette with a single accent color, heavy texture, dramatic rim lighting, intricate silhouette detail, reminiscent of film concept art`
**适用**：生物巨构、废墟巨构、压迫感。

### 10 · 复古版画 /  midpoint 印刷 Retro Print
`vintage mid-century lithograph, limited spot-color separation, halftone dot texture, slight misregistration, aged paper, muted palette`
**适用**：旅游海报式巨构，怀旧感。

### 11 · 热成像 / 科学观测 Specialized Capture
`long-wave infrared thermography, false-color thermal palette, no visible light, scientific survey capture, high contrast between warm and cold masses`
**适用**：需要陌生化处理的巨构，生物巨构尤其震撼。
**变体**：`sonar / LIDAR point cloud visualization, wireframe scan data`

### 12 · 微缩模型 Miniature / Diorama
`photographed scale model diorama, visible seams and paint wear, shallow depth of field with tilt-shift, studio lighting, behind-the-scenes of a film production`
**适用**：刻意做"这是一座模型"的元叙事，适合海报与封面。
**注意**：与巨构的"可信尺度"目标相反，只在用户明确要模型感时用。

---

## 调色速查

| 情绪 | 配色短语 |
|---|---|
| 敬畏 / 神圣 | `warm amber highlights against cool blue shadow` |
| 荒凉 / 废土 | `desaturated ochre and ash grey, dust-choked atmosphere` |
| 恐怖 / 压迫 | `near-monochrome with crushed blacks, single cold cyan accent` |
| 宁静 / 冥想 | `soft pearl and pale jade, low contrast, even overcast light` |
| 科幻 / 冷峻 | `steel blue with sodium orange accents, cold pre-dawn light` |
| 热带 / 生机 | `saturated jade green, coral and vermilion, humid haze` |

## 风格叠加规则

- 一次**只用一组**主风格预设，最多再叠加一个调色短语。
- 媒介词冲突（如 `oil painting` + `photorealistic photograph`）会让结果漂移，不要写。
- 若用户想锁定某个具体画风且能提供参考图 → **优先建议上传 1–10 张风格参考图**，文本只负责描述主体。Krea 2 的风格迁移远比形容词堆砌可靠。
