# Prompt 注册表

> 路径前缀：`references/prompts/`
> 商店版仅保留通用 Prompt 入口。新平台首次接入时，若不存在平台专属 Prompt，必须先回退到通用 Prompt。

## 查找规则

1. 按 `type` + `web` 精确匹配当前 `goal_web`
2. 找到平台专属记录时，读取其 `path`
3. 未找到时，必须回退到同类型通用 Prompt

## 注册表

| 名称 | 类型 | web | 核心描述 | 路径 | fallback |
|------|------|-----|---------|------|---------|
| goal_prompt | 任务拆解 | 通用 | 商店版通用任务拆解 Prompt，适用于所有新平台首次接入 | `references/prompts/goal_prompt.md` | — |
| retro_prompt | 复盘 | 通用 | 商店版通用复盘 Prompt，适用于所有新平台首次接入 | `references/prompts/retro_prompt.md` | — |

## 新增平台专属 Prompt 规则

1. 必须先使用 `references/prompts/meta_prompt.md`
2. 必须再用 `references/prompts/prompt_authoring_guide.md` 校验字段
3. 生成后的文件写入 `references/prompts/`
4. 最后在本注册表追加平台专属记录

## 商店版约束

- 当前文件不得保留任何真实业务平台条目
- 当前文件必须始终保留通用 `goal_prompt` 和通用 `retro_prompt`
- 若后续新增平台专属 Prompt，应以通用 Prompt 为 fallback
