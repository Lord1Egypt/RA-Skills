# Photo Search Skill 隐私与数据安全报告

**作者**: 北京老李（beijingLL）  
**日期**: 2026-05-16  
**版本**: v1.0

---

## 🔍 安全审计结果

### 🔴 严重问题（必须修复）

#### 1. 照片数据发送到远程服务器

**问题描述**：
- 使用远程 VL 模型时，**完整的照片内容**（base64 编码）会被发送到第三方服务器
- 第三方服务器（如 OpenRouter）可能存储、分析或使用这些照片数据
- 用户无法控制或审计第三方如何处理数据

**受影响功能**：
- `VLClient.analyze_image()` - 图片分析
- 远程模型调用（OpenRouter、NVIDIA 等）

**风险等级**：🔴 严重

**建议修复**：
1. ✅ **默认仅使用本地模型**（LM Studio）
2. ✅ 添加明确的用户确认提示
3. ✅ 提供"仅本地模式"选项
4. ✅ 记录所有远程传输日志

---

#### 2. 敏感照片路径泄露

**问题描述**：
- 数据库存储完整的文件路径（如 `D:\Personal\Photos\family\img001.jpg`）
- 路径可能包含敏感信息（用户名、文件夹名称等）
- 搜索结果会暴露完整路径

**风险等级**：🟡 中等

**建议修复**：
1. 提供路径脱敏选项
2. 数据库加密
3. 限制路径显示范围

---

### 🟡 中等问题（建议修复）

#### 3. API Key 明文存储

**问题描述**：
- `.env` 文件中 API Key 明文存储
- 可能被意外提交到版本控制系统
- 文件权限未限制

**风险等级**：🟡 中等

**建议修复**：
1. 添加 `.env` 到 `.gitignore`
2. 限制文件权限（仅所有者可读）
3. 提供环境变量替代方案

---

#### 4. 数据库未加密

**问题描述**：
- SQLite 数据库明文存储
- 包含照片路径、描述、标签等敏感信息
- 任何有文件访问权限的人都可以读取

**风险等级**：🟡 中等

**建议修复**：
1. 使用 SQLCipher 加密数据库
2. 提供数据库密码保护
3. 限制数据库文件权限

---

### 🟢 轻微问题（可选优化）

#### 5. 日志可能包含敏感信息

**问题描述**：
- 错误日志可能包含照片路径
- 调试模式可能输出详细信息

**风险等级**：🟢 轻微

---

## 🛡️ 安全改进计划

### Phase 1: 立即实施（必须）

#### 1. 添加隐私模式选项

```python
# 新增配置项
PRIVACY_MODE = "local_only"  # local_only | hybrid | remote
ALLOW_REMOTE_UPLOAD = false  # 默认禁止远程上传
```

#### 2. 添加用户确认机制

```python
def analyze_photo(self, image_path: str, prompt: str) -> dict:
    """分析照片"""
    # 检查是否使用远程模型
    if self.use_remote and not self.confirmed_remote:
        print("⚠️  警告：使用远程模型会将照片发送到第三方服务器")
        print(f"   目标服务器: {self.remote_endpoint}")
        print("   照片内容可能被第三方存储或分析")
        
        confirm = input("是否继续？(yes/no): ")
        if confirm.lower() != "yes":
            raise PermissionError("用户拒绝远程传输")
        
        self.confirmed_remote = True
    
    # ... 继续分析
```

#### 3. 添加隐私文档

创建 `PRIVACY.md` 文档，明确说明：
- 数据存储位置
- 数据传输方式
- 第三方服务使用
- 用户权利

---

### Phase 2: 短期改进（建议）

#### 4. 数据库加密

```python
# 使用 SQLCipher
import sqlite3

# 加密数据库
conn = sqlite3.connect('file:encrypted.db?cipher=sqlcipher')
conn.execute("PRAGMA key='your-secret-key'")
```

#### 5. 文件权限限制

```bash
# Linux/Mac
chmod 600 .env
chmod 600 data/photo_index.db

# Windows PowerShell
icacls .env /inheritance:r /grant:r "${env:USERNAME}:R"
```

#### 6. 路径脱敏

```python
def sanitize_path(path: str) -> str:
    """脱敏文件路径"""
    # D:\Users\John\Photos\family\img001.jpg
    # → Photos\family\img001.jpg
    parts = Path(path).parts
    if len(parts) > 3:
        return str(Path(*parts[3:]))
    return path
```

---

### Phase 3: 长期优化（可选）

#### 7. 本地优先架构

- 默认仅使用本地模型
- 远程模型作为可选增强
- 提供清晰的隐私选项

#### 8. 数据最小化

- 只存储必要的索引数据
- 不存储原始照片
- 定期清理缓存

#### 9. 审计日志

- 记录所有远程传输
- 记录数据访问
- 提供审计报告

---

## 📋 用户隐私建议

### 对于普通用户

1. ✅ **优先使用本地模型**（LM Studio）
   - 照片不会离开你的电脑
   - 完全控制数据

2. ✅ **谨慎使用远程模型**
   - 了解照片会被发送到第三方
   - 仅对不敏感照片使用

3. ✅ **定期清理数据**
   - 删除不需要的索引
   - 清理数据库缓存

4. ✅ **保护配置文件**
   - 不要分享 `.env` 文件
   - 不要提交到 Git

### 对于企业用户

1. ✅ **仅使用本地部署**
   - 禁止远程模型调用
   - 内网运行

2. ✅ **启用数据库加密**
   - 保护索引数据
   - 符合数据保护法规

3. ✅ **审计和监控**
   - 记录所有操作
   - 定期安全审计

---

## 🔐 安全配置示例

### 最安全配置（推荐）

```ini
# .env - 最安全配置

# 仅使用本地模型
LOCAL_LLM_ENABLED=true
LOCAL_LLM_ENDPOINT=http://localhost:1234/v1

# 禁用远程模型
REMOTE_LLM_ENABLED=false
REMOTE_LLM_API_KEY=

# 隐私模式
PRIVACY_MODE=local_only
ALLOW_REMOTE_UPLOAD=false

# 本地数据库
DB_PATH=data/photo_index.db
```

### 混合配置（谨慎使用）

```ini
# .env - 混合配置

# 本地模型优先
LOCAL_LLM_ENABLED=true
LOCAL_LLM_ENDPOINT=http://localhost:1234/v1

# 远程模型（仅用于非敏感照片）
REMOTE_LLM_ENABLED=true
REMOTE_LLM_API_KEY=your-key

# 需要用户确认
REQUIRE_REMOTE_CONFIRM=true

# 路由模式
LLM_ROUTING_MODE=local_only
```

---

## ✅ 安全检查清单

- [ ] 已添加隐私模式选项
- [ ] 已添加远程传输确认
- [ ] 已创建 PRIVACY.md 文档
- [ ] 已将 .env 加入 .gitignore
- [ ] 已限制文件权限
- [ ] 已提供数据库加密选项
- [ ] 已提供路径脱敏选项
- [ ] 已添加审计日志
- [ ] 已测试本地模式完整性
- [ ] 已记录所有远程传输

---

## 📞 联系方式

如有隐私或安全问题，请联系：

**作者**: 北京老李（beijingLL）  
**项目**: PhotoIndexWithLLM

---

**隐私保护是我们的首要责任！** 🔒
