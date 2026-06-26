# OpenClaw Skill EEAT Benchmark

> **Complete 80-Item Benchmark for AI Agent Skill Quality Evaluation** — Adapted from CORE-EEAT framework for OpenClaw Skills, focusing on utility, security, and reliability.

## Benchmark Structure

This benchmark defines 80 evaluation items across 8 dimensions, specifically adapted for OpenClaw Skills (modular AI agent capabilities defined by `SKILL.md` files).

### Dimension Overview

| Dimension | Code Context | Items | Focus Area |
|-----------|--------------|-------|------------|
| **C** - Correctness & Clarity | Skill Purpose & Logic | 10 | Does the skill do what it claims? |
| **O** - Organization & Structure | Skill Structure & Layout | 10 | Is the skill well-organized? |
| **R** - Referenceability & Reliability | Skill Quality & Consistency | 10 | Is the skill reliable and maintainable? |
| **E** - Exclusivity & Efficiency | Unique Value & Performance | 10 | Does the skill offer unique value? |
| **Exp** - Experience | Real-World Usage & Testing | 10 | Has the skill been tested in practice? |
| **Ept** - Expertise | Technical Standards & Best Practices | 10 | Does it follow professional standards? |
| **A** - Authority | Ecosystem Trust & Community | 10 | Is the skill trusted by the community? |
| **T** - Trust | Security & Safety | 10 | Is the skill safe to use? |

---

## CORE Dimensions (40 Items) — Skill Context

### C — Correctness & Clarity (Intent & Logic)

**Goal**: Ensure the skill delivers on its promises with clear, predictable behavior.

| ID | Check Item | Skill Context | Scoring Standard |
|----|------------|---------------|------------------|
| C01 🎯 | Intent Alignment | Skill description matches actual functionality | **Pass (10)**: Description accurately reflects all features<br>**Partial (5)**: Minor discrepancies or vague language<br>**Fail (0)**: Misleading or false claims |
| C02 🎯 | Direct Result | Skill produces clear, observable outputs | **Pass (10)**: Outputs are well-structured and actionable<br>**Partial (5)**: Outputs exist but require post-processing<br>**Fail (0)**: Ambiguous or inconsistent outputs |
| C03 | Edge Cases | Skill handles boundary conditions gracefully | **Pass (10)**: All documented edge cases handled<br>**Partial (5)**: Some edge cases crash or fail<br>**Fail (0)**: No edge case handling |
| C04 | Type Definitions | Input/output types are clearly defined | **Pass (10)**: Complete type annotations in prompts and scripts<br>**Partial (5)**: Partial type information<br>**Fail (0)**: No type definitions |
| C05 | Skill Scope | Well-defined boundaries and limitations | **Pass (10)**: Clear in-scope and out-of-scope documented<br>**Partial (5)**: Scope mentioned but unclear<br>**Fail (0)**: No scope definition |
| C06 | Target Context | Appropriate for intended use cases | **Pass (10)**: Perfect fit for target scenarios<br>**Partial (5)**: Works in some but not all target scenarios<br>**Fail (0)**: Mismatched with target use cases |
| C07 | Control Flow | Prompt instructions are logical and sequential | **Pass (10)**: Clear step-by-step instructions<br>**Partial (5)**: Some logical gaps or inconsistencies<br>**Fail (0)**: Disorganized or contradictory instructions |
| C08 | Usage Patterns | Clear API/tool usage patterns | **Pass (10)**: Explicit tool invocation examples<br>**Partial (5)**: Vague or implicit usage<br>**Fail (0)**: No usage guidance |
| C09 | Error Cases | Proper error handling and recovery | **Pass (10)**: Comprehensive error handling with messages<br>**Partial (5)**: Basic error handling<br>**Fail (0)**: No error handling |
| C10 | Semantic Closure | Complete logic, no loose ends | **Pass (10)**: All operations have clear completion<br>**Partial (5)**: Some operations may hang<br>**Fail (0)**: Incomplete workflows |

**C Dimension Score**: (Sum of scores) / 10

---

### O — Organization & Structure

**Goal**: Ensure the skill is well-structured, modular, and easy to navigate.

