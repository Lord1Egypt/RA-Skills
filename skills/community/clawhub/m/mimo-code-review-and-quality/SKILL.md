---
name: code-review-and-quality
version: 1.4.0
description: |
  多维度质量审查，覆盖五轴（正确性/可读性/架构/安全/性能）+ Agent Skill安全审计（NVIDIA SkillSpector 16类漏洞模式 + Palo Alto BIV声明-行为完整性验证 + MCP Server安全审计）。
  26%的Agent技能含漏洞，5.2%含恶意代码，80%存在声明与行为偏差——安全轴升级为八维：代码安全+Skill供应链+MCP权限+提示注入+数据外泄+特权升级+BIV完整性+MCP Server审计。
  触发：合并PR前、Skill安装前、MCP Server部署前、功能实现后、重构后、bug修复后、方案提交前。
---

# Code Review and Quality（代码/方案审查与质量）

## Overview

多维度质量审查，带质量门控。每个变更在合并前都要审查 — 没有例外。

审查覆盖五个轴：**正确性、可读性、架构、安全、性能**。

**批准标准：** 当变更明确改善了整体质量时就批准，即使不完美。完美代码不存在 — 目标是持续改进。不要因为变更不完全是你会写的方式就阻塞。如果它改善了代码库并遵循了项目约定，批准它。

## When to Use

- 合并任何 PR 或变更之前
- 完成功能实现之后
- 评估其他 Agent 或模型产出的代码/方案时
- 重构现有代码之后
- 任何 bug 修复之后（审查修复和回归测试）
- 重要技术方案/文档提交之前

## The Five-Axis Review（五轴审查）

### 1. Correctness（正确性）

代码/方案是否做了它声称要做的事？

- [ ] 是否匹配规格或任务要求？
- [ ] 边界情况是否处理（null、空值、边界值）？
- [ ] 错误路径是否处理（不只是 happy path）？
- [ ] 是否通过所有测试？测试是否真的在测正确的东西？
- [ ] 是否有 off-by-one 错误、竞态条件、状态不一致？
- [ ] 数据流是否正确？输入→处理→输出链条完整？

### 2. Readability & Simplicity（可读性与简洁性）

另一个工程师（或Agent）能否在不靠作者解释的情况下理解？

- [ ] 命名是否描述性且与项目约定一致？（禁止无上下文的 `temp`、`data`、`result`）
- [ ] 控制流是否直接？（避免嵌套三元运算、深层回调）
- [ ] 代码组织是否逻辑清晰？（相关代码分组、清晰的模块边界）
- [ ] 是否有应该简化的"聪明"技巧？
- [ ] **能否用更少行数完成？** （1000行解决100行就能解决的问题是失败）
- [ ] **抽象是否赚回了它的复杂度？** （第三个用例出现前不要泛化）
- [ ] 是否有死代码残留：无用变量、向后兼容垫片、`// removed` 注释？

### 3. Architecture（架构）

变更是否适合系统的设计？

- [ ] 是否遵循现有模式？如果引入新模式，是否有理由？
- [ ] 是否维护了清晰的模块边界？
- [ ] 是否有应该共享的代码重复？
- [ ] 依赖方向是否正确？（无循环依赖）
- [ ] 抽象级别是否适当？（不过度工程化，不过于耦合）

### 4. Security（安全）— 含 SkillSpector 增强

**4a. 代码安全（传统检查项）：**

- [ ] 用户输入是否经过验证和清理？
- [ ] 密钥是否远离代码、日志和版本控制？
- [ ] 认证/授权是否在需要的地方检查？
- [ ] SQL 查询是否参数化？（禁止字符串拼接）
- [ ] 输出是否编码以防止 XSS？
- [ ] 依赖是否来自可信来源且无已知漏洞？
- [ ] 外部数据源（API、日志、用户内容）是否被视为不可信？

**4b. Agent Skill 供应链安全（v1.1.0 新增，源自 NVIDIA SkillSpector 16 类漏洞模式）：**

> 背景：42,447 个公开技能中 26.1% 含漏洞、5.2% 含恶意意图（Liu et al., 2026）

