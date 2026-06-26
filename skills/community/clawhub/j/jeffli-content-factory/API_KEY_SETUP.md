# GLM API Key 设置指南

## 快速开始

### 步骤 1：获取 API Key

1. 访问智谱 AI 开放平台：https://open.bigmodel.cn/
2. 注册/登录账号
3. 进入控制台 → API Keys
4. 创建新的 API Key 并复制

### 步骤 2：设置 API Key

有 **3 种方式** 可以设置 API Key，选择最适合你的：

---

## 方式 1：使用 .env 文件（推荐）✅

**优点**：
- 项目级配置，不影响系统
- 易于管理和版本控制（记得添加到 .gitignore）
- 脚本自动加载

**步骤**：

1. **复制示例文件**：
   ```bash
   cd C:\Users\jeffl\.claude\skills\content-factory
   copy .env.example .env
   ```

2. **编辑 .env 文件**：
   ```bash
   notepad .env
   ```

3. **替换 API Key**：
   ```
   GLM_API_KEY=your-actual-api-key-here
   ```
   将 `your-actual-api-key-here` 替换为你从智谱 AI 获取的真实 API Key

4. **保存文件**

5. **验证配置**：
   ```bash
   python scripts/check_env.py
   ```

**示例 .env 文件**：
```env
# GLM-Image API Configuration (Required)
# Get your API key from: https://open.bigmodel.cn/
GLM_API_KEY=sk-1234567890abcdef1234567890abcdef

# WeChat Official Account Credentials (Optional - for auto-publishing)
# Get these from: https://mp.weixin.qq.com/
WECHAT_APP_ID=wxf9400829e3405317
WECHAT_APP_SECRET=a6800143c01df2e73121c631cac4ec32
```

**说明**：
- `GLM_API_KEY`：**必需**，用于生成封面图
- `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET`：**可选**，用于自动发布到微信公众号
  - 如果不配置，仍然可以生成文章和封面图，只是无法自动发布
  - 从微信公众平台获取：https://mp.weixin.qq.com/ → 设置与开发 → 基本配置

---

## 方式 2：系统环境变量（永久）

**优点**：
- 全局可用，所有项目共享
- 重启后仍然有效

**Windows 图形界面设置**：

1. 按 `Win + R`，输入 `sysdm.cpl`，回车
2. 点击"高级"标签
3. 点击"环境变量"按钮
4. 在"用户变量"区域点击"新建"
5. 输入：
   - 变量名：`GLM_API_KEY`
   - 变量值：你的 API Key
6. 点击"确定"保存
7. **重启终端**使其生效

**Windows PowerShell 设置**：
```powershell
[System.Environment]::SetEnvironmentVariable('GLM_API_KEY', 'your-api-key-here', 'User')
```

**验证**：
```powershell
echo $env:GLM_API_KEY
```

---

## 方式 3：临时环境变量（当前会话）

**优点**：
- 快速测试
- 不影响系统配置

**缺点**：
- 关闭终端后失效
- 每次都需要重新设置

**PowerShell**：
```powershell
$env:GLM_API_KEY="your-api-key-here"
```

**CMD**：
```cmd
set GLM_API_KEY=your-api-key-here
```

**Git Bash / WSL**：
```bash
export GLM_API_KEY="your-api-key-here"
```

**验证**：
```bash
echo $GLM_API_KEY
```

---

## 验证配置

### 方法 1：使用检查脚本
```bash
cd C:\Users\jeffl\.claude\skills\content-factory
python scripts/check_env.py
```

**期望输出**：
```
============================================================
🔑 Environment Configuration Checker
============================================================

📄 Loading environment from: C:\Users\jeffl\.claude\skills\content-factory\.env
   ✅ GLM_API_KEY = sk-1234567...

🔍 Checking required API keys...
   ✅ GLM_API_KEY: Set (GLM-Image API (required for cover generation))
   ⚠️  WECHAT_APP_ID: Not set (WeChat Official Account (optional))
   ⚠️  WECHAT_APP_SECRET: Not set (WeChat Official Account (optional))

============================================================
✅ All required API keys are configured!
   You can now use the cover photo generation script.
============================================================
```

### 方法 2：直接测试生成
```bash
python scripts/generate_cover_photo.py \
  --title "测试文章" \
  --theme "测试主题" \
  --output "output/test-cover.png"
```

如果配置正确，应该能成功生成封面图。

---

## 故障排除

### 问题 1：找不到 API Key

**错误信息**：
```
❌ Error: GLM API key required!
   Set GLM_API_KEY environment variable or use --api-key argument
```

**解决方案**：
1. 检查 .env 文件是否存在且包含正确的 API Key
2. 检查环境变量是否设置：`echo $env:GLM_API_KEY` (PowerShell)
3. 尝试使用 `--api-key` 参数直接传递：
   ```bash
   python scripts/generate_cover_photo.py \
     --api-key "your-api-key-here" \
     --title "测试" \
     --theme "测试" \
     --output "test.png"
   ```

### 问题 2：.env 文件不生效

**可能原因**：
- .env 文件位置不对（应该在 content-factory 根目录）
- 文件名错误（应该是 `.env`，不是 `.env.txt`）
- 文件编码问题（应该是 UTF-8）

**解决方案**：
```bash
# 检查文件位置
cd C:\Users\jeffl\.claude\skills\content-factory
dir .env

# 查看文件内容
type .env

# 重新创建
copy .env.example .env
notepad .env
```

### 问题 3：API Key 无效

**错误信息**：
```
❌ API request failed: 401 Unauthorized
```

**解决方案**：
1. 确认 API Key 是否正确复制（没有多余空格）
2. 检查 API Key 是否已激活
3. 登录智谱 AI 平台确认 API Key 状态
4. 如果过期，重新生成新的 API Key

---

## 安全建议

### ⚠️ 重要：保护你的 API Key

1. **不要提交到 Git**：
   ```bash
   # 确保 .env 在 .gitignore 中
   echo .env >> .gitignore
   ```

2. **不要分享**：
   - 不要在公开场合展示 API Key
   - 不要截图包含 API Key 的配置
   - 不要通过不安全的渠道传输

3. **定期轮换**：
   - 定期更换 API Key
   - 如果怀疑泄露，立即重新生成

4. **使用环境变量**：
   - 不要在代码中硬编码 API Key
   - 使用 .env 文件或系统环境变量

---

## 推荐配置方式

**开发环境**：使用 .env 文件（方式 1）
- 灵活，易于管理
- 不同项目可以使用不同的 Key

**生产环境**：使用系统环境变量（方式 2）
- 更安全
- 集中管理

**快速测试**：使用临时环境变量（方式 3）
- 快速验证
- 不影响其他配置

---

## 下一步

配置完成后，你可以：

1. **测试生成功能**：
   ```bash
   python scripts/test_cover_generation.py
   ```

2. **生成实际封面**：
   ```bash
   python scripts/generate_cover_photo.py \
     --title "你的文章标题" \
     --theme "文章主题" \
     --output "output/cover.png"
   ```

3. **查看完整文档**：
   - `scripts/COVER_PHOTO_GUIDE.md` - 详细使用指南
   - `scripts/WECHAT_COVER_UPDATE.md` - 功能更新说明

---

**需要帮助？**
- 查看智谱 AI 文档：https://open.bigmodel.cn/dev/api
- 运行检查脚本：`python scripts/check_env.py`
- 查看错误日志获取详细信息
