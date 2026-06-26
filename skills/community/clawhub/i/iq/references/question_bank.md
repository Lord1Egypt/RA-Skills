# IQ Question Bank Reference

This reference document provides patterns, examples, and guidelines for creating IQ test questions across all supported categories.

## Question Categories

### 1. Logical Reasoning

Tests deductive and inductive thinking, pattern recognition in arguments, and valid conclusion drawing.

**Sub-types:**
- **Syllogisms**: Given premises, determine valid conclusions
- **Analogies**: A : B :: C : ? (functional, categorical, proportional)
- **Deductive Puzzles**: Given conditions, deduce relationships or ordering
- **Conditional Logic**: If-Then statements and their valid inferences

**Difficulty Guidelines:**
- Easy: 2-premise syllogisms, simple analogies
- Medium: 3-premise chains, complex analogies, conditional reasoning
- Hard: Nested conditionals, counterintuitive valid conclusions, logic grid puzzles

**Example Patterns:**
```
Easy:   All A are B. All B are C. Conclusion?
Medium: If P then Q. Not Q. Therefore?
Hard:   5 people, 5 attributes, multiple conditional clues
```

### 2. Mathematical Sequences

Tests numerical pattern recognition, abstract reasoning with numbers, and mathematical intuition.

**Common Sequence Types:**
- Arithmetic: +n, -n (e.g., 2, 5, 8, 11 — add 3)
- Geometric: *n, /n (e.g., 3, 6, 12, 24 — multiply by 2)
- Polynomial: n², n³, n²+n (e.g., 2, 6, 12, 20 — n²+n)
- Fibonacci: Each term is sum of two preceding (1, 1, 2, 3, 5, 8...)
- Interleaved: Two alternating sequences (e.g., 1, 10, 3, 20, 5, 30...)
- Prime-based: Related to prime numbers
- Factorial: n! (1, 2, 6, 24, 120...)
- Recursive: Each term derived from previous via formula
- Look-and-say: Describe previous term (1, 11, 21, 1211...)

**Difficulty Guidelines:**
- Easy: Single operation (+, -, *, /), obvious pattern
- Medium: Two operations combined, squares/cubes, Fibonacci
- Hard: Recursive formulas, interleaved sequences, non-obvious patterns

### 3. Pattern Recognition

Tests ability to identify rules in abstract patterns, codes, and symbol systems.

**Sub-types:**
- **Letter Patterns**: Alphabet position patterns, every-nth-letter
- **Symbol Rotation**: Rotational or reflectional symmetry
- **Coding/Decoding**: Letter-to-number, Caesar cipher, word coding
- **Matrix Completion**: 3x3 grid pattern completion
- **Odd One Out**: Identify the item that doesn't belong
- **Number-Shape Relations**: Numbers representing shapes or vice versa

**Example Patterns:**
```
Alphabet: A, C, F, J, ? (skip 1, 2, 3, 4 letters)
Coding: If CAT = 3120, what is DOG? (C=3, A=1, T=20)
Matrix: Top-left + Top-right = Bottom-center
```

### 4. Spatial Visualization

Tests mental manipulation of 2D and 3D objects.

**Sub-types:**
- **Mental Rotation**: Visualize object rotated in space
- **Paper Folding**: Predict hole/crease patterns after unfolding
- **Cube Problems**: Opposite faces, painted cube dissections
- **Shape Assembly**: Combine pieces to form target shape
- **Mirror Images**: Reflections and symmetry
- **3D to 2D**: Net folding, orthographic projection
- **Counting Shapes**: Triangles in complex figures, faces of polyhedra

**Key Formulas:**
- Painted cube: n×n×n cube cut into unit cubes
  - 3-face painted: 8 (always the corners)
  - 2-face painted: 12 × (n-2) (edges excluding corners)
  - 1-face painted: 6 × (n-2)² (face centers)
  - 0-face painted: (n-2)³ (interior)

### 5. Verbal Reasoning

Tests language comprehension, vocabulary, and verbal logic.

**Sub-types:**
- **Synonyms/Antonyms**: Word meaning relationships
- **Analogies**: Word relationship mapping
- **Sentence Completion**: Fill in missing words
- **Odd Word Out**: Identify non-matching word
- **Verbal Classification**: Group words by category
- **Comprehension**: Read passage, answer questions
- **Grammar**: Identify correct sentence structure

**Difficulty Guidelines:**
- Easy: Common words, obvious relationships
- Medium: Less common vocabulary, multi-step reasoning
- Hard: Rare words, complex sentence structures, subtle distinctions

### 6. Memory & Attention

Tests short-term memory, concentration, and information retention.

**Sub-types:**
- **Digit Span**: Recall sequences of numbers
- **Word Lists**: Memorize and recall lists of words
- **Visual Memory**: Remember positions/colors/shapes
- **Selective Attention**: Count occurrences, spot differences
- **Working Memory**: Hold and manipulate information

**Standard Benchmarks:**
- Average digit span (forward): 7 ± 2 digits
- Average word recall (5 items): 4-5 words
- Chunking improves capacity significantly

## Scoring Methodology

### Raw Score to IQ Approximation (For Reference Only)

This is a rough educational estimate, not a clinical assessment:

| Percentage Correct | Approximate IQ Range | Classification |
|--------------------|----------------------|----------------|
| 95-100%            | 130+                 | Very Superior  |
| 85-94%             | 120-129              | Superior       |
| 70-84%             | 110-119              | High Average   |
| 50-69%             | 90-109               | Average        |
| 30-49%             | 80-89                | Low Average    |
| Below 30%          | Below 80             | Below Average  |

### Category Scoring

Track performance per category to identify strengths and weaknesses:

```
Strengths: Categories with >80% correct
Developing: Categories with 50-80% correct
Focus Areas: Categories with <50% correct
```

## Question Generation Best Practices

1. **Clear Wording**: Avoid ambiguity; each question should have exactly one correct answer
2. **Plausible Distractors**: Wrong options should be tempting but clearly wrong upon analysis
3. **Progressive Difficulty**: Tests should start easier and increase in difficulty
4. **Balanced Categories**: Include all categories for a well-rounded assessment
5. **Time Limits**: Consider adding time pressure for more realistic assessment
6. **Explanations Matter**: Always provide explanations; users learn from understanding

## Difficulty Calibration

| Metric | Easy | Medium | Hard |
|--------|------|--------|------|
| Steps to solve | 1-2 | 2-4 | 4+ |
| Familiarity | Common pattern | Recognizable with effort | Novel or obscure |
| Time (typical) | <30 sec | 30-90 sec | 90+ sec |
| Success rate | >70% | 40-70% | <40% |
