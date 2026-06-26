# 输出规则

这份文档只负责说明运行产物应该落到哪里，以及输出什么。

## 输出目录

运行产物应写入目标 agent workspace 下、与 skill 同名的目录：

- `<agent_workspace>/keplerjai-contract-draft`

不要把 skill 根目录当作主要输出目录。

## 路径优先级

优先级应为：

1. 显式传入的 `output_dir`
2. job spec 中的 `agent_workspace`
3. 环境变量
4. OpenClaw 本机配置中的 agent workspace
5. 从 spec 路径反推的 workspace
6. 最后才是当前工作目录兜底

不要把某台机器上的绝对路径写死为默认值。

## 最低输出产物

至少应输出：

1. 一份新的 `.docx` 草稿
2. `未决事项清单.md`
3. `run-summary.json`
4. `validation-report.json`

## 输出命名

Word 草稿默认命名：

1. `<模板标题>_草稿.docx`
2. 若同名已存在，则依次为 `_v2`、`_v3` 等
