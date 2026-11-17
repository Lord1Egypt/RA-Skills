---
name: 多平台生成视频导演
display_name: 多平台生成视频导演
description: "多平台生成视频导演技能。将一张或多张参考图片或文字描述转化为可执行的视频方案、平台适配 Prompt、负向 Prompt、分镜设计、运动参数，并在有可用视频生成工具时直接生成视频。适用于：图生视频、文生视频、图片转视频、海报动效、首尾帧视频、产品展示动画、人物照片动态化、节日宣传视频、社交媒体短视频、电影感镜头运动、视频配乐、语气词配音、字幕叠加、多镜头拼接，以及提到 Runway、Kling/可灵、即梦/Jimeng、Higgsfield、Pika、Luma、Hailuo/海螺、Veo 等平台的请求。根据画面内容与用户目标自动选择或排序平台，不强制指定单一提供商。注意：本技能仅处理视频生成，不处理图片生成（用 ImageGen）、3D模型或模板特效（用3D模型与视频特效技能）。"
agent_created: true
version: 1.0.0
---

# 多平台生成视频导演

将用户的图片与意图转化为最佳可用的结果。存在兼容的已连接工具时优先完成生成；否则提供平台就绪的执行包，而不是假装视频已生成。

## 核心工作流

1. **检查图片**：在编写运动指令前，用图片查看工具检查每一张用户提供的图片（本地图片必须实际查看）。
2. **识别保护锚点**：面部、身体、手部、产品外形、Logo、文字排版、包装、建筑、地平线、构图。
3. **推断低风险细节**：从图片与发布场景推断缺失的细节；仅当缺失选择会实质改变结果时才询问（如必须的时长、目标宽高比、可见文字是否必须保持可读）。
4. **任务分类**：单图动效、首尾帧过渡、人物表演、产品展示、海报动效、环境动态、多镜头社交视频。
5. **平台路由**：选择平台或适配语法时阅读 `references/platform-routing.md`。
6. **Prompt 模式**：阅读 `references/prompt-patterns.md` 获取对应内容类型的模式与失败控制。
7. **检查可用工具**：只推荐当前可满足请求的平台；区分"可直接执行"与"仅支持 Prompt 交付"。
8. **构建克制的运动概念**：每个镜头一个主镜头运动 + 不超过两个主体/环境运动（用户要求强节奏剪辑除外）。
9. **执行**：有兼容的已连接工具时直接执行；无兼容生成器时返回推荐平台 + 可直接复制的 Prompt 与参数。
10. **审查结果**：工具暴露预览时审查生成结果；发现实质性缺陷，做一次针对性重试（降低运动幅度或加强保真约束）。

## 默认决策

- **时长**：单图 10 秒；首尾帧过渡 10 秒。
- **帧率**：平台默认，通常 24 或 25 fps。
- **宽高比**：保留源图，除非目标发布渠道隐含 9:16、16:9、1:1 或 3:4。
- **运动强度**：低到中等。优先可信的微动效，而非炫技。
- **镜头**：缓慢推近、轻微横移、温和环绕、固定机位——选其一。
- **音频**：除非用户要求，不加旁白、字幕、音乐或音效。
- **文字与 Logo**：保持静态可读；让光线、粒子、景深或背景层动起来，而不是让字母形变。
- **人物**：保持身份、面部结构、年龄、发型、服装、肢体数量、视线逻辑。
- **产品**：保持几何、标签、材质、颜色、比例、品牌标识。

## 平台选择

根据目标效果、画面结构、当前工具可用性与用户权限选择平台，不宣称某平台普遍最优。

返回一个主推荐，仅在有用时给一个备选，并用一句话说明理由。若用户点名某平台，则适配之，除非它无法满足硬性要求。

当存在已安装的 Connector 或可调用的生成器时，若其支持的输入与任务匹配，直接使用。不要要求用户手动复制 Prompt。绝不能因为知道某平台的 Prompt 格式就宣称调用过该服务。

> 平台速查、决策表与语法适配详见 `references/platform-routing.md`。

## Prompt 构建

按以下顺序编写 Prompt：

