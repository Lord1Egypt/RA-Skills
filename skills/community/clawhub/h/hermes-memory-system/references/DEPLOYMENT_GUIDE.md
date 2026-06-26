# Hermes 系统生产部署指南

## 🚀 部署概述

本指南说明如何将 Hermes 系统部署到生产环境，与 OpenClaw 集成，提供 Skill 自动生成和持久化记忆功能。

### 部署目标
1. **无缝集成** - 与现有 OpenClaw 体系100%兼容
2. **零停机** - 部署过程不影响现有功能
3. **可回滚** - 提供完整的回滚机制
4. **监控就绪** - 部署后立即具备监控能力

### 系统要求
- **OpenClaw**: 2026.4.15+
- **Python**: 3.9+
- **内存**: 4+ GB
- **存储**: 1+ GB 可用空间
- **操作系统**: macOS / Linux / Windows (WSL)

## 📁 部署结构

### 目录结构
```
hermes-system/
├── bin/                    # 可执行脚本
│   ├── hermes-init        # 初始化脚本
│   ├── hermes-start       # 启动脚本
│   ├── hermes-stop        # 停止脚本
│   └── hermes-status      # 状态检查脚本
├── config/                # 配置文件
│   ├── hermes.yaml        # 主配置文件
│   ├── logging.yaml       # 日志配置
│   └── profiles/          # 环境配置
│       ├── development.yaml
│       ├── staging.yaml
│       └── production.yaml
├── src/                   # 源代码
│   ├── compatibility/     # 兼容性层
│   ├── memory/           # 记忆系统
│   ├── skill_generator/  # Skill生成系统
│   ├── data_exporter/    # 数据导出器
│   └── performance/      # 性能基准
├── docs/                  # 文档
│   ├── INSTALL.md        # 安装指南
│   ├── CONFIGURATION.md  # 配置说明
│   └── TROUBLESHOOTING.md # 故障排除
├── tests/                 # 测试文件
│   ├── unit/             # 单元测试
│   ├── integration/      # 集成测试
│   └── performance/      # 性能测试
├── scripts/              # 部署脚本
│   ├── deploy.sh         # 部署脚本
│   ├── backup.sh         # 备份脚本
│   └── rollback.sh       # 回滚脚本
└── var/                  # 运行时数据
    ├── logs/             # 日志文件
    ├── data/             # 数据文件
    └── cache/            # 缓存文件
```

## 🔧 部署前准备

### 1. 环境检查
```bash
# 检查 Python 版本
python3 --version

# 检查依赖
python3 -c "import yaml; print('PyYAML:', yaml.__version__)"

# 检查 OpenClaw
openclaw --version

# 检查磁盘空间
df -h /path/to/deployment

# 检查内存
free -h
```

### 2. 备份现有数据
```bash
# 备份 OpenClaw 配置
cp -r ~/.openclaw/config ~/.openclaw/config.backup.$(date +%Y%m%d)

# 备份记忆文件
cp -r ~/.openclaw/workspace/memory ~/.openclaw/workspace/memory.backup.$(date +%Y%m%d)
cp ~/.openclaw/workspace/MEMORY.md ~/.openclaw/workspace/MEMORY.md.backup.$(date +%Y%m%d)

# 备份技能目录
cp -r ~/.openclaw/workspace/skills ~/.openclaw/workspace/skills.backup.$(date +%Y%m%d)
```

### 3. 下载部署包
```bash
# 从发布页面下载
VERSION="1.0.0"
wget https://github.com/your-org/hermes-system/releases/download/v${VERSION}/hermes-system-${VERSION}.tar.gz

# 验证签名
wget https://github.com/your-org/hermes-system/releases/download/v${VERSION}/hermes-system-${VERSION}.tar.gz.sig
gpg --verify hermes-system-${VERSION}.tar.gz.sig hermes-system-${VERSION}.tar.gz

# 解压
tar -xzf hermes-system-${VERSION}.tar.gz
cd hermes-system-${VERSION}
```

