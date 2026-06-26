---
name: huo15-influencer-video-skill
displayName: 火一五带货视频技能
description: 通过火山方舟Ark API调用Seedance 2.0生成第一人称带货短视频，v2 新增剧本驱动的配音（edge-tts/火山TTS）、背景音乐自动混音、字幕烧录，内置 8 套人设模板（传统女、时尚主播、老中医、厨房主妇、美妆博主、健身教练、户外探店、数码博主）。触发词：生成视频、带货视频、产品视频、拍视频、剧本拍视频。
version: 2.0.0
aliases:
  - 火一五带货视频技能
  - 火一五AI带货视频技能
  - 火一五产品视频技能
  - 带货视频
  - 剧本带货视频
  - AI视频生成
  - 产品视频
---

# 火15 AI 带货视频生成 Skill v2

> 产品图 + 剧本 → 带配音、背景音乐、字幕的第一人称带货短视频。
> 内置 8 套人设模板，一句话指定品类即可自动选模板。

---

## ⚠️ 安全规则

1. 每次生成前**必须**告知用户预估费用（Seedance 视频部分；TTS edge-tts 免费、火山 TTS 单字 ≤¥0.0006）
2. 用户确认后才可提交任务
3. 单次最大时长 15 秒，默认按配音时长自动决定
4. 优先使用最省 Token 的配置

---

## 一、能力总览

| 模块 | v1 | v2（本次） |
|---|---|---|
| 视频生成 | Seedance 2.0 ✅ | Seedance 2.0 ✅ |
| 配音 | ❌ | edge-tts（默认免费） / 火山 TTS（可选） ✅ |
| 背景音乐 | ❌ | ffmpeg 自动循环+降音量+淡出 ✅ |
| 字幕 | ❌ | 按行字数比例切时间轴 + 烧录 ✅ |
| 人设模板 | 1 套（传统女） | **8 套**（按品类自动推荐） ✅ |
| 剧本驱动 | ❌ | JSON 剧本一键端到端 ✅ |

---

## 二、文件结构

```
huo15-influencer-video-skill/
├── SKILL.md                           # 本文档
├── _meta.json
├── scripts/
│   ├── templates.py                   # 8 套人设模板配置
│   ├── tts.py                         # 配音引擎（edge-tts + 火山）
│   ├── bgm.py                         # BGM 库 + 混音 + 视频/音频合并
│   └── pipeline.py                    # 端到端 pipeline（推荐入口）
└── examples/
    ├── script_traditional_lady.json
    ├── script_fashion_host.json
    └── script_auto_template.json
```

---

## 三、依赖与凭证

```bash
# 必需
brew install ffmpeg
pip install edge-tts requests

# 视频生成
export ARK_API_KEY=ak-xxxxx                # 方舟控制台获取

# 可选：火山 TTS（不设则降级到 edge-tts，免费但音质稍弱）
export VOLC_TTS_APP_ID=xxxxx
export VOLC_TTS_TOKEN=xxxxx
export VOLC_TTS_CLUSTER=volcano_tts

# 可选：BGM 库目录（默认 ~/Music/huo15-bgm/）
export HUO15_BGM_DIR=~/Music/huo15-bgm
```

### BGM 文件准备（一次性）

把 5 个免版税音乐放到 `~/Music/huo15-bgm/`（缺哪个跳过哪个，不影响视频生成）：

| 文件名 | 风格 | 推荐用途 | 下载关键词 |
|---|---|---|---|
| `warm.mp3` | 温暖钢琴 | 养生/食品/手工 | warm piano background |
| `energetic.mp3` | 活力电子 | 美妆/服装/直播 | upbeat electronic |
| `asian.mp3` | 中国风古筝 | 中药/茶/古风 | chinese guzheng |
| `soft.mp3` | 柔和氛围 | 数码/护肤 | soft ambient pad |
| `cinematic.mp3` | 电影弦乐 | 户外/特产 | cinematic strings |

