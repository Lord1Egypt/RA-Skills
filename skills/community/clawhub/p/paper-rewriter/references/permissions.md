> **何时读我**：安全审核、权限审计、或任何「这工具会连网/写哪里/装依赖吗」的质询。
> **最短路径**：读「只读取/只写入/零网络/零依赖」四条结论行即可；验证命令在节内可复制执行。
> **回 [INDEX](INDEX.md)**

## 权限与环境声明

供审核者、安全扫描与谨慎的用户查阅：

- 只**读取**你作为参数传入的文件路径（以及 stdin 管道输入，含 `--batch` 目录
  下的 .txt/.md/.docx/.pdf 文件）和技能自带的词表文件（`scripts/patterns_*.json`；
  若你用 `learn_guards.py` 建过用户守卫，还会读自己的 `scripts/user_guards.json`）。
  可自行验证：

  ```bash
  grep -rnE "urllib|requests|socket|subprocess|os\.environ" scripts/ || echo "clean"
  ```

  （本版实测输出 clean——承诺可复现，不是修辞。）
- 只**写入**你显式传入的输出路径：transform/compare/pipeline/plan/extract_terms
  的 `-o`/`--output`、`--suggestions`、`--html`、`--review`（detect.py 的审稿
  报告）、`--report`（check_terms.py / check_stats.py 的一致性报告）、`--track`（写 base.md +
  base.json 双文件）、`--bundle 目录`（v3.4.0 投稿自查包：在指定目录下创建带时间戳
  子目录，写 00-11 共 12 个编号件（00 写入清单〔权限自证：本次全部写入路径实测〕、01 自查报告 … 08 体检报告 dashboard、09 深改指令单、10 前后对照、11 守卫处方）与 README。一个派生例外：`pipeline --terms auto` 会额外写自动术语
  草稿 `<输出基名>.terms.auto.txt`（工具生成、未经人工确认，见工作流说明）。外加两个工具自有数据文件：`learn_guards.py
  add/from-text/remove` 写 `scripts/user_guards.json`（你自学的术语守卫，
  经瞬时 `.tmp` 原子替换落盘）；`--batch` 运行在**批量目录自身**写
  `.pr_batch_state.json`（v3.7.0 断点续传进度：每文件一条记录，
  经瞬时 `.tmp` 原子替换落盘；`--resume` 读取它，删掉即从头重建）及其并发锁
  `.pr_batch_state.json.lock`（v4.0.0，flock 并发锁文件）。除此之外无任何写入。
- **零网络访问**——无 HTTP 请求、无下载、无任何 API 密钥。
- **零第三方依赖**——仅 Python 标准库。
- **不读任何环境变量**；不创建子进程；不创建定时任务；唯一会写的临时文件
  是上述 `user_guards.json` 与 `.pr_batch_state.json` 原子替换各用的瞬时 `.tmp`。
- `selfcheck.py`（包内自检）只读技能包内文件（脚本/词表/文档）做环境/结构/冒烟/对账四段核查，不写盘、零网络、零子进程。
- `calibrate.py`（阈值校准证据工具）只读语料目录（缺省包内 `references/calib_corpus/`，或 `--corpus-dir` 指定）与包内模块，输出校准表，不写盘、零网络、零子进程。
- 测试语料与开发笔记仅存在于开发仓库，不随发布包分发。