## 🛠️ 安装步骤

### 步骤1: 运行安装脚本
```bash
# 授予执行权限
chmod +x bin/hermes-init

# 运行安装脚本
./bin/hermes-init --workspace ~/.openclaw/workspace --config config/hermes.yaml
```

安装脚本将执行以下操作：
1. 创建必要的目录结构
2. 复制源代码到正确位置
3. 应用配置文件
4. 初始化数据库（如果需要）
5. 验证安装

### 步骤2: 配置集成
```bash
# 编辑 OpenClaw 配置
vim ~/.openclaw/config.yaml

# 添加 Hermes 配置
hermes:
  enabled: true
  workspace_dir: "/Users/apple/.openclaw/workspace/hermes"
  config_path: "/Users/apple/.openclaw/workspace/hermes/config/hermes.yaml"
  
  # 记忆系统配置
  memory:
    enabled: true
    auto_sync: true
    prefetch_threshold: 0.1
    use_embedding: false  # 生产环境建议关闭，除非有嵌入模型API
    
  # Skill生成系统配置
  skill_generation:
    enabled: true
    auto_debrief: false   # 生产环境建议手动确认
    require_approval: true
    record_code_cases: true
    
  # 数据导出配置
  data_export:
    enabled: false        # 生产环境根据需要开启
    sync_to_claude_optimization: false
    
  # 日志配置
  logging:
    level: "INFO"
    file: "/Users/apple/.openclaw/logs/hermes.log"
    max_size_mb: 100
    backup_count: 5
```

### 步骤3: 验证安装
```bash
# 检查安装状态
./bin/hermes-status

# 预期输出
✅ Hermes System Status
├── Version: 1.0.0
├── Status: Installed
├── Memory System: Ready
├── Skill Generation: Ready
├── Compatibility Layer: Active
└── OpenClaw Integration: Connected

# 测试基本功能
./bin/hermes-test --quick

# 检查日志
tail -f ~/.openclaw/logs/hermes.log
```

### 步骤4: 启动服务
```bash
# 启动 Hermes 服务
./bin/hermes-start

# 验证服务运行
ps aux | grep hermes

# 检查服务端口（如果有）
netstat -tlnp | grep hermes
```

## ⚙️ 配置详解

### 主配置文件 (hermes.yaml)
```yaml
# Hermes 系统主配置
version: "1.0.0"

# 系统设置
system:
  name: "hermes"
  environment: "production"  # development, staging, production
  debug: false
  log_level: "INFO"
  
# 记忆系统配置
memory:
  enabled: true
  workspace_dir: "/Users/apple/.openclaw/workspace"
  memory_dir: "/Users/apple/.openclaw/workspace/memory"
  
  # 同步设置
  auto_sync: true
  sync_batch_size: 10
  sync_interval_seconds: 60
  
  # 预取设置
  prefetch_enabled: true
  prefetch_threshold: 0.1
  max_prefetch_results: 5
  
  # 嵌入模型设置
  use_embedding: false
  embedding_provider: "word_overlap"  # word_overlap, openai, ollama
  embedding_cache_size: 1000
  embedding_cache_ttl_seconds: 3600
  
# Skill生成系统配置
skill_generation:
  enabled: true
  trajectories_dir: "/Users/apple/.openclaw/workspace/trajectories"
  skills_dir: "/Users/apple/.openclaw/workspace/skills"
  skill_analysis_dir: "/Users/apple/.openclaw/workspace/skill_analysis"
  
  # 轨迹记录设置
  auto_record: true
  min_trajectory_steps: 3
  max_trajectory_steps: 50
  
  # 复盘分析设置
  debrief_enabled: true
  debrief_min_confidence: 0.3
  debrief_max_candidates: 3
  
  # Skill生成设置
  require_approval: true
  auto_install: false
  skill_template: "default"
  
# 数据导出配置
data_export:
  enabled: false
  export_dir: "/Users/apple/.openclaw/workspace/exports"
  
  # 记忆导出设置
  export_memory: true
  memory_export_format: "json"  # json, csv, markdown
  memory_export_interval_hours: 24
  
  # 代码案例导出设置
  export_code_cases: true
  code_cases_dir: "/Users/apple/.openclaw/workspace/code_cases"
  sync_to_claude_optimization: false
  
# 性能监控配置
performance:
  enabled: true
  metrics_port: 9090
  health_check_interval_seconds: 30
  
  # 监控阈值
  memory_warning_mb: 100
  memory_critical_mb: 200
  response_time_warning_ms: 500
  response_time_critical_ms: 1000
  
# 集成配置
integration:
  openclaw:
    enabled: true
    workspace_dir: "/Users/apple/.openclaw/workspace"
    config_path: "/Users/apple/.openclaw/config.yaml"
    
  # Webhook 集成
  webhooks:
    enabled: false
    endpoints:
      - url: "https://api.example.com/webhook/hermes"
        events: ["skill_generated", "memory_updated"]
        
# 安全配置
security:
  enabled: true
  api_key_required: false
  rate_limit_requests_per_minute: 60
  allowed_origins:
    - "http://localhost:3000"
    - "https://openclaw.ai"
```

