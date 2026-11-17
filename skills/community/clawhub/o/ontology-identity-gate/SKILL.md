---
name: ontology-identity-gate
description: 为 Agent 运营本体（Proposal Gate）提供 run-scoped 身份令牌（HMAC-SHA256，零第三方依赖）+ 两阶段提交治理：agent 只到 validated，commit 仅由 human 令牌触发；含指纹审计、scope 授权与 fail-closed 渐进启用。v1.1 增补对象级权限（mandatory Markings 行级 Visibility + clearance，单一 PolicyEvaluator 全入口 enforce）。触发：运营动作身份治理、agent-as-tool 消费编排、提案门禁 fail-open 收敛、决策指纹审计、对象/行级 ABAC 访问控制、PII/区域隔离。
metadata:
  version: "1.1"
  updated: "2026-11-08"
  layer: "L2-infra"
  input:
    kinds: [proposal_gate, identity_token, agent_toolchain, object_markings]
    max_chars: 200000
  boundaries:
    - "commit 只由 human 令牌触发，agent 令牌无法自提"
    - "secret 永不落 markdown/日志/git；默认 ~/.openclaw/state（0600）"
    - "identity 未配置 = 渐进兼容（P5 路径行为不变）；注入后 enforce 默认 fail-closed"
    - "不引入 OAuth/IdP/第三方依赖；v1.1 起对象级权限仅用标准库自实现"
    - "mandatory markings 走 AND + deny 优先/fail-closed；marking 挂标/移除须 owner 流程 + 审计"
---

# Ontology Identity Gate — 运营本体身份治理 + agent-as-tool 消费

> v1.0 | 2026-11-08 | L2 通用基础能力

把 Agent 对运营本体的"提案→校验→审批→提交"链路加上 **run-scoped 身份令牌**，
收敛 caller 身份 fail-open：任何写路径（propose/review/commit）都要求可验证的
令牌身份，且 **commit 永远由 human 令牌触发**。

## 何时使用

- 你的 Proposal Gate / 两阶段提交系统存在"调用方自报身份"（fail-open）问题；
- 需要让 agent 能"发起动作但无法自行提交"，人工审批后才能落地；
- 需要决策记录可审计：每条决策关联发起者 + 审批者的令牌指纹；
- 需要 MCP/工具层暴露 propose/review，但禁止 execute_*/write_*/commit_* 泄漏。

## 核心设计

### 1. 令牌（`IdentityAuthority`）

- 结构：`base64url(claims JSON) + "." + base64url(HMAC-SHA256(secret, payload))`
- claims：`run_id / sub / kind(human|agent) / scopes / iat / exp / jti`
- scope 语法：`<verb>:<action>:<domain>`，verb ∈ {propose, review}，支持 `*` 通配
- secret 托管：默认 `~/.openclaw/state/ontology-identity.secret`（0600，首次签发自动生成 32B），
  可 env `OPENCLAW_ONTOLOGY_SECRET`（hex/base64）覆盖（多机对齐）
- 校验失败一律抛异常（fail-closed）：`InvalidToken / TokenExpired / ScopeDenied`

### 2. Proposal Gate 接入

```python
svc = ProposalService(db, registry, identity=authority, enforce_identity=True)
```

- `identity=None`：身份治理未启用（兼容既有装配）；一旦注入，enforce 默认 True
- `propose_action(..., token=...)`：claims.sub/kind 为**权威身份**，与自报
  caller_id/caller_kind 冲突 → `InvalidToken`
- `review(..., token=...)`：human 级 action 要求 `claims.kind=human`；agent 令牌
  审 human 级动作 → 拒绝（叠加既有 `PermissionError`）
- `enforce_identity=False`：仅测试/历史逃生口，audit 标 `"identity_enforced": false`，
  生产恒 True

### 3. 决策指纹审计

migration 增加 `ont_decision_record.token_fingerprint`（ALTER 幂等 + 建表原生含列，
新老库一致）。approve/reject/commit 均落审批者令牌指纹（SHA256 前 16 hex）。

### 4. agent-as-tool 消费（`OntologyToolchain`）

```python
chain = OntologyToolchain(proposals, registry, authority)
out = chain.run_action(
    run_id="run-1", domain="your-domain", action="submit_to_oa",
    object_refs=["obj-1"], params={...},
    scopes=["propose:submit_to_oa:your-domain"],
    subject="agent:assistant", kind="agent",
    reviewer_token=operator_token(authority, "rex", domain_code="your-domain"),
)
# out["status"] == "committed"（human 令牌触发）或 "validated"（agent 到顶）
```

- `auto_review=False`（默认）：agent 只到 **validated**，绝不 commit
- `reviewer_token` 仅接受 `kind=human`；现场签发 operator 令牌（`operator:` 前缀）
- 幂等：同 `idempotency_key` 重放返回既有提案，不重跑

