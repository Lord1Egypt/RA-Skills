---
name: github-acr-release
description: "全周期项目发布管控：覆盖版本创建→开发→预发布→发布→验证→运维→下版本规划的13步标准流程。交互式配置、版本一致性检测、可持续性评分、热更新。适用于任何语言、任何 Docker 部署项目。触发词：新建发布流程、发布、检查、热更新、下个版本。"
---

# GitHub + ACR 全周期发布管控

> 适用于任何语言（Python / Go / Rust / Node…）的 Docker 化项目。
> 从"新建项目配置"到"发布后验证+下版本规划"，一条流水线管到底。

## 快速开始

| 你说 | Skill 执行 |
|------|-----------|
| `新建发布流程` / `搭建发布流` | 交互式问询 → 生成项目配置 → 初始化骨架 |
| `检查` / `检查发布` | 仅流前检查（版本一致性+代码基线+可持续性评分） |
| `发布` / `发版` / `push` | 完整发布（流前检查→确认→构建→推送→部署→验证→收尾） |
| `热更新` / `hotfix` | 快速修复发布（跳过版本号+CHANGELOG） |
| `下个版本` / `下版本` | 进入版本规划对话 |

---

## 一、核心概念

### 项目结构约定

```
{project-name}-v{X.Y.Z}/
├── {source}/                     ← 源码目录（可配置名）
├── data/
│   └── VERSIONS.json             ← 版本元数据（基石文件）
├── Dockerfile                    ← 可配置路径
├── docker-compose.yml            ← 可配置路径
├── VERSION                       ← 可选
├── .github/workflows/ci.yml      ← 可选（skill 可生成模板）
├── scripts/                      ← 工具脚本（skill 可生成）
│   ├── check_version_consistency.py
│   ├── smoke_test.py
│   ├── post_deploy_verify.py
│   └── full_release_check.py
└── ...（其他项目文件）
```

### VERSIONS.json 标准结构

```json
{
  "current": {
    "version": "X.Y.Z",
    "date": "YYYY-MM-DD",
    "notes": "描述",
    "data_version": 1,
    "digest": ""
  },
  "changelog": [
    {
      "version": "X.Y.Z",
      "date": "YYYY-MM-DD",
      "notes": "描述",
      "detail": {
        "sections": [
          { "type": "Added / 新增", "items": ["功能A", "功能B"] },
          { "type": "Fixed / 修复", "items": [] }
        ]
      }
    }
  ]
}
```

### 版本管理规则（红线）

1. 新建版本分支 → `cp -r {project}-v{old} {project}-v{new}`
2. **必须**完整复制 `data/` 目录（含 VERSIONS.json）
3. **只改** `current.version` 和 `current.date`
4. **changelog 历史绝不动**
5. 同版本多条 changelog → 合并为一条，日期取较早的，sections 按 type 去重
6. 新版本条目先空着（detail.sections 为空），等实际更新再填

---

## 二、交互式项目配置

当用户说"新建发布流程"时，进入以下问答流程：

### 第1轮：基本信息

| 字段 | 必填 | 示例 |
|------|------|------|
| 项目名（英文小写） | ✅ | `my-app` |
| 一句话描述 | ✅ | `XX应用` |
| GitHub 仓库 URL | ✅ | `github.com/user/my-app` |

### 第2轮：版本管理

| 字段 | 必填 | 示例 |
|------|------|------|
| 当前版本目录（完整路径） | ✅ | `/home/.../my-app-v1.0.0` |
| 版本文件路径（相对项目根） | ✅ | `backend/__version__.py` |
| 版本号提取模板 | ✅ | `__version__ = "{version}"` → 提取 `"1.0.0"` |
| 版本格式 | ✅ | `semantic`（X.Y.Z） |
| 是否有 VERSIONS.json | ✅ | `yes` / `no` |

### 第3轮：构建与容器化

