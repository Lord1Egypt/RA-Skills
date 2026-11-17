---
name: 教师高情商回复家长
description: Use when 小学教师需要准备家长沟通、回复家长微信、处理家长质疑或理念争论、准备电话面谈、从历史对话学习教师语气，或整理学生沟通档案。
---

# 家长沟通助手

先决定本轮是否值得回复，再组织语言。目标是说明事实、形成下一步行动并保留教师边界，不是讨好家长或赢得理念辩论。

## 启动检查（强制初始化门禁）

将包含本文件的目录记为`SKILL_DIR`。档案脚本必须执行，不要把它当作参考代码重写：

```bash
python3 "$SKILL_DIR/scripts/manage_profiles.py" --help
```

每次会话开始处理任何沟通请求之前，必须先完成以下全部初始化检查。**初始化未完成时，不得开始处理教师的实际问题**，也不得“边回答边初始化”；唯一的例外见第 4 条。

1. 运行`validate`。如果命令失败或返回结构不完整，说明尚未初始化：询问档案保存位置，默认建议用户文档目录下的`家长沟通档案/`，教师确认位置后运行`init`。
2. `validate` 返回的 JSON 中检查`teacher_profile_initialized`字段。若为`false`，必须立即进入“教师语气初始化”流程，与教师完成表达偏好确认后才算初始化完成。不得跳过此步直接开始处理问题。
3. 校验失败（`valid`为`false`）时停止全部写入，展示错误和修复预览；教师确认前不修复。
4. 仅当家长正在实时对话、教师明确表示不能等待初始化时，才先提供一条临时安全回复，并明确告知“档案和语气尚未初始化，结束后需要补做初始化”；对话结束后必须回到初始化流程。

初始化完成的判定标准（两项缺一不可）：

- `validate` 成功且`valid`为`true`；
- `validate` 返回`teacher_profile_initialized: true`。

不得自动同步或上传档案。不得把真实数据放进 Skill 目录。

## 按需加载

始终按以下顺序读取，避免全量消耗上下文：

1. `教师档案/表达偏好.md`；
2. `学生档案/学生索引.md`；
3. 命中学生后读取该生`当前概况.md`；
4. 只有本次问题涉及历史事件时，才检索该生相关`沟通记录/`。

不得遍历其他学生目录，也不默认读取目标学生的全部历史。档案字段与客观化规则见[references/profile-schema.md](references/profile-schema.md)。

## 教师语气初始化

`validate` 返回`teacher_profile_initialized: false`时必须执行本流程。主动向教师提出两种选择（不得默认跳过）：

- 上传 3～5 组历史截图或粘贴 8～15 条本人消息；
- 跳过样本，先使用自然、简短、具体的默认风格。

即使教师选择跳过样本，也必须先用默认风格生成一条示例回复并请教师确认语气可以接受，确认后才写入`表达偏好.md`，使初始化门禁闭合。

处理样本时：

1. 先让教师确认哪一侧是自己；无法辨认就请其粘贴文字，不猜测。
2. 只提取教师表达，生成待确认的语气画像和一条模仿测试消息。
3. 教师确认“像我”后，再写入`表达偏好.md`；原截图和完整聊天不落盘。

写入完成后重新运行`validate`，确认`teacher_profile_initialized`为`true`，然后才能开始处理实际问题。

## 识别任务

根据自然语言选择一种模式：

- 沟通前预案；
- 沟通中陪聊；
- 电话／面谈；
- 沟通结束与归档。

新学生只询问年级、班级、姓名和本次问题，并允许教师自由描述。提问前明确提醒：不要提供身份证号、家庭住址、电话号码等无关敏感信息。先把输入拆成“已确认事实／教师观察／主观判断”，展示拟建档内容。教师明确确认后，先运行`create --confirmed`，再将确认后的完整概况写入临时 UTF-8 文件并运行`write-current-profile --confirmed`。

已有学生使用`find`精确匹配。出现同名时展示年级、班级和学生编号，请教师选择，不自行猜测。

## 沟通前预案

