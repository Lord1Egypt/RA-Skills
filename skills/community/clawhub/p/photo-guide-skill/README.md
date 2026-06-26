# photo-guide-skill

[![license](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

[English](./README.en.md)

> 上传一张照片，告诉你怎么拍、怎么修、怎么学。

一个面向摄影新手的照片分析 Skill。基于 AgentSkills 开放标准构建，兼容 Claude Code、OpenClaw 等支持 Skill 的 AI Agent。

## 它能做什么？

| 功能 | 说明 |
|------|------|
| EXIF 提取 | 自动从照片中读取真实拍摄参数（光圈、快门、ISO、焦距、相机型号） |
| 五维视觉分析 | 从景深、动态、光影、色彩、构图五个维度推断拍摄参数 |
| 风格匹配 | 将照片归类到 10 种常见摄影风格模板，交叉验证参数 |
| 拍摄设置建议 | 推荐拍摄模式、对焦模式、测光方式、白平衡、曝光补偿、连拍策略 |
| 布光与道具建议 | 根据场景推荐布光方案和所需道具（三脚架、滤镜、补光灯等） |
| 手机替代方案 | 检测到手机拍摄时，给出手机专属参数调整和 App 推荐 |
| 后期调色指导 | 给出色调方向、曝光调整、对比度建议和风格预设关键词 |
| 新手学习建议 | 提供可操作的学习关键词，帮你快速入门 |

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 安装 Skill

将 `photo-guide-skill` 目录复制或链接到你的 Agent Skills 目录：

```bash
# Claude Code 示例
cp -r photo-guide-skill ~/.claude/skills/

# 或使用符号链接
ln -s $(pwd)/photo-guide-skill ~/.claude/skills/photo-guide-skill
```

### 使用方式

在 Agent 对话中上传照片并提问：

- 「这张照片怎么拍的？」
- 「教我拍出这种效果」
- 「这张照片的光圈/快门是多少？」
- 「怎么调这种色调？」
- 「帮我分析一下这张照片」

## 目录结构

```
photo-guide-skill/
├── SKILL.md                          # Skill 主入口（触发条件、工作流程、输出模板）
├── README.md                         # 项目说明（本文件）
├── README_EN.md                      # English README
├── requirements.txt                  # Python 依赖
├── LICENSE                           # MIT 许可证
├── .gitignore
├── references/                       # 参考知识库
│   ├── photography-basics.md         # 摄影参数参考表（光圈/快门/ISO/焦段/构图/光位/拍摄模式/对焦/测光/滤镜）
│   ├── style-templates.md            # 10 种摄影风格模板（人像/日系/街拍/夜景/美食等）
│   └── post-processing-guide.md      # 后期调色教程（基础概念 + 风格预设）
├── scripts/                          # 工具脚本
│   └── extract_exif.py               # EXIF 元数据提取脚本
└── examples/                         # 示例分析报告
    ├── test1.jpeg / test1.md         # 示例 1：建筑/宗教细节
    ├── test2.jpg  / test2.md         # 示例 2：风光建筑
    └── test3.jpg  / test3.md         # 示例 3：海景（无 EXIF，纯视觉推断）
```

## 工作流程

```
用户上传照片 + 提问
        │
        ▼
  ① 提取 EXIF ─── 有 EXIF ──→ 记录真实参数作为校验基准
        │
     无 EXIF
        │
        ▼
  ② 五维度视觉分析（景深/动态/光影/色彩/构图）
        │
        ▼
  ③ 匹配风格模板，交叉验证参数
        │
        ▼
  ④ 生成结构化分析报告
     ├── 画面概述
     ├── 拍摄参数（推断值 + 实际值对比）
     ├── 拍摄技巧要点
     ├── 照片优化建议
     ├── 后期调色建议
     ├── 拍摄设置建议（大部分场景出现）
     ├── 布光与道具建议（控光场景出现）
     ├── 手机拍摄替代方案（手机照片出现）
     └── 推荐学习关键词
```

## 分析报告示例

```
📷 照片分析报告
━━━━━━━━━━━━━━━

📋 画面概述
- 照片类型：海景风光
- 主要元素：海中岩石柱、浪花、天空
- 拍摄环境：室外，黄昏时分

⚙️ 拍摄参数
| 参数     | 推断值          | 推断理由              |
| -------- | --------------- | --------------------- |
| 光圈     | f/8 - f/11      | 画面整体清晰，大景深   |
| 快门速度 | 1/2s - 2s       | 水面呈现丝滑雾化效果   |
| ISO      | 100 - 200       | 画质细腻，无明显噪点   |
| 焦段     | 24mm - 35mm     | 广角视野，涵盖前景岩石 |
| 拍摄角度 | 低角度平视       | 岩石柱显得雄伟壮观     |

💡 拍摄技巧要点
- 使用三脚架 + 慢门拍出丝滑水面效果
- 低角度拍摄增强岩石柱的视觉冲击力

🎨 后期调色建议
- 色调方向：冷调偏暖，日落氛围
- 推荐风格预设：Long Exposure Seascape

📚 推荐学习关键词
- 长曝光海景拍摄
- ND 滤镜使用
```

## 设计原则

1. **推断为主，EXIF 为辅** — 大多数网络图片没有 EXIF，视觉推断才是核心能力
2. **给范围不给固定值** — 如 `f/2.0 - f/2.8`，因为同一效果可以由多种参数组合实现
3. **新手友好** — 先肯定优点，再给建议；专业术语附简短解释
4. **实用导向** — 重点是教会「怎么拍」，而非堆砌理论

## 依赖

- Python 3.10+
- Pillow >= 9.0.0（EXIF 提取）

详见 [requirements.txt](requirements.txt)。

## 兼容性

遵循 [AgentSkills](https://agentskills.io/home) 开放标准，兼容：

- Claude Code
- OpenClaw
- 其他支持 AgentSkills 标准的 AI Agent

## 许可证

[MIT License](LICENSE)

Copyright (c) 2026 dcison
