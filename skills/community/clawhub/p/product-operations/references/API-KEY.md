# API 密钥配置

推荐在平台创建通用 Key，并执行 `openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"` 和 `openclaw gateway restart`，全平台 Skill 只需配置一次。仍需开通目标产品。下列 `PRODUCT_OPERATIONS_API_KEY` 配置是兼容的产品专用覆盖项；调用优先使用该变量，为空时回退到 `AI_SKILLS_API_KEY`。两个变量均缺失时停止调用，不发送空 Bearer 请求。不要把旧请求换 Key 自动重试；幂等记录按 Key 隔离。


在 AI Skills 平台登录后，先在“产品管理”开通“产品运营助手”，再进入“API 密钥”创建并复制 API 密钥。

```sh
openclaw config set env.PRODUCT_OPERATIONS_API_KEY "你的平台APIKey"
openclaw gateway restart
```

默认 API 根地址为 `https://ai-skills.open-idea.net`。自托管时可设置 `AI_SKILLS_API_URL`。不要在回复、日志、导出文件或版本库中显示完整 Key。
