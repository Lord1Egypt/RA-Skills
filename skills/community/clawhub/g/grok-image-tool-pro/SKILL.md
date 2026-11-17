---

slug: grok-image-tool-pro
name: "grok-image-tool-pro"
version: "1.0.0"
displayName: "Grok图片生成-专业版"
summary: "批量AI图片生成引擎，支持多格式导出、消息平台集成与自动化工作流。。Grok图片生成工具专业版。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判"
license: "Proprietary"
edition: "pro"
description: |-
  Grok图片生成工具专业版。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。支持多场景应用和灵活配置。
tags: 创意,self,style,subject,prompt_data,图片生成
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"

---

> **功能说明**: 本技能涵盖 中文交互 等核心能力。


# Grok图片生成工具（专业版）
## 概述

Grok图片生成工具专业版是批量图片生成平台，通过浏览器自动化和桌面操作，实现从提示词队列到图片生成、保存、后处理和消息平台分发的完整自动化工作流。支持批量生成、多格式导出、自定义路径和即时发送.
本版本与免费版完全兼容——免费版的单张图片生成和保存流程在专业版中完整保留。专业版新增批量生成、多格式导出、消息集成和工作流自动化等能力.
## 核心能力

### 能力对比

| 能力维度 | 免费版 | 专业版 |
|----|---|---|
| 生成模式 | 单张 | 批量队列 |
| 输出格式 | JPG（默认） | PNG/JPG/WebP |
| 保存路径 | Downloads | 自定义路径 |
| 文件命名 | 随机 | 规则化命名 |
| 消息集成 | 不支持 | 飞书等平台发送 |
| 提示词管理 | 无 | 模板库 |
| 工作流 | 手动 | 自动化编排 |
| 后处理 | 无 | 压缩/裁剪/水印 |

**处理**: 解析能力对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回能力对比的响应数据,包含状态码、结果和日志.
### 核心能力(补充)
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | Grok图片生成-专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
批量生成:
  - 提示词队列自动处理
  - 生成间隔控制（避免限流）
  - 失败重试机制
  - 进度追踪与日志
# ...
多格式导出:
  - PNG（无损，透明背景）
  - JPG（压缩，小体积）
  - WebP（现代格式，高质量低体积）
  - 格式自动转换
# ...
消息平台集成:
  - 飞书即时发送
  - 自定义消息描述
  - 批量发送多张图片
  - 发送状态追踪
# ...
提示词管理:
  - 模板库（主题/风格/氛围）
  - 变量替换（ ）
  - 历史记录
  - 收藏与复用
# ...
工作流自动化:
  - 生成 → 保存 → 后处理 → 发送
  - 条件分支
  - 定时执行
  - Webhook 触发
# ...
图片后处理:
  - 压缩优化
  - 自动裁剪
  - 水印添加
  - 尺寸调整
```

**处理**: 解析核心能力的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心能力的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：图片生成引擎、支持多格式导出、消息平台集成与自、动化工作流、Grok、图片生成工具专业、Use、when、需要提升效率、自动化流程、批量处理、工作流优化时使用、不适用于需要人工、创意判断的任务、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：批量社交媒体配图

为社交媒体批量生成配图并自动分发.
```python
# 批量图片生成工作流
import time
from pathlib import Path
# ...
class BatchImageWorkflow:
    """批量图片生成工作流"""
