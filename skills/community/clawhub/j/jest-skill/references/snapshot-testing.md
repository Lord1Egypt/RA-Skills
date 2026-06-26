# Snapshot Testing Reference

## Basic Usage

### `toMatchSnapshot(propertyMatchers?, hint?)`

Compares the serialized value against a stored snapshot file (`.snap`). On first run, creates the snapshot. On subsequent runs, compares against it.

```javascript
test('renders correctly', () => {
  const tree = renderer.create(<Button label="Click" />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

### `toMatchInlineSnapshot(propertyMatchers?, snapshot?)`

Same as `toMatchSnapshot` but stores the snapshot inline in the test file. Jest auto-updates the inline snapshot string.

```javascript
test('formats greeting', () => {
  expect(formatGreeting('Alice')).toMatchInlineSnapshot(`"Hello, Alice!"`);
});
```

On first run, the snapshot string is auto-inserted:

```javascript
// Before first run:
expect(formatGreeting('Alice')).toMatchInlineSnapshot();

// After first run (auto-filled):
expect(formatGreeting('Alice')).toMatchInlineSnapshot(`"Hello, Alice!"`);
```

## Property Matchers

For objects with dynamic fields (timestamps, IDs), property matchers assert the type while letting the snapshot pin the static fields.

```javascript
test('creates user', () => {
  expect(createUser({ name: 'Alice' })).toMatchSnapshot({
    id: expect.any(String),
    createdAt: expect.any(Date),
  });
});
// Stored snapshot:
// Object {
//   "id": Any<String>,
//   "name": "Alice",
//   "createdAt": Any<Date>,
// }
```

Works with inline snapshots too:

```javascript
expect(createUser({ name: 'Alice' })).toMatchInlineSnapshot(
  { id: expect.any(String), createdAt: expect.any(Date) },
  `
  {
    "id": Any<String>,
    "name": "Alice",
    "createdAt": Any<Date>,
  }
  `
);
```

## Updating Snapshots

```bash
# Update all snapshots
npx jest --updateSnapshot
npx jest -u

# Update snapshots for specific tests
npx jest -u --testPathPattern='Button'

# In watch mode: press 'u' to update failed snapshots
```

## Snapshot Files

- Stored in `__snapshots__/` directory adjacent to the test file.
- File extension: `.snap`.
- Should be committed to version control.
- Review snapshot diffs carefully in PRs — they represent behavioral changes.

## Custom Serializers

Serializers control how objects are rendered in snapshots.

```javascript
// jest.config.js
module.exports = {
  snapshotSerializers: ['enzyme-to-json/serializer'],
};
```

### Writing a custom serializer

```javascript
// my-serializer.js
module.exports = {
  test(val) {
    return val && val.hasOwnProperty('myCustomProp');
  },
  serialize(val, config, indentation, depth, refs, printer) {
    return `MyCustom<${val.myCustomProp}>`;
  },
};
```

```javascript
// Add inline
expect.addSnapshotSerializer({
  test: (val) => typeof val === 'string' && val.startsWith('$$'),
  serialize: (val) => `Token(${val.slice(2)})`,
});
```

## Snapshot Format

```javascript
// jest.config.js
module.exports = {
  snapshotFormat: {
    escapeString: true,
    printBasicPrototype: false, // don't print "Object {" — just "{"
  },
};
```

## Best Practices

### Keep snapshots small

Snapshot large component trees into individual pieces:

```javascript
// Bad: entire page
expect(renderer.create(<Page />).toJSON()).toMatchSnapshot();

// Good: individual components
expect(renderer.create(<Header />).toJSON()).toMatchSnapshot();
expect(renderer.create(<Sidebar />).toJSON()).toMatchSnapshot();
```

### Prefer inline snapshots for small values

```javascript
expect(formatCurrency(1234.5)).toMatchInlineSnapshot(`"$1,234.50"`);
```

### Use descriptive hint parameters

```javascript
expect(tree).toMatchSnapshot('initial render');
expect(tree).toMatchSnapshot('after clicking button');
```

### Mock non-deterministic values

```javascript
jest.useFakeTimers({ now: new Date('2024-01-01') });
jest.spyOn(Math, 'random').mockReturnValue(0.5);
```

## toThrowErrorMatchingSnapshot

```javascript
test('throws formatted error', () => {
  expect(() => validate(null)).toThrowErrorMatchingSnapshot();
});

test('throws formatted error inline', () => {
  expect(() => validate(null)).toThrowErrorMatchingInlineSnapshot(
    `"Validation failed: value must not be null"`
  );
});
```

## Asymmetric Matchers in Snapshots

You can use asymmetric matchers as property matchers:

```javascript
expect(response).toMatchSnapshot({
  body: {
    users: expect.arrayContaining([
      expect.objectContaining({ role: 'admin' }),
    ]),
    total: expect.any(Number),
    timestamp: expect.stringMatching(/^\d{4}-\d{2}-\d{2}/),
  },
});
```
