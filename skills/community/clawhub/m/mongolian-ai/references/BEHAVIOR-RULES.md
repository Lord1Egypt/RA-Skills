# 行为规则

交付与计费：[SKILL.md](../SKILL.md)。路由：[INTERFACE-ROUTING.md](./INTERFACE-ROUTING.md)。

## 调用前

- **可直调**：短句翻译/短对话；能读到计费则按 SKILL 输出。
- **须先报价或说明计费并确认**：长文、批量、网页正文、Word/PDF、多图 OCR、长 ASR、Agent 主动提议、用户要先看价。金额以**预估 API（若有）**与**成功响应计费字段**为准；本文档**不列单价**。无预估或失败时只说明计费方式、**勿编造金额**；须取得「视为同意」（是/确认/好/行/可以/yes/OK；沉默、「随便」不算）。
- **覆盖**：用户明示「知道收费直接做」或声明「本会话不再问」→ 可直接；用户要「先报价」→ 先报价或说清计费并确认后再调。

## 禁止绕过 API

含传统蒙古文 U+1800–U+18AF → 须走接口；禁止模型裸译/裸答。

## 可见回复

仅 SKILL 允许的目标字段 + 计费行。

## Key

配置：[API-KEY.md](./API-KEY.md)。未配置时**仅**输出下列固定提示（原文不改写）：

```text
MONGOL_AI_SKILL_API_KEY 未配置。请按以下步骤操作：
1. 访问 https://mongol.open-idea.net 注册/登录账号
2. 进入后台 API Key 页面，创建并复制完整 Key（含前缀如 `1|xxxx...`）
3. 在本机终端自行执行（勿将 Key 粘贴到对话框）：
   openclaw config set env.MONGOL_AI_SKILL_API_KEY "<完整API Key>"
4. 执行后在终端运行 openclaw gateway restart，使配置立即生效
5. 若客户端不支持上述命令，可手动编辑 ~/.openclaw/.env（Windows 为 %USERPROFILE%\.openclaw\.env），写入 MONGOL_AI_SKILL_API_KEY=你的完整Key，再重启 Gateway
```

禁止索要 Key；用户若已粘贴 → 警告撤销重签 → `openclaw config set` + `openclaw gateway restart` → 不回显 Key；保留 `1|` 等前缀。

## 扣费与重试

- `200`/业务成功/异步 `done` 且能读业务或计费 → **通常已扣费**；勿因不满意用**同一** content/文件再调。改输入/路由前须说明并获同意。
- **4xx**：修参/Key，勿盲重试。**5xx**/未完结：同体限次退避（如 ≤3）。**勿**过小 `--max-time`；`chat` 不设或 `30～60s`。

## Chat · 预检

全程传统蒙文 → 输出须全蒙、禁多余汉字；等于 `choices[0].message.content`，勿二改（[CHAT-COMPLETIONS.md](./CHAT-COMPLETIONS.md)）。  
含传统蒙而未调 API → 先调再答；高成本先走「调用前」。
