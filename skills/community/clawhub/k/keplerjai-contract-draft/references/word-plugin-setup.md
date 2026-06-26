# Word 插件准备

这份文档只负责说明 `word-docx` 相关的环境准备逻辑。

## 默认顺序

1. 检查 `word-docx` 是否已可用
2. 如未安装，检查 `clawhub` 是否已可用
3. 如未安装 `clawhub`，先用 `npm` 安装
4. 检查 ClawHub 登录态
5. 如未登录，先完成登录
6. 执行 `clawhub install word-docx`
7. 再尝试调用 Word 插件能力

## 默认原则

当运行环境缺少 `word-docx` 时：

1. OpenClaw 应优先尝试自行补齐环境
2. 不要立刻把安装责任推给用户
3. 只有自动准备明确失败后，才退回纯文本兜底

## 兜底模式

如果插件准备失败，至少应输出以下一种或多种内容：

1. 字段清单
2. 替换正文草稿
3. 缺失信息列表
4. 后续手工填充计划

## 常用命令

- `npm i -g clawhub`
- `clawhub login`
- `clawhub whoami`
- `clawhub install word-docx`
