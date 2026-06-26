# Quality Checklist for Paper-to-Table

## Pre-Extraction Checks

- [ ] Paper text was successfully extracted (not empty or error message)
- [ ] Paper contains identifiable sections or coherent content
- [ ] Language is correctly identified
- [ ] Table headers are clearly defined

## Extraction Quality Checks

### Fidelity Verification
- [ ] Each extracted value can be traced to a specific location in the paper
- [ ] No information was invented or hallucinated
- [ ] Numerical values match exactly (no rounding unless specified)
- [ ] Author names are complete and correctly ordered
- [ ] Technical terms are preserved accurately

### Completeness Check
- [ ] All table headers have corresponding extracted values
- [ ] "N/A" is used appropriately (not as a shortcut for "didn't check")
- [ ] Multi-value fields use proper separator (semicolon)
- [ ] Subfields are not conflated (e.g., sample size vs. effect size)

### Confidence Assessment
- [ ] Each field has a confidence rating
- [ ] LOW confidence fields are flagged for human review
- [ ] No field is marked HIGH confidence without clear evidence
- [ ] MEDIUM confidence fields include reasoning

## Domain-Specific Validation

### Psychology
- [ ] Sample demographics match reported values
- [ ] Experimental design is correctly classified
- [ ] Psychometric measures include reliability if reported
- [ ] Effect sizes include confidence intervals if available

### Cognitive Neuroscience
- [ ] Brain regions use standard anatomical nomenclature
- [ ] MNI coordinates are correctly transcribed
- [ ] Imaging parameters match reported values
- [ ] Preprocessing steps are accurately described

### Computer Science
- [ ] Algorithm names are correctly identified
- [ ] Dataset sizes match reported values
- [ ] Metrics are clearly identified (primary vs. secondary)
- [ ] Code availability links are valid URLs

### Brain Science
- [ ] Species and strain are correctly identified
- [ ] Recording/stimulation parameters are accurately extracted
- [ ] Cell type markers are correctly named
- [ ] Behavioral task parameters match reported values

## Post-Extraction Checks

- [ ] JSON is well-formed and valid
- [ ] All keys match table headers exactly (case-sensitive)
- [ ] No duplicate entries (check against existing table)
- [ ] Data types are appropriate for each column
- [ ] Special characters are properly escaped

## Error Handling

### Paper Extraction Failures
- Log error type and paper identifier
- Attempt fallback extraction methods
- Flag for manual review if all methods fail

### Missing Information
- Distinguish between "not in paper" and "extraction failed"
- Mark clearly with "N/A" and reason
- Do not guess or infer

### Ambiguous Information
- Mark confidence as LOW
- Include multiple possible interpretations if relevant
- Flag for human review

## Batch Processing Quality

- [ ] Each paper processed independently
- [ ] Progress logged for each paper
- [ ] Failed papers don't block successful ones
- [ ] Summary report includes success/failure counts
- [ ] Output file is valid and readable
