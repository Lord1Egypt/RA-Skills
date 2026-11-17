# Analyzing a compiled `.op` plugin and judging portability (TMNEXT -> MP4)

Use when the user drops a `.op` file and asks "can this work on ManiaPlanet?".
Verified end-to-end on `TrackmaniaTrainer-1.0.0.op` (2026-08).

## 1. `.op` is a ZIP — always unpack first

```bash
unzip -l Plugins/Foo-1.0.0.op                 # manifest first
rm -rf /tmp/foo && mkdir -p /tmp/foo && unzip -q Plugins/Foo-1.0.0.op -d /tmp/foo
```

**Pitfalls:**
- `.op` archives written on Windows use **backslash path separators**. `unzip`
  warns and flattens `src\Foo.as` into a literal filename OR into a real `src/`
  dir depending on version — `ls -R` right after to see what you actually got.
- The MSYS `/tmp` path is NOT visible to `execute_code` (which runs native
  Python). Translate with `cygpath -w /tmp/foo` and use the Windows path in
  Python. Reading via `read_file` with the `/tmp/...` path works fine — only raw
  `open()` in `execute_code` needs the translated path.

## 2. Decide immediately: is the logic in AngelScript or in a native DLL?

If the archive contains a `.dll`, read `src/NativeBridge.as` (or whatever calls
`Import::GetLibrary`). Count the `Import::Function@` handles. If every user
action is a one-line `TT_ActionX.CallUInt64()`, **the AngelScript is a shell and
the plugin is the DLL**. Say so before promising a port.

Fingerprint the DLL without a disassembler:

```python
import re
b = open(r"C:\...\Native.dll", "rb").read()
s = set(re.findall(rb"[ -~]{6,}", b))
for k in [b"CSm", b"CGame", b"Openplanet", b"System.Private", b"TT_"]:
    print(k, sorted(x for x in s if k in x)[:20])
```

Reading:
- `System.Private.TypeLoader` -> **.NET NativeAOT**. No C# sources ship in the
  `.op`, so it cannot be recompiled for another game. Reverse-engineering a
  NativeAOT binary is the only path — treat as out of scope unless asked.
- **No** `CGame*` / `CSm*` / `Openplanet` strings -> the DLL does not use
  Openplanet reflection at all; it walks the target process with hardcoded
  offsets. Those offsets are worthless for a different executable.
- The internal type names that DO leak (e.g. `TrainerRuntime`,
  `VehicleStateManager`, `CheckpointsManager`) are still useful — they tell you
  the feature decomposition to reimplement.

## 3. Recover the data model from the marshalling code, not the DLL

The `.as` bridge reads structs field-by-field out of a `MemoryBuffer` in exact
declaration order. That `ReadFrom()` method **is** the struct definition — copy
field names, order, and widths straight out of it. Watch for `bool32`
(a `ReadUInt32() != 0` helper) and `0xFFFFFFFF` used as the "none" sentinel.

## 4. Verdict template

A native-DLL plugin from another game is **a rewrite, not a port**. State the
three blockers plainly: (a) offsets target the wrong executable, (b) no sources
to recompile, (c) manifest/API shape differs. Then pivot to "here is what MP4
can actually do", which is the useful half of the answer.

## 5. Deliverable shape the user wanted

For "give this to a stronger model", write a **single self-contained English
markdown brief** to `.agents/<Name>_PORT_BRIEF.md` and hand back the path as a
`MEDIA:` link. Sections that earned their place:
what-it-is / why-it-fails-here / what-the-target-platform-verifiably-offers /
proposed-design / hard-constraints / feature-possibilities-ranked-by-effort /
build-order-with-gates / open-questions. Every API claim must be tagged as
verified against the reflection DB — an unverified brief is worse than none,
because the receiving model will trust it.
