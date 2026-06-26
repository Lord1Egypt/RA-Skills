# CSV 格式说明

最小列：
- email（必填）

推荐列：
- name
- company
- title
- custom1/custom2（自定义字段）

示例：

email,name,company,title
alice@example.com,Alice,Acme,CTO
bob@example.com,Bob,Contoso,Head of Growth

注意事项：
- UTF-8 编码，逗号分隔（CSV）
- 首行是标题
- 无邮箱的行将被跳过并记录在日志中
