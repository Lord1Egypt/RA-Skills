# Multi Search Engine

一个更完整的多搜索引擎编排 Skill。它不只是列出 17 个引擎，而是把“如何选引擎、如何拼搜索参数、如何做对比搜索、如何控制风险”做成了可复用工程。

## 功能亮点

- 17 个引擎统一管理，支持别名
- 国内 / 国际 / 隐私优先 / 知识计算预设
- 高级搜索运算符拼装：`site:`、`filetype:`、精确短语、排除词、OR 组合
- 时间范围映射：小时 / 天 / 周 / 月 / 年
- 语言、地区、SafeSearch、compare mode
- 输出 `text` / `markdown` / `json`
- 无 API Key，无远程安装，无高风险命令

## 适用场景

- 做中英文多源检索
- 同一主题多引擎交叉验证
- 先生成 URL，再决定打开哪些页面
- 做 PDF / 文档 / 站内 / 新闻时效检索
- 在隐私优先与主流搜索之间平衡

## 目录结构

```text
multi-search-engine/
├── SKILL.md
├── README.md
├── SELF_CHECK.md
├── config.json
├── metadata.json
├── CHANGELOG.md
├── scripts/
│   └── build_search_urls.py
├── resources/
│   ├── engine-catalog.json
│   └── search-operator-cheatsheet.md
├── examples/
│   └── example-prompt.md
└── tests/
    └── smoke-test.md
```

## 安装要求

- `python3`
- 无额外三方依赖
- 可离线生成 URL；只有实际打开 URL 时才联网

## 输入方式

最核心脚本：

```bash
python3 scripts/build_search_urls.py --query "openclaw skills"
```

常用参数：

- `--engine`：单个引擎，如 `google`
- `--compare`：多个引擎对比，如 `google,ddg,brave`
- `--preset`：`balanced` / `cn-research` / `privacy` / `knowledge`
- `--site github.com`
- `--filetype pdf`
- `--exact "large language model"`
- `--exclude ads`
- `--or-terms "openclaw,clawhub"`
- `--time day|week|month|year`
- `--lang zh-CN|en|ja`
- `--region cn|global`
- `--safe strict|moderate|off`
- `--format text|markdown|json`

## 输出示例

### 1. 代码站内搜索

```bash
python3 scripts/build_search_urls.py   --query "react hooks"   --site github.com   --engine google
```

输出：

```text
[google] https://www.google.com/search?q=site%3Agithub.com%20react%20hooks
```

### 2. PDF 对比搜索

```bash
python3 scripts/build_search_urls.py   --query "retrieval augmented generation"   --filetype pdf   --time year   --compare google,brave,ddg   --format markdown
```

### 3. 隐私优先预设

```bash
python3 scripts/build_search_urls.py   --query "privacy tools"   --preset privacy
```

### 4. 知识计算

```bash
python3 scripts/build_search_urls.py   --query "100 USD to CNY"   --engine wolframalpha   --format json
```

## 触发示例

- “帮我把这个主题同时在 Google、DuckDuckGo 和 Brave 上做对比搜索。”
- “我只想搜中文互联网内容，优先国内引擎。”
- “帮我构造一个只搜 GitHub 上 PDF 文档的查询。”
- “给我一个隐私优先的搜索方案。”
- “把这个计算题直接用 WolframAlpha 打开。”

## 工程设计说明

### 为什么保留 17 个引擎而不是继续扩表
引擎越多不代表越强，维护成本和失效率会一起上升。当前版本优先覆盖：
- 国内常见入口
- 国际主流入口
- 隐私引擎
- 知识型入口

### 为什么新增脚本而不是继续只写 SKILL.md
只靠文档列链接，模型每次都要自己拼 URL，容易遗漏编码、参数映射和安全边界。脚本把这些规则固定下来，能复用、可测试、可审计。

### 为什么默认不直接抓取页面
Skill 的职责是“编排搜索入口”，不是绕过网站风控。先生成 URL，再由代理决定是否访问，更安全，也更符合审计要求。

## 常见问题

### 支持真正的搜索结果聚合吗？
不直接抓取并聚合 SERP 内容。这个 skill 负责生成高质量入口与比较方案。

### 为什么有些时间过滤不一定完全一致？
不同引擎参数不统一。脚本只在已知可映射时附加参数；不支持的引擎会保守跳过。

### 为什么不内置代理、Cookie、抓取脚本？
这些都会明显提高发布风险、维护复杂度和安全审查成本。

## 风险提示

- 搜索引擎页面结构和参数可能变化，需要定期维护模板。
- 实际访问搜索页面时，目标站点仍可能记录请求。
- 某些引擎在不同地区可用性不同。

## 安全审计结论

- 无 `curl|bash`
- 无 base64 混淆执行
- 无远程脚本下载
- 无未声明依赖
- 文件写入范围仅限本地标准输出
- 网络访问不由脚本自动发起
