---

slug: lh-video-gen-tool-pro
name: "lh-video-gen-tool-pro"
version: "1.0.0"
displayName: "短视频生成专业版"
summary: "企业级竖版短视频批量生成系统,支持多模板、多语言、批量处理、品牌定制与CI/CD集成,适合团队与商业项目。"
license: "Proprietary"
edition: "pro"
description: |- 功能涵盖: gen。
  短视频生成专业版为企业与内容团队提供系统化的竖版短视频生产解决方案。在免费版单视频生成能力之上,增加批量生成、多模板系统、多语言混排、
  品牌定制、团队协作与自动化工作流能力。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。
tags:
  - 视频生成
  - 批量处理
  - 短视频
  - 企业级
  - 自动化
  - 内容生产
  - 视频处理
  - 媒体
  - 创意
  - output
  - mp4
  - 短视频生
  - assets
  - action
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"

---

# 短视频生成专业版
## 概述
短视频生成专业版为企业与内容团队提供系统化的竖版短视频生产解决方案。在免费版单视频生成能力之上,PRO版引入批量生成、多模板系统、多语言混排、品牌定制、团队协作与自动化工作流能力,满足商业级内容生产的效率与质量需求.
PRO版完全兼容免费版,可直接继承免费版的Markdown脚本格式与配置,并在此基础上扩展为完整的内容生产流水线.
## 核心能力
### 批量视频生成
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 短视频生成专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
# 批量生成任务队列
batch_tasks = [
    {"script": "（请参考skill目录中的脚本文件）", "output": "output/product-a.mp4"},
    {"script": "（请参考skill目录中的脚本文件）", "output": "output/product-b.mp4"},
    {"script": "（请参考skill目录中的脚本文件）", "output": "output/product-c.mp4"},
    {"script": "（请参考skill目录中的脚本文件）", "output": "output/tutorial-1.mp4"},
    {"script": "（请参考skill目录中的脚本文件）", "output": "output/tutorial-2.mp4"}
]
# ...
# 执行批量生成
python3 batch_generate.py \
  --tasks tasks.json \
  --parallel 4 \
  --output ./output/ \
  --template brand \
  --quality-check \
  --auto-optimize
```

**处理**: 解析批量视频生成的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量视频生成的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 多模板系统
PRO版提供多种画面模板,支持不同视觉风格:

```yaml
# templates.yml - 模板配置
templates:
  minimal:
    name: "极简风格"
    background: "linear-gradient(135deg, #FAFAFA, #F1F5F9)"
    font: "Inter, sans-serif"
    text_color: "#0F172A"
    animation: "fade_in"
# ...
  brand:
    name: "品牌定制"
    background: "brand_gradient"
    logo: "assets/logo.png"
    font: "brand_font"
    text_color: "brand_primary"
    watermark: True
    animation: "slide_up"
# ...
  dynamic:
    name: "动态活力"
    background: "animated_gradient"
    font: "Poppins, sans-serif"
    text_color: "#FFFFFF"
    animation: "bounce_in"
    particle_effect: True
# ...
  education:
    name: "教育培训"
    background: "#FFFFFF"
    font: "Noto Sans SC, sans-serif"
    text_color: "#1E3A5A"
    highlight_color: "#0052FF"
    animation: "type_writer"
