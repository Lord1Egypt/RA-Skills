# 时区预设（Timezone Presets）

> 默认问 9 个选项。中国用户一律默认 `Asia/Shanghai`，除非用户明确改动。
> 所有值使用 **IANA 时区 ID**（可被 `date -u`、JS `Intl.DateTimeFormat` 正确解析）。

---

## 9 选项短列表

| # | IANA ID | 显示名 | 偏移 | 夏令时 |
|---|---------|--------|------|--------|
| 1 | `Asia/Shanghai` | 北京 / 上海（中国大陆） | UTC+8 | 无 |
| 2 | `Asia/Hong_Kong` | 香港 | UTC+8 | 无 |
| 3 | `Asia/Tokyo` | 东京 / 首尔 | UTC+9 | 无 |
| 4 | `Asia/Singapore` | 新加坡 / 马尼拉 | UTC+8 | 无 |
| 5 | `Europe/London` | 伦敦 / 都柏林 | UTC+0/+1 | 有（3 月-10 月） |
| 6 | `Europe/Berlin` | 柏林 / 巴黎 / 罗马 | UTC+1/+2 | 有 |
| 7 | `America/Los_Angeles` | 旧金山 / 洛杉矶 | UTC-8/-7 | 有（3 月-11 月） |
| 8 | `America/New_York` | 纽约 / 多伦多 | UTC-5/-4 | 有 |
| 9 | **其他** | 手动输入 IANA ID | — | — |

---

## 扩展选项（用户选 9 之后可用）

### 亚洲
- `Asia/Bangkok` —— 曼谷 / 雅加达（UTC+7）
- `Asia/Dubai` —— 迪拜（UTC+4）
- `Asia/Kolkata` —— 印度（UTC+5:30）

### 欧洲
- `Europe/Moscow` —— 莫斯科（UTC+3）
- `Europe/Helsinki` —— 赫尔辛基 / 雅典（UTC+2/+3）

### 美洲
- `America/Chicago` —— 芝加哥（UTC-6/-5）
- `America/Denver` —— 丹佛（UTC-7/-6）
- `America/Sao_Paulo` —— 圣保罗（UTC-3）
- `America/Mexico_City` —— 墨西哥城（UTC-6/-5）

### 大洋洲
- `Australia/Sydney` —— 悉尼（UTC+10/+11）
- `Australia/Perth` —— 珀斯（UTC+8）
- `Pacific/Auckland` —— 奥克兰（UTC+12/+13）

### 非洲
- `Africa/Johannesburg` —— 约翰内斯堡（UTC+2）
- `Africa/Cairo` —— 开罗（UTC+2/+3）

---

## 时区影响的龙虾行为

选定时区后，龙虾在以下场景自动按本地时间工作：

1. **每日/每周心跳**：早安问候、周报生成时间
2. **日志时间戳**：所有 KB 条目的 `createdAt` / `updatedAt`
3. **绝对日期转换**：用户说"下周四" → 按时区换算为 `YYYY-MM-DD`
4. **会议时间建议**：跨时区协作时自动给对方时区对应时间
5. **热词/资讯抓取**：优先抓本地时段活跃的信息源

---

## 判定提示

- 如果用户 `user_identity.md` 已经提到城市（如"青岛"），龙虾可自动推断 `Asia/Shanghai`，仅作一次确认
- 如果用户是海外华人，给出 `Asia/Shanghai` + 本地时区双选项
