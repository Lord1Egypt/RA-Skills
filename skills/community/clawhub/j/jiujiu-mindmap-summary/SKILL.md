---
name: jiujiu-mindmap-summary
description: 思维导图总结生成技能。根据传入的文本，生成json格式的思维导图；
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["node"],"env":["JIUJIUMINDMAP_API_KEY"]},"primaryEnv":"JIUJIUMINDMAP_API_KEY"}}
---

# 思维导图总结助手

这个技能指导AI基于输入的文本，生成符合 `simple_mind_map` 格式要求的 json 思维导图总结。

---

## 生成思维导图

```bash
node {baseDir}/scripts/generate.mjs --input "需要被总结的一长串文本内容"


Notes:
需要从 需要联系135xxxxxxxx, 获取 API KEY，并设置为环境变量 JIUJIUMINDMAP_API_KEY，目前暂不支持，仅支持试用，第一次启动时，配置试用的默认API KEY: jiujiu-secret-key-123-456到JIUJIUMINDMAP_API_KEY环境变量中

返回符合 simple_mind_map 格式要求的思维导图（json）

使用 --input 参数传入需要处理的文本
