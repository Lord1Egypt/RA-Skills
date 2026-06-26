# 备份与恢复

## 备份范围

Harbor 需要备份的组件：

| 组件 | 数据类型 | 备份方式 | 重要程度 |
|------|---------|---------|---------|
| **Harbor DB** | 项目/用户/策略等元数据 | `pg_dump` | ⭐⭐⭐ 极高 |
| **Registry Data** | 镜像层数据 | `tar` 打包 | ⭐⭐⭐ 极高 |
| **Redis** | 任务队列缓存 | 可选 | ⭐ 中 |
| **Trivy DB** | 漏洞库 | 不需要 | 低 |
| **Notary Data** | 签名数据 | `tar` 打包（如果启用） | ⭐⭐ |
| **Chart Museum** | Helm Chart | 同 Registry | ⭐ |

## 推荐备份脚本

```bash
#!/bin/bash
# /opt/harbor-backup/backup.sh
set -e

BACKUP_ROOT="/data/harbor-backup"
HARBOR_ROOT="/opt/harbor"
DATE=$(date +%Y%m%d_%H%M%S)
KEEP_DAYS=30

mkdir -p "$BACKUP_ROOT"

# === 1. 数据库备份 ===
echo "[1/4] 备份数据库..."
docker exec harbor-db pg_dump -U postgres registry > "$BACKUP_ROOT/harbor-db-$DATE.sql"
gzip "$BACKUP_ROOT/harbor-db-$DATE.sql"

# === 2. 配置文件备份 ===
echo "[2/4] 备份配置..."
tar czf "$BACKUP_ROOT/harbor-config-$DATE.tar.gz" \
  "$HARBOR_ROOT/common/config" \
  "$HARBOR_ROOT/common/templates" \
  2>/dev/null || true

# === 3. Registry 数据备份（差异/增量建议）===
echo "[3/4] 备份镜像数据（差异）..."
# 全量备份（首次或每周）
if [ "$(date +%u)" = "1" ]; then
  tar czf "$BACKUP_ROOT/harbor-registry-full-$DATE.tar.gz" \
    /data/harbor/registry /data/harbor/redis 2>/dev/null || true
else
  # 增量备份（rsync 方式）
  rsync -a --delete /data/harbor/registry/ \
    "$BACKUP_ROOT/registry-incremental-$DATE/" 2>/dev/null || true
fi

# === 4. 上传至对象存储 ===
echo "[4/4] 同步到对象存储..."
rclone copy "$BACKUP_ROOT/harbor-db-$DATE.sql.gz" \
  "s3:my-backup-bucket/harbor/$DATE/" --s3-storage-class GLACIER

# === 5. 清理本地旧备份 ===
find "$BACKUP_ROOT" -name "*.sql.gz" -mtime +$KEEP_DAYS -delete
find "$BACKUP_ROOT" -name "*.tar.gz" -mtime +$KEEP_DAYS -delete

echo "✅ 备份完成: $DATE"
echo "   DB: $BACKUP_ROOT/harbor-db-$DATE.sql.gz"
echo "   Config: $BACKUP_ROOT/harbor-config-$DATE.tar.gz"
```

## Cron 定时任务

```bash
# 每天凌晨3点执行全量备份
0 3 * * * /opt/harbor-backup/backup.sh >> /var/log/harbor-backup.log 2>&1
```

## 恢复步骤

### 1. 恢复数据库

```bash
# 停止 Harbor
cd /opt/harbor && docker-compose down

# 恢复数据库
gunzip < /data/harbor-backup/harbor-db-20240101_030000.sql.gz | \
  docker exec -i harbor-db psql -U postgres registry

# 如果数据库schema有变化，先创建扩展
docker exec harbor-db psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
```

### 2. 恢复配置

```bash
# 恢复配置目录
tar xzf /data/harbor-backup/harbor-config-20240101_030000.tar.gz -C /

# 确保权限正确
chown -R 10000:10000 /opt/harbor/common/config
```

### 3. 重启 Harbor

```bash
cd /opt/harbor && docker-compose up -d
```

### 4. 验证

```bash
# 检查所有组件状态
docker-compose ps

# 验证数据库内容
curl -s -u admin:Harbor12345 https://harbor.mycompany.com/api/v2.0/health | jq .

# 验证项目数据
curl -s -u admin:Harbor12345 https://harbor.mycompany.com/api/v2.0/projects | jq '.[].name'
```

## 灾难恢复预案

### 场景1：新服务器恢复

1. 在新服务器安装同版本 Harbor（`install.sh`）
2. 修改 `harbor.yml` 指向新的数据库和存储
3. 执行数据库恢复：`gunzip < backup.sql.gz | psql`
4. 恢复配置：`tar xzf config.tar.gz`
5. `docker-compose up -d`
6. 验证健康状态和镜像列表

### 场景2：误删除项目恢复

```bash
# 从备份中提取特定项目的数据
gunzip < harbor-db-20240101_030000.sql.gz | \
  grep "INSERT INTO project" | \
  grep '"name":"my-deleted-project"' > project_recovery.sql

# 恢复
docker exec -i harbor-db psql -U postgres registry < project_recovery.sql
```

### 备份验证（每月检查）

```bash
# 恢复测试：启动临时容器验证备份完整性
docker run --rm -v /data/harbor-backup:/backup postgres:15 \
  psql -h db-host -U postgres -d registry < /backup/harbor-db-latest.sql \
  -c "SELECT COUNT(*) FROM project;"  # 应返回项目数量
```

## 备份检查清单

- [ ] 备份脚本有执行权限且定时运行
- [ ] 对象存储上传成功（检查日志）
- [ ] 每月至少一次恢复演练
- [ ] 备份保留策略覆盖足够时长（建议 ≥ 90 天）
- [ ] 备份加密存储（敏感环境）
- [ ] 新管理员知道备份位置和恢复流程
