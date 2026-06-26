# Log Parser

日志解析与分析工具，支持多种日志格式。

## 功能

- ✅ **多格式支持** - nginx、apache、syslog、JSON
- ✅ **自动识别** - 自动检测日志格式
- ✅ **关键信息提取** - IP、时间、状态码、路径
- ✅ **过滤** - 按 IP、状态码、路径过滤
- ✅ **统计报告** - 生成汇总报告
- ✅ **错误检测** - 提取 4xx/5xx 错误

## 测试

```bash
# 解析日志
python3 scripts/log_parser.py parse --file /var/log/nginx/access.log

# 统计报告
python3 scripts/log_parser.py stats --file /var/log/nginx/access.log

# 过滤 IP
python3 scripts/log_parser.py filter --file /var/log/nginx/access.log --ip 192.168.1.1

# 提取错误
python3 scripts/log_parser.py errors --file /var/log/nginx/access.log

# Top 10 IP
python3 scripts/log_parser.py top --file /var/log/nginx/access.log --field ip --limit 10
```

## 状态

✅ 开发完成，测试通过
