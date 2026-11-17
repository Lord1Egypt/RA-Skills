---
name: jd-data
slug: jd-data
displayName: 京东商品数据采集
summary: 采集京东商品详情与商品评论（按次扣点，详情 180 点/次、评论 300 点/次，注册送 1000 点），支持批量、幂等防重复扣点、大响应落盘，适合选品分析与评论数据分析。
description: 京东商品数据采集（商品详情 / 商品评论）。当用户需要采集京东商品详情、商品评论，或提到"京东商品详情/京东评论采集/商品评论分析/商品数据分析"时使用。对接AI数据平台，按次扣点，批量任务前可免费查询余额与单价。
version: 1.6.7
license: MIT
---

# Skill：京东数据采集（jd-data）

对接「AI数据平台」，采集京东商品详情与商品评论。
每次调用消耗平台点数，**单价以 `GET /api/v1/account/balance` 返回的 `price` 字段为准**
（会随服务成本调整，不要在代码或脚本里写死；查询余额本身不扣点）。

## 一、前置条件（缺一不可，先向用户确认）

| 项 | 说明 |
|---|---|
| 平台地址 | **https://zlh.aidata366.com**（正式服务，直接可用）；也可用环境变量 `JD_PLATFORM_BASE_URL` 覆盖 |
| API Key | **推荐直接运行 `login` 自动获取并保存到本机**（见下文「首次使用」）；也可显式设置环境变量 `JD_PLATFORM_API_KEY`，优先级更高 |
| 点数 | 新用户注册赠送 1000 点；不足时按「五、客服与充值」联系客服充值（当前为人工充值） |

> 没有 Key 时不要尝试调用：会返回 `40100`，且浪费排查时间。先执行 `login` 拿 Key。

### 首次使用：一条命令完成登录（推荐）

没有 API Key 时，不要让用户手动去创建，直接执行：

```bash
python jd_api.py login --skill-name jd-data --ai-entry claude-code
```

把输出里的「二维码图片 / 授权链接」发给用户，让用户扫码或打开链接登录并点「确认授权」。
用户确认后执行（pending 时退出码为 6，3~5 秒后重试即可）：

```bash
python jd_api.py login_check --access-token <上一步输出的 access_token> --skill-name jd-data --ai-entry claude-code
```

成功后 API Key 会自动保存到 `~/.zhi_liao_hou/config.json`（仅本机），以后所有命令直接调用即可，
无需再设置环境变量；四个 skill 共用这份凭证。授权链接 10 分钟内有效且只能使用一次。

### 备选：手动注册 + 创建 Key（浏览器操作，约 1 分钟）

没有账号或自动登录失败时走这条路；**先注册，再执行上面的 `login`** 即可自动保存 Key。

1. **注册**：浏览器打开 `https://zlh.aidata366.com/auth/register?skill=jd-data`，填**手机号** →
   输入右侧**图片验证码** → 点「获取短信验证码」→ 填入收到的 6 位短信码 → 提交。
   **用户名和初始密码由平台自动分配**，注册成功页会一次性显示（请提醒用户立即记录，尤其是
   初始密码；登录后可在「总览」页修改）。注册即送 **1000 点**（注册赠送流水可在「总览」页看到；
   出于防薅考虑，同一 IP 每天最多注册 3 个账号）。
   注意：注册必须由**用户本人在浏览器完成**（图片验证码与短信验证码无法、也不应被脚本绕过），
   agent 可以代填其余配置，但不要尝试替用户注册。
2. **创建 API Key**：登录后进入左侧「API Key」页，起个名字点创建。**明文 Key 仅创建成功后的
   那一次页面显示**，立刻复制保存；关掉页面后只能看到前缀（`jh_` 开头 10 位），丢了只能重新创建。
3. **配置环境变量**后即可上手：
   ```bash
   export JD_PLATFORM_BASE_URL="https://zlh.aidata366.com"
   export JD_PLATFORM_API_KEY="jh_xxxxxxxx"
   ```

> 登录支持两种方式：**手机号 + 短信验证码**，或**用户名 + 密码**（注册成功页显示的自动分配凭据）。

预算预期：当前无免费额度（`free_quota=0`），注册赠送的 1000 点 ≈ **5 次商品详情**（180 点/次）
或 **3 次商品评论**（300 点/次），足够体验与联调；批量采集前先按「四、计费纪律」做预算预检。

## 二、安装与 30 秒上手

**安装**：本 skill 只有两个文件（`SKILL.md` + `jd_api.py`），`jd_api.py` 为 **Python 纯标准库实现
（零第三方依赖，Python 3.8+ 可跑）**，把整个 `jd-data/` 目录放入 agent 的 skills 目录即完成安装，
无需 pip 安装任何东西。

## AI 调用来源参数（必填）

所有会访问后端 API 的命令必须携带 `--skill-name jd-data` 和
`--ai-entry <AI工具标识>`（如 `claude-code`）。IP 无需传递，由服务端自动获取。
首次缺参会告警放行，第二次起拒绝。
`login` / `login_check` 也建议携带这两个参数，其余采集命令必须携带。

