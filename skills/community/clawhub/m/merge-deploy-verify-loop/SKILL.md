---
name: merge-deploy-verify-loop
description: >-
  将"本地改动 → 选择性提交 → push → 合并到目标分支 → CI 构建部署 → 重启工作负载 →
  端到端功能/数据库验证 → 失败则补丁再循环"这一段发布闭环按通用 SOP 跑通的技能。
  当用户的意图包含"提交并推送 / 合并到 develop 或 feature/* / 用 Jenkins/CI 部署到 DEV/STG /
  重启 pod 后自动测试 / 跑通发布闭环 / 改完上一道再走一遍" 等触发语境时使用；
  同样覆盖"测试不过 → 定位 → 仅提交本次修复 → 再次部署验证"的下一轮迭代。
  与具体项目/分支名/MCP 实现解耦，仅在描述步骤时给出常见 MCP（GitLab / Jenkins / Kubernetes / Postgres / Fetch）的推荐用法。
---

# Merge / Deploy / Verify Loop

把"本地已 ready 的改动"安全送到目标环境并完成验证闭环的通用流程。不绑定具体项目、具体分支命名、具体 MCP 实现。

## 何时启动

用户意图涉及以下任一项时按本 SOP 走：

- 把改动**合并到 develop / feature/* 分支**并部署
- 用 **CI（Jenkins 等）** 触发构建，再**重启 pod / 滚动更新**
- 部署完成后**端到端验证**接口 + 数据库
- 验证失败 → **定位 → 仅提交补丁 → 再循环一次**
- "走一遍发布闭环 / 完整链路 / to dev"

## 七步闭环

```
Task Progress:
- [ ] 1. 选择性暂存 - 只 add 本次相关的改动
- [ ] 2. Commit + Push
- [ ] 3. 合并到目标分支（MR）
- [ ] 4. 触发 CI 构建
- [ ] 5. 重启工作负载
- [ ] 6. 端到端验证
- [ ] 7. 若 6 失败 → 仅提交补丁 → 回到 2
```

### 1. 选择性暂存

**铁律**：永远只 `git add <file>` 单文件清单。**禁止** `git add -A` / `git add .` / `git commit -am`。

`git status` 先全量列出变更，对每个文件单独判断"是否属于本次任务"：

| 必须排除 | 理由 |
|---|---|
| 本地调试改动（config 指向 localhost / 自己机器路径） | 推上去会让 CI/同事炸 |
| `.idea/` `.vscode/` `*.exe` `*.log` 等 IDE/构建产物 | 该走 .gitignore |
| 含密钥、token、私钥的文件 | 安全事故 |
| 别人未关联本次任务的 in-flight 改动 | 偷带 |

判定不明时：用 AskQuestion 让用户拍板，**不要替用户决定**。

暂存后用 `git status --short` 复核：`M ` 前空格=已 staged，` M`=未 staged。

### 2. Commit + Push

- commit message 用 HEREDOC，遵循项目历史 commit 风格（先 `git log --oneline -10` 看一下）
- **不**修改 `git config`
- **不** `--amend` 已经 push 过的 commit；**不** `--no-verify`
- `git push origin HEAD`

### 3. 合并到目标分支

**目标分支**优先级：用户明说的 > 项目默认分支 > 询问用户。**不要**猜 `main` / `master`。

有 GitLab/GitHub MCP 时：

1. 创建 MR/PR：source=当前分支，target=目标分支，title 一句话概括"做了啥"
2. 等 `merge_status` 从 `checking` → `can_be_merged`（一般 5-15 秒）
3. 合并；记下 **merge commit SHA**，后面给 CI 对账用
4. 不要自动 remove source branch，除非用户明说

无 MCP 时：把 MR URL 输出给用户，请其完成合并后回告 merge SHA。

### 4. 触发 CI 构建

有 Jenkins MCP 时：

1. 列 jobs / 分页搜索，按 `<env>_<service>` 这类命名规律找到目标 job
2. **`getBuild` 看上一次成功构建的参数集** —— 直接照抄参数名和取值惯例（如 `branch=refs/heads/<target>`），不要自己造参数
3. `triggerBuild`；返回 HTTP 201 才算入队成功
4. 轮询 `getBuild` 直到 `building: false`；校验 `result == "SUCCESS"`
5. 用 `lastBuiltRevision.SHA1` **核对**等于第 3 步的 merge SHA，确认 CI 拉到的就是这次合并的代码

**多 service 并行**：边/云、多微服务都要部署时，所有 `triggerBuild` 在同一消息里并行触发；轮询时也并行查。

**轮询节奏**：先 sleep ~30s，之后参考 `estimatedDuration` 与上次 build `duration` 估时长，指数回退（30s → 60s → 120s → 180s）。

### 5. 重启工作负载

有 Kubernetes MCP 时：

1. 找 namespace、按 label selector 定位 pod
2. **优先**：`pods_delete` 删 pod 让 RS 拉新，**前提**用 `pods_get` 确认 `imagePullPolicy: Always` 且 image tag 不变
3. **次选**：如果 tag immutable 或走 helm/argocd 通道，引导用户用对应通道
4. 等新 pod `READY=N/N` 全就绪、旧 pod `Terminating` 完成

**关键检查**：
- `imagePullPolicy` 必须 `Always`；`IfNotPresent` + 不变 tag = 用本地缓存的旧 image，等于没部署
- 多容器 pod **必须等所有容器 ready** 再进第 6 步，readinessProbe 未过时打过去都不算数

### 6. 端到端验证

**覆盖原则**：每个新增/改动的接口都要被实际打到，每个落库字段都要被 SELECT 确认。

按权限差异分层选工具：

| 通道 | 工具 | 何时用 |
|---|---|---|
| 不要 token 的内部接口 | K8s `pods_exec` + `curl localhost:<port>` | 后端到后端互调（如内部 sync/health/admin） |
| 要 token 的外部接口 | 用户提供 token + Fetch MCP / shell curl | 完整模拟前端用户视角 |
| 数据库断言 | 对应 DB 的 MCP，或 `pods_exec` 进 DB pod 执行 psql/mysql | 任何"已落库"断言 |
| 路由生效验证 | `pods_log` 看启动日志里的路由列表 / "Total: N routes" | 确认新代码已部署 |

**最少覆盖的 4 类场景**：

1. **正向新增** — 创建一条记录，API 响应 + DB SELECT 都断言
2. **幂等 / upsert** — 相同 key 二次调用，验 id 不变、`updated_*` 变、`created_*` 保留
3. **守卫 / 校验失败** — 构造非法输入，期望业务错误码而非 panic
4. **副作用链** — A 操作要触发 B 系统状态变化，从 B 这边再断言一遍（典型：A→B 同步、B→A 反向调用）

**测试数据可清理**：

- 用一眼能认出的前缀（如 `E2E001` / `E2E-<service>-001`），不要用真实业务样子的 key
- 测完调对应 delete 接口或 SQL 把数据复位
- 如果中途清空 / 改写了**共享或生产数据**，**必须先 SELECT 备份原值**，测完用 SQL 恢复

**断言强度**：

- 不能"HTTP 200 就算过" —— `effectCount=0` 也是 200
- 不能只看 service 日志没报错 —— 没记录 ≠ 没问题
- 关键路径要有 DB 端的 evidence

### 7. 失败 → 补丁再循环

测试不过 / 部署失败 / pod 起不来时：

1. 抓证据：`pods_log`（带上下文窗）、`getBuild` 失败 stage、DB 查询、关键事件
2. 把错误**定位到层**：代码层 / 配置层 / 数据层 / 网络层。**不靠猜直接动代码**
3. 定位后**仅提交修复相关的文件**（重走第 1 步规则，严守"只 add 相关文件"）
4. **不要** `--amend` 已 push 的 commit；新建 `fix: <原因简述>` commit
5. 回到第 2 步开始下一轮闭环

## 全程铁律

- **只提交本次任务相关的文件**。一发现 untracked/modified 不属于本次，跳过它
- **每一步等真完成再进下一步**：MR `merged` 才触 CI；CI `SUCCESS` 才动 pod；pod `Ready` 才开测
- **三方 SHA 对账**：commit SHA → merge SHA → CI 拉的 SHA。任何一处对不上立刻停下查
- **共享数据先备份后改**，测完恢复
- **不静默吞错**：哪怕"看上去通了"也要至少一条 SQL/HTTP 响应作证据
- **破坏性操作**（force push、删 prod pod、大范围 DELETE）必须先和用户确认
- 不替用户做模糊决策；模糊处用 AskQuestion

## 输出对账表

每轮闭环结束给一份对账，让用户一眼能复核：

```
| 阶段 | 状态 | 关键凭证 |
|---|---|---|
| Commit | ✅ | <short-sha> |
| Merge | ✅ | MR #X，merge commit <sha> |
| Build A | ✅ | job #N SUCCESS，拉取 SHA = merge SHA ✅ |
| Build B | ✅ | job #M SUCCESS，拉取 SHA = merge SHA ✅ |
| Restart | ✅ | 新 pod Ready N/N，旧 pod 已 Terminating |
| Test 1..K | ✅ K/K | 见下方明细 |
```

后接每个测试场景的 HTTP 状态码、`effectCount`、DB SELECT 结果。

## 反模式

- ❌ `git add .` / `git commit -am` — 容易把 IDE 配置、本地调试、别人改动一起推
- ❌ 触 CI 后立刻去测 — 镜像还没构建完
- ❌ 删 pod 后立刻测 — 容器还没起或 readinessProbe 未过
- ❌ 只看 HTTP 200 不查 DB — `effectCount=0` 也是 200
- ❌ `pods_log` 取最后 20 行做断言 — ERROR 刷屏的服务关键日志会被冲掉，改成按时间窗 / grep 关键词
- ❌ 测完不恢复共享 / 生产数据 — 留给下个同事一个雷
- ❌ Build 失败 / hook 失败就 `--amend` — 历史被改还要 force push；正确做法是新 commit
- ❌ 没拿到 merge SHA 就开始触 CI — 没法核对 CI 是不是拉到本次代码
- ❌ 直接用本地默认分支 `main` / `master` 当目标 — 不同项目流派不同，必须问

## 与其他 SKILL 的边界

- 上游：开发阶段的需求拆解、设计、测试用例编写，参考更顶层的 `cursor-self-bootstrap-workflow`
- 平行：远程日志分析参考 `server-log-analysis`；复杂 bug 多轮排查参考 `complex-bug-debugging-with-ai`
- 本 SKILL 只负责"代码已 ready 之后到生效验证"这段，不掺合代码怎么写