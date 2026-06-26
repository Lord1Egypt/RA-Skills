/**
 * Validation Utils
 * Provides data validation and type checking utilities
 */

// ============================================
// Type Checking
// ============================================

function isString(value) {
  return typeof value === 'string';
}

function isNumber(value) {
  return typeof value === 'number' && !Number.isNaN(value);
}

function isInteger(value) {
  return Number.isInteger(value);
}

function isBoolean(value) {
  return typeof value === 'boolean';
}

function isFunction(value) {
  return typeof value === 'function';
}

function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function isPlainObject(value) {
  if (!isObject(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === null || proto === Object.prototype;
}

function isArray(value) {
  return Array.isArray(value);
}

function isDate(value) {
  return value instanceof Date && !Number.isNaN(value.getTime());
}

function isRegExp(value) {
  return value instanceof RegExp;
}

function isError(value) {
  return value instanceof Error;
}

function isPromise(value) {
  return value !== null && typeof value === 'object' && typeof value.then === 'function';
}

function isSymbol(value) {
  return typeof value === 'symbol';
}

function isBigInt(value) {
  return typeof value === 'bigint';
}

function isMap(value) {
  return value instanceof Map;
}

function isSet(value) {
  return value instanceof Set;
}

function isWeakMap(value) {
  return value instanceof WeakMap;
}

function isWeakSet(value) {
  return value instanceof WeakSet;
}

function isBuffer(value) {
  return Buffer.isBuffer(value);
}

function isArrayBuffer(value) {
  return value instanceof ArrayBuffer;
}

function isTypedArray(value) {
  return ArrayBuffer.isView(value) && !(value instanceof DataView);
}

function isDataView(value) {
  return value instanceof DataView;
}

function isNull(value) {
  return value === null;
}

function isUndefined(value) {
  return value === undefined;
}

function isNil(value) {
  return value === null || value === undefined;
}

function isDefined(value) {
  return value !== undefined;
}

function isTruthy(value) {
  return !!value;
}

function isFalsy(value) {
  return !value;
}

function isEmpty(value) {
  if (isNil(value)) return true;
  if (isString(value)) return value.length === 0;
  if (isArray(value)) return value.length === 0;
  if (isMap(value) || isSet(value)) return value.size === 0;
  if (isObject(value)) return Object.keys(value).length === 0;
  return false;
}

// ============================================
// Number Validation
// ============================================

function isPositive(value) {
  return isNumber(value) && value > 0;
}

function isNegative(value) {
  return isNumber(value) && value < 0;
}

function isZero(value) {
  return value === 0;
}

function isFinite(value) {
  return Number.isFinite(value);
}

function isInfinite(value) {
  return isNumber(value) && !Number.isFinite(value);
}

function isNaN(value) {
  return Number.isNaN(value);
}

function isIntegerInRange(value, min, max) {
  return isInteger(value) && value >= min && value <= max;
}

function isInRange(value, min, max) {
  return isNumber(value) && value >= min && value <= max;
}

function isEven(value) {
  return isInteger(value) && value % 2 === 0;
}

function isOdd(value) {
  return isInteger(value) && value % 2 !== 0;
}

function isPrime(value) {
  if (!isInteger(value) || value < 2) return false;
  if (value === 2) return true;
  if (value % 2 === 0) return false;
  for (let i = 3; i <= Math.sqrt(value); i += 2) {
    if (value % i === 0) return false;
  }
  return true;
}

// ============================================
// String Validation
// ============================================

function isEmptyString(value) {
  return isString(value) && value.length === 0;
}

function isBlankString(value) {
  return isString(value) && value.trim().length === 0;
}

function isNonEmptyString(value) {
  return isString(value) && value.length > 0;
}

function hasLength(value, min, max) {
  if (!isString(value) && !isArray(value)) return false;
  const len = value.length;
  if (min !== undefined && len < min) return false;
  if (max !== undefined && len > max) return false;
  return true;
}

function matches(value, pattern) {
  if (!isString(value)) return false;
  const regex = pattern instanceof RegExp ? pattern : new RegExp(pattern);
  return regex.test(value);
}

function isEmail(value) {
  if (!isString(value)) return false;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(value);
}

function isURL(value) {
  if (!isString(value)) return false;
  try {
    new URL(value);
    return true;
  } catch {
    return false;
  }
}

function isUUID(value, version) {
  if (!isString(value)) return false;
  const patterns = {
    1: /^[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
    2: /^[0-9a-f]{8}-[0-9a-f]{4}-2[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
    3: /^[0-9a-f]{8}-[0-9a-f]{4}-3[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
    4: /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
    5: /^[0-9a-f]{8}-[0-9a-f]{4}-5[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
    any: /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
  };
  const pattern = patterns[version || 'any'];
  return pattern.test(value);
}

function isHexColor(value) {
  if (!isString(value)) return false;
  return /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(value);
}

function isIPv4(value) {
  if (!isString(value)) return false;
  const parts = value.split('.');
  if (parts.length !== 4) return false;
  return parts.every(part => {
    const num = parseInt(part, 10);
    return num >= 0 && num <= 255 && part === String(num);
  });
}

function isIPv6(value) {
  if (!isString(value)) return false;
  const pattern = /^([0-9a-f]{1,4}:){7}[0-9a-f]{1,4}$/i;
  return pattern.test(value);
}

function isIP(value) {
  return isIPv4(value) || isIPv6(value);
}

function isJSON(value) {
  if (!isString(value)) return false;
  try {
    JSON.parse(value);
    return true;
  } catch {
    return false;
  }
}

function isBase64(value) {
  if (!isString(value)) return false;
  return /^[A-Za-z0-9+/]*={0,2}$/.test(value);
}

function isAlpha(value) {
  if (!isString(value)) return false;
  return /^[a-zA-Z]+$/.test(value);
}

function isAlphanumeric(value) {
  if (!isString(value)) return false;
  return /^[a-zA-Z0-9]+$/.test(value);
}

function isNumeric(value) {
  if (!isString(value)) return false;
  return /^[0-9]+$/.test(value);
}

function isLowercase(value) {
  if (!isString(value)) return false;
  return value === value.toLowerCase();
}

function isUppercase(value) {
  if (!isString(value)) return false;
  return value === value.toUpperCase();
}

// ============================================
// Date Validation
// ============================================

function isValidDate(value) {
  return isDate(value);
}

function isPastDate(value) {
  if (!isDate(value)) return false;
  return value.getTime() < Date.now();
}

function isFutureDate(value) {
  if (!isDate(value)) return false;
  return value.getTime() > Date.now();
}

function isToday(value) {
  if (!isDate(value)) return false;
  const today = new Date();
  return value.toDateString() === today.toDateString();
}

function isDateInRange(value, start, end) {
  if (!isDate(value) || !isDate(start) || !isDate(end)) return false;
  const time = value.getTime();
  return time >= start.getTime() && time <= end.getTime();
}

// ============================================
// Object Validation
// ============================================

function hasKey(obj, key) {
  return isObject(obj) && Object.prototype.hasOwnProperty.call(obj, key);
}

function hasKeys(obj, keys) {
  return isObject(obj) && keys.every(key => hasKey(obj, key));
}

function hasAnyKey(obj, keys) {
  return isObject(obj) && keys.some(key => hasKey(obj, key));
}

function isInstanceOf(value, constructor) {
  return value instanceof constructor;
}

// ============================================
// Schema Validation
// ============================================

function validate(value, schema) {
  const errors = [];
  
  function validateField(val, sch, path = '') {
    if (sch.required && isNil(val)) {
      errors.push({ path, message: 'Field is required' });
      return;
    }
    
    if (isNil(val)) return;
    
    if (sch.type) {
      const typeCheck = {
        string: isString,
        number: isNumber,
        integer: isInteger,
        boolean: isBoolean,
        array: isArray,
        object: isObject,
        date: isDate,
        function: isFunction
      };
      
      const checker = typeCheck[sch.type];
      if (checker && !checker(val)) {
        errors.push({ path, message: `Expected ${sch.type}` });
        return;
      }
    }
    
    if (sch.validator && !sch.validator(val)) {
      errors.push({ path, message: sch.message || 'Validation failed' });
    }
    
    if (sch.min !== undefined && val < sch.min) {
      errors.push({ path, message: `Must be at least ${sch.min}` });
    }
    
    if (sch.max !== undefined && val > sch.max) {
      errors.push({ path, message: `Must be at most ${sch.max}` });
    }
    
    if (sch.minLength !== undefined && val.length < sch.minLength) {
      errors.push({ path, message: `Must have at least ${sch.minLength} characters` });
    }
    
    if (sch.maxLength !== undefined && val.length > sch.maxLength) {
      errors.push({ path, message: `Must have at most ${sch.maxLength} characters` });
    }
    
    if (sch.pattern && !matches(val, sch.pattern)) {
      errors.push({ path, message: 'Does not match pattern' });
    }
    
    if (sch.enum && !sch.enum.includes(val)) {
      errors.push({ path, message: `Must be one of: ${sch.enum.join(', ')}` });
    }
    
    if (sch.properties && isObject(val)) {
      for (const [key, propSchema] of Object.entries(sch.properties)) {
        validateField(val[key], propSchema, path ? `${path}.${key}` : key);
      }
    }
    
    if (sch.items && isArray(val)) {
      val.forEach((item, index) => {
        validateField(item, sch.items, path ? `${path}[${index}]` : `[${index}]`);
      });
    }
  }
  
  validateField(value, schema);
  
  return {
    valid: errors.length === 0,
    errors
  };
}

// ============================================
// Assertion
// ============================================

function assert(condition, message = 'Assertion failed') {
  if (!condition) {
    throw new Error(message);
  }
}

function assertType(value, type, message) {
  const typeCheck = {
    string: isString,
    number: isNumber,
    integer: isInteger,
    boolean: isBoolean,
    array: isArray,
    object: isObject,
    date: isDate,
    function: isFunction
  };
  
  const checker = typeCheck[type];
  if (!checker || !checker(value)) {
    throw new Error(message || `Expected ${type}, got ${typeof value}`);
  }
}

function assertDefined(value, message = 'Value is undefined') {
  if (isUndefined(value)) {
    throw new Error(message);
  }
}

function assertNotNull(value, message = 'Value is null') {
  if (isNull(value)) {
    throw new Error(message);
  }
}

function assertNotNil(value, message = 'Value is null or undefined') {
  if (isNil(value)) {
    throw new Error(message);
  }
}

function assertRange(value, min, max, message) {
  if (!isNumber(value) || value < min || value > max) {
    throw new Error(message || `Value must be between ${min} and ${max}`);
  }
}

function assertOneOf(value, values, message) {
  if (!values.includes(value)) {
    throw new Error(message || `Value must be one of: ${values.join(', ')}`);
  }
}

// ============================================
// Validator Builders
// ============================================

function required(validator) {
  return (value) => !isNil(value) && validator(value);
}

function optional(validator) {
  return (value) => isNil(value) || validator(value);
}

function allOf(...validators) {
  return (value) => validators.every(v => v(value));
}

function anyOf(...validators) {
  return (value) => validators.some(v => v(value));
}

function not(validator) {
  return (value) => !validator(value);
}

// ============================================
// Main Entry Point
// ============================================

function main() {
  console.log('✅ Validation Utils Skill\n');
  
  // Test type checking
  console.log('Testing type checking:');
  console.log(`isString('hello'): ${isString('hello')}`);
  console.log(`isNumber(42): ${isNumber(42)}`);
  console.log(`isArray([1,2,3]): ${isArray([1,2,3])}`);
  console.log(`isObject({a:1}): ${isObject({a:1})}`);
  console.log(`isNull(null): ${isNull(null)}`);
  console.log(`isNil(undefined): ${isNil(undefined)}`);
  
  // Test number validation
  console.log('\nTesting number validation:');
  console.log(`isPositive(5): ${isPositive(5)}`);
  console.log(`isInRange(5, 1, 10): ${isInRange(5, 1, 10)}`);
  console.log(`isEven(4): ${isEven(4)}`);
  console.log(`isPrime(7): ${isPrime(7)}`);
  
  // Test string validation
  console.log('\nTesting string validation:');
  console.log(`isEmail('test@example.com'): ${isEmail('test@example.com')}`);
  console.log(`isURL('https://example.com'): ${isURL('https://example.com')}`);
  console.log(`isUUID('550e8400-e29b-41d4-a716-446655440000'): ${isUUID('550e8400-e29b-41d4-a716-446655440000')}`);
  console.log(`isIPv4('192.168.1.1'): ${isIPv4('192.168.1.1')}`);
  console.log(`isAlpha('hello'): ${isAlpha('hello')}`);
  console.log(`isAlphanumeric('hello123'): ${isAlphanumeric('hello123')}`);
  
  // Test schema validation
  console.log('\nTesting schema validation:');
  const schema = {
    type: 'object',
    properties: {
      name: { type: 'string', minLength: 1 },
      age: { type: 'number', min: 0, max: 150 },
      email: { validator: isEmail, message: 'Invalid email' }
    }
  };
  const result = validate({ name: 'John', age: 30, email: 'john@example.com' }, schema);
  console.log(`validate({name:'John',age:30,email:'john@example.com'}): valid=${result.valid}`);
  
  const badResult = validate({ name: '', age: 200, email: 'invalid' }, schema);
  console.log(`validate({name:'',age:200,email:'invalid'}): valid=${badResult.valid}, errors=${badResult.errors.length}`);
  
  // Test assertions
  console.log('\nTesting assertions:');
  try {
    assert(true, 'Should not throw');
    console.log('assert(true): passed');
  } catch {
    console.log('assert(true): failed');
  }
  
  try {
    assertNotNil('value');
    console.log('assertNotNil("value"): passed');
  } catch {
    console.log('assertNotNil("value"): failed');
  }
  
  // Test validator builders
  console.log('\nTesting validator builders:');
  const isPositiveNumber = required(isNumber);
  console.log(`required(isNumber)(5): ${isPositiveNumber(5)}`);
  console.log(`required(isNumber)(null): ${isPositiveNumber(null)}`);
  
  const isStringOrNumber = anyOf(isString, isNumber);
  console.log(`anyOf(isString, isNumber)('hello'): ${isStringOrNumber('hello')}`);
  console.log(`anyOf(isString, isNumber)(42): ${isStringOrNumber(42)}`);
  
  console.log('\n✅ validation-utils loaded successfully');
}

module.exports = {
  // Type checking
  isString,
  isNumber,
  isInteger,
  isBoolean,
  isFunction,
  isObject,
  isPlainObject,
  isArray,
  isDate,
  isRegExp,
  isError,
  isPromise,
  isSymbol,
  isBigInt,
  isMap,
  isSet,
  isWeakMap,
  isWeakSet,
  isBuffer,
  isArrayBuffer,
  isTypedArray,
  isDataView,
  isNull,
  isUndefined,
  isNil,
  isDefined,
  isTruthy,
  isFalsy,
  isEmpty,
  
  // Number validation
  isPositive,
  isNegative,
  isZero,
  isFinite,
  isInfinite,
  isNaN,
  isIntegerInRange,
  isInRange,
  isEven,
  isOdd,
  isPrime,
  
  // String validation
  isEmptyString,
  isBlankString,
  isNonEmptyString,
  hasLength,
  matches,
  isEmail,
  isURL,
  isUUID,
  isHexColor,
  isIPv4,
  isIPv6,
  isIP,
  isJSON,
  isBase64,
  isAlpha,
  isAlphanumeric,
  isNumeric,
  isLowercase,
  isUppercase,
  
  // Date validation
  isValidDate,
  isPastDate,
  isFutureDate,
  isToday,
  isDateInRange,
  
  // Object validation
  hasKey,
  hasKeys,
  hasAnyKey,
  isInstanceOf,
  
  // Schema validation
  validate,
  
  // Assertion
  assert,
  assertType,
  assertDefined,
  assertNotNull,
  assertNotNil,
  assertRange,
  assertOneOf,
  
  // Validator builders
  required,
  optional,
  allOf,
  anyOf,
  not,
  
  main
};
