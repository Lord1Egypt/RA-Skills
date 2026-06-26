# master-agent-workflow-global 迁移指南

## 概述

本文档指导您如何将现有的 `master-agent-workflow` 技能迁移到全局可迁移版本 `master-agent-workflow-global`，以及如何在不同的OpenClaw实例之间迁移配置。

## 迁移优势

### ✅ 新版本特性
1. **全局可用**：在任何OpenClaw实例中安装即可使用
2. **配置迁移**：支持导出/导入配置和状态
3. **模板系统**：预定义任务模板，快速启动
4. **版本管理**：支持版本升级和回滚
5. **依赖管理**：明确声明依赖关系

## 迁移步骤

### 步骤1：备份当前配置

```bash
# 从当前版本导出配置
cd "C:\Users\Shu JM\.openclaw\workspace\skills\master-agent-workflow"
# 如果有导出工具则使用，否则手动备份
cp -r . /tmp/maw-backup/
```

### 步骤2：安装全局版本

```bash
# 方法1：使用安装脚本
cd "C:\Users\Shu JM\.openclaw\workspace\master-agent-workflow-global"
./install.sh

# 方法2：通过ClawdHub（发布后）
clawdhub install master-agent-workflow-global
```

### 步骤3：迁移配置

```bash
# 使用迁移工具
cd "$HOME/.openclaw/global-skills/master-agent-workflow"
./scripts/migrate.sh import /tmp/maw-backup/
```

### 步骤4：验证迁移

```bash
# 测试基本功能
maw --version
maw-list templates

# 运行测试任务
maw --test --dry-run
```

## 跨系统迁移

### 场景1：Windows → Linux

```bash
# 在Windows上导出
maw export --format tar.gz --output maw-windows-backup.tar.gz

# 在Linux上导入
scp maw-windows-backup.tar.gz user@linux-server:/tmp/
ssh user@linux-server "maw import --file /tmp/maw-windows-backup.tar.gz"
```

### 场景2：开发环境 → 生产环境

```bash
# 开发环境导出
maw export --include-state --output maw-dev-to-prod.tar.gz

# 生产环境导入（不包含运行状态）
maw import --file maw-dev-to-prod.tar.gz --exclude-state
```

### 场景3：团队共享配置

```bash
# 创建团队配置模板
maw create-template team-config \
  --max-workers 8 \
  --timeout 4h \
  --report-channel slack

# 导出模板
maw export-template team-config --output team-maw-template.json

# 团队成员导入
maw import-template --file team-maw-template.json
```

## 配置迁移内容

### 可迁移的项目

| 项目 | 说明 | 是否必需 |
|------|------|----------|
| 任务模板 | 预定义的任务分解模板 | 可选 |
| 性能配置 | max_workers, timeout等参数 | 推荐 |
| 历史记录 | 任务执行历史统计 | 可选 |
| 错误处理 | 自定义错误处理规则 | 可选 |
| 报告模板 | 进度报告和最终报告模板 | 可选 |

### 配置文件结构

```json
{
  "migration": {
    "version": "2.0.0",
    "timestamp": "2026-03-27T09:58:00+08:00",
    "source": "master-agent-workflow@1.0.0",
    "target": "master-agent-workflow-global@2.0.0",
    "config": {
      "max_workers": 5,
      "timeout_hours": 3,
      "worker_timeout_minutes": 30
    },
    "templates": [...],
    "history": [...]
  }
}
```

## 自动化迁移脚本

### 完整迁移脚本

```bash
#!/bin/bash
# auto-migrate-maw.sh

set -e

echo "开始迁移 master-agent-workflow 到全局版本..."

# 1. 检查当前版本
if [ -d "$HOME/.openclaw/workspace/skills/master-agent-workflow" ]; then
    echo "检测到旧版本，开始备份..."
    BACKUP_DIR="/tmp/maw-backup-$(date +%Y%m%d-%H%M%S)"
    cp -r "$HOME/.openclaw/workspace/skills/master-agent-workflow" "$BACKUP_DIR"
    echo "备份完成: $BACKUP_DIR"
fi

# 2. 安装新版本
if [ -f "install.sh" ]; then
    ./install.sh
else
    echo "下载并安装全局版本..."
    curl -L https://clawhub.com/skills/master-agent-workflow-global/install.sh | bash
fi

# 3. 迁移配置
if [ -d "$BACKUP_DIR" ]; then
    echo "迁移配置..."
    MAW_HOME="$HOME/.openclaw/global-skills/master-agent-workflow"
    
    # 迁移skill.json配置
    if [ -f "$BACKUP_DIR/skill.json" ]; then
        jq '. + {migrated_from: "1.0.0"}' "$BACKUP_DIR/skill.json" > "$MAW_HOME/migrated-skill.json"
    fi
    
    # 迁移示例文件
    if [ -d "$BACKUP_DIR/examples" ]; then
        cp -r "$BACKUP_DIR/examples" "$MAW_HOME/migrated-examples/"
    fi
fi

# 4. 清理旧版本（可选）
read -p "是否删除旧版本？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/.openclaw/workspace/skills/master-agent-workflow"
    echo "旧版本已删除"
fi

echo "迁移完成！"
```

## 故障排除

### 常见问题

#### Q1: 迁移后任务无法执行
**原因**：权限或路径问题
**解决**：
```bash
# 检查权限
ls -la "$HOME/.openclaw/global-skills/master-agent-workflow"

# 重新安装
./install.sh --force
```

#### Q2: 配置导入失败
**原因**：版本不兼容
**解决**：
```bash
# 查看版本
maw --version

# 使用兼容模式导入
maw import --file backup.json --compatibility-mode
```

#### Q3: 模板无法使用
**原因**：模板格式错误
**解决**：
```bash
# 验证模板
maw validate-template template-name

# 重新创建模板
maw create-template template-name --from-file template-backup.json
```

## 回滚方案

### 回滚到旧版本

```bash
# 1. 备份当前全局版本
cp -r "$HOME/.openclaw/global-skills/master-agent-workflow" /tmp/maw-global-backup/

# 2. 卸载全局版本
./uninstall.sh

# 3. 恢复旧版本
cp -r /tmp/maw-backup/ "$HOME/.openclaw/workspace/skills/master-agent-workflow"

# 4. 更新OpenClaw配置
# 编辑 config.json，移除 master-agent-workflow-global，添加 master-agent-workflow
```

### 部分回滚（仅配置）

```bash
# 导出当前配置
maw export --output current-config.json

# 编辑配置，移除有问题部分
vim current-config.json

# 重新导入
maw import --file current-config.json --partial
```

## 最佳实践

### 迁移前
1. ✅ 备份所有重要数据
2. ✅ 记录当前配置参数
3. ✅ 测试迁移脚本（在测试环境）
4. ✅ 通知相关用户（如果是生产环境）

### 迁移中
1. ✅ 使用 `--dry-run` 先测试
2. ✅ 分阶段迁移（先配置，后数据）
3. ✅ 记录迁移日志
4. ✅ 验证每一步的结果

### 迁移后
1. ✅ 运行验证测试
2. ✅ 监控系统性能
3. ✅ 收集用户反馈
4. ✅ 更新文档

## 支持与帮助

### 获取帮助
```bash
# 查看帮助文档
maw --help

# 查看迁移指南
maw migration-guide

# 联系支持
maw support --contact
```

### 报告问题
```bash
# 生成诊断报告
maw diagnose --output diagnosis.json

# 提交问题
maw report-issue --description "迁移问题描述"
```

---

**版本**: 2.0.0  
**最后更新**: 2026-03-27  
**作者**: 小龙  
**状态**: ✅ 生产就绪