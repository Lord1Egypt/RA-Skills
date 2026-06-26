# MATLAB 仿真论文对照检查清单

Use this checklist while comparing MATLAB simulation code with the reference paper.

## System Model

- Antenna/user/subcarrier/path dimensions match the paper.
- Channel model distribution, path loss, fading, sparsity, visibility region, quantization, or near-field/far-field assumptions match.
- Noise variance, SNR definition, transmit power, normalization, and dB/linear conversion match.
- Pilot, training, frame, or sampling structure matches.
- Boundary conditions, initial conditions, and constraints match.

## Algorithm Fidelity

- Initialization matches the paper.
- Update equations match signs, transposes, conjugates, Hermitian operations, norms, projections, and regularizers.
- Iteration order matches the paper algorithm box.
- Step size, threshold, support size, rank, penalty, or damping rules match.
- Stopping criteria match tolerance, residual, support stability, maximum iterations, or paper-defined halting condition.
- Baselines are implemented under the same inputs and metrics.

## Simulation Settings

- Monte Carlo count, random seed policy, SNR grid, dimensions, and plotted metrics match.
- Axes, legends, averaging, normalization, confidence intervals, and exported values match.
- Generated figures/tables can be traced to scripts and saved numeric data.
- Every paper simulation result, figure, table, named experiment, and reported metric maps to one or more runnable MATLAB main scripts or main functions.
- Unmapped or partially mapped paper results are recorded explicitly with the missing entry point, missing output file, or missing plotting/metric code.

## MATLAB Performance Opportunities

- Preallocate arrays before loops.
- Move invariant computations outside Monte Carlo, SNR, user, or iteration loops.
- Replace explicit inverse with decomposition or backslash where equivalent.
- Cache dictionaries, steering matrices, FFT matrices, Kronecker products, and covariance matrices.
- Avoid repeated `clear all`, repeated `addpath`, excessive `save`, and plotting inside inner loops.
- Consider vectorization, sparse matrices, `parfor`, GPU arrays, or MEX only after correctness is stable.

## Cleanup Candidates

- Comments that describe deleted, obsolete, or unrelated experiments.
- Commented-out code blocks that are not part of paper-result generation.
- Debug scripts, ad hoc plotting, duplicate figure drawing, and old result export logic not mapped to paper figures/tables.
- Unused variables, parameters, helper functions, data-loading branches, and result files that are not used by any mapped paper result.
- Alternative algorithms or experimental variants not reported in the paper, unless the user wants to keep them.

Before deleting cleanup candidates, confirm they are not called by mapped main functions, verification commands, shared helpers, or paper-result plotting. Record every cleanup deletion in the summary.

## Summary Evidence

For every source edit, record:

- file and function/script;
- original behavior;
- paper requirement or performance reason;
- exact change made;
- verification command and observed result;
- whether algorithm logic or paper parameters changed.
