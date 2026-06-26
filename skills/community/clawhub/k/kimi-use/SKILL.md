# Kimi Use

Kimi AI 工具集，提供对话、图像理解、翻译等功能。使用 Node.js 实现。

## 环境变量

```bash
export KIMI_API_KEY="sk-kimi-xxxx"                              # 必填（Kimi For Coding 格式）
export KIMI_API_HOST="https://api.kimi.com/coding"               # Kimi For Coding 端点
export KIMI_MODEL="kimi-for-coding"                              # 可选，默认 kimi-for-coding
export KIMI_VISION_MODEL="kimi-vl-flash"                         # 可选，默认 kimi-vl-flash
```

获取 API Key: https://www.kimi.com/code/user-center/basic-information/interface-key

## 安装依赖

```bash
cd ~/workspace/skills/kimi-use
npm install
```

## CLI 命令

```bash
# 对话
node scripts/index.js chat "你好，介绍一下你自己"

# 图像理解（支持本地路径或 URL）
node scripts/index.js image "这张图片里有什么？" /path/to/image.jpg

# 翻译
node scripts/index.js translate "hello world" --to 中文

# 网络搜索（依赖模型知识库）
node scripts/index.js search "今日新闻"

# 流式输出
node scripts/index.js chat "讲一个故事" --stream
```

## Node.js 模块调用

```javascript
import { chat, understandImage, translate, webSearch } from './scripts/index.js';

// 对话
const r = await chat('你好');
console.log(r.result.content);

// 图像理解
const r = await understandImage('这张图里字幕在什么位置？用JSON返回', '/path/to/image.jpg');
console.log(r.result.content);

// 翻译
const r = await translate('hello', { to: 'Chinese' });
console.log(r.result.content);
```

## API 详情

- **API 地址**: `https://api.kimi.com/coding/v1`
- **模型**: kimi-for-coding, kimi-vl-flash (视觉)
- **视觉**: 支持本地 base64 图片和 URL
- **兼容**: OpenAI SDK 风格