### 环境特定配置

#### 开发环境 (development.yaml)
```yaml
system:
  environment: "development"
  debug: true
  log_level: "DEBUG"
  
memory:
  use_embedding: false  # 开发环境使用词重叠算法
  
skill_generation:
  require_approval: false  # 开发环境自动批准
  auto_install: true
```

#### 生产环境 (production.yaml)
```yaml
system:
  environment: "production"
  debug: false
  log_level: "INFO"
  
memory:
  use_embedding: true  # 生产环境使用嵌入模型（如果可用）
  
skill_generation:
  require_approval: true  # 生产环境需要人工确认
  auto_install: false
  
security:
  api_key_required: true
  rate_limit_requests_per_minute: 30
```

## 🔄 部署脚本

### 部署脚本 (deploy.sh)
```bash
#!/bin/bash
# hermes-system/deploy.sh

set -e  # 遇到错误立即退出

# 配置变量
VERSION="1.0.0"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
BACKUP_DIR="$WORKSPACE_DIR/backups/$(date +%Y%m%d_%H%M%S)"
DEPLOY_DIR="$WORKSPACE_DIR/hermes"

echo "🚀 开始部署 Hermes 系统 v$VERSION"

# 步骤1: 备份现有部署
echo "📦 步骤1: 备份现有部署"
mkdir -p "$BACKUP_DIR"
if [ -d "$DEPLOY_DIR" ]; then
    cp -r "$DEPLOY_DIR" "$BACKUP_DIR/hermes"
    echo "✅ 现有部署已备份到: $BACKUP_DIR/hermes"
fi

# 步骤2: 创建部署目录
echo "📁 步骤2: 创建部署目录"
mkdir -p "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR/bin"
mkdir -p "$DEPLOY_DIR/config"
mkdir -p "$DEPLOY_DIR/src"
mkdir -p "$DEPLOY_DIR/var/logs"
mkdir -p "$DEPLOY_DIR/var/data"
mkdir -p "$DEPLOY_DIR/var/cache"

# 步骤3: 复制文件
echo "📋 步骤3: 复制文件"
cp -r bin/* "$DEPLOY_DIR/bin/"
cp -r config/* "$DEPLOY_DIR/config/"
cp -r src/* "$DEPLOY_DIR/src/"
cp -r docs "$DEPLOY_DIR/"
cp -r tests "$DEPLOY_DIR/"

# 步骤4: 设置权限
echo "🔒 步骤4: 设置权限"
chmod +x "$DEPLOY_DIR/bin/"*
chmod 755 "$DEPLOY_DIR"
chmod 644 "$DEPLOY_DIR/config/"*.yaml

# 步骤5: 应用环境配置
echo "⚙️ 步骤5: 应用环境配置"
ENVIRONMENT="${1:-production}"
if [ -f "$DEPLOY_DIR/config/profiles/$ENVIRONMENT.yaml" ]; then
    cp "$DEPLOY_DIR/config/profiles/$ENVIRONMENT.yaml" "$DEPLOY_DIR/config/environment.yaml"
    echo "✅ 应用环境配置: $ENVIRONMENT"
else
    echo "⚠️  环境配置不存在: $ENVIRONMENT，使用默认配置"
fi

# 步骤6: 初始化系统
echo "🔧 步骤6: 初始化系统"
cd "$DEPLOY_DIR"
./bin/hermes-init --workspace "$WORKSPACE_DIR" --config config/hermes.yaml

# 步骤7: 验证部署
echo "✅ 步骤7: 验证部署"
if ./bin/hermes-status; then
    echo "🎉 部署成功!"
    echo "📊 部署信息:"
    echo "   - 版本: $VERSION"
    echo "   - 环境: $ENVIRONMENT"
    echo "   - 目录: $DEPLOY_DIR"
    echo "   - 备份: $BACKUP_DIR"
else
    echo "❌ 部署验证失败"
    exit 1
fi
```

