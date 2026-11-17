# Knowledge Base -- Syllabus-Based Subject Registry

## Build Priority: LOW (Deferred -- Phase 3 of Build Sequence)

**IMPORTANT:** This file is intentionally constructed last in the build sequence. The initial build creates the file with its structural skeleton and high-level outline; subsequent compilation passes populate the detailed syllabus-by-syllabus content.

---

## Purpose

This knowledge base serves as the subject matter registry for the k12-teacher skill. It is organized by teaching syllabus (教学大纲) rather than by grade level alone. Each teaching syllabus published by the Ministry of Education (or equivalent regional authority) maps to one or more grade levels and subjects, and the knowledge base is structured to allow retrieval by syllabus identifier.

The knowledge base supports three education stages:
- **Stage 1: Primary Education** (Grades 1-6)
- **Stage 2: Junior Secondary Education** (Grades 7-9)
- **Stage 3: Senior Secondary Education** (Grades 10-12)

---

## Syllabus-Based Organization

The knowledge base is organized by teaching syllabus rather than by grade level. Each syllabus entry contains the following structured fields:

### Syllabus Entry Schema

| Field | Description | Example |
|---|---|---|
| Syllabus ID | Unique identifier for the syllabus | MOE-2022-MATH-PRIMARY |
| Syllabus Title | Full title of the syllabus | Mathematics Teaching Syllabus for Compulsory Education |
| Version | Version number of the syllabus | 2022 Edition |
| Issuing Authority | Organization that published the syllabus | Ministry of Education / 教育部 |
| Effective Date | Date the syllabus becomes effective | 2022-09-01 |
| Expiration Date | Date the syllabus expires (if applicable) | null (active) |
| Applicable Grade Levels | Grade levels covered by this syllabus | Grades 1-6 |
| Applicable Subjects | Subjects covered by this syllabus | Mathematics, Chinese Language, Science |
| Topic Outline | Structured topic-by-topic content outline | See section below |
| Recommended Teaching Hours | Total recommended instructional hours | 672 hours (Grades 1-6) |
| Assessment Standards | Competencies and assessment criteria | See assessment standards section |

### Topic Outline Structure

Each syllabus topic outline follows this hierarchical structure:

- **Unit/Module**: Major thematic grouping
  - **Topic**: Specific concept or skill area
    - **Learning Objectives**: What learners should know and be able to do
    - **Key Concepts**: Core ideas and terminology
    - **Prerequisites**: Prior knowledge required
    - **Suggested Activities**: Recommended instructional strategies
    - **Assessment Items**: Sample assessment questions or tasks

---

## Structural Skeleton

The knowledge base comprises three interconnected files that form a cohesive syllabus-based retrieval system:

### 1. Syllabus Registry (references/syllabus-registry.md)

Purpose: Living index of all known teaching syllabi with version tracking and change history.

Structure per entry:
- Syllabus ID and title
- Version number and release date
- Issuing authority
- Status (active, deprecated, superseded)
- Last download timestamp
- Change log reference

This file serves as the canonical index that the knowledge base update mechanism maintains. Every update operation must synchronize this registry with the actual state of the knowledge base.

### 2. Syllabus Content (references/knowledge-base.md)

Purpose: Complete topic outlines for each syllabus, mapped to the knowledge base structure defined above.

This file contains the actual subject matter content organized by syllabus ID. Each syllabus entry includes the full topic outline with learning objectives, key concepts, prerequisites, suggested activities, and assessment items.

### 3. Grade-Level Crosswalk (references/grade-crosswalk.md)

Purpose: Mapping between grade-level organization and syllabus-based organization, providing backward compatibility and supporting legacy references that use grade-level addressing.

Structure:
- Grade level to syllabus ID mapping (one-to-many allowed)
- Subject-level crosswalk entries
- Jurisdiction tags for regional variations
- Deprecated mappings with replacement references

---

## Knowledge Base Update Mechanism

This skill supports automatic updating of the knowledge base by downloading teaching syllabi from official sources (e.g., Ministry of Education website). The update mechanism comprises the following components:

### Download Script

File: `scripts/knowledge-base-update.sh`

Capabilities:
- **Download mode**: `--download <syllabus-id>` fetches syllabus from configured official sources
- **Local mode**: `--local <path-to-file>` processes a manually downloaded syllabus document
- **Parse**: Extract topic outlines, learning objectives, teaching hours, and assessment standards
- **Map**: Associate extracted content to syllabus-based organization structure
- **Validate**: Run post-update validation via `scripts/validate-structure.sh`
- **Log**: Record all operations in CHANGELOG.md under appropriate sections

### Syllabus Registry

File: `references/syllabus-registry.md`

The syllabus registry maintains a living index of all downloaded syllabi. Each entry includes:
- Syllabus ID and title
- Version number and release date
- Issuing authority
- Status (active, deprecated, superseded)
- Last download timestamp
- Change log reference

### Update Triggers

Updates can be triggered by:
- **Manual execution**: Run `scripts/knowledge-base-update.sh --download <syllabus-id>`
- **Cron job scheduling**: Automated periodic checks for syllabus updates
- **CI/CD pipeline trigger**: Automated update as part of the build pipeline

