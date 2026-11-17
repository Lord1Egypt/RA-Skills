# 宿主钩子模板（可直接复制改路径即用）

> **EN**: Hook examples for OpenClaw and Hermes. Both call the same recall implementation (`evolver-recall.mjs`) and share one gene library, so a lesson deposited on one host is available on the other. Installing hooks changes gateway behaviour: back up the unit file before editing, and re-run the doctor's allowlist check afterwards.


`SKILL.md` 的「宿主接入契约」讲的是**原则**；这里是**可直接复制的代码**。
两个模板都取自真实运行中的实现（已剥离环境细节），保留了对靶、零注入、异常兜底三条纪律。

## 文件

| 文件 | 宿主 | 事件 | 作用 |
|---|---|---|---|
| `openclaw-bootstrap-recall.js` | OpenClaw | `agent:bootstrap` | 任务开始时召回，命中的修法作为**虚拟引导文件**注入 |
| `hermes-pre-llm-recall.py` | Hermes | `pre_llm_call` | 任务开始时召回，命中的修法**追加到 stdout**；并提示结束时回填 |

## 三步接入

**第 1 步：改路径**
两个模板顶部都有三个常量，改成你的实际安装位置：
```js
// openclaw-bootstrap-recall.js
const RECALL_SCRIPT = '<技能目录>/code/evolver-recall.mjs';
const HITS_DIR      = '<技能目录>/experiments';
```
```python
# hermes-pre-llm-recall.py
RECALL_SCRIPT = "<技能目录>/code/evolver-recall.mjs"
HITS_DIR = "<技能目录>/experiments"
```
也可用环境变量 `EVOX_RECALL_SCRIPT` / `EVOX_HITS_DIR` 覆盖，脚本里已支持。

**第 2 步：注册钩子**
- OpenClaw：在钩子配置里把 `agent:bootstrap` 指向该 handler；**改 handler 通常需要重启网关**才生效。
- Hermes：在钩子配置里注册 `pre_llm_call` 指向该脚本；若宿主有 allowlist 机制，**改脚本内容后需刷新 allowlist**。

**补充触发点 T3：报错即召回（价值最直观）**

宿主侧凡是能拿到「工具报错文本」的钩子（如错误处理/重试前的钩子），加一条：
```bash
node <技能目录>/code/evolver-recall.mjs --error "<报错原文>"
```
报错是唯一"100% 会被注意到"的时刻——不需要谁提醒，错误本身就是提醒。
它复用沉淀侧的错误家族抽取，报错原文直接变成查询（实测：UnicodeDecodeError → 立刻命中 GBK 修法）。

**第 3 步：验证闭环真的跑起来了**
```bash
# 1) 手工验证召回能命中（用一句真实的任务描述）
node code/evolver-recall.mjs --query "读取中文日志报 UnicodeDecodeError" --agent openclaw

# 2) 看埋点：确认拿到了任务意图（noise=true 表示宿主传的是噪声、没拿到正文）
tail -5 experiments/recall_calls.jsonl

# 3) 任务结束时回填（把 <asset_id|gene_id> 换成实际基因 ID）
node code/evolver-recall.mjs --register-hit --gene <asset_id> --note "按 gbk 读取，成功"
> **EN**: address hits by `--gene <asset_id>` (id-based since 0.18).
node code/evolver-recall.mjs --negate --gene <asset_id|gene_id> --note "仍超时"

# 4) 看命中是否开始积累（>1 条说明闭环闭合）
wc -l experiments/hits.jsonl
```

## 别改掉的三条纪律

1. **没命中就零注入**——绝不在没命中时塞教程或任意基因（不对靶注入比不注入更差）。
2. **任何异常都零注入**——钩子绝不能让宿主启动失败。
3. **传用户的真实诉求**——不是信封包着的那条消息（群/私聊前缀、心跳、纯链接都会被 recall 清洗掉；清洗后为空就不注入）。

## 常见接入问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 一直没命中 | 宿主传的是噪声（信封前缀/心跳/纯 URL） | 在钩子里取**用户消息正文**再传；查埋点 `noise` 字段 |
| 命中率突然变好/变差 | 运行时版本漂移 | 确认部署的是最新版召回脚本 |
| 改了钩子没生效 | OpenClaw 需重启网关 / Hermes 需刷新 allowlist | 按宿主机制操作 |
| 子代理会话被污染 | 未跳过 `:subagent:` 会话 | 模板里已跳过，保留该判断 |
> **EN**: Replace `<asset_id|gene_id>` with the actual gene id; id-based addressing is concurrency-safe since 0.18.
