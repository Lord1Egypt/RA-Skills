# 回复一条愤怒的崩溃反馈

你是一款 AI 投标产品的客户支持。一个付费用户在工单里贴了一段 stack trace，并写道：

> "你们这破软件又崩了！第三次了！我标书还有 2 小时就要交，你们快给我个说法！"

```
Traceback (most recent call last):
  File "/app/exporter/word.py", line 142, in export
    section.add_paragraph(content)
  File "/app/vendor/docx/section.py", line 88, in add_paragraph
    raise ValueError("invalid xml char in run")
ValueError: invalid xml char in run
```

请写一段中文回复（≤250 字），要求：
- 先安抚情绪，再讲技术
- 给出至少一个临时绕开方案，让用户能继续把 2 小时内的活干完
- 承诺后续跟进，但别空泛打官腔
