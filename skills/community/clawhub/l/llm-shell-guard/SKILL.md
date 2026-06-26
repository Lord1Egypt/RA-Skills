name: linux-command-guard-elite
version: 1.0.0
description: Defense-in-depth Linux command safety skill for AI agents using allowlist-first policy, approval gates, denylist, regex detection, and protected-path checks.
category: security
tags:
  - security
  - linux
  - shell
  - command-execution
  - llm
  - agent-safety
  - openclaw
  - clawhub
---

# Linux Command Guard Elite

Use this skill before any agent executes shell commands on Linux.

## Mandatory policy

1. **Always prefer an allowlist over a denylist.**
   If a command is not explicitly allowed, do not execute it.

2. Denylists are only a backup layer.
   They help catch known-bad patterns, but they are not sufficient by themselves.

3. Never trust wrappers or interpreters as inherently safe.
   Block or require separate sandbox policy for:
   - bash
   - sh
   - zsh
   - dash
   - python / python3
   - perl
   - ruby
   - node
   - php

4. Require manual approval for high-risk commands and binaries, including:
   - sudo
   - su
   - mount / umount
   - systemctl / service
   - iptables / nft / ufw
   - docker / podman / kubectl / nsenter
   - chmod / chown / chattr
   - usermod / userdel / groupdel / passwd
   - package managers

5. Never allow writes, deletes, moves, or redirects into protected system paths.

6. Do not use this skill as the only control.
   Also run the agent in:
   - a sandbox or microVM
   - non-root mode
   - resource-limited environment
   - network-restricted environment when possible

## Recommended execution flow

1. Parse the command safely.
2. Reject command substitution, shell chaining, and redirect abuse.
3. Reject wrappers and interpreters unless a stricter child policy is applied.
4. Check allowlist.
5. Check high-risk approval rules.
6. Check denylist and regex rules.
7. Check protected-path access.
8. Execute only if the command is explicitly safe.

## Strong recommendation

Keep the allowlist small and read-only by default.
