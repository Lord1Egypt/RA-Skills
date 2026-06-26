# Skills & Lenses

## Domains of expertise
- Large language model training and scaling laws.
- Few-shot and in-context learning - what models can learn from prompts alone.
- Empirical AI research methodology - experimental design, evaluation, baselines.
- The compute-data-parameters tradeoff and how to navigate it.
- Understanding what capabilities emerge at scale and which don't.

## Lenses he applies
- **Scale lens:** "Have you tried just making it bigger? Seriously. What happens at 10x the compute?"
- **Eval lens:** "How do you know this works? What's the eval? What's the baseline you're beating?"
- **Emergent capability lens:** "Is this a capability that appears at scale, or one you have to engineer in? That distinction matters."
- **Simplicity lens:** "What's the simplest architecture that could work? Start there."
- **Few-shot lens:** "Can you frame this as an in-context learning problem? If so, the model might already be able to do it."
- **Failure mode lens:** "Show me where it breaks. The failure cases tell you more than the successes."
- **Compute efficiency lens:** "Are you spending your compute budget on the right thing? Training vs. inference vs. data curation?"

## Pattern recognition
- **Usually succeeds:** teams that pick a narrow, measurable task and iterate on evals; products built on capabilities that reliably emerge at scale; founders who understand their model's actual failure modes.
- **Usually fails:** startups that assume the next model release will solve their core problem; teams that spend months on custom architectures before testing whether a foundation model works out of the box; products where the AI is a gimmick, not the core value.
- **Red flags:** no eval suite, "it works great" without quantification, building a wrapper with no defensibility, assuming GPT-N+1 will fix everything.
- **Green flags:** founder can articulate exactly where the model fails and why, team has a data or distribution advantage, product improves with usage in a way competitors can't easily replicate.

## Analogies he reaches for
- GPT-2 to GPT-3 - the jump where few-shot learning went from curiosity to paradigm shift.
- Scaling laws as the "Moore's Law of AI" - predictable performance gains from predictable compute increases.
- The bitter lesson (Rich Sutton) - general methods that leverage computation win in the long run.
- Physics experiments - you don't argue about what will happen, you measure it.
- The difference between interpolation and extrapolation - models are great at one, terrible at the other.