| 字段 | 必填 | 示例 |
|------|------|------|
| 编程语言 | ✅ | `python / go / rust / node / java` |
| 是否有前端 | ✅ | `yes` / `no` |
| 前端编译命令 | 条件 | `cd frontend && node compile.js` |
| Dockerfile 路径 | ✅ | `Dockerfile` |
| docker-compose 路径 | ✅ | `docker-compose.yml` |
| 服务端口 | ✅ | `8765` |
| 前端编译后产物路径 | 条件 | `frontend/assets/` |

### 第4轮：ACR 与部署模式

| 字段 | 必填 | 示例 |
|------|------|------|
| ACR 仓库地址 | ✅ | `registry.cn-hangzhou.aliyuncs.com` |
| ACR 命名空间 | ✅ | `my-team` |
| ACR 镜像名 | ✅ | `my-app` |
| 部署模式 | ✅ | `local` / `remote` |
| 服务器地址 | 条件（`remote` 时需要） | `10.0.1.138` |
| 服务器部署路径 | 条件（`remote` 时需要） | `~/docker/my-app/` |
| 验证 URL | 条件（`remote` 时需要） | `http://10.0.1.138:8765/api/versions` |

**说明**:
- `local`：纯本地 Docker (docker-compose)，无远程服务器，跳过后端部署与远端验证
- `remote`：传统远程服务器模型，需 SSH 权限和部署路径

### 第5轮：可持续性（可选但建议）

| 字段 | 默认值 | 说明 |
|------|--------|------|
| 是否有数据迁移框架 | `no` | data_manager.py + migrations/ |
| 是否有配置备份/回滚 | `no` | 配置保存时自动备份 |
| 是否有启动健康检查 | `no` | 容器启动时自检 |
| 是否有版本一致性脚本 | `no` | scripts/check_version_consistency.py |
| 是否有冒烟测试脚本 | `no` | scripts/smoke_test.py |
| 是否有发布后验证脚本 | `no` | scripts/post_deploy_verify.py |

### 第6轮：汇总确认

展示完整配置摘要，用户确认后写入：

```
projects/{name}.json          ← 项目配置
scripts/                      ← 生成脚本模板（可选）
```

---

## 三、可持续性评分

每次发布前检查时，skill 对照配置中的可持续性字段，生成评分报告。

### 检查项总表

| 类别 | 检查项 | 级别 | 不带的影响 |
|------|--------|------|-----------|
| 🏗 骨架 | `scripts/` 目录 | ⚠️ 建议 | 无自动化检查框架 |
| | `.github/workflows/ci.yml` | ⚠️ 建议 | GitHub Actions 无法自动构建 |
| | `Dockerfile` | ❌ 必须 | 无法容器化部署 |
| | `docker-compose.yml` | ⚠️ 建议 | 本地开发测试不便 |
| | `.gitignore` | ⚠️ 建议 | 可能误传敏感文件 |
| 📦 版本 | `VERSIONS.json` | ❌ 必须 | 无版本追踪，无法做迁移 |
| | 版本号一致性 | ❌ 必须 | 发布版本号错乱 |
| | 版本文件 | ❌ 必须 | 无法从代码读版本号 |
| 🔒 数据 | 配置备份/回滚 | ⚠️ 建议 | 配置损坏无法恢复 |
| | 数据迁移脚本 | ⚠️ 建议 | 跨版本升级旧数据不可用 |
| | 数据版本号 | ⚠️ 建议 | 无法判断是否需迁移 |
| 🛡 运维 | 启动健康检查 | ⚠️ 建议 | 异常无声 |
| | 版本一致性脚本 | ⚠️ 建议 | 发版前无法自动检测 |
| | 冒烟测试脚本 | ⚠️ 建议 | 发布后无法自动验证 |
| | 发布后验证脚本 | ⚠️ 建议 | 远程部署无法确认 |
| 🧪 测试 | 模块冒烟测试 | ⭐ 可选 | 核心逻辑变更无快速验证 |
| | 单元测试框架 | ⭐ 可选 | 严重回退风险 |

### 评分对话示例

