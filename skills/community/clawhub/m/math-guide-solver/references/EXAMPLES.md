# Math Solver Skill - Test Cases & Examples

## Test Case 1: Simple Fraction Addition
```
Problem Image: "Simplify: 1/2 + 1/3"

Expected Output:
- OCR Recognition: ✓ Text recognized
- LaTeX Extraction: \frac{1}{2} + \frac{1}{3}
- Solution Guidance:
  1. What do we need to add fractions?
     → Common denominator
  2. What's the LCD of 2 and 3?
     → 6
  3. Rewrite fractions...
```

## Test Case 2: Quadratic Equation
```
Problem: "Solve: x^2 + 2x + 1 = 0"

Processing:
1. Domain: algebra
2. Difficulty: intermediate
3. LaTeX: x^{2} + 2x + 1 = 0
4. Extracted LaTeX in quadratic form: (x+1)^2 = 0

Socratic Guidance:
- "What form is this equation?"
- "Can you factor the left side?"
- "What's the solution?"
```

## Test Case 3: Limit Problem
```
Problem: "Find: lim(x→0) sin(x)/x"

LaTeX: \lim_{x \to 0} \frac{\sin(x)}{x}

Detailed Solution:
Step 1: Recognize this as indeterminate form 0/0
Step 2: Option A - Apply L'Hôpital's rule
Step 3: Option B - Use Taylor series
```

## Test Case 4: Batch Processing
```
Input: Folder with 5 homework photos

Output:
- problem_1_fractions.png
- problem_2_quadratic.png
- problem_3_geometry.png
- problem_4_calculus.png
- problem_5_statistics.png

Plus: solution_guide.md with all solutions
```

## Example Usage Scenarios

### Scenario 1: Student Learning
```
User: [Uploads photo of quadratic equation]
Skill Response:
1. Extracts: x^2 + 5x + 6 = 0
2. Renders formula in light theme
3. Provides Socratic hints:
   - "What method would you use?"
   - "Can you factor?"
4. Student works through problem
5. Asks for hints if stuck
6. Finally requests full solution
```

### Scenario 2: Homework Checking
```
User: "Check my work on these 3 problems"
Skill:
1. Processes all 3 images
2. Extracts formulas
3. Renders in dark theme (user preference)
4. Compares student answers with solutions
5. Provides detailed feedback
```

### Scenario 3: Formula Reference
```
User: "Make a beautiful PNG of Einstein's E=mc²"
Skill:
1. Converts to LaTeX: E = mc^{2}
2. Renders with chalk theme
3. Returns high-quality PNG
4. Can customize size/colors
```

## Performance Benchmarks

### OCR Accuracy
- Clear print: 95%+
- Handwriting (good): 80-90%
- Handwriting (poor): 60-70%

### LaTeX Conversion
- Simple formulas: 98%
- Complex formulas: 85%
- Edge cases: 70%

### Rendering Speed
- Single formula: <2 seconds
- Batch (10 formulas): <15 seconds
- High-quality (600 DPI): +2x time

## Integration Points

### With OpenClaw Gateway
```python
# In OpenClaw agent
response = await openclaw.call_skill(
    'math-solver',
    {
        'input_image': image_bytes,
        'mode': 'socratic',
        'theme': 'dark'
    }
)
```

### With External APIs (Optional)
- **Wolfram Alpha**: Answer verification
- **Mathpix**: Enhanced OCR for complex formulas
- **Symbolab**: Alternative solution methods

## Error Recovery

### If OCR Fails
```
User: [Blurry image]
Skill: "I couldn't read this clearly. Could you..."
→ Suggest retake photo
→ Offer manual LaTeX input
```

### If LaTeX Invalid
```
Extracted: "x²+2x+1=0" → Attempts: "x^2+2x+1=0"
If still invalid: Shows detected formula, asks for correction
```

### If Problem Type Unrecognized
```
"I'm not confident about this problem type.
Would you like to:"
- Specify the domain (algebra/geometry/etc.)
- Provide hints about the method
- Try a different approach
```

## Configuration Examples

### For Teachers
```yaml
config:
  mode: detailed
  theme: sepia
  include_step_by_step: true
  include_alternative_methods: true
  language: en
```

### For Students
```yaml
config:
  mode: socratic
  theme: light
  step_detail_level: low  # Hints only, not answers
  progressive_revealing: true  # Hints get stronger
```

### For Quick Reference
```yaml
config:
  mode: quick
  theme: dark
  formula_size: large
  dpi: 600  # High quality for printing
```

## Known Issues & Workarounds

### Issue: Mixed handwriting/print
**Status:** Known issue
**Workaround:** Clarify which parts are formulas

### Issue: Complex diagrams with formulas
**Status:** Limited support
**Workaround:** Crop formula area, use separately

### Issue: Non-English problems
**Status:** Beta support
**Workaround:** Specify language in preferences

## Future Enhancements

### Phase 2
- [ ] Video walkthrough generation
- [ ] Interactive problem solver
- [ ] Formula suggestion/autocomplete
- [ ] Handwriting style preservation

### Phase 3
- [ ] Real-time camera mode
- [ ] AR formula overlay
- [ ] Collaborative problem solving
- [ ] AI tutoring integration