| 检查维度 | 关键风险 | 快速验证 |
|----------|---------|---------|
| 提示注入(5种) | 指令覆盖、隐藏指令、有害内容 | 检查 markdown 注释/隐藏 HTML/零宽字符 |
| 数据外泄(4种) | 发送 env vars/文件到外部服务器 | grep `fetch`/`http`/`curl` + 检查目标URL |
| 特权升级(3种) | sudo/root/cron 持久化 | grep `sudo`/`chmod 777`/`cron`/`systemctl` |
| 供应链(6种) | 未锁定依赖、`curl\|bash`、混淆代码 | 检查 unpinned deps / Base64 / `eval()` |
| 过度代理(4种) | 不受限工具访问、自主高影响决策 | 审查工具白名单是否有 `*` 通配符 |
| 系统提示泄漏(3种) | 直接/间接提取系统指令 | 检查输出是否可能包含内部 prompt |
| 记忆投毒(3种) | 持久上下文注入、窗口填充 | 检查是否写入 MEMORY/references 无验证 |
| MCP 权限(4种) | 声明权限 > 实际使用（或反之） | 对比 manifest vs 实际工具调用 |
| MCP 工具投毒(4种) | Unicode 同形字、隐藏 HTML 注释 | 检查工具描述的不可见字符 |
| 流氓代理(2种) | 自我修改、未授权持久化 | 检查自修改代码 + cron/startup |

**4c. CI/CD 管线安全（v1.2.0 新增，源自 OpenAI Axios 供应链攻击事件 2026-03）：**

> 背景：攻击者入侵 Axios 维护者账号，注入恶意代码到 v1.14.1，通过 GitHub Actions 泄露 OpenAI 签名证书

- [ ] GitHub Actions 工作流是否 pin 到完整 SHA（而非 `@v1`/`@main`）？
- [ ] 第三方 actions 是否限制在可信组织（`actions/*`、`github/*`、`docker/*`）？
- [ ] CI 环境变量中的签名证书/密钥是否避免打印到日志？
- [ ] 构建产物是否有完整性校验（checksum/signature verification）？
- [ ] 是否监控关键依赖的维护者变更（`npm owner`/`pip maintainer` diff）？
- [ ] `GITHUB_TOKEN`/`NPM_TOKEN` 权限范围是否最小化（read-only 优先）？

**4d. 声明-行为完整性验证 BIV（v1.3.0 新增，源自 Palo Alto Unit 42 "Trust No Skill" 研究 2026-06）：**

> 背景：对 49,916 个公开技能的审计发现 80%（39,933 个）存在声明与行为偏差，137 个偏差分类，4 种复合威胁模式

**核心方法：三面对比审计（Metadata vs Executable vs Natural-language）**

- [ ] **SKILL.md 声明 vs 代码行为**：技能描述声称的能力是否与代码实际功能匹配？
  - 描述说"只读操作"但代码包含写入/删除/网络发送？
  - 描述说"本地处理"但代码包含外部 API 调用？
- [ ] **Manifest 权限 vs 实际调用**：YAML manifest 声明的工具权限是否与实际代码调用一致？
  - 声明只需 `read_file` 但代码调用了 `bash`/`fetch`/`subprocess`？
- [ ] **复合威胁链检测**：单个能力看起来无害，但组合后形成攻击链？
  - `FILE_READ → base64 编码 → NETWORK_SEND`（数据外泄链）
  - `ENV_READ → HTTP_POST → 外部服务器`（凭证窃取链）
  - `PROMPT_INJECT → MEMORY_WRITE → 持久上下文投毒`（记忆投毒链）
  - `TOOL_CALL → OUTPUT_EXFIL → SELF_REPLICATE`（自我复制链）

**BIV 快速命令参考：**
```bash
# 1. 提取技能声明的能力关键词
grep -i 'description\|capabilities\|features' SKILL.md
# 2. 提取代码实际的能力关键词
grep -rn 'fetch\|http\|exec\|eval\|spawn\|writeFile\|deleteFile\|network' scripts/
# 3. 对比：声明中没有但代码中存在的能力 → 偏差标记
# 4. 复合链：检查是否存在 READ→ENCODE→SEND 模式
grep -rn 'readFile\|readFileSync\|readdir' scripts/ | grep -l 'base64\|btoa\|Buffer.from'
```

**偏差严重度分级：**
| 级别 | 含义 | 示例 |
|------|------|------|
| **Benign** | 文档不完善，功能无害 | 描述遗漏了一个次要功能 |
| **Suspicious** | 偏差需要解释 | 声明"本地处理"但有网络调用（可能是日志） |
| **Malicious** | 明确的欺骗行为 | 声明"无网络"但实际发送凭证到外部 |

**4e. MCP Server 安全审计（v1.4.0 新增，源自 2026-06 MCP 生态爆发 + Akamai KYA 信任框架）：**

