# 百度 API Key 获取指南

## 📋 步骤说明

### 步骤 1：访问百度智能云

打开网址：https://ai.baidu.com/tech/search

---

### 步骤 2：登录/注册百度账号

- 如果有百度账号，直接登录
- 如果没有，点击 "注册" 创建账号（支持手机号注册）

---

### 步骤 3：进入控制台

登录后，点击页面右上角的 **"控制台"** 按钮。

---

### 步骤 4：创建应用

1. 在控制台页面，点击 **"创建应用"**
2. 填写应用信息：
   - **应用名称：** OpenClaw Search（随意填写）
   - **应用描述：** 搜索功能（可选）
   - **图标：** 可跳过
3. 点击 **"创建"**

---

### 步骤 5：获取 API Key

创建成功后，会显示应用详情页面，包含：

- **API Key（AK）：** 类似 `xxxxxxxxxxxxxxxxxxxxxx`
- **Secret Key（SK）：** 类似 `xxxxxxxxxxxxxxxxxxxxxx`

**复制这两个 Key，保存到配置文件！**

---

## ⚙️ 配置到 Search Pro

编辑配置文件：

```bash
vi ~/.openclaw/workspace/skills/search-pro/config/search-config.json
```

修改为：

```json
{
  "engines": {
    "baidu": {
      "enabled": true,
      "apiKey": "你的 API Key",
      "secretKey": "你的 Secret Key"
    }
  }
}
```

保存后，百度搜索即可使用！

---

## 🧪 测试

```bash
cd ~/.openclaw/workspace/skills/search-pro
python3 scripts/multi-search.py "测试搜索" --engine baidu
```

---

## 💰 免费额度

百度搜索引擎 API 的免费额度：

- **每日限额：** 查看控制台具体说明
- **超出后：** 需要付费或等待次日重置

---

## ❓ 常见问题

### Q: API Key 无效？
A: 检查是否复制完整，不要有多余空格。

### Q: 提示额度不足？
A: 登录控制台查看使用情况，可能需要升级套餐。

### Q: 搜索结果为空？
A: 检查关键词是否太特殊，尝试简单关键词测试。

---

## 🔗 相关链接

- 百度搜索引擎 API：https://ai.baidu.com/tech/search
- 百度智能云控制台：https://console.bce.baidu.com/
- API 文档：https://ai.baidu.com/ai-doc/SEARCH

---

**配置完成后，即可享受快速稳定的中文搜索！** 🎉