### Validation

After any update operation, run `scripts/validate-structure.sh` to ensure all quality gates pass (G-01 through G-10). This verifies:
- File existence and non-emptiness
- Content structure compliance
- Constraint compliance (no emoji, English only, etc.)
- Cross-reference integrity

---

## Build Strategy

### Pass 1: Initial Compile (Skeleton)

The initial compilation pass creates the file with its structural skeleton only:
- Syllabus registry skeleton with placeholder entries for known syllabi
- Grade-level crosswalk headers with mapping structure
- Subject category outlines with topic structure templates
- Update mechanism documentation and scripts

This pass establishes the file structure and organization without populating detailed content.

### Pass 2+: Content Population

Subsequent compilation passes fill in syllabus-specific content:
- Populate each syllabus entry with complete topic outlines
- Reference official curriculum standards documents
- Map content to the grade-level crosswalk
- Update the syllabus registry with version metadata

Each content pass should be tracked in CHANGELOG.md with scope description.

### Version Tracking

Each syllabus update should create a new version entry in `references/syllabus-registry.md`. Download and update operations should be logged in `CHANGELOG.md` under the "Changed" or "Added" sections as appropriate.

---

## Syllabus Index (Skeleton)

The following is a preliminary index of teaching syllabi to be populated in subsequent passes. Syllabi are organized by issuing authority and education stage.

### Ministry of Education (教育部) -- Compulsory Education Stage

| Syllabus ID | Title | Stage | Grades | Subjects | Status |
|---|---|---|---|---|---|
| MOE-2022-MATH-PRIMARY | Mathematics Teaching Syllabus (Primary) | Stage 1 | Grades 1-6 | Mathematics | Pending Population |
| MOE-2022-CHN-PRIMARY | Chinese Language Teaching Syllabus (Primary) | Stage 1 | Grades 1-6 | Chinese Language | Pending Population |
| MOE-2022-SCI-PRIMARY | Science Teaching Syllabus (Primary) | Stage 1 | Grades 3-6 | Science | Pending Population |
| MOE-2022-MATH-JUNIOR | Mathematics Teaching Syllabus (Junior Secondary) | Stage 2 | Grades 7-9 | Mathematics | Pending Population |
| MOE-2022-CHN-JUNIOR | Chinese Language Teaching Syllabus (Junior Secondary) | Stage 2 | Grades 7-9 | Chinese Language | Pending Population |
| MOE-2022-SCI-JUNIOR | Science Teaching Syllabus (Junior Secondary) | Stage 2 | Grades 7-9 | Science | Pending Population |
| MOE-2022-HIST-JUNIOR | History Teaching Syllabus (Junior Secondary) | Stage 2 | Grades 7-9 | History | Pending Population |

### Ministry of Education (教育部) -- Senior Secondary Stage

| Syllabus ID | Title | Stage | Grades | Subjects | Status |
|---|---|---|---|---|---|
| MOE-2022-MATH-SENIOR | Mathematics Teaching Syllabus (Senior) | Stage 3 | Grades 10-12 | Mathematics | Pending Population |
| MOE-2022-CHN-SENIOR | Chinese Language Teaching Syllabus (Senior) | Stage 3 | Grades 10-12 | Chinese Language | Pending Population |
| MOE-2022-PHY-SENIOR | Physics Teaching Syllabus (Senior) | Stage 3 | Grades 10-12 | Physics | Pending Population |
| MOE-2022-CHE-SENIOR | Chemistry Teaching Syllabus (Senior) | Stage 3 | Grades 10-12 | Chemistry | Pending Population |
| MOE-2022-BIO-SENIOR | Biology Teaching Syllabus (Senior) | Stage 3 | Grades 10-12 | Biology | Pending Population |
| MOE-2022-HIST-SENIOR | History Teaching Syllabus (Senior) | Stage 3 | Grades 10-12 | History | Pending Population |
| MOE-2022-GEO-SENIOR | Geography Teaching Syllabus (Senior) | Stage 3 | Grades 10-12 | Geography | Pending Population |

### Provincial Education Departments

| Syllabus ID | Title | Stage | Grades | Subjects | Status |
|---|---|---|---|---|---|
| GD-2023-MATH-PRIMARY | Guangdong Province Mathematics Syllabus (Primary) | Stage 1 | Grades 1-6 | Mathematics | Pending Population |
| GD-2023-SCI-JUNIOR | Guangdong Province Science Syllabus (Junior) | Stage 2 | Grades 7-9 | Science | Pending Population |

---

## Grade-Level Crosswalk (Skeleton)

The following crosswalk maps grade levels to syllabus IDs. This mapping is populated in subsequent passes.

### Stage 1: Primary Education (Grades 1-6)

