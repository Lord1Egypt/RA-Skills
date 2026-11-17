# Changelog

公开版仅保留用户可感知的功能变更。内部迭代历史不入仓。

## v5.0.0 (2026-07-24) ⚠️ BREAKING

### 加 (New)
- **架构重写**：skill 不再写死任何业务词 / 行业模板 / 平台字典
  - 删除 `INDUSTRY_TEMPLATES` (mcn/saas/law/mfg 4 个行业的所有 abilities/upstream/downstream/peer 列表)
  - 删除 `INDUSTRY_SIGNALS` (token 频率猜行业)
  - 删除 `PLATFORM_TERMS` / `GENERIC_TERMS` / `TAIL_GENERIC` / `MID_GENERIC` (所有 stop word 词表)
  - skill 现在认任何中文公司 rawText：律所 / 餐饮 / 制造 / 数字营销 / … 都用同一套代码
- **LLM 任务包**：每张卡 + JSON 输出都含
  - `evidenceCandidates` (string[30]): n-gram 频次排名 + 长度加分
  - `evidenceAnswerPrompt` (string): 单卡 LLM 选择规则 + JSON 输出格式
  - `llmInstruction` (string): 顶层 LLM 一次性任务流 (read → pick → rewrite → submit)
  - 占位符 `(证据词: <待 LLM 填写>)` 在 rawText 里等 LLM 填
- **heading 驱动拆卡**:
  - rawText `## 业务描述` 节下 `### 维度名` 直接生成 ability 卡片
  - `### 上游依赖 / 下游客户 / 同业联盟` 子标题自动判定 type (无需模板)
  - 其它行业 (律所/餐饮等) 写啥拆啥: `### 公司诉讼` / `### 火锅堂食` 都能识别

### 改 (Changed)
- 数据流从 "skill 输出 → 用户确认 → LLM 再审 → submit" 多步，简化为 "skill 输出 LLM 任务包 → LLM 一次性完成 → submit"
- 无行业推断 (token 频率猜), 行业归属由 LLM 在对话里判断并传入

### 弃用 (Deprecated)
- 任何用户写死的维度词表 (e.g. 老 v4.x 模板里硬编码的"达人营销"/"短视频内容制作")

### 测 (Test)
- 11 个单元测试: 通用性守卫 (源码不许有业务词) / heading 拆 / n-gram 候选 / 占位符 / LLM 提示
- 用 `npm test` 跑

## v4.0.10 (2026-07-24)

### 加 (New)
- **knowledge-card evidence 提取加固** (extractEvidenceFromDesc):
  - 长度上限 6→8, 让 "短视频内容制作"/"店铺代运营" 等 7-8 字短语能拆出
  - 新增 PLATFORM_TERMS 优先扫 (抖音/快手/小红书/B站/视频号 等 14 平台)
  - 解决 "精选小红书博主合作" 短语被 6 字限制吞掉的 case, 拆出关键词 "小红书"
  - 尾部泛词剥离 (等等/行业/领域/场景/赛道/玩法/业务/服务/平台/资源)
  - 列表前缀剥离 (包括/比如/例如/以及)
  - 人称前缀剥除 (我们/你/他/她/它)

### 测 (Test)
- 单元测试 9 → 12 (新增 3 个边缘 case 覆盖人称/列表前缀/跨公司对比)
- `npm test` 全部 12 测试通过 (~600ms)

## v4.0.9 (2026-07-24)