### 回滚脚本 (rollback.sh)
```bash
#!/bin/bash
# hermes-system/rollback.sh

set -e

WORKSPACE_DIR="$HOME/.openclaw/workspace"
DEPLOY_DIR="$WORKSPACE_DIR/hermes"
BACKUP_DIR="$WORKSPACE_DIR/backups"

echo "↩️  开始回滚 Hermes 系统"

# 检查备份目录
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ 备份目录不存在: $BACKUP_DIR"
    exit 1
fi

# 列出可用备份
echo "📦 可用备份:"
ls -1 "$BACKUP_DIR" | sort -r | head -5

# 选择备份版本
read -p "请输入要回滚的备份版本 (YYYYMMDD_HHMMSS): " BACKUP_VERSION

BACKUP_PATH="$BACKUP_DIR/$BACKUP_VERSION/hermes"
if [ ! -d "$BACKUP_PATH" ]; then
    echo "❌ 备份不存在: $BACKUP_PATH"
    exit 1
fi

# 确认回滚
read -p "确认回滚到版本 $BACKUP_VERSION? (y/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "回滚取消"
    exit 0
fi

# 停止当前服务
echo "⏹️  停止当前服务"
if [ -f "$DEPLOY_DIR/bin/hermes-stop" ]; then
    "$DEPLOY_DIR/bin/hermes-stop" || true
fi

# 备份当前部署
CURRENT_BACKUP="$BACKUP_DIR/rollback_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$CURRENT_BACKUP"
if [ -d "$DEPLOY_DIR" ]; then
    cp -r "$DEPLOY_DIR" "$CURRENT_BACKUP/"
    echo "✅ 当前部署已备份到: $CURRENT_BACKUP"
fi

# 恢复备份
echo "🔄 恢复备份"
rm -rf "$DEPLOY_DIR"
cp -r "$BACKUP_PATH" "$DEPLOY_DIR"

# 启动服务
echo "▶️  启动服务"
cd "$DEPLOY_DIR"
./bin/hermes-start

echo "✅ 回滚完成"
echo "📊 回滚信息:"
echo "   - 从版本: $(cat $CURRENT_BACKUP/hermes/VERSION 2>/dev/null || echo '未知')"
echo "   - 到版本: $(cat $DEPLOY_DIR/VERSION 2>/dev/null || echo '未知')"
echo "   - 备份位置: $CURRENT_BACKUP"
```

## 📊 监控与维护

### 健康检查
```bash
# 手动健康检查
./bin/hermes-status --health

# 自动健康检查（cron job）
*/5 * * * * /path/to/hermes/bin/hermes-status --health --quiet > /dev/null 2>&1 || /path/to/hermes/bin/hermes-restart
```

### 日志管理
```bash
# 查看实时日志
tail -f var/logs/hermes.log

# 查看错误日志
grep -i error var/logs/hermes.log | tail -20

# 日志轮转配置
# 在 /etc/logrotate.d/hermes 中添加：
/path/to/hermes/var/logs/hermes.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
```