下载渠道：[Pixabay Music](https://pixabay.com/music/)（CC0）、[Freesound](https://freesound.org/)、[Incompetech](https://incompetech.com/music/royalty-free/)（注明出处）。

---

## 四、8 套预设模板

| key | 角色 | 推荐音色 | 推荐 BGM | 适用品类 |
|---|---|---|---|---|
| `traditional_lady` | 传统中年女性（默认） | 晓秋（沉稳） | warm | 养生 / 茶叶 / 手工 / 古法食品 |
| `fashion_host` | 时尚女主播 | 晓晓（活泼） | energetic | 美妆 / 服装 / 饰品 / 数码配件 |
| `tcm_doctor` | 老中医 | 云健（沉稳男） | asian | 中药 / 保健品 / 膏方 / 艾灸 |
| `kitchen_mom` | 厨房主妇 | 晓涵（温暖） | warm | 调味料 / 食材 / 厨具 / 速食 |
| `beauty_blogger` | 美妆博主 | 晓梦（活泼） | soft | 护肤 / 彩妆 / 香水 / 美容仪 |
| `fitness_coach` | 健身教练 | 云皓（激情男） | energetic | 蛋白粉 / 运动器材 / 补剂 |
| `outdoor_explorer` | 户外探店达人 | 云夏（轻快男） | cinematic | 地方特产 / 户外装备 / 民俗 |
| `tech_geek` | 数码博主 | 云扬（专业男） | soft | 手机 / 耳机 / 智能家居 / 电脑 |

### 自动选模板

```json
{ "template": "auto", "category": "蛋白粉", ... }
```
→ 命中 `fitness_coach`。无匹配回退 `traditional_lady`。

---

## 五、剧本格式

```json
{
  "template": "traditional_lady",
  "image": "/path/to/product.jpg",
  "lines": [
    {"text": "姐妹们，今天给大家推一款好东西", "action": "举起产品给镜头"},
    {"text": "古法配方，纯手工制作",            "action": "微笑展示产品细节"},
    {"text": "用过的姐妹都说好",                "action": "点头肯定"}
  ],
  "bgm": "warm",
  "bgm_volume": 0.18,
  "subtitle": true,
  "voice_override": null,
  "rate_override": null,
  "output": "/tmp/huo15/final.mp4"
}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `template` | ✅ | 模板 key 或 `"auto"`（配合 `category`） |
| `category` | template=auto 时必填 | 品类关键词，自动选模板 |
| `image` | ✅ | 产品图本地路径 |
| `lines` | ✅ | 数组，每条 `{text, action}`。**首条 action 会写进 Seedance prompt** |
| `bgm` | ❌ | BGM key（warm/energetic/...）或绝对路径；null=无 BGM |
| `bgm_volume` | ❌ | 0~1，覆盖模板默认（0.18~0.25 较合适） |
| `subtitle` | ❌ | 默认 true；烧录字幕到视频 |
| `voice_override` | ❌ | 强制换音色，如 `"zh-CN-XiaoxiaoNeural"` |
| `rate_override` | ❌ | 强制改语速，如 `"+10%"` |
| `output` | ❌ | 成片路径 |

### 台词长度上限

整段配音必须 ≤ 14.5 秒（Seedance 单次最长 15s）。中文约 **50~70 字**。
超长会抛错并提示精简，不强行截断。

---

## 六、调用方式

### 6.1 命令行（最直接）

```bash
cd huo15-influencer-video-skill

# 自检 — 第一次跑先做这一步
python3 scripts/pipeline.py preflight

# 列出 8 套人设模板 / 8 个推荐音色
python3 scripts/pipeline.py templates
python3 scripts/pipeline.py voices

# dry-run — 只跑 TTS + 字幕，不调 Seedance（省 ¥）
# 用于先验证剧本节奏、TTS 音色、字幕断句
python3 scripts/pipeline.py dry-run examples/script_traditional_lady.json

# 完整端到端
python3 scripts/pipeline.py render examples/script_traditional_lady.json
```

### 6.2 Python 调用

```python
import sys, json
sys.path.insert(0, "scripts")
from pipeline import render

result = render({
    "template": "auto",
    "category": "蛋白粉",
    "image": "/path/to/protein.jpg",
    "lines": [
        {"text": "兄弟们练完这一组",   "action": "拿起产品"},
        {"text": "蛋白吸收率高得离谱", "action": "展示成分"},
    ],
    "subtitle": True,
})
print(result)
# {'output': '/tmp/huo15_video/final.mp4', 'template': 'fitness_coach',
#  'voice_duration': 6.2, 'video_duration': 8, 'tokens': 172800,
#  'cost_yuan': 7.95, 'size_mb': 3.1}
```

### 6.3 仅生成无声视频（兼容 v1 用法）

需要老接口的话，从 `pipeline._generate_silent_video` 直接调，跳过 TTS/BGM。

---

### 6.4 Dry-run（强烈建议先跑）

```python
result = render(script, dry_run=True)
# 返回：voice_path / srt_path / tokens 预估 / cost_yuan / prompt
# 不调 Seedance，不计费；TTS 是免费的
```

用途：调剧本节奏、试音色、看字幕断行 —— 全部确认满意再跑 render(dry_run=False)。
Agent 应该在用户首次给剧本时**默认先做 dry-run**，把生成的 voice.mp3 路径告诉用户试听。

---

## 七、Agent 工作流

当用户说"用这张图按这个剧本拍带货视频"时，按下面的步骤走：

1. **收集要素**
   - 产品图路径
   - 剧本（多句台词）；如未给可主动起草
   - 品类关键词（用于自动选模板）
2. **选模板**
   - 用户没明说就调 `templates.suggest_template(category)`
   - 给用户看一眼"我准备用 XX 模板（XX 角色 + XX 音色 + XX BGM）"
3. **预算确认**
   - 算配音预估时长（80字 ≈ 9~10s）
   - 算视频费用（`estimate_cost`），告知用户
4. **执行**
   - `render(script)` 端到端
5. **交付**
   - 文件路径、实际时长、Seedance tokens、¥ 费用

### 对话示例

```
用户: 用 product.jpg 拍个卖蛋白粉的，3 句台词，自己想词
Agent: 我帮您起草剧本，按健身教练模板（云皓男声 + energetic BGM）：
        1) 兄弟们，练完这一组
        2) 蛋白吸收率高得离谱
        3) 练大一年，从这罐开始
       预估视频时长 8s ≈ ¥7.95，配音免费。确认生成？
