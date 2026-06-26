# JSON Formatter Skill

JSON 格式化、压缩、校验、转换工具。

## 功能

- ✅ **格式化** - 美化 JSON，添加缩进
- ✅ **压缩** - 移除空白，压缩 JSON
- ✅ **校验** - 检查 JSON 语法
- ✅ **转换** - JSON ↔ YAML 互转

## 安装

```bash
pip install pyyaml
```

## 测试

```bash
# 格式化
python3 scripts/json_formatter.py format --input '{"name":"test","value":123}'

# 压缩
python3 scripts/json_formatter.py compress --input '{"name": "test", "value": 123}'

# 校验
python3 scripts/json_formatter.py validate --input '{"name":"test"}'

# 转 YAML
python3 scripts/json_formatter.py to-yaml --input '{"name":"test","items":[1,2,3]}'

# 从 YAML 转换
python3 scripts/json_formatter.py from-yaml --input 'name: test'
```

## 状态

✅ 开发完成，待测试
