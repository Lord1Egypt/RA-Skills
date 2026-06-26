# Multi Search Engine

## 基本信息

- **名称**: multi-search-engine
- **版本**: v2.1.0
- **定位**: 多搜索引擎 URL 编排与对比检索 Skill
- **特点**: 无 API Key、可审计、支持 compare / preset / 高级搜索语法

## 本次增强

- 从“链接清单”升级为“可执行搜索编排工具”
- 新增 `scripts/build_search_urls.py`
- 新增预设：balanced / cn-research / privacy / knowledge
- 新增输出格式：text / markdown / json
- 新增站内、文件类型、精确短语、排除词、OR 组合
- 新增时间、语言、地区、SafeSearch 参数
- 新增 README / SELF_CHECK / examples / tests / resources

## 典型用法

```bash
python3 scripts/build_search_urls.py --query "openclaw skills" --compare google,ddg,brave
python3 scripts/build_search_urls.py --query "量化投资" --preset cn-research --time week
python3 scripts/build_search_urls.py --query "100 USD to CNY" --engine wolframalpha --format json
```

## 安全结论

- 不自动联网
- 不执行外部命令下载
- 不读取敏感环境变量
- 仅基于本地模板生成 URL