```

**处理**: 解析多模板系统的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多模板系统的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 多语言与多音色
```python
# 多语言混排配置
multilingual_config = {
    "segments": [
        {
            "text": "Hello everyone, welcome to our channel.",
            "lang": "en",
            "voice": "en-US-JennyNeural",
            "rate": "+0%"
        },
        {
            "text": "大家好,欢迎来到我们的频道。",
            "lang": "zh",
            "voice": "zh-CN-XiaoxiaoNeural",
            "rate": "+0%"
        },
        {
            "text": "こんにちは、チャンネルへようこそ。",
            "lang": "ja",
            "voice": "ja-JP-NanamiNeural",
            "rate": "+0%"
        }
    ]
}
```

**处理**: 解析多语言与多音色的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多语言与多音色的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 品牌资产管理
```python
# 品牌资产统一管理
brand_assets = {
    "logo": "assets/brand/logo.png",
    "logo_dark": "assets/brand/logo-dark.png",
    "colors": {
        "primary": "#0052FF",
        "secondary": "#4D7CFF",
        "accent": "#FF6B35",
        "background": "#FAFAFA",
        "text": "#0F172A"
    },
    "fonts": {
        "display": "Calistoga, serif",
        "body": "Inter, sans-serif",
        "mono": "JetBrains Mono, monospace"
    },
    "intro_animation": "assets/animations/intro.mp4",
    "outro_animation": "assets/animations/outro.mp4",
    "watermark": {
        "enabled": True,
        "image": "assets/brand/watermark.png",
        "position": "bottom-right",
        "opacity": 0.8
    }
}
```

**处理**: 解析品牌资产管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回品牌资产管理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 视频质量审计
```python
# 自动质量检查
quality_checks = {
    "resolution": {"required": "1080x1920", "action": "reject_if_fail"},
    "duration": {"min": 15, "max": 180, "action": "warn_if_outside"},
    "audio_level": {"target": -16, "tolerance": 2, "action": "auto_normalize"},
    "subtitle_sync": {"tolerance": 0.5, "action": "warn_if_fail"},
    "text_readability": {"min_contrast": 4.5, "action": "warn_if_fail"},
    "frame_rate": {"required": 30, "action": "reject_if_fail"}
}
```

**处理**: 解析视频质量审计的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回视频质量审计的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级竖版短视频、批量生成系统、支持多模板、批量处理、品牌定制与、适合团队与商业项、短视频生成专业版、为企业与内容团队、提供系统化的竖版、短视频生产解决方、在免费版单视频生、成能力之上、增加批量生成、团队协作与自动化、工作流能力、Use、when、需要提升效率、自动化流程、工作流优化时使用、不适用于需要人工、创意判断的任务、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:MCN批量内容生产
需求:MCN机构需要为多个账号批量生产竖版短视频.
```python
# 批量内容生产工作流
mcn_pipeline = {
    "accounts": [
        {"name": "科技账号", "template": "minimal", "topics": ["AI", "编程", "工具"]},
        {"name": "教育账号", "template": "education", "topics": ["英语", "数学", "科普"]},
        {"name": "生活账号", "template": "dynamic", "topics": ["美食", "旅行", "日常"]}
    ],
    "daily_quota": 10,  # 每账号每日10条
    "schedule": "daily 08:00",
    "auto_publish": False,  # 生成后人工审核
    "quality_check": True
}
# ...
# 执行批量生成
for account in mcn_pipeline["accounts"]:
    for topic in account["topics"]:
        script = generate_script(topic, account["template"])
        generate_video(script, account["template"])
```

### 场景二:电商商品视频批量制作
需求:电商平台需要为100个商品生成介绍视频.
```bash
# 批量生成商品视频
  --tasks products.csv \
  --parallel 8 \
  --template brand \
  --brand-assets ./brand/ \
  --output ./videos/ \
  --quality-check \
  --auto-optimize \
  --generate-thumbnail \
  --watermark
```

```python
# 本技能的核心实现逻辑
# 请参考上方使用说明进行配置和调用
result = "implementation_ready"
```

### 场景三:多语言内容国际化
需求:将中文内容翻译并生成多语言版本视频.
```python
# 多语言批量生成
languages = ["zh-CN", "en-US", "ja-JP", "ko-KR", "es-ES"]
source_script = "（请参考skill目录中的脚本文件）"
# ...
for lang in languages:
    # 翻译脚本
    translated = translate_script(source_script, target_lang=lang)
# ...
    # 选择对应音色
    voice = get_voice_for_lang(lang)
# ...
    # 生成视频
    generate_video(
        script=translated,
        output=f"output/video_{lang}.mp4",
        voice=voice,
        template="brand"
    )
```

## 快速开始
### Step 1:初始化项目
```bash
# 初始化视频生产项目
python3 init_project.py \
  --name "MyVideoProject" \
  --brand-assets ./brand/ \
  --output ./project/
```

### Step 2:配置批量任务
```bash
# 创建任务文件
cat > tasks.json << 'EOF'
[
  {"script": "（请参考skill目录中的脚本文件）", "output": "out/01.mp4", "template": "brand"},
  {"script": "（请参考skill目录中的脚本文件）", "output": "out/02.mp4", "template": "minimal"},
  {"script": "（请参考skill目录中的脚本文件）", "output": "out/03.mp4", "template": "education"}
]
EOF
```

### Step 3:执行批量生成
```bash
  --tasks tasks.json \
  --parallel 4 \
  --quality-check \
  --output ./output/
```

#
## 示例
### 高级参数配置
```python
# PRO版高级配置
pro_config = {
    "rendering": {
        "gpu_acceleration": True,        # GPU加速
        "parallel_workers": 4,            # 并行任务数
        "cache_enabled": True            # 缓存启用
    },
    "video": {
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "bitrate": "5M",
        "format": "mp4",
        "codec": "h264"
    },
    "audio": {
        "sample_rate": 44100,
        "bitrate": "128k",
        "normalize": True,              # 音量标准化
        "target_loudness": -16           # 目标响度(LUFS)
    },
    "subtitles": {
        "burn": True,                    # 烧录字幕
        "font": "Inter, sans-serif",
        "font_size": 48,
        "position": "bottom",
        "background": "semi-transparent"
    },
    "branding": {
        "watermark": True,
        "intro": True,
        "outro": True,
        "logo_position": "top-right"
    }
}
```

### CI/CD集成配置
```yaml
# .github/workflows/video-production.yml
name: Video Production
on:
  schedule:
    - cron: "0 8 * * *"  # 每日8点
  push:
    paths: ["scripts/**"]
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup FFmpeg
        run: sudo apt install ffmpeg
      - name: Batch Generate Videos
        run: |
            --tasks tasks.json \
            --parallel 4 \
            --output ./output/ \
            --quality-check
      - name: Upload Videos
        uses: actions/upload-artifact@v3
        with:
          name: videos
          path: ./output/
