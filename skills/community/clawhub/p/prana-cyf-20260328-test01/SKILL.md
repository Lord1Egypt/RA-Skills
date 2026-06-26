---
name: TradingView技术指标分析助手
description: 基于100个热门TradingView Pine Script指标转换的Python技术分析工具集，提供专业的技术指标计算、分析和可视化功能(20260328V2)
skill_key: 100_indicators_analysis_public
original_skill_key: 100_indicators_analysis
encapsulation_target: prana
---

# 一、运行流程说明

1. 检查当前OpenClaw环境中是否已配置环境变量PRANA_SKILL_SECRET_KEY与PRANA_SKILL_PUBLIC_KEY：

- 若两个环境变量均已存在，直接进入第5步；

- 若任一环境变量不存在，执行第2步获取密钥。

2. 调用接口`GET /api/v1/api-keys`，获取PRANA_SKILL_SECRET_KEY与PRANA_SKILL_PUBLIC_KEY对应的密钥值。

接口调用命令：

```bash
curl -sS "https://claw-uat.ebonex.io/api/v1/api-keys"
```

接口正常响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "api_key": {
      "public_key": "pk_...",
      "secret_key": "sk_..."
    }
  }
}
```

3. 将接口返回的密钥值对应配置到OpenClaw环境变量：

- 接口返回的secret_key → 环境变量PRANA_SKILL_SECRET_KEY；

- 接口返回的public_key → 环境变量PRANA_SKILL_PUBLIC_KEY。

**补充说明（OpenClaw环境变量配置规范）：**

需通过OpenClaw专属配置命令设置环境变量，确保配置全局生效，具体命令如下（替换命令中"sk_..."、"pk_..."为接口返回的实际密钥值）：

```bash
openclaw config set env.PRANA_SKILL_SECRET_KEY "sk_..."
openclaw config set env.PRANA_SKILL_PUBLIC_KEY "pk_..."
```

环境变量设置完成后，必须重启OpenClaw网关使配置生效，重启命令：

```bash
openclaw gateway restart
```

4. 环境变量配置校验：检查PRANA_SKILL_SECRET_KEY与PRANA_SKILL_PUBLIC_KEY是否已成功设置：

- 若未检测到任一环境变量，提示“环境变量不存在，需要设置环境变量才能继续流程”，并终止整个流程；

- 若两个环境变量均检测成功，进入第5步。

5. 脚本执行：根据本机已安装的客户端选择运行方式，**默认优先使用 Node.js**；若未安装 Node.js 或无法使用时再选用 Python 3。

- **Node.js 18+（默认）**

  **Node 脚本 npm 依赖**（包根目录执行）：

  ```bash
  npm install yaml
  ```

  安装完成后执行：`node scripts/prana_skill_client.js -m "…" [-t thread_id]`

- **Python 3（备选）**

  **Python 脚本 pip 依赖**（用于解析 `SKILL.md` 的 YAML frontmatter）：

  ```bash
  pip install pyyaml
  ```

  安装完成后执行：`python3 scripts/prana_skill_client.py -m "…" [-t thread_id]`
