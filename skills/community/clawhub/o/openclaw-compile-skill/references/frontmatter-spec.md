# Frontmatter 规范

共享字段定义见本文件与 `references/compile-template.md`。

## 编译 Skill 额外约束

- `compiled_by`：由脚本接收参数生成，必须是带双引号的非空字符串
- `author`：社交账号作者应统一为 `@name` 形式
- `original`：必须写带路径 wikilink，例如 `[[Knowledge/原材料仓库/标题]]`
- `keywords`：必填，优先复用 `Knowledge/_INDEX.md` 中已有主题词；若不存在合适词，再由 Agent 自行设计
- `tags`：可为空；如填写，必须是扁平字符串数组
- `related_wiki`：必须是扁平字符串数组，例如 `[[主题]] | rough`
- `compiled_version`：只存在于原材料 frontmatter，且必须指向真实存在的中转站文件

## 单一信源

- 字段集合：`_shared/frontmatter-spec.md`
- 编译模板：`references/compile-template.md`
- 机械校验：`{baseDir}/scripts/compile_check.sh`
