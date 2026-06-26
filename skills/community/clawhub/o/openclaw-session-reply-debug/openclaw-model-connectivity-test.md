# OpenClaw 模型可运行性测试手册

本手册由 `SKILL.md` 调用，用于在“模型切换”前后验证模型可用性。

## 目标

验证某个模型（例如 `openai/gpt-5.3`）在当前 OpenClaw 环境是否可用，并快速定位问题是在：

- OpenClaw 配置层
- 上游模型网关层
- OpenClaw Agent 运行链路层

## 结论判定标准

- 通过：`Provider 直连探针` 返回 `OK 200 ...`，且 `OpenClaw Agent 探针` 返回业务可读回复（非报错文本）
- 不通过：任一步返回 `ERROR/FAIL`，或 Agent 输出包含模型错误（例如 `unknown provider for model ...`）

## 前提

- 已安装并可执行 `openclaw`
- 已配置 `$HOME/.openclaw/openclaw.json`
- 本机有 `node`（本手册不依赖 `jq`）

## 与 Skill 的配合方式（强制）

1. 切换前：先测目标模型，或按优先级测一组候选模型是否可用。
2. 执行切换脚本（固定回滚或通用 fallback 脚本）。
3. 切换后：再次用同样探针验证，确认最终选中的模型仍可用。
4. 任一步失败都不算完成切换。

## Step 1. 检查模型是否在 OpenClaw 配置中声明

```bash
cd "$HOME/.openclaw"
MODEL_ID=gpt-5.3 node -e '
const fs=require("fs");
const c=JSON.parse(fs.readFileSync("openclaw.json","utf8"));
const p=c.models?.providers?.openai;
const m=p?.models?.find(x=>x.id===process.env.MODEL_ID);
if(!p){ console.log("ERROR no openai provider in openclaw.json"); process.exit(2); }
if(!m){ console.log(`ERROR model ${process.env.MODEL_ID} not configured`); process.exit(3); }
console.log(`OK configured: provider=openai baseUrl=${p.baseUrl} model=${m.id}`);
'
```

如果这里失败，先修配置再继续（例如模型 ID 未注册）。

## Step 2. Provider 直连探针（最快定位模型本身是否可用）

```bash
cd "$HOME/.openclaw"
MODEL_ID=gpt-5.3 node -e '
const fs=require("fs");
const c=JSON.parse(fs.readFileSync("openclaw.json","utf8"));
const p=c.models.providers.openai;
const model=process.env.MODEL_ID;
fetch(`${p.baseUrl}/chat/completions`,{
  method:"POST",
  headers:{Authorization:`Bearer ${p.apiKey}`,"Content-Type":"application/json"},
  body:JSON.stringify({
    model,
    messages:[{role:"user",content:"reply with OK"}],
    max_tokens:8
  })
})
.then(async r=>({status:r.status,body:await r.text()}))
.then(({status,body})=>{
  let j; try{ j=JSON.parse(body); } catch { console.log(`ERROR ${status} NON_JSON ${body.slice(0,200)}`); process.exit(2); }
  if(j.error){ console.log(`ERROR ${status} ${j.error.message || JSON.stringify(j.error)}`); process.exit(3); }
  console.log(`OK ${status} ${j.choices?.[0]?.message?.content || "NO_CONTENT"}`);
})
.catch(e=>{ console.log(`FAIL ${e.message}`); process.exit(1); });
'
```

常见输出：

- `OK 200 OK`：上游模型可用
- `ERROR 502 unknown provider for model gpt-5.3`：上游不识别该模型 ID
- `ERROR 401 ...`：鉴权失败（Key 或权限问题）

## Step 3. OpenClaw Agent 端到端探针（验证“在 OpenClaw 里跑”）

```bash
cd "$HOME/.openclaw"
openclaw agent --agent main --message "Connectivity test: reply only OK" --json --timeout 90
```

注意：

- 必须给 `--agent main`（否则会报：`Pass --to <E.164>, --session-id, or --agent`）
- 即使 `status` 是 `ok`，也要检查 `result.payloads[0].text` 是否是错误文本
- 告警噪音（例如插件重复）不一定是本问题根因

## Step 4. 双探针结果矩阵（推荐）