| ID | Check Item | Skill Context | Scoring Standard |
|----|------------|---------------|------------------|
| O01 🎯 | Module Hierarchy | Clear directory structure (SKILL.md, scripts/, references/) | **Pass (10)**: Follows OpenClaw convention<br>**Partial (5)**: Deviates but understandable<br>**Fail (0)**: Chaotic structure |
| O02 | Interface Summary | Clear skill metadata in YAML frontmatter | **Pass (10)**: All required fields present (name, description, version)<br>**Partial (5)**: Missing some metadata<br>**Fail (0)**: No or invalid frontmatter |
| O03 | Data Structures | Well-defined data schemas and types | **Pass (10)**: Clear input/output schemas<br>**Partial (5)**: Some schema ambiguity<br>**Fail (0)**: No schema definitions |
| O04 | List/Sequence | Proper handling of collections/arrays | **Pass (10)**: Correct batch/array processing<br>**Partial (5)**: Limited collection support<br>**Fail (0)**: Fails with collections |
| O05 | Schema/Type Markers | Type hints in scripts and prompts | **Pass (10)**: Comprehensive type annotations<br>**Partial (5)**: Partial annotations<br>**Fail (0)**: No type hints |
| O06 | Function Length | Reasonable prompt/section sizes | **Pass (10)**: Prompts under 2000 tokens, modular sections<br>**Partial (5)**: Some long sections<br>**Fail (0)**: Monolithic, difficult to follow |
| O07 | Visual Hierarchy | Clear formatting, headings, code blocks | **Pass (10)**: Professional Markdown formatting<br>**Partial (5)**: Basic formatting<br>**Fail (0)**: Poor or no formatting |
| O08 | Navigation | Easy to find relevant sections | **Pass (10)**: Clear sections, table of contents<br>**Partial (5)**: Some navigation aid<br>**Fail (0)**: Hard to navigate |
| O09 | Density | Balanced information density | **Pass (10)**: Appropriate detail level<br>**Partial (5)**: Too dense or too sparse<br>**Fail (0)**: Information overload or too sparse |
| O10 | Multimedia | Diagrams, screenshots, visual aids | **Pass (10)**: Includes helpful visuals<br>**Partial (5)**: Basic visuals<br>**Fail (0)**: No visual aids |

**O Dimension Score**: (Sum of scores) / 10

---

### R — Referenceability & Reliability

**Goal**: Ensure the skill is reliable, testable, and maintainable.

| ID | Check Item | Skill Context | Scoring Standard |
|----|------------|---------------|------------------|
| R01 | Test Precision | Clear test scenarios and expectations | **Pass (10)**: Comprehensive test cases documented<br>**Partial (5)**: Some test examples<br>**Fail (0)**: No testing guidance |
| R02 | Coverage | Sufficient test coverage for key paths | **Pass (10)**: All major paths testable<br>**Partial (5)**: Partial test coverage<br>**Fail (0)**: No testability consideration |
| R03 | Source Authority | Uses trusted dependencies and APIs | **Pass (10)**: All dependencies vetted and stable<br>**Partial (5)**: Some dependencies questionable<br>**Fail (0)**: Uses untrusted or deprecated deps |
| R04 | Evidence | Assertions, validations, checks in code | **Pass (10)**: Robust validation throughout<br>**Partial (5)**: Some validation<br>**Fail (0)**: No validation |
| R05 | Methodology | Clear algorithms and approaches | **Pass (10)**: Well-documented approach<br>**Partial (5)**: Vague methodology<br>**Fail (0)**: No clear method |
| R06 | Versioning | Semantic versioning and change logs | **Pass (10)**: Proper semver, changelog maintained<br>**Partial (5)**: Basic versioning<br>**Fail (0)**: No versioning |
| R07 | Entity Precision | Consistent naming conventions | **Pass (10)**: Professional, consistent naming<br>**Partial (5)**: Some inconsistency<br>**Fail (0)**: Chaotic naming |
| R08 | Internal References | Clear module/script dependencies | **Pass (10)**: Well-documented dependencies<br>**Partial (5)**: Some dependency info<br>**Fail (0)**: No dependency documentation |
| R09 | Semantics | Meaningful variable/function names | **Pass (10)**: Self-documenting code<br>**Partial (5)**: Some unclear names<br>**Fail (0)**: Cryptic or misleading names |
| R10 ⚠️ | Consistency | No contradictions, consistent behavior | **Pass (10)**: Fully consistent<br>**Fail (0)**: Contradictions or unpredictable behavior |

**R Dimension Score**: (Sum of scores) / 10

---

### E — Exclusivity & Efficiency

**Goal**: Ensure the skill offers unique value and performs efficiently.

