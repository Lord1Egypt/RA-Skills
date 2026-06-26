# Workflow Patterns

## Sequential Workflow

For linear processes where each step depends on the previous:

```markdown
## Workflow

1. **Step 1**: [Action]
   - [sub-step a]
   - [sub-step b]

2. **Step 2**: [Action]
   - Verify output from Step 1

3. **Step 3**: [Action]
   - [sub-step]
```

## Conditional Workflow

For branching based on user input or state:

```markdown
## Workflow

1. **Check condition**
   - If [condition A]: Go to Section A
   - If [condition B]: Go to Section B

2. **Section A**: [Actions for condition A]

3. **Section B**: [Actions for condition B]

4. **Finalize**: [Common final steps]
```

## Loop Workflow

For iterative processes:

```markdown
## Workflow

1. **Initialize**: Set up initial state

2. **Iterate** (until condition met):
   - Process current item
   - Check if more items remain
   - If yes: continue loop
   - If no: exit loop

3. **Finalize**: Clean up, report results
```

## Error Recovery Workflow

```markdown
## Workflow

1. **Attempt primary method**
   - If success: continue to step 3
   - If failure: go to step 2

2. **Fallback method**
   - Try alternative approach
   - If success: continue
   - If failure: report error

3. **Verify**: Confirm expected outcome
```

## Interactive Workflow

For tasks requiring user input:

```markdown
## Workflow

1. **Gather requirements**
   - Ask user for [input 1]
   - Ask user for [input 2]

2. **Process**
   - [Process based on inputs]

3. **Present results**
   - Show output
   - Ask for confirmation or adjustments

4. **Finalize** (after user confirms)
   - [Final actions]
```

## Parallel Workflow

For independent tasks:

```markdown
## Workflow

1. **Start** (all can run in parallel):
   - Task A: [description]
   - Task B: [description]
   - Task C: [description]

2. **Wait for all** to complete

3. **Combine results**:
   - Merge outputs from A, B, C
```

---

## Best Practices

- **Name steps clearly**: Use descriptive step names
- **Include verification**: After each major step, verify success
- **Handle errors**: Always have a fallback path
- **Keep it simple**: If a workflow has >7 steps, consider breaking it into sub-workflows
- **Document decisions**: Note why certain branches exist
