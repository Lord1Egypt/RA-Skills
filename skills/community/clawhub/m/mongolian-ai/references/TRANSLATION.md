# 文本翻译

POST https://ai-skills.open-idea.net/api/v1/mongolian-ai/translation
Content-Type: application/json

请求字段：from、to、content。from/to 仅 zh、mw、mn，且必须不同；content 必填，最多 4000 字符。六个方向均支持：zh→mw、zh→mn、mw→zh、mn→zh、mw→mn、mn→mw。

成功只提取 data.tgtText。按段落或句子边界将长文拆成不超过 4000 字符的段，保留顺序，每段独立 Idempotency-Key；不得截断原文或用对话结果冒充翻译。
