---
name: meituan-coupon-auto
description: "自动领取美团优惠券。触发词: 领取美团优惠券, 运行美团优惠券技能, 设置每日自动领取, 查看优惠券, meituan coupon, 美团领券"
metadata:
  {
    "openclaw": {
      "emoji": "🛵",
      "requires": {}
    }
  }
---

# 美团优惠券自动领取

自动浏览器领取美团全部优惠券，**两次点击**解锁券明细弹窗，直接读取张数/总金额/分类明细。

## 验证数据
- 69张券，800元（2026-03-16 实测）
- 两次点击策略：第1次触发领取→页面跳转，第2次触发明细弹窗
- 覆盖：外卖神券 + 闪购券 + 堂食券 + 玩乐变美 + 生活服务

## 触发词
- "领取美团优惠券" / "美团领券" — 立即领取
- "运行美团优惠券技能" / "meituan coupon" — 运行技能
- "设置每日自动领取" — 设置定时任务
- "查看优惠券" — 查看今日领取记录

## 执行流程（5步）

### 步骤1：启动浏览器

```
browser(action=status, profile=openclaw)
# 未运行则先 start
browser(action=start, profile=openclaw)
```

### 步骤2：打开领券页（不等完整加载）

```
browser(action=open, profile=openclaw, url="https://click.meituan.com/t?t=1&c=2&p=mcB9ObxznZMn")
```

### 步骤3：等待页面就绪 + 第一次点击（触发领取）

等待2秒后执行第一次点击：

```
browser(action=act, kind=wait, timeMs=2000)
browser(action=act, kind=evaluate, fn="document.querySelector('.gundam-view.receive-btn, .receive-btn, [class*=\"receive-btn\"]')?.click()")
```

### 步骤4：等待页面跳转 + 第二次点击（触发明细弹窗）

等待2秒（等待页面跳转至 market.waimai.meituan.com），再点击一次触发明细弹窗：

```
browser(action=act, kind=wait, timeMs=2000)
browser(action=act, kind=evaluate, fn="document.querySelector('.gundam-view.receive-btn, .receive-btn, [class*=\"receive-btn\"]')?.click()")
```

### 步骤5：等待明细出现 + 读取快照 + 解析 + 关闭

```
browser(action=act, kind=wait, timeMs=2000)
browser(action=snapshot, profile=openclaw, compact=true)
→ 在快照中查找 "共X张券" / "总计Y元已到账" / 各优惠券明细
browser(action=stop, profile=openclaw)
```

## 快照解析规则

领取成功后，快照顶部会出现明细弹窗，格式如下：

```
共 69 张券, 总计 800 元已到账
¥17 满58可用 今日有效 外卖大额神券
¥12 满34可用 今日有效 外卖神券
¥5 满25可用 今日有效 闪购零食神券
...
```

解析逻辑（用 JS 或 regex 均可）：

```javascript
// 从 snapshot text 提取汇总
const summary = text.match(/共\s*(\d+)\s*张券.*?总计\s*(\d+)\s*元已到账/);
// coupons = summary[1], totalValue = summary[2]

// 提取每张券明细（格式：¥金额 满X可用 有效期描述 类型名称）
const itemRe = /¥\s*(\d+)\s+(满\d+可用\s+)?(今日有效|有效期至[\d.]+|明日[\d:]+截止)\s+(.+)/g;
let m, items = [];
while ((m = itemRe.exec(text)) !== null) {
  items.push({ value: parseInt(m[1]), condition: m[2]?.trim() || '', validity: m[3], name: m[4].trim() });
}
```

## 输出格式（最终回复用户）

```
🛵 美团优惠券领取成功

📊 共 69 张券，总计 ¥800 已到账

🛵 外卖神券（今日有效）
  ¥17 满58可用 · 外卖大额神券
  ¥15 满38可用 · 外卖大额神券
  ¥12 满34可用 · 外卖神券

🛒 闪购券（今日有效）
  ¥35 满99可用 · 松鼠坚果
  ¥29 满109可用 · 闪购酒饮
  ... (其余汇总)

🍽️ 堂食/生活（至本周）
  ¥30 满300可用 · 堂食膨胀神券
  ...

⏱ 2026-03-16 13:18 | 今日有效券请尽快使用
```

## 状态检测

| 状态 | 识别关键词 | 处理 |
|------|-----------|------|
| ✅ 成功 | `共X张券.*总计Y元已到账` | 解析明细输出 |
| ⚠️ 需打开App | `请打开美团App继续查看` | 执行第二次点击 |
| 🔐 需登录 | `请输入手机号` / `登录` | 提示手动登录后重试 |
| ✋ 已领取 | `剩余 0 次` / `已领取` | 回复"今日已领过" |
| 🔥 太火爆 | `太火爆` | 提示30分钟后重试 |

## 选择器降级顺序

| 优先级 | 选择器 | 说明 |
|--------|--------|------|
| 1 | `.gundam-view.receive-btn.vyx6l` | 精确class（常用） |
| 2 | `.receive-btn` | 模糊class |
| 3 | `[class*="receive-btn"]` | 更宽松 |
| 4 | `innerText === '立即领取'` | 文本降级 |

## 定时任务（每天 10:00 & 13:18）

```json
{
  "name": "美团每日领券",
  "schedule": { "kind": "cron", "expr": "18 13 * * *", "tz": "Asia/Shanghai" },
  "payload": { "kind": "systemEvent", "text": "⏰ 定时提醒：领取美团优惠券" },
  "sessionTarget": "main",
  "delivery": { "mode": "none" }
}
```

> ⚠️ 必须使用 `sessionTarget: "main"` + `payload.kind: "systemEvent"`。
> 使用 `isolated` + `announce` 在无外部渠道（Telegram/Discord）时会报错：
> `Channel is required (no configured channels detected)`

## 领券页面地址

```
https://click.meituan.com/t?t=1&c=2&p=mcB9ObxznZMn
```
覆盖：外卖神券 · 闪购券 · 堂食券 · 玩乐变美 · 生活服务 · 医疗 · 超市

---

> 📋 实测记录（2026-03-16）：
> - [x] 两次点击策略验证：第1次→页面跳转至 market.waimai.meituan.com，第2次→明细弹窗出现
> - [x] 成功读取：69张券 / ¥800 / 含外卖、闪购、堂食、玩乐变美等分类
> - [x] 每次点击后 wait 2000ms 确保页面稳定
> - [x] compact snapshot 可清晰读取券明细列表