```bash
export JD_PLATFORM_BASE_URL="https://zlh.aidata366.com"
export JD_PLATFORM_API_KEY="jh_xxxxxxxx"

python jd_api.py balance --skill-name jd-data --ai-entry claude-code  # 免费：余额 + 各接口单价
python jd_api.py goods_detail 10174613130151 --skill-name jd-data --ai-entry claude-code  # 商品详情
python jd_api.py goods_comment 100118481919 1 --skill-name jd-data --ai-entry claude-code  # 商品评论（第 1 页）
python jd_api.py goods_comment 100118481919 1 --out ./comment_p1.json --skill-name jd-data --ai-entry claude-code  # 大响应写文件
```

参数支持三种写法：**位置参数** / **`key=value`** / **整段 JSON**。
批量脚本里建议统一用 `key=value` 或 JSON，避免位置错位。

CLI 退出码：`0` 成功 ｜ `2` 参数或配置错误（**未发请求、未扣点**）｜ `3` 鉴权或点数问题 ｜ `4` 本次取数失败 ｜ `5` 网络问题 ｜ `6` 等待用户完成授权（`login_check` 轮询时）。
判断成败请看退出码，不要靠 grep 输出。

## 三、接口清单（均 POST，JSON body）

| 用途 | 命令 | 路径 | 必填 | 可选 |
|---|---|---|---|---|
| 商品详情 | `goods_detail` | `/api/v1/jd/goods_detail` | `goods_id` | — |
| 商品评论 | `goods_comment` | `/api/v1/jd/goods_comment` | `goods_id`,`page` | — |
| 余额/单价（免费） | `balance` | `GET /api/v1/account/balance` | — | — |
| 登录授权（免费/不扣点） | `login` | `POST /auth/cli-session` | — | — |
| 校验授权并保存 Key（免费/不扣点） | `login_check` | `POST /auth/cli-session/check` | `--access-token` | — |

**只允许传表内参数**：平台只转发已声明的字段，多余字段会被丢弃——你以为加了筛选条件，实际没生效。
CLI 会在本地直接拒绝未知参数（退出码 2）。

选型建议：
- 商品基础信息（标题/价格/图片/规格/店铺）用 `goods_detail`；
- 评论列表、评分、追评、商家回复、评论汇总统计用 `goods_comment`；
- 评分数组在 `item[]` 里，好评率在 `good_rate`（0~1 小数），最大页码看 `page_count`。

## 四、计费纪律（必须遵守）

1. **任何批量任务开始前**，先 `balance`：
   - 总成本 = 计划调用次数 × 对应接口 `price`
   - `总成本 > balance` 时**停止**并告知用户差额（按 `points_per_yuan` 折算成元），
     引导用户按「五、客服与充值」联系客服
2. 单次任务预计超过 **50 次**调用，先向用户确认预算再执行
3. 循环中每 20 次复查一次 `balance`，发现余额骤降立即停止
4. 拿到 `40200`（点数不足）**立即停止，不要重试**
5. 拿到 `40300`（限频）等待约 60 秒再继续；批量任务默认串行 + 每次间隔 0.5~1 秒
6. 拿到 `50001`（数据服务暂不可用）停止任务，告知用户稍后再试

## 五、客服与充值

### 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、数据结果异常、批量采购等），
请引导用户联系客服，**不要自行尝试绕过或代用户操作**：

- **客服微信**（扫码添加）：<http://st.aidata366.com/assets/concat.png>
- **客服电话**：**18722121663**

### 充值方式（当前为人工充值阶段）

1. 联系客服确认充值金额，**批量/大额采购可洽谈优惠**；
2. 当前兑换率：**1 元 = 1000 点**（1 点 = 0.001 元；按当前单价约可调用
   商品详情 5 次/元、商品评论 3 次/元，以 `balance` 返回的实时 `price` 为准）；
3. 转账后把**平台用户名 + 转账凭证**告知客服，管理员加点后到平台「充值说明」页
   刷新即可看到余额到账；
4. **点数永不过期**；余额、冻结与累计消费可在平台「总览」页自助查询。

> 到账以平台「充值说明」页显示为准；充值前不需要把 API Key 或密码发给客服。

## 六、幂等与重试（防重复扣点）

平台按 `Idempotency-Key` + 「接口 + 请求体指纹」做幂等：

- **CLI 已内置**：默认自动生成幂等键，网络错误/响应超时/并发已满时自动重试 1 次并复用该键，
  重试不会重复扣点。键会打印在 stderr（`# 幂等键: task-xxx`），手工续跑时用 `--idem` 复用。
- 手工 curl 或自写脚本时：**同一次业务调用的所有重试必须复用同一个键**，换接口或改参数会被判 `40910`。
- 调节重试次数：`--retry 0`（不重试）～ `--retry 3`；超时：`--timeout 60`。

```bash
python jd_api.py goods_detail 10174613130151 --idem task-0001 --skill-name jd-data --ai-entry claude-code  # 指定键
python jd_api.py goods_detail goods_id=10174613130151 --retry 2 --timeout 60 --skill-name jd-data --ai-entry claude-code
```

