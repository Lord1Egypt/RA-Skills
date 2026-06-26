# 命令参考

## 全局选项

```bash
.venv/bin/python3 scripts/skill.py [--env-file path/to/env.sh] <子命令> [子命令选项]
```

| 参数 | 说明 | 默认 |
|------|------|------|
| `--env-file` | 指定 env.sh 路径，**强制覆盖**已有环境变量 | 自动查找 |

## info — 打印当前 VLM 配置

```bash
.venv/bin/python3 scripts/skill.py info
```

仅 stderr 输出 provider / model / base_url / 超时设置；exit 0 表示就绪，exit 1 表示未配置。

## parse — 同步解析（推荐入口）

```bash
.venv/bin/python3 scripts/skill.py parse \
  --input <pdf_or_image> \
  --output <result_dir> \
  [--parse-mode normal|detail] \
  [--pages 1-10,15] \
  [--model doubao-1.5-vision-pro] \
  [--dpi 200] \
  [--save-images] \
  [--password ****]
```

| 参数 | 说明 | 默认 |
|------|------|------|
| `--input` | PDF / 图片 路径（必填） | — |
| `--output` | 结果目录（必填，自动创建） | — |
| `--parse-mode` | `normal` / `detail` | `normal` |
| `--pages` | 页范围 `1-10,15,20-25` | 全部页 |
| `--model` | 覆盖默认模型名 | 各 provider 默认 |
| `--dpi` | 渲染 DPI | 200 |
| `--save-images` | 保留渲染后的 PNG 到 `images/` | false |
| `--password` | 加密 PDF 密码 | — |

**stdout**：一行 JSON
```json
{"status":"COMPLETED","task_id":"task_xxx","output_dir":"...","parse_mode":"normal","model":"...","total_pages":10,"page_count":10,"table_count":5,"block_count":42,"failed_pages":[],"wall_time_seconds":24.1,"preview":"..."}
```

**stderr**：渲染进度、模型调用、重试日志。

**Exit code**：`0` 全部成功；`1` 失败；`PARTIAL` 时仍为 `0`（在 stdout 的 status 字段标记）。

## submit / check-and-notify — 异步语义

为兼容 byted-las 的"提交 → 轮询"工作流，把 `parse` 拆为两步。**本地实现下 `check-and-notify` 同步执行**，`--poll` 是 no-op。

```bash
# 1. 提交：生成 task_id，把参数写入 <output_dir>/task.json
.venv/bin/python3 scripts/skill.py submit \
  --input <pdf> --parse-mode detail \
  [--output /tmp/pdf_parse_xxx]
# stdout: {"task_id":"task_xxx","output_dir":"...","eta":"...","total_pages":10,...}

# 2. 执行
.venv/bin/python3 scripts/skill.py check-and-notify \
  --task-id <id> --output <same_dir> --poll
# stdout: 同 parse 的 summary
```

后续若把执行体替换成远端异步算子（如真正的 LAS operator），只需改 `cmd_check_and_notify` 内部逻辑，CLI 接口不变。

## 与评测脚本配合

```bash
# 批跑样本
for pdf in samples/documents/*.pdf; do
  doc_id=$(basename "$pdf" .pdf)
  .venv/bin/python3 scripts/skill.py parse \
    --input "$pdf" --output "samples/outputs/$doc_id" --parse-mode normal
done

# 评测对比 GT
python3 evaluation/scripts/run_eval.py \
  --pred_dir samples/outputs \
  --gt_dir evaluation/gt_templates/annotated \
  --report_dir evaluation/reports
```
