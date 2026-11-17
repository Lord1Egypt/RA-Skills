# 场景举例合集 — mu-excel-toolbox

> 22 个功能的真实使用场景，帮助理解何时用哪个工具

---

## 1. 📋 智能预览（peek.py）

**场景：** 收到同事发来的 Excel，想快速了解里面有什么
```
用户：帮我看看这个文件有什么内容
→ peek.py report.xlsx --rows 3
→ 输出：3个Sheet、各Sheet的列名和行数、前3行数据预览
```

**场景：** 数据量很大的文件，想知道有多少行再决定操作
```
用户：这个表有多少行？列是什么？
→ peek.py big_data.xlsx --rows 0
→ 只看结构不看数据
```

---

## 2. 📖 读取 Excel（read_excel.py）

**场景：** 只想看某个 Sheet 的特定列
```
用户：读取 Sheet2 的姓名和部门列
→ read_excel.py data.xlsx --sheet Sheet2 --columns "姓名,部门"
```

**场景：** 筛选符合条件的数据
```
用户：找出年龄大于30的员工
→ read_excel.py staff.xlsx --filter "年龄 > 30" --format markdown
```

---

## 3. ✏️ 写入/创建（write_excel.py）

**场景：** 把整理好的数据生成 Excel
```
用户：把这份 JSON 数据做成 Excel
→ write_excel.py --output result.xlsx --data '[{"姓名":"张三","年龄":28},...]'
```

**场景：** 往已有文件追加数据
```
用户：把新一批数据加到现有表格后面
→ write_excel.py --output existing.xlsx --data new_data.json --append
```

---

## 4. 🔄 格式互转（convert.py）

**场景：** 系统导出 CSV 需要转 Excel 交给领导
```
用户：把这个 csv 转成 xlsx
→ convert.py export.csv --to xlsx --output report.xlsx
```

**场景：** Excel 数据要喂给 API
```
用户：把 Excel 转成 JSON 格式
→ convert.py data.xlsx --to json --output data.json
```

**场景：** Windows 导出的 GBK 编码 CSV
```
用户：这个文件打开乱码
→ convert.py data.csv --to xlsx --encoding gbk --output data.xlsx
```

---

## 5. 📎 合并文件（merge.py）

**场景：** 每月一份报表，年底要汇总
```
用户：把1月到12月的报表合并成年度汇总
→ merge.py jan.xlsx feb.xlsx ... dec.xlsx --output annual.xlsx --ignore-headers
```

**场景：** 两张表横向拼接（列不同）
```
用户：把基本信息和绩效数据横向合并
→ merge.py info.xlsx perf.xlsx --output combined.xlsx --mode horizontal
```

---

## 6. ✂️ 拆分文件（split.py）

**场景：** 一个 workbook 有多个 Sheet，要拆成独立文件
```
用户：把这个文件的每个 Sheet 拆出来
→ split.py workbook.xlsx --output-dir ./sheets --mode by-sheet
```

---

## 7. ✂️ 按列值拆分（split.py --mode by-column）

**场景：** HR 给各部门分发各自的花名册
```
用户：按部门拆分，每个部门一份文件
→ split.py all_staff.xlsx --output-dir ./by_dept --mode by-column --column 部门
→ 输出：技术部.xlsx、产品部.xlsx、运营部.xlsx...
```

**场景：** 按面试官拆分候选人安排
```
用户：按面试官列拆分，每人一份面试安排表
→ split.py interview_schedule.xlsx --mode by-column --column 面试官 --output-dir ./schedules
```

---

## 8. 🔗 VLOOKUP / 多表关联（vlookup.py）

**场景：** 花名册匹配考勤数据
```
用户：用工号把花名册和考勤表关联起来
→ vlookup.py --main roster.xlsx --lookup attendance.xlsx --key 工号 --columns "出勤天数,迟到次数" --output result.xlsx
```

**场景：** 候选人列表匹配面试评价
```
用户：把候选人基本信息和面评结果对上
→ vlookup.py --main candidates.xlsx --lookup evaluations.xlsx --key 姓名 --output full_report.xlsx --how left
```

---

## 9. 🧹 去重（dedup.py）

**场景：** 多次导出合并后有重复数据
```
用户：按姓名+手机号去重，保留最新的
→ dedup.py contacts.xlsx --columns "姓名,手机号" --keep last --output clean.xlsx --report duplicates.xlsx
```

---

## 10. 🧽 数据清洗（clean.py）

**场景：** 从各渠道汇总的数据格式不统一
```
用户：手机号有的带区号有的不带，日期格式五花八门，还有空行
→ clean.py raw.xlsx --output clean.xlsx --rules '[
  {"type":"remove_empty_rows"},
  {"type":"normalize_phone","column":"手机"},
  {"type":"normalize_date","column":"入职日期","format":"%Y-%m-%d"},
  {"type":"trim_spaces"}
]'
```

