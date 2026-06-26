# Article Auto Generate Skills

Claude Code Skill for end-to-end content production and distribution.

```
素材收集 → 写文章 → 排版 → 封面图 → 多平台内容 → 一键分发
```

## 功能

- **Path A**: 日常收集素材 → 生成文章 → 排版 → 封面图 → 社交媒体文案
- **Path B**: 微信文章URL → 自动生成微贴图、博客园、播客、视频画布 → 一键分发

### 支持平台

| 平台 | 状态 |
|------|------|
| 微信公众号 | 可用 |
| 微贴图 | 可用 |
| 博客园 | 可用 |
| 微博 | 可用 |
| 抖音 | 实验性 |

## 安装

1. 克隆到你的 Claude Code skills 目录：

```bash
git clone https://github.com/oddmeta/odd-article-skills.git ~/.claude/skills/odd-article-skills
```

2. 复制环境变量配置：

```bash
mkdir -p ~/.claude/skills/odd-article-skills/local
cp ~/.claude/skills/odd-article-skills/.env.example ~/.claude/skills/odd-article-skills/local/.env
```

3. 编辑 `local/.env` 填入你的凭证

## 配置

### 技能所需的环境变量

| 变量 | 说明 |
|------|------|
| `OUTPUT_DIR` | 输出目录，用于放置收集到的素材、生成的文章、排版预览、封面图、微贴图轮播图等文件。 |
| `ARCHIVE_DIR` | 存档目录，用于归档历史文档文件。 |
| `BRAND_NAME` | 品牌名称，用于在生成的文章中显示品牌名称。|
| `BRAND_LOGO_DARK` | 品牌logo（深色），用于在生成的文章中显示品牌logo。|
| `BRAND_LOGO_LIGHT` | 品牌logo（浅色），用于在生成的文章中显示品牌logo。|
| `WECHAT_ID` | 微信公众号ID，用于发布文章。|
| `WECHAT_SLOGON` | 微信公众号标语，用于在文章中显示。|
| `WECHAT_APPID` | 微信公众号AppID，用于发布文章时的认证。|
| `WECHAT_APPSECRET` | 微信公众号AppSecret，用于发布文章时的认证。|
| `CNBLOGS_TOKEN` | 博客园Token，用于发布博客园文章时的认证。|
| `MD_FORMATTER_DIR` | Markdown格式化工具目录，用于格式化Markdown文章。|
| `BAOYU_WECHAT_SKILL_DIR` | 奥德元微信技能目录，用于发布文章。|
| `MD_TO_WECHAT_SCRIPT` | Markdown文章转微信文章脚本，用于将Markdown文章转换为微信文章。|
| `FISH_API_KEY` | Fish Audio TTS API key |

## 使用

在 Claude Code、OpenCode、OpenClaw 等工具 中使用这些触发词：

| 触发词 | 功能 |
|-------|------|
| "出稿" | 从素材生成文章 + 排版 + 封面图 |
| "排版" | Markdown → 微信公众号 HTML |
| "做头图" | 生成公众号头图 |
| `/chartlet` + 微信链接 | 微信文章转微贴图轮播图 |
| "转微博" + 微信链接 | 生成微博文案 |
| "转播客" + 微信链接 | 生成播客脚本 + AI 语音 |
| "做视频画布" + 内容 | 生成可录制的视频画布 |
| `/distribute` | 一键发布到所有平台 |

## 项目结构

```
odd-article-skills/
├── SKILL.md                                # 主要技能定义
├── .env.example                            # 环境变量示例
├── local/                                  # 本地配置（不提交到Git）
│   ├── SKILL.local.md                      # 个人设置覆盖
│   └── .env                                # API密钥
├── references/                             # 模板和样式指南
│   ├── cover_template.md                   # 封面图设计规范
│   ├── frameworks.md                       # 文章框架类型
│   ├── platform_copy.md                    # 平台文案指南
│   ├── tts_config.md                       # Fish Audio TTS配置
│   └── ...
└── scripts/
    ├── wechat_download.py                  # 微信文章抓取
    ├── md2wechat.py                        # 微信文章排版
    └── distribute/                         # 多平台发布器
```

## 许可证

MIT