### 性能监控
```bash
# 查看性能指标
./bin/hermes-metrics

# 导出性能数据
./bin/hermes-metrics --export --format=json --output=var/data/metrics_$(date +%Y%m%d).json
```

## 🚨 故障排除

### 常见问题

#### 问题1: 服务启动失败
**症状**: `./bin/hermes-start` 返回错误
**解决**:
```bash
# 检查日志
tail -n 50 var/logs/hermes.log

# 检查配置
./bin/hermes-validate-config

# 手动启动调试模式
python3 -m src.compatibility.hermes_compatibility --debug
```

#### 问题2: 记忆系统不工作
**症状**: 对话未同步到记忆文件
**解决**:
```bash
# 检查配置
grep -A5 "memory:" config/hermes.yaml

# 测试记忆系统
./bin/hermes-test --memory

# 检查权限
ls -la ~/.openclaw/workspace/memory/
```

#### 问题3: Skill生成失败
**症状**: 任务轨迹未生成Skill
**解决**:
```bash
# 检查轨迹目录
ls -la var/data/trajectories/

# 测试Skill生成
./bin/hermes-test --skill-generation

# 检查模板文件
ls -la config/templates/
```

#### 问题4: 性能下降
**症状**: 响应时间变慢
**解决**:
```bash
# 查看性能指标
./bin/hermes-metrics --detailed

# 清理缓存
rm -rf var/cache/*

# 重启服务
./bin/hermes-restart
```

### 紧急恢复

#### 完全重置
```bash
# 停止服务
./bin/hermes-stop

# 备份数据
cp -r var/data var/data.backup.$(date +%Y%m%d)

# 清理数据（谨慎操作）
rm -rf var/data/*
rm -rf var/cache/*

# 重新初始化
./bin/hermes-init --force

# 启动服务
./bin/hermes-start
```

#### 回滚到上一个版本
```bash
# 使用回滚脚本
./scripts/rollback.sh

# 或手动回滚
BACKUP_VERSION="20240423_093000"  # 替换为实际备份版本
cp -r ../backups/$BACKUP_VERSION/hermes/* .
./bin/hermes-restart
```

## 🔄 升级流程

### 小版本升级 (1.0.0 → 1.0.1)
```bash
# 1. 备份当前版本
./scripts/backup.sh

# 2. 下载新版本
wget https://github.com/your-org/hermes-system/releases/download/v1.0.1/hermes-system-1.0.1.tar.gz

# 3. 停止服务
./bin/hermes-stop

# 4. 解压新版本
tar -xzf hermes-system-1.0.1.tar.gz
cd hermes-system-1.0.1

# 5. 运行升级脚本
./bin/hermes-upgrade --from 1.0.0 --to 1.0.1

# 6. 启动服务
./bin/hermes-start

# 7. 验证升级
./bin/hermes-status
```

### 大版本升级 (1.0.x → 2.0.0)
```bash
# 1. 阅读升级说明
cat docs/UPGRADE_2.0.0.md

# 2. 备份数据和配置
./scripts/backup.sh --full

# 3. 运行数据迁移
./bin/hermes-migrate --version 2.0.0

# 4. 执行小版本升级流程
# ... (同上)
```

## 📞 支持与联系

### 获取帮助
- **文档**: 查看 `docs/` 目录
- **问题跟踪**: GitHub Issues
- **社区支持**: OpenClaw Discord
- **紧急支持**: support@example.com

### 报告问题
```bash
# 生成诊断报告
./bin/hermes-diagnose --output=hermes_diagnose_$(date +%Y%m%d).tar.gz

# 报告包含:
# - 系统信息
# - 配置信息
# - 日志文件
# - 性能指标
# - 错误信息
```

### 贡献指南
1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 推送分支
5. 创建 Pull Request

---

**部署指南版本**: 1.0  
**最后更新**: 2026-04-23 09:58  
**适用版本**: Hermes System 1.0.0+