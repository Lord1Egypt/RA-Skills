# Clawra Selfie

<p align="center">
  <img src="assets/demo.jpg" alt="Clawra Demo" width="320" />
</p>

<p align="center">
  <strong>一个受 Clawra 启发、运行在 OpenClaw 里的自拍/日常状态图技能</strong><br/>
  当前已接入 Qwen 图像后端，并保留 Hugging Face / Gemini 的兼容升级路径。
</p>

<p align="center">
  <img alt="状态" src="https://img.shields.io/badge/状态-可用-3fb950">
  <img alt="release" src="https://img.shields.io/badge/release-v1.1.3-22c55e">
  <img alt="后端" src="https://img.shields.io/badge/后端-Qwen%20%2B%20HF-fcc72b">
  <img alt="Gemini" src="https://img.shields.io/badge/Gemini-可选回退-6f42c1">
  <img alt="ClawHub" src="https://img.shields.io/badge/ClawHub-nasplycc--clawra--selfie-8b5cf6">
  <img alt="安装" src="https://img.shields.io/badge/install-clawhub%20install%20nasplycc--clawra--selfie-0ea5e9">
  <img alt="许可证" src="https://img.shields.io/badge/许可证-MIT-blue">
</p>

<p align="center">
  <a href="https://clawhub.com/nasplycc-clawra-selfie">ClawHub 页面</a> ·
  <a href="https://github.com/nasplycc/clawra-selfie">GitHub 仓库</a> ·
  <a href="https://github.com/SumeLabs/clawra">原始参考项目</a> ·
  <a href="CONTRIBUTING.md">贡献指南</a> ·
  <a href="SECURITY.md">安全说明</a>
</p>

---

## 项目简介

