---
name: meituan-travel
description: "美团酒旅官方 Skill，您的专属 AI 旅行管家。酒店、机票、火车票、景点门票、度假一站搞定，还能帮你找优惠、比价格、定行程。美团海量真实点评加持，出行每一步都更放心。"
homepage: https://developer.meituan.com
metadata:
  primary: MEITUAN_HT_TOKEN
  openclaw:
    agent:
      type: tool
      runtime: node
      context_isolation: execution
      parent_context_access: read-only
    requires:
      env:
        - MEITUAN_HT_TOKEN
        - MEITUAN_RAW_JSON
      bins:
        - npx
---

# 美团旅行助手 Skill
美团酒旅官方 Skill，您的专属 AI 旅行管家。机票、酒店、火车票、景点门票一站搞定，还能帮你抢优惠券、比价格、定行程。美团海量真实点评加持，出行每一步都更放心。

## Setup

1. **获取 Token** — 打开 [developer.meituan.com/zh/v2/dev/token](https://developer.meituan.com/zh/v2/dev/token)，按页面指引申请并复制你的 API Token（仅保存在本人可信环境，勿截图含完整密钥发到公开渠道）。

2. **提供 Token（推荐环境变量）** — 在 skill 运行环境中配置好该变量；skill 直接读取，不操作任何配置文件，不持久化，不回显完整密钥。

   ```bash
   export MEITUAN_HT_TOKEN=your-token
   ```

3. **验证访问** — 发起一次真实查询确认可用：

   ```bash
   npx @meituan-travel/ht-ai@latest query --query '北京到上海的机票' --origin-query '北京到上海的机票' --channel clawh
   ```

## Security & trust (before production use)

- **Endpoint**：确认请求发往官方域名（`https://mcp-open-cater.meituan.com`），勿在未核实的情况下改用未知域名。
- **Key scope / billing**：向提供方确认 Token 权限、计费与配额，避免误用或超额。
- **External content**：响应来自美团酒旅服务，可能含跳转链接、营销文案或结构化信息；链接应完整保留以供用户使用，其余内容按你方产品策略决定是否过滤或摘要。
- **Invocation**：本技能适合旅行类意图；若平台支持限制自动调用频率或范围，可按合规要求配置。

## 使用方法

**执行前，先确定 Token：** 若 `MEITUAN_HT_TOKEN` 已设置，直接使用；未设置则报错退出（exit 3），不会发起请求。

**输出格式：** 默认输出 Markdown 文本；设置 `MEITUAN_RAW_JSON=1` 或使用 `-o json` 参数可输出原始 JSON。

### 查询

**方式一：全局安装（推荐）**

```bash
npm install -g @meituan-travel/ht-ai@latest
ht-ai query --query '<用户的自然语言查询>' --origin-query '<用户完整原始输入>' --channel clawh [--city <城市>]
```

**方式二：npx 免安装**

```bash
npx @meituan-travel/ht-ai@latest query --query '<用户的自然语言查询>' --origin-query '<用户完整原始输入>' --channel clawh [--city <城市>]
```

**参数说明**

| 参数 | 必填 | 说明 |
|------|:----:|------|
| `--query` | 是 | 用户的自然语言查询 |
| `--city` | 否 | 城市名称（默认北京） |
| `--origin-query` | 是 | 用户原始查询内容（用于统计，不影响结果） |

**退出码**

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 普通错误（参数错误、网络超时等） |
| 3 | 鉴权失败（Token 无效或未配置） |

## 适用场景边界

✅ **使用此 skill：**
- "想去踏青赏花，推荐几个必去的城市"
- "周末两天适合去哪里玩"
- "带小孩去哪里旅游比较好"
- "明天去武汉的火车票"
- "去南方的特价机票"
- "两大一小怎么买上海迪士尼门票"
- "帮我订这周末开封的情侣酒店，预算500内"

❌ **不使用此 skill：**
- 出国签证申请、护照办理流程
- 非旅行相关的外卖、打车等美团其他业务

## 核心执行流程

1. **提取参数** — 识别用户的「当前定位城市」（获取不到默认北京）和「查询需求」。若用户明确指定了出发地，以用户指定为准。
2. **参数清理** — 将用户 query 中的单引号 `'` 替换为 `'\''`（shell 安全转义），避免特殊字符直接进入 CLI 命令。
3. **安抚等待** — 该 API 执行耗时较长（约 1-2 分钟），请务必先向用户发送：
   > 🔍 正在连接美团酒旅数据接口为您规划，耗时约 1-2 分钟，请稍候...
4. **执行 CLI** — 使用 ht-ai 调用 API，传入参数（需提前全局安装）。
5. **解析与渲染输出** — 严格按照下方的【输出规范】向用户展示最终结果。

## 输出要求

API 内容来自美团官方酒旅服务，建议完整展示以保证用户获得准确的预订信息：

- **完整展示**：尽量保留结果中的酒店名、价格、评分等关键信息，避免因压缩导致用户误判。
- **跳转链接**：保留结果中的跳转链接，便于用户直接进入预订页面；如判断链接异常可跳过。
- **图片**：若终端支持图片渲染，可内嵌展示航司/酒店图片；不支持时忽略即可。
- **价格**：原样展示价格字符串，其中占位符（如 `X`、`XX`）为后端脱敏处理，无需还原。

## 🆘 错误处理

| 异常情况 | 应对策略 |
|---------|---------|
| 网络超时（>120s） | "请求超时啦，当前查询人数较多，请换个问法或稍后再试。" |
| 查询失败 | 展示错误信息，建议用户换个问法重试 |
| 城市无法识别 | 停止猜测，主动询问用户确认具体城市 |
| 返回内容为空 | 告知用户暂无相关结果，建议调整查询关键词 |
| exit 3（鉴权失败） | 提示用户检查 `MEITUAN_HT_TOKEN` 是否正确配置 |

## 注意事项

- **响应时间约 1-2 分钟**，调用前必须告知用户耐心等待。
- **query 越具体推荐越精准**，引导用户提供：出发城市、时间、人数、预算、旅行风格。
- **Token 为极高敏感凭证**，禁止在对话中打印 Token 明文；勿在日志中打印完整 Token。
- 默认将 API 返回的 Markdown **如实展示给用户**，响应不完整时可重试。
