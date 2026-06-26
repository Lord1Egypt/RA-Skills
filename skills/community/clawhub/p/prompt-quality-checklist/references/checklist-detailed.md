# 提示词质量检查清单 — 详细说明

本文档是 [SKILL.md](./SKILL.md) 的详细展开，包含：
- 每项检查的深度解释
- 常见错误归类
- 错误 → 正确对比示例
- 自审工作流

---

## 自审工作流

### 每日自审流程（批量生成前）

```
┌─────────────────────────────────┐
│  Step 1: 收集当日所有 prompt     │
│  (从剧本/分镜文档中提取)          │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  Step 2: 逐条跑 10 项检查        │
│  (建议用表格工具批量标注 PASS/FAIL)│
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  Step 3: FAIL 项打回修改        │
│  (记录错误类型)                  │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  Step 4: 修改后重新提交复审      │
│  (直到全部 PASS)                 │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  Step 5: 归档                   │
│  (通过清单 + 错误记录存档)        │
└─────────────────────────────────┘
```

### 单条 prompt 自审流程（30秒速审）

1. 读 prompt 全句
2. 问：时间标注在第一个分句吗？
3. 问：人物和定妆照一致吗？有资产路径吗？
4. 问：场景有≥3个硬质物件锚点吗？
5. 问：光源方向具体吗？用了"自然光"吗？
6. 问：有地面阴影吗？
7. 问：用了 retouching 词汇吗？
8. 问：前景/中景/背景三层完整吗？
9. 问：景别服务于情绪吗？
10. 问：投影方向和光源一致吗？
11. 问：末尾有 [ASSET] 路径标注吗？

---

## 检查项详细说明

---

### ① 日夜景标注 / Day–Night Marking

**级别：** 强制（必过项）

**目的：** AI 对日夜的光线模拟差异极大（色温、对比度、氛围），时间标注是画面基调的第一决定因素。

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 完全无时间标注 | A man walking on the street | Night, a man walking on the wet street |
| 时间标注位置靠后 | A street scene at midnight, a woman in blue | Midnight, a woman in blue standing on a neon-lit street |
| 时间词模糊 | A bright room | Daytime interior, bright room with sunlight from the right |
| 黄昏/黎明混用 | Evening / Dusk 不分 | Dusk, warm orange light at 3200K color temperature |

**错误 → 正确对比：**

❌ A businessman sitting in his office, looking out the window
✅ Night, interior of office_int_003, businessman sitting behind walnut desk, green banker lamp, city lights through blinds

❌ 夜晚，一个女人站在天台上
✅ 深夜，天台顶视图，女人穿红色风衣，背景是城市夜景的灯光

---

### ② 主体描述 / Character Consistency

**级别：** 强制（必过项）

**目的：** AI 短剧要求跨镜头主体一致性。人物外貌、服装、姿态必须锁定，否则会出现"同一角色不同脸"的问题。

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 模糊外貌描述 | A beautiful woman, a handsome man | Woman, mid-30s, black hair in low bun, pale complexion, sharp jawline |
| 服装不具体 | Wearing elegant clothes | White silk qipao with gold embroidery on collar, fitted waist |
| 缺定妆照引用 | — | Character ref: char_heroine_001.png |
| 姿态不锁定 | Reaching out her hand | Right hand slightly raised, palm open, fingers slightly curved |

**错误 → 正确对比：**

❌ A beautiful girl in a red dress
✅ Character ref: heroine_002.png, woman in red silk qipao, right hand touching the earring, hair up in a bun, appearance strictly matching the reference photo

❌ 一个高个子男人，穿着很酷的衣服
✅ Character ref: hero_lead_001.png, male, late 30s, 180cm, black short hair, navy western-style suit, red tie, same face and costume as in reference photo

---

### ③ 空间坐标 / Scene Asset Anchor

**级别：** 强制（必过项）

