# Multi-Model Orchestrator

基于 [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) 框架的多模型编排系统。集成 **superpowers-systematic-debugging**（调试纪律）和 **frontend-design**（UI 品质）。

## 核心工作流

```
$deep-interview → $ralplan → $team / $ralph → $code-review
                                        ↓
                              $debug (遇 bug)  $frontend (遇 UI)
```

### 模式

| 模式 | 触发词 | 说明 |
|------|--------|------|
| `$deep-interview` | "澄清需求" "我不确定" | 先澄清再行动 |
| `$ralplan` | "规划一下" "制定计划" | Planner/Architect/Critic 共识 |
| `$team N` | "并行执行" "同时做" | N 个 Agent 并行执行 |
| `$ralph` | "做完它" "持续执行" | 单 Agent 持久完成 |
| `$debug` 🆕 | "有 bug" "测试失败" "报错了" | 四阶段系统化调试 |
| `$frontend` 🆕 | "做个页面" "前端" "UI" | 多模型协作 UI 开发 |
| `$code-review` | "审查代码" "code review" | 多模型交叉审查（含 UI） |
| `$autopilot` | "全自动" | ralplan → ralph → code-review |

## 模型分配

| 角色 | 模型 | 用途 |
|------|------|------|
| 🧠 Architect | `sub2api-openai/gpt-5.5` | 架构设计、复杂推理、调试根因分析 |
| 💻 Coder | `sub2api-openai/gpt-5.3-codex` | 代码生成、调试修复实现 |
| ⚡ Executor | `mimo/mimo-v2.5-pro` | 快速执行（免费）、UI 交互 |
| 🔍 Reviewer | `sub2api-openai/gpt-5.5` | 代码审查、UI 结构审查 |
| ⚡ Quick | `sub2api-openai/gpt-5.4-mini` | 简单任务 |
| 🎨 Frontend | `sub2api-openai/gpt-5.3-codex` | UI 样式/主题 |

## 集成技能

| 来源 | 集成内容 | 应用模式 |
|------|---------|---------|
| [superpowers-systematic-debugging](https://github.com/wcygan/dotfiles/tree/main/config/claude/skills/superpowers-systematic-debugging) | 四阶段调试流程、铁律、红旗识别 | `$debug` + `$ralph`/`$autopilot` 自动调试 |
| [frontend-design](https://github.com/iuliandita/skills/tree/main/skills/frontend-design) | UI 品质标准、AI 美学红线、双主题、移动优先 | `$frontend` + `$code-review` UI 审查 |

## 使用方式

```bash
# 调试
"帮我调试这个报错"                    # $debug 四阶段调试
"测试失败了"                         # $debug
"这个 bug 修了3次都不行"              # $debug（自动质疑架构）

# 前端
"帮我做个登录页面，要有深色浅色主题"    # $frontend
"做个管理后台界面"                    # $frontend
"审查一下这个 UI"                    # $frontend + UI 审查

# 编排
"帮我编排：实现一个 REST API"          # 自动选择模式
"用 $deep-interview 澄清需求"         # 需求澄清
"用 $ralplan 规划方案"                # 共识规划
"用 $team 3 并行执行"                 # 3 路并行
"用 $ralph 完成这个任务"              # 持久完成
"用 $code-review 审查代码"            # 代码审查
"全自动搞定"                         # $autopilot
```

## 目录结构

```
multi-model-orchestrator/
├── SKILL.md              # OpenClaw skill 入口（增强版：含 $debug + $frontend）
├── README.md             # 本文件
├── agents/
│   └── team.json         # Agent 团队定义
├── workflows/
│   ├── deep-interview.md # 需求澄清工作流
│   ├── ralplan.md        # 共识规划工作流
│   ├── team.md           # 并行执行工作流
│   └── ralph.md          # 持久完成工作流
├── skills/
│   ├── code-review.md    # 代码审查技能
│   ├── security-review.md# 安全审查技能
│   └── tdd.md            # TDD 技能
└── scripts/
    └── orchestrate.sh    # 编排脚本
```

## License

MIT
