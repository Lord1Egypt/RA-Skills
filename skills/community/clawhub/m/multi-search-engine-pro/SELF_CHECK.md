# SELF_CHECK

## 规范检查

- [x] Skill 为独立目录
- [x] 包含 `SKILL.md`
- [x] `SKILL.md` 使用 YAML frontmatter
- [x] frontmatter 包含 `name` / `description` / `version`
- [x] 使用 `metadata.openclaw.requires`
- [x] 仅包含文本类文件，适合 ClawHub 发布

## 目录检查

- [x] `scripts/build_search_urls.py` 存在
- [x] `resources/engine-catalog.json` 存在并被脚本引用
- [x] `resources/search-operator-cheatsheet.md` 存在
- [x] `examples/example-prompt.md` 存在
- [x] `tests/smoke-test.md` 存在
- [x] `README.md` 存在

## 依赖检查

- [x] 仅依赖 `python3`
- [x] 无三方 Python 包
- [x] 无 API Key
- [x] 无额外系统服务要求

## 脚本检查

- [x] 有明确命令行参数
- [x] 有错误处理（未知引擎、空查询、参数冲突）
- [x] 有结构化输出
- [x] 可用于单引擎和多引擎 compare 模式

## 资源引用检查

- [x] 脚本读取 `resources/engine-catalog.json`
- [x] 文档引用 `resources/search-operator-cheatsheet.md`

## 安全检查

- [x] 不执行外部下载
- [x] 不执行 shell 拼接命令
- [x] 不调用远程 API
- [x] 不读敏感目录
- [x] 不写磁盘缓存
- [x] 不要求秘密环境变量

## 实用性检查

- [x] 覆盖中文与国际检索
- [x] 覆盖隐私搜索
- [x] 覆盖知识计算类入口
- [x] 支持高级搜索语法
- [x] 支持时间范围
- [x] 支持 compare 研究流程

## 可维护性评分

- 规范对齐：9/10
- 工程完整度：9/10
- 安全性：9/10
- 可复用性：9/10
- 发布就绪度：9/10

## 发布前人工复核

1. 抽查 5 个引擎 URL 模板是否仍有效
2. 抽查各引擎的时间参数是否仍兼容
3. 检查 README 与 SKILL.md 的版本号一致
4. 检查 `CHANGELOG.md` 是否记录本次增强
