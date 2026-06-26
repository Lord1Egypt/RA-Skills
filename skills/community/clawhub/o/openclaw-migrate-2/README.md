# agent-migrate

OpenClaw Agent 跨平台迁移工具

## 功能

- 导出 Agent 完整状态
- 同步到 GitHub 私有仓库
- 跨服务器迁移部署
- Docker 容器化支持

## 安装

```bash
# 克隆到本地 skills 目录
cd ~/.openclaw/skills
git clone https://github.com/YOUR_USERNAME/agent-migrate.git

# 或使用 .skill 文件
openclaw skills install agent-migrate.skill
```

## 使用

### 导出 Agent

```bash
./scripts/export-agent.sh [名称]
```

### 同步到 GitHub

```bash
./scripts/sync-github.sh git@github.com:username/repo.git --push
```

### 从 GitHub 恢复

```bash
./scripts/sync-github.sh git@github.com:username/repo.git --pull
```

## 许可证

MIT
