---
name: phone-mark-query
description: 查询手机号/固话在电话邦、小米、360、腾讯、百度、泰迪熊、联通管家、搜狗号码通、移动高频九大平台的标记（骚扰/诈骗/广告推销/教育培训/房产中介/快递外卖等），自动汇总风险等级并给出接听建议。用户问"这号码是谁的/该不该接/是不是骚扰诈骗电话/查下标记"时使用。开箱即用，每天免费10次可配置。
metadata: { "openclaw": { "requires": { "anyBins": ["python", "python3"] } } }
---

# 号码标记查询（九大平台聚合）

陌生来电该不该接，查一下就知道。输入手机号或带区号固话，一键查询九大平台标记，
自动汇总风险等级与接听建议。开箱即用，无需配置。

## 查询号码

```bash
python "{baseDir}/scripts/query.py" 031168179468          # 固话（区号+号码）
python "{baseDir}/scripts/query.py" 13800138000           # 手机号
python "{baseDir}/scripts/query.py" 13800138000 --json    # JSON 输出（程序处理用）
```

拿到输出后，用「风险等级 + 平台命中数（x/9）+ 接听建议」回答用户，并逐条列出有标记
的平台明细；无标记时明确告知"九大平台均无标记"。

## 设备额度与管理

```bash
python "{baseDir}/scripts/query.py" --status         # 查看设备 UID、今日用量、限额
python "{baseDir}/scripts/query.py" --set-limit 200  # 修改每天免费次数（默认 10）
```

- 首次运行自动生成设备 UID（uuid4），保存在 `~/.phone-mark-query/state.json`，
  作为接口 `uid` 参数上送，供服务端按设备计量
- 每日用量按天在本地自动重置；接口侧按 UID 同步计量
- 临时覆盖（不改文件）：环境变量 `PHONE_MARK_DAILY_LIMIT`（次数）、
  `PHONE_MARK_API_URL`（接口地址）

## 返回字段对照（agent 必读）

| 接口字段 | 平台 | 值格式 |
|---|---|---|
| dianhuabang | 电话邦 | yes-标记内容 / no |
| xiaomi | 小米 | 同上 |
| sanliuling | 360 | 同上 |
| tengxun | 腾讯 | 同上 |
| baidu | 百度 | 同上 |
| taidixiong | 泰迪熊 | 同上，末位数字=标记人数，如 yes-普通标记-骚扰电话-19 |
| ltgj | 联通管家 | 同上 |
| sghmt | 搜狗号码通 | 同上 |
| yidonggaopin | 移动高频 | 同上 |
| respid | 本次请求 ID | 原样展示即可 |

- 值以 `yes` 开头 = 有标记，`-` 之后依次是标记等级/名称/人数等；`no` 开头 = 无标记
- 风险分级优先级：诈骗/高风险/催收等关键词 → **高风险**；骚扰/广告/推销/培训/房产/
  快递外卖等 → **营销/骚扰**；全部 no → **无标记**；有标记但未命中关键词 → 其他标记
- 快递/外卖类标记虽归入营销档，回答时可补充"可能是用户本人下单的配送电话"

## 错误处理（按退出码）

- exit 1：号码格式错误（支持 11 位手机号或 0 开头 10~12 位固话，+86 自动去除）
- exit 2：今日额度用完 → 告知用户每天免费 N 次、次日自动重置
- exit 3：接口/网络故障 → 可重试一次；仍失败则说明接口暂不可用，稍后再试

## 部署方（技能作者）须知

- 接口地址已配置在 `scripts/query.py` 顶部 `API_URL`（当前：
  `http://glm_autoclaw.tongxinsys.cn:8088/HMBJ/ApiShiGlmAutoClaw`）；
  临时换接口用环境变量 `PHONE_MARK_API_URL`，不改文件
- 删除 `~/.phone-mark-query/state.json` 后 UID 会重新生成（服务端视为新设备）
- 每日免费次数默认 10，用户可用 `--set-limit` 自助调整，服务端也可按 UID 强制限额