| Grade | Mathematics Syllabus | Chinese Language Syllabus | Science Syllabus |
|---|---|---|---|
| Grade 1 | MOE-2022-MATH-PRIMARY | MOE-2022-CHN-PRIMARY | -- |
| Grade 2 | MOE-2022-MATH-PRIMARY | MOE-2022-CHN-PRIMARY | -- |
| Grade 3 | MOE-2022-MATH-PRIMARY | MOE-2022-CHN-PRIMARY | MOE-2022-SCI-PRIMARY |
| Grade 4 | MOE-2022-MATH-PRIMARY | MOE-2022-CHN-PRIMARY | MOE-2022-SCI-PRIMARY |
| Grade 5 | MOE-2022-MATH-PRIMARY | MOE-2022-CHN-PRIMARY | MOE-2022-SCI-PRIMARY |
| Grade 6 | MOE-2022-MATH-PRIMARY | MOE-2022-CHN-PRIMARY | MOE-2022-SCI-PRIMARY |

### Stage 2: Junior Secondary Education (Grades 7-9)

| Grade | Mathematics Syllabus | Chinese Language Syllabus | Science Syllabus | History Syllabus |
|---|---|---|---|---|
| Grade 7 | MOE-2022-MATH-JUNIOR | MOE-2022-CHN-JUNIOR | MOE-2022-SCI-JUNIOR | MOE-2022-HIST-JUNIOR |
| Grade 8 | MOE-2022-MATH-JUNIOR | MOE-2022-CHN-JUNIOR | MOE-2022-SCI-JUNIOR | MOE-2022-HIST-JUNIOR |
| Grade 9 | MOE-2022-MATH-JUNIOR | MOE-2022-CHN-JUNIOR | MOE-2022-SCI-JUNIOR | MOE-2022-HIST-JUNIOR |

### Stage 3: Senior Secondary Education (Grades 10-12)

| Grade | Mathematics Syllabus | Chinese Language Syllabus | Physics | Chemistry | Biology | History | Geography |
|---|---|---|---|---|---|---|---|
| Grade 10 | MOE-2022-MATH-SENIOR | MOE-2022-CHN-SENIOR | MOE-2022-PHY-SENIOR | MOE-2022-CHE-SENIOR | MOE-2022-BIO-SENIOR | MOE-2022-HIST-SENIOR | MOE-2022-GEO-SENIOR |
| Grade 11 | MOE-2022-MATH-SENIOR | MOE-2022-CHN-SENIOR | MOE-2022-PHY-SENIOR | MOE-2022-CHE-SENIOR | MOE-2022-BIO-SENIOR | MOE-2022-HIST-SENIOR | MOE-2022-GEO-SENIOR |
| Grade 12 | MOE-2022-MATH-SENIOR | MOE-2022-CHN-SENIOR | MOE-2022-PHY-SENIOR | MOE-2022-CHE-SENIOR | MOE-2022-BIO-SENIOR | MOE-2022-HIST-SENIOR | MOE-2022-GEO-SENIOR |

---

## Knowledge Base Update Procedure

For detailed instructions on updating the knowledge base, see Section 15 of README_FOR_AI.md.

### Quick Reference

1. **Identify Target Syllabus**: Check `references/syllabus-registry.md` for currently tracked syllabi
2. **Download**: Run `scripts/knowledge-base-update.sh --download <syllabus-id>`
3. **Parse**: Script extracts topic outlines, learning objectives, teaching hours, assessment standards
4. **Validate**: Run `scripts/validate-structure.sh` to ensure all quality gates pass
5. **Review**: Manually review changes for accuracy
6. **Commit**: Use message format `docs(kb): update <syllabus-id> to version <x.y>`
7. **Changelog**: Update CHANGELOG.md with update scope

### Supported Sources

- Ministry of Education (教育部) official website: https://www.moe.gov.cn
- Provincial education department websites
- Locally adopted curriculum standards documents
- Custom sources configured via script parameters

### Update Frequency

- Monitor for new syllabus releases quarterly
- Major syllabus revisions trigger a MINOR version bump
- Minor topic adjustments trigger a PATCH version bump
- Emergency updates for critical errors trigger an immediate PATCH

### Fallback Procedure

If automated download fails:
1. Manually download the syllabus document
2. Place it in the `downloads/syllabus/` directory
3. Run `scripts/knowledge-base-update.sh --local <path-to-file>`
4. Review and merge changes
5. Run full validation suite (`scripts/validate-structure.sh`)
6. Commit and update CHANGELOG.md

### Security Considerations

- Always verify the authenticity of downloaded syllabus documents against official sources
- Validate file integrity (checksums) before processing
- Review parsed content before merging into the knowledge base
- Maintain audit trail of all download and update operations in CHANGELOG.md

---

## Maintenance Notes

- This file is a living document. Populate syllabus content in subsequent compilation passes.
- Each syllabus update must synchronize the syllabus registry (`references/syllabus-registry.md`) with the actual state of the knowledge base.
- Grade-level crosswalk entries (`references/grade-crosswalk.md`) must be updated when new syllabi are added or existing ones are modified.
- All changes must be tracked in CHANGELOG.md with appropriate scope descriptions.
- Run `scripts/validate-structure.sh` after every update to ensure quality gate compliance.

---

*This file is part of the k12-teacher skill. License: GNU GPL v3.*
