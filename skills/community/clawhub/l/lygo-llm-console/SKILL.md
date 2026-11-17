---
name: lygo-llm-console
description: "Use when an operator asks for the sovereign LYGO LLM Console, console 1.7.0, a local GGUF agent portal, or the online API portal. This is a pointer-only skill: it bundles no runtime, no Python, no executables and runs nothing on install. It links to the official chatagent.ca downloads, the SkillHub FULL vault, the 1.7.0 GitHub source and the API portal, with hash verification and an unprivileged-user warning. Not Ollama. Not a sandbox. No cloud inference."
version: 2.0.3
license: MIT-0
metadata:
  openclaw:
    emoji: "L"
    homepage: "https://chatagent.ca/lygo-llm-console.html"
    requires:
      anyBins: []
    os: [windows, macos, linux]
  lygo: true
  signature: "LYGO-LLM-CONSOLE-POINTER-v2.0.3"
  publisher: deepseekoracle
  steward: "Justin Helmer / Excavationpro / Lightfather"
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-llm-console"
  console_release: "1.7.0"
  package_kind: "pointer"
  bundled_runtime: false
  permissions:
    skill: "no network, no subprocess, no shell, no writes"
    console_runtime: "separate download; loopback HTTP, HTTPS GET, own-folder writes, optional workspace shell/Python; not a sandbox"
---

# LYGO LLM Console — pointer skill v2.0.3

This is a **pointer**, not the console. The console is version **1.7.0**. No runtime, kit,
archive, Python file, executable or script is bundled here.

## Get it

- **1.7.0 PC SETUP.exe:** <https://chatagent.ca/lygoskillhub.html#builds>
  - direct: <https://huggingface.co/DeepSeekOracle/lygo-console-builds/resolve/console-v1.7.0/LYGO_LLM_CONSOLE_1.7.0_PC_SETUP.exe>
- **1.7.0 USB CLAW SETUP.exe:** <https://chatagent.ca/lygoskillhub.html#builds>
  - direct: <https://huggingface.co/DeepSeekOracle/lygo-console-builds/resolve/console-v1.7.0/LYGO_LLM_CONSOLE_1.7.0_USB_SETUP.exe>
- Build card and install notes: <https://chatagent.ca/lygoskillhub.html#builds>
- 1.7.0 source: <https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/lygo_llm_console>
- Online API portal, no local install: <https://chatagent.ca/portal/>

Use only the official downloads or source tree. Verify the published SHA-256 before opening any
installer or archive. The console can run standalone on Windows with a local GGUF model, or use
the API online portal when no local engine is present.

## Run

Unzip into a folder you control. Run `INSTALL.bat` once, put a pinned ggml-org CPU
`llama-server.exe` in `engine/` (or let install fetch it), then run
`LYGO_LLM_CONSOLE.bat` as an unprivileged user. Portal: <http://127.0.0.1:9641/>.

LAN exposure is not default. It requires `--lan --i-consent`.

## Boundary

This skill does nothing on install. The console itself is a separate program: loopback HTTP,
HTTPS GET to public hosts, writes inside its own folder, optional workspace shell/Python,
pinned llama-server subprocess. It is not a sandbox. Keep secrets and unrelated files out of
its folder.

## Why 2.0.x

The 1.6.x ClawHub package embedded a 1.5.7 operator tree. The audit flagged dynamic
execution and incomplete static coverage in that tree. The embedded tree is gone. This
artifact contains only text pointers to the maintained 1.7.0 source and official downloads.

2.0.3 points at the actual 1.7.0 PC and USB installers on the SkillHub Builds card instead of
the older public-kit page.

Steward: Justin Helmer / Excavationpro / Lightfather. RESOURCE, not CANON.
