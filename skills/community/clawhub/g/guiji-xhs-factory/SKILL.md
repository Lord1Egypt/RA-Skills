---
name: guiji-xhs-factory
version: 1.0.0
description: 龙虾内容工厂。批量生成小红书信息图+视频，定时自动发布。
metadata:
  emoji: "🏭"
  category: "content"
  requires:
    bins: ["ffmpeg", "python3"]
---

# 🏭 龙虾内容工厂

批量生成小红书帖子（信息图+视频），定时自动发布。

**核心流程**：定义帖子 → 生成图片 → 拼成视频 → 定时发布

---

## 安装

```bash
# 1. 解压到 skills 目录
unzip guiji-xhs-factory.skill.zip -d ~/.openclaw/workspace/skills/

# 2. 安装 Python 依赖
pip3 install Pillow

# 3. 安装 ffmpeg（macOS）
brew install ffmpeg

# 4. 安装 Playwright（发布用）
npm install -g playwright
npx playwright install chromium

# 5. 确认 Chrome 运行中（CDP 端口 18800）
#    需要以 --remote-debugging-port=18800 启动 Chrome
```

---

## 快速开始（3 步）

### 第1步：编辑帖子内容

打开 `{baseDir}/scripts/generate-today.py`，编辑 `POSTS` 数组：

```python
POSTS = [
    {
        "id": "my_post_1",
        "schedule": "12:00",           # 发布时间
        "title": "帖子标题(≤20字)",    # 小红书标题
        "content": "正文内容+标签",    # 小红书正文（含#标签）
        "cards": [                     # 信息图配置
            {"title": "封面大标题", "items": []},     # items为空=纯标题封面
            {"title": "要点标题", "items": [
                "##分类名",           # 高亮分类标题
                "要点1",              # 普通内容
                "要点2",
                "» 副标题文字",       # 灰色副标题
                "",                   # 空行=间距
                "要点3",
            ]},
        ]
    },
]
```

**items 格式说明**：
| 前缀 | 效果 | 示例 |
|------|------|------|
| 无 | 普通文字 | `"自动安全审核"` |
| `##` | 分类标题（高亮色） | `"##安全防护"` |
| `»` | 副标题（灰色小字） | `"» 效率提升"` |
| `""` | 空行间距 | `""` |

**配色预设**（在 card 上加 `"preset": "xxx"`）：
- `default` — 深蓝黑 + 天蓝（通用）
- `tutorial` — 深绿 + 翠绿（教程）
- `case` — 深棕 + 橙色（案例）
- `secret` — 深紫 + 紫色（秘诀）
- `cover` — 深蓝 + 蓝色（封面）

### 第2步：生成内容

```bash
python3 {baseDir}/scripts/generate-today.py
```

自动完成：
- 每张 card → 1080×1440 PNG 信息图
- 所有图片 → 视频幻灯片（每张 6 秒，25fps）
- 输出 `content-queue/manifest.json` 清单

### 第3步：发布

**方式A：定时发布（推荐）**

```bash
openclaw cron add \
  --name "小红书-午间发布" \
  --cron "0 12 * * *" \
  --tz "Asia/Shanghai" \
  --message "定时发布：读 manifest.json → 运行 node {baseDir}/scripts/publish-xhs.js <视频路径> '<标题>' '<正文>'"
```

**方式B：手动发布**

```bash
node {baseDir}/scripts/publish-xhs.js \
  /tmp/openclaw/uploads/my_post_1_slideshow.mp4 \
  "我的标题" \
  "我的正文内容"
```

---

## 发布脚本说明

`publish-xhs.js` 使用 Playwright 连接 Chrome（CDP 18800）：

1. 打开小红书创作者平台
2. 上传视频
3. 填写标题（React nativeInputValueSetter hack）
4. 填写正文（innerHTML 注入）
5. **不自动点击发布** — 等你确认后手动点

---

## 发布规则速查

| 项目 | 规则 |
|------|------|
| 标题 | ≤20 字，含数字或关键词 |
| 正文 | 300-800 字，5-8 个 #标签 |
| 配图 | 3:4 (1080×1440)，3-9 张 |
| 视频 | MP4，15-60 秒 |
| 时间 | 工作日 12-13 点、20-22 点 |
| 频率 | 每天 1-3 篇，间隔 ≥2 小时 |

---

## 文件结构

```
guiji-xhs-factory/
├── SKILL.md                  # 本文件（Agent 行为手册）
├── scripts/
│   ├── generate-today.py     # 内容生成脚本
│   ├── make_card.py          # 信息图生成器（PIL）
│   └── publish-xhs.js        # Playwright 发布脚本
└── references/
    ├── post-templates.md     # 5 种帖子模板
    └── publish-rules.md      # 发布规则详解
```

---

## 注意事项

- ⚠️ Chrome 必须以 `--remote-debugging-port=18800` 启动
- ⚠️ 小红书需在 Chrome 中已登录（creator.xiaohongshu.com）
- ⚠️ 视频上传比图片上传更稳定，优先用视频格式
- ⚠️ 发布脚本不会自动点发布按钮，需人工确认

---

Built with 🦞 by 龙虾养成师 Ursa