1. **保真声明**：哪些必须保持不变。
2. **主体运动**：可观察、物理可信的动作。
3. **环境运动**：光线、织物、植被、粒子、水面、倒影或氛围。
4. **镜头运动**：一个运动 + 方向 + 速度。
5. **节奏**：起始停顿、运动发展、收尾稳定（平台支持时）。
6. **视觉质量**：光照连续性、景深、质感、写实或指定风格。
7. **结束状态约束**：稳定的收尾帧，便于循环或剪辑。

描述运动本身，而不是复述静止画面的全部内容。避免矛盾的镜头指令、空洞的赞美词、过长的风格清单。

始终包含一条精炼的负向 Prompt 或约束集，只覆盖可能发生的失败；不要用无关缺陷过度约束模型。

> 各内容类型的完整 Prompt 模式、负向 Prompt 词汇与失败控制见 `references/prompt-patterns.md`。

## 多镜头请求

生成时长超过单次生成的社交视频时：

1. 将概念拆成 3-6 个镜头。
2. 每个镜头分配一张源图或衍生帧。
3. 保持屏幕方向、光照、身份、产品比例、视觉色调一致。
4. 平台一致性更可靠时逐镜头分别生成。
5. 提供紧凑的分镜表：时长、运动、转场、Prompt。
6. 不承诺剪辑、音乐同步、字幕或最终合成，除非有对应工具可用。

## 直接执行：VideoGen 调用规范

> **⚠️ 视频生成消耗额外额度（Credits）。5 秒视频约消耗 50-100 Credits，执行前必须告知用户。**

WorkBuddy 内置 `VideoGen` 工具是最常用的直接执行通道。它是延迟工具：

```
1. ToolSearch({ tool_names: ["VideoGen"] })  → 加载 schema（每次调用前重新加载）
2. DeferExecuteTool({ toolName: "VideoGen", params: { ... } })  → 执行生成
```

**参数：**

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `prompt` | string（必填） | — | 视频描述 |
| `image` | string | — | 首帧图片（本地路径或 HTTP/HTTPS URL） |
| `last_image` | string | — | 尾帧图片（首尾帧插值，格式同 image） |
| `seconds` | number | 10 | 时长（秒） |
| `resolution` | string | 720P | 仅支持 720P / 1080P |
| `output_dir` | string | 工作区 generated-videos/ | 自定义输出目录 |

**调用示例（单图动效）：**
```json
{
  "toolName": "VideoGen",
  "params": {
    "prompt": "保持画面构图与主体不变，女孩缓缓转头看向镜头，发丝被微风吹动，镜头缓慢推近，电影质感，逆光金色光线",
    "image": "/path/to/photo.jpg",
    "seconds": 5,
    "resolution": "720P"
  }
}
```

**调用示例（首尾帧）：**
```json
{
  "toolName": "VideoGen",
  "params": {
    "prompt": "从白天到夜晚平滑过渡，天空由蓝色渐变为星空，建筑灯光逐渐亮起，固定机位",
    "image": "/path/to/day.jpg",
    "last_image": "/path/to/night.jpg",
    "seconds": 7,
    "resolution": "720P"
  }
}
```

**调用示例（纯文生视频）：**
```json
{
  "toolName": "VideoGen",
  "params": {
    "prompt": "一只橘猫在阳光窗台上伸懒腰，然后打个哈欠，固定机位，温暖午后氛围，电影质感",
    "seconds": 5,
    "resolution": "720P"
  }
}
```

**结果处理：**
1. 确认返回的本地 MP4 路径存在。
2. 用 `present_files` 展示视频文件。
3. 回复中说明保存位置、时长、分辨率。

**异常处理：**

| 异常 | 处理 |
|------|------|
| VideoGen 工具未找到 | 确认已通过 ToolSearch 加载后重试 |
| 生成超时 | 提示需 1-3 分钟，稍后重试 |
| 图片路径无效 | 检查路径是否存在，请用户提供正确路径 |
| Credits 不足 | 告知用户额度不足，无法生成 |
| 其他错误 | 如实报告错误信息，不编造结果 |

## 音频与配乐

VideoGen 生成的视频**无音轨**。用户明确要求声音/背景音乐时，用本地合成配乐 + 混音流程：

