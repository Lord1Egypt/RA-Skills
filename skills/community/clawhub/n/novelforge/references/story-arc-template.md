# Arc checkpoint template

Store an arc checkpoint in the project's planning directory. It may be Markdown
for human reading, but every claim must point to a chapter Settlement or a
declared setting document.

```markdown
# Arc: <arc-id>

- Chapters: <first-id> to <last-id>
- Durable question: <question>
- Endpoint state: <earned state>

## Chapter ledger
| Chapter | Goal | Choice | Consequence | Open question | Settlement hash |
| --- | --- | --- | --- | --- | --- |
| <id> | ... | ... | ... | ... | ... |

## Hook ledger
| Hook ID | Lifecycle | Evidence chapter | Next check |
| --- | --- | --- | --- |

## Continuity risks
- <risk and the field or source that will detect it>
```

The checkpoint is a compact index, not a substitute for explicit chapter
dependencies or the machine state under `.novelforge/`.
