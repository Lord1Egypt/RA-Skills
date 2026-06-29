---
name: hermes-workflow-engine
description: |
  Hermes DAG工作流引擎 v3.0 — 目标驱动的多步骤任务编排系统。
  支持DAG依赖、并行执行、故障转移、资源监控、版本管理、模式检测、可视化面板、社区共享。
  当用户要求执行工作流、运行workflow、自动化任务、多步骤任务、创建工作流、模式检测、
  版本管理、DAG编排、并行执行、故障转移时触发。
  适用场景：重复性多步骤任务自动化、需要暂停/恢复的长流程、跨工具协作编排。
triggers:
  - "执行工作流"
  - "运行workflow"
  - "自动化任务"
  - "多步骤任务"
  - "创建工作流"
  - "模式检测"
  - "版本管理"
  - "DAG编排"
  - "并行执行"
  - "故障转移"
  - "run workflow"
  - "automate task"
version: 3.0.0
author: 小狗
tags: [workflow, dag, automation, orchestration, metaskill]
---

# Workflow Engine v3.0

Hermes版MetaSkill — 目标驱动的多步骤任务编排系统。

## 何时使用

- 用户说"执行工作流xxx"
- 用户说"自动化这个任务"
- 用户说"创建工作流"
- 用户说"模式检测"或"发现重复任务"
- 用户说"版本管理"或"版本对比"
- 需要多步骤协作的复杂任务
- 需要暂停/恢复的任务

## 架构总览

```
~/.hermes/workflow-engine/
  ├─ engine.py              # DAG核心：解析、拓扑排序、环检测、状态管理
  ├─ executor.py            # 执行器：5种步骤类型、故障转移、并行执行
  ├─ resource_monitor.py    # 资源监控：token/时间/API预算控制
  ├─ pattern_detector.py    # 模式检测：历史扫描、聚类分析、提案生成
  ├─ version_manager.py     # 版本管理：版本化存储、对比、回滚、变更日志
  ├─ dashboard.py           # 可视化面板：HTML实时执行状态
  ├─ community.py           # 协作共享：导出/导入、社区库、评分、同步
  ├─ run.py                 # CLI入口：16个命令
  ├─ FORMAT.md              # YAML工作流格式规范
  ├─ test_engine.py         # 测试脚本
  ├─ examples/              # 示例工作流
  ├─ workflows/             # 版本化存储
  ├─ runs/                  # 运行记录
  └─ _community/            # 社区库
```

## CLI命令（16个）

```bash
# 基础操作
python3 ~/.hermes/workflow-engine/run.py list                              # 列出工作流
python3 ~/.hermes/workflow-engine/run.py validate <yaml>                   # 验证工作流
python3 ~/.hermes/workflow-engine/run.py plan <yaml>                       # 执行计划

# 执行相关
python3 ~/.hermes/workflow-engine/run.py next <yaml>                       # 下一批可执行步骤
python3 ~/.hermes/workflow-engine/run.py parallel <yaml>                   # 并行执行计划
python3 ~/.hermes/workflow-engine/run.py execute <yaml> [inputs_json]      # 生成执行指令
python3 ~/.hermes/workflow-engine/run.py delegate <yaml> [inputs_json]     # delegate_task格式

# 高级功能
python3 ~/.hermes/workflow-engine/run.py detect [days] [min_confidence]    # 模式检测
python3 ~/.hermes/workflow-engine/run.py dashboard [run_dir]               # 生成可视化面板

# 版本管理
python3 ~/.hermes/workflow-engine/run.py versions <name>                   # 列出版本
python3 ~/.hermes/workflow-engine/run.py diff <name> <v1> <v2>             # 版本对比
python3 ~/.hermes/workflow-engine/run.py rollback <name> <version>         # 回滚版本

# 社区共享
python3 ~/.hermes/workflow-engine/run.py community list [tag]              # 列出社区工作流
python3 ~/.hermes/workflow-engine/run.py community search <keyword>        # 搜索社区
python3 ~/.hermes/workflow-engine/run.py community publish <name>          # 发布到社区
python3 ~/.hermes/workflow-engine/run.py community install <name>          # 从社区安装
python3 ~/.hermes/workflow-engine/run.py community rate <name> <1-5>       # 评分
python3 ~/.hermes/workflow-engine/run.py community export <name>           # 导出.tgz
python3 ~/.hermes/workflow-engine/run.py community import <tgz_path>       # 导入.tgz
```