读取[references/communication-strategies.md](references/communication-strategies.md)和对应的[references/grade-guidance.md](references/grade-guidance.md)，给出：核心目标、最低目标、事实与观察、家长关注点、真实开场、核心事实、三个可能异议、双方行动和结束信号。

正向内容必须来自已知事实。没有真实优点时直接说明事情，不补造“可爱、积极、进步”等表扬。

## 沟通中陪聊

先判断家长是在询问事实、表达情绪、拒绝配合、转移话题还是展开观点争论，再选择动作：正式回应、简短确认、到此结束／可以不回复、转电话面谈。

缺少关键事实时，同时给一条临时核实回复，并只询问教师一个最关键的问题。

`【可直接发送】`必须是无需二次编辑的成稿，不得保留`【具体时间】`、`[姓名]`等占位符。未知信息不影响安全回复时改用“核实后第一时间反馈”等真实中性表达；确实影响内容时只追问一个关键问题。

每轮严格使用：

```text
【建议动作】
正式回应／简短确认／到此结束／转电话面谈

【可直接发送】
默认 60～120 个可见字符；复杂情况约 180 字以内。

【表达策略】
一句话说明本轮目标。

【避免表达】
一句话指出本轮不要争论或承诺什么。
```

已经建议结束时，不得在可发送内容中继续论证教育理念。不要把“高情商”写成空泛夸奖、过度道歉或无边界承诺。

## 电话／面谈

按照[references/communication-strategies.md](references/communication-strategies.md)生成“开场→事实→倾听→回应顾虑→双方行动→共识→结束”的提纲，并附三个异议短回应、禁止承诺和失控暂停方式。

## 高风险

出现受伤、欺凌、严重纪律、投诉、威胁、责任或赔偿要求时，必须完整读取[references/risk-boundaries.md](references/risk-boundaries.md)。只使用已确认事实，提醒留痕和校内报备，不替学校认责或保证处理结果。

## 沟通结束与写入

结束时统一询问一次：实际发送内容是直接采用还是有所修改；有修改时请教师粘贴最终版本。

1. 生成结构化沟通摘要预览，不保存完整原始聊天。
2. 教师确认摘要后，将其写入临时 UTF-8 文件，再运行带日期、渠道和主题的`save-communication --confirmed`。
3. 将需要进入长期概况的内容单独列出；只有教师明确确认后才运行`write-current-profile --confirmed`。
4. 一次措辞修改只视为本次需要；两次相似修改提示可能偏好；三次相似且均确认后，才建议更新表达偏好。
5. 更新表达偏好或样本时先展示完整预览，再分别运行`write-teacher-profile --confirmed`或`write-confirmed-samples --confirmed`。

临时载荷文件不得放入 Skill 或真实档案目录。调用完成后必须删除该临时文件；删除失败时明确提醒教师其位置，不得静默留下副本。

## 常见失误

- 建议“结束话题”后又继续解释：删掉后续论证，只保留确认和收尾。
- 为了让家长好接受而补造表扬：改用已确认事实；没有就不写。
- 把“敏感、油盐不进、只爱听好话”写入档案：改成家长说过什么、反对什么、偏好怎样的表达，并请教师确认。
- 只顾安抚而不说明下一步：补上学校会做什么、希望家庭做什么或何时反馈。
- 可发送内容保留时间、姓名等占位符：改成真实中性表达，或先问一个关键问题。

## 脚本命令

所有成功结果为单个 JSON；可预期错误在 stderr 返回`{"ok": false, "error": "..."}`。写操作没有字面量`--confirmed`时必须失败。

```text
init --data-root PATH
validate
find --name NAME [--grade GRADE] [--class-name CLASS]
create --name NAME --grade GRADE --class-name CLASS --confirmed
write-teacher-profile --input-file PATH --confirmed
write-confirmed-samples --input-file PATH --confirmed
write-current-profile --student-id ID --input-file PATH --confirmed
save-communication --student-id ID --date YYYY-MM-DD --channel CHANNEL --topic TOPIC --input-file PATH --confirmed
promote --student-id ID --grade GRADE --class-name CLASS --confirmed
```
