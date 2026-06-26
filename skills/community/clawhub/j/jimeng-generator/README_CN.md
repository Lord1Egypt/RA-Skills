# 即梦图片生成器

基于火山引擎即梦 AI 4.0 的图片生成工具。

即梦 4.0 在统一框架内集成了文生图、图像编辑及多图组合生成功能：支持单次输入最多 10 张图像、输出最多 15 张图像，提供智能比例检测与 4K 超高清输出。

## 安装

```bash
npm install
```

### 配置凭证

| 变量 | 是否必需 | 说明 |
|------|----------|------|
| `VOLCENGINE_AK` | 必需 | 火山引擎 Access Key |
| `VOLCENGINE_SK` | 永久凭证需要 | 火山引擎 Secret Key |
| `VOLCENGINE_TOKEN` | STS 场景需要 | 安全令牌（临时凭证） |

```bash
export VOLCENGINE_AK="<你的AK>"
export VOLCENGINE_SK="<你的SK>"
```

获取方式：[火山引擎控制台](https://console.volcengine.com/) → 访问控制 → 密钥管理

## 使用

```bash
npx ts-node scripts/generate.ts "一只坐在窗台上的可爱猫咪"
```

脚本会自动提交任务、轮询状态、下载并保存图片到 `./output/` 目录。

### 参数

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--images <url,...>` | 参考图片 URL（逗号分隔，最多 10 张） | — |
| `--width <n>` | 输出宽度 | 自动 |
| `--height <n>` | 输出高度 | 自动 |
| `--size <n>` | 输出面积（如 `4194304` = 2048×2048） | 自动 |
| `--scale <0-1>` | 文本影响程度（越大文本影响越强） | `0.5` |
| `--single` | 强制单图输出 | `false` |
| `--out <dir>` | 输出目录 | `./output` |
| `--no-save` | 不保存文件，只输出 URL | `false` |
| `--interval <ms>` | 轮询间隔 | `3000` |
| `--timeout <ms>` | 最大等待时间 | `180000` |
| `--debug` | 调试模式 | `false` |

### 示例

**智能比例文生图：**

```bash
npx ts-node scripts/generate.ts "水彩风景画，山水湖泊，16:9 比例"
```

**4K 输出：**

```bash
npx ts-node scripts/generate.ts "抽象艺术" --size 16777216
```

**图片编辑（换背景）：**

```bash
npx ts-node scripts/generate.ts "把背景换成演唱会现场" \
  --images "https://example.com/photo.jpg"
```

**多图组合：**

```bash
npx ts-node scripts/generate.ts "合成一张合照" \
  --images "https://a.jpg,https://b.jpg,https://c.jpg"
```

**指定尺寸：**

```bash
npx ts-node scripts/generate.ts "赛博朋克城市" --width 2560 --height 1440
```

## 输出格式

```json
{
  "success": true,
  "taskId": "7392616336519610409",
  "prompt": "一只可爱的猫咪",
  "count": 1,
  "files": ["./output/1.png"],
  "urls": ["https://..."]
}
```

错误：

```json
{
  "success": false,
  "error": {
    "code": "FAILED",
    "message": "错误描述"
  }
}
```

## 工作原理

1. 使用 HMAC-SHA256 签名请求（火山引擎 Header 鉴权）
2. 向 `CVSync2AsyncSubmitTask` 提交异步任务
3. 轮询 `CVSync2AsyncGetResult` 直到状态为 `done`
4. 解码 base64 图片数据并保存为 PNG 文件

## 项目结构

```
jimeng-generator/
├── scripts/
│   └── generate.ts      # 生成器脚本（签名 + API + CLI）
├── docs/
│   ├── jimengv4.md       # 即梦 4.0 API 文档
│   └── authorization.md  # 火山引擎鉴权文档
├── package.json
├── tsconfig.json
├── skill.yaml
└── _meta.json
```

## 许可证

MIT