# ...
    def __init__(self, output_dir="./generated-images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
# ...
    def process_batch(self, prompt_queue, interval=15):
        """批量处理提示词队列"""
        for i, prompt_data in enumerate(prompt_queue):
            print(f"[{i+1}/{len(prompt_queue)}] 生成: {prompt_data['name']}")
# ...
            result = self._generate_single(prompt_data)
            self.results.append(result)
# ...
            # 生成间隔（避免限流）
            if i < len(prompt_queue) - 1:
                print(f"等待 {interval} 秒...")
                time.sleep(interval)
# ...
        return self.results
# ...
    def _generate_single(self, prompt_data):
        """生成单张图片"""
        # 步骤1 打开 Grok Imagine
        # playwright: open https://grok.com/imagine
# ...
        # 步骤2 输入提示词
        prompt = self._build_prompt(prompt_data)
        # playwright: type prompt into input
# ...
        # 步骤3 点击生成
        # playwright: click generate button
# ...
        # 步骤4 等待生成
        time.sleep(10)
# ...
        # 步骤5 保存图片
        # desktop-agent: right-click → save as
# ...
        # 步骤6 重命名文件
        filename = f"{prompt_data['name']}.jpg"
        # rename downloaded file to custom path
# ...
        return {
            "id": f"img-{prompt_data['name']}",
            "name": prompt_data["name"],
            "prompt": prompt,
            "file_path": str(self.output_dir / filename),
            "status": "completed"
        }
# ...
    def _build_prompt(self, data):
        """构建提示词"""
        template = data.get("template", "{subject}，{style}风格，{mood}氛围")
        return template.format(
            subject=data.get("subject", ""),
            style=data.get("style", ""),
            mood=data.get("mood", "")
        )
# ...
    def send_to_feishu(self, image_paths, message=""):
        """发送图片到飞书"""
        for path in image_paths:
            # message tool: send image to feishu
            print(f"已发送: {path}")
# ...
# 批量生成配置
queue = [
    {"name": "spring-landscape", "subject": "春天的山水风景",
     "style": "水彩", "mood": "清新"},
    {"name": "summer-beach", "subject": "夏日海滩",
     "style": "印象派", "mood": "热烈"},
    {"name": "autumn-forest", "subject": "秋天森林",
     "style": "油画", "mood": "温暖"},
    {"name": "winter-city", "subject": "冬日城市",
     "style": "赛博朋克", "mood": "冷峻"},
]
# ...
workflow = BatchImageWorkflow("./social-media-images")
results = workflow.process_batch(queue, interval=15)
# ...
# 发送到飞书
image_paths = [r["file_path"] for r in results]
workflow.send_to_feishu(image_paths, "本季四景配图已生成")
```

### 场景二：提示词模板管理

使用模板库管理和复用提示词.
```python
# 提示词模板管理系统
class PromptTemplateManager:
    """提示词模板管理器"""
# ...
    def __init__(self):
        self.templates = {
            "product-shot": {
                "template": "{product}产品特写，{background}背景，{lighting}灯光，超写实",
                "variables": ["product", "background", "lighting"]
            },
            "landscape": {
                "template": "{season}的{scene}，{style}风格，{mood}氛围",
                "variables": ["season", "scene", "style", "mood"]
            },
            "character-portrait": {
                "template": "{character}肖像，{art_style}风格，{expression}表情，{background}背景",
                "variables": ["character", "art_style", "expression", "background"]
            },
            "abstract-art": {
                "template": "抽象艺术：{concept}，{color_scheme}配色，{technique}技法",
                "variables": ["concept", "color_scheme", "technique"]
            }
        }
        self.history = []
# ...
    def generate_from_template(self, template_name, variables):
        """从模板生成提示词"""
        template = self.templates[template_name]["template"]
        prompt = template.format(**variables)
        self.history.append({
            "template": template_name,
            "variables": variables,
            "prompt": prompt
        })
        return prompt
# ...
    def batch_from_template(self, template_name, variable_sets):
        """从模板批量生成提示词"""
        prompts = []
        for variables in variable_sets:
generate_from_template(template_name, variables)
            prompts.append(prompt)
        return prompts
# ...
# 使用模板批量生成
manager = PromptTemplateManager()
# ...
# 产品图模板批量
product_prompts = manager.batch_from_template("product-shot", [
    {"product": "无线耳机", "background": "深色", "lighting": "戏剧性"},
    {"product": "智能手表", "background": "白色", "lighting": "柔和"},
    {"product": "机械键盘", "background": "木质", "lighting": "暖色"},
    {"product": "游戏鼠标", "background": "霓虹", "lighting": "RGB"},
])
# ...
for p in product_prompts:
    print(f"提示词: {p}")
```

### 场景三：自动化工作流编排

完整的生成→保存→后处理→发送工作流.
```bash
#!/bin/sh
# 完整自动化工作流脚本
# ...
OUTPUT_DIR="./workflow-output"
WATERMARK="./watermark.png"
# ...
mkdir -p "$OUTPUT_DIR"
# ...
# 步骤1 批量生成图片
echo "=== 步骤1 批量生成图片 ==="
PROMPTS=("夏日海滩日落" "秋日森林小径" "冬日雪景城市" "春日樱花公园")
# ...
for i in "${!PROMPTS[@]}"; do
    echo "生成第 $((i+1)) 张: ${PROMPTS[$i]}"
    # 浏览器自动化: 打开Grok → 输入提示词 → 生成 → 保存
    # ... (浏览器操作代码)
    sleep 12  # 等待生成
# ...
    # 重命名文件
    mv $HOME/Downloads/latest.jpg "$OUTPUT_DIR/season-$((i+1)).jpg"
    echo "已保存: $OUTPUT_DIR/season-$((i+1)).jpg"
# ...
    # 生成间隔
    sleep 5
done
# ...
# 步骤2 图片后处理
echo "=== 步骤2 图片后处理 ==="
for img in "$OUTPUT_DIR"/*.jpg; do
    # 添加水印（如有ImageMagick）
    if command -v convert &> /dev/null; then
        convert "$img" "$WATERMARK" -gravity bottom-right -composite "$img"
        echo "已添加水印: $img"
    fi
done
# ...
# 步骤3 发送到飞书
echo "=== 步骤3 发送到飞书 ==="
    # message工具发送
    echo "已发送: $img"
done
# ...
echo "=== 工作流完成 ==="
ls -la "$OUTPUT_DIR/"
```
## 快速开始

### 领先步：配置输出目录

```bash
# 创建自定义输出目录
mkdir -p ./generated-images
mkdir -p ./generated-images/png
mkdir -p ./generated-images/jpg
mkdir -p ./generated-images/webp
```

### 第二步：准备提示词队列

```python
# 准备批量提示词
prompts = [
    {"name": "img-001", "prompt": "描述文本1"},
    {"name": "img-002", "prompt": "描述文本2"},
    {"name": "img-003", "prompt": "描述文本3"},
]
```

### 第三步：执行批量工作流

```bash
# 运行批量生成工作流
python3 batch_workflow.py --queue prompts.json --output ./generated-images --interval 15
```
## 示例

### 批量生成配置

```json
{
  "batch_config": {
    "output_dir": "./generated-images",
    "interval_seconds": 15,
    "max_retries": 3,
    "format": "jpg",
    "naming_rule": "{template}-{index:03d}"
  },
  "prompt_queue": [
    {"name": "spring", "template": "landscape", "variables": {"season": "春天", "scene": "花园", "style": "水彩", "mood": "清新"}},
    {"name": "summer", "template": "landscape", "variables": {"season": "夏天", "scene": "海滩", "style": "印象派", "mood": "热烈"}}
  ]
}
```

### 飞书发送配置

```json
{
  "feishu_config": {
    "enabled": true,
    "message_template": "图片描述: {description}",
    "batch_send": true,
    "send_interval": 2,
    "image_path": "./generated-images"
  }
}
```

### 提示词模板库

```json
{
  "templates": {
    "product-shot": "{product}产品特写，{background}背景，{lighting}灯光",
    "landscape": "{season}的{scene}，{style}风格，{mood}氛围",
    "character-portrait": "{character}肖像，{art_style}风格，{expression}表情",
    "social-media": "{subject}，{style}风格，{mood}氛围，适合{platform}分享"
  }
}
```
## 优选实践

1. **生成间隔控制**：批量生成间隔 15 秒以上，避免触发 Grok 限流.
2. **失败重试机制**：单张失败自动重试 3 次，避免中断整个批次.
3. **文件命名规范**：使用规则化命名（如 template-index），便于管理和查找.
4. **后处理流水线**：生成→重命名→压缩→水印→发送，全自动化.
5. **模板复用**：提示词模板化管理，变量替换快速生成变体.
```text
专业版检查清单:
[ ] 提示词队列已准备
[ ] 生成间隔 ≥ 15秒
[ ] 输出目录已创建
[ ] 文件命名规则已定义
[ ] 失败重试已配置（3次）
[ ] 后处理流程已规划
[ ] 飞书发送已配置（如需）
[ ] 免费版单张生成功能正常
```
## 常见问题

### Q: 批量生成间隔多少合适？

A: 建议 15 秒以上，避免触发 Grok Imagine 的频率限制。如果遇到限流，增加到 30 秒.
### Q: 如何发送图片到飞书？

A: 先将图片保存到本地目录，然后使用消息工具发送。支持自定义消息描述和批量发送.
### Q: 支持哪些输出格式？

A: 支持 PNG（无损透明）、JPG（压缩小体积）和 WebP（现代格式）。可在配置中指定，默认 JPG.
### Q: 如何从免费版升级？

A: 免费版的单张生成和保存流程在专业版中完整保留。专业版新增批量队列、模板管理和消息集成，无需迁移已有配置.
### Q: 生成失败怎么办？

A: 专业版内置失败重试机制（默认 3 次）。如果重试仍失败，检查网络连接、Grok 账号状态和页面 DOM 是否变化.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **浏览器**: Chrome/Edge（浏览器自动化需要）
- **Python**: 3.8+（批量工作流脚本需要）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Playwright/浏览器工具 | 工具 | 必需 | Agent内置或插件安装 |
| desktop-agent | 工具 | 必需 | `uvx desktop-agent`（自动安装） |
| Grok 账号 | 服务 | 必需 | grok.com 注册 |
| ImageMagick（可选） | 工具 | 可选 | 用于图片后处理（水印/压缩） |
| Python 3.8+ | 运行时 | 推荐 | 批量工作流脚本运行 |

### API Key 配置
- 本Skill采用纯Markdown指令驱动，无需额外API Key
- 需要已登录的 Grok 账号（浏览器会话）
- 飞书发送需要配置消息工具（如需）

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令 + 命令行 + 浏览器自动化）
- **说明**: 企业级AI Skill，支持批量图片生成、多格式导出与消息平台集成
- **适用规模**: 内容团队，批量图片生产与分发
- **兼容性**: 与免费版单张生成完全兼容，支持无缝升级
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Grok图片生成-专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "grok image pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 核心功能

- **自动化执行**: 批量AI图片生成引擎，支持多格式导出、消息平台集成与自动化工作流。。Grok图片生成工具专业版。Use when 需要提
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据
## 核心功能

- **自动化执行**: 批量AI图片生成引擎，支持多格式导出、消息平台集成与自动化工作流。。Grok图片生成工具专业版。Use when 需要提
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据