**目的：** 场景失控是 AI 生图的第二大问题。笼统描述会让 AI 随机生成不同时代/风格的资产，导致镜头之间场景割裂。

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 场景笼统 | A luxury bedroom | Master bedroom of villa_int_001, king-size bed with dark gray linen, floor-to-ceiling window on the left |
| 仅一个物件 | A kitchen | Industrial kitchen, stainless steel counter on the right, overhead lamp above, gas stove on the left |
| 缺空间感描述 | In a park | Wide shot, city park, bare Sycamore tree in the foreground (left 1/3), bench in midground, fountain in background |

**错误 → 正确对比：**

❌ A restaurant scene
✅ Interior of restaurant_loc_004, dimly lit, round mahogany table center, red tablecloth, crystal chandelier above, French window with rain on the right

❌ 发生在咖啡馆
✅ 咖啡馆内景（ref: loc_cafe_007.png），深棕色木质圆桌，咖啡杯在桌面右侧，暖黄色台灯在左侧吧台，手写菜单贴在墙上

---

### ④ 光源方向 / Light Direction

**级别：** 强制（必过项）

**目的：** 光源方向决定了角色的体积感、情绪基调、阴影位置。模糊的光源描述 = 不可控的 AI 生成结果。

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 使用"自然光" | Natural lighting, cinematic | Single light source from camera left at 45°, hard light |
| 光源模糊 | Soft lighting, good lighting | Warm fill light from the right at 90°, intensity 0.7 |
| 允许多个随机光源 | Lit by multiple light sources | Single key light from above at 30°, no fill, high contrast |
| 缺色温描述（夜景重要） | Night scene, street | Night, neon signs on both sides, cold blue-pink mixed lighting, ambient light near zero |

**错误 → 正确对比：**

❌ Soft natural lighting, cinematic atmosphere
✅ Single warm key light from the left at 45°, soft shadow on right side of face, no fill light, cinematic contrast ratio 1:4

❌ 室内场景，光线柔和
✅ Interior day scene, large window light from the right (camera right), sheer curtains diffusing light, soft shadows on floor, color temperature 5600K

---

### ⑤ 接触阴影 / Ground Contact Shadow

**级别：** 强制（必过项）

**目的：** 地面阴影是角色"接地"的基本视觉证据。没有地面阴影的人物在竖屏叙事中会显得漂浮，破坏空间真实感。

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 完全不提阴影 | A woman standing on the grass | Woman standing on the grass lawn, dark ground shadow directly beneath feet |
| 阴影位置错误 | Shadow to the left of feet | Shadow stretching 1m to the right, matching light source position |
| 阴影不具体 | With a shadow | Hard shadow on the wooden floor, 0.5m length, slight blur on edges |
| 特写镜头跳过（误区） | Extreme close-up, no floor visible (excuse) | Even in close-up, foreground fingers cast subtle shadow on cheek (touch shadow) |

**错误 → 正确对比：**

❌ Full body shot of a woman standing on the beach
✅ Full body shot, woman standing on wet sand, hard shadow directly beneath feet, shadow stretching 2m to the left, golden hour light from the right

❌ 特写镜头不需要阴影
✅ Close-up, woman's face, a strand of hair casting a thin shadow across her cheekbone, touch shadow reinforcing proximity and intimacy

---

### ⑥ 质感统一 / Material Consistency

**级别：** 强制（必过项）

**目的：** Retouching 类词汇会触发 AI 的"美颜/后期"生成模式，产生不真实的皮肤质感、过度磨皮、或材质属性矛盾（哑光+光泽叠加）的画面。

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 皮肤磨皮描述 | Porcelain smooth skin, flawless skin | Realistic skin texture, visible pores, natural skin oil sheen on T-zone |
| 眼部描述矛盾 | Matte eyeshadow, glossy eyelids | Semi-matte eyeshadow, satin finish eyelids |
| 混用质感词 | Soft lighting, hard metallic texture | Consistent material finish: matte metal frame, frosted glass panel |
| 过度描述皮肤 | Pale white glowing skin, ethereal glow | Fair complexion, natural skin undertone, no artificial glow |

**错误 → 正确对比：**

❌ Porcelain smooth skin, beautiful eyes, glossy lips
✅ Realistic skin texture, visible pores on cheeks, natural matte finish, semi-matte lips with slight natural shine

