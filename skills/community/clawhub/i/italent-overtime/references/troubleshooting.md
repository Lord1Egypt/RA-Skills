# 故障排查指南

## 认证问题

### 错误：未找到 access_token

**现象：**
```
错误：未找到 access_token
请先执行认证命令
```

**原因：** 首次使用未执行认证，或配置文件被删除

**解决方案：**
```bash
python3 scripts/italent-overtime-simple.py auth \
    --key "你的 AppKey" \
    --secret "你的 AppSecret" \
    --save
```

---

### 错误：HTTP 错误：Unauthorized (401)

**现象：**
```
✗ 无权限 - 请检查 access_token 是否有效
```

**原因：** access_token 已过期（有效期 2 小时）

**解决方案：** 重新执行认证命令

---

### 错误：HTTP 错误：Forbidden (403)

**现象：**
```
✗ 无权限
```

**原因：** AppKey 或 AppSecret 错误，或应用无权限

**解决方案：**
1. 检查 AppKey/AppSecret 是否正确
2. 确认应用已开通加班管理权限
3. 联系北森管理员

---

## 推送加班问题

### 错误：不能提交历史考勤期间的单据

**现象：**
```
✗ 失败
消息：不能提交历史考勤期间的单据
```

**原因：** 开始/结束时间是过去的日期

**解决方案：** 使用未来的日期
```bash
# 错误示例（过去日期）
--start "2024-01-01 18:00:00"

# 正确示例（未来日期）
--start "2026-04-01 18:00:00"
```

---

### 错误：您的企业没有 [工作日加班项目]

**现象：**
```
✗ 失败
消息：您的企业没有 [工作日加班项目],请更改加班日期!
```

**原因：**
1. 选择的日期不是工作日
2. 企业未在北森后台配置加班项目

**解决方案：**
1. 选择工作日（周一至周五）
2. 联系北森管理员配置加班项目
3. 确认日期不是节假日

---

### 错误：参数不可为空

**现象：**
```
✗ 失败
消息：参数不可为空，请检查！
```

**原因：** 缺少必填参数

**解决方案：** 检查以下必填参数：
- `--start` - 开始时间
- `--end` - 结束时间
- `--email` 或 `--staff-id` - 员工标识

---

## 查询加班问题

### 错误：超过查询限制

**现象：**
```
✗ 失败
消息：查询数量超过限制
```

**原因：** 员工数 × 天数 > 100

**解决方案：** 分批查询
```bash
# 错误：10 个员工 × 15 天 = 150 > 100
--staff-ids 1,2,3,4,5,6,7,8,9,10 --start 2024-01-01 --end 2024-01-15

# 正确：分两批
--staff-ids 1,2,3,4,5 --start 2024-01-01 --end 2024-01-15
--staff-ids 6,7,8,9,10 --start 2024-01-01 --end 2024-01-15
```

---

### 错误：员工 ID 不存在

**现象：**
```
✗ 失败
消息：员工 ID 不存在
```

**原因：** StaffId 格式错误或不存在

**解决方案：**
1. 确认 StaffId 是数字
2. 确认员工在北森系统中存在
3. 使用邮箱代替 StaffId

---

## 撤销加班问题

### 错误：加班 ID 不存在

**现象：**
```
✗ 失败
消息：加班 ID 不存在
```

**原因：** 加班 ID 错误或已被撤销

**解决方案：**
1. 确认加班 ID 格式正确（UUID 格式）
2. 确认加班记录存在
3. 确认加班未被撤销过

---

### 错误：不能撤销已审批通过的加班

**现象：**
```
✗ 失败
消息：不能撤销已审批通过的加班
```

**原因：** 加班已审批通过，不能直接撤销

**解决方案：**
1. 联系审批人驳回
2. 或走线下流程处理

---

## 网络问题

### 错误：网络错误

**现象：**
```
✗ 失败
消息：网络错误：[Errno 110] Connection timed out
```

**原因：** 无法访问北森 API 服务器

**解决方案：**
1. 检查网络连接
2. 确认能访问 `https://openapi.italent.cn`
3. 检查防火墙/代理设置

```bash
# 测试网络连通性
curl -I https://openapi.italent.cn
```

---

### 错误：DNS 解析失败

**现象：**
```
✗ 失败
消息：网络错误：[Errno -2] Name or service not known
```

**原因：** DNS 解析问题

**解决方案：**
1. 检查 DNS 配置
2. 尝试使用 IP 地址
3. 联系网络管理员

---

## Python 环境问题

### 错误：python3: command not found

**现象：**
```
bash: python3: command not found
```

**原因：** 未安装 Python3

**解决方案：**
```bash
# Ubuntu/Debian
sudo apt-get install python3

# macOS
brew install python3

# CentOS/RHEL
sudo yum install python3
```

---

### 错误：Permission denied

**现象：**
```
bash: ./italent-overtime-simple.py: Permission denied
```

**原因：** 脚本没有执行权限

**解决方案：**
```bash
chmod +x scripts/italent-overtime-simple.py
```

---

## 配置文件问题

### 配置文件位置

```
~/.italent-overtime.conf
```

### 配置文件格式

```json
{
  "access_token": "X4eTEiMr-r_64sjPaOQ6...",
  "expires_at": 1711864893.359761,
  "app_key": "7C4D767784DA4A1F8867E273EC4FB4C1"
}
```

### 重置配置

如果配置文件损坏，可以删除后重新认证：

```bash
rm ~/.italent-overtime.conf
python3 scripts/italent-overtime-simple.py auth --key XXX --secret XXX --save
```

---

## 获取帮助

### 查看帮助信息

```bash
python3 scripts/italent-overtime-simple.py help
```

### 查看命令帮助

```bash
python3 scripts/italent-overtime-simple.py push --help
```

### 使用 JSON 输出调试

```bash
python3 scripts/italent-overtime-simple.py push ... --json
```

---

## 联系支持

如果以上方法都无法解决问题：

1. **查看日志：** 使用 `--json` 参数查看完整响应
2. **检查文档：** 查看 [API 接口文档](api-docs.md)
3. **联系北森：** 提交工单或联系技术支持
4. **联系作者：** 佳敏

---

**最后更新：** 2026-03-31
