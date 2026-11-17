# 故障排除指南

> 本文件为 SKILL.md 故障排除的详细参考文档，按需加载。

---

## 一、常见问题与解决方案

### 1.1 专业教学标准检索

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 找不到专业教学标准 | 名称/代码错误或未发布 | 检查官方名称、用代码检索、用备选数据源 |
| 专业代码不匹配 | 输入了错误的代码格式 | 确认代码为6位数字（如 700206） |
| 层次不匹配 | 层次名称不规范 | 使用标准名称：中等职业教育/高等职业教育/职业教育本科 |

**调试命令**：

```bash
# 使用代码检索
python scripts/search_major.py --major "700206"

# 使用名称检索
python scripts/search_major.py --major "汽车运用与维修" --level "中等职业教育"
```

---

### 1.2 职业大典解析

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 大模型解析失败 | 内容过大或格式异常 | 使用分块文件、精确提示词、手动提取 |
| 职业代码找不到 | 代码格式错误或职业已更新 | 检查代码格式（X-XX-XX-XX），参考职业大典 |
| 解析结果不完整 | 提示词不够精确 | 参考 `prompt_templates.md` 优化提示词 |

**调试方法**：

```python
from scripts.occupation_dict_loader import get_occupation_dictionary

# 检查职业代码对应的大类
content = get_occupation_dictionary('6-22-02')
print(f"加载了 {len(content)} 字符")

# 检查是否包含目标职业
if '汽车维修工' in content:
    print("职业代码有效")
```

---

### 1.4 报告生成

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Markdown 表格不显示 | 格式错误（缺少分隔行） | 检查纵向表格是否有 `\|---\|` 分隔行 |
| Word 文档样式错误 | Pandoc 模板问题 | 检查 `references/reference.docx` 是否存在 |
| 表格编号跳跃 | 缺少某些表格 | 检查 `analysis_data.json` 数据完整性 |
| 能力动词不符合层次 | 层次适配未生效 | 检查 `metadata.education_level` 字段 |

**调试方法**：

```bash
# 验证报告
python scripts/validate_report.py --report temp/report.md --data temp/analysis_data.json

# 检查数据完整性
python -c "
import json
with open('temp/analysis_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print('典型任务数:', len(data.get('typical_tasks', [])))
print('行动领域数:', len(data.get('action_domains', [])))
print('学习领域数:', len(data.get('learning_domains', [])))
"
```

---

### 1.5 Pandoc 转换

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `pandoc: command not found` | 未安装 Pandoc | 安装 Pandoc 并添加到 PATH |
| 中文乱码 | 编码问题 | 确保文件使用 UTF-8 编码 |
| 表格格式丢失 | Word 模板问题 | 使用 `--reference-doc` 指定样式模板 |

**调试命令**：

```bash
# 检查 Pandoc 版本
pandoc --version

# 简单转换测试
pandoc temp/report.md -o output/test.docx

# 使用样式模板
pandoc temp/report.md --reference-doc=references/reference.docx -o output/report.docx
```

---

## 二、自动回退机制

当主要方法失败时，系统会自动尝试备选方案：

1. **本地文档查询失败** → 检查 `assets/esco_details_md/` 和 `assets/onet_details_md/` 是否存在
2. **MD文档不存在** → 报告警告，用户确认后继续
3. **所有本地文档缺失** → 报告错误，保留已获取的数据

---

## 三、日志标记说明

| 标记 | 含义 | 示例 |
|------|------|------|
| `[OK]` | 操作成功 | `[OK] 报告已生成` |
| `[INFO]` | 信息提示 | `[INFO] 加载数据文件` |
| `[WARNING]` | 警告（可继续） | `[WARNING] 以下任务未被覆盖` |
| `[ERROR]` | 错误（需处理） | `[ERROR] 文件不存在` |
| `[HINT]` | 建议提示 | `[HINT] 请检查数据文件` |

---

## 四、数据完整性检查

### 4.1 analysis_data.json 必需字段

```json
{
  "metadata": { "education_level": "..." },
  "major_info": { "major_name": "...", "major_code": "..." },
  "occupations": [...],
  "typical_tasks": [...],
  "action_domains": [...],
  "learning_domains": [...]
}
```

### 4.2 数据一致性约束

| 约束 | 验证方法 |
|------|----------|
| 表1 岗位与表2 一致 | `validate_report.py` 自动验证 |
| 表4 覆盖表2 所有任务 | `validate_report.py` 自动验证 |
| 学习领域对应行动领域 | 数据整合时检查 |

---

## 五、获取帮助

1. **查看日志**：检查终端输出的错误信息
2. **验证数据**：运行 `validate_report.py` 检查报告
3. **检查配置**：确认环境变量和依赖正确安装
4. **参考示例**：查看 `example/template.md` 示例报告