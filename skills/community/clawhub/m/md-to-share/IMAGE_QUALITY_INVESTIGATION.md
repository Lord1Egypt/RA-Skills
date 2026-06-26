# md-to-share Skill 调研报告：图片清晰度问题分析与优化建议

## 问题描述

用户使用 `md-to-share` skill 生成 Markdown 长图发送到手机时，收到的图片**远远小于预期的 1600px 宽度**，清晰度不足，且图片没有被切分。

## 核心发现

### 发现 1：OpenClaw 有两层独立的图片压缩机制

当 skill 生成的图片通过 OpenClaw 发送到消息渠道时，会经过**两个独立的压缩层**：

| 压缩层 | 位置 | 默认限制 | 触发条件 |
|--------|------|----------|----------|
| **Agent 图片清理** | `src/agents/tool-images.ts` | `1200px`, 5MB | Agent 返回包含 base64 图片的 tool result |
| **媒体加载优化** | `src/web/media.ts` | 6MB → 逐步缩小到 800px | 通过 `loadWebMedia()` 加载图片发送到渠道 |

### 发现 2：md2img.mjs 的配置与 OpenClaw 限制不匹配

**md2img.mjs 的配置** (`md2img.mjs:28-44`):
```javascript
const CONFIG = {
  width: 800,              // CSS 像素
  deviceScaleFactor: 2,    // 实际输出 1600px
  jpegQuality: 85,
  maxFileSizeMB: 8,        // Discord 限制
};
```

**问题**：
- md2img 生成 1600px 宽度的图片
- OpenClaw Agent 层默认限制 `1200px`，会将图片缩小
- 如果图片超过 6MB，媒体加载层会进一步从 2048px → 800px 逐步缩小

### 发现 3：图片切分逻辑在 skill 层无效

md2img.mjs 的切分逻辑（第 524-588 行）基于文件大小（8MB）触发，但：
1. OpenClaw 的压缩在**内存中**处理 base64 数据
2. 压缩逻辑优先检查**尺寸**而非文件大小
3. 即使 skill 输出多个切分文件，每个文件仍会被独立压缩

### 发现 4：用户无法通过配置绕过压缩

| 配置项 | 作用域 | 能否解决清晰度问题 |
|--------|--------|-------------------|
| `agents.defaults.imageMaxDimensionPx` | Agent 层 | 部分解决（但媒体加载层仍会压缩） |
| `agents.defaults.mediaMaxMb` | Agent 层 | 只影响大小限制，不影响尺寸 |
| 渠道级 `mediaMaxMb` | 渠道层 | 只影响大小限制，不影响尺寸 |

**关键问题**：OpenClaw 没有提供 "发送原始图片不压缩" 的配置选项。

## 技术细节

### 压缩流程详解

```
Skill 生成图片 (1600px)
    ↓
Agent Tool Result (base64)
    ↓
[第一层] sanitizeContentBlocksImages() ← src/agents/tool-images.ts:269-335
    │  限制: maxDimensionPx=1200, maxBytes=5MB
    │  使用 buildImageResizeSideGrid() 逐步缩小
    │  尺寸网格: [sideStart, 1800, 1600, 1400, 1200, 1000, 800]
    │  质量网格: [85, 75, 65, 55, 45, 35]
    ↓
消息发送 → loadWebMedia()
    ↓
[第二层] optimizeImageToJpeg() ← src/web/media.ts:426-491
    │  限制: MAX_IMAGE_BYTES=6MB
    │  尺寸网格: [2048, 1536, 1280, 1024, 800]
    │  质量网格: [80, 70, 60, 50, 40]
    │  如果图片 > 6MB，从 2048px 开始逐步缩小
    ↓
发送到渠道 (Telegram/Discord/WhatsApp 等)
```

### 关键代码位置

1. **Agent 图片清理入口**：
   - `src/agents/tool-images.ts:269` - `sanitizeContentBlocksImages()`
   - `src/agents/image-sanitization.ts:8-9` - 默认限制常量

2. **媒体加载优化入口**：
   - `src/web/media.ts:404` - `loadWebMedia()`
   - `src/web/media.ts:426` - `optimizeImageToJpeg()`
   - `src/media/constants.ts:1` - `MAX_IMAGE_BYTES = 6MB`

3. **尺寸/质量网格**：
   - `src/media/image-ops.ts:15-20` - Agent 层网格
   - `src/web/media.ts:445-446` - 媒体加载层网格

