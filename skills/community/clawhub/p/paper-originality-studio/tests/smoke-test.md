# smoke-test

在 skill 根目录执行以下命令。

## 1. 基础扫描

```bash
python3 scripts/originality_toolkit.py scan examples/sample-manuscript.txt --json-out /tmp/scan.json --report-md /tmp/scan.md
```

预期：

- 退出码为 0
- 生成 `/tmp/scan.json`
- 生成 `/tmp/scan.md`
- 报告中能看到“风险等级”“Recommendations”“Template / Cliche Hits”

## 2. 原稿 / 改稿比较

```bash
python3 scripts/originality_toolkit.py compare examples/sample-manuscript.txt examples/sample-revised.txt --json-out /tmp/compare.json --report-md /tmp/compare.md
```

预期：

- 退出码为 0
- 生成 `/tmp/compare.json`
- 生成 `/tmp/compare.md`
- 报告中能看到 `Sequence ratio`、`Shared 8-char shingle retention`

## 3. 章节切分

```bash
python3 scripts/originality_toolkit.py chunk examples/sample-manuscript.txt --out-dir /tmp/paper_chunks
```

预期：

- 退出码为 0
- 生成 `/tmp/paper_chunks/INDEX.md`
- 至少生成 3 个 chunk 文件

## 4. 提示生成

```bash
python3 scripts/originality_toolkit.py prompt --section 引言 --goal "自然学术化、保持引文边界"
```

预期：

- 退出码为 0
- 标准输出包含“先输出问题”“然后再输出改写版本”

## 5. 打包校验

```bash
python3 scripts/package_skill.py .
```

预期：

- 退出码为 0
- 输出一个 `.skill` 文件路径
