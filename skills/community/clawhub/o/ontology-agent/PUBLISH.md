# Ontology Agent — ClawHub 发布方案（PUBLISH.md）

> **英文名定案：Ontology Agent**（选项 A），slug `ontology-agent`，发布组织 `ontoai`（昂图AI）。
> **本版为中英双语版（中英文皆可适配）**：默认文件为英文，中文原版完整保留为 `.zh.md` / `.zh.yaml`。

## 1. 英文名（已选 A）

| 选项 | Display name | slug | 说明 |
|------|--------------|------|------|
| **A ✅ 已选** | **Ontology Agent** | `ontology-agent` | 与品牌 ontoagent.net / 中文名一致，最连贯；ClawHub 上直白好搜 |
| B | Digital Company Ontology | `digital-company-ontology` | 更突出"企业数字孪生"卖点，但偏离品牌 |
| C | OntoCraft | `ontocraft` | 短、好记，但与原品牌弱关联 |

> 商标提示：OntoAgent / OntoAI / OntoForge 在第 9 类已被堵死，故不使用；`ontology-agent` 安全且品牌一致。

## 2. 双语架构（本次核心改动）

```
默认文件 (.md / .yaml)      = 英文版   → 服务英文用户
.zh 文件 (.zh.md/.zh.yaml)  = 中文原版 → 服务中文用户
```

**路由规则已写入 `SKILL.md` 顶部**（AI 加载后据此选择）：
- 英文用户 → 读 `SKILL.md` / `README.md` / `GUIDE.md` / `references/*.yaml` / `references/packs/*.yaml`
- 中文用户 → 读 `SKILL.zh.md` / `README.zh.md` / `GUIDE.zh.md` / `references/*.zh.yaml` / `references/packs/*.zh.yaml`
- 权威中英术语对照表：`references/glossary.yaml`

**关键设计：机器键两版完全一致**——动作 `slug`、`source` 代号、部门码、实体类型名，以及整个
`scripts/` + `experts-template/` 层都不随语言变化，因此**脚本在任一语言下都能正常运行**。

## 3. 翻译清单 / 中文保留清单

**已译为英文（门面文档 + 内核部门动作目录）：**

| 文件 | 内容 |
|------|------|
| `SKILL.md` | frontmatter + 全文 + 双语路由规则 |
| `README.md`、`GUIDE.md` | 说明与六步引导 |
| `references/product_intro.md` | 产品介绍 |
| `LICENSE.md`、`THIRD-PARTY.md` | 法律与开源声明 |
| `references/contact.yaml` | 厂商联系信息（AI 读取后回复用户） |
| **`references/department_actions.yaml`** | **内核：24 部门 / 177 动作绑定，完整英译** |
| **`references/action_specs.yaml`** | **内核：159 个动作定义（name / desc / inputs / outputs）完整英译** |
| **`references/packs/*.yaml`（8 个）** | **内核：行业包全译** — opc / ecommerce / sme / biomed / edu_research / finance / manufacturing（含 12 个 subtypes）/ public_institution |
| **`experts-template/department_experts.yaml`** | **内核：24 部门 AI 员工人设全译**（role / responsibilities / working_style / boundaries / report_style + 行业红线 flavor） |
| **`references/semantic.yaml`** | 语义层：13 类实体 / 关系类型库 / 全局约束库 |
| **`references/decision.yaml`** | 决策层：PII 红线 / 权限治理 / 决策规则 / 9 类合规红线 |
| **`references/logic.yaml`** | 逻辑层：toolset 范式 / 六阶段状态机 / 3 个工作流 |
| **`references/monitoring.yaml`** | 监测层：13 个信号域 + 自动化模板 |
| **`references/deployment.yaml`** | 部署层：三档形态 / 2 个 pattern / 6 个宿主平台 |
| **`references/roles.yaml`、`proactive.yaml`** | 角色治理 / 自发行为四档分级 |
| `references/customization.md`、`onboarding.md`、`portability.md` | 定制机制 / 渐进引导 / 可移植对接 |
| `connectors/dingtalk.yaml`、`wecom.yaml`、`feishu.yaml` | IM 接入契约 stub |
| `examples/demo_company/instance.yaml` | 示例实例 |

**中文原版完整保留（31 个 `.zh` 文件）：**
- 门面（9）：`SKILL.zh.md`、`README.zh.md`、`GUIDE.zh.md`、`LICENSE.zh.md`、`THIRD-PARTY.zh.md`、
  `references/product_intro.zh.md`、`customization.zh.md`、`onboarding.zh.md`、`portability.zh.md`
- 内核（18）：`action_specs.zh.yaml`、`department_actions.zh.yaml`、`semantic.zh.yaml`、`logic.zh.yaml`、
  `decision.zh.yaml`、`roles.zh.yaml`、`monitoring.zh.yaml`、`deployment.zh.yaml`、`proactive.zh.yaml`、
  `packs/*.zh.yaml`（8 个行业包）、`experts-template/department_experts.zh.yaml`
- 其他（4）：`connectors/{dingtalk,wecom,feishu}.zh.yaml`、`examples/demo_company/instance.zh.yaml`

## 4. 校验结果（全部通过）

| 校验项 | 结果 |
|--------|------|
| EN YAML 可解析 | **PASS** — 24 个英文 YAML 全部解析正常 |
| 双语结构一致性（EN vs ZH） | **PASS** — 9 组内核对（含 24 部门 / 177 动作 / 159 动作）机器键逐字一致 |
| 残留中文扫描 | **PASS** — 默认（英文）文件零残留中文（双语提示行与 glossary/contact 专有名词除外） |
| clawhub dry-run | **PASS** — `ok:true` / `would-publish` / 83 文件 / slug `ontology-agent` |

> 唯一"结构差异"：`proactive.yaml` 的授权键 `if_owner_authorization_is_*` 英译为
> `key_confirmation` / `full_delegation`（中文版为 `关键确认` / `全委托`）。这是有意的键名本地化，
> 已在文件头注明"须与所用语言版本的 instance.yaml 保持一致"。

## 5. 关键词 / 分类

- **categories（3）**：`knowledge, agents, productivity`
- **topics（6）**：`ontology-agent, ai-employees, company-digitization, knowledge-graph, digital-twin, enterprise-agents`
- 备选补充：`one-person-company, sme, agent-team`

## 6. 发布命令

```bash
clawhub skill publish ./clawhub-ontology-agent \
  --slug ontology-agent \
  --name "Ontology Agent" \
  --owner ontoai \
  --changelog "Bilingual (zh+en) edition: English default + full Chinese originals preserved" \
  --categories knowledge,agents,productivity \
  --topics "ontology-agent,ai-employees,company-digitization,knowledge-graph,digital-twin"
```

## 7. 遗留项

1. **Python 脚本界面字串未英译**（`scripts/*.py`）：代码逻辑本身是英文，仅 CLI 提示/报错为中文。
   属"英文骨架 + 中文显示层"，不影响功能；如需全英化可后续处理（本轮未动，避免引入回归风险）。
   注：`glossary.yaml` 本就内置 `zh`+`en` 双语字段，无需翻译；`.gitkeep.md` 为占位文件。
2. **组织头像**：ontoai 组织头像（昂图AI 带红色波浪纹 512×512）因 ClawHub 头像上传组件服务端故障未上传
   —— 顺然已决定**搁置不处理**。
3. **待确认后真实发布**：本包已 dry-run 通过，等顺然确认后执行真实发布。
