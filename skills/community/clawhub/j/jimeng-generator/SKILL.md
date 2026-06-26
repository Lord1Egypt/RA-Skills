---
name: jimeng-generator
description: 即梦 4.0 图片生成器，通过文本描述生成高质量图片，支持多图编辑与智能比例。
---

# 即梦 4.0 图片生成器

基于火山引擎即梦 AI 4.0 生成图片。一条命令完成：提交任务 → 等待完成 → 保存图片。

## 配置凭证

使用前需要配置火山引擎凭证。请按以下步骤操作：

1. 前往 [火山引擎控制台](https://console.volcengine.com/) → 访问控制 → 密钥管理，获取 Access Key 和 Secret Key
2. 在项目根目录创建 `.env` 文件，写入你的凭证：

```bash
VOLCENGINE_AK=你的AccessKey
VOLCENGINE_SK=你的SecretKey
```

> 如果使用 STS 临时凭证，改为填写 AK + Token：
> ```bash
> VOLCENGINE_AK=你的AccessKey
> VOLCENGINE_TOKEN=你的SecurityToken
> ```

项目已提供 `.env.example` 模板，也可以直接复制后修改：

```bash
cp .env.example .env
```

`.env` 文件已被 `.gitignore` 忽略，不会提交到仓库，请放心填写真实凭证。

## 安装

```bash
npm install
```

## 基本用法

```bash
npx ts-node scripts/generate.ts "提示词"
```

脚本会自动提交 → 轮询 → 保存图片到 `./output/`。

## 完整用法

```bash
npx ts-node scripts/generate.ts "提示词" [选项]
```

### 选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--images <url,...>` | 参考图片 URL，逗号分隔，最多 10 张 | — |
| `--width <n>` | 输出宽度 | 自动 |
| `--height <n>` | 输出高度 | 自动 |
| `--size <n>` | 输出面积 | 自动 |
| `--scale <0-1>` | 文本影响程度 | 0.5 |
| `--single` | 强制单图输出 | false |
| `--out <dir>` | 输出目录 | ./output |
| `--no-save` | 不保存，只输出 URL | false |
| `--interval <ms>` | 轮询间隔 | 3000 |
| `--timeout <ms>` | 最大等待时间 | 180000 |
| `--debug` | 调试模式 | false |

## 使用示例

### 文生图

```bash
npx ts-node scripts/generate.ts "水墨山水画"
```

### 指定尺寸

```bash
npx ts-node scripts/generate.ts "赛博朋克城市" --width 2560 --height 1440
```

### 图片编辑

```bash
npx ts-node scripts/generate.ts "背景换成星空" --images "https://example.com/photo.jpg"
```

### 多图组合

```bash
npx ts-node scripts/generate.ts "合成一张合照" --images "https://a.jpg,https://b.jpg"
```

### 强制单图 + 高影响

```bash
npx ts-node scripts/generate.ts "精细插画风格的城堡" --single --scale 0.8
```

## 输出格式

脚本结果通过 **stdout** 输出一行 JSON，便于解析。**请用其中的 `files` 数组直接作为“生成结果”返回给用户**（本地文件路径，可用来展示或附件），不要只贴直链或把本地路径藏在文案里。

成功时示例：

```json
{
  "success": true,
  "taskId": "7392616336519610409",
  "prompt": "水墨山水画",
  "count": 1,
  "files": ["/path/to/output/1.png"],
  "urls": ["https://..."]
}
```

| 字段 | 说明 |
|------|------|
| `files` | **本地文件路径数组**，即生成图片的保存位置，应作为主结果直接返回给用户 |
| `urls` | 图片直链（可选），仅作备用 |
| `taskId` | 任务 ID |
| `count` | 图片张数 |

集成建议：解析 stdout 该行 JSON，若 `success === true`，则把 `files` 中的路径作为“已生成的图片”直接提供给用户（例如展示图片或作为附件），无需再组织成“直链在这：… 本地文件在：…”的文案。

失败时错误信息在 stderr，JSON 形如：

```json
{
  "success": false,
  "error": { "code": "FAILED", "message": "错误描述" }
}
```

## 即梦 4.0 特性

- **智能比例**：可在 prompt 中描述比例，模型自动适配最优宽高
- **多图输入**：最多 10 张参考图，支持图片编辑和多图组合
- **多图输出**：单次最多输出 15 张关联图片
- **4K 输出**：支持从 1K 到 4K 分辨率
- **中文增强**：显著提升中文生成准确率

## 推荐尺寸

| 分辨率 | 1:1 | 4:3 | 3:2 | 16:9 | 21:9 |
|--------|-----|-----|-----|------|------|
| 2K | 2048×2048 | 2304×1728 | 2496×1664 | 2560×1440 | 3024×1296 |
| 4K | 4096×4096 | 4694×3520 | 4992×3328 | 5404×3040 | 6198×2656 |