---

## 11. 📄 模板填充（template_fill.py）

**场景：** 批量生成 offer letter
```
用户：用这个模板和员工数据批量生成 offer
→ template_fill.py --template offer_template.xlsx --data new_hires.csv --output-dir ./offers --naming "{{姓名}}_offer.xlsx"
→ 输出：张三_offer.xlsx、李四_offer.xlsx...
```

**场景：** 批量生成工资条
```
用户：每个人一份工资条
→ template_fill.py --template salary_slip.xlsx --data salary_data.xlsx --output-dir ./slips --naming "{{工号}}_{{月份}}.xlsx"
```

---

## 12. ✅ 数据校验（validate.py）

**场景：** 新员工信息录入后检查数据质量
```
用户：检查必填项是否填完、邮箱格式对不对、工号有没有重复
→ validate.py staff.xlsx --rules '[
  {"type":"required","column":"姓名"},
  {"type":"required","column":"工号"},
  {"type":"type","column":"邮箱","dtype":"email"},
  {"type":"unique","column":"工号"}
]' --output report.json
```

---

## 13. 🎨 条件格式（style.py --mode conditional）

**场景：** 绩效报表中高亮异常值
```
用户：绩效分低于60标红，高于90标绿
→ style.py scores.xlsx --output highlighted.xlsx --mode conditional --column 绩效分 --rule lt --value 60 --color FF0000
→ style.py highlighted.xlsx --output final.xlsx --mode conditional --column 绩效分 --rule gt --value 90 --color 00FF00
```

---

## 14. 💅 样式排版（style.py）

**场景：** 给领导看的报表要美观
```
用户：加粗表头、蓝色背景、自动列宽、加边框
→ style.py report.xlsx --output styled.xlsx --header-bold --header-bg 4472C4 --auto-width --border all --freeze-row 1
```

---

## 15. 📐 函数公式（formula.py）

**场景：** 批量填入汇总公式
```
用户：E列加一个SUM公式汇总B到D列
→ formula.py data.xlsx --output result.xlsx --column E --sum-columns "B,C,D"
```

**场景：** 自定义公式
```
用户：F列 = 单价 × 数量（B列×C列）
→ formula.py data.xlsx --output result.xlsx --column F --formula "=B{row}*C{row}" --range "2:100"
```

---

## 16. 📊 图表生成（chart.py）

**场景：** 月度销售报告配图表
```
用户：做一个月度销售额柱状图
→ chart.py sales.xlsx --output report.xlsx --type bar --x-column 月份 --y-columns 销售额 --title "2026年月度销售"
```

**场景：** 组合图表（柱状+折线）
```
用户：收入用柱状图，利润率用折线图
→ chart.py data.xlsx --output report.xlsx --type combo --x-column 月份 --y-columns "收入,利润率" --combo "收入:bar,利润率:line"
```

---

## 17. 📈 数据透视表（pivot.py）

**场景：** 按部门按月汇总销售额
```
用户：做一个部门×月份的销售额透视表
→ pivot.py sales.xlsx --output pivot.xlsx --rows 部门 --columns 月份 --values 销售额 --aggfunc sum --margins
```

---

## 18. 🔬 数据分析（analyze.py）

**场景：** 快速了解数据全貌
```
用户：给我这份数据的统计摘要
→ analyze.py employee_data.xlsx --detail full --format markdown
→ 输出：行列数、空值率、数值统计、文本分布、异常值检测
```

---

## 19. 🔍 差异对比（diff.py）

**场景：** 组织架构调整前后对比
```
用户：对比这两版花名册的变化
→ diff.py --old roster_q1.xlsx --new roster_q2.xlsx --key 工号 --highlight --output changes.xlsx
→ 输出：新增15人、离职8人、信息变更23人（绿=新增/红=离职/黄=变更）
```

---

## 20. 🖼️ 图片插入（image.py）

**场景：** 员工通讯录加照片
```
用户：在F列插入每个人的照片，照片文件名是工号
→ image.py staff.xlsx --output with_photos.xlsx --column F --images ./photos/ --match-by 工号 --size 60,80
```

---

## 21. 🔒 密码保护（protect.py）

**场景：** 薪酬表加密后发给领导
```
用户：给这个薪酬表加密码
→ protect.py salary.xlsx --output salary_locked.xlsx --mode encrypt --password "Hr2026!"
```

**场景：** 打开加密文件
```
用户：解密这个文件
→ protect.py locked.xlsx --output unlocked.xlsx --mode decrypt --password "Hr2026!"
```

---

## 22. ⚡ 大文件处理

**场景：** 全员考勤导出 50 万行
```
自动触发：utils.py 检测到 >10 万行，自动切换流式模式
→ 不全量加载到内存，逐块处理
→ 遇到坏行自动跳过，最后汇报错误清单
```
