# 🔑 ThinkZone API 配置

## ✅ API 配置已更新

**API Key：** `amags_b6324919c0056a78dc326ef06011ecc7d2af896b6b659c216371e55d66895dac`

**API 地址：** `https://open.thinkzoneai.com/`

**更新时间：** 2026-03-19 14:03

---

## 🔧 环境变量设置

### Windows PowerShell（当前会话）
```powershell
$env:THINKZONE_API_KEY="amags_b6324919c0056a78dc326ef06011ecc7d2af896b6b659c216371e55d66895dac"
```

### Windows（永久设置）
1. 右键"此电脑" → 属性 → 高级系统设置
2. 点击"环境变量"
3. 新建用户变量：
   - **变量名：** `THINKZONE_API_KEY`
   - **变量值：** `amags_b6324919c0056a78dc326ef06011ecc7d2af896b6b659c216371e55d66895dac`
4. 重启终端生效

---

## 🧪 测试命令

```powershell
cd C:\Users\Administrator\.openclaw\workspace\skills\thinkzone-image

# 使用 Seedream 模型测试
$env:THINKZONE_API_KEY="amags_b6324919c0056a78dc326ef06011ecc7d2af896b6b659c216371e55d66895dac"
python scripts/gen_image.py --prompt "一只可爱的金毛犬正在吃玉米" --model "doubao-seedream-5-0-260128" --size "2K"
```

---

## ⚠️ 故障排查

### 401 Unauthorized

**可能原因：**
1. API Key 格式错误
2. API Key 未激活
3. API Key 已过期

**解决方法：**
1. 检查密钥是否完整复制（前后无空格）
2. 访问 https://testing.amags.thinkzoneai.com 确认账户状态
3. 联系 ThinkZone 支持

### 503 Service Unavailable

**可能原因：** 账户余额不足

**解决方法：** 充值账户

---

## 📞 相关资源

- **ThinkZone 平台：** https://testing.amags.thinkzoneai.com
- **API 文档：** 查看平台文档
- **支持联系：** 通过平台客服

---

**配置者：** 田渝米 🍚
