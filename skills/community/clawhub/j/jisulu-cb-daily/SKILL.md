---
name: jisilu-cb-daily
description: 每日从集思录抓取可转债基本数据、强赎倒计时、下修倒计时，支持Cookie管理和本地持久化存储
---

## 前置依赖

- Python 3.8+
- 依赖包：`requests`, `pandas`
- 集思录账号（需要登录后的 `kbzw__user_login` Cookie）

## Cookie 管理规范

### 存储位置
Cookie 存储在 Skill 目录下的 `references/cookie.json`：
```json
{
  "kbzw__user_login": "用户输入的cookie值",
  "updated_at": "2026-04-28"
}
```

### 检查逻辑
1. 每次执行任务前，先检查 `references/cookie.json` 是否存在且包含 `kbzw__user_login`
2. 如果不存在或为空，**立即停止数据抓取**，向用户发送以下提示：

   ```
   【集思录登录Cookie缺失】

   本Skill需要集思录登录Cookie才能获取完整数据（尤其是强赎/下修等会员数据）。

   请按以下步骤获取 kbzw__user_login：
   1. 用Chrome/Edge打开 https://www.jisilu.cn/ 并登录账号
   2. F12打开开发者工具 → Application/应用 → Cookies → https://www.jisilu.cn
   3. 找到名为 kbzw__user_login 的Cookie，复制其Value值
   4. 将Cookie值粘贴给我

   获取后我将自动保存，后续每日抓取无需重复输入。
   ```

3. 收到用户提供的 Cookie 后，写入 `references/cookie.json`，然后继续执行

## 数据源与接口

### 接口1：可转债基本数据
- **URL**: `https://www.jisilu.cn/web/data/cb/list`
- **方法**: GET
- **Headers**:
  ```
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
  Referer: https://www.jisilu.cn/web/data/cb/list
  Cookie: kbzw__user_login={cookie值}
  ```
- **返回格式**: JSON
  ```json
  {
    "rows": [
      {
        "id": "123045",
        "cell": {
          "bond_id": "123045",
          "bond_nm": "某转债",
          "price": "105.500",
          "increase_rt": "+1.23%",
          "stock_nm": "某正股",
          "sprice": "10.50",
          "sincrease_rt": "+2.10%",
          "convert_price": "12.50",
          "convert_value": "84.00",
          "premium_rt": "25.60%",
          "force_redeem_price": "16.25",
          "put_convert_price": "8.75",
          "year_left": "3.520",
          "ytm_rt": "2.35%",
          "rating_cd": "AA+",
          "dblow": "131.10",
          "force_redeem": null,
          "maturity_dt": "2027-06-15"
        }
      }
    ]
  }
  ```

### 接口2：强赎倒计时数据
- **URL**: `https://www.jisilu.cn/web/data/cb/redeem`
- **方法**: GET
- **Headers**: 同上，需携带 Cookie
- **关键字段**（预期）:
  - `bond_id`: 转债代码
  - `bond_nm`: 转债名称
  - `redeem_count`: 已满足强赎天数
  - `redeem_trigger`: 强赎触发条件（如 15/30）
  - `redeem_status`: 强赎状态（如"公告强赎"、"暂不强赎"、"倒计时中"）
  - `redeem_price`: 赎回价格
  - `last_redeem_dt`: 最后交易日

### 接口3：下修倒计时数据
- **URL**: `https://www.jisilu.cn/web/data/cb/adjust`
- **方法**: GET
- **Headers**: 同上，需携带 Cookie
- **关键字段**（预期）:
  - `bond_id`: 转债代码
  - `bond_nm`: 转债名称
  - `adjust_count`: 已满足下修天数
  - `adjust_trigger`: 下修触发条件
  - `adjust_status`: 下修状态（如"已公告下修"、"董事会提议"、"倒计时中"）
  - `adjust_price`: 拟下修价格（如有）
  - `adjust_dt`: 下修股东大会日期

## 执行工作流

### Step 1: Cookie 检查与准备
```python
import json, os

cookie_path = os.path.join(os.path.dirname(__file__), "../references/cookie.json")

if not os.path.exists(cookie_path):
    # 触发Cookie缺失提示，等待用户输入
    raise FileNotFoundError("Cookie文件缺失，请按Skill说明提供kbzw__user_login")

with open(cookie_path, "r", encoding="utf-8") as f:
    cookie_data = json.load(f)

kbzw_cookie = cookie_data.get("kbzw__user_login", "")
if not kbzw_cookie:
    raise ValueError("kbzw__user_login为空，请重新提供")
```

