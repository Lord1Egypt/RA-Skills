# Quality Gate Workflow

## Pipeline Flow

```mermaid
graph TD
    START[开始batch] --> CH{逐章执行}
    CH --> GEN{生成结果}
    GEN -->|errors==0| OK[标记成功 继续]
    GEN -->|errors<=2| DEBT[记录QualityDebt 标记成功 继续]
    GEN -->|errors>2| FAIL[标记失败 继续]
    GEN -->|fatal error| STOP[中断batch]
    
    OK --> NEXT{还有下一章?}
    DEBT --> NEXT
    FAIL --> NEXT
    NEXT -->|yes| CH
    NEXT -->|no| REPORT[输出报告+Debt清单]
```

## Quality Debt Levels

| Severity | Meaning | Action |
|:---------|:--------|:-------|
| warning | Minor issue | Record, continue |
| minor | Recoverable quality flaw | Record, mark chapter as debt, continue |
| major | Needs human review | Record, mark chapter as debt, continue |
| critical | Data integrity failure | STOP |

## Persistence

QualityDebt saved to `追踪/quality_debt.json` after each batch.