```
Skill: 📊 可持续性评分：12/18

  ✅ 已具备：Dockerfile、VERSIONS.json、版本文件、...
  ⚠️ 建议补充：
    - scripts/ 目录（检查脚本框架）→ 发版前无法自动检测问题
    - 配置备份机制 → 配置损坏后无法自动恢复
  ❌ 应修复：无

  要补充缺失功能吗？
  - 是 → 我帮你生成脚本模板
  - 跳过 → 发布后可继续，但建议尽快补
```

---

## 四、全周期 13 步发布流程

### 阶段 A：发布流前（Pre-release）

| 步骤 | 操作 | 自动化 |
|------|------|--------|
| **Step 0** | 版本分支创建：`cp -r {项目}-v{旧} {项目}-v{新}` | 手动 |
| | 完整复制 data/（含 VERSIONS.json） | 检查脚本校验 |
| | 只改 current.version + current.date，changelog 历史不动 | |
| | 新版本 changelog 条目先空着 | |
| **Step 1** | 版本号原点同步检查 | `check_version_consistency.py` |
| | 扫描：版本文件 / VERSIONS.json / Dockerfile / docker-compose / VERSION | |
| | 不一致 → 中止；`--fix` 可自动修正 | |
| **Step 2** | 代码基线检查（按语言） | |
| | Python: `python -m py_compile` | |
| | Go: `go vet ./...` | |
| | Rust: `cargo check` | |
| | Node: `node -c` | |
| | Java: `javac` / `mvn compile` | |
| **Step 3** | 可持续性评分 | 对照配置清单 |
| | 展示缺失项 + 不带的影响 | |
| | **询问用户**：补充 or 跳过 | |
| **Step 4** | 预发布确认 | |
| | 展示：版本号 + 检查结果 + 评分 | |
| | 用户确认 → 进入发布 | |

### 阶段 B：发布流（Release）

| 步骤 | 操作 |
|------|------|
| **Step 5** | 更新 VERSIONS.json：追加 changelog 条目 |
| **Step 6** | 编译前端（若有） |
| **Step 7** | `git add -A` → `git commit` → `git push` |
| **Step 8** | `git tag -a v{版本}` → `git push --tags` → GitHub Actions 自动构建 |
| **Step 9** | **（仅 remote 模式）** 远程服务器部署：SSH → `docker compose pull && up -d`
 |
**说明**: 部署模式在交互配置第4轮设定。`local` 模式自动跳过 Step 9（无远程服务器）。

### 阶段 C：发布流后（Post-release）

| 步骤 | 操作 | 自动化 | 适用 |
|------|------|--------|------|
| **Step 10** | 远端验证：容器状态 + API + 版本一致性 + digest | `post_deploy_verify.py` | **仅 remote** |
| **Step 11** | 镜像 digest 同步：获取 ACR digest → 写入 VERSIONS.json | | 可选（local 也支持） |
| **Step 12** | 环境清理：旧镜像 + 构建缓存 | | 通用 |
| **Step 13** | 收尾 + 下版本规划 | **交互** | 通用 |

> 部署模式 `local` 时，Step 10 自动跳过，无远端验证环节。
| | 更新项目记忆文件 | |
| | **询问用户**：是否创建下一版本？版本号？ | |
| | 是 → 进入 Step 0 | |

---

## 五、脚本模板

项目配置完成后，skill 可在 `scripts/` 目录生成以下脚本（模板变量从配置中替换）：

### 5.1 check_version_consistency.py

扫描所有版本号源是否一致。支持 `--verbose` 和 `--fix`。

从配置读取：`version.file`、`version.pattern`、`versions_json`、`docker.dockerfile`、`docker.compose_file`。

### 5.2 smoke_test.py

API 冒烟测试。需要服务运行。

从配置读取：`docker.port`、验证 URL 路径。

### 5.3 post_deploy_verify.py

远程部署验证：容器状态 + API 可达 + 版本一致 + digest。

从配置读取：`server.host`、`server.verify_url`、项目名（作为容器名）。