❌ 皮肤像瓷器一样光滑细腻
✅ 真实皮肤纹理，面部毛孔可见，自然肤色，高光自然分布在鼻梁和颧骨

---

### ⑦ 三层纵深 / Three-Layer Depth

**级别：** 强制（必过项）

**目的：** 竖屏画面空间有限，但纵深是叙事层次的基础。没有纵深的镜头在 AI 视频中会显得"扁平"，缺乏电影院级别的空间感。

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 仅中景，无前景/背景 | Character in center frame | Medium shot, character in midground, blurred window frame in foreground (left edge), bookshelf in background (right wall) |
| 前景/背景与中景空间矛盾 | Character in room but books floating in air | Foreground: chair back edge in blur; Midground: woman seated; Background: window with curtains |
| 仅用虚化代替纵深（不足） | Background bokeh, blurred | Foreground: rain drops on lens edge; Midground: character; Background: neon-lit street, shallow DOF |

**错误 → 正确对比：**

❌ Close-up of a woman's face in a dark room
✅ Close-up, woman's face in midground, a thin strand of hair drifting in the foreground (very shallow DOF, hair slightly out of focus), dim candle light in the deep background (right corner), three distinct depth layers

❌ 中景，女人站在房间里
✅ 中景，女人站在画面中央偏左，前景左侧是半虚化的铁门边缘，背景是深纵深的走廊尽头的光亮，三层纵深物理合理

---

### ⑧ 景别对应 / Shot Type Matches Emotion

**级别：** 强制（必过项）

**目的：** 景别不是随机选择。不同景别触发观众不同的心理反应。选择错误景别会让镜头叙事力度打折甚至反向。

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 情绪压抑却用特写 | Character in despair, extreme close-up face | Wide shot, character tiny in vast empty frame, vastness amplifying despair |
| 力量展示用远景 | Heroic moment, wide shot | Low angle medium shot, character dominant in frame, power and dominance |
| 亲密场景用远景 | Intimate conversation, wide shot | Medium close-up, two characters in profile, shallow DOF isolating them |
| 建立镜头后无过渡直接切特写 | Establishing shot → extreme close-up | Establishing shot → medium shot → close-up (gradual tightening) |

**景别 → 情绪对应速查表：**

| 景别 | 触发情绪 | 适用场景 |
|------|---------|---------|
| Extreme Wide / 大远景 | 孤独、渺小、命运感、环境压迫 | 开场建立、命运揭示 |
| Wide / 远景 | 叙事交代、角色与环境关系 | 场景引入 |
| Medium Wide / 全景 | 动作完整性、群体关系 | 动作戏、群戏 |
| Medium / 中景 | 叙事主力景别、角色行动 | 大部分叙事镜头 |
| Medium Close-up / 中近景 | 情感对话、反应镜头 | 对话场景 |
| Close-up / 特写 | 情感爆发、关键道具 | 情绪高点 |
| Extreme Close-up / 大特写 | 心理极致、紧张感 | 关键细节、道具特写 |

**错误 → 正确对比：**

❌ A man standing in the rain, close-up shot
✅ Medium wide shot, man in rain, tiny figure against the gray sky, vastness reinforcing his despair and isolation

❌ 两人深情对视，远景
✅ Medium close-up, two characters in profile, faces 30cm apart, shallow DOF, foreheads almost touching, intimacy and tension

---

### ⑨ 投影方向 / Shadow Direction Consistency

**级别：** 强制（必过项）

**目的：** 投影方向必须与光源方向物理一致。这是 AI 画面"穿帮"最高发的细节之一——AI 有时会生成方向矛盾的阴影。

**检查逻辑：**

```
光源位置 → 推导投影位置 → 对照 prompt 描述是否一致
```

