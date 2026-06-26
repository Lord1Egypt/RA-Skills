# master-agent-workflow-global 使用示例

## 快速开始

### 示例1：基本使用
```bash
# 使用默认配置执行任务
使用 master-agent-workflow-global execute "处理我的任务"

# 快捷命令
maw "处理我的任务"
```

### 示例2：自定义配置
```bash
# 指定并行数和超时时间
使用 master-agent-workflow-global execute "批量处理文件" \
  --max-workers 10 \
  --timeout 2h \
  --worker-timeout 45m
```

### 示例3：使用模板
```bash
# 使用文件处理模板
使用 master-agent-workflow-global execute "处理100个文件" \
  --template file_processing

# 使用API调用模板
使用 master-agent-workflow-global execute "调用50个API" \
  --template api_calling
```

## 配置管理示例

### 保存自定义配置
```bash
# 保存高性能配置
使用 master-agent-workflow-global configure save high-performance \
  --max-workers 20 \
  --timeout 4h \
  --worker-timeout 60m \
  --stuck-threshold 30 \
  --fail-threshold 5

# 保存安全配置
使用 master-agent-workflow-global configure save safe-mode \
  --max-workers 3 \
  --timeout 1h \
  --worker-timeout 15m \
  --fail-threshold 1
```

### 使用保存的配置
```bash
# 使用高性能配置
使用 master-agent-workflow-global execute "大数据处理" \
  --config high-performance

# 使用安全配置
使用 master-agent-workflow-global execute "关键任务" \
  --config safe-mode
```

### 列出所有配置
```bash
使用 master-agent-workflow-global configure list
# 输出:
# - default
# - high-performance
# - safe-mode
```

## 模板使用示例

### 查看可用模板
```bash
使用 master-agent-workflow-global template list
# 输出:
# - file_processing: 文件处理模板
# - api_calling: API调用模板
# - data_processing: 数据处理模板
```

### 创建自定义模板
1. 创建模板文件 `my-template.json`:
```json
{
  "name": "my_template",
  "description": "我的自定义模板",
  "config": {
    "max_workers": 8,
    "timeout_hours": 2,
    "worker_timeout_minutes": 20,
    "report_channel": "console"
  }
}
```

2. 复制到模板目录:
```bash
cp my-template.json ~/.openclaw/global-skills/master-agent-workflow/templates/
```

3. 使用自定义模板:
```bash
使用 master-agent-workflow-global execute "自定义任务" \
  --template my_template
```

## 迁移示例

### 导出配置
```bash
# 导出所有配置和模板
使用 master-agent-workflow-global migrate export \
  --output maw-backup-$(date +%Y%m%d).json

# 导出包含运行状态
使用 master-agent-workflow-global migrate export \
  --include-state \
  --output maw-full-backup.tar.gz
```

### 导入配置
```bash
# 导入配置
使用 master-agent-workflow-global migrate import \
  maw-backup-20260327.json

# 从其他系统导入
scp user@remote-server:~/maw-backup.json .
使用 master-agent-workflow-global migrate import maw-backup.json
```

### 跨系统迁移
```bash
# 系统A：导出
使用 master-agent-workflow-global migrate export \
  --output migration-package.json

# 系统B：导入
使用 master-agent-workflow-global migrate import \
  migration-package.json
```

## 实际应用场景

### 场景1：文件批量处理
```bash
# 处理大量图片文件
使用 master-agent-workflow-global execute "批量压缩图片" \
  --template file_processing \
  --max-workers 5 \
  --worker-timeout 30m

# 具体任务描述
任务描述: 压缩images/目录下的所有图片
文件列表: [image1.jpg, image2.png, ... image100.webp]
处理逻辑: 使用ImageMagick压缩到原大小的80%
输出目录: compressed/
```

### 场景2：API批量调用
```bash
# 批量调用用户API
使用 master-agent-workflow-global execute "更新用户信息" \
  --template api_calling \
  --max-workers 3 \
  --timeout 1h

# API端点列表
端点: /api/users/{id}
ID列表: [1, 2, 3, ..., 1000]
请求方法: GET
处理逻辑: 获取用户信息并更新本地数据库
```

