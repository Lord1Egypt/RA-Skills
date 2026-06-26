# IP Threat Check

IP 威胁情报查询工具。

## 功能

- ✅ **多源查询** - ip-api.com、AbuseIPDB
- ✅ **地理位置** - 国家、城市、ISP
- ✅ **威胁评分** - 滥用分数、风险等级
- ✅ **批量查询** - 支持文件批量检查

## 使用

```bash
# 基本信息（无需 API key）
python3 scripts/ip_threat.py info --ip 8.8.8.8

# 完整威胁检查（需要 API key）
ABUSEIPDB_API_KEY=xxx python3 scripts/ip_threat.py check --ip 1.2.3.4

# 批量查询
python3 scripts/ip_threat.py bulk --file ips.txt
```

## 环境变量

- `ABUSEIPDB_API_KEY` - AbuseIPDB API key（可选）

## 状态

✅ 开发完成
