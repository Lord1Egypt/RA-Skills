---
name: kes-deploy
description: KingbaseES ISO 安装部署 — 测试用例
---

# KingbaseES ISO 安装部署测试用例

## 测试用例 1: Linux 静默安装

**场景**：运维人员需要在生产服务器自动化部署 KingbaseES

**输入问题**："Linux 服务器怎么静默安装金仓数据库？"

**期望答案要点**：
- 命令：`./setup.sh -i silent -f silent.cfg`
- silent.cfg 关键参数：INSTALL_PATH、COMPONENTS、DB_USER、DB_PASS
- 组件列表：Server, Interface, KStudio, KDTS 等
- 安装前需创建 kingbase 用户和目录

**验证方法**：答案包含静默安装命令格式和 silent.cfg 配置示例

---

## 测试用例 2: Linux 系统参数调整

**场景**：安装前准备 Linux 环境，需要调整系统参数

**输入问题**："安装金仓数据库前，Linux 系统需要调整哪些参数？"

**期望答案要点**：
- 内核参数：kernel.shmmax、kernel.shmall、net.core.rmem_default 等
- 资源限制：nofile/nproc 设置为 102400
- RemoveIPC=no 设置
- 应用命令：`sysctl -p`

**验证方法**：答案列出 shmmax/shmall 资源限制等关键参数

---

## 测试用例 3: ksql 连接测试

**场景**：安装完成后需要验证数据库是否正常

**输入问题**："金仓数据库安装完了，怎么用命令行测试连接？"

**期望答案要点**：
- 设置环境变量：`export KINGBASE_HOME=/opt/Kingbase/ES/V9`
- 版本检查：`kingbase -V`
- 连接测试：`ksql -U SYSTEM -d test`
- 查询验证：`select version();`

**验证方法**：答案包含 ksql 连接命令和 version 查询

## 测试用例 4: kingbase.conf 关键配置

**场景**：生产环境需要优化数据库配置

**输入问题**："kingbase.conf 怎么配置？给个生产环境的示例"

**期望答案要点**：
- listen_addresses = '*'
- port = 54321
- shared_buffers 建议物理内存 1/3
- effective_cache_size 建议物理内存 3/4
- WAL 配置：wal_level、archive_mode
- 日志配置：logging_collector、log_statement

**验证方法**：答案包含 shared_buffers/effective_cache_size 内存配置建议