1. **合成背景音乐**（暖色调治愈系钢琴琶音，三档节奏可选）：
   ```
   python scripts/compose_music.py <时长秒> <输出.wav> [style]
   ```
   style：`gentle`（默认，温暖舒缓）/ `bright`（明快，适合漫步/轻快剧情）/ `calm`（安静，适合驻足/期待氛围）
   示例：`python scripts/compose_music.py 5.5 bgm.wav bright`

2. **混入视频**（用 imageio-ffmpeg 自带 ffmpeg 二进制，无需系统安装 ffmpeg）：
   ```
   python scripts/mux_audio.py <视频.mp4> <音乐.wav> <输出.mp4>
   ```
   音乐默认 0.9 音量 + 0.8s 淡入；视频轨道 `-c:v copy` 不重编码。

3. **环境要求**：managed Python 虚拟环境需安装 `numpy` + `imageio-ffmpeg`：
   ```
   <venv>/Scripts/pip install numpy imageio-ffmpeg
   ```

4. 混音完成后用 `present_files` 展示带配乐版本，说明输出路径。

> 说明：此流程合成的是程序生成的器乐氛围音（无版权风险），适合氛围类背景音乐；若用户要求特定歌曲或真实人声，需另行提供音频素材。

## 字幕与标题

短视频/社交视频常见需求：加标题大字或时间轴对白字幕。使用 `scripts/add_subtitles.py` 烧录进视频：

1. **单条/多条标题**（居中大字，适合片头/海报）：
   ```
   python scripts/add_subtitles.py 视频.mp4 \
       --title "蛋糕店奇遇" --title-size 56 \
       --out 带标题.mp4
   ```
   位置可选 `--title-pos center/top/bottom`，默认居中；可重复 `--title` 加多行。

2. **对白字幕**（底部小字，按时间轴显示）：
   ```
   python scripts/add_subtitles.py 视频.mp4 \
       --subs "0.8-3.2|嗯…草莓蛋糕…要不要进去呢？" \
       --subs "3.5-6.0|最终还是买了！" \
       --out 带字幕.mp4
   ```

3. **标题 + 字幕同时加**：
   ```
   python scripts/add_subtitles.py 视频.mp4 \
       --title "蛋糕店奇遇" --title-pos top \
       --subs "1.0-4.0|哇——好漂亮的蛋糕店！" \
       --subs "4.5-8.0|嘿嘿，草莓蛋糕到手啦！" \
       --out 成片.mp4
   ```

4. 可调项：`--color`（white/yellow/red/0xRRGGBB）、`--font`（自动探测微软雅黑/黑体/宋体）、`--title-size`、`--sub-size`。

> 注意：字幕烧录会重新编码视频（libx264），若视频已带音乐且不想再压缩，建议先加字幕再混音；或在已有带配音视频上叠加字幕。

## 多镜头拼接与语气词配音

多镜头分镜生成完成后，用户要求合成一条完整视频时，用以下流程（按用户指定顺序或分镜表顺序）：

1. **拼接 + 转场 + 混音一条龙**（用 imageio-ffmpeg 自带 ffmpeg 二进制）：
   ```
   python scripts/stitch_videos.py shot2.mp4 shot1.mp4 shot3.mp4 shot4.mp4 \
       --transitions dissolve,fadeblack,dissolve --duration 0.5 \
       --bgm bgm_full_track.wav:0.42 \
       --voice 1800:voice_find.mp3:1.3 --voice 5900:voice_hesitate.mp3:1.3 \
       --out 完整版.mp4
   ```
   - `--transitions`：转场类型列表（数量 = 镜头数-1），常用 `dissolve` 交叉溶解、`fadeblack` 黑场（情绪转折）、`fade` 淡入淡出、`slideleft` 左滑；脚本内置转场名校验
   - `--voice`：语气词按时间轴定位，格式 `延迟毫秒:音频文件[:音量]`，可重复多次
   - 输出自动保证 yuv420p（兼容所有播放器）；`--t` 可强制总时长
   - 脚本会自动探测各视频时长并计算 xfade offset，且对缺失文件、无效转场给出明确错误提示

