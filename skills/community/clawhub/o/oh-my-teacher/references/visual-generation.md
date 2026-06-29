# Visual, Image, Video, and Animation Support

For coding-related animations and algorithm visualizations, see `references/coding-demos.md`. For subject-specific visual defaults (math plots, physics diagrams, etc.), see `references/subject-adaptation.md`. For host fallbacks, see `references/environment-adaptation.md`.

Use visuals when they improve understanding, especially for processes, structure, comparison, spatial reasoning, dynamic changes, and memory sheets.

## Visual Selection

- Mermaid: concept maps, flowcharts, timelines, system architecture.
  - **Proactive Chinese label check**: Before generating any Mermaid diagram with Chinese labels, state to the user: "注意：Mermaid 渲染中文标签时可能出现乱码。如果发生这种情况，我会自动改用英文标签并附中文注释。" When generating, add a comment at the top of the Mermaid code: `%% 若中文标签显示乱码，请将标签改为英文并添加中文注释，或复制此图到本地 Mermaid 编辑器查看。`
  - If rendering fails, fall back to English labels with Chinese comments alongside, or switch to ASCII diagrams.
- Tables: comparisons, formulas, definitions, error categories.
- ASCII diagrams: quick sketches in text-only contexts.
- Code-generated plots/animations: math, physics, algorithms, probability, simulation.
- Image API: polished concept illustrations, experiment apparatus, memory posters, visual flashcards.
- Video API: dynamic processes, algorithm execution, physical motion, experimental procedures, historical development.

Do not force image generation when a diagram/table is clearer.

## Environment-Aware Visual Form

Pick the visual form that the host environment can actually render. Use capability checks rather than product names.

| Visual goal | Agent shell | RAG notebook | Notes app | Plain chat |
|-------------|-------------|--------------|-----------|------------|
| Concept map / flowchart | Mermaid file (`.mmd`) the student can preview in any Mermaid renderer | Mermaid code block inline if supported | Mermaid or Markdown outline with backlinks | ASCII tree or numbered hierarchy |
| Comparison | Markdown table in a file | Markdown table inline | Markdown table with tags/backlinks | Plain-text table or bullet list with `|` separators |
| Math / physics plot | Python (matplotlib) script, run, attach image or save PNG | Describe the plot + shape; cite source if based on materials | Describe plot; optionally link note sections | Describe the plot; ASCII for very small graphs; no PNG expected |
| Algorithm trace | HTML Canvas / p5.js / Manim file | Pseudocode + state table inline | State table note block | State table inline (line × variable columns) |
| Polished illustration | Image API — confirm cost first | Image API only if exposed; otherwise Mermaid/ASCII | Provider-neutral prompt only unless plugin supports generation | **Do not call.** Describe in prose and offer Mermaid/ASCII |
| Dynamic process / video | Manim / HTML Canvas / video API — confirm cost first | Storyboard inline + key frames as Mermaid or text | Storyboard Markdown | Storyboard inline only; no video, no Manim execution |

### ASCII Quick Sketches

When nothing else is available, use these compact forms:

- Tree: `Root -> Child A -> Grandchild A1, A2`
- Boxes:

  ```
  +---------+      +---------+
  |  Step1  | ---> |  Step2  |
  +---------+      +---------+
       |                |
       v                v
     out1              out2
  ```

- Sequence: send arrow `A -> B: msg`, reply `B --> A: reply`
- State: numbered list with state name and active variables

ASCII is best for short, structural visuals. For long paths or many branches, recommend the student switch to an agent shell and a Mermaid file.

## Image API Workflow

Before high-cost calls:

1. Produce a prompt with educational objective, visual elements, labels, style, aspect ratio, and constraints.
2. Ask the user to confirm unless they explicitly requested immediate generation and the environment supports it.
3. Prefer OpenAI image generation when available; otherwise provide a provider-neutral prompt.

Prompt template:

```text
Create an educational diagram for [course/topic].
Goal: help a university student understand [concept/process].
Include: [labeled elements].
Avoid: copyrighted textbook replication, decorative clutter, ambiguous labels.
Style: clean academic illustration, high contrast, readable labels.
Aspect ratio: [ratio].
Language: [Chinese/English/bilingual].
```

## Video API Workflow

Before video generation:

1. Produce storyboard: duration, scenes, narration, on-screen labels, motion, checkpoints.
2. Ask for confirmation before calling Sora or another video provider.
3. If no video API is available, downgrade to Manim, HTML Canvas, GIF frame plan, or storyboard only.

Storyboard template:

- Title and learning goal
- Total duration
- Scene list with timing
- Narration
- Visual motion
- On-screen labels
- Final active-recall question

## Dynamic Explanation Defaults

- Algorithms: show data structure state after each step.
- Math: show transformation from definition to result.
- Physics: show variables changing over time, units, and graph.
- Lab: show setup, operation sequence, and failure points.
- Humanities: show timeline, causal chain, or comparison map.