4. **绕过压缩的例子**（仅特定场景）：
   - `src/web/media.ts:415` - `loadWebMediaRaw()` (不优化)
   - `src/discord/send.emojis-stickers.ts:14,38` - Discord emoji/sticker 使用 raw 模式

## 问题根因总结

| 问题 | 根因 | skill 能否自行解决 |
|------|------|-------------------|
| 图片被缩小到 1200px 以下 | Agent 层 `imageMaxDimensionPx=1200` | 否（用户配置决定） |
| 大图片被进一步压缩 | 媒体加载层 6MB 限制 + 优化逻辑 | 否（系统内置） |
| 切分功能无效 | OpenClaw 压缩在内存中处理，切分后仍被压缩 | 部分有效（可减小单个文件大小） |
| 不同渠道行为不一致 | 各渠道使用不同的 `maxBytes` | 部分有效（需针对渠道优化） |

## 优化建议

### 方案 A：Skill 层优化（推荐，skill 可自行实现）

1. **降低输出分辨率到 1200px 以内**
   - 将 `width=800, deviceScaleFactor=2` 改为 `width=600, deviceScaleFactor=2` (1200px)
   - 或 `width=800, deviceScaleFactor=1.5` (1200px)
   - 好处：避免 Agent 层压缩，保持 skill 控制的质量
   - 缺点：分辨率降低

2. **针对不同渠道输出不同尺寸**
   - 检测目标渠道，调整输出尺寸
   - 例如：Telegram 发送 1280px，Discord 发送 1024px

3. **优化切分逻辑**
   - 将切分阈值从 8MB 降低到 5MB（匹配 Agent 层限制）
   - 切分后确保每段 < 5MB，避免媒体加载层二次压缩

4. **提供质量/尺寸参数**
   - 让调用者指定目标分辨率（如 `--max-width 1200`）
   - 自动适应当前 OpenClaw 配置

### 方案 B：OpenClaw 层修改（需要提交 PR）

1. **添加 `loadWebMediaRaw` 的使用场景**
   - 为 "高清图片" 类消息提供绕过压缩的路径
   - 例如：`message send --raw` 或 `message send --no-optimize`

2. **提高默认 `imageMaxDimensionPx`**
   - 从 1200px 提高到 1600px 或 2000px
   - 平衡清晰度与性能

3. **添加 per-message 图片质量控制**
   - 允许 skill 在返回结果时指定 `preserveQuality: true`

### 方案 C：文档与用户指导

1. **在 skill 文档中说明限制**
   - 告知用户默认 1200px 限制
   - 提供配置调整指南

2. **检测并警告**
   - 如果生成的图片 > 1200px，输出警告日志
   - 建议用户调整配置或降低输出分辨率

## 验证测试

修改后应测试以下场景：

1. **基础测试**：
   ```bash
   # 生成 1200px 宽度的图片
   node md2img.mjs test.md output.jpg
   # 验证输出图片宽度 <= 1200px
   ```

2. **长图切分测试**：
   ```bash
   # 生成超过 5MB 的长图
   # 验证切分后每个文件 < 5MB
   ```

3. **渠道测试**：
   - Telegram 发送
   - Discord 发送
   - WhatsApp 发送
   - 验证各渠道收到的图片清晰度

## 结论

**核心问题**：OpenClaw 的图片处理流程针对 API 限制和传输效率优化，会自动压缩大图。Skill 生成的 1600px 图片会经过两层压缩，最终用户收到的图片远小于预期。

**推荐方案**：
1. 短期：修改 skill，将输出分辨率调整到 1200px 以内，切分阈值降到 5MB
2. 长期：向 OpenClaw 提交 PR，添加高清图片发送支持

## 附录：相关文件路径

```
# OpenClaw 源码
src/agents/tool-images.ts          # Agent 图片清理
src/agents/image-sanitization.ts   # 图片清理限制常量
src/web/media.ts                   # 媒体加载优化
src/media/image-ops.ts             # 图片操作工具
src/media/constants.ts             # 媒体大小常量
src/telegram/send.ts               # Telegram 发送
src/discord/send.outbound.ts       # Discord 发送
src/discord/send.emojis-stickers.ts # Discord emoji/sticker (raw 模式示例)

# md-to-share skill
md2img.mjs                         # 主脚本
CLAUDE.md                          # 项目说明
```
