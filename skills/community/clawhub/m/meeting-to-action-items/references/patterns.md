# Reference: Entity Recognition & Output Patterns
# 参考：实体识别模式与输出格式

## 人名识别

中文姓氏列表：王李张刘陈杨黄赵周吴徐孙马胡朱郭何罗高林郑梁谢唐许宋韩冯邓彭曾曹田萧潘袁蔡蒋余于杜叶程魏苏吕丁沈任姚卢傅钟崔伍廖谭翟熊纪舒屈项祝梁阮蓝闵席季麻强贾路娄危盛梅郭钱秦邱尹万常贺龚文

识别上下文：
- 主动句式：`{某人}(任何中间文本)(负责|完成|做|搞定|跟进|处理|写|制作|提交)` → 负责人
- 被动句式：`(让|由|交给){某人}(来)?(负责|做|完成)` → 负责人
- 英文句式：`{Name} (will/should/needs to/is responsible for) ...` → owner
- 称谓剥离：张姐 → 张，老赵 → 赵，小王 → 王

## 截止时间解析

### 相对日期对照表（以会议日期为基准）

| 表达式 | 规则 |
|--------|------|
| 今天 / 今日 | 基准日 |
| 明天 / 明日 | 基准日 + 1天 |
| 后天 / 後天 | 基准日 + 2天 |
| 昨天 / 前天 | 通常为过去时间，跳过 |
| 下周X | 下周一 +（星期X偏移量） |
| 下周一〜日 | 明确的下周某日 |
| 本周X / 这X | 当周的星期X（若尚未过去） |
| 周五（无前缀） | 会议日在周一至周四则本周五；周五及之后则下周五 |
| 下下X | 两周后的星期X |
| 下个月 | 基准月份 + 1，同一天 |
| 节后 / 假期后 | 标记为"节后" |

### 截止时间关键词

`(截止|deadline|DDL|due|by|之前|前|以内|前完成)` 出现在日期表达式之前或之后。

若存在"前/by/before"等修饰语，则该日期为截止日。若不存在修饰语但上下文为预期目标（争取X出），则按目标日期处理。

## 任务动词

中文：负责、完成、做、搞定、准备、整理、跟进、处理、写、制作、修改、查、检查、联系、通知、安排、推进、发送、提交、封装、调通、解决

英文：will handle, will do, will take care of, should, must, needs to, has to, is responsible for, is in charge of, owns

## 分类标准

### 决策标记词

决定、确定、确认、同意、就按、批准、就这么定、就这样、approved、agreed、confirmed

### 风险标记词

但、不过、担心、不确定、还没、没有、问题、风险、尚未、未完成、blocker、blocking、stuck、pending

### 优先级等级

| 等级 | 标签 | 中文关键词 | 英文关键词 |
|------|------|-----------|-----------|
| P0 | 阻塞 | 阻塞、依赖、卡住 | blocked、dependent、stuck |
| P1 | 高优 | 马上、赶紧、立刻、紧急、重要、必须 | urgent、important、asap、must |
| P2 | 正常 | （大部分任务的默认值） | （default） |
| P3 | 低优 | 有空、不着急、方便的时候 | sometime、whenever、no rush |

## 边界情况处理

1. **隐式负责人** — "数据清洗下周二前完成" → 负责人标记为"待确认"
2. **分句任务** — "小王做清洗，李华做PPT" → 拆分为两个独立条目
3. **中英混杂** — "小王 will handle the data cleaning by Friday"
4. **聊天对话** — 多人发言（"A: xxx B: xxx"）→ 根据发言者标签归因
5. **相对日期 vs 绝对日期** — "下周三" vs "5月27日" → 输出时优先使用解析后的绝对日期
6. **星期几的歧义** — "周五前" 可能指本周或下周；参见上方解析规则

## 示例——旧版 vs 新版输出风格

### 旧版（聊天风格 / emoji 过多）

```
【会议总结】
讨论了数据清洗与PPT制作的安排。（参与人：小王、李华）

【待办事项】
1. 小王：数据清洗
   - Deadline：2026-05-25
   - 优先级：Medium

2. 李华：制作PPT
   - Deadline：待确认
   - 优先级：Medium

【后续计划】
- 周五确认实验结果

【风险提醒】
⚠️ (none)
```

### 新版（Linear / Notion 风格）

```
Meeting Summary
讨论了数据清洗与PPT制作的安排。（参与人：王, 李）

Action Items
Owner    Task                     Deadline     Pri
───      ────                     ───────      ───
王       完成数据清洗              2026-05-25   P1
李       制作PPT                  TBD          P2

Decisions
- 实验结果确认 → 周五统一确认

Risks
- (无)

Next Milestones
- 2026-05-23: 周五确认实验结果
```

### 英文输入示例

**输入：**
```
Alice needs to finish the Q3 report by Friday.
Bob will handle the client presentation.
We agreed to move forward with the new design.
The data pipeline is still blocked though.
```

**输出：**
```
Meeting Summary
Discussed Q3 report delivery and client presentation. New design approved. Pipeline blocking risk identified. (Participants: Alice, Bob)

Action Items
Owner    Task                            Deadline     Pri
───      ────                            ───────      ───
Alice    Finish Q3 report                2026-05-22   P1
Bob      Prepare client presentation     TBD          P2

Decisions
- New design → approved and proceed

Risks
- Data pipeline blocked → impacts Q3 report timeline if not resolved

Next Milestones
- 2026-05-22: Q3 report due
```
