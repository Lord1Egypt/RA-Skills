# 跨机基因工作手册（0.26）

> **EN**: Practical handbook for multi-machine gene work: named pools, pull/push/contribute workflow, review semantics, conflict resolution, and troubleshooting. Command-level, copy-paste ready.

**适用场景**：一台机器沉淀经验，多台机器共享；或团队共用一个基因池。

## 1. 五分钟上手（单机 → 跨机）

```bash
# ① 本机首次：装起步包 + 自检
node code/light-cli.mjs doctor && node code/light-cli.mjs starter

# ② 定义命名池（官方镜像；团队池同理填自己的 git URL）
mkdir -p ~/.evomap && cat > ~/.evomap/pools.json <<'EOF'
{"pools": {"official": "https://zyx.pink/pool/genes.jsonl",
           "team":    "https://github.com/<org>/<team-pool>.git"}}
EOF

# ③ 按名拉取（拉过的池缓存在 ~/.evomap/pool-cache/，后续 pull 增量更新）
node code/gene_share.mjs pull official --tier official
node code/gene_share.mjs pull team --tier community   # 团队池默认隔离待审

# ④ 只想拉某个场景的子集
node code/gene_share.mjs pull official --scene ops-deploy
```

## 2. 每日闭环（T1-T5 不变）

| 节点 | 命令 | 跨机注意 |
|---|---|---|
| T1 任务开始 | `evolver-recall.mjs --query "<任务>"` | 召回读本机库；库内容取决于你 pull 过哪些池 |
| T3 报错 | `evolver-recall.mjs --error "<报错>"` | 同上 |
| T4 修好后 | `light-cli.mjs draft --error ... --strategy ... --commit` | 落库即写 deposit 事件（本机 timeline），**不会自动共享** |
| T4 审核 | `light-cli.mjs approve <gene_id>` | 本机审核台账；多机各自审核，互不影响 |
| T5 结束 | `evolver-recall.mjs --register-hit --gene <id> --note "..."` | 按 gene_id 寻址，多机各写各的账本 |

## 3. 贡献回官方池（人工流程，不自动外发）

```bash
# ① 标记可共享（通用教训 + 含 AVOID/FIX + 无私有内容）
node code/light-cli.mjs shareable <gene_id>

# ② 产出提交包（单文件，带你的 keyid 署名头）
node code/light-cli.mjs gene submit --bundle my-submission.jsonl

# ③ 发送（PR / issue 附件 / 文件交换三选一）
#    维护者侧：gene import <bundle> --tier community → 默认隔离 → evidence 逐条取证 → approve → 入池
```

**doctor 的推送就绪提示**：已审核可共享但尚未入池 ≥3 条时会提醒（只提示，不自动发送）。

## 4. 冲突与并发语义（三层）

| 场景 | 语义 | 依据 |
|---|---|---|
| 单机多会话并发写 | `withLock` 文件锁（O_EXCL + 15s stale 破除） | store.mjs |
| 同机多进程 | 同上；appendGene 幂等（asset_id 去重） | genes.jsonl 行级 |
| 跨机共享 | **Git 化**：各机独立提交 → 维护者审核合并；台账 last-write-wins | review.jsonl |
| 审核冲突 | LWW：每个 assetId 取**最后一条状态**——quarantine 可撤销 approve | review.jsonl |
| 多宿主并行召回 | 按 gene_id 寻址（0.18 起），不用位置序号 | register-hit --gene |

## 5. 团队池建议结构

```
<team-pool>.git/
└── genes.jsonl        # 仅 shareable AND approved 的基因（maintainer 导出）
    CONTRIBUTING.md    # 贡献条款（提交即授权 CC-BY-4.0）
    LICENSE
```

- **同步**：各机 `gene pull team`（git URL 走 clone/pull 缓存，timeout 30s + 有界重试）；
- **审门**：团队池默认按 community 导入（隔离待审），维护者 approve 后生效；
- **归属**：每条基因保留贡献者 keyid（Ed25519 签名），冲突/审计可追溯。

## 6. 排障速查

| 症状 | 原因 | 处理 |
|---|---|---|
| `gene pull official` 报池源不存在 | pools.json 未建/名字拼错 | 检查 `~/.evomap/pools.json`，名字区分大小写 |
| 拉取后 recall 仍无对靶 | 场景不匹配或库为空 | `light-cli list --scene <名>` 看本机有什么 |
| submit 提示 0 条 | 基因未 shareable 或未 approve | `light-cli list` 查 state |
| verify 找不到公钥 | 包内无 issuer-pub.txt（许可功能） | 非核心功能，可忽略；或从发行方获取 |
| git 拉取失败 | 网络/权限 | 手动 `git clone` 到 `~/.evomap/pool-cache/` 后用本地路径 `gene pull <path>` |

## 7. 安全边界（不可协商）
- 沉淀审核语义统一见 SKILL.md「审核状态机」；**审核永远不绕过**；**EN**: review semantics live in the SKILL.md review-state-machine section; approval is never bypassed.
- 导入验签：篡改基因 BLOCKED；无签名标 unsigned（不拒收但标注）；
- 私有内容（内部主机名/凭据/绝对路径）**零容忍**：提交前自查，池维护方红线扫描拦回。
## 8. 多宿主兼容性矩阵（0.26）

| 宿主 | 接入方式 | 命令 | 生效动作 | 边界/注意 |
|---|---|---|---|---|
| Claude Code | 规程文件 | `install claude-code`（写 `~/.claude/CLAUDE.md`） | 新会话自动见 T1-T5 | 需 `--yes` 落盘；已有文件原位更新（幂等） |
| Cursor | 规则文件 | `install cursor`（写 `.cursor/rules/pievox.md`） | 规则自动加载 | 项目级规则，跨项目需各自写入 |
| Codex | 规程文件 | `install codex`（写 `~/.codex/AGENTS.md`） | 新会话自动见 | 同 Claude Code |
| 通用 AGENTS.md 宿主 | 规程文件 | `install agents-md`（写项目 `AGENTS.md`） | 该项目每会话可见 | 项目级；不跨项目 |
| Windsurf | 规则文件 | `install windsurf`（写 `.windsurf/rules/pievox.md`） | 规则自动加载 | 同 Cursor |
| OpenClaw | **钩子** | `install-hooks --yes` | 消息进站自动召回（agent:bootstrap） | **改 handler 须重启网关**；备份 unit |
| Hermes | **钩子** | `install-hooks --yes` | LLM 调用前召回（pre_llm_call，is_first_turn 闸） | 只改脚本无需重启；须刷新 allowlist（mtime 用 ISO-8601 字符串） |
| 任意宿主（手工） | 粘贴规程 | `light-cli snippet` 打印规程 → 粘进任意指令文件 | 取决于宿主 | 最弱但最通用 |

**边界说明**：钩子类宿主能力最强（自动触发）；规程类需宿主加载指令文件；纯文件粘贴最弱。三者共用同一召回实现，行为一致。
