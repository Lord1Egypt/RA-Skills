---
name: minor-detection
description: 当用户或上层系统需要判断聊天记录中的说话者是否可能是未成年人、青少年、中学生、高中生，或需要对单会话、多会话历史做年龄倾向、校园倾向、学生画像、未成年人风险与证据分析时使用此技能。即使用户没有直接说“未成年人识别”，但需求本质上是判断“像不像未成年用户”、输出未成年人概率、画像、趋势、风险等级或结构化证据，也应激活此技能。
metadata:
  openclaw:
    requires:
      env:
        - MINOR_DETECTION_CLASSIFIER_BASE_URL
        - MINOR_DETECTION_CLASSIFIER_API_KEY
    primaryEnv: MINOR_DETECTION_CLASSIFIER_API_KEY
---

# Minor Detection

把这个 skill 视为“调用固定控制脚本并返回单个 JSON 结果”的能力，不要把它当成自由发挥的推理任务。

## 硬性约束

你必须遵守以下规则：
- 始终调用 `scripts/run_minor_detection_pipeline.py`。
- 不要自行重写未成年人识别逻辑。
- 不要直接调用 `extract_time_features.py` 或 `retrieve_cases.py`，除非控制脚本内部决定调用它们。
- 脚本成功时，最终回答必须是 stdout 返回的单个 JSON object。
- 脚本失败时，只返回错误，不要自行补充判断。

## 输入准备

先把当前输入整理成一个 JSON payload，再交给控制脚本。

推荐字段：
- `mode`
- `conversation`
- `sessions`
- `context`
- `meta`
- `request_id`
- `sample_id`
- `user_id`

`context` 可包含：
- `raw_time_hint`
- `opportunity_time`
- `time_features`
- `prior_profile`
- `retrieved_cases`

如果上游已经提供完整 JSON，就尽量保持结构不变，只做最小整理。

## 执行方式

执行步骤：
1. 把整理后的 payload 写入临时 JSON 文件。
2. 运行 `python scripts/run_minor_detection_pipeline.py --payload-file <payload-file>`。
3. 读取 stdout 中最后输出的 JSON object。
4. 将该 JSON 原样作为最终结果返回。

## 外部服务与隐私说明

此技能不是纯离线技能。

运行时行为：
- 控制脚本会在分类阶段把对话文本、时间线索、历史画像、身份提示以及相关元数据发送到你显式配置的远程模型接口。
- 如果内置检索资源存在，并且显式配置了 embedding 端点与密钥，检索模块才会调用远程 embedding 接口。
- 当前这个轻量版包不包含内置检索资源，因此检索通常会降级为 `disabled:assets_missing`，并返回空的 `retrieved_cases`。
- 如果调用方已经提供 `context.retrieved_cases`，流水线也可以直接使用外部提供的检索结果。

显式配置要求：
- 若未设置 `MINOR_DETECTION_CLASSIFIER_BASE_URL` 或 `MINOR_DETECTION_CLASSIFIER_API_KEY`，分类调用会直接报错而不是联网。
- 若未来需要启用远程 embedding 检索，需要显式设置 `MINOR_DETECTION_EMBEDDING_BASE_URL` 和 `MINOR_DETECTION_EMBEDDING_API_KEY`。

此技能会读取的环境变量：
- `MINOR_DETECTION_CLASSIFIER_BASE_URL`
- `MINOR_DETECTION_CLASSIFIER_API_KEY`
- `MINOR_DETECTION_CLASSIFIER_MODEL`
- `MINOR_DETECTION_CLASSIFIER_TIMEOUT_SEC`
- `MINOR_DETECTION_CLASSIFIER_MAX_RETRIES`
- `MINOR_DETECTION_CLASSIFIER_RETRY_BACKOFF_SEC`
- `MINOR_DETECTION_EMBEDDING_BASE_URL`
- `MINOR_DETECTION_EMBEDDING_API_KEY`
- `MINOR_DETECTION_EMBEDDING_MODEL`
- `MINOR_DETECTION_TIMEZONE`
- `MINOR_DETECTION_RETRIEVAL_TOP_K`
- `SKILL_EMBEDDING_BASE_URL`
- `SKILL_EMBEDDING_API_KEY`
- `SKILL_EMBEDDING_MODEL`

凭证说明：
- 建议使用专用、最小权限的 API Key。
- 如果数据必须完全本地处理，请不要使用此技能。

## 输出规则

最终回答必须：
- 只输出一个 JSON object。
- 不输出 Markdown。
- 不添加解释性前言。
- 不补充 skill 输出之外的推理内容。



