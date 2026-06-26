# Prompts 目录说明

本目录存放快导(KD) Skill 10步流程的子任务提示词模板。

## 目录结构

```
prompts/
├── step1_search_trending.md      # 子任务1：搜索目标平台爆款
├── step2_read_rules.md            # 子任务2：读取平台规则
├── step3_search_external.md       # 子任务3：搜索外网平台
├── step4_check_duplicates.md      # 子任务4：同质化检查
├── step5_scan_format.md           # 子任务5：格式检查
├── step6_generate_scripts.md      # 子任务6：生成脚本
├── step7_validate_scripts.md      # 子任务7：合理性检查
├── step8_append_to_excel.md       # 子任务8：更新文案库
├── step9_verify_write.md          # 子任务9：全面检查对比
├── step10_generate_report.md      # 子任务10：提交报告
└── README.md                      # 本文件
```

## 文件命名规则

```
step{序号}_{任务简称}.md
```

**示例：**
- `step1_search_trending.md` - 子任务1，搜索爆款
- `step6_generate_scripts.md` - 子任务6，生成脚本

## 文件内容结构

每个提示词文件包含以下部分：

1. **任务目标** - 该子任务的目标说明
2. **输入变量** - 需要动态填充的数据（`{{变量名}}`）
3. **执行流程** - 该子任务的执行步骤
4. **输出格式** - 期望的输出结构和示例
5. **注意事项** - 执行时的关键点
6. **错误处理** - 异常情况的处理方式

## 使用方式

提示词文件由 `ScriptGenerator` 类动态读取和使用：

```python
from script_generator import ScriptGenerator

# 生成脚本时自动加载 step6_generate_scripts.md
generator = ScriptGenerator(platform="xiaohongshu")
prompt = generator.load_prompt("step6", {
    "platform": "xiaohongshu",
    "trending_titles": [...],
    "rules_summary": {...}
})
```

## 10步流程概览

| 步骤 | 名称 | 核心任务 | 输出 |
|:---:|:---|:---|:---|
| 1 | 搜索目标平台爆款 | 搜索并选定4个爆款 | 爆款列表+主题 |
| 2 | 读取平台规则 | 提取7项关键规则 | 规则摘要 |
| 3 | 搜索外网平台 | 搜索并选定1个外网爆款 | 外网爆款（可选）|
| 4 | 同质化检查 | 检查已有脚本，确定避开方向 | 需避开主题 |
| 5 | 格式检查 | 读取Excel实际格式 | 格式参数 |
| 6 | 生成脚本 | 生成4-5条差异化脚本 | 完整脚本 |
| 7 | 合理性检查 | 检查7项合理性，直接修改 | 检查清单+修改记录 |
| 8 | 更新文案库 | 脚本写入Excel | 写入确认 |
| 9 | 全面检查对比 | 验证格式、内容、位置 | 验证报告 |
| 10 | 提交报告 | 生成并保存执行报告 | Markdown报告 |

## 提示词变量规范

### 通用变量

| 变量名 | 说明 | 示例 |
|:---|:---|:---|
| `{{platform}}` | 平台英文标识 | xiaohongshu, douyin, shipinhao |
| `{{platform_name}}` | 平台中文名 | 小红书, 抖音, 视频号 |
| `{{task_date}}` | 任务日期 | 2026-04-22 |

### 子任务特定变量

每个提示词文件会定义自己的输入变量，详见各文件。

## 自定义提示词

您可以根据实际运营经验修改提示词：

```bash
# 编辑子任务6的提示词
nano prompts/step6_generate_scripts.md

# 编辑子任务7的提示词
nano prompts/step7_validate_scripts.md
```

**注意：** 修改提示词可能影响生成脚本的质量，建议先备份原文件。

## 版本管理

提示词文件版本与Skill版本一致：

| Skill版本 | 提示词版本 | 更新日期 |
|:---:|:---:|:---:|
| 1.0.0 | 1.0.0 | 2026-04-22 |

## 相关文件

- **配置：** `config/templates.json` - 提示词模板配置
- **脚本：** `scripts/script_generator.py` - 提示词加载器
- **流程：** `config/workflow.json` - 10步流程定义

## 常见问题

**Q: 提示词文件可以删除吗？**

A: 不建议删除，会导致对应子任务无法执行。可以修改内容，但不要删除文件。

**Q: 如何添加新的子任务提示词？**

A: 按照命名规则创建新文件（如 `step11_xxx.md`），并在 `config/workflow.json` 中添加对应步骤。

**Q: 提示词中的变量如何填充？**

A: 由 `ScriptGenerator` 类自动从子任务结果中提取并填充，无需手动处理。
