# huo15-openclaw-plan-form ｜ 计划表单统一与差异标注 Skill

---

<div align="center">

<img src="https://tools.huo15.com/uploads/images/system/logo-colours.png" alt="火一五Logo" style="width: 120px; height: auto; display: inline; margin: 0;" />

</div>

<div align="center">

<h3>打破信息孤岛，用一套系统驱动企业增长</h3>
<h3>加速企业用户向全场景人工智能机器人转变</h3>

</div>
<div align="center">

| 🏫 教学机构 | 👨‍🏫 讲师 | 📧 联系方式         | 💬 QQ群      | 📺 配套视频                         |
|:-----------:|:--------:|:------------------:|:-----------:|:-----------------------------------:|
| 逸寻智库 | Job | support@huo15.com | 1093992108  | [📺 B站视频](https://space.bilibili.com/400418085) |

</div>

---

## 正文内容

一个面向 OpenClaw 的 Skill：把客户发来的**各种格式**的排产 / 计划 / 需求 Excel 表单，自动识别、归类、转换成公司的**三个标准模板**，并支持新旧版本的差异标注。

### 它解决什么

客户来的表单五花八门——横向表、T+2 真单、滚动计划、物料到货计划、生产计划下发表，中英文混杂、单 sheet 或多 sheet、表头位置不一。本 Skill 让 AI 助手能：

1. **识别归类**：判断一个文件属于三个标准模板中的哪一个。
2. **转换填充**：把源文件内容熔解后填进对应模板，自动去掉模板里的示例数据、用规范名重命名；多个源文件可合并成一份。
3. **差异标注**：把「新文件」与库里「旧文件」按内容主键比对（文件名可不同），红底+批注标出变化、绿底标新增、单列删除项。

### 三个标准模板

| 模板 | 形态 | 典型来源 |
|---|---|---|
| **客户需求排产表** | 标识列 + 横向周/日需求量 + 合计 + 备注 | 横向表、T+2 真单/预报、滚动计划、物料到货 |
| **计划跟踪跟单表** | 按成品料号跟踪库存/已交/未交/结余/在制/欠料/预测 | 跟单个人表、到货进度表 |
| **工厂DIP排产计划表** | 工单维度 + 白班/夜班日排程 + UPH/人力/线体 | DIP 工单排产、配料明细、返工工单 |

### 目录结构

```
SKILL.md                      # Skill 入口：触发条件 + 5 步流程
requirements.txt              # pandas / openpyxl / xlrd
scripts/
  inspect_form.py             # 看任意表的结构（sheet/表头/日期列）
  classify_form.py            # 判定属于哪个模板（含置信度）
  extract_form.py             # 源文件 → 规范化 JSON（带列映射报告，可覆盖）
  fill_template.py            # 规范化 JSON → 统一模板（自动去示例、重命名、可合并多表）
  diff_forms.py               # 新旧文件比对 → 标注更新（红/绿/黄 + 批注）
  build_clean_templates.py    # 生成三个干净空白模板
  lib_forms.py / lib_xlsx.py  # 底层库（日期解析 / 别名匹配 / xlsx 渲染）
reference/
  templates_schema.json       # 三模板规范列 + 别名词典 + 分类关键词 + 主键（单一事实来源）
  classification.md           # 模板画像与判别指南
  workflow.md                 # 详细流程、--mapping 写法、边界处理
assets/templates/             # 三个已重命名、无示例数据的空白模板
用户文档/                      # 样例数据（开发/测试用）
```

### 快速开始

```bash
pip install -r requirements.txt

# 一个客户横向表 → 标准排产表，并与上一版比对
python3 scripts/classify_form.py "客户来的表.xlsx"
python3 scripts/extract_form.py  "客户来的表.xlsx" --template demand_schedule --out work/new.norm.json
python3 scripts/fill_template.py  work/new.norm.json --out-dir out/
python3 scripts/diff_forms.py     --new work/new.norm.json --old "库里/上一版.xlsx" --template demand_schedule --out "out/差异标注.xlsx"
```

详细流程见 [`SKILL.md`](SKILL.md) 与 [`reference/workflow.md`](reference/workflow.md)。

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>

---
