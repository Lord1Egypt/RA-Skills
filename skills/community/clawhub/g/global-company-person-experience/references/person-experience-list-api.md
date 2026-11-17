# 全球企业库工作经历列表 API 参考

> 根据人物ID获取某人的历史工作经历列表，支持游标翻页，可选传入公司ID(pid)筛选指定公司的工作经历。
> 接口路径：`POST /agent/search/depth_company/person/experience/list`

## python脚本参数

- `--hid`：人物ID（必填），如 `H_67890`
- `--pid`：公司ID（可选），如 `US_12345`，传入则代表查询指定公司的工作经历
- `--cursor`：分页游标（可选），首次查询不传，翻页时传入上一次响应返回的cursor

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hid | string | 是 | 人物ID |
| pid | string | 否 | 公司ID，传入则代表查询指定公司的工作经历 |
| cursor | string | 否 | 分页游标，首次请求不传，翻页时传入上一次响应返回的cursor |
| limit | integer | 否 | 每页条数，默认20 |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：工作经历列表数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

- cursor（string）：下一页游标，为空表示无更多数据
- list（array）：工作经历列表

### list 工作经历字段

- pid（string）：公司ID
- companyName（string）：公司名称
- titleName（string）：职位名称
- startDate（integer）：任职开始时间（秒级时间戳）
- endDate（integer）：任职截止时间（秒级时间戳），0表示至今
- postStatus（integer）：任职状态：0-未检测，1-在职，2-离职，3-不确定
- summary（string）：经历总结
