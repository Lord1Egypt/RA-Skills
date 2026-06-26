# 模型开放平台对比：Moonshot / 阿里云百炼 / SiliconFlow / DeepSeek / OpenRouter / BigModel / Ark / 混元 / 千帆 / MiniMax

> 这个文件用于快速对比，不追求穷尽字段；优先给出文档入口与最常用调用要点。

| 平台 | 常见品牌名 | OpenAI 兼容 | Base URL | 常见环境变量 | 示例模型名/备注 | 官方文档 |
|---|---|---|---|---|---|---|
| Moonshot | Kimi / 月之暗面 | 是 | `https://api.moonshot.cn/v1` | `MOONSHOT_API_KEY` | `kimi-k2.5` | `platform.kimi.com/docs` |
| 阿里云百炼 | DashScope / Model Studio | 是 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_API_KEY` | `qwen-plus` | `help.aliyun.com/model-studio` |
| SiliconFlow | 硅基流动 | 是 | `https://api.siliconflow.cn/v1` | 常自定义 | `Pro/zai-org/GLM-4.7` | `docs.siliconflow.cn` |
| DeepSeek | DeepSeek Platform | 是 | `https://api.deepseek.com` / `.../v1` | `DEEPSEEK_API_KEY` | `deepseek-chat` | `api-docs.deepseek.com` |
| OpenRouter | OpenRouter | 通常是 | `https://openrouter.ai/api/v1` | 常自定义 | 聚合路由层 | `openrouter.ai/docs` |
| BigModel | 智谱开放平台 | 支持 | 以官方文档为准 | 以控制台为准 | GLM / OpenAI 兼容路线 | `docs.bigmodel.cn` |
| Ark | 火山方舟 | 需按文档确认 | 以官方文档为准 | 以控制台为准 | 文本生成/工具调用/Responses | `volcengine.com/docs/82379` |
| Hunyuan | 腾讯混元 | 需按文档确认 | 以官方文档为准 | 以控制台为准 | 腾讯混元 API | `cloud.tencent.com/document/product/1729` |
| Qianfan | 百度千帆 | 需按文档确认 | 以官方文档为准 | 以控制台为准 | 模型服务 + Agent 平台 | `cloud.baidu.com/doc/qianfan` |
| MiniMax | MiniMax | 非完全同路径 | `https://api.minimaxi.com` | 以控制台为准 | `/v1/text/chatcompletion_v2` | `platform.minimaxi.com/docs` |

## 迁移心法

如果用户已经有 OpenAI 代码，通常先改三件事：

1. `api_key`
2. `base_url`
3. `model`

但最容易出错的也是这三件：

- Key 对了，URL 没换
- URL 对了，模型名不属于该平台
- 模型名对了，但没注意兼容模式 / 区域 / 聚合路由层差异
- 有些平台虽然兼容 OpenAI SDK，但 endpoint 路径不一定完全一致

## 默认回答模板

当用户问“XX 平台怎么调用”时，优先按这个顺序回答：

1. 官方文档入口
2. 认证方式
3. Base URL / endpoint
4. 最小 Python / curl 示例
5. 该平台和 OpenAI 的差异

当用户问“多平台怎么对比”时，优先输出：

- 对比表
- 迁移建议
- 容易踩坑点
- 官方链接入口
