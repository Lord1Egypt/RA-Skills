# 企业应急响应指导 Skill（AI 时代｜工程化闭环 + 多智能体协作）

本 Skill 支持两种模式：
1. **单智能体模式**：传统AI助手模式，适合个人使用和快速响应
2. **多智能体模式**：多角色协作模式，适合团队协作和复杂事件处理

核心吸收：
- **TCH 大赛**：Harness/Environment Engineering、共享状态（黑板/WAL）、纠偏（Advisor/Alignment）、证据驱动（VBR）。  
- **Solar 应急题解**：以"应急工程师视角"从流量/日志/主机/内存取证出发，还原攻击路径与处置链路（并提醒"比赛方法不等于生产最优解"，需结合环境）。
- **NOPTrace Linux/Windows 应急响应手册**：吸收了现场处置顺序、低误用证据保全、按事件类型分流、Linux/Windows 常规安全检查、善后与横向定损等高价值内容。
- **多智能体架构**：角色分工、并行分析、智能协调、HITL人工确认，提升复杂事件处理效率和质量。

---

## 0) 使用前提（强约束）
1) **仅限授权与合规场景**（内部处置/演练/委托）  
2) **先取证后处置**：对业务影响大的动作必须走 HITL 闸门  
3) **VBR（Verify Before Reporting）**：结论必须可复现、可追溯  
4) **共享状态优先**：必须把关键事实写入 WAL（`memory/working/current_session.json`）

---

## 1) 角色分工（可单人执行，但建议按角色思维推进）
- **IC（Incident Commander）**：定范围、定优先级、审批高风险动作（HITL）
- **Lead Analyst**：技术研判、证据链、时间线、IOC
- **Scribe（记录员）**：用 note.py 把事实/证据/动作写入 WAL
- **Advisor（纠偏顾问）**：打转/无进展时重写计划（loop_detector 输出模板）

---

## 1.1 事件分流（必须先判断是哪一类）
优先将事件归入以下一类或多类：

### 传统IT基础设施事件
- 挖矿 / 木马 / 远控
- 勒索
- 暴力破解 / 账号被盗 / 权限滥用
- 钓鱼
- 隧道 / 非授权代理 / 中转
- 非持续性事件（偶发恶意外联/执行）
- 数据库事件（MSSQL / MySQL / Redis / Mongo 等）
- 供应链 / 恶意软件包
- BadUSB / 介质投毒

### AI基础设施事件（新增）
- 模型服务被投毒/后门
- GPU集群异常/挖矿
- MLOps平台被入侵/数据泄露
- AI智能体失控/恶意行为
- 训练数据投毒/污染
- AI API被滥用/恶意调用
- 模型逆向/知识产权泄露
- AI供应链攻击（恶意依赖库/预训练模型）

若无法归类，先按 `triage` 做"证据固定 + 范围界定"，不要急于处置。

可优先参考：
- `playbooks/常见事件处置速查.md`
- `playbooks/Linux应急响应现场手册.md`
- `playbooks/Windows应急响应现场手册.md`
- `playbooks/AI基础设施应急响应手册.md`（新增）
- `playbooks/善后与横向定损检查单.md`

---

## 2) 阶段机（FSM）：用证据驱动应急流程
推荐阶段：
1) `detect`：告警接收与初筛（是否真实事件）
2) `triage`：范围界定、证据收集、初步根因假设
3) `contain`：最小影响隔离（网关/EDR 优先）
4) `eradicate`：清除与加固（补丁/配置/凭据/持久化清理）
5) `recover`：恢复业务、验证无残留
6) `postmortem`：复盘与进化（候选经验→审核→合并）
7) `report`：交付报告与改进项

进入/退出门槛（示例）：
- 进入 contain：必须完成最小证据集（见 playbooks/取证与证据规范.md）
- 进入 eradicate：必须有可复现的根因证据（VBR）
- 进入 recover：必须验证关键 IOC/持久化已清除，并监测一段时间

---

## 3) WAL（黑板）协议：必须写什么（降噪）

### 3.1 初始化会话
```bash
python3 scripts/note.py --phase triage \
  --set incident_name="2026Q2-疑似挖矿告警" \
  --set scope="srv-01,10.0.0.0/24,example.com" \
  --set rules="最小影响+先取证后处置+关键动作需HITL确认"
```

### 3.2 结构化 actions（推荐）
```bash
python3 scripts/note.py "验证：发现异常高CPU进程，疑似挖矿" --phase triage \
  --action verify --verdict pass --reason "cpu-anomaly" \
  --tool ssh --target "srv-01" --evidence "./evidence/top.txt"
```

### 3.3 IOC 与时间线（推荐）
```bash
python3 scripts/note.py --ioc-ip "1.2.3.4" --ioc-domain "bad.example" \
  --timeline "2026-04-29 10:21:00 发现异常外联到 1.2.3.4:443"
```

