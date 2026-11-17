# 领英校友列表 API 参考

> 根据人物ID和学校ID获取某人的校友信息，支持游标翻页。
> 接口路径：`POST /agent/search/linkedin/person/alumni/list`

## python脚本参数

- `--hid`：人物ID（必填），如 `H_67890`
- `--sid`：学校ID（必填），如 `S_001`
- `--cursor`：分页游标（可选），首次查询不传，翻页时传入上一次响应返回的cursor

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hid | string | 是 | 人物ID |
| sid | string | 是 | 学校ID |
| cursor | string | 否 | 分页游标，首次请求传空串，翻页时传入上一次响应返回的cursor |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：校友列表数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

- cursor（string）：下一页游标，为空表示无更多数据
- list（array）：校友列表

### list 校友字段

- sid（string）：学校ID
- hid（string）：人物ID
