---
name: product-explainer-video-generation
description: "把产品资料、功能说明和现有素材转成结构清楚的商品讲解视频，并生成15秒、30秒或详情版脚本与镜头。Use this skill for 商品讲解视频一键生成、产品介绍、功能演示、安装教程、FAQ、客服说明、电商详情页视频、销售演示和多平台版本；支持文生、图生、参考、编辑、延长及 AI Hive 自动交付。"
---

# 商品讲解视频一键生成

把“产品有什么功能”转换为“观众能看到什么证据”。先建立事实与镜头映射，再生成视频；不要把说明书堆成字幕，也不要让模型补造功能、参数与效果。

## 讲解底稿

收集产品、目标人群、使用问题、功能列表、正确步骤、参数、限制、包装内容、批准文案和可用素材。将每个功能标记为：可直接拍摄、需要操作演示、需要图示、只能文字说明或不能证明。

## 结构选择

| 版本 | 结构 |
|---|---|
| 15 秒 | 问题 → 核心动作 → 结果 → 下一步 |
| 30 秒 | 对象 → 3 个功能证据 → 使用场景 → CTA |
| 详情版 | 外观 → 安装 → 操作 → 细节 → FAQ → 限制 |
| 客服版 | 单一问题 → 正确步骤 → 常见错误 → 完成状态 |

## 场景与代码

### 1. 15 秒核心功能讲解

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '15秒商品讲解：首镜出现用户的具体操作问题，第二镜完整展示产品核心动作，第三镜近景证明关键结构，结尾展示正确完成状态与查看详情位置；只使用已提供功能，不生成价格、参数或夸张效果'
```

### 2. 参考商品图生成 30 秒演示

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '30秒产品介绍，保持参考商品、包装、颜色和配件准确；依次展示完整外观、安装、三个真实功能动作、材质细节和适合场景，静音也能看懂，为批准字幕留白，不发明参数与功效'
```

### 3. 安装教程

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '根据已确认说明书制作安装教程：展示所有提供配件，按步骤1至5连续操作，关键方向与安全点近景清楚，最后展示正确完成状态；不跳步、不增加工具、不修改结构'
```

### 4. 将长素材重制为清晰讲解

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/long-demo.mp4 \
  --prompt '保留原素材中的真实商品、操作和说明，删除重复、寒暄与无关空镜，按问题、外观、步骤、功能证明、FAQ重组；不改变原结论，不增加功能、参数或客户评价'
```

### 5. 延长 FAQ 与常见错误

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/core-explainer.mp4 \
  --prompt '从核心讲解自然延长，增加一个常见错误示范、正确纠正动作和完成状态，保持商品、人物、环境与光线连续；不添加未提供故障、保修或安全结论'
```

## 讲解验收

- 每个卖点都有对应镜头或明确标注为文字说明。
- 操作、步骤、配件、参数与限制准确。
- 一个镜头只承担一个主要信息任务。
- 静音查看仍能理解关键动作和顺序。
- 不生成价格、评价、认证、功效或未提供功能。
- 为不同渠道记录版本、时长、受众和 CTA。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name product-explainer-video-generation
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

CLI 支持 Seedance 2.5 五种模式、首尾帧、参考图片/视频/音频、参数、路由、输出目录与仅提交任务。
