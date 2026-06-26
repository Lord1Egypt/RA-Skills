# Quality Assurance & Testing Engine

Ensuring everything delivered meets high standards — code, content, analysis, and output.

---

## 1. Testing Philosophy

### The Testing Pyramid
```
    /  E2E Tests  \        ← Few, slow, high confidence
   / Integration    \      ← Some, medium speed
  /    Unit Tests    \     ← Many, fast, focused
```

### What to Test
- **Happy path**: Does it work with correct input?
- **Edge cases**: Empty, null, huge, negative, zero, special chars
- **Error paths**: Does it fail gracefully?
- **Performance**: Does it scale? Memory leaks?

---

## 2. Code Testing

### Python Testing
```python
import pytest

def add(a, b):
    return a + b

# Happy path
def test_add_positive():
    assert add(2, 3) == 5

# Edge cases
def test_add_zero():
    assert add(0, 0) == 0
def test_add_negative():
    assert add(-1, -2) == -3
def test_add_floats():
    assert abs(add(0.1, 0.2) - 0.3) < 1e-10

# Error cases
def test_add_invalid():
    with pytest.raises(TypeError):
        add("a", 2)
```

### JavaScript Testing
```javascript
// Using built-in assert or vitest/jest
function add(a, b) { return a + b; }

assert.strictEqual(add(2, 3), 5);
assert.strictEqual(add(0, 0), 0);
assert.strictEqual(add(-1, -2), -3);
assert.throws(() => add("a", 2));
```

### Shell Script Testing
```bash
# Test with various inputs
./script.sh "normal input"          # Happy path
./script.sh ""                       # Empty input
./script.sh "$(cat large_file.txt)"  # Large input
./script.sh "special chars: $@#!"    # Special chars
echo $?                              # Check exit code
```

---

## 3. Content Quality

### Writing Checklist
- [ ] Clear thesis/main point
- [ ] Logical structure
- [ ] No grammatical errors
- [ ] Consistent tone/style
- [ ] Proper citations
- [ ] No plagiarism
- [ ] Appropriate length
- [ ] Scannable formatting

### Code Review Checklist
- [ ] Does what it claims
- [ ] Handles errors
- [ ] No security issues
- [ ] Efficient (no unnecessary work)
- [ ] Readable (clear names, comments)
- [ ] Follows project style
- [ ] No dead code
- [ ] Tests included

### Data Quality Checklist
- [ ] Source documented
- [ ] Types are consistent
- [ ] No missing critical fields
- [ ] No obvious outliers/errors
- [ ] Sufficient sample size
- [ ] Transformations documented

---

## 4. Output Verification

### Before Delivering Anything
1. **Run it** — Execute code, verify output
2. **Read it** — Proofread text, check logic
3. **Test it** — Try edge cases, error paths
4. **Check it** — Verify against requirements
5. **Format it** — Clean presentation

### Self-Review Process
- Wait 1 minute, then re-read with fresh eyes
- Read backwards (end to start) for typos
- Run linting/formatting tools
- Check for leftover debug code/comments
- Verify file paths and references

---

## 5. Regression Prevention

### Before Changing Existing Code
1. Run existing tests
2. Understand what depends on this code
3. Make the minimal change
4. Run tests again
5. Check for side effects

### Version Control Hygiene
- Atomic commits (one logical change each)
- Descriptive commit messages
- Never commit secrets
- Review changes before committing
