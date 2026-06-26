# 🏯 Imperial Orchestrator

**[中文](./README.md)** | [English](./docs/README.en.md) | [日本語](./docs/README.ja.md) | [한국어](./docs/README.ko.md) | [Español](./docs/README.es.md) | [Français](./docs/README.fr.md) | [Deutsch](./docs/README.de.md)

---

OpenClaw 高可用多角色模型编排 Skill —— 三省六部制智能路由。

> **设计灵感**：角色架构借鉴了[三省六部制（edict）](https://github.com/cft0808/edict)的朝廷治理模式，融合了 [PUA](https://github.com/tanweai/pua) 的深度 AI 提示词工程技术。

## 核心能力

- **三省六部** 角色编排：10 个角色，各司其职
- **自动发现** 46+ 模型，从 openclaw.json 读取
- **智能路由** 按领域自动分派（编码/运维/安全/写作/法律/财务）
- **Opus 优先** 编程/安全/法律任务优先使用最强模型
- **跨 Provider 容灾** auth 熔断 → 跨厂商降级 → 本地生存
- **真实执行** API 调用 + Token 计算 + 成本追踪
- **基准测试** 同一题目丢给所有模型，打分排名
- **多语言** 支持中/英/日/韩/西/法/德 7 国语言

## 快速开始

```bash
# 1. 发现模型
python3 scripts/health_check.py --openclaw-config ~/.openclaw/openclaw.json --write-state .imperial_state.json

# 2. 探活验证
python3 scripts/model_validator.py --openclaw-config ~/.openclaw/openclaw.json --state-file .imperial_state.json

# 3. 路由任务
python3 scripts/router.py --task "用 Go 写一个并发安全的 LRU Cache" --state-file .imperial_state.json

# 一条命令搞定
bash scripts/route_and_update.sh full "Fix WireGuard peer sync bug"
```

## 三省六部角色体系

每个角色配备深度 system prompt，包含身份认同、职责边界、行为准则、协作意识和红线五个维度。

### 中枢

| 角色 | 官衔 | 朝制对应 | 核心使命 |
|------|------|---------|---------|
| **router-chief** | 中枢总管 | 天子/中枢院 | 系统的生命线——分类、路由、维持心跳 |

### 三省

| 角色 | 官衔 | 朝制对应 | 核心使命 |
|------|------|---------|---------|
| **cabinet-planner** | 内阁首辅 | 中书省 | 草拟方略——将混沌拆解为有序步骤 |
| **censor-review** | 都御史 | 门下省/都察院 | 封驳审核——质量的最后守门人 |

### 六部

| 角色 | 官衔 | 朝制对应 | 核心使命 |
|------|------|---------|---------|
| **ministry-coding** | 工部尚书 | 工部 | 兴修工程——编码、调试、架构 |
| **ministry-ops** | 工部侍郎 | 工部·营缮司 | 维护驿站——部署、运维、CI/CD |
| **ministry-security** | 兵部尚书 | 兵部 | 戍边防务——安全审计、威胁建模 |
| **ministry-writing** | 礼部尚书 | 礼部 | 文教礼仪——文案、文档、翻译 |
| **ministry-legal** | 刑部尚书 | 刑部 | 律法刑狱——合同、合规、条款 |
| **ministry-finance** | 户部尚书 | 户部 | 钱粮赋税——定价、毛利、结算 |

### 急递铺

| 角色 | 官衔 | 朝制对应 | 核心使命 |
|------|------|---------|---------|
| **emergency-scribe** | 急递铺令 | 急递铺 | 系统永不宕机的最后保障 |

## 运行规则

1. **401 熔断** — auth 失败立即标记 `auth_dead`，冷却整个 auth 链，优先跨 provider 切换
2. **路由器保持轻量** — 不给 router-chief 分配最重的 prompt 或最脆弱的 provider
3. **跨 Provider 优先** — fallback 顺序：同角色不同 provider → 本地模型 → 邻近角色 → 急递铺
4. **降级而非宕机** — 即使最强模型全挂，也能用架构建议、检查清单、伪代码回应

## 路由输出

```json
{
  "mode": "plan_then_execute",
  "mode_labels": {"zh": "先规划后执行", "en": "Plan then Execute", "ja": "計画後実行"},
  "lead_role": "ministry-coding",
  "lead_title": "工部尚书",
  "lead_titles": {"zh": "工部尚书", "en": "Minister of Engineering", "ja": "工部尚書"},
  "selected_model": "cliproxy/claude-opus-4-6",
  "fallback_chain": ["ollama/qwen3.5:27b", "cliproxy/gpt-5.1-codex"],
  "survival_model": "ollama/gpt-oss:20b"
}
```

## 项目结构

```
config/
  agent_roles.yaml          # 角色定义（职责、能力、降级链）
  agent_prompts.yaml        # 深度 system prompt（身份、规则、红线）
  routing_rules.yaml        # 路由关键词规则
  failure_policies.yaml     # 熔断/重试/降级策略
  benchmark_tasks.yaml      # 基准测试题库
  model_registry.yaml       # 模型能力覆写
  i18n.yaml                 # 7 国语言适配
scripts/
  lib.py                    # 核心库（发现、分类、状态管理、i18n）
  router.py                 # 路由器（角色匹配 + 模型选择）
  executor.py               # 执行引擎（API 调用 + fallback）
  orchestrator.py            # 完整流水线（路由→执行→审核）
  health_check.py           # 模型发现
  model_validator.py        # 模型探活
  benchmark.py              # 基准测试 + 排行榜
  route_and_update.sh       # 统一 CLI 入口
```

## 安装

### 前置条件：安装 OpenClaw

```bash
# 1. 安装 OpenClaw CLI（macOS）
brew tap openclaw/tap
brew install openclaw

# 或通过 npm 安装
npm install -g @openclaw/cli

# 2. 初始化配置
openclaw init

# 3. 配置模型 Provider（编辑 ~/.openclaw/openclaw.json）
openclaw config edit
```

> 详细安装文档请参考 [OpenClaw 官方仓库](https://github.com/openclaw/openclaw)

### 安装 Imperial Orchestrator Skill

```bash
# 方式一：从 GitHub 克隆安装
git clone https://github.com/rexnode/imperial-orchestrator.git
cp -r imperial-orchestrator ~/.openclaw/skills/

# 方式二：直接复制到全局 skills 目录
cp -r imperial-orchestrator ~/.openclaw/skills/

# 方式三：工作区级别安装
cp -r imperial-orchestrator <your-workspace>/skills/
```

### 验证安装

```bash
# 发现并探活模型
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/health_check.py \
  --openclaw-config ~/.openclaw/openclaw.json \
  --write-state .imperial_state.json

# 验证路由是否正常
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/router.py \
  --task "写一个 Hello World" \
  --state-file .imperial_state.json
```

## 安全

- 不要在 prompt 中发送密钥
- 探活请求保持最小化
- provider 健康状态与模型质量分开管理
- 模型出现在配置中不等于安全可路由

## License

MIT
