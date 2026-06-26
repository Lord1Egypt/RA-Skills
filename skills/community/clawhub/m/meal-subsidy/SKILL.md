---
name: meal-subsidy
description: 2号人事部餐补申请自动化 — 读考勤判断下班时间，全自动填表提交。触发方式："申请餐补"查昨天；"申请4月7日餐补"查指定日期；"申请4月餐补"查整月批量申请；"本周餐补"查本周批量申请。
---

# 餐补申请自动化

自动读取2号人事部考勤，判断下班时间是否满足餐补条件，全自动填写并提交。

## 申请条件

| 下班时间 | 餐补 |
|---------|------|
| ≥ 20:30 | 20元 |
| 00:00 ~ 06:00（跨天） | 40元 |
| 其他 | 不申请 |

**跨天**：结束时间日期+1天（如 00:30 → 第二天00:30）

---

## 触发指令

| 指令 | 效果 |
|------|------|
| "申请餐补" | 查昨天，满足则申请 |
| "申请4月7日餐补" | 查指定日期（默认当年，如2026年4月7日）|
| "申请4月餐补" | 查整个4月（默认当年），批量申请所有满足条件的日期 |
| "本周餐补" | 批量申请本周所有满足条件的日期 |

---

## 快速开始

### 第一步：安装依赖

```bash
pip install playwright
playwright install chromium
```

> 只需安装一次。依赖 Playwright 而非 Selenium，无需额外配置 ChromeDriver。

### 第二步：启动 Chrome 远程调试（只需一次）

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

> Mac：`/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222`

打开后扫码登录 `https://i-wework.2haohr.com/desk/home`，之后运行无需重复登录。

> 如果脚本报错 "Cannot connect to Chrome"，先执行此步骤

### 第三步：运行脚本

```bash
# 申请指定日期（默认昨天）
py -3 meal_subsidy.py --date 2026-04-07

# 申请整月（批量）
py -3 meal_subsidy.py --mode month --year 2026 --month 4
```

---

## 截图说明

| 文件 | 内容 |
|------|------|
| `screenshots/att_YYYYMMDD.png` | 考勤截图（上传用） |
| `screenshots/meal_form_*.png` | 餐补表单截图 |
| `screenshots/meal_before_submit_*.png` | 提交前确认 |
| `screenshots/after_submit_*.png` | 提交后截图 |
| `screenshots/late_YYYYMM.csv` | 申请记录表 |

---

## 依赖

| 依赖 | 说明 |
|------|------|
| Python 3.8+ | 语言环境 |
| playwright | `pip install playwright` |
| Chrome 浏览器 | 系统已安装即可 |

---

## 常见问题

**Q: 报错 "Cannot connect to Chrome"**
A: Chrome 没有以远程调试模式启动。按第二步重新启动 Chrome。

**Q: 提示 "登录超时"**
A: 需要先在 Chrome 里手动扫码登录一次（只需一次）。

**Q: 提交流程正常但上传的截图不对**
A: 请确保 Chrome 打开了考勤页面（显示日期和下班时间），再运行脚本。

---

## 技术说明

- **浏览器连接**：通过 CDP（Chrome DevTools Protocol）连接端口 9222，已登录状态不丢失
- **iView picker 填写**：直接 send_keys 无效，必须用 JS 原生 setter 触发 Vue 响应式
- **iframe 处理**：餐补表单在 iframe 内，JS 直接跨帧操作 `.ivu-date-picker`
- **自动启动**：端口 9222 不可用时，脚本会自动启动新的带调试端口的 Chrome