### 修 (Fixed)
- **knowledge-card 证据词提取**: 之前用模板写死的 `purpose` 字符串当证据词源, 不同公司卡片雷达词趋同 (e.g. 都显示 "KOL 投放"/"媒介代理")。现在从 rawText 自然语言描述里挖真实关键词 (拆标点 + 滤停用前缀 + 限 2-6 字名词性片段), 两家公司 evidence 完全独立。
- **证据词格式统一**: 修复 `buildCard()` 漏传 `evidenceList` 参数 bug。所有卡片现在统一输出 `(证据词: kw1, kw2, ...)` 格式, 去掉旧 `(证据: rawText 包含 "${dim}")` 兜底文案 (前端 regex 解析不到)。
- **雷达不再有杂质**: 前端雷达原显示 "蓝色光标"/"宝马等"等公司名/团队背景, 现在都是真实能力词 (达人筛选/店铺搭建/活动策划等)。
- **extractParsedFields 城市检测**: 不再被同业联盟里 `无忧传媒(北京...)` 这类字符串污染。限定到「地址字段 || 工商信息节」内查找城市。
- **knowledge-discover 骨架校验**: 加 `SKELETON_PATTERNS` 检测, rawText 含 `(名称 / 法人 / 注册资本...)` 等填空内容时直接拒绝 (skeleton_unfilled), 强制 LLM 用 web_search 搜真实数据。
- **knowledge-discover 搜索指令内嵌**: `--name` 模式输出 `_explicitInstructions` 字段, 列出每节搜索命令 + 禁止传空骨架警告。

### 加 (New)
- 9 个单元测试覆盖 `extractEvidenceFromDesc` / `extractDimDesc` / `extractParsedFields` 三大核心逻辑。用 `npm test` 跑 (`tests/unit-knowledge-card.js`)。

### 测 (Test)
- `node --test tests/unit-knowledge-card.js` 全部 9 测试通过 (~450ms)
- `npm test` 端到端验证脚本 (`tests/e2e-verify.js`) 不动

## v4.0.0 (2026-07-22)

### 加 (New)

- OAuth Device Flow 登录 + token 自动写 macOS Keychain / Linux AES-256-GCM 加密文件
- 6 步闭环引导: 注册 → 登录 → 装 plugin → 配默认通道 → 知识库 → 商机匹配
- 开放式知识库录入: discover (生成 rawText 骨架) + card (按行业拆能力卡片) + submit (idempotent 入库 + 冲突检测)
- 关联公司录入: relate (xls/html 合同解析, 拆 top 客户 / 供应商 / 类别聚合)
- bot turn 调用 LLM 工具 (web_search / web_fetch / image / pdf / memory_search / wiki_search) 作为数据源
- 错误结构化: 统一返 `{ ok, stage, code, retryable, hint, traceId }`

### 改 (Changed)

- 通道元数据真源 = OpenClaw runtime (读 `openclaw channels list --json`)
- 默认通道真源 = opphub-server (PATCH `/api/user/channels/default`)
- token 写入方 = opphub-plugin (Keychain 单写入, skill 不双源)
- OAuth device flow start 30 秒内复用 (避免重复申请 device_code)
- ingest-batch 用 mkdtemp 每次独立目录 (避免并发竞态)

### 弃用 (Deprecated)

- `bin/opphub-knowledge-autofill.js` (DEPRECATED 2026-07-22) — 读本机敏感源违反产品红线
- `bin/opphub-cron-setup.js` (DEPRECATED 2026-07-22) — v4 cron 改由 plugin 维护

### 修 (Fixed)

- knowledge-card 行业歧义时双 JSON 输出
- token refresh 返字符串 (无法读 expires_at) 改为返完整对象
- OAuth URL/path 改 spawn argv 避免 shell 注入
- knowledge-relate 必需列校验 + 金额解析增强 (逗号/中文/括号负数/货币符号)
- knowledge-relate 二进制 xls 检测 (拒绝 OLE2 二进制)

### 安全 (Security)

- skill 不再读 token / IM channel / openclaw.json / outbox / MEMORY (隐私红线)
- skill 不再硬编码真实 user open_id (cron fallback 改为返 null)
- 错误响应含 traceId 便于排查

### 已知限制

- cron 操作 (create/list/rm) 需 plugin 已装 (peer 由 plugin 维护)
- knowledge POST 路径 v2 (opphub-web server 端合并待定)
- refresh endpoint 探测待 plugin client 暴露