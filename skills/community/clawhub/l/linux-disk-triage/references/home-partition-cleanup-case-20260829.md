# /home 分区清理实测案例（2026-08-29，96%→60%，回收 72G）

> 前置技能：`linux-disk-space-triage` SKILL.md。本案例补充 **用户主目录（~）清理** 的
> 完整战术——SKILL.md 原有清单主要覆盖 / 分区（docker/日志），~ 清理有独立套路。

## 诊断阶段（先定位再动手）

```bash
# 一级目录定位（200G 主目录：du 全盘必超时）
du -x --max-depth=1 /home/<user> 2>/dev/null | sort -rh | head -30
# 超时处理：max-depth=1 本身较快；若仍超时（>120s），逐个大目录再 du -x --max-depth=1
# 注意 du 与 ls 不同：du 报告目录**实际占用**（含子目录），ls 的"总用量"是首层合计
```

**判定顺序**：先看一级目录大头 → 对每个可疑项查引用（grep 脚本/lsof/fuser）→ 无引用才删。
`du -x` 必须加 `-x`（不跨挂载点），避免把 /data 等独立分区算进来。

## 两轮清理策略（无争议先清，有争议查证后清）

### 第一轮：无争议缓存/垃圾（本案例回收 ≈53G）
| 项 | 大小 | 命令 |
|---|---|---|
| pip 缓存 | 13.9G | `rm -rf ~/.cache/pip` |
| npm 缓存 | 5.2G | `rm -rf ~/.npm/_cacache ~/.npm/_npx` |
| uv/yarn/go-build/puppeteer | 6G | `rm -rf ~/.cache/uv ~/.cache/yarn ~/.cache/go-build ~/.cache/puppeteer` |
| 浏览器缓存 | 1.1G | `rm -rf ~/.cache/mozilla ~/.cache/google-chrome` |
| 回收站 | 1.3G | `rm -rf ~/.Trash/*` |
| 已安装软件安装包 | 1.5G | `~/下载`、`~/Downloads` 下的 .deb/.rpm（Feishu/chrome/code/cursor 已装） |
| 模型导入源文件 | 6.7G | `~/.cache` 下 `.fr-*` 解压残留、`~model_imports` 已导入 Ollama 的 GGUF |

**`.fr-*` 目录识别**：`~/.cache/.fr-<随机>` 是**安装包解压残留**（本机 7.4G，
`data/opt/bytedance` = 飞书 .deb 解压产物）。删除前 `lsof <dir>` 确认无进程持有。

**模型导入源文件删除条件**：`docker exec ollama ollama list` 中已出现该模型（如 gemma4:12b）
→ 源 GGUF 可删；未导入完成绝不可删。

### 第二轮：有争议项（查引用后清，本案例回收 ≈19G）
| 项 | 大小 | 判定 |
|---|---|---|
| SDXL-turbo 冗余单文件 | 19.5G | diffusers 目录格式在用，同目录 fp32/fp16 单文件 .safetensors 未被引用 |
| finetune/venv | 5.2G | `ps aux | grep finetune` 无进程引用，venv 可重建 |
| Hermes 旧备份 | 2.2G | 0.9.0 时代备份，当前已 0.20.x |
| Go 模块缓存 | 2.2G | 纯缓存（见下方坑） |
| 智能体平台 3月备份 | 952M | 有每周日自动备份兜底 |
| 误建 conda 环境 "ls" | 861M | `conda env list` 无活动引用，`conda env remove -p ~/ls` |

## 模型重复文件检测（最重要的技巧）

diffusers 目录格式模型常同时存在**目录版 + 单文件版**，可能差 20G+：
```bash
# 1. 看脚本实际加载路径（from_pretrained 目录？还是 safetensors 单文件？）
grep -n 'from_pretrained\|MODEL_DIR' ~/scripts/*.py
# 2. 查单文件是否被任何代码引用
grep -rl 'sd_xl_turbo_1.0.safetensors' ~/scripts ~/projects ~/.hermes/cache 2>/dev/null
# 3. 无人引用 → 删；有人引用 → 保留
```
本机实测：`sd_batch_gen.py` 用 `from_pretrained("~/models/sdxl-turbo")`（读目录内 unet/vae/
text_encoder 分片），同目录 `sd_xl_turbo_1.0.safetensors`(13G fp32) + `..._fp16.safetensors`(6.5G)
均未被引用 → 可删。**单文件是 fp32/fp16 全量模型，目录版是同一模型的分片副本**——两者选一保留即可。

## 坑（本案例实测新增）

1. **Go 模块缓存只读（rm 报"权限不够"）**：`~/go/pkg/mod` 下文件权限 0444（Go 设计如此），
   `rm -rf ~/go/pkg` 每个文件都报权限错误。**正确：`go clean -modcache`**。
   若 go 不在 PATH：`chmod -R u+w ~/go/pkg && rm -rf ~/go/pkg`（回退方案）。
2. **du 全盘超时**：200G 主目录 `du -xsh ~` 120s 超时 → 改用 `--max-depth=1` 逐层定位。
3. **删除前必查引用**：模型/venv/环境/备份类，一律先 `grep -rl`（代码引用）+
   `ps aux | grep`（进程引用）+ `lsof`（打开句柄）三重确认；conda 环境用
   `conda env list` 看是否活动。
4. **备份删除判断**：软件旧备份（hermes-agent 0.9.0）→ 已无回滚价值可删；业务数据备份
   → 确认有更新备份兜底（本机每周日 cron 自动备份）才可删。
5. **清理后复检**：每轮结束后 `df -h` 报告前后对比；两轮合计报告总回收量。

## 验证
- 清理后 `df -h /home`：192G → 120G 使用（96% → 60%），可用 8.8G → 81G
- 出图功能验证：`~/scripts/sd_batch_gen.py` 冒烟跑 1 张确认模型目录版完好
- OLLAMA 模型验证：`docker exec ollama ollama list` 确认 gemma4:12b 等仍可列出
