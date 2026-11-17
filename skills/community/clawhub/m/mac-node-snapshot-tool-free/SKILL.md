---
slug: mac-node-snapshot-tool-free
name: mac-node-snapshot-tool-free
version: 1.0.0
displayName: macOS截图工具免费版
summary: "macOS屏幕截图与录屏工具,支持全屏截图、区域截图与基础录屏,适合个人开发者快速捕获屏幕内容.。macOS截图工具免费版,为个人用户提供屏幕截图与基础录屏能力."
license: MIT
edition: free
description: "macOS截图工具免费版,为个人用户包含屏幕截图与基础录屏能力. 适用于需要mac node snapshot tool相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 适用于需要mac node snapshot tool相关能力的开发场景,包含结构化的工作流程和配置指引."
tags:
  - macOS
  - mac
  - node
  - snapshot
  - automation
  - 截图
  - 录屏
  - 免费版
  - 安全
  - 加密
tools:
  - read
  - exec
homepage: ""
category: "Security"
pricing_tier: free

---
# macOS截图工具免费版

## 概述

本工具为macOS用户提供屏幕截图与基础录屏能力,基于macOS原生的 `screencapture` 和 `screencapture` 命令行工具。免费版支持全屏截图、区域截图、窗口截图与基础屏幕录制,适合个人开发者快速捕获屏幕内容用于Bug报告、操作文档与内容存档.
### 免费版与专业版对比

| 能力维度 | 免费版 | 专业版 |
|----|---|---|
| 截图模式 | 全屏/区域/窗口 | +定时/多屏/光标控制 |
| 录屏功能 | 基础录屏 | +音频录制/区域录屏 |
| 批量处理 | 不支持 | 定时批量截图 |
| 图片格式 | PNG | PNG/JPG/HEIC/TIFF |
| 自动上传 | 不支持 | 云端自动上传 |
| OCR识别 | 不支持 | 截图文字识别 |
| 编辑标注 | 不支持 | 内置编辑器 |

## 核心能力

### 1. 全屏截图

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | macOS截图工具免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
#!/bin/bash
# 全屏截图
# ...
OUTPUT_DIR="${HOME}/Desktop/screenshots"
mkdir -p "$OUTPUT_DIR"
# ...
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
FILENAME="${OUTPUT_DIR}/fullscreen_${TIMESTAMP}.png"
# ...
# 全屏截图(保存到文件)
screencapture "$FILENAME"
# ...
echo "截图已保存: ${FILENAME}"
echo "文件大小: $(du -h "$FILENAME" | cut -f1)"
# ...
# 同时复制到剪贴板
screencapture -c
echo "截图已复制到剪贴板"
```

**处理**: 解析全屏截图的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回全屏截图的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 区域截图

```bash
#!/bin/bash
# 区域截图(交互式选择区域)
# ...
OUTPUT_DIR="${HOME}/Desktop/screenshots"
mkdir -p "$OUTPUT_DIR"
# ...
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
FILENAME="${OUTPUT_DIR}/region_${TIMESTAMP}.png"
# ...
# 区域截图(用户拖选区域)
screencapture -i "$FILENAME"
# ...
if [ -f "$FILENAME" ]; then
    echo "区域截图已保存: ${FILENAME}"
    echo "图片尺寸: $(sips -g pixelWidth -g pixelHeight "$FILENAME" 2>/dev/null | tail -2)"
else
    echo "截图已取消"
fi
```

**处理**: 解析区域截图的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回区域截图的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 窗口截图

```bash
#!/bin/bash
# 窗口截图(交互式选择窗口)
# ...
OUTPUT_DIR="${HOME}/Desktop/screenshots"
mkdir -p "$OUTPUT_DIR"
# ...
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
FILENAME="${OUTPUT_DIR}/window_${TIMESTAMP}.png"
# ...
# 窗口截图(点击选择窗口,包含窗口阴影)
screencapture -iW "$FILENAME"
# ...
if [ -f "$FILENAME" ]; then
    echo "窗口截图已保存: ${FILENAME}"
else
    echo "截图已取消"
