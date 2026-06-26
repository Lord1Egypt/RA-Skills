# 不安全代码示例

⚠️ **警告**: 此目录包含故意编写的不安全代码，仅用于测试！
**切勿在生产环境中使用！**

## 包含的安全问题

1. ❌ 使用 DES 加密
2. ❌ SQL 字符串拼接
3. ❌ os.system 命令执行
4. ❌ eval 执行用户输入
5. ❌ 硬编码密码
6. ❌ Flask debug=True

## 测试方法

```bash
# 扫描此示例项目
python scripts/python_sec_check.py examples/unsafe-example

# 预期结果：应检测到所有安全问题
```

## 预期检测报告

- ✅ 项目结构检查 - 通过
- ❌ 加密算法 - 发现 DES
- ❌ SQL 注入 - 发现字符串拼接
- ❌ 命令注入 - 发现 os.system/eval
- ❌ 敏感信息 - 发现硬编码密码
- ❌ 调试模式 - 发现 debug=True

---

*仅用于安全测试！*
