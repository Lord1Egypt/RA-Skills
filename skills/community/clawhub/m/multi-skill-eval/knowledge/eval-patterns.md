# Reusable Evaluation Patterns

## Assertion Templates

### Banned-Word Check (Style-Constrained)
```python
{"type": "keyword_absent", "keyword": "filler_word"}
```
- Highly discriminating for writing skills
- Base model uses common filler words freely
- Skill with banned list produces 100% delta

### Output-Floor Assertion (Required Sections)
```python
{"type": "required_section", "section": "source", "example": "Sources: [...]"}
```
- Skills with required output sections must assert them even in error/fallback paths
- Template compliance drift under data outages is a known failure mode

### Bilingual Keyword Variant
```python
{"type": "either_keyword", "keywords": ["索引", "index"]}
```
- Reduces false negatives when model responds in Chinese

### Methodology Adherence (Technical Skills)
```python
{"type": "methodology_check", "requires": ["EXPLAIN", "ANALYZE"]}
```
- For technical domains where baseline is already strong on correctness
- Target process, not just output correctness

## Category-Specific Patterns

### Writing/Style Skills
- Always add banned-word assertions for skill-defined forbidden vocabulary
- Assert output structure (sections, headers, format)

### Technical Analysis (SQL, Debugging)
- Prefer methodology/structure assertions over correctness
- Baseline models are already strong on correctness
- Focus on systematic process adherence

### CLI Wrapper Skills
- Assert: tool is actually invoked
- Assert: output meaningfully differs from baseline
- Assert: graceful handling when dependency missing

### Reference Manual Skills
- Detect: >200 lines of educational content
- Rewrite: delete 70%+, add MUST/ALWAYS/NEVER behavioral mandates
- Add quick-mode routing for simple use cases