| ID | Check Item | Skill Context | Scoring Standard |
|----|------------|---------------|------------------|
| E01 | Original Algorithms | Custom implementations, not just wrappers | **Pass (10)**: Novel or optimized approach<br>**Partial (5)**: Standard implementation<br>**Fail (0)**: Trivial wrapper |
| E02 | Innovative Patterns | Novel design patterns or workflows | **Pass (10)**: Creative solution<br>**Partial (5)**: Conventional approach<br>**Fail (0)**: Generic or copied |
| E03 | Benchmarks | Performance metrics documented | **Pass (10)**: Comprehensive benchmarks<br>**Partial (5)**: Basic timing info<br>**Fail (0)**: No performance data |
| E04 | Alternative Approaches | Considers multiple solutions | **Pass (10)**: Compares alternatives<br>**Partial (5)**: Mentions alternatives<br>**Fail (0)**: Single solution only |
| E05 | Visual Assets | Diagrams, flowcharts, architecture | **Pass (10)**: Rich visual documentation<br>**Partial (5)**: Basic visuals<br>**Fail (0)**: No visual assets |
| E06 | Gap Filling | Solves unaddressed problems | **Pass (10)**: Fills clear gap<br>**Partial (5)**: Incremental improvement<br>**Fail (0)**: Redundant solution |
| E07 | Utilities | Helper functions, convenience methods | **Pass (10)**: Useful utilities included<br>**Partial (5)**: Basic utilities<br>**Fail (0)**: No utilities |
| E08 | Depth | Comprehensive implementation | **Pass (10)**: Full-featured<br>**Partial (5)**: Partial implementation<br>**Fail (0)**: Shallow or incomplete |
| E09 | Integration | Good ecosystem integration | **Pass (10)**: Seamless OpenClaw integration<br>**Partial (5)**: Basic integration<br>**Fail (0)**: Poor integration |
| E10 | Future-Proof | Anticipates changes and updates | **Pass (10)**: Forward-compatible design<br>**Partial (5)**: Some consideration<br>**Fail (0)**: Brittle design |

**E Dimension Score**: (Sum of scores) / 10

---

## EEAT Dimensions (40 Items) — Skill Context

### Exp — Experience (Practical Testing)

**Goal**: Ensure the skill demonstrates real-world testing and usage.

| ID | Check Item | Skill Context | Scoring Standard |
|----|------------|---------------|------------------|
| Exp01 | Usage Examples | Demonstrates skill usage with examples | **Pass (10)**: Multiple, varied examples<br>**Partial (5)**: Basic example<br>**Fail (0)**: No examples |
| Exp02 | Observable Behavior | Logging, metrics, or debug output | **Pass (10)**: Comprehensive logging<br>**Partial (5)**: Basic logging<br>**Fail (0)**: No observability |
| Exp03 | Process Docs | Step-by-step workflow documentation | **Pass (10)**: Clear workflow guide<br>**Partial (5)**: Basic steps<br>**Fail (0)**: No workflow docs |
| Exp04 | Substantive Proof | Screenshots, demo outputs, evidence | **Pass (10)**: Rich evidence of working skill<br>**Partial (5)**: Basic evidence<br>**Fail (0)**: No proof |
| Exp05 | Runtime Duration | Performance characteristics documented | **Pass (10)**: Detailed performance info<br>**Partial (5)**: Basic timing info<br>**Fail (0)**: No performance data |
| Exp06 | Issues Encountered | Known limitations documented | **Pass (10)**: Honest, detailed limitations<br>**Partial (5)**: Basic limitations list<br>**Fail (0)**: No limitations documented |
| Exp07 | Before/After | Comparative improvements shown | **Pass (10)**: Clear comparison<br>**Partial (5)**: Some comparison<br>**Fail (0)**: No comparison |
| Exp08 | Quantified Metrics | Benchmarks, success rates, SLAs | **Pass (10)**: Comprehensive metrics<br>**Partial (5)**: Basic metrics<br>**Fail (0)**: No metrics |
| Exp09 | Stress Testing | Load tests, edge case testing | **Pass (10)**: Stress testing documented<br>**Partial (5)**: Basic edge testing<br>**Fail (0)**: No stress testing |
| Exp10 | Limitations | Honest capability documentation | **Pass (10)**: Thorough limitations section<br>**Partial (5)**: Some limitations<br>**Fail (0)**: Overly optimistic claims |

**Exp Dimension Score**: (Sum of scores) / 10

---

### Ept — Expertise (Technical Proficiency)

**Goal**: Ensure the skill demonstrates professional engineering standards.

