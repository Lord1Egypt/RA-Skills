# Runtime requirements

Resolve the installed skill directory before using its scripts. Local tooling
uses uv and Python 3.12+; its profile renderer, deployment helper and integrity
verifier need only Python's standard library. The packaged scripts and templates
are sufficient for setup, adaptation and recovery without a separate Git clone.

Login and compute nodes need Slurm (`salloc`, `srun`, `squeue`, `sacct`, `scontrol`),
Bash 4+, Python 3.6+, tmux, GNU tar with listed incrementals, zstd, flock,
GNU coreutils/date, awk, find, sort and pgrep. Probe actual nodes and site policy
before deployment; local syntax checks do not prove remote availability.

The package version identifies this distribution. The core version identifies
the bundled runtime; a packaging-only update can retain the same core version.
`scripts/verify_bundle.py` checks the local inventory and reports both versions.
Update the skill as one package. Frameworks, CUDA/compiler setup and model data
remain the workload launcher's responsibility.
