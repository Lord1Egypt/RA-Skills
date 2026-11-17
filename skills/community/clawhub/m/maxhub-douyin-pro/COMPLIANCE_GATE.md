# 合规提醒系统框架 - 抖音

**版本**：1.0.0 | **生效日期**：2026-07-10 | **适用范围**：抖音（douyin-pro）

---

## 1. 系统概述

本框架定义 抖音 skill 的运行时合规提醒机制，采用三层防护：

| 层级 | 机制 | 触发时机 | 目标 |
|------|------|----------|------|
| 第一层 | 首次使用合规闸门 | 用户首次使用 抖音 skill 时 | 确保用户知悉法律风险并明确同意 |
| 第二层 | 风险检测与定向提醒 | 每次用户请求命中风险规则时 | 针对高风险操作提供定向警告 |
| 第三层 | 审计日志 | 每次合规交互 | 记录合规交互供审计追溯 |

**平台风险警告**：抖音对未授权数据访问可能采取封号、诉讼等法律行动

**法律内容版本**：`legal_version: 1.0.0`。版本变更时，首次闸门将重新触发。

---

## 2. 首次使用合规闸门

### 2.1 触发条件

Agent 在执行任何 抖音 skill 功能前，必须检查合规确认状态：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
[ -f "$COMPLIANCE_DIR/confirmed_douyin-pro.txt" ] && cat "$COMPLIANCE_DIR/confirmed_douyin-pro.txt" || echo "not_found"
```

- 返回 `not_found`：首次使用，触发完整合规闸门
- 返回的 `legal_version` 低于 `1.0.0`：法律内容已更新，重新触发闸门
- 返回的 `legal_version` 等于 `1.0.0`：已确认，跳过闸门

### 2.2 完整合规提醒内容

当触发首次闸门时，向用户显示以下提醒：

> ⚠️ **法律合规提醒 - 抖音**
>
> 本 skill 通过第三方数据聚合服务（MaxHub API）获取 抖音 数据，**非平台官方 API**。
>
> **数据来源声明**：
> - 本项目不持有、不存储、不控制任何平台数据
> - 所有数据请求经 MaxHub API（`https://www.aconfig.cn`）中转至 抖音
> - MaxHub API 的数据获取方式未获得 抖音 官方授权
>
> **合法使用场景**：公开数据分析、竞品研究、内容创作辅助、学术研究、自动化测试
>
> **禁止使用场景**：
> - 电信诈骗相关活动（《反电信网络诈骗法》）
> - 侵犯他人通信自由和通信秘密（《宪法》第40条）
> - 规避实名身份验证（《网络安全法》第24条）
> - 代发私信或消息
> - 收集、存储未公开的个人信息（联系方式、位置、社交关系）
> - 使用他人登录凭证（cookie/token）访问非本人数据
>
> **已移除的高风险能力**：刷量操控、反爬绕过、会话伪造、批量提取、私信、登录加密等端点已从代码中完全移除。
>
> **平台特定风险**：抖音对未授权数据访问可能采取封号、诉讼等法律行动
>
> **完整法律条款**：请参阅 [数据使用政策](./DATA_USAGE_POLICY.md) 和 [合规审查清单](./COMPLIANCE_CHECKLIST.md)。
>
> 输入 **"同意"** 确认已阅读并遵守以上条款，或输入 **/legal** 查看完整法律条款。

### 2.3 确认验证规则

**接受的确认措辞**（明确肯定）：
- `同意`
- `确认`
- `我已阅读并同意`
- `我同意`
- `确认同意`

**拒绝的模糊回应**（需提示用户使用明确措辞）：
- `嗯` / `ok` / `行` / `好的` / `可以` / `嗯嗯` / `好` / `yes`
- 回复提示："请使用明确措辞确认（如输入'同意'），以确保您已阅读并理解合规条款。"

**用户拒绝或未确认时**：
- **必须停止**，不执行 Step 1 及后续任何步骤
- 即使用户再次要求执行操作，也必须先完成合规确认
- 提示用户可输入 `/legal` 查看完整法律条款

### 2.4 确认通过后操作

