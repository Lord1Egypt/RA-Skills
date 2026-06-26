# Panda Data Skill（panda_data）安装指南

本文面向 **OpenClaw** 及需要在编程环境中使用 **PandaAI 金融数据** 的用户，结构与常见 Skills 安装说明（可参考 [Tushare Skills 安装指南](https://tushare.pro/document/1)）一致，便于对照操作。

---

## Skills 是什么

在 OpenClaw 生态中，**Skills** 是一种能力扩展方式，可以理解为给 AI 助手增加的「领域扩展包」：

- **专注领域**：例如本 Skill 面向股票、指数、期货、财务与因子等金融数据查询。
- **内置约定**：`SKILL.md` 中说明了调用规则、日期与代码格式、必须先完成认证等。
- **与运行时代码分离**：Skill 压缩包主要包含说明文档与辅助脚本；**Python 可执行库需单独通过 pip 安装**（见下文步骤 2）。

为便于大模型稳定调用 PandaAI 接口，**请同时完成：安装 Skill → 安装 SDK 与工具包 → 配置账号凭证**。

---

## 安装与准备

### 步骤 1：安装 Panda Data Skill

#### 在 OpenClaw 里通过 ClawHub 安装

若已在 [ClawHub](https://clawhub.com)（或你环境提供的等价命令）发布/收录本技能，一般形式为：

```bash
# 使用 clawhub 安装（技能在 ClawHub 上的名称为 panda-data-skill）
clawhub install panda-data-skill

# 升级
clawhub update panda-data-skill
```

也可在 OpenClaw 对话中让助手安装，例如提示：**请安装最新版 Panda Data skill，名称为 panda-data-skill**（若平台展示名称略有差异，以 ClawHub 为准）。

若线上安装失败（如限流、网络问题），可使用 **离线 zip**：将技能包 zip 下载到本地后，在 OpenClaw 中按平台说明导入该 zip，或通过对话提示「安装某目录下的 xxx.zip Skills」。

> **说明**：ClawHub 下载的 skill **通常只含** `SKILL.md`、`README.md`、`api_reference.md`、`scripts/` 等，**不包含** `panda_tools` 源码，步骤 2 必须执行。

---

### 步骤 2：安装 Python 依赖（panda_data + panda-data-tools）

大模型或脚本实际调数据时，需要：

| 组件 | 作用                                                                                                           |
|------|--------------------------------------------------------------------------------------------------------------|
| **panda_data** | PandaAI 官方 Python SDK（一般 `pip install panda_data`                                                            |
| **panda-data-tools** | 本项目的 PyPI 包名，`pip install panda-data-tools`提供 `panda_tools` 模块（`ToolRegistry`、`CredentialManager`、各 tool 封装） |

**2.1 安装 PandaAI SDK（panda_data）**

```bash
pip install panda_data
```

**2.2 安装 panda-data-tools**

若已在 [PyPI](https://pypi.org/) 发布：

```bash
pip install panda-data-tools
```

建议使用 **Python 3.12+**，并在虚拟环境中操作。

---

### 步骤 3：获取 PandaAI 账号凭证
官网账号注册：https://www.pandaai.online

PandaAI 数据接口使用 **86手机号+ 密码** 登录（该账号密码与PandaAI官网账号密码相同）

- 可用的 **用户名**
- 对应的 **密码**

请妥善保管，不要提交到公开仓库或聊天记录的公开频道。

---

### 步骤 4：配置凭证

**方式 A：环境变量（推荐脚本/服务）**

```bash
export PANDA_DATA_USERNAME="86+你的手机号"
export PANDA_DATA_PASSWORD="你的密码"
```

**方式 B：`.env` 文件（与 python-dotenv 配合）**

在运行时的**当前工作目录**或其**上级目录**放置 `.env`（`panda-data-tools` 会向上查找并加载，且默认**不覆盖**已在 shell 中设置的变量）：

```env
PANDA_DATA_USERNAME=86+你的手机号
PANDA_DATA_PASSWORD=你的密码
```

**方式 C：在 OpenClaw 里**

将用户名与密码（或说明已写入环境变量 / `.env`）告知助手，请其在**安全前提下**协助写入环境或配置文件，并提醒勿泄露。

**方式 D：代码中显式传入**

```python
from panda_tools.credential import CredentialManager

CredentialManager.init_with_credentials("86+手机号", "密码")
```

---

### 步骤 5：验证是否可用

```python
from panda_tools.credential import CredentialManager
from panda_tools.registry import ToolRegistry

CredentialManager.init_from_env()
registry = ToolRegistry()
result = registry.call_tool(
    "get_market_data",
    start_date="20250101",
    end_date="20250110",
    symbol="000001.SZ",
)
print(result)
```

或使用 skill 包内脚本（需已安装 `panda-data-tools` 且路径正确）：

```bash
python scripts/call_tool.py get_market_data start_date=20250101 end_date=20250110 symbol=000001.SZ
```

---

## 常见问题

| 现象 | 处理思路 |
|------|----------|
| `panda_tools 未安装` | 执行 `pip install panda-data-tools`|
| `panda_data` 相关导入失败 | 先执行 `pip install panda_data`|
| 认证失败 / 客户端未初始化 | 检查环境变量或 `.env`，并先调用 `CredentialManager.init_from_env()` |
| ClawHub 里只有几个 md/py 文件 | 正常；可执行代码在 pip 包中，不是 skill zip 缺文件 |

---

## 更多文档

- 技能规则与 API 摘要：`SKILL.md`
- 参数与接口说明：`api_reference.md`
- 变更记录：`CHANGELOG.md`
- 开源仓库：`SKILL.md` 中 `homepage` 字段

---

*文档版本与 skill 版本同步维护；若与 PandaAI 官方说明冲突，以官方为准。*