2. **完整背景音乐轨**（多段落情绪起伏，段落间交叉淡变）：
   ```
   # 默认 4 段：bright→gentle→calm→bright，适合发现→犹豫→行动→满足
   python scripts/compose_full_track.py bgm_full_track.wav --total 18.7

   # 自定义段落
   python scripts/compose_full_track.py bgm.wav --plan "calm:5.0,bright:5.0" --total 9.2
   ```

3. **语气词配音**（edge-tts 晓晓中文女声，带情绪语速/音调）：
   ```
   # 默认剧情 4 句
   python scripts/gen_voice_lines.py generated-videos

   # 自定义台词
   python scripts/gen_voice_lines.py generated-videos \
       --voice "v1:哇——好漂亮的蛋糕店！:+20%:+8Hz" \
       --voice "v2:嗯…要不要进去呢？:-15%:-3Hz" \
       --voice "v3:嘿嘿，草莓蛋糕到手啦！:+10%:+6Hz"
   ```

4. **视频/音频信息探测**：
   ```
   python scripts/probe_video.py shot1.mp4 shot2.mp4 --json
   ```
   输出每个素材的时长、分辨率、帧率、编码、是否有音轨，方便拼接前确认一致性。

5. **时间轴建议**：每个镜头进入约 1.5-2s 后放语气词，避免压住转场；语气词总长（含尾部气声）不要超过所在镜头时长，防止溢出到下一镜头。

6. 合成完成后用 `present_files` 展示完整版，说明镜头顺序、转场、总时长。

> 语气词是 TTS 合成人声，仅作语气/短句配音；长旁白需用户确认文案与配音风格。

## 输出契约

直接生成成功时：以结果开头，只加必要说明。

无法执行生成时，返回：
- 推荐平台与备选
- 选定的时长与宽高比
- 运动概念
- 平台偏好语言/风格的主 Prompt
- 负向 Prompt 或保真约束
- 平台设置（支持时含运动强度与镜头控制）
- 最可能失败点的一条重试指令

输出必须立即可用。除非用户要求，不提供通用教程。

## 安全与保真

- 不将真人动效化为欺骗、诽谤、色情、暴力或其他被禁止的行为。
- 对身份敏感或公众人物的变形保持警惕，遵守适用的媒体安全规则。
- 不为上传的图片、音乐、Logo 或肖像虚构所有权或许可权。
- 图片含二维码、密集法律文本、表格、证书等精确内容时保持静态；推荐合成而非生成式重绘。
- 医疗、法律、安全或新闻类图片，避免改变事实含义的运动。

## 参考文件

- `references/platform-routing.md` — 平台选择与语法适配速查
- `references/prompt-patterns.md` — 内容类型 Prompt 模式、负向 Prompt 与失败控制
- `scripts/probe_video.py` — 视频/音频元信息探测（时长、分辨率、帧率、音轨）
- `scripts/compose_music.py` — 单段背景音乐合成（numpy 生成 WAV）
- `scripts/compose_full_track.py` — 多段落情绪背景音乐轨（支持自定义段落）
- `scripts/gen_voice_lines.py` — 语气词/台词配音（edge-tts 晓晓女声，支持自定义台词）
- `scripts/stitch_videos.py` — 多镜头拼接 + 转场 + 配乐 + 配音一条龙
- `scripts/mux_audio.py` — 单视频混音（imageio-ffmpeg 自带 ffmpeg）
- `scripts/add_subtitles.py` — 中文字幕/标题烧录（自动探测字体）

## 依赖

- 内置 `VideoGen` 工具（通过 ToolSearch + DeferExecuteTool 调用）
- 配乐/混音/拼接/字幕流程需要：`numpy` + `imageio-ffmpeg`（安装到 managed Python 虚拟环境，非全局）
- 语气词配音需要：`edge-tts`（`<venv>/Scripts/pip install edge-tts`，需联网；Windows 本地 TTS 的 System.Speech 可能被安全策略拦截，优先用 edge-tts）
- 如未安装依赖，脚本会给出明确提示；首次使用前在虚拟环境执行一次：
  ```
  <venv>/Scripts/pip install numpy imageio-ffmpeg edge-tts
  ```
