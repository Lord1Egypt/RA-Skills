# Multimodal Understanding Skill

使用智谱 GLM-4.6V 模型进行多模态内容理解。

## 安装

已安装到 `~/.openclaw/workspace/skills/multimodal/`

依赖：
- Python 3
- requests 库（自动安装）

配置：
```bash
export ZHIPU_API_KEY="your-api-key"
```

## 使用方法

### 命令行

```bash
# 图片分析
multimodal-analyze -t image -i photo.jpg -p "描述这张图片"

# 视频分析（需要公网URL）
multimodal-analyze -t video -i https://example.com/video.mp4 -p "视频讲了什么"

# 文档分析
multimodal-analyze -t file -i document.pdf -p "总结这个文档"

# 深度思考模式
multimodal-analyze -t image -i photo.jpg -p "分析构图和风格" --thinking

# 流式输出
multimodal-analyze -t image -i photo.jpg -p "描述" --stream
```

### 在对话中使用

直接告诉我：
- "分析这张图片：[图片]"
- "这个视频讲了什么：[视频URL]"
- "理解这个PDF：[文件]"

## 支持的输入

| 类型 | 格式 | 来源 |
|------|------|------|
| 图片 | jpg, png, gif, webp | 本地文件或URL |
| 视频 | mp4, mov, avi | URL（推荐）或本地 |
| 文档 | pdf, txt, docx | 本地文件或URL |

## 模型信息

- **模型:** GLM-4.6V (106B参数)
- **上下文:** 128K tokens
- **能力:** 原生多模态工具调用、深度思考

## 文件结构

```
skills/multimodal/
├── SKILL.md           # 技能说明
├── README.md          # 本文件
├── agent.json         # Agent配置
└── scripts/
    ├── analyze.py     # 主分析脚本
    └── multimodal-analyze  # Bash wrapper
```
