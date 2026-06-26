# Workflow 09 — Final Storyboard Image PDF Assembly

Use this workflow only after the user has approved all storyboard images from the staged visual workflow.

## Goal

Combine all final storyboard images into one paginated 16:9 PDF that can be downloaded, shared, or used as a visual appendix / presentation handout.

## Trigger prompts

Users may ask:

```text
使用这个skill，根据状态，执行最后一步：把所有已经生成的图合成一个PDF。
```

or:

```text
使用这个skill，根据状态，执行第7步：最终图片PDF合成。
```

## Inputs

Collect, in order:

1. image files from Step 1: background / defects / problem / inspiration;
2. image files from Step 2: algorithm overview and modules;
3. image files from Step 3: experiments;
4. image files from optional Step 4: limitations / defense;
5. image files from optional Step 5: future directions;
6. image files from optional Step 6: cover / summary / Q&A backup.

If filenames do not encode order, ask the user for the desired order or infer from visible titles such as `第1幕`, `第2幕`, ... and state the inferred order before assembly.

## Rules

- Do **not** create new storyboard images in this step.
- Do **not** rewrite the full report in this step.
- Preserve each image as a full page with 16:9 aspect ratio.
- Use one image per page unless the user explicitly asks for a contact sheet.
- Add no extra watermarks or unrelated branding.
- If an image is not exactly 16:9, fit it on a 16:9 page without clipping; use white margins if needed.
- Verify the output by reopening or rendering the PDF when the environment supports verification.

## Recommended PDF output

```text
paper_storyboard_all_images.pdf
paper_storyboard_images_and_pdf.zip   # optional handoff bundle
```

## ChatGPT web/app implementation guidance

Use the available file/Python/PDF workflow. A robust approach is:

1. collect image paths;
2. sort by stage and幕 number;
3. use PIL/Pillow to normalize orientation and fit each image onto a 16:9 canvas;
4. save all canvases as a single PDF;
5. provide the PDF link and a short status note.

## Codex / Claude Code / coding-agent implementation guidance

Use `scripts/assemble_storyboard_pdf.py` or an equivalent local implementation with PIL/Pillow or ReportLab.

Example:

```bash
python scripts/assemble_storyboard_pdf.py   --input-dir generated/storyboards/final_images   --output generated/storyboards/paper_storyboard_all_images.pdf
```

## Final response template

After assembly, reply briefly:

```text
已完成最终图片 PDF 合成。

Current Status
- 已将 X 张图按第1幕 -> 第X幕顺序合成为 16:9 PDF。
- 输出：paper_storyboard_all_images.pdf

Possible User Inputs For Next Stage
- 使用这个skill，根据状态，检查PDF顺序和页面标题是否正确。
- 使用这个skill，根据状态，生成多张连续的卡通图，用于PPT封面、总结页和答辩备用页。
```
