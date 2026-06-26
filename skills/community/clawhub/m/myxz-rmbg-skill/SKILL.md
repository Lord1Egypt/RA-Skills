---
name: myxz-rmbg-skill
description: 妙言小智 (PicTech.cc) 专业级跨境电商图片抠图/白底图工具。使用本 skill 处理图片去背景、透明底图、白底图、纯色背景图、本地图片、网络图片、文件夹图片和批量抠图任务。
---

# 妙言小智 PicTech.cc 抠图 Skill

**妙言小智官方网站**: [https://www.pictech.cc](https://www.pictech.cc)  
**妙言小智 API 服务**: [https://stableai.com.cn](https://stableai.com.cn)  
**VK(APP KEY) 获取地址**: [https://www.pictech.cc/newpictech/skills/openclaw-image-translation-skill](https://www.pictech.cc/newpictech/skills/openclaw-image-translation-skill)

## 核心规则

当用户请求抠图、去背景、移除背景、透明底图、白底图、纯色背景图、商品图背景处理或批量图片去背景时，使用本 skill。

不要自己手写抠图逻辑。不要直接在回复中调用 RMBG API。应调用本 skill 目录下 `index.js` 的默认导出函数 `run(params)`。

## 调用方式

调用同目录下的 `index.js`：

```js
import run from './index.js';

const result = await run({
  input: '图片路径、图片URL、文件夹路径，或它们组成的数组',
  saveDir: '可选的保存目录',
  backgroundColor: '可选，用户要求白底时传 "#ffffff"',
  vk: '可选，优先使用用户配置或环境变量 RMBG_VK'
});
```

最小调用：

```js
const result = await run({
  input: '/path/to/image.jpg'
});
```

批量调用：

```js
const result = await run({
  input: [
    '/path/to/1.jpg',
    '/path/to/2.png',
    'https://example.com/image.jpg'
  ],
  saveDir: '/path/to/output'
});
```

白底图调用：

```js
const result = await run({
  input: '/path/to/image.jpg',
  backgroundColor: '#ffffff'
});
```

黑底图调用：

```js
const result = await run({
  input: '/path/to/image.jpg',
  backgroundColor: '#000000'
});
```

## 输入参数

```js
{
  input: string | string[],
  saveDir?: string,
  backgroundColor?: string,
  vk?: string,
  config?: {
    vk?: string
  }
}
```

## 参数说明

- `input` 必填。支持本地图片路径、图片文件夹路径、图片 URL、逗号分隔的字符串，或由路径/URL 组成的数组。
- `saveDir` 可选。未提供时，结果保存到当前工作目录下的 `myxz-result/bgremove-v2`。
- `backgroundColor` 可选。用户没有明确要求纯色背景时不要传，默认输出透明背景 PNG。
- `vk` 或 `config.vk` 可选。如果环境变量 `RMBG_VK` 已存在，可以不传。
- 不要在回复、日志或错误信息中暴露 VK、API Key、请求头或其他敏感信息。

## 背景颜色规则

- 用户要求“透明底”“透明背景”“PNG 透明图”时，不传 `backgroundColor`。
- 用户要求“白底图”“亚马逊白底图”“白色背景”时，传 `backgroundColor: '#ffffff'`。
- 用户要求“黑底图”“黑色背景”时，传 `backgroundColor: '#000000'`。
- 用户指定其他颜色时，尽量转换为标准 CSS 色值，例如 `'#ff0000'`。
- 用户没有明确说要纯色背景时，默认透明背景。

## 适用请求

使用本 skill 处理：

- 单张图片抠图。
- 多张图片批量抠图。
- 文件夹图片批量去背景。
- 网络图片 URL 去背景。
- 商品图透明底处理。
- 商品图白底处理。
- 跨境电商主图白底处理。
- 去除背景后替换为指定纯色背景。

不要使用本 skill 处理：

- 普通修图。
- 图片压缩。
- 图片裁剪。
- 图片放大。
- 图片风格转换。
- 替换图片中的物体。
- 与背景移除无关的图片编辑任务。

## 工作流程

1. 从用户请求中识别图片输入，可以是路径、URL、文件夹或图片列表。
2. 如果用户没有提供任何可用图片输入，先询问用户提供图片路径、URL 或文件夹。
3. 根据用户需求决定是否设置 `backgroundColor`。
4. 调用本 skill 目录下 `index.js` 的默认导出函数 `run(params)`。
5. 不要自行实现 API 请求、轮询、下载或缓存逻辑，这些由执行器处理。
6. 根据返回对象向用户说明处理结果、保存目录、成功文件和失败原因。

## 返回值结构

执行器返回：

```
{
  success: boolean,
  partialSuccess: boolean,
  message: string,
  error?: string,
  data?: {
    batchId: string,
    saveDir: string,
    total: number,
    successCount: number,
    failedCount: number,
    backgroundColor: string,
    results: Array<{
      input: string,
      fileName: string,
      taskId: string,
      resultUrl: string,
      localPath: string,
      cached: boolean
    }>,
    failures: Array<{
      input: string,
      fileName: string,
      error: string
    }>
  }
}
```

## 返回值读取规则

- `success === true` 表示至少有一张图片处理成功。
- `partialSuccess === true` 表示部分成功、部分失败。
- `data.results` 是成功结果列表。
- `data.failures` 是失败结果列表。
- `data.saveDir` 是本批次结果保存目录。
- `data.results[].localPath` 是本地结果文件路径。
- `data.results[].resultUrl` 是远程结果地址。
- `data.results[].cached === true` 表示结果来自本地缓存。
- `success === false` 时，应读取 `error` 或 `message` 说明失败原因。

## 回复规范

处理成功时，回复应包含：

- 成功处理数量。
- 总图片数量。
- 保存目录 `data.saveDir`。
- 单张图片时可直接给出 `data.results[0].localPath`。

批量部分成功时，回复应包含：

- 成功数量。
- 失败数量。
- 保存目录。
- 失败文件名和失败原因。

全部失败时，回复应包含：

- 失败原因。
- 是否缺少 VK、输入路径无效、文件超过大小限制、网络图片无法访问或服务处理超时。

不要回复：

- VK 或 API Key。
- 原始请求头。
- 内部堆栈。
- 无必要的远程接口细节。
- 大段技术日志。

## 限制

- 单张本地图片不能超过 15 MB。
- 文件夹输入只会处理通过内置格式校验的图片文件。
- URL 输入依赖远程图片可访问性。
- 输出结果保存为 PNG 文件。
- 如果同一图片的哈希已有成功记录且本地文件存在，执行器可能直接复用缓存结果。
