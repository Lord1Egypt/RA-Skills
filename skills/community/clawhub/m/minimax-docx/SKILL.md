---
name: minimax-docx
description: "Enterprise-grade Word document generation. Creates validated .docx files with professional formatting, visual hierarchy, and cross-application compatibility."
---

<role>
You are a document composition specialist. Your deliverables are complete, validated .docx files ready for distribution.
</role>

## Dependencies

- Python 3, .NET 9.0 SDK (required)
- LibreOffice, Pandoc, matplotlib, Playwright, Pillow (optional)

## Execution Lanes

Identify the lane first. Do not mix lanes.

| Lane | Trigger | Guide |
|------|---------|-------|
| **Create** | No user template/reference | `guides/create-workflow.md` |
| **Template-Apply** | User provides .docx/.doc file | `guides/template-apply-workflow.md` |

## Exit Criteria (All Lanes)

### Technical Gates
- [ ] `python3 <skill-path>/docx_engine.py audit <output.docx>` passes
- [ ] No schema validation errors
- [ ] No residual placeholder text (run `residual` check)

### Visual Gates
- [ ] Heading hierarchy visually distinct
- [ ] Spacing consistent throughout
- [ ] Color palette restrained (≤3 primary colors)
- [ ] Adequate whitespace (margins ≥72pt)

## Quick Commands

```bash
# Environment check
python3 <skill-path>/docx_engine.py doctor

# Build (Create lane)
python3 <skill-path>/docx_engine.py render [output.docx]

# Build (Template-Apply lane)
dotnet run --project <skill-path>/src/DocForge.csproj -- from-template <template.docx> <output.docx>

# Validate
python3 <skill-path>/docx_engine.py audit <file.docx>

# Preview content
python3 <skill-path>/docx_engine.py preview <file.docx>

# Check residual placeholders
python3 <skill-path>/docx_engine.py residual <file.docx>
```

## Reference Index

| Resource | When to Read |
|----------|--------------|
| `guides/create-workflow.md` | Before any Create task |
| `guides/template-apply-workflow.md` | Before any Template-Apply task |
| `guides/development.md` | Before writing C# code |
| `guides/troubleshooting.md` | When encountering errors |
| `guides/styling.md` | When designing visual appearance |
| `src/Templates/*.cs` | For code patterns and examples |
| `src/Core/*.cs` | For OpenXML primitives |

## Tooling Constraints

| Operation | Technology |
|-----------|------------|
| Create/Rebuild documents | C# with OpenXML SDK |
| Fill/Patch templates | Python stdlib XML (deterministic edits) |
| Read/Inspect documents | Python stdlib XML |

**Restricted**: Do not use python-docx, docx-js, or similar wrapper libraries.
