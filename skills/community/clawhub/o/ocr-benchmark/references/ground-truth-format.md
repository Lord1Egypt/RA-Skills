# Ground Truth Format

Ground truth file is a JSON object keyed by image name, with an array of expected text strings.

Example `ground_truth.json`:
```json
{
  "Image001": [
    "小胡鸭",
    "Xiao Hu Duck",
    "去骨凤爪",
    "柠檬酸辣",
    "净含量580克"
  ],
  "Image002": [
    "柿饼夹心卷",
    "Persimmon Cake Sandwich Roll",
    "净含量450克"
  ]
}
```

## Scoring Rules

Each ground truth item is checked against the model's `text_extracted` array:
- **Full match (1.0 pt)**: Normalized text found in model output
- **Partial match (0.5 pt)**: >75% of characters found (handles splits/typos)
- **Miss (0 pt)**: Not found

Normalization strips: whitespace, `*`, `✓`, punctuation, brackets.

Split text (e.g., "柠檬" + "酸辣" for "柠檬酸辣") counts as full match since normalization concatenates all output.

## Creating Ground Truth

1. Run OCR with the best available model
2. **Human review** the output against the actual image
3. Correct any errors (wrong numbers, missing text, typos)
4. Save as `ground_truth.json`

Key lesson: Do not assume any model (even Opus) is 100% correct. Human verification is essential.