## 七、错误码与处置

| code | 含义 | 可重试 | 处置 |
|---|---|---|---|
| `40000` | 请求体非法 | 否 | 修正 payload（必须是 JSON 对象），不要原样重发 |
| `40100` | API Key 无效 | 否 | 检查 `JD_PLATFORM_API_KEY`，或让用户重新创建 Key |
| `40101` | API Key 已停用 | 否 | 让用户到平台「API Key」页启用/新建 |
| `40200` | 点数不足 | 否 | 停止任务，引导用户按「五、客服与充值」联系客服充值 |
| `40201` | 接口未开放 | 否 | 该接口已停用，联系客服确认（见「五、客服与充值」） |
| `40300` | 触发限频 | 是 | 等约 60 秒，降低并发/加间隔 |
| `40910` | 幂等键冲突 | 否 | 该键已用于其它接口或其它参数 → **换新键** |
| `40911` | 同键请求处理中 | 是 | 等 2~3 秒用**同一键**重试一次 |
| `50000` | 本次取数失败 | 否 | 把 `msg` 转告用户；响应里会显示本次退款点数，未退款表示该次成本已产生 |
| `50001` | 数据服务暂不可用 | 否 | 停止任务，稍后再试 |
| `50002` | 数据服务响应超时 | 是 | 用同一幂等键重试（结果不确定，平台保留幂等记录） |
| `50003` | 平台并发已满 | 是 | 降低并发后重试 |

响应包统一为 `{"code":0,"msg":"success","data":{...},"request_id":"req_..."}`。
失败时 `data` 含 `balance`（当前余额）与 `refunded`（本次退回点数）；`msg` 与 `request_id` 要一并转告用户。

## 八、批量采集范式

```bash
# 1) 预算预检
python jd_api.py balance --skill-name jd-data --ai-entry claude-code

# 2) 串行 + 每任务独立幂等键 + 大响应落盘 + 失败不中断整批
mkdir -p out
i=0
while read -r gid; do
  i=$((i+1))
  python jd_api.py goods_detail "goods_id=$gid" --idem "batch-$(date +%Y%m%d)-$i" \
      --out "out/$gid.json" --skill-name jd-data --ai-entry claude-code
  rc=$?
  case $rc in
    0) ;;                                   # 成功
    3) echo "第 $i 条：鉴权或点数问题，终止"; break ;;
    4) echo "第 $i 条：本次取数失败，跳过 $gid" ;;  # 已按规则退款/标记，继续下一条
    5) echo "第 $i 条：网络异常，稍后重跑（复用同一 --idem 键）"; sleep 5 ;;
  esac
  sleep 0.5                                  # 主动节流，避免 40300
done < goods_ids.txt
```

`goods_id` 从链接取：`https://item.jd.com/<goods_id>.html`。

## 九、数据要点（踩坑清单）

- **详情价格**：SKU 内 `price` 可能不准，以顶层 `price` 为准；多个规格看 `skus.sku[]`。
- **详情标题/店铺**：`title`、`nick`、`shop_id`、`seller_info.shop_name`。
- **评论（`goods_comment`）**：评论列表在 `item[]`，每条含 `rate_content`（正文）/ `score`（1~5）/
  `rate_date`（时间）/ `display_user_nick`（昵称）/ `pics[]`（晒图）/ `auction_sku`（规格）/
  `add_feedback`（追评）；好评率在 `good_rate`（0~1 小数）；总条数看 `total_results`，
  最大页码看 `page_count`。
- **评论为空是正常业务结果**：`code=0` 但 `item` 为空，通常是该商品无评论或该页无数据，
  不要当异常重试（重试只会白扣点）。
- **图片地址**：部分字段是 `//img*.360buyimg.com/...` 协议相对地址，展示时补 `https:`。

## 十、排障

1. 记录 `request_id`（响应体里，或错误信息末尾），到平台「调用记录」页按 request_id 查：
   可看到扣点、退款、失败原因与耗时。
2. `50000` 且本次退款为 0：该次取数成本已产生，按平台规则不退；如需申诉把 request_id
   通过客服（见「五、客服与充值」）提交给运营。
3. 「获取商品评论失败」：多为该商品本身无可采评论，换个 goods_id 试，不要循环重试。
4. 全部请求都失败：先 `balance` —— 若返回 `40100/40101` 是 Key 问题；若连接被拒/超时，检查平台地址，
   以及本机是否挂了代理（CLI 默认**不使用**系统代理；确有需要时用 `JD_PLATFORM_PROXY` 显式指定）。

## 十一、安全要求

- API Key 只从环境变量或本机配置 `~/.zhi_liao_hou/config.json` 读取，**不要写进脚本、
  不要提交到仓库**；登录成功时终端会显示一次，不要把该输出转发到公开渠道。
- 不要把 Key 拼进 URL 或日志；分享排障信息时只给 `request_id`。
- 不要并发轰炸平台（默认串行）；单个 Key 的频率上限由平台配置决定。

## 触发词

京东商品详情、京东评论采集、商品评论筛选、评论按评分排序、商品数据分析
