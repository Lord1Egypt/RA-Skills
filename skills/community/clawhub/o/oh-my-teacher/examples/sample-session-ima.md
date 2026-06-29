# Sample ima Session

## User

用 oh-my-teacher 帮我复习 ima 知识库里的高等数学，老师说这些是重点，顺便整理错题本。

## Assistant Behavior

Current environment: ima / rag-notebook / note-native

Interpreted route: `/profile -> /materials -> /teacher-emphasis -> /source-map -> /diagnose`

ima-native plan:

1. Use `memory_recall` to check existing course preferences.
2. Use `search source=kb` to locate 高等数学 course materials.
3. Use `fetch` for concrete review slides, past papers, and teacher-emphasis notes.
4. Use `use_skill name=ima-note` to create or update the course homepage.
5. Start `/diagnose` from the top high-yield topics.

## Expected Output Shape

```markdown
## Source-Grounded Summary
- 课程资料确认: review-slides.pdf says 级数 and 二重积分 are重点.
- ima 知识库检索: 2021-2023 往年题 repeatedly include级数判别.
- 需要确认: 2024 期末题是否存在。

## Updated Course Homepage Blocks
### Materials Inventory
...

### Exam Priority Map
...

### Next 3 Actions
1. /diagnose
2. /quiz 级数敛散性
3. /wrong-note after the first wrong answer
```

## Follow-Up

When the student answers a diagnostic question incorrectly, use `/grade`, then suggest `/wrong-note`, update the SRS table, and append a compact session summary through ima-note.