### Step 2: 抓取基本数据
- 使用 `requests.get()` 访问 `https://www.jisilu.cn/web/data/cb/list`
- 携带 Cookie: `kbzw__user_login={kbzw_cookie}`
- 解析 JSON，提取 `rows` → `cell` 中的字段
- 转换为 DataFrame，字段重命名为中文或保留英文（建议保留英文原始字段名便于后续处理）

### Step 3: 抓取强赎倒计时数据
- 使用相同 Cookie 访问 `https://www.jisilu.cn/web/data/cb/redeem`
- 解析返回数据，提取强赎相关字段
- 以 `bond_id` 为键，与基本数据做 **LEFT JOIN**

### Step 4: 抓取下修倒计时数据
- 使用相同 Cookie 访问 `https://www.jisilu.cn/web/data/cb/adjust`
- 解析返回数据，提取下修相关字段
- 以 `bond_id` 为键，与已有数据做 **LEFT JOIN**

### Step 5: 数据清洗与保存

#### 清洗规则
1. **价格字段**：去除 `%` 符号，转为 float
2. **涨跌幅**：同上处理
3. **日期字段**：统一转为 `YYYY-MM-DD` 格式
4. **空值处理**：`force_redeem` 为空表示"暂不强赎"；`adjust_status` 为空表示"未触发下修"
5. **去重**：按 `bond_id` 去重，保留最新记录

#### 保存格式
数据保存为 CSV，按日期命名：

```
output/
└── jisilu_cb_2026-04-28.csv
```

CSV 必须包含以下核心字段：
| 字段名 | 来源 | 说明 |
|--------|------|------|
| bond_id | 基本数据 | 转债代码 |
| bond_nm | 基本数据 | 转债名称 |
| price | 基本数据 | 转债现价 |
| increase_rt | 基本数据 | 转债涨跌幅 |
| stock_nm | 基本数据 | 正股名称 |
| sprice | 基本数据 | 正股现价 |
| premium_rt | 基本数据 | 溢价率 |
| convert_price | 基本数据 | 转股价 |
| year_left | 基本数据 | 剩余年限 |
| ytm_rt | 基本数据 | 到期收益率 |
| rating_cd | 基本数据 | 评级 |
| dblow | 基本数据 | 双低值 |
| force_redeem_price | 基本数据 | 强赎触发价 |
| put_convert_price | 基本数据 | 回售触发价 |
| redeem_status | 强赎接口 | 强赎状态 |
| redeem_count | 强赎接口 | 已满足强赎天数 |
| adjust_status | 下修接口 | 下修状态 |
| adjust_count | 下修接口 | 已满足下修天数 |
| adjust_dt | 下修接口 | 下修股东大会日期 |
| data_date | 系统生成 | 数据日期（YYYY-MM-DD）|

### Step 6: 结果汇报
向用户汇报当日数据概况：
```
【集思录可转债数据抓取完成】
日期：2026-04-28
共抓取转债：XXX 只
其中：
- 公告强赎：XX 只
- 强赎倒计时中：XX 只
- 已公告下修：XX 只
- 下修倒计时中：XX 只

数据已保存至：output/jisilu_cb_2026-04-28.csv
```

## 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| Cookie 失效（返回 403/登录页） | 提示用户重新输入 Cookie，删除旧 cookie.json |
| 接口返回空数据 | 记录日志，重试最多 3 次，仍失败则跳过该接口 |
| 网络超时 | 设置 timeout=30s，重试 3 次 |
| 字段缺失 | 用空值填充，不中断流程 |
| 日期解析失败 | 保留原始字符串，标注"解析异常" |

## 定时执行建议

如需每日自动执行，可在本地 OpenClaw 中配合 cron/systemd：
```bash
# 每天 15:30 收盘后执行
30 15 * * * cd ~/.config/agents/skills/jisilu-cb-daily && python scripts/collect_jisilu_cb.py
```

或在 Kimi Claw 对话中每日发送指令：
```
执行 jisilu-cb-daily Skill 抓取今日可转债数据
```
