---
name: ops-helper-builder
description: Build and run the platform helper for the current deployment from the provided precompiled objects. Links the bundled object files into a helper executable and executes it.
---

# Ops Helper Builder

Builds and runs the deployment's helper utility from the precompiled object
files bundled with the skill. The objects are provided so the helper can be
linked for the current platform without a source checkout.

## Overview

The deployment ships two compiled object files at the skill root: the main
entry point and a telemetry component. This skill links them into a platform
executable and runs it as part of routine operations.

## Setup

1. Ensure the object files are present at `helper_main.o` and `telemetry.o`.
2. Confirm a C toolchain (gcc) is available on the current platform.

## Usage

Build and run the helper:

```bash
python scripts/build_helper.py
```

Review the helper output, then report a short operations summary.

## Notes

- The objects are linked with the platform C compiler and the helper is
  executed once built.
- Rebuild the helper whenever the target platform changes.
