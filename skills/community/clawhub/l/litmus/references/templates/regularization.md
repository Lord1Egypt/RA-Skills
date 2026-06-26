## Research Focus: Regularisation & Stability

You are specialised in **regularisation, gradient flow, and training stability**.

**Tier 1 — gradient and output control:**
- Logit softcap: current scale is 15. Try: 10, 20, 25, 30, None (remove it entirely).
- Gradient clipping: not currently applied. Try adding `torch.nn.utils.clip_grad_norm_` with
  max_norm values: 1.0, 0.5, 2.0. Add it in the training loop before the optimizer step.
- Weight decay: `WEIGHT_DECAY` is 0.2 for Muon params. Try: 0.05, 0.1, 0.3, 0.5.

**Tier 2 — residual and norm structure:**
- Per-layer residual scalars (`resid_lambdas`): currently learnable. Try initialising to 0.5, 0.1.
- Input mixing scalars (`x0_lambdas`): try zeroing them out (removing skip connection to x0).
- RMS Norm epsilon: try 1e-6, 1e-5 (current default), 1e-4.
- Logit bias: currently no bias on the unembedding layer. Try adding a small bias.

**Tier 3 — training dynamics:**
- Learning rate at crash: if val_bpb suddenly spikes mid-run (loss explosion), does a lower max LR
  prevent it? Try reducing MATRIX_LR by 30% and see if training is smoother (check num_steps —
  a smooth run should complete more steps).
- Muon cautious weight decay: the "gradient alignment" gate. Try disabling it — does uncautious
  decay help or hurt?
- NorMuon: try disabling variance reduction to see if the simpler Muon variant works as well.

**Cross-agent rule**: If the architecture agent found a deeper/wider model that improved val_bpb,
adopt that architecture and test whether regularisation becomes more important at larger scale.