| ID | Check Item | Skill Context | Scoring Standard |
|----|------------|---------------|------------------|
| Ept01 | Author Identity | Clear skill author attribution | **Pass (10)**: Complete author info<br>**Partial (5)**: Basic author info<br>**Fail (0)**: No author attribution |
| Ept02 | Credentials | Links to portfolio, GitHub, expertise | **Pass (10)**: Verified credentials<br>**Partial (5)**: Some credentials<br>**Fail (0)**: No credentials |
| Ept03 🎯 | Professional Terminology | Standard AI/ML/programming terminology | **Pass (10)**: Accurate, professional language<br>**Partial (5)**: Some jargon or imprecise terms<br>**Fail (0)**: Inaccurate or amateurish |
| Ept04 | Technical Depth | Appropriate complexity for the task | **Pass (10)**: Right level of depth<br>**Partial (5)**: Too shallow or too complex<br>**Fail (0)**: Mismatched complexity |
| Ept05 | Methodology | Follows skill engineering best practices | **Pass (10)**: Professional approach<br>**Partial (5)**: Decent methodology<br>**Fail (0)**: Poor or no methodology |
| Ept06 | Edge Cases | Handles corner cases professionally | **Pass (10)**: Comprehensive edge case handling<br>**Partial (5)**: Some edge cases<br>**Fail (0)**: Ignores edge cases |
| Ept07 | Historical Context | References best practices or standards | **Pass (10)**: Well-researched, references standards<br>**Partial (5)**: Some references<br>**Fail (0)**: No context |
| Ept08 🎯 | Reasoning | Prompts are self-explanatory | **Pass (10)**: Clear, logical instructions<br>**Partial (5)**: Some ambiguity<br>**Fail (0)**: Confusing or illogical |
| Ept09 | Cross-Domain | Integrates multiple concerns well | **Pass (10)**: Holistic approach<br>**Partial (5)**: Limited integration<br>**Fail (0)**: Siloed thinking |
| Ept10 | Review Process | Code review or peer review evidence | **Pass (10)**: Review process documented<br>**Partial (5)**: Some review mentions<br>**Fail (0)**: No review process |

**Ept Dimension Score**: (Sum of scores) / 10

---

### A — Authority (Ecosystem Standing)

**Goal**: Ensure the skill and its repository have community trust.

| ID | Check Item | Skill Context | Scoring Standard |
|----|------------|---------------|------------------|
| A01 | Dependencies | Quality and security of upstream deps | **Pass (10)**: All deps are reputable<br>**Partial (5)**: Some deps questionable<br>**Fail (0)**: Uses problematic deps<br>**N/A**: No external deps |
| A02 | Community Mentions | References, citations, usage | **Pass (10)**: Widely referenced<br>**Partial (5)**: Some mentions<br>**Fail (0)**: No mentions<br>**N/A**: New skill |
| A03 | Awards/Badges | CI badges, security scores, quality indicators | **Pass (10)**: Multiple quality badges<br>**Partial (5)**: Basic badges<br>**Fail (0)**: No badges |
| A04 | Release History | Stable, frequent updates | **Pass (10)**: Active, stable releases<br>**Partial (5)**: Sporadic updates<br>**Fail (0)**: Abandoned or unstable |
| A05 | Brand/Repo Recognition | Repository reputation and trust | **Pass (10)**: Highly regarded repo<br>**Partial (5)**: Moderate reputation<br>**Fail (0)**: Unknown or suspicious |
| A06 | Social Proof | Stars, forks, contributors, downloads | **Pass (10)**: Strong community adoption<br>**Partial (5)**: Some adoption<br>**Fail (0)**: No adoption<br>**N/A**: Private skill |
| A07 | Package Index | Listed on ClawHub or package managers | **Pass (10)**: Official listing<br>**Partial (5)**: Informal listing<br>**Fail (0)**: Not listed |
| A08 | Entity Consistency | Consistent naming across ecosystem | **Pass (10)**: Consistent branding<br>**Partial (5)**: Some inconsistency<br>**Fail (0)**: Confusing naming |
| A09 | Partner Integrations | Official or verified integrations | **Pass (10)**: Official integrations<br>**Partial (5)**: Unofficial integrations<br>**Fail (0)**: No integrations |
| A10 | Community Response | Issue resolution, support activity | **Pass (10)**: Active, responsive support<br>**Partial (5)**: Some response<br>**Fail (0)**: Unresponsive community |

**A Dimension Score**: (Sum of scores) / 10

---

### T — Trust (Reliability & Security)

**Goal**: Ensure the skill is trustworthy, secure, and safe to use.

