# 产物输出协议

## 最终交付物

本 skill 的最终交付物为 HTML 报告，由 `linkfox-report-generator` 生成并落盘到：
```
<cwd>/linkfox/<YYYY-MM-DD>/<session>/reports/ip-full-detection-<timestamp>.html
```

## 中间数据文件

### AIGC 预筛结果
```
<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/aigc-prescreen-<timestamp>.json
```

### 专业检测 JSON（仅模糊项）
```
<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-ruiguan-<detection-name>-<timestamp>.json
```

## 对话输出

agent 在对话中返回：
1. AIGC 预筛概览摘要（1 段表格：6 项 verdict + 跳过/执行标注）
2. 积分节省统计（N 项跳过专业检测，M 项执行专业检测）
3. 总体风险等级摘要（1 段表格）
4. 高风险项关键发现（文字摘要）
5. 报告完整路径
6. AIGC 预筛数据文件完整路径
7. 专业检测 JSON 数据文件完整路径（仅模糊项）

## 路径规范

所有落盘通过 `scripts/linkfox_paths.py` 的 `resolve_report_path` 和 `resolve_data_path` 函数，禁止裸写绝对路径或 /tmp。
