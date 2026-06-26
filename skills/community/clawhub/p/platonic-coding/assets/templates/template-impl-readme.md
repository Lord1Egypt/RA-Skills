# {{PROJECT_NAME}} Implementation Guides

This directory contains implementation guides that translate RFC specifications into concrete, project-specific designs.

## Purpose

Implementation guides bridge the gap between abstract specs (RFCs) and actual code. They provide:

- Concrete module/package structure
- Type definitions with full field specifications
- Interface/trait/class definitions
- Implementation details and algorithms
- Error handling strategies
- Testing approaches

## Relationship to Specs

```
RFC Specification (abstract, what)
        |
        v
Implementation Guide (concrete, how)   <-- This directory
        |
        v
Actual Code (executable)
```

Implementation guides **supersede** RFC specs with concrete details but **MUST NOT contradict** them.

## Creating a New Guide

Use the **platonic-impl** skill to create implementation guides and implement code:

```
Use platonic-impl to implement RFC-NNN targeting the <module-name> module.
```

Or create a guide only (without coding):

```
Use platonic-impl to create a guide for RFC-NNN targeting the <module-name> module.
```

## Guide Template

Use the **platonic-impl** skill which includes its own template for generating implementation guides.

## Naming Convention

Implementation guides should follow the pattern `IG-<number>-semantic-short-desc.md`:

- `IG-001-user-authentication.md` - User authentication implementation
- `IG-042-message-queue-protocol.md` - Message queue protocol implementation
- `IG-053-cli-command-nesting.md` - CLI command nesting implementation

The number typically corresponds to the RFC number it implements.
