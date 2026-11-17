# LinkedIn 学校详情 API 参考

> 根据学校ID获取学校的详细信息，无需翻页。
> 接口路径：`POST /agent/search/linkedin/person/school/detail`

## python脚本参数

- `--sid`：学校ID（必填），如 `S_001`

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sid | string | 是 | 学校ID |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：学校详情数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

- list（array）：学校详情列表

### list 学校详情字段

- sid（string）：学校ID
- schoolName（string）：学校名称
- schoolType（string）：学校类型
- countryCode（string）：学校所属国家二字码
- province（string）：学校所属州省
- city（string）：学校所属城市
- websites（string）：学校网址
- linkedinUrl（string）：学校领英链接
- facebookUrl（string）：学校脸书链接
- twitterUrl（string）：学校推特链接
