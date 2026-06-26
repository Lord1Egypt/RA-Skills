# Matchers Reference

## Equality Matchers

### `toBe(value)`
Uses `Object.is` (strict reference equality). Use for primitives and reference identity.

```javascript
expect(1 + 1).toBe(2);
expect('hello').toBe('hello');
expect(obj).toBe(sameObjRef);
```

### `toEqual(value)`
Deep value equality. Ignores `undefined` properties and does not check class type.

```javascript
expect({ a: 1, b: undefined }).toEqual({ a: 1 }); // passes
expect(new Cat('Mimi')).toEqual({ name: 'Mimi' }); // passes (ignores class)
```

### `toStrictEqual(value)`
Deep equality with strict checks: `undefined` properties, sparse arrays, and class types must match.

```javascript
expect({ a: 1, b: undefined }).not.toStrictEqual({ a: 1 }); // fails — b is missing
expect(new Cat('Mimi')).not.toStrictEqual({ name: 'Mimi' }); // fails — different class
```

## Truthiness Matchers

| Matcher | Matches |
|---|---|
| `toBeNull()` | `null` only |
| `toBeUndefined()` | `undefined` only |
| `toBeDefined()` | anything except `undefined` |
| `toBeTruthy()` | anything `if()` considers true |
| `toBeFalsy()` | `false`, `0`, `''`, `null`, `undefined`, `NaN` |

## Number Matchers

```javascript
expect(value).toBeGreaterThan(3);
expect(value).toBeGreaterThanOrEqual(3);
expect(value).toBeLessThan(5);
expect(value).toBeLessThanOrEqual(5);
expect(0.1 + 0.2).toBeCloseTo(0.3);          // default precision: 5
expect(0.1 + 0.2).toBeCloseTo(0.3, 10);      // custom precision
expect(NaN).toBeNaN();
```

## String Matchers

```javascript
expect('team').toContain('tea');
expect('hello world').toMatch(/world/);
expect('hello world').toMatch('world');       // substring match
expect(str).toHaveLength(5);
```

## Array/Iterable Matchers

```javascript
expect(['a', 'b', 'c']).toContain('b');
expect([{ a: 1 }, { b: 2 }]).toContainEqual({ a: 1 }); // deep equality
expect(arr).toHaveLength(3);
```

## Object Matchers

```javascript
expect(obj).toHaveProperty('key');
expect(obj).toHaveProperty('key', 'value');
expect(obj).toHaveProperty('nested.key');
expect(obj).toHaveProperty(['nested', 'key']);
expect(obj).toMatchObject({ subset: 'value' }); // partial match
```

## Error Matchers

```javascript
expect(() => fn()).toThrow();                    // any error
expect(() => fn()).toThrow('message');            // message substring
expect(() => fn()).toThrow(/regex/);              // message regex
expect(() => fn()).toThrow(TypeError);            // error class
expect(() => fn()).toThrow(new Error('exact'));   // exact error
```

## Promise Matchers

```javascript
await expect(promise).resolves.toBe('value');
await expect(promise).resolves.toEqual({ key: 'value' });
await expect(promise).rejects.toThrow('error');
await expect(promise).rejects.toBeInstanceOf(Error);
```

## Asymmetric Matchers

Asymmetric matchers can be used inside `toEqual`, `toHaveBeenCalledWith`, `toMatchObject`, and snapshot property matchers.

```javascript
expect.any(Number)                         // any instance of Number
expect.any(String)                         // any instance of String
expect.anything()                          // anything except null/undefined
expect.stringContaining('sub')             // string containing substring
expect.stringMatching(/pattern/)           // string matching regex
expect.arrayContaining([1, 2])             // array containing these items
expect.objectContaining({ key: 'val' })    // object containing these properties
expect.not.arrayContaining([3])            // array NOT containing 3
expect.not.objectContaining({ bad: true }) // object NOT containing bad
expect.closeTo(0.3, 5)                     // number close to 0.3
```

### Usage in assertions

```javascript
expect(fn).toHaveBeenCalledWith(
  expect.any(String),
  expect.objectContaining({ role: 'admin' })
);

expect(result).toEqual({
  id: expect.any(Number),
  name: expect.stringContaining('Alice'),
  tags: expect.arrayContaining(['active']),
});
```

## Custom Matchers

```javascript
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        `expected ${received} to be within range ${floor} - ${ceiling}`,
    };
  },
});

expect(100).toBeWithinRange(90, 110);
```

### TypeScript typing for custom matchers

```typescript
declare module 'expect' {
  interface AsymmetricMatchers {
    toBeWithinRange(floor: number, ceiling: number): void;
  }
  interface Matchers<R> {
    toBeWithinRange(floor: number, ceiling: number): R;
  }
}
```

## Mock Function Matchers

```javascript
expect(fn).toHaveBeenCalled();
expect(fn).toHaveBeenCalledTimes(3);
expect(fn).toHaveBeenCalledWith(arg1, arg2);
expect(fn).toHaveBeenLastCalledWith(arg1, arg2);
expect(fn).toHaveBeenNthCalledWith(1, arg1, arg2);
expect(fn).toHaveReturned();
expect(fn).toHaveReturnedTimes(3);
expect(fn).toHaveReturnedWith(value);
expect(fn).toHaveLastReturnedWith(value);
expect(fn).toHaveNthReturnedWith(1, value);
```
