# Category Keyword Mapping

Based on common expense categories for QianJi users.

## Quick Reference Table

| Keywords / Patterns | 分类 | 二级分类 | Special Rules |
|---|---|---|---|
| 麦当劳, 肯德基, 饿了么, 美团外卖, 外卖, 午饭, 晚饭, 早饭, 午餐, 晚餐, 早餐, 吃饭, meal, lunch, dinner, breakfast, 叮咚买菜, 赛百味, 老乡鸡, 杨国福, 麻辣烫, 西贝, 萨莉亚, 米粉, 饺子, 牛肉饼, 食堂 | 餐饮 | 三餐 | |
| 咖啡, coffee, Manner, 瑞幸, 星巴克, Starbucks, latte, 拿铁, 美式 | 餐饮 | 咖啡 | |
| 零食, 友宝, 自动售货机, vending, 7-11, 711, 便利店, 物美, 便利蜂, 霸王茶姬, 奶茶, 烧饼, snack | 餐饮 | 零食 | |
| 打车, 滴滴, 高德, taxi, cab, 出租车, 顺风车, 哈啰, 一卡通, 地铁, 公交, 骑车 | 交通 | | |
| 充电, 小绿人, 电驴 | 交通 | 电驴充电 | |
| 按摩, 足疗, 金色印象, 桑拿, spa, SPA, 80分钟 | 娱乐 | 桑拿按摩 | 账户1=金色印象, 标签=10号 |
| 日用品, 宜家, IKEA, 京东日用, 日常用品, household | 居家生活 | 日用品 | |
| 水费, 电费, 水电, electricity, water | 居家生活 | 水电 | |
| 话费, 电信, 联通, 移动, 网费, phone bill | 居家生活 | 话费网费 | |
| 房租, 自如, rent | 住房 | 房租 | |
| 理发, 美发, haircut | 清洁护理 | 美发 | |
| 旅行, 旅游, 火车票, 机票, 携程, 飞猪, 同程, 中铁, 徒步, hiking, travel, hotel, 酒店 | 旅行 | | |
| 红包, 请客, 送礼, 礼物, gift, treat, 群收款 | 人情 | 请客送礼 | |
| 工资, salary, 代发工资 | 工资 | | 类型=收入 |
| 公积金, housing fund | 公积金 | | 类型=收入 |
| 服装, 衣服, clothing, 鞋, shoes, H&M | 服饰 | | |
| 会员, 订阅, subscription, Xmind, 域名, domain, 得到 | 自我成长 | 付费会员 | |
| 健身, gym, 乐刻, 运动, exercise, 户外 | 运动 | | |
| 快递, 物流, delivery, 菜鸟 | 快递 | | |
| 转账, transfer | 其它 | | 类型=转账, 账户2=现金 or 中转账户 |
| 退款, refund | 其它 | | 类型=退款 |

## Special Rules

### 1. 娱乐/桑拿按摩

When category is 娱乐/桑拿按摩, ALWAYS apply:
- 账户1 = `金色印象` (NOT 工资卡)
- 标签 = `10号`
- Default amount: 206.0

### 2. 转账 (Transfer)

When type is 转账:
- 分类 = `其它`
- 二级分类 = empty
- 账户2 = `现金` (for credit card / person payments) or `中转账户` (for loan repayments)

### 3. 收入 (Income)

Income keywords and their categories:
- 工资/salary → 工资 (income)
- 公积金 → 公积金 (income)
- 退款/refund → use original category if known, otherwise 其它 (type=退款)
- 充值/top-up to 金色印象 → 其它 (income), 账户1=金色印象

### 4. Default Values

- 类型: 支出 (expense) unless income/transfer/refund keywords detected
- 账户1: 工资卡 (except 娱乐/桑拿按摩 → 金色印象)
- 账户2: empty (except 转账)
- 币种: CNY
- 记账者: 小明

### 5. Ambiguous Cases

If the input doesn't clearly match any category, suggest 2-3 candidates and let the user choose. Common ambiguities:
- 京东/JD purchases → could be 居家生活/日用品 or 其它 (ask user)
- 美团 → could be 餐饮/三餐 or 其它 (ask user)
- Large round amounts with no context → likely 其它

### 6. Merchant Name Shortcuts

Users commonly use short names. Map these to their categories:
- 麦当劳/麦记/M记/金拱门 → 餐饮/三餐
- KFC/肯德基 → 餐饮/三餐
- 瑞幸/luckin → 餐饮/咖啡
- Manner → 餐饮/咖啡
- 星巴克/Starbucks/星爸爸 → 餐饮/咖啡
- 滴滴/DD → 交通
- 高德 → 交通
- 宜家/IKEA → 居家生活/日用品