> 背景：2026年6月一周内 Azure App Service / Oracle Essbase / IBM watsonx / AWS DevOps Agent / MDN 等 5+ 企业级 MCP Server 发布，MCP 正成为 Agent 工具调用的事实标准协议。MCP Server 暴露 REST API 为 AI 可调用工具，其安全风险不同于传统 API——AI Agent 自主决策调用，无人类逐次审批。

**MCP Server 安全检查清单：**

| 检查维度 | 关键风险 | 快速验证 |
|----------|---------|---------|
| **认证与授权** | OAuth 2.1 配置是否正确？PKCE 是否强制？ | 检查 `/.well-known/oauth-authorization-server` 端点 |
| **工具权限分级** | 是否实现 viewer/analyst/admin 三级权限？默认是否只读？ | 检查启动参数默认 profile，grep `viewer\|analyst\|admin` |
| **凭证保护** | 错误响应是否脱敏？是否泄露密码/token/路径？ | 构造错误请求，检查 error response 内容 |
| **破坏性操作确认** | delete/update 操作是否要求 confirm 参数？ | 检查 mutating tools 是否有 `confirm` 参数要求 |
| **输出边界** | 查询结果是否有 max_rows 限制？是否防止 token 爆炸？ | 检查 `max_rows`/`limit`/`output_bound` 配置 |
| **传输安全** | stdio vs streamable-http 选择是否合理？HTTP 是否强制 TLS？ | 检查 `--transport` 默认值，非 loopback 绑定是否要求 auth token |
| **网络隔离** | 非 loopback 绑定是否有默认保护？ | 检查 bind address 默认值和 MCP_AUTH_TOKEN 要求 |
| **审计日志** | 所有 mutating 操作是否有审计记录？ | 检查 INFO/WARN 级别日志是否覆盖 tool 调用 |
| **工具目录治理** | 是否有 YAML policy 定义工具拦截规则？启动时是否扫描不安全工具？ | 检查 `AgentGovernance` 配置和 startup scan |
| **OpenAPI 映射安全** | 从 OpenAPI spec 自动生成 MCP 工具时，是否审查了每个 operation 的副作用？ | 对比 OpenAPI spec 中 POST/PUT/DELETE 操作与生成的 MCP 工具 |

**MCP Server 审计快速命令：**
```bash
# 1. 认证检查：是否要求 auth token
grep -rn 'auth\|token\|oauth\|pkce\|credential' server.py main.py app.py
# 2. 权限分级：默认 profile 是否为 viewer
grep -rn 'profile\|viewer\|admin\|read.only\|default.*mode' *.py *.ts *.js
# 3. 破坏性操作确认
grep -rn 'confirm\|destructive\|delete\|drop\|truncate' tools/ handlers/
# 4. 输出边界
grep -rn 'max_rows\|limit\|output_bound\|page_size\|cap' *.py *.ts
# 5. 网络绑定安全
grep -rn 'bind\|host\|0\.0\.0\.0\|loopback\|127\.0\.0\.1' *.py *.ts *.js
# 6. 凭证脱敏
grep -rn 'redact\|mask\|sanitize\|scrub' errors/ middleware/ utils/
# 7. 审计日志
grep -rn 'audit\|log.*tool\|log.*mutation\|info.*call' *.py *.ts
```

**MCP Server 安全评级：**
| 评级 | 条件 | 建议 |
|------|------|------|
| **A** | 默认只读 + 凭证脱敏 + 破坏性确认 + 审计日志 + 输出边界 | 可部署到生产 |
| **B** | 缺少 1-2 项但无 Critical 缺陷 | 补充后部署 |
| **C** | 默认非只读 或 无认证 或 凭证可能泄露 | 修复后重新审计 |
| **F** | 无认证 + 无权限分级 + 无输出边界 | 拒绝部署 |

### 5. Performance（性能）

变更是否引入了性能问题？

- [ ] 是否有 N+1 查询模式？
- [ ] 是否有无界循环或不受约束的数据获取？
- [ ] 是否有应该是异步的同步操作？
- [ ] 是否有不必要的 UI 重渲染？
- [ ] 是否有列表端点缺少分页？
- [ ] 是否有热路径中创建的大对象？

## Change Sizing（变化规模控制）

小的、聚焦的变更更容易审查、更快合并、更安全部署。

```
~100 行变更    → 好。一次审查完成。
~300 行变更    → 可接受，如果是单个逻辑变更。
~1000 行变更   → 太大。拆分。
```

**什么时候算"一个变更"：** 一个自包含的修改，解决一件事，包含相关测试，提交后系统保持功能完整。是功能的一部分 — 不是整个功能。

**拆分策略：**

