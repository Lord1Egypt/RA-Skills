## 📋 最新的心电报告列表

| 序号 | 测量时间 | 分析结果 | 报告编号 |
| :---: | :--- | :--- | :--- |
{% for item in list %}| **{{ item.index }}** | {{ item.takeTime }} | {{ item.result_icon }} **{{ item.result }}** | `{{ item.report_no }}` |
{% endfor %}

💡 **操作提示**：请回复 **序号** (如 "1") 查看详细报告