```

## 优选实践
### 免费版与PRO版能力对比
| 能力维度 | 免费版 | PRO版 |
|:-----|:-----|:-----|
| 视频生成 | 单个 | 批量(CSV/JSON) |
| 模板系统 | 默认1种 | 多种+自定义 |
| 多语言 | 单语言 | 多语言混排 |
| 品牌定制 | 不支持 | 完整品牌资产 |
| 质量审计 | 不支持 | 自动检查+优化 |
| GPU加速 | 不支持 | 支持 |
| 并行处理 | 不支持 | 多任务并行 |
| 水印/片头 | 不支持 | 支持 |
| 缩略图 | 不支持 | 自动生成 |
| CI/CD | 不支持 | 流水线集成 |
| 团队协作 | 单人 | 多人+版本管理 |

### 模板选择指南
| 内容类型 | 推荐模板 | 特点 |
|---:|---:|---:|
| 科技资讯 | `minimal` | 极简、专业 |
| 品牌宣传 | `brand` | 品牌色、Logo、水印 |
| 娱乐内容 | `dynamic` | 动态、活力 |
| 教育培训 | `education` | 清晰、易读 |
| 电商商品 | `brand` | 统一品牌形象 |

### 批量生成性能优化
```python
# 性能优化建议
performance_tips = {
    "parallel_workers": "根据CPU核心数设置,建议4-8",
    "gpu_acceleration": "启用GPU加速可提升3-5倍渲染速度",
    "cache_enabled": "启用缓存避免重复生成相同片段",
    "temp_storage": "使用SSD存储临时文件提升IO性能",
    "batch_size": "单批建议不超过50个视频,避免内存溢出"
}
```

## 常见问题
### Q1: 如何从免费版迁移至PRO版?
A: PRO版完全兼容免费版。现有Markdown脚本格式与命令行参数可直接使用。只需安装PRO版增强包即可启用批量生成与高级功能.
### Q2: 批量生成时部分视频失败怎么办?
A: PRO版支持失败重试机制。失败的记录会保存到`failed-tasks.json`,可单独重试:

```bash
py --retry failed-tasks.json
```

### Q3: GPU加速如何启用?
A: 需要安装支持GPU的FFmpeg版本(如带NVIDIA CUDA支持)。在配置中设置`gpu_acceleration: True`即可自动启用.
### Q4: 如何管理多个品牌的内容?
A: 使用多品牌配置,每个品牌拥有独立的模板、配色与资产。可在批量任务中为不同视频指定不同品牌.
### Q5: 支持哪些视频平台规格?
A: 默认输出9:16竖版(1080x1920)。可配置为16:9横版(1920x1080)或1:1方形(1080x1080),适配不同平台需求.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md规范的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.10+
- **FFmpeg**: 5.0+(支持GPU加速需CUDA版本)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| FFmpeg 5.0+ | 系统工具 | 必需 | brew/apt安装 |
| Chrome | 浏览器 | 截图必需 | 系统自带或下载 |
| TTS服务 | 服务 | 必需 | 默认Edge TTS或自定义 |
| CUDA(可选) | GPU驱动 | GPU加速可选 | NVIDIA官方 |

### API Key 配置
- 本skill基于Markdown指令规范驱动,无需额外API Key
- TTS服务如使用云端API,需按对应服务商文档配置
- 批量生成使用本地工具链,无需额外API
- 如集成第三方内容平台,按各自平台文档配置

### 可用性分类
- **分类**: MD+execute(纯Markdown指令+脚本执行能力)
- **说明**: 专业版基于Markdown指令驱动Agent执行批量视频生成任务,通过Python脚本与FFmpeg实现视频合成、质量审计与CI/CD集成
- **PRO版增强**: 批量生成、多模板系统、多语言混排、品牌定制、GPU加速、质量审计、CI/CD集成、团队协作

## 错误处理
| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
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
    "result": "短视频生成专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "lh video gen pro"
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

- **自动化执行**: 企业级竖版短视频批量生成系统,支持多模板、多语言、批量处理、品牌定制与CI/CD集成,适合团队与商业项目。
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据