| 策略 | 方法 | 适用场景 |
|------|------|---------|
| **堆叠** | 提交一个小变更，基于它开始下一个 | 顺序依赖 |
| **按文件组** | 为需要不同审查者的文件组分开变更 | 跨领域关注 |
| **水平** | 先创建共享代码/stub，再创建消费者 | 分层架构 |
| **垂直** | 分解为更小的全栈功能切片 | 功能开发 |

**大变更可接受的场景：** 完整文件删除和自动化重构（审查者只需验证意图，不需要逐行审查）。

**将重构与功能开发分开。** 既重构又添加新行为的变更是两个变更 — 分开提交。

## Review Process（审查流程）

### Step 1: 理解上下文

在看代码之前，理解意图：
- 这个变更要完成什么？
- 它实现什么规格或任务？
- 预期行为变更是什么？

### Step 2: 先审查测试

测试揭示意图和覆盖范围：
- 变更有测试吗？
- 测试的是行为（不是实现细节）吗？
- 边界情况覆盖了吗？
- 测试名有描述性吗？
- 如果代码变了，测试能捕获回归吗？

### Step 3: 审查实现

带着五个轴遍历代码：

对每个变更的文件：
1. **正确性**：代码是否做了测试说它应该做的？
2. **可读性**：不靠帮助能理解吗？
3. **架构**：适合系统吗？
4. **安全**：有漏洞吗？
5. **性能**：有瓶颈吗？

### Step 4: 分类发现

为每个评审意见标记严重级别，让作者知道什么是必须的 vs 可选的：

| 前缀 | 含义 | 作者行动 |
|------|------|---------|
| **Critical:** | 阻塞合并 | 安全漏洞、数据丢失、功能破坏 |
| **Important:** | 需要修复 | 合并前必须处理 |
| **Nit:** | 次要、可选 | 作者可以忽略 — 格式、风格偏好 |
| **Optional:** / **Consider:** | 建议 | 值得考虑但不必须 |
| **FYI** | 仅供参考 | 不需要行动 — 为未来参考的上下文 |

这防止作者把所有反馈都当作必须的而在可选建议上浪费时间。

### Step 5: 验证验证

检查作者的验证故事：
- 运行了什么测试？
- 构建通过了吗？
- 手动测试了变更吗？
- UI 变更有截图吗？
- 有 before/after 比较吗？

### Step 6: Skill 安装前审计 & MCP Server 审计（v1.1.0 新增，v1.3.0 BIV增强，v1.4.0 MCP审计）

安装任何 Agent Skill 或部署任何 MCP Server 前执行此快速审计（≤3分钟）：

**Phase A: 静态扫描（原有）**
1. **危险函数扫描**：检查 scripts/ 目录是否有 `exec`/`eval`/`subprocess`/`__import__`
2. **网络行为**：grep 所有 `.js`/`.py`/`.sh` 中的外部URL，标记非已知域名
3. **依赖锁定**：检查是否有 unpinned deps（`*` 版本）或 `curl | bash`
4. **隐藏指令**：检查 markdown 中是否有 HTML 注释/零宽字符/Base64 编码块
5. **持久化检查**：grep `cron`/`systemctl`/`.bashrc`/`startup`/`schedule`

**Phase B: BIV 声明-行为完整性验证（v1.3.0 新增）**
6. **三面对比**：SKILL.md 描述 vs manifest 权限 vs 代码实际行为 → 标记偏差
7. **复合链检测**：检查是否存在 `READ→ENCODE→SEND` / `ENV→HTTP` / `INJECT→MEMORY→PERSIST` 模式
8. **偏差评级**：每个偏差标记 Benign/Suspicious/Malicious

**Phase C: MCP Server 安全审计（v1.4.0 新增，仅 MCP Server 部署时执行）**
9. **认证检查**：确认 OAuth 2.1/PKCE/Access Token 配置正确
10. **默认权限**：确认默认为 viewer（只读）模式
11. **凭证脱敏**：构造错误请求验证 error response 不含密码/token/路径
12. **破坏性确认**：确认 delete 类工具要求 `confirm` 参数
13. **输出边界**：确认查询结果有 max_rows 限制
14. **网络绑定**：确认非 loopback 绑定要求 MCP_AUTH_TOKEN
15. **MCP 安全评级**：按 4e 评级表给出 A/B/C/F 评级

**判定规则：**
- 0 Suspicious + 0 Malicious → ✅ 可安装
- 1-2 Suspicious + 0 Malicious → ⚠️ 需作者解释偏差后安装
- 任何 Malicious → ❌ 拒绝安装
- 复合威胁链存在 → ❌ 立即拒绝，不论单步看起来多无害