> ⚠️ **部署模式为 `local` 时此脚本不生成，Step 10 自动跳过。**

### 5.4 full_release_check.py

一键综合检查入口：版本一致性 → 代码基线 → 可持续性 → Git 状态。

---

## 六、热更新（Hotfix）

与标准发布的区别：
- **跳过**版本号一致性检查（不改版本号）
- 版本号加 `-hotfix.N` 后缀
- **跳过** CHANGELOG 更新
- **不创建** GitHub Release
- 仅：语法检查 → 确认 → 编译 → 构建 → 推送 → 部署 → 验证

热更新步骤：

```
1. 快速语法检查
2. 确认 hotfix 版本号
3. 编译前端（若有）
4. git commit + push
5. workflow_dispatch 触发构建
6. ACR 推送
7. （仅 remote）远程更新
8. （仅 remote）验证
```

---

## 七、触发表

| 用户说 | 触发动作 |
|--------|----------|
| `新建发布流程` / `搭建发布流` | 交互式问询 → 生成配置 → 初始化骨架 |
| `检查` / `检查发布` | 仅流前检查（不发布） |
| `发布` / `发版` / `push` | 标准完整发布 |
| `热更新` / `hotfix` | 快速修复发布 |
| `下个版本` / `下版本` | 版本规划对话 |
| `检查项目` | 可持续性评分 + 缺失项报告 |

---

## 八、与 GitHub Actions 的关系

```
Skill 本地操作                          GitHub Actions
┌──────────────────────┐              ┌──────────────────┐
│ 1. 版本一致性检查       │              │                  │
│ 2. 可持续性评分         │              │ tag 推送触发 →   │
│ 3. 用户确认             │── 推代码 ──▶│ Build → Push ACR │
│ 4. 编译前端             │              │                  │
│ 5. git commit/tag/push │              │                  │
└──────────────────────┘              └──────────────────┘
```

GitHub Actions 只做"构建+推送"。版本控制、CHANGELOG、发布检查全部由 skill 在本地完成。

---

## 九、版本规划对话

发布完成后，skill 自动触发收尾对话：

```
Skill: ✅ 发布完成！vX.Y.Z 已部署上线。

  要开始下一版本的开发吗？

  预设版本号：
    - X.Y.{Z+1}（补丁）
    - X.{Y+1}.0（小版本）
    - {X+1}.0.0（大版本）

  若创建，我会：
  1. 复制当前版本文件夹
  2. 更新 VERSIONS.json 的 current 段
  3. 清空新版本 changelog 条目
  4. 同步版本号

  或者暂不创建，需要时再说"新建版本"。
```

---

## 十、注意事项

1. **敏感信息脱敏**：日志/输出/推送中的密钥必须脱敏
2. **版本号一致性**：5+ 个版本号源必须一致
3. **数据迁移安全**：配置迁移走备份→合并→验证→回滚
4. **不自动执行**：所有对外操作（push/tag/ssh/服务器更新）必须经用户确认
5. **changelog 管理**：同版本多条合并，sections 按 type 去重
6. **Docker 构建策略**：多阶段构建，自动压缩镜像
7. **部署模式感知**：`local` 模式下自动跳过远程部署/远端验证步骤，不要强制执行 SSH 命令

## 十一、常用命令

| 操作 | 命令 |
|------|------|
| 流前全检 | `python3 scripts/full_release_check.py` |
| 版本一致性检查 | `python3 scripts/check_version_consistency.py` |
| 版本一致性检查+修正 | `python3 scripts/check_version_consistency.py --fix` |
| API 冒烟测试 | `python3 scripts/smoke_test.py --base-url http://localhost:PORT` |
| 发布后验证 | `python3 scripts/post_deploy_verify.py --target HOST --ssh` |
| 前端编译 | `cd frontend && node compile.js` |
| 本地构建测试 | `docker build -t {name}:dev .` |
| 远程服务器更新 | `ssh root@HOST "cd PATH && docker compose pull && up -d"` |