### 3.4 建议补充字段（真实企业处置强烈建议）
```bash
python3 scripts/note.py --severity high --timezone Asia/Shanghai \
  --source edr --source siem --stakeholder "应急负责人" --stakeholder "系统负责人" \
  --asset "srv-01" --asset "10.0.0.12" --asset "支付业务"
```

---

## 4) HITL 闸门（必须人工确认）
满足任一条件必须先询问确认：
- 隔离主机/封禁账号/下线服务（影响业务）
- 删除文件/重启/恢复系统命令（可能破坏现场）
- 大范围封禁/大范围猎杀（误封风险）

询问必须包含：动作、影响面、可回滚方式、预期收益、替代方案。

---

## 5) 卡住/打转：强制纠偏（Advisor）
```bash
python3 scripts/loop_detector.py
```
将输出的 Advisor 模板粘贴给 AI，要求其重写 3-6 步 TodoList（每步含 VBR 验证点与风险提示）。

---

## 6) 交付（报告 + 时间线）
```bash
python3 scripts/generate_report.py --out reports/ir-report.md
```
会同时生成：
- `reports/ir-report.md`
- `reports/timeline.md`

报告中会重点输出：
- 范围、时区、告警源、干系人、资产
- IOC 清单
- 关键证据与关键动作
- 遏制 / 清除 / 恢复动作
- 经验教训与下一步

---

## 7) 可门禁进化（候选→审核→合并）
1) 生成候选（不合并）：
```bash
python3 scripts/retrospect_ir.py --limit 5
```
2) 列出候选：
```bash
python3 scripts/apply_updates_ir.py --list
```
3) 负责人审核后合并：
```bash
python3 scripts/apply_updates_ir.py --ids cand-... --reviewer "应急负责人"
```

---

## 8) CTF 应急题模式（CTF-IR）如何使用本 Skill

> 你可以把 CTF 应急题当作“低成本、可复现的桌面演练”：流程与方法复用真实应急，但**输出目标**变为“回答题目问题/提交 flag”。  
> 本 Skill 通过 `mode=ctf` + `flags[]` 支持将“解题产出”纳入同一套 WAL/证据链/复盘进化体系。

### 8.1 CTF-IR 的工作原则
1) **依然先取证后处置**：CTF 题常见陷阱是“急于清除导致丢线索”（例如内存/日志线索）
2) **VBR 更严格**：每个答案都要能指向“证据锚点”（哪段日志/哪条流量/哪个文件/哪个命令输出）
3) **明确题目→证据→答案映射**：把每个题目问题当作一个子任务，分别验证
4) **允许更激进但要写清楚**：CTF 环境可能允许重启/删除/修改（与生产不同），但仍建议“先导出证据再操作”，并在 notes 中注明“这是 CTF 环境动作”

### 8.2 初始化（CTF 模式）
```bash
python3 scripts/note.py --mode ctf --flag-format "flag{...}" --phase triage \
  --set incident_name="Solar-IR-CTF-题目名" \
  --set scope="给定镜像/pcap/日志包" \
  --set rules="先取证后处置+答案必须可复现+低噪声记录"
```

### 8.3 记录答案（flags）
建议把“题目=答案”写进 WAL：
```bash
python3 scripts/note.py --flag "问题1=flag{...}" --evidence "./evidence/q1-proof.txt"
python3 scripts/note.py --flag "攻击者IP=10.0.100.22" --evidence "./evidence/accesslog-snippet.txt"
```

### 8.5 CTF-IR 解题 Playbook（推荐）
见：`playbooks/CTF应急题解题模板.md`

### 8.4 交付
CTF 题结束后同样可以生成报告与时间线（便于复盘/教学）：
```bash
python3 scripts/generate_report.py --out reports/ir-ctf-report.md
```

---

## 9) 多智能体模式（Multi-Agent）- 高级特性

> 适用场景：复杂事件处理、团队协作、需要并行分析、大规模应急响应

### 9.1 多智能体架构概览

系统支持两种模式：
- **单智能体模式**（默认）：单个AI助手处理所有任务
- **多智能体模式**（高级）：多个专业化智能体协作处理

### 9.2 核心智能体角色

| 智能体 | 角色 | 职责 |
|--------|------|------|
| **IC Agent** | 指挥官 | 全局决策、资源调度、HITL审批 |
| **Analyst Agent** | 分析师 | 技术研判、证据分析、IOC提取 |
| **Scribe Agent** | 记录员 | WAL记录、证据管理、报告生成 |
| **Advisor Agent** | 顾问 | 循环检测、纠偏建议、最佳实践推荐 |
| **Forensics Agent** | 取证专家 | 证据收集、内存/磁盘取证 |
| **Threat Intel Agent** | 威胁情报专家 | IOC丰富、威胁情报查询 |
| **Recovery Agent** | 恢复专家 | 恢复计划制定与执行 |
| **Compliance Agent** | 合规专家 | 合规检查、监管报告 |

### 9.3 启用多智能体模式