## 工作流执行流程

1. **加载验证** — `validate` 检查YAML格式和依赖
2. **查看计划** — `plan` 确认步骤顺序和并行层
3. **按层执行** — 按拓扑排序的层逐步执行：
   - terminal类型 → 用terminal工具执行
   - skill类型 → 加载skill后按prompt执行
   - subagent类型 → 用delegate_task执行（并行层用batch模式）
   - user_input类型 → 用clarify暂停等用户输入
   - llm类型 → 直接生成内容
4. **故障转移** — 主路径失败时自动尝试备选方案
5. **资源监控** — 跟踪token/时间消耗，超预算暂停
6. **更新状态** — 每步完成后更新state.json
7. **生成面板** — `dashboard` 生成HTML可视化面板

## YAML工作流格式

```yaml
name: my-workflow          # 必填，小写+连字符，≤64字符
version: "1.0"             # 语义化版本号
description: "工作流描述"   # 必填，≤256字符
author: 绪哥
tags: [tag1, tag2]

trigger:
  type: manual | cron | event
  schedule: "0 8 * * *"    # cron格式，仅type=cron时生效

resources:
  max_tokens: 50000        # token预算上限
  max_time: 300            # 秒，总执行时间上限
  max_api_calls: 50        # API调用次数上限

inputs:
  - name: topic            # 变量名，步骤中用 {{topic}} 引用
    type: string
    default: "AI"

steps:
  - id: step1              # 必填，全局唯一，小写+连字符
    name: "步骤名称"
    type: terminal | skill | subagent | user_input | llm
    depends: []            # 依赖的步骤ID列表，空=第一层
    config:
      command: "shell命令"         # terminal类型，支持{{变量}}插值
      skill_name: "技能名"         # skill类型
      prompt: "提示词"             # skill/llm类型
      goal: "目标"                 # subagent类型
      toolsets: ["web","terminal"] # subagent类型，可选
    output:
      type: text | file
      variable: "输出变量名"       # 后续步骤用{{变量名}}引用
    timeout: 120                   # 秒，单步超时
    retry:
      max_attempts: 3              # 重试次数
      on_fail: abort | skip | pause
      fallbacks:                   # 故障转移链
        - type: terminal
          command: "备选命令"

error_handling:
  on_step_fail: pause | skip | abort  # 全局失败策略
  notify: true                         # 失败时通知用户
```

## 步骤类型

| type | 执行方式 | config关键字段 |
|------|---------|---------------|
| terminal | terminal工具 | command |
| skill | skill_view + 按prompt执行 | skill_name, prompt |
| subagent | delegate_task | goal, toolsets |
| user_input | clarify暂停 | prompt |
| llm | 直接LLM生成 | prompt, model |

## 故障转移机制

每步骤有完整的故障转移链：
1. **用户显式fallback** — YAML中定义的fallbacks
2. **同类工具自动备选** — 内置映射表（web_search→tavily→firecrawl等）
3. **降级方案** — 用缓存/跳过/标注

失败策略（on_fail）：
- `abort` — 中止工作流（默认）
- `skip` — 跳过该步骤继续
- `pause` — 暂停等用户决定

## 同类工具备选映射

```python
TOOL_FALLBACKS = {
    'web_search': ['tavily-search', 'firecrawl', 'hermes-cli'],
    'tavily-search': ['web_search', 'firecrawl'],
    'firecrawl': ['web_search', 'tavily-search'],
    'baoyu-infographic': ['sn-infographic', 'claude-design'],
    'terminal': ['execute_code'],
    'browser': ['web_fetch', 'terminal:curl'],
}
```

## 并行执行

DAG拓扑排序自动识别可并行步骤：
- 同一层的步骤无依赖关系 → 自动并行
- 使用delegate_task batch模式执行
- 等待所有并行步骤完成后再进入下一层

