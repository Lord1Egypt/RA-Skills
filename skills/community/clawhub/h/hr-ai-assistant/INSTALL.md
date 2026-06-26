# 快速安装指南

欢迎使用 HR AI Assistant Skill! 本指南将帮助你在 5 分钟内完成配置。

## 🚀 快速开始 (3 步配置)

### 第 1 步: 获取免费 API Key

访问: **https://ai.hrrule.com/**

1. 注册/登录账号
2. 在个人中心申请 API Key
3. **完全免费,申请后立即可用**

### 第 2 步: 配置 API Key (3 种方式任选其一)

#### 方式 A: 使用配置脚本 (推荐，小白友好)

运行配置脚本，交互式配置 API Key：

```bash
python ~/.workbuddy/skills/hr-ai-assistant/scripts/config_api_key.py
```

配置脚本会：
- 自动检测 API Key 格式
- 支持粘贴完整文本（会自动提取）
- 保存到配置文件
- 显示当前配置状态

**优势**：
- ✅ 最简单，无需手动编辑文件
- ✅ 自动检测 API Key 格式
- ✅ 支持多种 API Key 格式
- ✅ 交互式操作，小白友好

#### 方式 B: 设置环境变量

```bash
# Linux/Mac
export HRRULE_API_KEY='your-api-key'

# Windows PowerShell
$env:HRRULE_API_KEY='your-api-key'

# Windows CMD
set HRRULE_API_KEY=your-api-key
```

#### 方式 C: 编辑配置文件

编辑 `config.json`:

```json
{
  "api_key": "your-api-key",
  "model": "deepseek-ai/DeepSeek-R1",
  "timeout": 120,
  "verbose": true
}
```

#### 方式 D: 创建 .env 文件

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件,填入你的 API Key
```

### 第 3 步: 安装依赖

```bash
pip install python-socketio aiohttp
```

## ✅ 测试安装

运行测试命令:

```bash
python scripts/call_hrrule_api.py \
    --content "财务公司 需要招聘 社保专员,帮我生成一份 招聘JD" \
    --tag-id 4 \
    --rt "招聘JD"
```

如果看到生成的招聘JD,说明配置成功!

## 💡 常见问题

### Q: 提示"未找到有效的 API Key"

**A:** 请确认:
1. 已在 https://ai.hrrule.com/ 申请 API Key
2. 已配置环境变量、config.json 或 .env 文件
3. API Key 已正确填写,没有占位符

### Q: 连接超时

**A:** 请检查:
1. 网络连接是否正常
2. 能否访问 `wss://ai.hrrule.com`
3. 防火墙是否阻止 WebSocket 连接

### Q: 编码错误 (Windows)

**A:** 脚本已内置 UTF-8 编码支持,如果仍有问题,请确保终端使用 UTF-8 编码。

## 📚 详细文档

- **README.md** - 完整使用指南
- **SKILL.md** - 技能文档
- **USAGE_GUIDE.md** - 详细使用说明

## 🆘 需要帮助?

如有问题,请访问: https://ai.hrrule.com/

---

**配置完成后,即可享受免费的 HR AI 服务!** 🎉