- `Step 2 失败 + Step 3 失败`：优先处理上游模型可用性/路由/模型 ID
- `Step 2 成功 + Step 3 失败`：重点排查 OpenClaw 运行链路（会话模型选择、agent 配置、网关日志）
- `Step 2 成功 + Step 3 成功`：模型可在 OpenClaw 正常运行

## Step 5. 多模型优先级验证（Heartbeat / Fallback 场景）

当你要实现：

- `primary = gpt-5.4`
- `fallbacks = [gpt-5.3, gpt-5.2]`
- heartbeat 周期探测后自动降级 / 自动回切

推荐先手工验证一遍优先级序列，再把同一组参数交给 heartbeat：

```bash
node scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2
```

预期：

- 若 `gpt-5.4` 可用：选中 `gpt-5.4`
- 若 `gpt-5.4` 不可用且 `gpt-5.3` 可用：选中 `gpt-5.3`
- 若 `gpt-5.4` / `gpt-5.3` 都不可用但 `gpt-5.2` 可用：选中 `gpt-5.2`
- 若都不可用：脚本失败，不应宣称切换完成

这也是 heartbeat 自动恢复的基础：它不是记住“上次用了什么”，而是**每次按优先级重新探测一次**。

## Step 6. Heartbeat 接入前的手工预演（推荐）

在把任务挂到 OpenClaw heartbeat / cron 之前，先手工跑一遍与 heartbeat 完全一致的命令：

```bash
node scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2 \
  --apply
```

确认输出里至少能看见：

- `Candidates: ...`
- `Probe results:`
- `Selected model: ...`
- `Changed files: ...`
- `Total updates: ...`

只有手工预演成功后，才建议把同一组参数挂到 heartbeat 任务中。

## 高频错误与处理

### 1) `unknown provider for model <model-id>`

- 含义：上游网关不支持该模型 ID，或模型映射未开通
- 快速确认：把 `MODEL_ID` 临时切换为已知可用模型（例如 `gpt-5.2`）对照测试

### 2) `Pass --to <E.164>, --session-id, or --agent`

- 含义：`openclaw agent` 未指定目标会话
- 处理：补 `--agent main` 或 `--session-id <id>`

### 3) `401/403`

- 含义：API Key 无效或权限不足
- 处理：检查 `openclaw.json` 中 `baseUrl/apiKey` 与供应商侧权限

## 实测样例（2026-03-06）

在当前环境下（`$HOME/.openclaw`）：

- `gpt-5.3`：`ERROR 502 unknown provider for model gpt-5.3`
- `gpt-5.2`：`OK 200 OK`

说明链路可用，但 `gpt-5.3` 模型 ID 在当前上游不可用。

## 一键复测模板（建议）

先测目标模型（应当成功）：

```bash
cd "$HOME/.openclaw"
MODEL_ID=gpt-5.2 node -e '
const fs=require("fs");
const c=JSON.parse(fs.readFileSync("openclaw.json","utf8"));
const p=c.models.providers.openai;
fetch(`${p.baseUrl}/chat/completions`,{
  method:"POST",
  headers:{Authorization:`Bearer ${p.apiKey}`,"Content-Type":"application/json"},
  body:JSON.stringify({model:process.env.MODEL_ID,messages:[{role:"user",content:"reply with OK"}],max_tokens:8})
})
.then(async r=>({status:r.status,body:await r.text()}))
.then(({status,body})=>{ let j; try{ j=JSON.parse(body);} catch { console.log(`ERROR ${status} NON_JSON`); process.exit(2); }
  if(j.error){ console.log(`ERROR ${status} ${j.error.message || JSON.stringify(j.error)}`); process.exit(3); }
  console.log(`OK ${status} ${j.choices?.[0]?.message?.content || "NO_CONTENT"}`); })
.catch(e=>{ console.log(`FAIL ${e.message}`); process.exit(1); });
'
```

再测 Agent 链路（应当成功）：

```bash
cd "$HOME/.openclaw"
openclaw agent --agent main --message "Connectivity test after model switch: reply only OK" --json --timeout 90
```

如果你要验证 heartbeat 的“自动恢复到最高优先级模型”行为，重复执行同一条 `switch-model-with-fallback.js` 命令即可；不需要换命令，只需要等更高优先级模型恢复可用。