| 光源位置 | 正确投影位置 |
|---------|------------|
| 左侧 45° | 阴影投向右前方 |
| 右侧 45° | 阴影投向左前方 |
| 正上方 | 阴影在正下方（短而实） |
| 后侧高位 | 阴影投向前方（轮廓光） |
| 低位侧面 | 阴影拉长，对侧面部大面积暗 |

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 光源和投影方向相反 | Light from the left, shadow on the left | Light from the left at 45°, shadow stretching to the right |
| 夜景缺投影 | Night scene, neon lights | Night, cold blue light from left, long warm shadow on the right (neon bounce) |
| 投影长度不描述 | With shadow | Hard shadow, 1.5m length, slight blur at edges |

**错误 → 正确对比：**

❌ Warm light from the left at 45°, soft shadow on the left side
✅ Warm key light from the left at 45°, hard shadow stretching 1.5m to the right of the character, shadow angle matches light angle

❌ 右侧打光，角色左边有阴影
✅ 右侧单光源45°照射，角色右侧身体阴影投向左侧地面，阴影边缘柔和，投影角度与光源方向一致

---

### ⑩ 资产锚点 / Asset Path Annotation

**级别：** 强制（必过项）

**目的：** AI 短剧是资产密集型创作。每个镜头的资产（角色、场景、道具、服装）必须有路径可查，确保跨镜头一致性 + 方便后期复审。

**标准格式：**

```
[ASSET] character: [文件名.png] | location: [文件名.png] | prop: [文件名.png] | costume: [文件名.png]
```

**说明：**
- `character`: 该镜头出现的角色定妆照
- `location`: 场景参考图（若为纯文字描述场景则标注 "text_only"）
- `prop`: 重要道具（若无语义重要道具则标注 "none"）
- `costume`: 若与 character ref 中的服装相同则标注 "same_as_char_ref"

**常见错误类型：**

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 完全无资产标注 | — | [ASSET] character: heroine_001.png \| location: loc_temple_ext_01.png |
| 资产路径不完整 | [ASSET] char: heroine_001 | [ASSET] character: heroine_001.png \| location: loc_roof_access.png \| prop: none |
| 路径格式不统一 | char: heroine / ASSET: char_hero / asset: hero | [ASSET] 统一格式，所有路径均在同一行 |
| 使用网络链接（不稳定） | location: https://xxx.jpg | 全部使用本地相对路径或项目资产库路径 |

**错误 → 正确对比：**

❌ A warrior in a dark forest
✅ Dark forest clearing, warrior in worn armor, longsword at hip, fog in background
[ASSET] character: warrior_male_001.png | location: forest_dark_001.png | prop: weapon_sword_002.png | costume: armor_worn_001.png

❌ 天台场景，女人穿红裙
✅ 深夜，天台顶视图，城市夜景背景，女人红色丝绸长裙，风吹起裙角
[ASSET] character: heroine_suit_001.png | location: loc_rooftop_001.png | prop: none | costume: cost_red_silk_001.png

---

## 高频 FAIL 类型排行（自审统计用）

以下是最常见的 10 项不合格原因，按频率排序。制作 prompt 时优先规避：

1. **④ 光源方向** — "自然光"出现率最高
2. **① 日夜景标注** — 时间标注缺失或位置靠后
3. **⑩ 资产锚点** — 路径缺失或格式不统一
4. **② 主体描述** — 定妆照引用缺失，主体模糊
5. **③ 空间坐标** — 场景过于笼统
6. **⑤ 接触阴影** — 地面阴影完全未提
7. **⑦ 三层纵深** — 仅中景，无前景/背景
8. **⑥ 质感统一** — retouching 词汇出现
9. **⑨ 投影方向** — 光源和阴影方向矛盾
10. **⑧ 景别对应** — 景别和情绪目标不匹配

---

## 错误记录模板

用于归档每次审查的 FAIL 记录：

```
## 错误记录 — [日期]

**镜头编号：** SCENE_XXX
**Prompt 原文：** [...]
**不合格项：** ④光源方向、⑩资产锚点
**错误类型：** 使用"自然光"描述；资产路径缺失
**修改后 Prompt：** [...]
**复审结果：** PASS
**教训：** 夜景光源必须写具体方向和色温，不能用"自然光"
```

---

## 参考资源

- SKILL.md — 完整使用说明和快速参考卡
- 本文档 — 详细检查项说明及完整错误/正确示例
