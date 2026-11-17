# 配置结构

AI 助手将用户需求维护为 MCP 工具的 `config` 对象。只使用下列业务字段，由服务端生成现有抽奖后端 payload。

## 完整示例

```json
{
  "version": 1,
  "title": "八月会员感谢抽奖",
  "play": "classic",
  "publish_to_square": false,
  "description": "感谢会员支持，每人限参与一次。",
  "draw": {
    "mode": "timed",
    "start_at": "now",
    "end_at": "3d",
    "max_people": 100,
    "draws_per_user": 1
  },
  "prizes": [
    {
      "name": "蓝牙耳机",
      "count": 1,
      "delivery": "express"
    },
    {
      "name": "咖啡兑换券",
      "count": 10,
      "delivery": "none"
    }
  ]
}
```

## 字段

| 字段 | 必填 | 值 |
|---|---:|---|
| `version` | 是 | 固定 `1` |
| `title` | 是 | 1–60 字符 |
| `play` | 是 | `classic` / `turntable` / `gashapon` / `egg` / `nine-grid` / `flip-card` |
| `publish_to_square` | 否 | 默认 `false` |
| `description` | 否 | 活动说明，最多 5000 字符 |
| `draw.mode` | 是 | `timed` / `instant` / `full` / `manual` |
| `draw.start_at` | 否 | `now`、Unix 秒、ISO 8601，默认 `now` |
| `draw.end_at` | 否 | ISO 8601 或 `30m` / `12h` / `3d`，默认 `3d` |
| `draw.max_people` | 否 | 1–1000，默认 100 |
| `draw.draws_per_user` | 否 | 1–100，默认 1 |
| `draw.people_count` | 满人开奖 | 1–1000；触发人数也是参与上限，与 `max_people` 保持一致 |
| `winning_rate` | 即抽即开必填 | 只设置一个总中奖概率，0.01–100，最多两位小数；服务端按奖品数量比例分摊 |
| `prizes[].level` | 否 | 非 VIP 不提供；服务端按顺序使用“一等奖”开始的标准奖项名 |
| `prizes[].name` | 是 | 奖品名称 |
| `prizes[].count` | 是 | 1–9999 |
| `prizes[].delivery` | 否 | `express`：中奖后需填写姓名、手机号、地址；`none`：中奖后无需填写领奖信息；服务端默认 `express`，助手必须请用户确认 |
| `prizes[].image_url` | 否 | 已有 HTTPS 图片 URL；不填用系统默认图 |

## 约束

- AI 助手直接创建正式活动，不需要 `test_mode`；测试活动不能转为正式活动。
- 定时、满人和手动开奖使用 `classic`；互动玩法必须使用 `instant`。
- `draw.draws_per_user` 是所有参与者相同的次数；当前 `config` 没有订单金额、消费档位或按用户分配次数的字段。“消费满额”不能配置成 `draw.mode: full`，后者仅指参与人数达到阈值后开奖。
- 按消费金额分档的两种小程序运营路径是上传凭证后核验、或核验后发放口令；两者均不在当前 `config` 中。凭证审核通过时发放的次数取活动统一设置，审核页不能逐单指定次数；参与口令与额外机会口令也不是同一设置。专家不能在基础活动预览中声称这些分档规则已经生效。
- 奖项上限：经典 50，大转盘 50，扭蛋机 50，砸金蛋 50，九宫格 8，翻翻乐 9。奖项超过玩法上限时不得选择该玩法。
- 非 VIP 边界：单个奖项最多 9999 份奖品；`draw.max_people` 和满人开奖的 `draw.people_count` 最大 1000；开始到结束最长 30 天。
- 助手只提交总中奖概率 `winning_rate`，不填写 `prizes[].probability`，也不要求用户逐项提供；读取工具可能返回各奖项概率，不能因此把它们变成必填项。大转盘 50 个、九宫格 8 个、翻翻乐 9 个奖项时，总中奖概率必须为 100%。
- 第一版不使用 VIP 专属自定义奖项等级；`level` 由标准顺序生成，奖品名称放到 `name`。
- 小程序支持大转盘的参与条件及助力任务；当前 MCP 未开放这些高级配置字段，创建基础活动后引导用户到小程序内补充，不得表述成产品不支持或经典玩法专属。
- `get_lottery` 返回包含 `activity_id`、`short_id` 和奖项 `custom_id` 的基础配置，不包括全部高级规则；首版仅用于读取，不调用 `update_lottery`。