| ID | Check Item | Skill Context | Scoring Standard |
|----|------------|---------------|------------------|
| T01 | Legal Compliance | License compliance, proper attribution | **Pass (10)**: Clear, compliant license<br>**Partial (5)**: License ambiguity<br>**Fail (0)**: License violation or no license |
| T02 | Contact Info | Maintainer is contactable | **Pass (10)**: Multiple contact methods<br>**Partial (5)**: Basic contact info<br>**Fail (0)**: No way to contact maintainer |
| T03 🎯 | Security Standards | Secure coding practices in scripts | **Pass (10)**: Follows security best practices<br>**Partial (5)**: Some security measures<br>**Fail (0)**: No security consideration |
| T04 ⚠️ | Disclosure | Security vulnerabilities disclosed | **Pass (10)**: Transparent about issues<br>**Fail (0)**: Hidden vulnerabilities or no disclosure |
| T05 | Code Review Policy | Review standards documented | **Pass (10)**: Clear review process<br>**Partial (5)**: Basic review mention<br>**Fail (0)**: No review process |
| T06 | Deprecation Policy | Version management and deprecation | **Pass (10)**: Clear deprecation policy<br>**Partial (5)**: Basic version info<br>**Fail (0)**: No deprecation planning |
| T07 | Dependency Hygiene | No vulnerable dependencies | **Pass (10)**: All deps secure and updated<br>**Partial (5)**: Some outdated deps<br>**Fail (0)**: Vulnerable dependencies |
| T08 | Risk Disclaimers | Beta/alpha warnings, risk disclosures | **Pass (10)**: Clear risk communication<br>**Partial (5)**: Basic warnings<br>**Fail (0)**: No risk disclosure |
| T09 | Authenticity | Not plagiarized, properly attributed | **Pass (10)**: Original or properly attributed<br>**Partial (5)**: Some attribution missing<br>**Fail (0)**: Plagiarized or uncredited |
| T10 | Support Channels | Issues, discussions, help docs | **Pass (10)**: Comprehensive support resources<br>**Partial (5)**: Basic support<br>**Fail (0)**: No support channels |

**T Dimension Score**: (Sum of scores) / 10

---

## Veto Items (Critical Failures)

These items, if failed, prevent skill installation or use:

- **C10**: Semantic Closure - Incomplete workflows
- **R10**: Consistency - Contradictory behavior
- **T03**: Security Standards - No security consideration
- **T04**: Disclosure - Hidden vulnerabilities
- **T07**: Dependency Hygiene - Vulnerable dependencies

**Action**: If any veto item fails, do not install or use the skill until fixed.

---

## GEO-First Items (🎯)

These items are critical for AI agent citation and reuse:

- **C01**: Intent Alignment - Clear, accurate purpose
- **C02**: Direct Result - Observable, actionable outputs
- **O01**: Module Hierarchy - Standard structure
- **O02**: Interface Summary - Complete metadata
- **Ept03**: Professional Terminology - Accurate language
- **Ept08**: Reasoning - Self-explanatory prompts
- **T03**: Security Standards - Secure implementation

**Focus**: Prioritize these for skills intended to be widely adopted or cited by AI agents.

---

## Skill Type Weightings

Different skill types prioritize different dimensions:

### Productivity Skills
- C: 30% | O: 5% | R: 25% | E: 0% | Exp: 20% | Ept: 15% | A: 5% | T: 0%

### Development Skills
- C: 25% | O: 20% | R: 20% | E: 5% | Exp: 5% | Ept: 20% | A: 5% | T: 0%

### Research Skills
- C: 25% | O: 10% | R: 25% | E: 15% | Exp: 0% | Ept: 0% | A: 20% | T: 5%

### Automation Skills
- T: 30% | C: 25% | O: 15% | R: 20% | E: 0% | Exp: 5% | Ept: 5% | A: 0%

### Content Skills
- C: 30% | O: 15% | R: 5% | E: 25% | Exp: 20% | Ept: 5% | A: 0% | T: 0%

### System Skills
- T: 25% | C: 20% | O: 10% | R: 20% | E: 15% | Exp: 5% | Ept: 5% | A: 0%

---

## Scoring Summary

**Dimension Score** = (Sum of item scores) / 10

**System Scores**:
- **GEO Score** (AI Citation Potential) = (C + O + R + E) / 4
- **SEO Score** (Utility & Trust) = (Exp + Ept + A + T) / 4

**Weighted Total Score** = Σ (Dimension Score × Skill Type Weight)

**Rating Standards**:
- 90-100: Excellent
- 75-89: Good
- 60-74: Fair
- 40-59: Poor
- 0-39: Critical