**MCP Server 判定规则（v1.4.0 新增）：**
- 评级 A 或 B + Phase A/B 无 Critical → ✅ 可部署
- 评级 C → ⚠️ 修复后重新审计
- 评级 F → ❌ 拒绝部署

**快速命令参考：**
```bash
# 危险函数扫描
grep -rn 'exec\|eval\|subprocess\|__import__\|child_process' scripts/
# 外部网络调用
grep -rn 'fetch\|http\|https\|curl\|wget\|axios' scripts/
# 持久化行为
grep -rn 'cron\|systemctl\|bashrc\|startup\|schedule' .
# BIV: 复合威胁链检测
grep -rl 'readFile\|readFileSync\|open(' scripts/ | xargs grep -l 'base64\|btoa\|Buffer.from'
grep -rl 'process.env\|os.environ' scripts/ | xargs grep -l 'fetch\|http\|post\|axios'
```

## Review Output Template（审查输出模板）

```markdown
## Review: [变更标题]

### 上下文
- [ ] 我理解这个变更做什么、为什么

### 正确性
- [ ] 变更匹配规格/任务要求
- [ ] 边界情况已处理
- [ ] 错误路径已处理
- [ ] 测试充分覆盖变更

### 可读性
- [ ] 命名清晰一致
- [ ] 逻辑直接
- [ ] 无不必要的复杂性

### 架构
- [ ] 遵循现有模式
- [ ] 无不必要的耦合或依赖
- [ ] 适当的抽象级别

### 安全
- [ ] 代码中无密钥
- [ ] 边界处输入已验证
- [ ] 无注入漏洞
- [ ] 认证检查就位

### 性能
- [ ] 无 N+1 模式
- [ ] 无无界操作
- [ ] 列表端点有分页

### 验证
- [ ] 测试通过
- [ ] 构建成功
- [ ] 手动验证完成（如适用）

### 发现
| # | 发现 | 级别 | 轴 | 说明 |
|---|------|------|-----|------|
| 1 | ... | Critical/Important/Nit | ... | ... |

### 裁决
- [ ] **Approve** — 可以合并
- [ ] **Request changes** — 问题必须解决
```

## Handling Disagreements（处理分歧）

当解决审查分歧时，应用此层级：
1. **技术事实和数据** 优先于意见和偏好
2. **风格指南** 是风格问题的绝对权威
3. **软件设计** 必须基于工程原则评估，不是个人偏好
4. **代码库一致性** 是可接受的，前提是不降低整体质量

**不要接受"我稍后清理。"** 经验表明延迟清理很少发生。要求提交前清理。

## Honesty in Review（审查中的诚实）

- **不要橡皮图章。** 没有审查证据的"LGTM"对任何人都没帮助。
- **不要弱化真实问题。** "这可能是个小问题"而实际上是将影响生产的 bug 是不诚实的。
- **尽可能量化问题。** "这个 N+1 查询会为列表中的每一项增加约50ms" 比 "这可能很慢" 更好。
- **对有明确问题的方案推回。** 谄媚是审查中的失败模式。
- **优雅接受覆盖。** 如果作者有完整上下文并不同意，尊重他们的判断。

## Common Rationalizations

| 借口 | 现实 |
|------|------|
| "能用就行了" | 能用但不可读/不安全/架构错误的代码创造复利债务。 |
| "我写的，所以我知道是对的" | 作者对自己的假设视而不见。每个变更都受益于另一双眼睛。 |
| "稍后清理" | 稍后从不到来。审查是质量门控 — 使用它。 |
| "测试通过了所以没问题" | 测试是必要的但不充分。它们不捕获架构问题、安全问题或可读性问题。 |
| "变更太小不需要审查" | 小变更也可能引入安全漏洞或破坏边界情况。 |

## Red Flags

- 变更未经审查就合并
- 只检查测试是否通过的审查（忽略其他轴）
- 没有审查证据的"LGTM"
- 安全敏感变更没有安全焦点的审查
- 太大无法认真审查的变更（拆分它们）
- bug 修复 PR 没有回归测试
- 没有严重级别标签的审查意见
- 接受"我稍后修复" — 它从不发生

## Verification

审查完成后：
- [ ] 所有 Critical 问题已解决
- [ ] 所有 Important 问题已解决或明确延迟（附理由）
- [ ] 测试通过
- [ ] 构建成功
- [ ] 验证故事已记录（变了什么、如何验证的）
