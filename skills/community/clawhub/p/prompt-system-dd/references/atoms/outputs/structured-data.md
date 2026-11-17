# structured-data 结构化数据输出原子

<!--
ATOM
type: output
id: structured-data
deps: none
-->

> 唯一真相源:本文件是结构化数据类输出的唯一权威定义。
> 自包含:不依赖其他原子内容,可独立注入组装。

## 输出规范

- 命中信号:JSON、YAML、结构化数据、字段定义、Schema。
- 格式要求:标准 Markdown 代码围栏(```json 或 ```yaml),顶层结构先给空骨架再填内容。
- 结构要求:字段名用 snake_case,必填/可选字段分别标注;枚举值列出全部合法取值。
- 粒度要求:嵌套不超过 3 层;数组元素给出完整示例项;时间统一 ISO 8601 格式。
- 填充要求:JSON 必须语法有效(可直接解析),禁止注释混入 JSON 体;Schema 附字段说明表。