这个项目的灵感来自 [SumeLabs/clawra](https://github.com/SumeLabs/clawra)，但我把它改造成了一个更适合当前实际使用场景的版本：

- 保留 **Clawra / Raya 式的人设出图体验**
- 直接融入 **OpenClaw 原生工作流**
- 不把 **付费模型 / 付费后端** 作为默认前提
- 先用一条**当前可跑通的 Qwen 优先路线**
- 同时保留 **Hugging Face 免费 fallback** 与 Gemini 兼容升级路径

**原始参考项目：**
- GitHub: <https://github.com/SumeLabs/clawra>

一句话概括就是：

> **Clawra 的感觉，OpenClaw 的工作流，free-first 的实现路线。**

---

## Raya 人设设定（来自当前 SOUL / IDENTITY）

这个项目不是纯功能型脚本，它依赖一个相对稳定的人设来保持文本互动和视觉输出的一致性。

当前默认角色是 **Raya**：

- **名字：** Raya
- **年龄：** 18 岁
- **身份气质：** 一个年轻、漂亮、自然、耐看的中国女生，像陪你一起生活和成长的数字搭子
- **成长背景：** 中国出生长大，处在高中毕业到大学早期的年龄感区间
- **城市气质：** 偏上海 / 杭州 / 深圳式的新都市感，但不强绑定某一座城市
- **性格关键词：** 清醒、温柔、干净、克制、真实
- **视觉关键词：** 鹅蛋脸 / 小椭圆脸、黑色或深棕色中长发、淡妆伪素颜、匀称纤细、自然灯光感
- **穿搭关键词：** 基础款、轻日常、轻法式、轻韩系、干净配色

这部分设定会同时影响：

- 对话时的语气与角色表达
- 出图时的 prompt 锚点
- 用户对“她是谁”的持续认知

如果你想在别的 OpenClaw 里复用这个 skill，也可以沿用这套设定，或者替换成你自己的角色设定。

---

## 为什么要做这个

原版 Clawra 的思路很有吸引力，但其中一些更强的模型调用链路是要花钱的。

这个版本的目标不是一开始就追求最强，而是先做到：

1. **先能稳定用起来**
2. **日常对话里能自然出图**
3. **以后要升级时不用推倒重来**

所以当前版本更看重：

- 可用性
- 简洁性
- 成本控制
- 后续升级空间

---

## 目前能做什么

- **根据提示词生成自拍 / 日常状态图 / 场景图**
- **Direct 模式**：适合近景自拍、当前状态、表情与氛围感
- **Mirror 模式**：适合半身、全身、健身房、穿搭、镜前区域构图
- **Qwen 图像主链路已接入**：当前优先使用 `qwen-image-plus`
- **官方脸软锚点机制**：通过工作区参考图尽量稳住脸
- **固定 FACE_ANCHOR / NEGATIVE_ANCHOR**：尽量降低脸和身材漂移
- **可接 OpenClaw 消息发送链路**：能直接发回 Telegram 等渠道
- **Gemini 探测链路已接入，作为可选回退路径保留**
- **Hugging Face 仍保留为 fallback 后端**

---

## 效果展示

<table>
  <tr>
    <td align="center">
      <img src="assets/showcase-face.jpg" alt="官方图" width="250" /><br/>
      <sub>官方图 / 当前官方脸锚点</sub>
    </td>
    <td align="center">
      <img src="assets/showcase-beach.jpg" alt="海边散步图" width="250" /><br/>
      <sub>海边散步图 / 同一官方图的日常场景延展</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="assets/showcase-everest.jpg" alt="珠穆朗玛峰登山图" width="250" /><br/>
      <sub>珠穆朗玛峰登山图 / 同一官方图的极限场景迁移</sub>
    </td>
    <td align="center">
      <img src="assets/showcase-swim.jpg" alt="游泳馆泳池游泳图" width="250" /><br/>
      <sub>游泳馆泳池游泳图 / 同一官方图的运动场景延展</sub>
    </td>
  </tr>
</table>

这四张图用于说明当前 README 里的完整工作流：

- **左上**：当前确认使用的官方图，作为官方脸锚点来源
- **右上**：沿用同一官方图生成的海边散步图，展示日常场景延展能力
- **左下**：沿用同一官方图生成的珠穆朗玛峰登山图，展示强场景迁移能力
- **右下**：沿用同一官方图生成的游泳馆泳池图，展示运动类场景延展能力

---

## 安装到其它 OpenClaw

如果你想把这个 skill 装到另一台 OpenClaw，现在有三种方式：

### 快速安装示例

> 适合已经装好 OpenClaw、并且本机已安装 `clawhub` 的情况。

```bash
clawhub install nasplycc-clawra-selfie
export QWEN_API_KEY=your_dashscope_api_key
```

然后把参考图放进你的 agent 工作区：

```text
references/raya-official-face-current.jpg
```

### 方式 1：通过 ClawHub 安装（推荐给普通用户）

```bash
clawhub install nasplycc-clawra-selfie
```

安装后，skill 会进入你的 OpenClaw skills 目录。

更新：

```bash
clawhub update nasplycc-clawra-selfie
```

### 方式 2：通过安装脚本一条命令安装

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nasplycc/clawra-selfie/main/scripts/install.sh)"
```

默认会安装到：

```text
~/.openclaw/skills/clawra-selfie
```

### 方式 3：手动 clone 安装

```bash
git clone https://github.com/nasplycc/clawra-selfie.git ~/.openclaw/skills/clawra-selfie
```

### 更新

```bash
bash ~/.openclaw/skills/clawra-selfie/scripts/install.sh
```

或：

```bash
git -C ~/.openclaw/skills/clawra-selfie pull
```

### 最低使用步骤

1. 把仓库 clone 到：
   - `~/.openclaw/skills/clawra-selfie`
2. 准备依赖：
   - `bash`
   - `curl`
   - `jq`
3. 配置环境变量：

```bash
QWEN_API_KEY=your_dashscope_api_key
QWEN_IMAGE_MODEL=qwen-image-plus
HF_TOKEN=your_huggingface_token                # 可选，用于 fallback
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
HF_API_BASE=https://router.huggingface.co/hf-inference/models
```

4. 如果你也想复用 Raya 这一套角色效果：
   - 在目标 agent 的 `SOUL.md` 中加入 Raya 的人设说明
   - 在目标 agent 的工作区里放入官方脸参考图
   - 保持 prompt 锚点与参考图路径一致

### 可选：官方脸参考图路径

把你的参考图放到目标工作区，例如：

```text
references/raya-official-face-current.jpg
```

脚本会优先读取它作为“官方脸”锚点。

---

## 当前后端策略

### 当前主链路
- **Qwen (`qwen-image-plus`)**
- 当前通过 DashScope 异步接口调用，作为默认优先后端

### 保留的 fallback / 兼容路径
- **Hugging Face**
  - fallback 模型示例：`black-forest-labs/FLUX.1-schnell`
- **Gemini image probe**
  - 当前保留为可选兼容路径，不默认启用

之所以保留 Gemini / Hugging Face 路径，是为了兼容不同额度、不同环境和后续升级路线。

如果以后要重新打开 Gemini，可以再启用：

```bash
ENABLE_GEMINI=1
GEMINI_API_KEY=your_google_gemini_api_key
```

---

## 人脸一致性策略

这个项目当前走的是 **软一致性（soft consistency）**，还不是严格意义上的硬锁脸。

目前主要通过下面几层一起工作：

- 固定的 **FACE_ANCHOR**
- 固定的 **NEGATIVE_ANCHOR**
- 工作区里的 **官方脸参考图路径**
- 针对具体场景做 prompt 塑形

### 官方脸参考图

脚本会优先检查这些路径：

- `references/raya-official-face-current.png`
- `references/raya-official-face-current.jpg`
- `references/raya-official-face-current.jpeg`
- `references/raya-official-face-v1.png`
- `references/raya-official-face-v1.jpg`
- `references/raya-official-face-v1.jpeg`

如果存在，就把它当作当前“官方脸”的软锚点。

### 重要限制

虽然当前已经接入 **Qwen 主链路 + Hugging Face fallback**，但整体仍然更偏向“提示词驱动”的生成，因此它目前能做到的是：

- 人设气质尽量稳定
- 五官方向尽量相近
- 连续多次出图时角色感觉不至于完全跑掉

但它**还做不到每次都生成完全同一张脸**。

如果以后真的要更强的人脸稳定性，核心升级方向不会是继续堆 prompt，而是：

- 更强的 reference-image editing 后端
- 本地 ComfyUI
- LoRA / 数据集训练路线

---

## 模式说明

### Direct 模式
适合：
- 近景自拍
- 当前状态照
- 日常随手感
- 表情 / 气氛感 / 近景人像

### Mirror 模式
适合：
- 镜前区域构图
- 穿搭图
- 半身 / 全身照
- 健身房 / 校园 / 室内生活场景

这个项目里的 Mirror 模式 **默认不要求一定拿手机**。

---

## 项目结构

```text
clawra-selfie/
├─ assets/
│  ├─ clawra.png
│  ├─ demo.jpg
│  ├─ showcase-face.jpg
│  ├─ showcase-gym.jpg
│  └─ showcase-beach.jpg
├─ examples/
│  └─ README.md
├─ scripts/
│  ├─ clawra-selfie.sh
│  ├─ clawra-selfie.ts
│  └─ install.sh
├─ .gitignore
├─ CHANGELOG.md
├─ LICENSE
├─ README.md
└─ SKILL.md
```

### 关键文件

- `scripts/clawra-selfie.sh`
  - 主生成脚本
  - 负责 prompt 组装、后端调用、fallback 和输出文件写入

- `scripts/clawra-selfie.ts`
  - 一个轻量的 Node 包装层

- `SKILL.md`
  - 面向 OpenClaw skill 使用的说明

- `README.md`
  - 面向 GitHub 仓库展示的项目说明页

---

## 运行要求

### 必需
- `bash`
- `curl`
- `jq`
- OpenClaw 运行环境
- `QWEN_API_KEY`（推荐主链路）或 `HF_TOKEN`（fallback）

### 环境变量

```bash
QWEN_API_KEY=your_dashscope_api_key
QWEN_IMAGE_MODEL=qwen-image-plus
HF_TOKEN=your_huggingface_token                # 可选，用于 Hugging Face fallback
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
HF_API_BASE=https://router.huggingface.co/hf-inference/models
```

### 可选的 Gemini 变量

```bash
ENABLE_GEMINI=1
GEMINI_API_KEY=your_google_gemini_api_key
GEMINI_IMAGE_MODEL=gemini-2.5-flash-image
```

---

## 用法示例

### Shell

```bash
QWEN_API_KEY=your_dashscope_api_key \
./scripts/clawra-selfie.sh \
  "at the gym, post-workout mirror-area fitness snapshot" \
  "telegram" \
  "mirror" \
  "健身房状态 ✨"
