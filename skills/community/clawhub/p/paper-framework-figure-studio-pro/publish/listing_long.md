# Paper Framework Figure Studio Pro

This skill helps researchers design, generate, critique, and integrate publication-ready framework-style diagram figures for research papers. It covers method framework diagrams, architecture diagrams, pipelines, agent workflows, system/data-flow diagrams, graph/network diagrams, mechanism diagrams, case walkthroughs, evidence boards, taxonomy/design-space maps, data/benchmark/protocol diagrams, failure/limitation diagrams, and theory/proof-intuition diagrams.

It is regenerated from `research-paper-figure-skill-factory` v1.0.1 and grounded in the full feasible local PDF corpus indexed in the project: 7,631 candidate/accessible/processed PDF records, including 3,356 verified official oral PDFs and 4,275 supplemental local PDFs. The builder run extracted 146,071 figure captions, identified 119,534 diagram-relevant captions, recorded 93,088 multi-label diagram records, and rendered 96 representative pages as audit aids only.

Core behavior:

- first reply shows a startup plan only;
- if the first user message asks for images, the first reply still shows startup text only and records image generation as pending;
- text generation and image generation are never combined in the same reply;
- every text reply includes current plan, current status/output footer, all workflow steps plus current position, and next-question prompts;
- text candidates default to 6 within a 4-6 range;
- after text candidates or any other multi-option visual decision, the skill must set up and generate a multi-image candidate board before locking direction;
- P4 is text-only candidate-board setup, P5 is image-only candidate-board generation, and P6 is text-only candidate review/selection;
- key visual decisions recommend 6 generated image candidates, not only text comparison;
- ChatGPT web uses Create image through ChatGPT Images 2.0;
- Codex uses `$imagegen` first; if unavailable, it falls back to ChatGPT Images 2.0 API or another approved image-generation API;
- optional sample images can guide style, layout, density, labels, color, or callout grammar, with per-image preferred attributes;
- diagram routing is multi-label before selecting one primary production subtype;
- source corpus coverage is full-feasible, not a small fixed subset;
- SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, and code-rendered visuals are forbidden as final image outputs or fallbacks.
