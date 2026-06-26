# Retrieval Query Template

请把下面信息压缩成适合相似案例检索的查询文本，优先保留：
- 当前对话里的用户侧内容
- 原始时间线索
- 结构化时间特征
- 明显身份线索

模式：{{MODE}}
用户对话：
{{USER_TEXT}}

原始时间线索：{{TIME_HINT}}
时间特征：
{{TIME_FEATURES_JSON}}

身份线索：{{IDENTITY_HINTS}}

建议检索文本：
{{BASE_QUERY}}
