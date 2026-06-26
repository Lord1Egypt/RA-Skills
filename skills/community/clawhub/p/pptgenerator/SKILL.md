---
name: pptultra
description: 支持HTML格式PPT的智能生成与编辑，涵盖通用演示、总结汇报、教学课件、公众演讲等场景，提供换风格、换语种、文本润色、信息核验等功能；当用户需要生成PPT/演示文稿/幻灯片，或对现有PPT执行换风格/换语种/润色/核验时使用。
dependency:
  python:
    - requests>=2.28.0
---

# ✦ PPTUltra - AI 智能演示文稿生成引擎

> Powered by [pptultra.com](https://pptultra.com)

支持 HTML PPT 的智能生成与编辑，涵盖通用演示文稿、总结汇报、教学课件、公众演讲等场景。

## 功能列表

| 功能键 | 类型 | 功能名称 | 说明 |
|---|---|---|---|
| `ppt` | 生成 | 通用PPT创作 | 默认功能 |
| `summary-report` | 生成 | 总结汇报 | 生成总结汇报类 PPT |
| `teaching-courseware` | 生成 | 教学课件 | 生成教学课件 |
| `public-speaking` | 生成 | 公众演讲 | 生成演讲型 PPT |
| `restyle-all` | 编辑 | 一键换风格 | 整套 PPT 替换风格 |
| `translate-all` | 编辑 | 一键换语种 | 整套 PPT 语种切换 |
| `polish-text` | 编辑 | 文本润色 | 润色已有内容 |
| `fact-check` | 编辑 | 信息核验 | 核验并修正内容 |

## 触发条件

用户出现以下需求时触发：
- 生成 PPT / 演示文稿 / 幻灯片
- 生成总结汇报、教学课件、公众演讲对应的 PPT
- 对现有 PPT 执行换风格、换语种、文本润色、信息核验

默认使用 `ppt` 功能；只有在用户明确提出其他功能时，才切换对应 `--skill`。

## 执行流程

### 第一步：确认功能

- 新建 PPT → 默认 `ppt`
- 用户说"总结汇报 / 教学课件 / 公众演讲" → 切到对应功能键
- 用户说"换风格 / 换语种 / 润色 / 核验" → 切到对应编辑类功能键

### 第二步：调用脚本

**脚本路径：** `scripts/generate_ppt.py`（相对于本 skill 目录）

**依赖安装（首次使用）：**
```bash
pip install requests
```

**生成类示例：**
```bash
# 通用 PPT 创作（默认）
python scripts/generate_ppt.py "帮我生成一个关于 AI 的 PPT"

# 总结汇报
python scripts/generate_ppt.py "帮我写季度工作总结" --skill summary-report

# 教学课件
python scripts/generate_ppt.py "Python 入门教学" --skill teaching-courseware

# 公众演讲
python scripts/generate_ppt.py "AI 对未来教育的影响" --skill public-speaking
```

**编辑类示例：**

编辑类建议同时提供 `--current-ppt`、`--operations`、`--size` 参数以获得最佳效果。

```bash
# 一键换语种
python scripts/generate_ppt.py "把当前 PPT 改成英文版" \
  --skill translate-all \
  --operations "整套换成英文" \
  --size "1366*768" \
  --current-ppt ~/Desktop/current_ppt.json

# 文本润色
python scripts/generate_ppt.py "请润色第2页标题和导语" \
  --skill polish-text \
  --operations "第2页标题和导语润色，更专业简洁" \
  --size "1366*768" \
  --current-ppt ~/Desktop/current_ppt.json

# 一键换风格
python scripts/generate_ppt.py "改成深色科技风" \
  --skill restyle-all \
  --operations "整套改成深色科技风" \
  --size "1366*768" \
  --current-ppt ~/Desktop/current_ppt.json
```

### 第三步：等待生成

- 生成通常需要 **5-15 分钟**，不要中途中断
- 脚本会自动处理流式响应、去噪和结果提取

### 第四步：呈现结果

- 优先展示摘要和 PPT 分享页链接
- 如返回分享页链接，明确高亮给用户
- 如返回 Markdown 文本，直接展示

## 常见问题

**Q: 返回内容为空怎么办？**
A: 请稍后重试。如果问题持续出现，检查网络连接。

**Q: 怎么查看支持的功能列表？**
A: 直接运行不带参数的命令：`python scripts/generate_ppt.py`

**Q: 编辑类功能效果不理想？**
A: 请确保同时提供 `--current-ppt`（当前 PPT 内容）、`--operations`（操作说明）和 `--size`（尺寸）三个参数。

## 使用限制

- 仅支持 HTML 版 PPT 的生成与编辑
- 不支持 PPTX 格式编辑
- 不支持演讲稿与转场视频