## 资源监控

执行前预估、执行中监控：
- Token消耗（默认预算100000）
- 执行时间（默认预算600s）
- API调用次数（默认预算50）
- 超80%预警，超100%暂停

## 模式检测

扫描历史session发现重复任务：
- 关键词提取（任务类型+工具使用模式）
- 频次统计+置信度评估
- 自动生成工作流提案（含YAML模板）
- 阈值过滤（默认≥0.3置信度才提案）

## 版本管理

每个工作流独立版本化存储：
```
~/.hermes/workflow-engine/workflows/<name>/
  ├─ v1.0.yaml          # 版本快照
  ├─ v2.0.yaml
  ├─ current.yaml → v2.0  # 当前版本链接
  ├─ meta.json           # 元信息
  ├─ changelog.md        # 变更日志
  └─ metrics.json        # 运行指标
```

支持：版本对比(diff)、回滚(rollback)、运行指标记录

## 可视化面板

生成HTML实时执行状态面板：
- 步骤进度（pending/running/success/failed/paused）
- 资源消耗进度条
- 错误信息展示
- 暗色主题

## 协作共享

社区工作流库：
- 导出为.tgz包（含所有版本+元信息）
- 从.tgz导入
- 社区库浏览/搜索/评分
- 下载计数
- 版本同步检查

## 创建新工作流

1. 创建YAML文件到 `~/.hermes/workflow-engine/examples/`
2. 定义name、description、steps
3. `validate` 验证
4. `plan` 查看执行计划
5. 执行
6. `community publish` 发布到社区

### 快速创建工作流示例

```bash
# 1. 创建YAML
cat > ~/.hermes/workflow-engine/examples/my-task.yaml << 'EOF'
name: my-task
version: "1.0"
description: "示例：搜索→总结"
author: 绪哥
tags: [example]

steps:
  - id: search
    name: "搜索"
    type: skill
    depends: []
    config:
      skill_name: "web-tools-guide"
      prompt: "搜索{{topic}}"
    output:
      type: text
      variable: "search_results"

  - id: summarize
    name: "总结"
    type: llm
    depends: [search]
    config:
      prompt: "总结以下内容：{{search_results}}"
    output:
      type: text
      variable: "summary"
EOF

# 2. 验证
python3 ~/.hermes/workflow-engine/run.py validate ~/.hermes/workflow-engine/examples/my-task.yaml

# 3. 查看计划
python3 ~/.hermes/workflow-engine/run.py plan ~/.hermes/workflow-engine/examples/my-task.yaml

# 4. 执行
python3 ~/.hermes/workflow-engine/run.py execute ~/.hermes/workflow-engine/examples/my-task.yaml '{"topic":"AI最新进展"}'
```

## 端到端执行工作流

当用户说"执行工作流xxx"时：

1. 加载YAML → `python3 run.py validate examples/xxx.yaml`
2. 查看计划 → `python3 run.py plan examples/xxx.yaml`
3. 获取指令 → `python3 run.py execute examples/xxx.yaml`
4. 按指令逐步执行：
   - terminal类型 → 调用terminal工具
   - skill类型 → skill_view加载后按prompt执行
   - subagent类型 → delegate_task执行
   - user_input类型 → clarify暂停
   - llm类型 → 直接生成
5. 每步完成后记录输出
6. 全部完成后保存运行日志

## 异常与故障排查

| 场景 | 触发条件 | 一线修复 | 仍失败兜底 |
|------|---------|---------|-----------|
| YAML解析失败 | 格式错误/缩进不对 | `python3 run.py validate <file>` 定位错误行 | 手动检查YAML缩进（2空格） |
| 环依赖检测 | A→B→A循环 | `python3 run.py validate` 自动报环 | 重画依赖图，打破循环 |
| 步骤超时 | 单步执行>timeout | 检查网络/API状态，重试 | `on_fail: skip` 跳过继续 |
| Token超限 | 资源监控报警 | 减少并行步骤或增大max_tokens | 暂停工作流，手动优化 |
| 子agent失败 | delegate_task返回错误 | 检查goal描述是否清晰 | 改用terminal类型直接执行 |
| 模式检测无结果 | session历史不足 | 增加扫描天数 `detect 30` | 手动创建工作流 |
| 版本回滚冲突 | 工作树脏 | `git stash` 后重试 | 从workflows目录手动复制yaml |
| 社区发布失败 | 网络/权限问题 | 检查_community目录权限 | 手动复制到_community/ |

