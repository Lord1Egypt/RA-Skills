# 历史错误与防御

## C1 标题自拟 / 截短 / 改写
- 防御：标题规则单独文档 + `compile_check.sh` 校验 H1 与文件名

## C2 eb-clipper 脏数据
- 防御：`compile_clipper_fix.sh` 先行修复 `Value:`、YAML 闭合、图片混入 YAML

## C4 frontmatter 字段错误
- 防御：`compile_frontmatter_gen.sh` 统一生成，`compile_check.sh` 统一校验

## C6 wikilink 歧义
- 防御：`original` 和 `compiled_version` 一律写带路径 wikilink

## C7 跳过知识扫描
- 防御：Step 0.3 强制写 checkpoint，并要求 `related_wiki` 明确有值或空数组

## C8 图片归档遗漏
- 防御：`compile_archive.sh` 统一迁移图片并做回读验证

## C9 批量编译质量漂移
- 防御：一篇走完再做下一篇；每篇单独 task log

## C10 文件名与内容不符
- 防御：`compile_filename_check.sh` 强制主题核对；默认只输出建议改名，只有显式传 `--apply` 才允许落盘改名，并记决策日志

## C11 FAIL 后自作主张继续
- 防御：Step 5 FAIL 时写 blocked checkpoint，Step 6 入口必须检查 blocked 状态

## C12 compiled_version 写错
- 防御：`compile_archive.sh` 先 Glob 真文件名，再写回并回读验证

## C13 扫描做了但没落到字段
- 防御：Step 0.3 的 audit 必须检查 `related_wiki` 字段已明确写出
