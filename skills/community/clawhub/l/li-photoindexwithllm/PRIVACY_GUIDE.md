# 隐私保护指南

**作者**: 北京老李（beijingLL）  
**日期**: 2026-05-16

---

## 🔒 隐私保护原则

PhotoIndexWithLLM 将用户隐私和数据安全放在首位。本指南说明如何最大程度保护您的照片数据。

---

## ⚠️ 重要隐私警告

### 🔴 使用远程模型的风险

当您使用远程 VL 模型（如 OpenRouter、NVIDIA 等）时：

1. **照片会被发送到第三方服务器**
   - 完整的照片内容（base64 编码）会传输到远程服务器
   - 第三方可能存储、分析或使用这些照片

2. **无法控制第三方行为**
   - 您无法审计第三方如何处理数据
   - 隐私政策可能随时更改

3. **敏感照片可能泄露**
   - 家庭照片、个人照片、工作照片等
   - 包含人脸、位置、文档等敏感信息

---

## 🛡️ 推荐安全配置

### 配置 1：最安全（推荐）

```ini
# .env 文件 - 最安全配置

# ✅ 仅使用本地模型
LOCAL_LLM_ENABLED=true
LOCAL_LLM_ENDPOINT=http://localhost:1234/v1
LOCAL_LLM_MODEL=qwen3-vl-8b-q4_k_m

# ❌ 禁用远程模型
REMOTE_LLM_ENABLED=false
REMOTE_LLM_API_KEY=

# 🔒 隐私模式
PRIVACY_MODE=local_only
ALLOW_REMOTE_UPLOAD=false
REQUIRE_REMOTE_CONFIRM=true
```

**优点**：
- ✅ 照片永远不会离开您的电脑
- ✅ 完全控制数据
- ✅ 无第三方风险

**缺点**：
- ⚠️ 需要本地 GPU（8GB+ 显存）
- ⚠️ 处理速度可能较慢

---

### 配置 2：混合模式（谨慎使用）

```ini
# .env 文件 - 混合配置

# ✅ 本地模型优先
LOCAL_LLM_ENABLED=true
LOCAL_LLM_ENDPOINT=http://localhost:1234/v1

# ⚠️ 远程模型（仅用于非敏感照片）
REMOTE_LLM_ENABLED=true
REMOTE_LLM_API_KEY=your-key

# 🔒 隐私保护
PRIVACY_MODE=hybrid
ALLOW_REMOTE_UPLOAD=true
REQUIRE_REMOTE_CONFIRM=true  # 需要用户确认
```

**使用建议**：
- ✅ 仅对不敏感照片使用远程模型
- ✅ 家庭照片、个人照片使用本地模型
- ✅ 风景照、公开照片可以使用远程模型

---

## 📋 安全检查清单

使用本程序前，请确认：

- [ ] 已了解远程模型的风险
- [ ] 已设置合适的隐私模式
- [ ] 已保护 `.env` 文件（不要提交到 Git）
- [ ] 已限制数据库文件权限
- [ ] 已定期清理不需要的数据

---

## 🔐 数据安全最佳实践

### 1. 保护配置文件

```bash
# Linux/Mac - 限制文件权限
chmod 600 .env
chmod 600 data/photo_index.db

# Windows - 使用 PowerShell
icacls .env /inheritance:r /grant:r "${env:USERNAME}:R"
```

### 2. 不要提交敏感文件

```bash
# .gitignore 应包含
.env
data/*.db
*.log
```

### 3. 定期清理数据

```bash
# 删除不需要的索引
rm data/photo_index.db

# 清理日志
rm logs/*.log
```

### 4. 使用本地模型

```bash
# 测试本地模型连接
python skill.py test

# 仅使用本地模式扫描
python skill.py scan --dir D:\Photos
```

---

## 🚨 隐私事件响应

如果您怀疑数据泄露：

1. **立即停止使用远程模型**
   ```ini
   REMOTE_LLM_ENABLED=false
   ```

2. **更改 API Key**
   - 联系服务提供商
   - 生成新的 API Key

3. **清理数据库**
   ```bash
   rm data/photo_index.db
   ```

4. **审查日志**
   ```bash
   cat logs/*.log
   ```

---

## 📞 报告安全问题

如果您发现任何隐私或安全问题，请联系：

**作者**: 北京老李（beijingLL）  
**项目**: PhotoIndexWithLLM

---

**隐私是我们的责任！** 🔒
