<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-21 | Updated: 2026-04-21 -->

# references

## Purpose
Schema definitions and terminology normalization for knowledge extraction. Provides the structural blueprint for knowledge cards and standardized TCM constitution terminology.

## Key Files
| File | Description |
|------|-------------|
| `knowledge-card-schema.md` | JSON schema definition for knowledge cards extracted from papers and clinical experiences |
| `ontology.md` | TCM constitution terminology table with synonyms, English translations, and normalization rules |

## For AI Agents

### Working In This Directory
- These are reference documents - do not modify without careful consideration
- Changes to schema require updating `../scripts/extract_knowledge_cards.py`
- Ontology changes affect retrieval accuracy and term normalization

### Knowledge Card Schema Structure
The schema defines two main card types:
- **Paper cards** (`source_type: "paper"`): SCI research papers with methods, results, conclusions
- **Clinical experience cards** (`source_type: "clinical_experience"`): Treatment approaches, case studies, diagnostic insights

### Evidence Levels
| Level | Definition | Use Case |
|-------|------------|----------|
| A | Multiple RCTs or Meta-analyses | Core treatment recommendations |
| B | Single RCT or high-quality cohort study | Important clinical findings |
| C | Case series or expert consensus | Clinical experience summaries |
| D | Expert opinion or case reports | Treatment approach reference |

### Ontology Categories
- **体质类型**: Nine constitution types with aliases
- **证型**: TCM syndrome differentiation patterns
- **疾病**: Chinese-Western disease name mappings
- **治法**: Treatment principle terminology
- **方剂**: Common formulas and Professor Wang's experience formulas
- **药物**: Herb names with aliases

### Testing Requirements
- Validate extracted JSON cards against schema
- Verify terminology normalization in retrieval results

## Dependencies

### Internal
- Used by `../scripts/extract_knowledge_cards.py` for card structure
- Used by `../scripts/ask.py` for term normalization in retrieval

### External
- None (pure reference documentation)

<!-- MANUAL: -->
