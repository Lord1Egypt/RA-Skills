# GB/T 35273 文件分类分级关键词规则

## 类别定义

依据 GB/T 35273《个人信息安全规范》，将个人信息分为两个类别：

### S - 敏感个人信息

一旦泄露、非法提供或滥用可能危害人身和财产安全，导致个人名誉、身心健康受到损害或歧视性待遇等的个人信息。

### G - 一般个人信息

除敏感个人信息以外的其他个人信息，以及不涉及个人信息的文件。

## S 类关键词（敏感个人信息）

### 个人身份信息
- 身份证、身份证号、身份证复印件、idcard、id_card、identity_card
- 护照、护照号、passport
- 社保号、社保卡、social_security
- 军官证、军官证号
- 户口本、户口簿、户籍
- 出生证、出生医学证明

### 金融账户信息
- 银行卡、银行卡号、bank_card、bank_card_number
- 信用卡、credit_card
- 银行流水、bank_statement
- 账户密码、login_password、pwd
- 支付密码、pay_password
- 资金流水、交易记录、transaction_record
- 贷款、loan
- 征信、credit_report

### 认证凭据
- 密码、password、passwd
- 密钥、secret_key、api_key
- 令牌、token
- 签名证书、signature_certificate

### 生物识别信息
- 人脸、face、facial
- 指纹、fingerprint
- 虹膜、iris
- 声纹、voiceprint
- 步态、gait

### 通讯与社交信息
- 通讯录、contacts、address_book
- 通话记录、call_log、call_history
- 短信记录、sms_record
- 即时通讯、im_chat、wechat_record、qq_chat
- 社交关系、social_graph、social_relation

### 位置与行踪信息
- 定位、location、gps
- 行踪轨迹、trajectory、track_record
- 轨迹数据、location_history

### 健康与财产信息
- 病历、medical_record
- 体检、health_checkup
- 诊疗、diagnosis
- 药物、medication
- 财产信息、property_info、asset_info
- 收入、income、salary
- 纳税、tax_record
- 保险、insurance_policy

### 其他敏感信息
- 宗教信仰、religion
- 性取向、sexual_orientation
- 政治面貌、political_status

## G 类关键词（一般个人信息）

命中以下关键词且未命中任何 S 类关键词的文件，归类为 G 类。

- 姓名、name
- 手机号、phone、mobile、cell_phone
- 电话、telephone
- 邮箱、email、e_mail
- 性别、gender
- 年龄、age
- 生日、birthday、birth_date
- 籍贯、native_place
- 民族、ethnicity
- 婚姻、marital_status
- 学历、education
- 职位、position
- 工号、employee_id
- 用户画像、user_profile
- 客户信息、customer_info
- 用户信息、user_info
- IP地址、ip_address
- MAC地址、mac_address
- 设备指纹、device_fingerprint
- 浏览记录、browsing_history
- 搜索记录、search_history
- Cookie
- 账号、account、username

未命中任何关键词的文件默认为 G 类。

## 匹配规则

1. **大小写不敏感**：文件名统一转为小写后匹配
2. **S 类优先**：同一文件名同时命中 S 类和 G 类关键词时，归为 S 类
3. **去除扩展名**：匹配前先去掉文件扩展名（.docx、.doc、.pdf 等）
4. **分隔符等价**：空格、下划线、连字符视为等价分隔符

## 输出字段说明

| 字段 | 说明 |
|------|------|
| file_path | 文件完整路径 |
| file_name | 文件名（含扩展名） |
| category | 类别（S/G） |
| category_name | 类别名称 |
| matched_keywords | 匹配到的关键词（逗号分隔） |
| suggestion | 处理建议 |

## 处理建议

| 类别 | 建议处理方式 |
|------|-------------|
| S | 加密存储，严格限制访问权限，传输需加密，建议脱敏后使用 |
| G | 内部使用，注意保护，避免不必要的公开分享 |
