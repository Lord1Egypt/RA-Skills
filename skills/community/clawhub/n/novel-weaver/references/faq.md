# FAQ / 常见问题

## 一、参数错误

### Q: 运行脚本时报 "用法: ..." 错误

**原因：** 命令行参数数量或顺序不对。

**修复：** 查阅脚本的 docstring 或用 `--help` 查看正确用法。
```bash
python novel_workflow_engine.py --help
python novel_state_manager.py --help
```

### Q: `plan-chapter` 报 "subs_json 格式错误"

**原因：** 传入的 JSON 字符串格式不正确（少引号、多逗号等），或直接在命令行中嵌入 JSON

**修复：**
- **推荐方案**：写 JSON 到文件后用 `@` 加载，避免 shell 转义问题
  ```bash
  python novel_workflow_engine.py plan-chapter <state_path> <L##> @data/subs_<L##>.json
  ```
- 或用 `--generate` 生成模板文件再修改：
  ```bash
  python novel_workflow_engine.py plan-chapter <state_path> <L##> --generate
  # 输出同时自动写入 data/subs_<L##>_template.json
  ```
- 确保 JSON 是合法的数组格式，每项含必填 `writing_prompt`（≥50字符）：
  ```json
  [{"s_key":"S01","title":"...","summary":"...","tone":"...","writing_prompt":"..."}]
  ```

### Q: `context_loader` 报 "子结构未注册"

**原因：** 尝试加载的子结构尚未通过 `plan-chapter` 注册到 `novel_state.json`。

**修复：**
```bash
python novel_workflow_engine.py plan-chapter <state_path> <L##> '<subs_json>'
```
然后重新运行 context_loader。

## 二、依赖错误

### Q: 运行脚本时报 "ModuleNotFoundError"

**原因：** 缺少 Python 依赖模块。

**修复：** 核心功能仅依赖 Python 标准库（json/os/sys/re/subprocess），不需要 pip install。
可选增强功能需额外安装：
- **BERT 语义检查**（finalize-chapter 第5步）：
  ```
  pip install sentence-transformers -i https://mirrors.aliyun.com/pypi/simple/
  ```
- **DeepSeek-R1-Distill-Qwen-1.5B 推理审核**（finalize-chapter 第6步，CPU 可跑）：
  ```
  pip install transformers torch -i https://mirrors.aliyun.com/pypi/simple/
  ```
两者均未安装时自动跳过，不影响现有流程。

### Q: context_loader 报 "子结构已完成，禁止重复写作"

**原因：** 尝试加载一个已经写完（status=done）的子结构。

**修复：** 用 next-step 命令查找下一个待写的子结构：
```bash
python novel_workflow_engine.py next-step <state_path>
```

### Q: 提示 "novel_state.json not found"

**原因：** 数据目录未初始化或路径不对。

**修复：** 确保 `<state_path>` 指向正确的路径：
```
~/.workbuddy/skills/.standardization/novel-weaver/projects/<项目名>/data/novel_state.json
```
可用 list-projects 查看所有已创建的项目：
```bash
python novel_workflow_engine.py list-projects
```

## 三、环境错误

### Q: Windows 下运行报编码错误（gbk 相关）

**原因：** Python 默认编码与 UTF-8 文件不兼容。

**修复：**
```bash
set PYTHONUTF8=1
```

### Q: 子结构写入时断电，文件会丢吗？

**不会。** `novel_atomic_writer.py` 每写入一行就调用 `os.fsync()`，确保数据落盘。
```bash
# 写入完成后自动追加编号标记，可通过文件内容恢复进度
cat <chapter_dir>/<sub_key>.txt | wc -l
```

## 四、流程异常

### Q: `set-phase` 报 "拒绝推进"

**原因：** pipeline 门禁检查未通过，前置步骤尚未完成。

**修复：**
```bash
# 查看当前门禁状态
python novel_pipeline_gate.py status <state_path>
# 确认缺失的门禁后按顺序完成
# fidelity → ending_verify → complete
```

