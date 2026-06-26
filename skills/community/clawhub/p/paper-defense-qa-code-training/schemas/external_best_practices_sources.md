# External Best-Practice Sources Used For This Skill

This file records the public sources used to shape the paper-defense, reviewer-Q&A, code-audit, and training-reproducibility logic. These are source inspirations for the skill; concrete defense answers must still be grounded in the target paper, code, logs, and review materials.

## Official venue and reproducibility guidance

- NeurIPS Paper Checklist Guidelines
  - Source: https://neurips.cc/public/guides/PaperChecklist
  - Used for: claims, limitations, theory assumptions/proofs, experiment reproducibility, datasets, code, compute, ethics, societal impact.
- NeurIPS Main Track Handbook 2026
  - Source: https://neurips.cc/Conferences/2026/MainTrackHandbook
  - Used for: research artifacts, code, environment versions, weights, hyperparameters, compute resources.
- ICLR 2026 Reviewer Guide
  - Source: https://iclr.cc/Conferences/2026/ReviewerGuide
  - Used for: timely, substantive, careful reviews and decision-context awareness.
- ICLR 2026 Author Guide
  - Source: https://iclr.cc/Conferences/2026/AuthorGuide
  - Used for: supplementary code, reproducibility statement, assumptions, complete proofs, data processing, ethics, public discussion/rebuttal behavior.
- AISTATS 2026 Reviewer Guidelines
  - Source: https://virtual.aistats.org/Conferences/2026/ReviewerGuidelines
  - Used for: soundness, significance, novelty, clarity, relation to prior work, non-conventional contributions.
- Machine Learning Reproducibility Checklist v2.0
  - Source: https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf
  - Used for: model/algorithm clarity, assumptions, complexity, theoretical claims, dataset splits, preprocessing, dependencies, training/evaluation code, pretrained models, hyperparameters, number of runs, metrics, error bars, runtime, compute.
- IJCAI 2026 Reproducibility guidance
  - Source: https://2026.ijcai.org/reproducibility/
  - Used for: evidence-backed results are more convincing; lack of evidence should be treated as reduced persuasiveness rather than ignored.

## GitHub / ClawHub / public skill patterns

- Bytedance Deer Flow academic-paper-review skill
  - Source: https://github.com/bytedance/deer-flow/blob/main/skills/public/academic-paper-review/SKILL.md
  - Used for: structured paper review covering methodology, contribution, literature positioning, limitations, reproducibility.
- Scientific peer-review skill in claude-code-templates
  - Source: https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/scientific/peer-review/SKILL.md
  - Used for: systematic peer review over methodology, statistics, design, reproducibility, ethics, reporting standards.
- Papers with Code releasing-research-code checklist
  - Source: https://github.com/paperswithcode/releasing-research-code
  - Used for: dependencies, training code, evaluation code, pretrained models, README with result table and exact commands.
- ClawHub Sopaper Evidence skill
  - Source: https://clawhub.ai/sheepxux/sopaper-evidence
  - Used for: source priority, claim/evidence mapping, evidence type labels, gap triage.

## Teaching, presentation, and defense communication

- Stanford CS324 paper discussions
  - Source: https://stanford-cs324.github.io/winter2022/paper-discussions/
  - Used for: role-based critical questioning: archaeologist, social impact assessor, industry practitioner, researcher, salesperson/author-defender, bug hunter.
- MIT EECS Communication Lab: Research Qualifying Examination
  - Source: https://mitcommlab.mit.edu/eecs/commkit/research-qualifying-examination-rqe/
  - Used for: committee/audience analysis, central message, backup slides, technical questions, practice with technical audiences.
- MIT EECS Communication Lab: Paper Introduction
  - Source: https://mitcommlab.mit.edu/eecs/commkit/journal-article-introduction/
  - Used for: problem, importance, solution, contribution, audience-aware story construction.
- MIT EECS Communication Lab: Paper Discussion/Conclusion
  - Source: https://mitcommlab.mit.edu/eecs/commkit/journal-article-discussion/
  - Used for: limitations, relation to prior work, scientific implications, future work.
- MIT EECS Communication Lab: Slide Presentation
  - Source: https://mitcommlab.mit.edu/eecs/commkit/slideshow/
  - Used for: one message per slide, audience orientation, connecting data to motivation, preparing figures before showing them.

## X / social-media notes

X posts can provide timely community heuristics about rebuttals and reviewer expectations, but they are less stable and less citable than official venue guides, published checklists, and maintained GitHub/ClawHub skills. This skill therefore treats X-style advice as optional soft context only. Do not use social-media claims as the main evidence for a defense answer.

## Visual generation and ClawHub packaging guidance

- OpenAI Image generation API guide
  - Source: https://developers.openai.com/api/docs/guides/image-generation
  - Used for: separating text prompt preparation from image-generation execution, using GPT Image models such as `gpt-image-2`, and distinguishing Image API generation/editing from conversational image flows.
- OpenAI Academy: Creating images with ChatGPT
  - Source: https://openai.com/academy/image-generation/
  - Used for: writing clear image prompts with purpose, subject, context, visual style, and constraints.
- OpenAI: Introducing ChatGPT Images 2.0
  - Source: https://openai.com/index/introducing-chatgpt-images-2-0/
  - Used for: recommending Create image mode / ChatGPT Images 2.0 for visually rich explanation cards when available.
- ClawHub skill format documentation
  - Source: https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md
  - Used for: `SKILL.md`, frontmatter metadata, URL-safe slug, text-file-only bundle, size limit, semver versions, and MIT-0 license expectation.
- ClawHub Skill Creator
  - Source: https://clawhub.ai/chindden/skill-creator
  - Used for: concise skills, progressive disclosure, required `SKILL.md`, bundled scripts/references/assets, and validation-before-packaging workflow.
