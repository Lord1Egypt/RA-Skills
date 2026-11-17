---
name: mind
description: Write MIND source for deterministic agentic systems, with canonical MIC@3 artifacts, supported native ELF compilation, and feature-aware guidance for MIND v0.10.2.
metadata:
  short-description: Write MIND v0.10.2 source
  version: 1.0.4
  compiler-release: 0.10.2
---

# Write MIND Code

Use this skill when a user asks for a `.mind` program for an agentic or numerical system, a port to MIND, or an explanation of released MIND syntax. Target the public compiler release **v0.10.2** unless the user names another checkout or version. Generated code still needs compilation with the user's exact toolchain.

## Reliable baseline

MIND is a statically typed language for deterministic, auditable agentic and numerical systems. Its canonical binary IR format is MIC@3. Evidence MAP metadata and the associated determinism record are added when requested with `--emit-evidence`; a plain MIC@3 artifact does not itself assert those metadata fields. The public compiler accepts functions, `let` bindings, explicit primitive types, structs, enums, imports/exports, conditionals, `while` and `for` loops, pattern matching, indexing, arithmetic and comparisons. Use the surface syntax shown in the repository's released examples and documentation.

```mind
fn add(a: i64, b: i64) -> i64 {
    return a + b;
}

fn sum_to(n: i64) -> i64 {
    let mut i = 0;
    let mut total = 0;
    while i < n {
        total += i;
        i += 1;
    }
    return total;
}
```

The supported native path can compile the documented integer/control-flow subset to a native ELF. Tensor, float, and GPU workflows remain feature-gated and use MLIR/LLVM-dependent paths. The minimal compiler path is suitable for parsing, checking, and canonical MIC@3 output. `mlir-lowering` enables MLIR text emission; `autodiff` enables compile-time reverse-mode gradient IR for the documented Core v1 operations; `aot` enables object emission and includes the MLIR/autodiff prerequisites. Use the feature set required by the command instead of implying that every build supports every operation.

```bash
cargo run --bin mindc -- program.mind --verify-only
cargo run --features "mlir-lowering autodiff" --bin mindc -- program.mind --func main --autodiff --emit-grad-ir
```

Autodiff is static IR transformation, not a claim of full-language differentiation. The released documentation identifies unsupported or non-differentiable cases, including modulo, bitwise/shift operations, and some dynamic or non-Core-v1 shapes; report those limits clearly.

## Version and capability boundaries

- Treat compiler version, cargo feature flags, and target tools as separate facts. Ask for the user's version when compatibility matters.
- Do not present closures, `defer`, generic trait bounds, or arbitrary trait-based APIs as compile-ready v0.10.2 examples. If requested, describe them as unsupported or needing a checked migration path.
- Do not claim complete native independence, universal autodiff, global floating-point bit identity, or available GPU execution. The native path covers a supported subset; scalar float, tensor, and GPU code generation still has MLIR/LLVM or external-runtime dependencies. Determinism claims apply only to documented paths, and production runtime backends are separate products.
- `std-surface`, `cross-module-imports`, `cpu-exec`, `mlir-lowering`, `autodiff`, and `full` are opt-in cargo features with different meanings. Do not silently add them to a user's command.
- Evidence signing is opt-in. The public release documents classical Ed25519 and optional PQC feature-gated schemes; distinguish the signing scheme from whether CI has exercised it. Never imply that an unsigned artifact is signed.

## Output rules

Prefer a small complete example and state required features. Use Markdown `mind` code fences. Explain assumptions when porting from another language. Tell the user to compile and test generated code before deployment. Keep private runtime, commercial implementation, credentials, and internal repository details out of generated output.
