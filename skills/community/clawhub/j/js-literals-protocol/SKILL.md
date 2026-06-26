---
name: "js-literals-protocol"
description: "Implements a JavaScript literal syntax-based protocol for LLM tool calls. Invoke when needing to enable LLM to call local JS functions using template literal syntax."
---

# JavaScript Literals Protocol Tool Skill

## Overview
This skill establishes a new protocol for LLM to call tools using JavaScript's template literal syntax. It allows seamless integration between LLM prompts and local JavaScript functions through a tag function mechanism.

## Protocol Definition

### Core Concept
The protocol uses JavaScript template literals with tag functions to enable LLM to invoke local functions. This provides a natural, JavaScript-native way for LLMs to interact with tools.

### Syntax Format
```javascript
// Define variables
const var1 = value1;
const var2 = value2;

// Define tag function (tool)
function toolTag(strings, ...expressions) {
  // Process the strings and expressions
  // Return the result
}

// LLM invokes the tool using template literal syntax
const result = toolTag`Template ${var1} with ${var2} expressions`;
```

## Usage Example

### Basic Function Call
```javascript
// Define variables
const person = "Mike";
const age = 28;

// Define a simple tool function
function describePerson(strings, personExp, ageExp) {
  const str0 = strings[0]; // "That " 
  const str1 = strings[1]; // " is a " 
  const str2 = strings[2]; // "." 
  
  const ageStr = ageExp > 99 ? "centenarian" : "youngster";
  
  return `${str0}${personExp}${str1}${ageStr}${str2}`;
}

// LLM invokes the tool
const output = describePerson`That ${person} is a ${age}.`;

console.log(output);
// Output: That Mike is a youngster.
```

### Multi-Parameter Tool Call
```javascript
// Define a calculation tool
function calculate(strings, ...nums) {
  const operation = strings.join(' ').trim();
  let result;
  
  if (operation.includes('add')) {
    result = nums.reduce((a, b) => a + b, 0);
  } else if (operation.includes('multiply')) {
    result = nums.reduce((a, b) => a * b, 1);
  }
  
  return `${operation} ${nums.join(', ')} = ${result}`;
}

// LLM invokes with multiple parameters
const sum = calculate`add ${5} ${3} ${7}`;
const product = calculate`multiply ${2} ${4} ${6}`;

console.log(sum);     // Output: add 5, 3, 7 = 15
console.log(product); // Output: multiply 2, 4, 6 = 48
```

## Implementation Guidelines

### For Developers Creating Tools
1. Define tag functions that accept `strings` as the first parameter and variable expressions as rest parameters
2. Process the template strings and expressions appropriately
3. Return a result that provides meaningful feedback to the LLM

### For LLMs Using the Protocol
1. Use the template literal syntax with backticks
2. Insert variables and expressions inside `${}` placeholders
3. Call the appropriate tag function as the prefix to the template literal

## Benefits

1. **JavaScript Native**: Uses existing JavaScript syntax that developers are familiar with
2. **Natural Integration**: Seamlessly blends with JavaScript code
3. **Type Safety**: Leverages JavaScript's type system
4. **Flexible**: Supports multiple parameters and complex logic
5. **Readable**: Provides clear, self-documenting tool calls

## Limitations

1. Requires JavaScript runtime environment
2. Template literal syntax may need special handling in some LLM prompts
3. Limited to JavaScript function capabilities

## Example Workflow

1. Developer defines local tool functions using tag function pattern
2. LLM is instructed to use the JavaScript literals protocol
3. LLM generates template literal calls to the defined tools
4. System executes the tool calls and returns results to the LLM
5. LLM continues interaction based on the results