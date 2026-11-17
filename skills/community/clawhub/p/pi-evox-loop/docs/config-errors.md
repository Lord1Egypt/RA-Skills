# 常见配置错误与排查（Config Errors）

> **EN**: Common configuration errors and fixes. Self-check first: `doctor` (Node version / store dir writable / instrumentation dir reachable / stray-instrumentation detection) and `info` (loop health: recall count / hits / pending / quarantined).


## Node 版本

| 症状 | 原因 | 处置 |
|---|---|---|
| `SyntaxError: Invalid or unexpected token` / 命令无输出 | Node < 22（锁用了 `Atomics.wait` 等较新 API） | `node -v` 检查；升级到 ≥22（`nvm install 22` 或官网） |
| `pi_evolve` 启动即失败 | Pi CLI 要求更高 Node | 同上 |

## 环境变量

| 变量 | 常见错误 | 症状 | 正确用法 |
|---|---|---|---|
| `EVOX_HITS_DIR` | 未设（默认 `$cwd/experiments`） | **埋点散落**：timeline/info/harvest 读不到别的项目目录的账本；`doctor` 会提示"埋点散落" | 生产固定 `EVOX_HITS_DIR=$EVOX_ROOT/experiments` |
| `EVOX_STORE_DIR` | 指向只读目录 / 打错路径 | 沉淀报 EACCES/ENOENT | 指向可写目录（默认 `$HOME/.evomap/assets`） |
| `EVOX_NODE` | 相对路径 | 钩子宿主 PATH 不同解析失败 | 绝对路径 |
| `EVO_POOL_DIR` | 与 stage 目录混用 | 池文件被 stage 覆盖 | 池用独立目录（建议自有 Git 仓） |

## 双引擎混淆

| 症状 | 原因 | 处置 |
|---|---|---|
| 装了 evolver 但行为像旧版 | `--engine auto` 检测到即用 | 明确 `--engine light`（默认）或 `--engine evolver` |
| `evolver: command not found` | 用了 `--engine evolver` 但未 `npm install` | 安装，或切回默认 light 后端 |
| GPL 顾虑 | `@evomap/evolver` 是 GPL-3.0-or-later | 仅可选集成涉及；默认 light 后端为 MIT、零依赖 |

## Provider（流程 C）

| 症状 | 原因 | 处置 |
|---|---|---|
| `$ENV` 插值不生效 | pi < 0.85.1 不支持 `$ENV` | 升级 pi，或 `--api-key "$MY_KEY"` 显式传 |
| `--llm-refine` 无反应 | 未配 `EVOLVER_REFINE_URL/MODEL`（未配置时自动禁用——防数据外发） | 显式配置端点+模型 |
| 国内端点超时 | 端点选择/网络 | 换 DeepSeek/百炼/硅基流动/智谱（见 `providers.md`） |

## 并发与共享

| 症状 | 原因 | 处置 |
|---|---|---|
| approve 显示"此前已通过"但状态没变 | 0.19.0 前的 `.some()` 幂等 bug（已修） | 升级 ≥0.19.0 |
| 埋点/台账偶发丢失 | 多会话并发写（0.19.0 前无锁） | 升级 ≥0.19.0（O_EXCL 锁） |
| `.evox.lock` 残留 | 持锁进程被 kill -9 | 15s 后自动 stale 破除，无需手工处理 |

## 自检

```bash
node code/light-cli.mjs doctor    # Node 版本 / 库目录可写 / 埋点目录可达 / 埋点散落检测
node code/light-cli.mjs info      # 闭环健康度：召回次数 / 命中 / 待审 / 隔离
```
