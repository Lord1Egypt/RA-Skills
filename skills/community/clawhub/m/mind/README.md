# MIND Language skill

Skill version **1.0.4**, aligned to the public MIND compiler release **v0.10.2**.

This package provides version-aware guidance for writing and explaining `.mind` source for deterministic agentic and numerical systems, including canonical MIC@3 artifacts and the supported native ELF subset. MIC@3 is the canonical binary IR format; evidence MAP metadata is added only when requested with `--emit-evidence`. It keeps experimental or unsupported constructs separate from compile-ready v0.10.2 examples, distinguishes opt-in cargo features and signing schemes, and avoids claims that exceed the released compiler's documented support.

Review generated code with the intended compiler and tests.
