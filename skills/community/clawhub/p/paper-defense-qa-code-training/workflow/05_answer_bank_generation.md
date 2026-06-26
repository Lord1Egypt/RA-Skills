# Step 5: Answer Bank Generation

## Goal

把攻击面转成可直接背诵和可追溯证据的问答库。

## Minimum categories

- Beginner questions
- Peer technical questions
- Advisor / committee questions
- Reviewer / bug-hunter questions
- Code/training questions
- Limitation questions
- Future-work questions
- Hostile but fair questions

## Item format

```markdown
### Qxx. <question>

- **对象**：...
- **攻击轴**：...
- **优先级**：...
- **为什么会问**：...
- **短回答**：...
- **长回答**：...
- **证据**：...
- **证据标签**：...
- **不能过度声称**：...
- **追问后的回应**：...
- **备份页 / 材料**：...
```

## Answer rule

Use the CEBA pattern:

```text
Claim -> Evidence -> Boundary -> Action
```

## Red-team revision

Rewrite any answer that:

- has no evidence reference;
- hides an important limitation;
- says “should” or “probably” where evidence is required;
- claims generalization outside tested settings;
- suggests reproducibility without code/config/log support.
