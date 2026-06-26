# Omni-X - X (Twitter) 技能库

一个为 AI 代理提供的技能项目，用于提取 X (Twitter) 数据，包括帖子、关注者、关注列表、个人资料详情和媒体内容。

## 🙏 致谢

本项目基于 [TweeterPy](https://github.com/iSarabjitDhiman/TweeterPy) 构建 - 这是一个优秀的 Python 库

**特别感谢 [@iSarabjitDhiman](https://github.com/iSarabjitDhiman)** 创建和维护 TweeterPy，使本项目成为可能。TweeterPy 提供了以下核心功能：
- 提取推文和用户资料
- 访问关注者和关注列表数据
- 搜索推文和提取媒体
- 处理 Twitter 身份验证

Omni-X 中的所有 Twitter 数据提取功能都由 TweeterPy 提供支持。我们感谢开源社区和 TweeterPy 团队所做的出色工作。

**TweeterPy 仓库：** https://github.com/iSarabjitDhiman/TweeterPy

## 功能特性

- 提取推文
- 提取用户关注者
- 提取用户关注列表
- 提取用户资料详情
- 提取 Twitter 个人资料媒体
- 按查询搜索推文

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 直接使用

```python
from scripts import TwitterSkills

# 初始化技能库
twitter = TwitterSkills()

# 提取用户资料
profile = twitter.get_user_profile("username")

# 提取推文
tweets = twitter.get_user_tweets("username", count=10)

# 提取关注者
followers = twitter.get_user_followers("username", count=20)

# 提取关注列表
followings = twitter.get_user_followings("username", count=20)

# 提取媒体
media = twitter.get_user_media("username", count=10)
```

### AI 代理使用（推荐）

`TwitterSkillInterface` 提供了一个标准化接口，AI 代理可以使用它来动态发现和执行技能：

```python
from scripts import TwitterSkillInterface

# 初始化接口
interface = TwitterSkillInterface()

# 发现可用技能
skills = interface.get_available_skills()
# 返回：包含技能名称、描述、参数和返回类型的字典

# 执行技能
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 5}
)

# 结果格式：
# {
#     "success": True/False,
#     "data": [...],
#     "count": 5,
#     "skill_name": "get_user_tweets",
#     "parameters": {"username": "elonmusk", "count": 5}
# }
```

### AI 代理可用技能

1. **get_user_profile** - 提取用户资料信息
2. **get_user_tweets** - 提取用户最近的推文
3. **get_user_followers** - 提取用户的关注者列表
4. **get_user_followings** - 提取用户的关注列表
5. **get_user_media** - 从用户推文中提取媒体
6. **search_tweets** - 按查询搜索推文

## 文档

### AI 代理文档
- **[SKILL.md](SKILL.md)** - 核心技能定义和使用指南（AI 代理入口点）（英文）
- **[references/AI_AGENT_GUIDE.md](references/AI_AGENT_GUIDE.md)** - AI 代理完整 API 参考（英文）
- **[agent_example.py](agent_example.py)** - AI 代理集成示例代码

### 通用文档
- **[references/LOGIN_GUIDE.md](references/LOGIN_GUIDE.md)** - 身份验证和登录说明（英文）
- **[references/INSTALLATION.md](references/INSTALLATION.md)** - 安装和使用指南（英文）

## 示例

运行示例脚本：

```bash
# AI 代理接口示例
python agent_example.py
```

## 系统要求

- Python 3.7+
- tweeterpy

## ⚠️ 免责声明和使用条款

**本项目仅供教育和研究目的使用。**

使用本工具即表示您同意：

1. **遵守 X (Twitter) 服务条款**：您有责任确保使用本工具符合 [X (Twitter) 服务条款](https://twitter.com/tos) 和 [开发者协议](https://developer.twitter.com/en/developer-terms/agreement-and-policy)。

2. **尊重速率限制**：在请求之间实施适当的延迟，避免对 X (Twitter) 服务器造成过大压力。过度请求可能导致您的账户被临时或永久限制。

3. **负责任地使用**：
   - 不要将此工具用于垃圾信息、骚扰或任何恶意活动
   - 尊重用户隐私和数据保护法规（GDPR、CCPA 等）
   - 仅提取公开可用的数据
   - 未经适当授权，不得重新分发或出售提取的数据

4. **无担保**：本工具按"原样"提供，不提供任何担保。作者对使用本工具产生的任何后果不承担责任。

5. **账户风险**：使用自动化数据提取工具可能违反 X (Twitter) 的条款，并可能导致账户被暂停。使用风险自负。

**推荐的最佳实践：**
- 实施速率限制（例如，请求之间延迟 1-2 秒）
- 使用合理的请求数量（从小开始，逐步增加）
- 缓存结果以最小化重复请求
- 监控您的账户是否有任何警告或限制

## 登录要求

某些功能需要 Twitter 身份验证：

**无需登录即可使用（访客会话）：**
- get_user_profile
- get_user_tweets

**需要登录：**
- get_user_followers
- get_user_followings
- get_user_media
- search_tweets

详细登录说明请参阅 [references/LOGIN_GUIDE.md](references/LOGIN_GUIDE.md)（英文）。

## 为什么使用技能接口？

`TwitterSkillInterface` 专为 AI 代理设计：

- **动态发现**：代理可以查询可用技能及其参数
- **标准化执行**：所有技能使用相同的 `execute_skill()` 方法
- **结构化响应**：一致的响应格式，包含元数据
- **错误处理**：优雅的错误处理，提供信息丰富的消息
- **可扩展性**：无需更改接口即可轻松添加新技能

## 许可证

请参阅 [LICENSE](LICENSE) 文件了解详情。
