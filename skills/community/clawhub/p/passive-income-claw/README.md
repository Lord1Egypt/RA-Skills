# Passive Income Claw

Binance 被动收益 AI 助手。自动扫描理财机会，按你的偏好筛选推送，在授权范围内执行申购。

## 安装

```bash
clawhub install passive-income-claw
```

## 配置 API Key

1. 在 [Binance](https://www.binance.com/en/my/settings/api-management) 创建 API Key，权限设置：

| 权限 | 开启 |
|------|------|
| 读取（余额/持仓/历史） | ✅ |
| 理财操作（Earn） | ✅ |
| 杠杆（Margin） | ✅ 如果要用借贷套利 |
| 现货交易 | ❌ |
| 合约 / 期货 | ❌ |
| 提币 | ❌ 绝对不开 |
| IP 白名单 | ✅ 绑定 OpenClaw 运行 IP |

2. 编辑 `~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "entries": {
      "passive-income-claw": {
        "enabled": true,
        "env": {
          "BINANCE_API_KEY": "你的key",
          "BINANCE_API_SECRET": "你的secret"
        }
      }
    }
  }
}
```

## 开始使用

对 OpenClaw 说以下任意一句：

- `/passive-income`
- "帮我设置被动收益"
- "help me set up passive income"

系统会通过对话问你 3 个偏好问题和 5 个授权配置，然后立刻跑一次扫描展示推荐。

## 设置自动扫描

setup 结束后，执行以下命令注册定时任务：

```bash
openclaw cron add \
  --name "passive-income-scan" \
  --cron "0 1,5,9,13,17,21 * * *" \
  --message "Run passive income scan" \
  --session isolated
```

每 4 小时扫描一次，只在有变化时推送。

## 日常用法

| 你说 | 系统做什么 |
|------|----------|
| "现在有什么适合我的机会？" | 获取产品列表，按你的偏好分析推荐 |
| "帮我买第 1 个" | 授权校验 → 币种换算 → 执行申购 → 记录 |
| "帮我买第 1 个，500 USDT" | 同上，指定金额 |
| "赎回 BNB 活期" | 执行赎回 |
| "我没有 USDT，怎么参与那个 8.2% 的？" | 分析借贷套利路径（用你的持仓做抵押借入 USDT） |
| "把单次上限改成 1000" | 更新授权配置 |
| "看看执行记录" | 展示历史操作 |
| （什么都不说，auto 模式） | 定时扫描 → 发现机会 → 自动申购 → 推送结果 |

## 两种运行模式

### confirm-first（默认）

```
扫描 → 推送推荐 → 你决定要不要买 → 你说"买" → 执行
```

### auto

```
扫描 → 发现匹配机会 → 直接申购 → 推送执行结果
```

切换方式：对 OpenClaw 说"改成自动模式"或"改成手动确认模式"。

## 安全机制

- **5 步授权硬校验**：开关、单次上限、日累计上限、操作类型白名单、资产白名单
- 所有校验在 TypeScript 脚本中执行，不依赖 AI 做算术
- 每日累计额度自动重置
- 失败操作不扣额度
- 不提币、不做合约/期货
- 借贷套利有保底安全线：净收益 < 2% 不推荐，margin level < 2.0 不执行

## 数据文件

| 文件 | 内容 |
|------|------|
| `~/passive-income-claw/user-profile.md` | 偏好 + 授权配置 + 每日计数器 |
| `~/passive-income-claw/snapshot.md` | 上次扫描的产品快照 |
| `~/passive-income-claw/execution-log.md` | 所有执行历史 |

纯文本，可直接查看或编辑。

## 卸载

```bash
clawhub update passive-income-claw --remove
rm -rf ~/passive-income-claw  # 可选：删除数据文件
```
