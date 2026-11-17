## Description:

Train GPT-2 scale models (~124M parameters) efficiently on a single GPU. Covers GPT-124M architecture, tokenized dataset loading (e.g., HuggingFace Hub shards), modern optimizers (Muon, AdamW), mixed precision training, and training loop implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft and adapt NanoGPT-style training workflows, including model architecture, tokenized dataset loading, optimizer setup, mixed precision, and training loop implementation for single-GPU GPT-2 scale experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned ML dependencies can change behavior, break reproducibility, or introduce unexpected package versions.

Mitigation: Pin package versions and use a lockfile or package hashes before running the training environment.

Risk: Public dataset shard downloads can change or fail if revisions are not fixed.

Mitigation: Pin Hugging Face dataset revisions and verify downloaded shard checksums before training.

Risk: Training workflows install large dependencies and run GPU code that may expose local credentials in shared environments.

Mitigation: Run training in an isolated environment without unnecessary secrets or credentials.

## Reference(s):

- [GPT Architecture](references/gpt-architecture.md)
- [Tokenized Data Loading](references/tokenized-data.md)
- [FineWeb Data Loading](references/fineweb-data.md)
- [Optimizers](references/optimizers.md)
- [Training Loop](references/training-loop.md)
- [Hyperparameters](references/hyperparameters.md)
- [nanoGPT](https://github.com/karpathy/nanoGPT)
- [build-nanogpt](https://github.com/karpathy/build-nanogpt)
- [modded-nanogpt](https://github.com/KellerJordan/modded-nanogpt)
- [modded-nanogpt FineWeb cache loader](https://github.com/KellerJordan/modded-nanogpt/blob/master/data/cached_fineweb100B.py)
- [FineWeb-Edu GPT-2 token shards](https://huggingface.co/datasets/karpathy/fineweb-edu-100B-gpt2-token-shards)
- [ClawHub skill page](https://clawhub.ai/lnj22/skills/mhc-layer-impl-nanogpt-training)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream agent guidance that may include package installation, training configuration, model code, data-loading code, and training-loop snippets.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