```bash
# 写入确认状态文件
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
mkdir -p "$COMPLIANCE_DIR" && echo "legal_version=1.0.0 confirmed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$COMPLIANCE_DIR/confirmed_douyin-pro.txt"

# 记录审计日志
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"douyin-pro","event":"first_time_confirmation","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

---

## 3. 风险检测与定向提醒

### 3.1 风险类别

本 skill 的 `risk_rules.yaml` 包含以下风险类别：

**基础风险类别**：

| 类别 | 描述 | 检测方式 |
|------|------|----------|
| `cookie_usage` | 涉及 cookie/session/token 凭证 | 关键词匹配 + 端点标志 |
| `batch_operation` | 批量操作请求 | 关键词匹配 |
| `personal_data` | 个人信息查询（粉丝/关注/画像/联系方式） | 关键词匹配 |
| `write_operation` | 写入操作 | 端点标志（write_operation: true） |

**条件性风险类别（本 skill 适用）**：

| （无） | 本 skill 无额外条件性风险类别 | - |

> 完整风险规则见本目录下的 `risk_rules.yaml`。

### 3.2 风险检测流程

每次用户请求时，agent 对照 `risk_rules.yaml` 检查：

1. **关键词检测**：用户请求中是否包含风险类别的关键词
2. **端点标志检测**：匹配的端点是否带有 `cookie_warning`、`write_operation` 等标志
3. **平台检测**：本 skill 为国内平台，不触发跨境数据类别

### 3.3 定向提醒模板

命中风险时，显示对应类别的定向提醒：

**cookie_usage**:
> ⚠️ **风险提醒：Cookie/凭证使用**
> 此操作需要使用 cookie 或登录凭证。请确认：
> - 使用的是您本人的账号凭证
> - 不使用他人账号的 cookie 或 session
> - 了解凭证可能被滥用的风险
> 输入 **"同意"** 继续。

**batch_operation**:
> ⚠️ **风险提醒：批量操作**
> 此请求涉及批量数据采集。请确认：
> - 遵循最小必要原则，不采集超出使用目的的数据
> - 不用于批量注册、刷量等违规场景
> - 已评估平台服务条款的限制
> 输入 **"同意"** 继续。

**personal_data**:
> ⚠️ **风险提醒：个人信息查询**
> 此请求涉及个人信息（粉丝/关注/画像/联系方式等）。请确认：
> - 遵循《个人信息保护法》最小必要原则
> - 不存储、不传播查询到的个人信息
> - 尊重数据主体的被遗忘权
> 输入 **"同意"** 继续。

**write_operation**:
> ⚠️ **风险提醒：写入操作**
> 此操作为写入/非幂等操作，可能产生副作用。请确认：
> - 已确认操作参数正确
> - 了解操作不可撤销
> - 操作符合平台服务条款
> 输入 **"同意"** 继续。


### 3.4 风险提醒确认

确认规则与首次闸门相同（§2.3）。确认后记录审计日志：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"douyin-pro","event":"risk_reminder","risk_type":"<matched_category>","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

---

## 4. 审计日志规范

### 4.1 日志文件

- **路径**：`$HOME/.maxhub-skills/.compliance/audit_log.jsonl`
- **格式**：JSONL（每行一个 JSON 对象）
- **编码**：UTF-8

### 4.2 日志条目结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `timestamp` | string | ISO 8601 UTC 时间戳 |
| `skill` | string | `douyin-pro` |
| `event` | string | 事件类型（见下表） |
| `risk_type` | string | 命中的风险类别（仅 risk_reminder 事件） |
| `legal_version` | string | 当时的法律内容版本 |
| `status` | string | `confirmed` / `rejected` / `pending` |

**事件类型**：

| event | 说明 |
|-------|------|
| `first_time_confirmation` | 首次合规闸门确认 |
| `risk_reminder` | 风险检测提醒 |
| `legal_review` | 用户主动查阅法律条款 |
| `api_call` | API 调用审计 |

### 4.3 日志保留

- 审计日志不自动删除
- 日志文件通过 `.gitignore` 排除，不纳入版本控制
- 日志仅用于合规审计目的，不用于其他用途

---

## 5. 法律条款查阅命令

用户可随时通过以下方式查阅完整法律条款：

- 输入 `/legal`
- 输入 `查看法律条款`
- 输入 `法律条款`

Agent 收到以上指令后：

1. 读取并显示 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md) 的完整内容
2. 记录审计日志：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"douyin-pro","event":"legal_review","legal_version":"1.0.0","status":"completed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

---

## 6. 版本控制

### 6.1 版本字段

- `legal_version`：法律内容版本号，当前为 `1.0.0`
- 版本号格式：`主版本.次版本.修订号`

### 6.2 版本变更流程

当法律法规或合规要求发生变化时：

1. 更新本目录下的 `DATA_USAGE_POLICY.md` 和 `COMPLIANCE_GATE.md`
2. 递增 `COMPLIANCE_GATE.md` 中的 `legal_version`
3. 递增 `risk_rules.yaml` 中的 `version`
4. 首次闸门将因版本号不匹配而重新触发

### 6.3 快速更新机制

- 修改本目录下的 `risk_rules.yaml` 即可更新风险检测逻辑
- 修改本目录下的 `DATA_USAGE_POLICY.md` 即可更新法律条款
- 修改本文件的 §3.3 即可更新提醒文案
- `SKILL.md` Step 0.5 已内嵌核心风险规则摘要，完整规则见 `risk_rules.yaml`

---

*本框架不构成法律建议。如有具体法律问题，请咨询专业律师。*

*最后更新：2026-07-10*
