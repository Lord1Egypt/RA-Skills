---
name: myxz-image-translation
description: 妙言小智 (PicTech.cc) 专业级跨境电商图片翻译 Skill，支持批量翻译、主图保护、多语言映射、在线编辑与自动化工作流集成。
---

# 妙言小智图片翻译

使用本 skill 通过 妙言小智 图片翻译服务翻译图片中的文字。

妙言小智官方网站：https://www.pictech.cc  
妙言小智API 服务域名：https://stableai.com.cn
VK(APP KEY) 获取地址：https://www.pictech.cc/newpictech/skills/openclaw-image-translation-skill

## VK 凭证规则

VK 是必需的 API 凭证。

- 必须优先从 skill/plugin 的持久配置中读取 VK，即 `config.vk`。
- 不要要求用户在每次图片翻译任务中都输入 VK。
- 不要把 VK 写入普通用户提示、聊天消息、日志、报告、文件名或返回摘要。
- 如果缺少 VK，告诉用户需要先在 skill/plugin 配置中填写一次 VK，然后重新执行任务。
- 只有在受控内部测试时才允许使用直接传入的 `vk` 字段；正式使用时优先使用 `config.vk`。

缺少 VK 时可以这样回复用户：

```text
需要先在图片翻译 skill 的配置中填写一次 VK。配置完成后，我会自动读取，不需要你每次翻译都输入。
```

## 处理用户请求的流程

1. 识别图片输入来源：
   - 单个本地图片路径
   - 包含图片的本地文件夹
   - 一个或多个图片 URL
   - 逗号分隔的多个路径或 URL
2. 判断翻译语言方向：
   - 默认源语言：`中文`
   - 默认目标语言：`英文`
   - 如果用户明确说明语言方向，使用用户指定的语言。
   - 如果用户没有说明语言方向，使用默认值。
3. 判断是否启用主图/主体保护：
   - 默认值：`false`
   - 当用户要求保护主商品、主体、主图、产品本体、Logo 区域或关键视觉元素不被翻译/修改时，设置 `mainImageProtection: true`。
4. 判断保存目录：
   - 如果用户指定了保存目录，使用用户指定的目录。
   - 如果用户没有指定保存目录，让 `index.js` 使用默认结果目录。
5. 使用结构化参数调用 skill 执行器。
6. 根据返回的结构化结果向用户总结任务结果。

## 支持语言

支持的源语言：

- `中文`
- `繁体中文`
- `英文`
- `泰语`
- `俄语`
- `印尼语`
- `马来语`
- `葡萄牙语`
- `西班牙语`
- `法语`
- `德语`

目标语言除了支持以上语言外，还支持 `index.js` 中映射到 API 的其他语言，例如：

- `韩语`
- `意大利语`
- `波兰语`
- `荷兰语`
- `土耳其语`
- `越南语`
- `菲律宾语`

如果用户指定了不支持的源语言，需要说明当前支持的源语言列表，并请用户选择其中一种。

## 调用方式

从 `index.js` 导入默认导出的执行函数，并传入结构化参数。

单张图片示例：

```js
await run({
    input: "C:/path/to/image.png",
    sourceLanguage: "中文",
    targetLanguage: "英文",
    mainImageProtection: false,
    saveDir: "C:/path/to/output",
    config: {
        vk: "<从 skill/plugin 持久配置中读取>"
    }
});
```

多张图片示例：

```js
await run({
    input: [
        "C:/path/to/one.jpg",
        "C:/path/to/two.png",
        "https://example.com/three.webp"
    ],
    sourceLanguage: "中文",
    targetLanguage: "英文",
    mainImageProtection: true,
    config: {
        vk: "<从 skill/plugin 持久配置中读取>"
    }
});
```

文件夹示例：

```js
await run({
    input: "C:/path/to/image-folder",
    sourceLanguage: "中文",
    targetLanguage: "英语",
    config: {
        vk: "<从 skill/plugin 持久配置中读取>"
    }
});
```

## 参数说明