## Pitfalls

- 步骤ID必须唯一（重复ID导致覆盖）
- 依赖必须指向已存在的步骤（悬空引用报错）
- 不能有环（A→B→A拓扑排序死循环）
- user_input步骤会暂停整个工作流（设timeout防永久挂起）
- 并行步骤需要互不依赖（有依赖的自动降为串行）
- 资源预估中user_input步骤默认300s（用户可能很久才回复）
- 模式检测需要session历史数据，首次运行可能无结果
- 版本管理的current.yaml是符号链接，Windows不支持
- **⚠️ DAG并行执行容易中断 (2026-06-09验证)**: 在实际执行ai-news-daily工作流时，第2层（信息图+文章并行）的执行被打断。原因是工作流引擎的多层DAG执行依赖连续的agent会话，而会话可能被用户消息/超时/上下文窗口限制中断。**对于固定流程任务（如每日新闻速报），直接用cron job prompt-driven方式比DAG编排更稳定可靠**。DAG引擎更适合需要动态决策、分支、条件跳转的复杂流程。

## 触发方式（六模式自动触发）

### ① 关键词触发（显式）
用户说"执行工作流xxx"等关键词时直接触发。

### ② 意图匹配触发（自动）
分析用户消息语义，自动匹配工作流模式。**不需要说触发词**：
```
用户: "帮我搜点AI新闻然后发公众号"
→ 检测到news_report意图，置信度1.0
→ 触发执行ai-news-daily工作流
```

支持的意图类型（10种）：
| 意图 | 触发词示例 | 匹配工作流 |
|------|-----------|-----------|
| news_report | 新闻、速报、日报 | ai-news-daily |
| research | 调研、研究、分析 | auto-research |
| content_creation | 写文章、公众号 | auto-content |
| data_analysis | 数据、Excel、报表 | auto-data |
| deployment | 部署、上线、发布 | auto-deploy |
| monitoring | 检查、巡检、状态 | auto-monitor |
| backup | 备份、同步、迁移 | auto-backup |
| image_gen | 图片、封面、海报 | auto-image |
| email | 邮件、邮箱 | auto-email |
| code_review | 代码、review、PR | auto-code-review |

### ③ 工具序列触发（自动）
检测到连续使用特定工具组合时触发：
```
连续使用: web_search → write_file → terminal
→ 匹配"搜索→写文件→执行"模式
→ 生成auto-search-write-execute工作流模板
```

### ④ 时间规律触发（自动）
发现固定时间做固定事时触发：
```
过去7天每天8点执行ai-news-daily
→ 自动设置cron: "0 8 * * *"
```

### ⑤ 历史模式触发（自动）
扫描session历史发现重复任务时触发：
```
过去7天做了3次"搜索→信息图→文章"
→ 置信度0.75
→ 创建标准工作流
```

### ⑥ 事件驱动触发（自动）
外部事件匹配工作流时触发：
```
收到邮件 → 触发auto-email工作流
收到PR → 触发auto-code-review工作流
```

### 触发器使用

```bash
# 分析消息意图
python3 run.py trigger "帮我搜点AI新闻"

# 检查定时触发
python3 run.py trigger-scheduled
```

### 触发决策流程

```
用户消息进来
  ├─ 关键词匹配 → 直接触发
  ├─ 意图分类器 → 匹配工作流 → 提议执行
  ├─ 工具序列检测 → 匹配历史模式 → 提议创建工作流
  └─ 都不匹配 → 正常对话

cron定时
  ├─ 时间规律检测 → 自动执行/提议
  └─ 历史模式扫描 → 提议创建工作流

事件监听
  └─ 收到事件 → 匹配事件工作流 → 执行
```

## 🔴 CHECKPOINT