### Q: 写作时 context_loader 输出了 "未知" 标题

**原因：** 子结构未通过 `plan-chapter` 注册。此情况已改为报错退出。

**修复：** 先运行 `verify-chapter` 确认所有子结构已注册。

### Q: 想知道当前写作进度

```bash
python novel_workflow_engine.py next-step <state_path>
```

### Q: context_loader 报 "上一子结构未标记完成"

**原因：** 子结构写作必须串行。上一子结构的文件虽已存在，但未通过 `write-sub` 管道写入 `novel_state.json`，state 显示为 pending。

**修复：** 运行 write-sub 完成上一子结构的 state 标记，再重新加载下一子结构：
```bash
cat chapters/<L##>/<S##>.txt | python novel_workflow_engine.py write-sub <state_path> <L##> <S##>
```

### Q: write-sub 提示 "字数 < 篇幅下限" 或 "字数 > 上限+15%"

**原因：** write-sub 写入后自动校验字数是否在篇幅目标范围内。中篇目标 1,500-2,000，校验上浮至 2,300。低于下限出 WARN，超上限+15% 出 INFO，范围内出 OK。

**修复：**
- WARN（低于下限）：内容过少，建议补充
- INFO（超上限+15%）：篇幅过长，注意控制
- OK：字数达标，无需操作
- WARN/INFO 均为提示性，**不阻断写入**，不影响写作进度

### Q: finalize-chapter 中的「语义检查」和「推理审核」是什么？

**语义检查（第5步）：** 基于 BAAI/bge-small-zh-v1.5（33MB），检测：
- overview-vs-content 语义对齐（正文是否真的在讲概述规划的内容）
- 子结构间语义跳跃（两段之间话题是否断裂）
- 情绪偏离+同义冗余+跨章主题延续辅助提示

**推理审核（第6步）：** 基于 DeepSeek-R1-Distill-Qwen-1.5B（transformers，~1GB，CPU 可跑），检测：
- 因果合理性（事件是否有前文铺垫）
- 人物行为一致性（行为是否符合人格配置）
- 情绪弧自然度（情绪转变是否合理）
- 对话匹配度（对话是否符合角色身份）
- 论证可靠性（推理是否成立）

两者均有模型时执行，无模型时自动跳过，不影响现有流程。

### Q: 安装 BERT 语义检查

```bash
pip install sentence-transformers -i https://mirrors.aliyun.com/pypi/simple/
HF_ENDPOINT=https://hf-mirror.com python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-zh-v1.5')"
```

### Q: 安装推理审核模型

```bash
pip install transformers torch -i https://mirrors.aliyun.com/pypi/simple/
HF_ENDPOINT=https://hf-mirror.com python -c "from transformers import AutoModel; AutoModel.from_pretrained('deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', trust_remote_code=True)"
```

### Q: 出错了怎么办？

按错误类型分类处理：

**参数错误（命令行参数写错了）**
- 检查章节目录是否存在：`ls chapters/`
- 检查章节 ID 格式：`L01`、`L02`（两位数字）
- 检查项目路径是否正确：`python novel_workflow_engine.py list-projects`

**依赖错误（Python 包缺失）**
- BERT 语义检查：`pip install sentence-transformers -i https://mirrors.aliyun.com/pypi/simple/`
- 推理审核：`pip install transformers torch -i https://mirrors.aliyun.com/pypi/simple/`
- 模型下载：设置 `HF_ENDPOINT=https://hf-mirror.com` 后重试

**环境错误（文件/路径问题）**
- novel_state.json 损坏 → 检查 data/novel_state.json 是否为合法 JSON
- 子结构文件缺失 → 运行 `verify-chapter` 检查
- 缓存不完整 → 删除 `~/.cache/huggingface/hub/` 对应条目重新下载
- GitHub 网络不通 → 使用国内镜像：`HF_ENDPOINT=https://hf-mirror.com`
