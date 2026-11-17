# API 密钥配置

推荐在平台创建通用 Key，并执行 `openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"` 和 `openclaw gateway restart`，全平台 Skill 只需配置一次。仍需开通目标产品。下列 `MONGOL_AI_SKILL_API_KEY` 配置是兼容的产品专用覆盖项；调用优先使用该变量，为空时回退到 `AI_SKILLS_API_KEY`。两个变量均缺失时停止调用，不发送空 Bearer 请求。不要把旧请求换 Key 自动重试；幂等记录按 Key 隔离。


在 [产品管理](https://ai-skills.open-idea.net/dashboard/products) 开通蒙语 AI，在 [API 密钥管理](https://ai-skills.open-idea.net/dashboard/keys) 创建或复制现有通用 Key。密钥只存入 `AI_SKILLS_API_KEY` 或兼容的 `MONGOL_AI_SKILL_API_KEY`，不能放入 URL、日志、截图或最终回复。

当前 Skill 使用 `MONGOL_AI_SKILL_API_KEY`，与 ClawHub 旧版 v1.0.14 保持一致；已配置该变量且密钥可用于 AI Skills 平台的用户只需更新 Skill，无需重新配置或生成密钥。若此前按 2.0.0–2.0.2 配置了其它变量名，请将同一个有效平台密钥配置到 `MONGOL_AI_SKILL_API_KEY` 并重启 Gateway；新接口验证成功前保留旧配置。旧站点密钥若未被平台迁移或兼容，不能仅凭复制变量用于新接口，也不得把旧密钥自动上传到其它服务换取新密钥。

请求使用 Authorization: Bearer 平台密钥。缺少配置时停止请求，提示用户完成配置；不得猜测凭证或寻找其它服务密钥。配置后重启 Gateway。

升级后的请求统一使用 `https://ai-skills.open-idea.net/api/v1/mongolian-ai`。先用一个短句验证翻译结果及 `X-AI-Skills-Billing-*` 响应头，再处理文件或异步任务。401/403 表示密钥或产品权限不正确；不要通过反复创建新密钥或新幂等键重放付费操作。
