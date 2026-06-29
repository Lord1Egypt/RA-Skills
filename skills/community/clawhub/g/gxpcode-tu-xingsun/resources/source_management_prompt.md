# GxpCode-制药法规跟踪 — 源管理 Prompt

当用户输入以下关键词时执行：`源管理` `管理法规源` `打开源面板`

## 执行步骤

1. 启动面板服务：

```bash
python "${SKILL_DIR}/scripts/source_manager.py"
```

2. 服务启动后，使用 `present_files` 打开 `http://localhost:8888`

3. 用户在面板中操作：
   - 按 jurisdiction 分组查看所有法规源
   - 开关拨钮切换单个源的启用/禁用
   - 每组支持「全部启用」「全部禁用」
   - 搜索框按名称/URL 过滤
   - 点击「保存」后通过 POST 写回 `sources.yaml`

4. Step 1（`step1_rss.py` / `step1_web.py`）会自动跳过 `enabled: false` 的源。

## CLI 快捷操作

不用启动面板时，直接命令行操作：

```bash
python scripts/source_manager.py list              # 表格输出所有源及状态
python scripts/source_manager.py status            # 按机构统计活跃源
python scripts/source_manager.py toggle "源名"      # 切换单个源的启用/禁用
python scripts/source_manager.py enable "源名"      # 启用
python scripts/source_manager.py disable "源名"     # 禁用
```

## 数据格式

`sources.yaml` 中各源均带 `enabled` 字段：

```yaml
sources:
  - name: CDE-指导原则
    enabled: true    # false 时跳过
    type: web
    jurisdiction: CDE
    ...
```