### 场景3：数据批量处理
```bash
# 处理数据库记录
使用 master-agent-workflow-global execute "数据清洗" \
  --template data_processing \
  --max-workers 10 \
  --worker-timeout 15m

# 数据源
数据库表: users
记录数: 10000
处理逻辑: 
  1. 验证邮箱格式
  2. 标准化电话号码
  3. 清理重复记录
  4. 导出清洗后数据
```

### 场景4：监控和报告
```bash
# 定期生成系统报告
使用 master-agent-workflow-global execute "生成周报" \
  --max-workers 1 \
  --timeout 30m \
  --report-channel feishu

# 报告内容
1. 系统性能统计
2. 任务完成情况
3. 错误和警告
4. 优化建议
5. 下周计划
```

## 高级用法

### 组合使用配置和模板
```bash
# 使用模板并覆盖部分配置
使用 master-agent-workflow-global execute "特殊处理" \
  --template file_processing \
  --max-workers 15 \
  --worker-timeout 90m
```

### 环境变量覆盖
```bash
# 使用环境变量设置配置
export MAW_MAX_WORKERS=20
export MAW_TIMEOUT_HOURS=4
使用 master-agent-workflow-global execute "环境变量测试"
```

### 脚本集成
```bash
#!/bin/bash
# 自动化脚本示例

# 加载配置
CONFIG_FILE="maw-config.json"
if [ -f "$CONFIG_FILE" ]; then
    CONFIG="--config $(jq -r '.config_name' "$CONFIG_FILE")"
else
    CONFIG=""
fi

# 执行任务
使用 master-agent-workflow-global execute "自动化任务" \
  $CONFIG \
  --max-workers 8 \
  --timeout 2h

# 检查结果
if [ $? -eq 0 ]; then
    echo "任务执行成功"
else
    echo "任务执行失败"
    exit 1
fi
```

## 故障排除示例

### 调试模式
```bash
# 启用详细日志
export MAW_DEBUG=true
使用 master-agent-workflow-global execute "调试任务" \
  --dry-run

# 查看日志
cat ~/.openclaw/global-skills/master-agent-workflow/logs/debug.log
```

### 性能测试
```bash
# 测试不同配置的性能
for workers in 1 3 5 10; do
    echo "测试并行数: $workers"
    使用 master-agent-workflow-global execute "性能测试" \
      --max-workers $workers \
      --timeout 10m \
      --dry-run
    echo ""
done
```

### 配置验证
```bash
# 验证配置有效性
使用 master-agent-workflow-global execute "配置验证" \
  --config my-config \
  --dry-run \
  --validate-only
```

## 最佳实践示例

### 生产环境配置
```bash
# 生产环境推荐配置
使用 master-agent-workflow-global configure save production \
  --max-workers $(nproc) \
  --timeout 6h \
  --worker-timeout 30m \
  --stuck-threshold 30 \
  --fail-threshold 3 \
  --auto-cleanup true \
  --report-channel feishu
```

### 开发环境配置
```bash
# 开发环境配置
使用 master-agent-workflow-global configure save development \
  --max-workers 2 \
  --timeout 1h \
  --worker-timeout 10m \
  --fail-threshold 10 \
  --report-channel console
```

### 测试环境配置
```bash
# 测试环境配置
使用 master-agent-workflow-global configure save testing \
  --max-workers 1 \
  --timeout 30m \
  --worker-timeout 5m \
  --fail-threshold 0 \
  --dry-run true
```

## 集成示例

### 与cron集成
```bash
# 创建cron任务
0 2 * * * /usr/bin/使用 master-agent-workflow-global execute "每日备份" --config production
```

### 与CI/CD集成
```yaml
# GitHub Actions示例
name: MAW Processing
on: [push]
jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run MAW
        run: |
          使用 master-agent-workflow-global execute "CI处理" \
            --max-workers 4 \
            --timeout 30m
```

### 与监控系统集成
```bash
# 发送监控指标
使用 master-agent-workflow-global execute "生成监控报告" \
  --max-workers 1 \
  --timeout 5m \
  --report-channel prometheus
```

---
**示例版本**: 2.0.0  
**最后更新**: 2026-03-27  
**更多示例**: 参考技能文档和模板目录