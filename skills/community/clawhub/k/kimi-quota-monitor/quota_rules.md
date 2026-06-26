# Kimi 额度监控规则参考

## 页面信息

- **额度页面**: `https://www.kimi.com/membership/subscription`
- **登录方式**: Playwright headless Chrome + cookies + localStorage (access_token/refresh_token)

## 抓取策略

额度百分比显示在会员页面，需要通过以下步骤获取：

1. 启动 Playwright `chromium.launch(channel='chrome', headless=True)`
2. 创建新 context，设置 `device_scale_factor=1`
3. 打开页面后注入 cookies（来自 `kimi_cookies.json`）
4. 注入 localStorage：`access_token`、`refresh_token`、`msh_user_id`
5. 刷新页面等待加载完成
6. 页面加载完成后提取额度信息
7. 关闭浏览器

## 周期计算规则

- **重置日期**: 每月 22 日（可修改脚本中的 `get_cycle_info` 逻辑调整）
- **每月总天数**: 当前月份的天数（28/29/30/31）
- **每日基准额度**: `100% / 月总天数`
- **KimiClaw 沙箱预估消耗**: 每天 0.6%

### 计算公式

```
已过天数 = 今天日期 - 22（如果今天 >= 22）
        或 今天日期 + (上月总天数 - 22)（如果今天 < 22，跨周期）

每日计划额度 = (已过天数) × (100 / 月总天数)

原始差额 = 每日计划额度 - 实际已用百分比

KimiClaw 预估 = 剩余天数 × 0.6%

显示差额 = max(原始差额 - KimiClaw预估, 0)
显示 KimiClaw = max(KimiClaw预估 - 原始差额, 0)  [为0时隐藏]
```

## 消息模板（实际推送格式）

```
📊 Kimi 额度日报 · 04.30

周期：04.22 – 05.21（共30天）
进度：[████████░░] 17.1%

📌 截止今日：
   累计计划：15.00%
   累计实际：17.06%
   差   额：+0.00%
   KimiClaw预估：+7.2%

💰 剩余总额度：82.94%
```

## 环境依赖

- `playwright` Python 包
- 系统 Chrome 浏览器（`google-chrome` 或 `chromium`）
- `openclaw` CLI（用于微信推送）

## 状态文件

- `kimi_cookies.json` — Kimi 登录 cookies（用户自行导出配置）
- `kimi_quota.log` — 运行日志