以下操作必须先征得用户确认再执行：

| # | 操作 | 需确认内容 |
|---|------|-----------|
| 1 | **创建工作流** | 先validate验证YAML格式和依赖正确性 |
| 2 | **执行工作流** | 先plan确认步骤顺序和并行层，检查资源预估 |
| 3 | **user_input步骤** | 暂停等待用户输入，不可自动跳过 |
| 4 | **发布到社区** | 确保工作流已测试通过，版本号正确 |
| 5 | **版本回滚** | 确认回滚目标版本，会创建新变更日志 |
| 6 | **删除工作流** | 不可恢复，确认用户意图 |
| 7 | **并行执行>5步骤** | 确认资源预算充足，避免token/时间超限 |

## 模块依赖关系

```
engine.py (独立，无外部依赖)
  ↑
executor.py (依赖engine.py)
  ↑
resource_monitor.py (独立)
pattern_detector.py (独立)
version_manager.py (独立)
dashboard.py (独立)
community.py (依赖version_manager.py)
  ↑
run.py (依赖所有模块)
```

### 模块职责矩阵

| 模块 | 核心职责 | 输入 | 输出 |
|------|---------|------|------|
| engine.py | DAG解析、拓扑排序、环检测 | YAML文件 | ExecutionPlan对象 |
| executor.py | 步骤执行、故障转移、并行 | ExecutionPlan + 步骤配置 | 步骤输出 |
| resource_monitor.py | token/时间/API预算监控 | 执行过程中的消耗 | 预警/暂停信号 |
| pattern_detector.py | 历史session扫描、聚类 | session历史 | 模式列表+提案 |
| version_manager.py | 版本化存储、对比、回滚 | YAML文件 | 版本快照+变更日志 |
| dashboard.py | HTML实时执行状态 | run_dir | HTML文件 |
| community.py | 导出/导入/社区库 | 工作流目录 | .tgz包/社区条目 |
| run.py | CLI入口，分发命令 | 用户命令 | 执行结果 |

### 数据流

```
用户命令 → run.py → engine.py (解析YAML)
                  → executor.py (执行步骤)
                  → resource_monitor.py (监控资源)
                  → dashboard.py (生成面板)
                  → version_manager.py (版本管理)
                  → community.py (社区共享)
```

## 扩展点

1. **新增步骤类型** — 在executor.py的TOOL_FALLBACKS添加映射
2. **新增工具备选** — 在TOOL_FALLBACKS字典中添加
3. **自定义资源估算** — 修改ResourceMonitor的DEFAULT_TOKEN_ESTIMATES
4. **自定义模式检测** — 修改pattern_detector.py的TASK_PATTERNS和TOOL_PATTERNS
5. **自定义面板样式** — 修改dashboard.py的HTML/CSS模板

## 部署与发布

### ClawHub 发布
```bash
# 1. 把代码复制到技能目录
cp ~/.hermes/workflow-engine/*.py ~/.hermes/skills/devops/workflow-engine/scripts/
cp -r ~/.hermes/workflow-engine/examples ~/.hermes/skills/devops/workflow-engine/scripts/

# 2. 发布
cd ~/.hermes/skills/devops/workflow-engine
clawhub publish . --slug hermes-workflow-engine --name "Hermes Workflow Engine" --version x.y.z

# 3. 验证
clawhub inspect hermes-workflow-engine --files
```

**⚠️ 关键：ClawHub 只发布技能目录内的文件。代码必须在 `scripts/` 下，否则别人安装后没有代码。**

### GitHub 仓库
https://github.com/LGX281227231/workflow-engine

### 跨服务器部署（龙虾）
```bash
# 1. 创建目录
ssh root@43.173.120.234 "mkdir -p /root/.openclaw/workspace/workflow-engine"

# 2. 打包传输
cd ~/.hermes/workflow-engine && tar czf /tmp/wf.tar.gz --exclude='runs/*' --exclude='_community/*' *.py *.md examples/
scp /tmp/wf.tar.gz root@43.173.120.234:/tmp/

# 3. 解压并适配路径
ssh root@43.173.120.234 "cd /root/.openclaw/workspace/workflow-engine && tar xzf /tmp/wf.tar.gz"
ssh root@43.173.120.234 "sed -i 's|Path.home() / .hermes / workflow-engine|Path.home() / .openclaw / workspace / workflow-engine|g' /root/.openclaw/workspace/workflow-engine/run.py"
```