```python
from multi_agent.framework.agent_framework import Orchestrator

async def main():
    # 创建协调器
    orchestrator = Orchestrator()
    await orchestrator.initialize()
    
    # 创建会话
    session_id = await orchestrator.create_session("应急响应事件")
    
    # 创建智能体
    await orchestrator.spawn_agent("ic_agent", "multi_agent/agents/ic_agent.yaml")
    await orchestrator.spawn_agent("analyst_agent", "multi_agent/agents/analyst_agent.yaml")
    await orchestrator.spawn_agent("scribe_agent", "multi_agent/agents/scribe_agent.yaml")
    
    # 运行工作流
    await run_incident_response(orchestrator, session_id)
```

### 9.4 并行分析优势

**单智能体模式**：
```
Task 1 (5分钟) → Task 2 (10分钟) → Task 3 (8分钟)
总耗时：23分钟
```

**多智能体模式**：
```
Task 1 (Agent A, 5分钟) ┐
Task 2 (Agent B, 10分钟)├→ 汇总 (2分钟)
Task 3 (Agent C, 8分钟) ┘
总耗时：12分钟（节省48%）
```

### 9.5 HITL人工确认增强

在多智能体模式下，HITL流程更加完善：

1. **Analyst Agent** 提出遏制建议
2. **Advisor Agent** 评估风险与替代方案
3. **IC Agent** 审批（触发HITL）
4. **人类决策者** 最终确认
5. **IC Agent** 下达执行命令

### 9.6 智能体协作示例

```python
# 并行收集证据和分析
tasks = [
    Task(task_type="collect_evidence", priority=Priority.HIGH),
    Task(task_type="analyze_logs", priority=Priority.HIGH),
    Task(task_type="enrich_iocs", priority=Priority.MEDIUM)
]

# 并行提交到不同智能体
for task in tasks:
    await orchestrator.task_router.submit_task(task)
    await orchestrator.task_router.route_task(task)

# 等待结果汇总
results = await wait_for_all_tasks(tasks)
```

### 9.7 冲突解决机制

当多个Analyst Agent提出不同结论时：

1. **投票机制**：简单多数决策
2. **权重机制**：基于历史准确率加权
3. **IC Agent最终决策**：指挥官裁决
4. **人类升级**：复杂情况升级到人工

### 9.8 配置文件

所有智能体配置文件位于：`multi_agent/agents/`

```yaml
# 示例：ic_agent.yaml
name: ic_agent
role: Incident Commander
capabilities:
  - risk_assessment
  - decision_making
  - coordination
hitl_policy:
  triggers:
    - action_type: host_isolation
      timeout: 300
```

### 9.9 工作流定义

标准应急响应工作流：`multi_agent/workflows/standard_ir.yaml`

包含完整的阶段转换、任务分配、HITL流程。

### 9.10 部署方式

**单机部署**（适合小型团队）：
```bash
python multi_agent/framework/agent_framework.py
```

**Docker部署**（适合生产环境）：
```bash
docker-compose up -d
```

**Kubernetes部署**（适合大规模部署）：
```bash
kubectl apply -f kubernetes/deployment.yaml
```

### 9.11 监控与运维

```python
# 监控智能体状态
async def monitor_agents():
    while True:
        for agent_id, agent in orchestrator.agents.items():
            print(f"{agent_id}: {agent.state.value}")
        await asyncio.sleep(30)
```

### 9.12 详细文档

- **架构设计**：`multi_agent/ARCHITECTURE.md`
- **部署指南**：`multi_agent/DEPLOYMENT_GUIDE.md`
- **工作流定义**：`multi_agent/workflows/standard_ir.yaml`
- **智能体配置**：`multi_agent/agents/*.yaml`

### 9.13 何时使用多智能体模式

**推荐使用**：
- ✅ 复杂事件（涉及多个系统、多种技术栈）
- ✅ 大规模事件（影响范围广、资产多）
- ✅ 团队协作（多人参与、分工明确）
- ✅ 高价值事件（业务关键、需要高质量分析）

**单智能体即可**：
- ⚪ 简单事件（单一系统、单一问题）
- ⚪ 快速响应（时间紧迫、无需深度分析）
- ⚪ 个人使用（单人处理、资源有限）

---

## 10) 快速决策指南

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 日常应急响应 | 单智能体 | 简单快速 |
| CTF应急题 | 单智能体（CTF模式） | 单人解题 |
| 复杂入侵事件 | 多智能体 | 需要并行分析 |
| 勒索事件 | 多智能体 | 需要多专家协作 |
| 团队演练 | 多智能体 | 模拟真实协作 |
| AI基础设施事件 | 多智能体 | 需要专业智能体 |

---

## 11) 扩展与定制

本Skill设计为高度可扩展：

1. **添加新智能体**：创建新的YAML配置和Python类
2. **自定义工作流**：修改或新增工作流YAML文件
3. **集成外部系统**：通过API集成SIEM/EDR/SOAR等工具
4. **定制playbook**：根据组织特点定制处置流程

详见：`IMPROVEMENT_ROADMAP.md`
