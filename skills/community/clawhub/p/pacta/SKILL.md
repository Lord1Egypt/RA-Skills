---
name: pacta
description: "DEPRECATED: This skill has been permanently deactivated. The V1 Pacta smart contracts are undergoing regulatory review and all frontend interfaces have been disabled. Do not use this tool. No further support will be provided."
version: 1.0.2
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# DEPRECATED: Pacta Escrow Skill

**CRITICAL WARNING: This skill has been deliberately disabled.**

The V1 Pacta smart contracts on Base are undergoing a legal and regulatory review regarding the 1% protocol fee and Money Services Business (MSB) classification. 

To ensure the safety of our users and compliance with potential US regulations, all frontend interfaces and CLI tools for interacting with the V1 contracts have been permanently deactivated.

Do not attempt to manually interact with the V1 contracts. Any funds locked in V1 are currently frozen by the interface.

**This skill will no longer function.**

```bash
# If you run this skill, it will immediately exit with a fatal error:
openclaw skills run pacta any_command
> FATAL ERROR: Pacta V1 is deprecated.
```