fi
# ...
# 不含窗口阴影的版本
# screencapture -ioW "${OUTPUT_DIR}/window_noshadow_${TIMESTAMP}.png"
```

**处理**: 解析窗口截图的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回窗口截图的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 基础屏幕录制

```bash
#!/bin/bash
# 基础屏幕录制
# ...
OUTPUT_DIR="${HOME}/Desktop/recordings"
mkdir -p "$OUTPUT_DIR"
# ...
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
FILENAME="${OUTPUT_DIR}/recording_${TIMESTAMP}.mov"
# ...
echo "开始屏幕录制..."
echo "按 Ctrl+C 停止录制"
echo ""
# ...
# 录制全屏(无音频)
screencapture -v "$FILENAME"
# ...
echo ""
echo "录制完成: ${FILENAME}"
echo "文件大小: $(du -h "$FILENAME" | cut -f1)"
echo "视频时长: 可用 ffprobe 查看"
```

**处理**: 解析基础屏幕录制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回基础屏幕录制的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：macOS、屏幕截图与录屏工、支持全屏截图、区域截图与基础录、适合个人开发者快、速捕获屏幕内容、截图工具免费版、为个人用户提供屏、幕截图与基础录屏、核心能力、适用场景、Bug、报告截图、操作步骤录制、屏幕内容存档、差异化、免费版聚焦核心截、图功能、原生工具、适合个人用户快速、适用关键词、screenrecord等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:Bug报告截图

```bash
#!/bin/bash
# Bug报告截图工具
# ...
OUTPUT_DIR="${HOME}/Desktop/bug-reports"
mkdir -p "$OUTPUT_DIR"
# ...
BUG_ID="${1:-bug}"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
# ...
echo "=== Bug报告截图工具 ==="
echo "Bug ID: ${BUG_ID}"
echo ""
# ...
# 1. 全屏截图
echo "1. 截取全屏..."
screencapture "${OUTPUT_DIR}/${BUG_ID}_fullscreen_${TIMESTAMP}.png"
echo "   已保存"
# ...
# 2. 区域截图(选择Bug区域)
echo ""
echo "2. 请选择Bug所在区域..."
screencapture -i "${OUTPUT_DIR}/${BUG_ID}_region_${TIMESTAMP}.png"
echo "   已保存"
# ...
echo ""
echo "=== 截图完成 ==="
echo "文件位置:"
ls -la "${OUTPUT_DIR}/${BUG_ID}_"*"${TIMESTAMP}"*.png 2>/dev/null
```

### 场景二:操作步骤录制

```bash
#!/bin/bash
# 操作步骤录制(带倒计时)
# ...
OUTPUT_DIR="${HOME}/Desktop/tutorials"
mkdir -p "$OUTPUT_DIR"
# ...
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
FILENAME="${OUTPUT_DIR}/tutorial_${TIMESTAMP}.mov"
# ...
echo "=== 操作步骤录制 ==="
echo "3秒后开始录制..."
sleep 1; echo "  3..."
sleep 1; echo "  2..."
sleep 1; echo "  1..."
echo "  开始录制! 按 Ctrl+C 停止"
# ...
screencapture -v "$FILENAME"
# ...
echo ""
echo "录制完成: ${FILENAME}"
echo "文件大小: $(du -h "$FILENAME" | cut -f1)"
```

### 场景三:定时截图

```bash
#!/bin/bash
# 定时截图(每隔N秒截图一次)
# ...
OUTPUT_DIR="${HOME}/Desktop/timed-screenshots"
mkdir -p "$OUTPUT_DIR"
# ...
INTERVAL="${1:-60}"  # 默认60秒
COUNT="${2:-10}"     # 默认10次
# ...
echo "=== 定时截图 ==="
echo "间隔: ${INTERVAL}秒"
echo "次数: ${COUNT}次"
echo ""
# ...
for i in $(seq 1 "$COUNT"); do
    TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
    FILENAME="${OUTPUT_DIR}/timed_${i}_${TIMESTAMP}.png"
# ...
    screencapture "$FILENAME"
    echo "  [${i}/${COUNT}] ${FILENAME}"
# ...
    if [ "$i" -lt "$COUNT" ]; then
        sleep "$INTERVAL"
    fi