`input`：必填。可以是本地图片路径、文件夹路径、图片 URL、路径/URL 数组，或逗号分隔的字符串。

`config.vk`：必填。必须来自 skill/plugin 的持久配置。

`sourceLanguage`：可选。默认值为 `中文`。

`targetLanguage`：可选。默认值为 `英文`。

`mainImageProtection`：可选。默认值为 `false`。

`saveDir`：可选。未提供时，执行器会保存到默认输出目录。

## 返回结果结构

执行器会返回适合大模型解析的结构化对象：

```js
{
    success: true,
    status: "completed",
    message: "图片翻译完成，成功 1 个，无文字 0 个，失败 0 个，总计 1 个。",
    batchId: "batch_...",
    sourceLanguage: "中文",
    targetLanguage: "英文",
    sourceLanguageCode: "Chinese",
    targetLanguageCode: "English",
    mainImageProtection: false,
    saveDir: "C:/path/to/result/batch",
    counts: {
        total: 1,
        success: 1,
        noText: 0,
        failed: 0
    },
    results: [
        {
            taskId: "...",
            input: "C:/path/to/image.png",
            fileName: "image.png",
            resultUrl: "https://...",
            editorUrl: "https://...",
            localPath: "C:/path/to/result.png",
            fromCache: false
        }
    ],
    errors: [],
    skipped: []
}
```

## 无文字图片处理

后端 `querytask` 返回 `data.status === 300` 时，表示该图片上没有可翻译文字：

```json
{
  "code": 200,
  "data": {
    "status": 300,
    "errorMessage": "图片上无文字 翻译失败，无需重试"
  }
}
```

Agent 必须把 `300` 当作终态处理：

- 不要继续轮询该任务
- 不要把该图片重新提交给 `submittask`
- 不要把它当作需要重试的普通失败
- 应记录为 `no_text` / `skipped`，并在本地缓存中标记，后续同图同语言方向直接跳过提交
- 最终统计中写入 `counts.noText`，并在 `skipped` 中说明原因
- 如果一批图片里只有无文字图片且没有真实失败，整体 `status` 可以是 `completed`

可能的 `status` 值：

- `completed`：全部图片翻译成功
- `partial_success`：部分图片成功或无文字跳过，部分图片失败
- `failed`：所有已尝试图片均失败
- `no_tasks`：没有找到可处理的有效图片任务
- `invalid_params`：缺少必填参数
- `invalid_source_language`：源语言不受支持
- `invalid_target_language`：目标语言不受支持
- `missing_api_key`：没有配置 VK

## 给用户的回复规范

任务成功时，向用户说明：

- 成功、无文字跳过和失败的图片数量
- 本地文件保存位置
- 可用的翻译结果预览链接
- 可用的在线编辑链接

不要暴露内部缓存 key、请求头、原始 VK、堆栈信息或完整 API 请求数据。

当 `status` 是 `partial_success` 时，先展示成功结果，再简要列出失败文件和失败原因。

当返回结果包含 `skipped` 或 `counts.noText > 0` 时，说明这些图片是“图片上无文字，无需重试”，不要建议用户再次提交这些图片。

当 `status` 是 `missing_api_key` 时，不要反复要求用户在对话里输入 VK。应提示用户到 skill/plugin 配置中填写一次 VK。

## 典型用户请求

- `把这张图片从中文翻译成英文`
- `翻译这个文件夹里的所有商品图，中文到西班牙语`
- `把这些图片 URL 翻译成英文，主图产品不要动`
- `中文图片翻译成英语，结果保存到指定目录`

## 可靠性要求

- 不要修改原始输入图片。
- 保留返回结果中的本地路径，方便用户找到文件。
- 将 URL 作为远程图片输入处理，将本地路径作为文件系统输入处理。
- 后端 `status=300` 是“图片上无文字”的无需重试终态，必须跳过并缓存，不要重复提交。
- 如果某张图片超过大小限制或格式不支持，将该图片记录为失败，并继续处理剩余图片。
- 最终回复优先使用简洁摘要，不要默认向用户倾倒完整结构化对象，除非用户要求查看原始返回结果。