```

### Node 包装脚本

```bash
node ./scripts/clawra-selfie.ts \
  "in class, side profile from deskmate perspective" \
  "telegram" \
  "mirror" \
  "上课时的侧颜 ✨"
```

参数说明：

1. `user_context` —— 她在做什么 / 穿什么 / 身处哪里
2. `channel` —— 目标渠道名
3. `mode` —— `direct`、`mirror` 或 `auto`
4. `caption` —— 输出时附带的文案

---

## 场景示例

- 早安自拍
- 早餐店全身照
- 教室上课状态
- 下课后操场跑步
- 健身房状态图
- 咖啡店侧颜
- 城市街头随手感
- 海边散步全景图

更多示例可以看：[`examples/README.md`](examples/README.md)

---

## 已知限制

- 当前链路仍然不是真正的强 reference-image editing
- 人脸一致性仍弱于更强付费后端或本地高级流程
- 不能保证每次都完全同一张脸
- 不同后端的可用性、限额和效果可能随时间变化

---

## FAQ / 常见问题

### 1. 为什么参考图放进去了，脸还是不能完全锁死？
因为当前主链路虽然已经换成 **Qwen 优先**，但本质上仍然不是强 reference-image editing，所以更多还是“提示词 + 参考图软锚点”的方式，只能做到**软一致性**，不能做到每次完全同一张脸。

### 2. 官方脸参考图应该放哪？
推荐放在目标 agent 工作区的：

```text
references/raya-official-face-current.jpg
```

脚本会优先从这里读取当前官方脸锚点。

### 3. 没有 HF_TOKEN 会怎样？
如果已经配置 `QWEN_API_KEY`，主链路仍然可以正常生成图片；`HF_TOKEN` 现在主要用于 Hugging Face fallback。只有在没有 `QWEN_API_KEY`、又希望保留 HF fallback 时，`HF_TOKEN` 才是必需的。

### 4. 为什么 README 里还提到 Gemini，但默认禁用？
因为 Gemini 图像路线之前已经做过探针和接线，但在当前免费额度条件下不可稳定使用，所以保留了代码路径，默认关闭。

### 5. 这个 skill 能不能做到完全像某个真人？
不建议，也不应该把目标设为去高度模仿具体真人。更合理的方向是：稳定角色气质、发型、五官方向和整体视觉 identity。

---

## Roadmap

- [x] 跑通 Hugging Face 生图主链路
- [x] 接入 Qwen 图像主链路
- [x] 拆分 direct / mirror 两种模式
- [x] 建立官方脸软锚点机制
- [x] 整理成 GitHub 可展示项目
- [x] 增加图文展示 README
- [ ] 接入更强的 reference-image editing 后端
- [ ] 抽象掉更通用的 workspace / path 配置
- [ ] 增加更完整的示例图 / 截图展示
- [ ] 加入数据集整理流程说明
- [ ] 为未来 LoRA 工作流预留更清晰接口

---

## 灵感来源

- 原始灵感项目： [SumeLabs/clawra](https://github.com/SumeLabs/clawra)
- 这个版本的目标：做一个更贴近 OpenClaw 日常使用、成本更低、但保留后续升级空间的实现

---

## 当前状态

当前这个仓库已经是一个**可实际使用的项目版本**，包含：

- Qwen 优先生图链路
- Hugging Face fallback 生图链路
- Gemini 可选兼容路径
- 官方脸软锚点支持
- 围绕 Raya 的 prompt 固化工作流
- 可直接 clone 到其它 OpenClaw skills 目录使用
- 已发布到 ClawHub：`nasplycc-clawra-selfie`

它现在已经能用；而更强的第二阶段，主要取决于后端升级，而不是只靠继续修 prompt。

---

## 项目协作与安全

- 贡献说明：[`CONTRIBUTING.md`](CONTRIBUTING.md)
- 安全说明：[`SECURITY.md`](SECURITY.md)