用户: 行
Agent: [render] → /tmp/huo15/protein.mp4 (3.1MB)，实际 ¥7.95
```

---

## 八、Seedance API 速查（保留 v1）

| 项 | 值 |
|---|---|
| 模型 | `doubao-seedance-2-0-260128` |
| 端点 | `https://ark.cn-beijing.volces.com/api/v3` |
| 计费 | `Token = 秒 × 720 × 1280 × 24 / 1024`，`¥ = Token × 46 / 1e6` |
| 比例 | `9:16` 竖屏带货 |
| 时长 | 4 ~ 15 秒 |

| 时长 | Token | 费用 |
|---|---|---|
| 4s  | ~86,400  | ¥3.97 |
| 5s  | ~108,000 | ¥4.97 |
| 10s | ~216,000 | ¥9.94 |
| 15s | ~324,000 | ¥14.90 |

content 中的 role：

| role | 用途 |
|---|---|
| `reference_image` | 默认；AI 参考产品外观 |
| `first_frame` | 视频必须从这张图开始 |
| `last_frame` | 指定结束画面 |
| `reference_video` | 运动风格参考 |
| `reference_audio` | 音频风格参考 |

---

## 九、混音参数（bgm.py）

```
voice 主轨 ──┐
              ├─ amix(duration=first) ─ afade(out, 0.5s) ─→ mixed.mp3
BGM 副轨 ────┘    （BGM aloop 到与 voice 等长，volume=bgm_volume）
```

- `bgm_volume` 默认 0.18~0.25。模板已按角色调过，一般不用改。
- `voice_volume` 默认 1.0；想突出 BGM 可降到 0.85。
- 末尾统一 0.5 秒淡出，避免硬切。

成片合成：`mux_video_audio(silent.mp4, mixed.mp3, final.mp4)` —
`-c:v copy -c:a aac -shortest`，无视频重编码，秒出。

---

## 十、字幕（pipeline._build_srt + _burn_subtitles）

- 按每行台词字数比例切时间轴生成 SRT
- 用 ffmpeg `subtitles` 滤镜烧录到视频
- 默认字体 PingFang SC、字号 14、白字黑边、底部 80px
- 想关字幕：剧本里 `"subtitle": false`

字体不可用时报 `Fontconfig error`，换 `font: "Heiti SC"` 或装 `brew install --cask font-noto-sans-cjk-sc`。

---

## 十一、降级策略（哪步失败也别全废）

| 失败 | 降级行为 |
|---|---|
| 火山 TTS 凭证缺失 | 自动用 edge-tts |
| edge-tts 也挂 | 抛错，提示 `pip install edge-tts` 并检查网络 |
| BGM 文件找不到 | 跳过 BGM，仅人声 + 0.5s 淡出 |
| 字体找不到 | `subtitle: false` 重跑，或装中文字体 |
| Seedance 超时 | 默认 20 分钟轮询，超时抛 TimeoutError |

---

## 十二、常见问题

### Q: 配音不准 / 多音字读错怎么办？
A: 在 `lines.text` 里用谐音字。edge-tts 不支持 SSML phoneme tag。

### Q: BGM 太响盖过人声？
A: 剧本里 `"bgm_volume": 0.12` 进一步压低，或换 soft.mp3。

### Q: 想纯人声没 BGM？
A: 剧本里 `"bgm": null`。

### Q: 想要长视频（>15 秒）？
A: 当前版本不支持。建议拆段：每段 ≤15s 单独生成，再用 ffmpeg `concat` 拼接。

### Q: 视频画面和剧本对不上？
A: 把第一句的 `action` 写得更具体（"举起产品贴近镜头"比"展示"准）。
   剧本中段的 action 仅用于字幕节奏参考，不会写进 Seedance prompt。

### Q: 想保留 v1 的纯视频生成？
A: 直接调 `pipeline._generate_silent_video(image, prompt, duration, output)`。

---

## 十三、版本历史

- **v2.0.0**（2026-04-27）— 剧本驱动 + 配音 + BGM + 字幕 + 8 套模板 + dry-run + preflight
- v1.2.x — 单一传统女模板 + 无声视频