→ 详细发布流程见 [references/clawhub-publishing.md](references/clawhub-publishing.md)

## 参考与理论基础

| 资源 | 说明 |
|------|------|
| [跨系统部署指南](references/cross-system-deployment.md) | Hermes→OpenClaw部署流程、路径适配、Pitfalls |
| [Apache Airflow DAG](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) | DAG编排参考，拓扑排序和依赖管理 |
| [MetaGPT MetaSkill](https://deepwisdom.github.io/) | MetaSkill概念来源，目标驱动多Agent协作 |
| [Karpathy autoresearch](https://github.com/karpathy/autoresearch) | 自主实验循环理念，ratchet机制来源 |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | 状态图编排，条件分支和循环 |
| [Prefect](https://docs.prefect.io/) | 现代工作流引擎，故障转移和重试策略 |
| [Temporal](https://docs.temporal.io/) | 持久化工作流，长时间运行任务 |
| [Hermes Agent Skills](https://hermes-agent.nousresearch.com/docs) | 本引擎运行的Agent平台 |
| [SkillLens arXiv 2605.23899](https://arxiv.org/abs/2605.23899) | Skill质量评估9维度rubric |
| [SkillOpt arXiv 2605.23904](https://arxiv.org/abs/2605.23904) | Validation-gated skill优化 |
| [DAG Scheduler理论](https://en.wikipedia.org/wiki/Directed_acyclic_graph) | DAG基础：拓扑排序、环检测、关键路径 |
| [OpenSquilla MetaSkill](https://github.com/opensquilla) | 工作流引擎设计灵感来源 |
| [Hermes Agent CLI参考](https://hermes-agent.nousresearch.com/docs/cli) | run.py使用的Hermes CLI工具 |
| [delegate_task文档](https://hermes-agent.nousresearch.com/docs/tools#delegate-task) | subagent类型步骤的执行方式 |
| [YAML规范](https://yaml.org/spec/1.2.2/) | 工作流定义文件格式 |
| [JSON Schema](https://json-schema.org/) | 工作流输入输出验证 |

### 相关文件

- `references/darwin-optimization-cycle.md` — 达尔文优化实战记录（80.3→98.4，5轮+触顶检测）
| [Darwin优化日志](references/darwin-optimization-log.md) | 本技能的达尔文优化记录（80.3→98.4） |

## 反例与黑名单

| # | 不要做的事 | 为什么 | 正确做法 |
|---|---|---|---|
| 1 | DAG中创建环依赖(A→B→A) | 拓扑排序死循环，引擎卡死 | `validate`检查环，依赖必须是有向无环图 |
| 2 | 并行步骤共享输出变量 | 竞态条件，结果不确定 | 并行步骤各自独立输出，合并到下一层 |
| 3 | 跳过validate直接执行 | YAML格式错误在运行时才暴露 | 先validate再plan再execute |
| 4 | user_input步骤无超时 | 用户不回复时工作流永久挂起 | 设置timeout，超时自动skip或abort |
| 5 | 在cron job中嵌套创建工作流 | 递归调度失控 | cron job只执行已有工作流，不动态创建 |
| 6 | 同一工作流并发执行多个实例 | 状态文件冲突，数据损坏 | 加文件锁或队列机制 |
| 7 | 用"建议/可以考虑"等软化词定义步骤 | LLM执行时产生歧义，可能跳过关键步骤 | 步骤指令必须是确定性命令式语句 |
| 8 | 省略fallback直接abort | 单点失败导致整个工作流中止 | 每步至少定义一个fallback方案 |
| 9 | 步骤输出变量名重复 | 后续步骤读到错误数据 | 每步variable全局唯一 |
| 10 | resources预算设太小 | 执行中途被resource_monitor暂停 | 按实际任务规模估算，留20%余量 |
