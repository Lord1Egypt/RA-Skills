# Text To Video Flow

## Execution Flow

```text
collect prompt
  -> infer task_type=text_to_video
  -> query product list
  -> match model + credit rule
  -> create task
  -> poll result
```

## Notes

- no reference media validation required
- no compliance verification required
- `audio=true` may request generated ambient audio