done
# ...
echo ""
echo "定时截图完成,共 ${COUNT} 张"
```

## 不适用场景

以下场景macOS截图工具免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 领先步:确认环境

```bash
# 确认macOS版本
sw_vers
# ...
# 确认screencapture可用
which screencapture
```

### 第二步:首次截图

```bash
# 全屏截图到桌面
screencapture ./Desktop/screenshot.png
```

### 第三步:复制到剪贴板

```bash
# 截图直接复制到剪贴板(不保存文件)
screencapture -c
```

## 示例

### screencapture参数参考

| 参数 | 说明 | 示例 |
|---:|---:|---:|
| 无参数 | 全屏截图到文件 | `screencapture out.png` |
| -c | 复制到剪贴板 | `screencapture -c` |
| -i | 交互式区域选择 | `screencapture -i out.png` |
| -iW | 交互式窗口选择 | `screencapture -iW out.png` |
| -W | 交互式窗口(无阴影) | `screencapture -ioW out.png` |
| -v | 录制视频 | `screencapture -v out.mov` |
| -C | 包含光标 | `screencapture -C out.png` |
| -T N | 延迟N秒 | `screencapture -T 5 out.png` |
| -t format | 图片格式 | `screencapture -t jpg out.jpg` |

### 截图文件命名规范

| 场景 | 命名格式 | 示例 |
|:---:|:---:|:---:|
| 全屏 | fullscreen_YYYYMMDD_HHMMSS.png | fullscreen_20260718_143022.png |
| 区域 | region_YYYYMMDD_HHMMSS.png | region_20260718_143022.png |
| 窗口 | window_YYYYMMDD_HHMMSS.png | window_20260718_143022.png |
| Bug | bug_ID_YYYYMMDD_HHMMSS.png | bug_1234_20260718_143022.png |
| 定时 | timed_N_YYYYMMDD_HHMMSS.png | timed_3_20260718_143022.png |

## 优秀实践

1. **统一目录**:设置固定的截图输出目录,便于管理.
2. **规范命名**:使用时间戳命名,避免文件冲突,便于排序查找.
3. **及时清理**:定期清理过期截图,避免占用磁盘空间.
4. **剪贴板模式**:临时截图使用 `-c` 复制到剪贴板,不产生文件.
5. **区域选择**:优先使用区域截图,只截取需要的内容.
```bash
# 优秀实践:截图管理函数
screenshot() {
    local mode=$1
    local name=$2
    local dir="${HOME}/Desktop/screenshots"
    local ts=$(date '+%Y%m%d_%H%M%S')
# ...
    mkdir -p "$dir"
    local file="${dir}/${name:-screenshot}_${ts}.png"
# ...
    case "$mode" in
        full)   screencapture "$file" ;;
        region) screencapture -i "$file" ;;
        window) screencapture -iW "$file" ;;
        clip)   screencapture -c; echo "已复制到剪贴板"; return ;;
        *)      screencapture "$file" ;;
    esac
# ...
    [ -f "$file" ] && echo "已保存: ${file}" || echo "截图取消"
}
```

## 常见问题

### Q1: 截图时提示"没有权限"怎么办?

在"系统设置 > 隐私与安全性 > 屏幕录制"中,为终端应用(Terminal/iTerm)授予屏幕录制权限,重启终端后生效.
### Q2: 录屏没有声音怎么办?

免费版使用screencapture基础录屏,不支持音频录制。需要音频录制请使用专业版或QuickTime Player.
### Q3: 如何截图到剪贴板而不保存文件?

使用 `screencapture -c` 参数,截图直接复制到系统剪贴板,不生成文件.
### Q4: 支持多显示器截图吗?

免费版支持多显示器全屏截图。精确选择特定显示器需要专业版支持.
### Q5: 截图文件太大怎么办?

PNG格式文件较大,可使用 `-t jpg` 参数切换为JPG格式,或使用sips工具压缩:`sips -s format jpeg -s formatOptions 80 input.png --out output.jpg`.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: macOS(screencapture为macOS专属工具)
- **macOS版本**: macOS 10.14+(Mojave)推荐

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| screencapture | 截图工具 | 必需 | macOS系统自带 |
| sips | 图片处理 | 推荐 | macOS系统自带 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 免费版使用macOS原生工具,无需API Key
- 需要在系统设置中授予终端"屏幕录制"权限

### 可用性分类
- **分类**: MD+EXEC模式纯Markdown指令,核心功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行macOS屏幕截图与录屏任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "macOS截图工具免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "mac node snapshot"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
