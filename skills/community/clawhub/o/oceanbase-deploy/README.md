# oceanbase-deploy

OceanBase OBD 部署与运维 Skill 集合，供任意 AI Agent 加载使用。

源码位置：[`oceanbase/oceanbase-skills`](https://github.com/oceanbase/oceanbase-skills) 的 `skills/` 目录。

## Skill 列表

| Skill | 功能 |
|-------|------|
| [`oceanbase-deploy`](./) | 总览入口，路由到具体 skill |
| [`cluster-management`](./cluster-management/) | 集群生命周期：部署、启停、升级、扩容、OCP CE 接管、监控 |
| [`tenant-management`](./tenant-management/) | 租户管理：创建、删除、优化、备份恢复 |
| [`seekdb`](./seekdb/) | seekdb：安装、部署、主备复制、switchover/failover/decouple |
| [`testing-and-benchmark`](./testing-and-benchmark/) | 压测：Sysbench、TPC-H、TPC-C；功能测试：mysqltest |

> 更多 skill 持续开发中，计划覆盖：内核调优、SQL 诊断、数据迁移等。

---

## 安装方式

### Claude Code 一键安装（全部 skill）

```bash
mkdir -p .claude/skills/oceanbase-deploy
curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/SKILL.md" \
  -o .claude/skills/oceanbase-deploy/SKILL.md
for s in cluster-management tenant-management seekdb testing-and-benchmark; do
  mkdir -p .claude/skills/oceanbase-deploy/$s
  curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/$s/SKILL.md" \
    -o .claude/skills/oceanbase-deploy/$s/SKILL.md
done
```

### 从 GitHub 加载单个 skill

```
https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/<skill-name>/SKILL.md
```

---

## Agent 集成

### Claude Code

使用上方 [一键安装](#claude-code-一键安装全部-skill) 命令，或手动将 `SKILL.md` 文件放入 `.claude/skills/oceanbase-deploy/` 目录。

### Cursor

```bash
mkdir -p .cursor/skills/oceanbase-deploy
curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/SKILL.md" \
  -o .cursor/skills/oceanbase-deploy/SKILL.md
for s in cluster-management tenant-management seekdb testing-and-benchmark; do
  mkdir -p .cursor/skills/oceanbase-deploy/$s
  curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/$s/SKILL.md" \
    -o .cursor/skills/oceanbase-deploy/$s/SKILL.md
done
```

### Windsurf

在 Windsurf 的 Rules 或项目上下文配置中，添加 SKILL.md 文件路径或粘贴其内容。

### 其他 Agent

- **系统提示词 / 规则文件**：粘贴 `SKILL.md` 内容。
- **URL 加载**：使用上方 GitHub raw 链接。
- **会话上下文**：在会话开始时粘贴 `SKILL.md` 内容。

---

## 常用提示词

### 集群管理

```text
部署一个本机 OceanBase 开源版本，能快速跑起来就行
```

```text
用 config.yaml 部署一个名为 test-cluster 的 OceanBase 社区版集群
```

```text
帮我部署 OCP
```

```text
帮我直接启动 test-cluster，并检查启动后状态
```

```text
如何给 ob-test 添加 Prometheus 和 Grafana 监控
```

### 租户管理

```text
在 test-cluster 上创建一个名为 mysql 的租户
```

```text
给 test-cluster 上的 mysql 租户配置备份路径并执行一次备份
```

### seekdb

```text
部署并启动一个 seekdb 实例
```

```text
创建一个 seekdb 主备集群，并告诉我主库和备库分别怎么部署
```

```text
查看 seekdb-test 的拓扑，如果主库挂了该用 switchover 还是 failover
```

### 压测

```text
对 test-cluster 的 mysql 租户跑一个 sysbench 测试
```

```text
给我跑 TPC-H 的完整命令和参数
```

---

## 提问建议

- 想让 Agent 直接执行 → 说 **"帮我执行"**
- 想先看方案 → 说 **"先不要执行，只给我命令和步骤"**
- 涉及销毁、重建、故障切换 → 说 **"我确认允许高风险操作"** 或 **"先不要执行破坏性命令"**

---

## License

[MIT](../../LICENSE)