### 5. MCP 暴露

- handler 装配可选 `IdentityAuthority`（测试可注入固定 secret，隔离真实密钥文件）
- `ont_propose_action` / `ont_review_proposal` / 动态 `ont_propose_<name>` 透传 token
- descriptor 增加 `token` 字段；MCP 层不伪造令牌、不回显完整令牌

## 落地清单

1. `identity_token.py`：IdentityAuthority（issue/verify/authorize/fingerprint）+ operator_token
2. `db.py`：migration v12（token_fingerprint 列，`PRAGMA table_info` 幂等检查）
3. `proposal.py`：identity/enforce_identity 构造 + propose/review 校验 + 指纹入决策记录
4. `agent_toolchain.py`：OntologyToolchain（discover/run_action）
5. MCP server：装配 + token 透传 + descriptor
6. 测试：令牌原语 18 用例（fail-closed/篡改/过期/scope/指纹/逃生口）+ toolchain 7 用例
   + 端到端黄金用例（agent 停 validated / human 令牌 commit 双指纹）

## 6. 对象级权限（v1.1 增补，P7）

在 run/action 级 scope 之上叠加**行级 Visibility**：对象挂 mandatory markings，
主体须持有**全部** marking 且 clearance 达标。读/写/审/提/MCP **共用单一评估器**，
无旁路。

### 6.1 数据模型（migration v13）

- `ont_marking(domain_id, code, name, sensitivity[normal|high], owner)`：marking 注册
- `ont_marking_grant(marking_id, subject, source, granted_at, expires_at, revoked_at, granted_by)`：主体授予
- 对象不加新列：`metadata.markings=[...]` + `metadata.permissions.clearance`（JSON 内）

### 6.2 判定顺序（`PolicyEvaluator.evaluate`，deny 优先 / fail-closed）

1. **clearance**：四级 `public<internal<confidential<restricted`，主体须 ≥ 对象；claims 缺省 internal（不提权）
2. **markings AND**：缺任一 ⇒ deny(`missing_marking:<code>`)；引用未注册 code ⇒ deny(`unregistered_marking`)
3. **realtime 高敏复查**（仅 review/commit + sensitivity=high）：实时查 grant 表，吊销/过期 ⇒ deny(`realtime_revoked:<code>`)

坏 metadata（非 dict / markings 非数组 / clearance 非法）⇒ 一律 deny(`bad_metadata`)。

### 6.3 全入口接入

```python
# claims 由签发方写入，agent 不可自报提权
tok = authority.issue(subject="agent:a", kind="agent",
                      markings=["pii"], clearance="confidential", ...)
# ProposalService / MCP query / 动态工具全部透传 directory + token
# 读拒统一口径，不泄字段：{"found": true, "allowed": false, "error": "access denied"}
# commit 层 realtime_assert：防 review→commit 间隙高敏授予被吊销
```

### 6.4 授予可治理（D1/D2/D3）

- **D1**：grant 强制 `expires_at`、TTL 上限（默认 90 天）、`source` 枚举、revoke 留痕
- **D2**：高敏 marking review/commit 实时查 grant，短 TTL 收敛吊销延迟
- **D3**：clearance 单字段，`confidence_level` 仅只读别名
- 渐进启用：未注入 directory ⇒ 行为完全同 v1.0；对象无 marking 退化为只看 clearance；不回填历史

## 红线

- **validated ≠ committed**：validate 永不产生副作用；commit 只由 human 令牌触发
- **secret 永不落 markdown/日志/git**
- 不新增第三方依赖（仅标准库 hmac/hashlib/base64/json/secrets/datetime/dataclasses）
- 运行期结构 gate 关闭；注册仅装配期
- **mandatory markings AND + deny 优先/fail-closed**；marking 挂标/移除走 owner 流程 + 审计
- 写不过不落地：propose 校验须在 INSERT 之前；读拒不泄存在性字段

## 参考实现

- L2 组件：`L2-infra/components/ai-knowledge-base/ai_kb/ontology/identity_token.py`、
  `agent_toolchain.py`、`proposal.py`、`mcp/server.py`
- 验收：`L2-infra/components/ai-knowledge-base/docs/VERIFICATION-P6-operational-ontology-v1.0.md`、
  `VERIFICATION-P7-operational-ontology-v1.0.md`
- 详设：`L2-infra/components/ai-knowledge-base/docs/DESIGN-DETAIL-operational-ontology-p6-v1.0.md`、
  `DESIGN-DETAIL-operational-ontology-p7-v1.0.md`

## 变更历史

- v1.1（2026-11-08）：增补对象级权限（P7）— migration v13、MarkingDirectory、PolicyEvaluator、claims 扩展、全入口 enforce
- v1.0（2026-11-08）：初版 — run-scoped 身份令牌（P6）+ agent-as-tool
