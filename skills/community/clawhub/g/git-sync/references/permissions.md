# 基于 skill-standardization 渐进式披露规范的权限说明

本文档由 `skill-standardization` 权限扫描器自动维护。

## 风险等级

**CRITICAL**（实际权重: 0.9）

## 权限总览

| 权限类别 | 涉及项数 | 风险等级 |
|-----------|----------|----------|
| `subprocess_call` | 15 项 | 🔴 HIGH |
| `file_delete` | 19 项 | 🔴 HIGH |
| `network_access` | 2 项 | 🔴 HIGH |
| `sensitive_access` | 9 项 | 🔴 HIGH |
| `critical_write` | 0 项 | ✅ LOW |

## 高权限操作说明

- **子进程调用（subprocess）**（15 项，unified）

- **文件删除**（19 项，unified）

- **网络访问**（2 项，silent）

- **敏感信息访问**（9 项，unified）


## 权限详细说明

### 子进程调用（subprocess）（15 项）

> **功能说明**：技能需要通过 subprocess/操作系统调用来执行外部命令或脚本。
> **授权方式**：unified

| 文件 | 行号 | 匹配内容 | 功能说明 |
|------|------|----------|----------|
| `scripts\git-sync.py` | 11 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 96 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 98 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 108 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 109 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 117 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 120 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 122 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 123 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 834 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\permission_checker.py` | 86 | `SUBPROCESS` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\permission_checker.py` | 98 | `Subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\permission_checker.py` | 259 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\permission_checker.py` | 608 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\permission_checker.py` | 616 | `SUBPROCESS` | 自动化技能：一次性授权，后续自动执行不再询问 |


### 文件删除（19 项）

> **功能说明**：技能在执行过程中需要删除临时文件或清理旧版产物。
> **授权方式**：unified

| 文件 | 行号 | 匹配内容 | 功能说明 |
|------|------|----------|----------|
| `scripts\clean_zip_source.py` | 62 | `os.remove` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\clean_zip_source.py` | 78 | `shutil.rmtree` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 340 | `shutil.rmtree` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 362 | `shutil.rmtree` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 727 | `shutil.rmtree` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 807 | `shutil.rmtree` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 147 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 212 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 231 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 250 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 253 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 339 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 356 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 370 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 379 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 382 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.sh` | 395 | `rm` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\manifest.py` | 78 | `os.unlink` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\sync_with_exclude.py` | 117 | `shutil.rmtree` | 自动化技能：一次性授权，后续自动执行不再询问 |


### 网络访问（2 项）

> **功能说明**：技能需要通过网络连接到外部服务或远程仓库。
> **授权方式**：silent

| 文件 | 行号 | 匹配内容 | 功能说明 |
|------|------|----------|----------|
| `scripts\git-sync.py` | 479 | `urllib` | 自动化技能：中风险静默执行，仅记录 |
| `scripts\git-sync.py` | 543 | `urllib` | 自动化技能：中风险静默执行，仅记录 |


### 敏感信息访问（9 项）

> **功能说明**：技能代码中检测到敏感关键词（token/password 等）。
> **授权方式**：unified

| 文件 | 行号 | 匹配内容 | 功能说明 |
|------|------|----------|----------|
| `scripts\git-sync.py` | 82 | `credential.helper` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 112 | `credential.helper=` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 113 | `credential.https://gitee.com.provider=` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 114 | `credential.https://github.com.provider=` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 513 | ` 用户名或密码/Token 错误` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 562 | ` 的凭证（remote URL 未内嵌 token，~/.git-credent` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 840 | `credential.helper` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\git-sync.py` | 845 | `credential.helper` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\permission_checker.py` | 449 | `credential` | 自动化技能：一次性授权，后续自动执行不再询问 |


### 关键位置写入

**无**。


## 授权方式说明

- **immediate（即时授权）**：每次执行前需获得用户批准
- **unified（统一授权）**：首次执行前获得用户批准，后续不再询问
- **silent（静默授权）**：无需用户交互，自动执行并记录

<!-- fp:risk=CRITICAL|sensitive=9|critical_write=0|network=2|delete=19|subprocess=15|issues=45 -->

## 基于 skill-function-test 的测试报告

| 运行时间 | S1 场景链路 | D1-D6 功能测试 | S4 执行忠实度 | 耗时(s) |
|---------|-------------|----------------|--------------|---------|
| 2026-06-16 07:15 | 3/3 通过 | - | 24/24 (100%) | 323.459 |
