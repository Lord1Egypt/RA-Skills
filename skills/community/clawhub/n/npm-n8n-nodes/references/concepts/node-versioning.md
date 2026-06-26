# Node Versioning

When you need to change a node's behavior in a way that would break existing workflows (renaming a field, changing output structure, adding required params), use node versioning instead of changing the existing node in place.

## Table of Contents
1. [When to version vs. not](#1-when-to-version-vs-not)
2. [Simple versioned node](#2-simple-versioned-node)
3. [Multiple version classes (recommended for large changes)](#3-multiple-version-classes)
4. [Version routing pattern](#4-version-routing-pattern)
5. [Deprecating old versions](#5-deprecating-old-versions)

---

## 1. When to Version vs. Not

**Version (breaking change):**
- Renaming a node parameter that's used in expressions (`{{ $node.MyNode.json.oldField }}`)
- Removing a parameter
- Changing the output data structure
- Changing what a required field means

**Don't version (safe change):**
- Adding a new optional field with a default
- Adding a new operation or resource
- Fixing a bug without changing the interface
- Updating description text

---

## 2. Simple Versioned Node

For minor version bumps — same class, different version number:

```typescript
export class MyNode implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Node',
    name: 'myNode',
    version: [1, 2],           // ← supports both v1 and v2
    defaultVersion: 2,          // ← new instances get v2
    // ...
    properties: [
      // New field only shown in v2
      {
        displayName: 'Output Format',
        name: 'outputFormat',
        type: 'options',
        options: [
          { name: 'Simple', value: 'simple' },
          { name: 'Full',   value: 'full' },
        ],
        default: 'simple',
        displayOptions: {
          show: { '@version': [2] },    // ← special: show only on v2 nodes
        },
      },
      // Field removed in v2 (hide it, don't delete — old workflows may still use it)
      {
        displayName: 'Legacy Option',
        name: 'legacyOption',
        type: 'boolean',
        default: false,
        displayOptions: {
          show: { '@version': [1] },   // only visible on v1 nodes
        },
      },
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const nodeVersion = this.getNode().typeVersion;  // 1 or 2

    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];

    for (let i = 0; i < items.length; i++) {
      // Version-specific behavior
      if (nodeVersion === 1) {
        // old behavior
      } else {
        // new behavior
      }
    }

    return [returnData];
  }
}
```

---

## 3. Multiple Version Classes (Recommended for Large Changes)

For significant structural changes, split into separate class files:

```
nodes/MyNode/
├── MyNode.node.ts          ← router, decides which version to instantiate
├── v1/
│   └── MyNodeV1.node.ts   ← original implementation
└── v2/
    └── MyNodeV2.node.ts   ← new implementation
```

**MyNode.node.ts** (router):
```typescript
import { NodeVersionedType } from 'n8n-workflow';
import { MyNodeV1 } from './v1/MyNodeV1.node';
import { MyNodeV2 } from './v2/MyNodeV2.node';

export class MyNode extends NodeVersionedType {
  constructor() {
    const baseDescription = {
      displayName: 'My Node',
      name: 'myNode',
      icon: 'file:mynode.svg',
      group: ['transform'],
      defaultVersion: 2,
      description: 'Interact with My Service',
    };

    const nodeVersions = {
      1: new MyNodeV1(),
      2: new MyNodeV2(),
    };

    super(nodeVersions, baseDescription);
  }
}
```

**v1/MyNodeV1.node.ts**:
```typescript
import { INodeType, INodeTypeDescription } from 'n8n-workflow';

export class MyNodeV1 implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Node',
    name: 'myNode',
    version: 1,
    // ... v1 properties
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    // v1 logic
  }
}
```

**v2/MyNodeV2.node.ts**:
```typescript
export class MyNodeV2 implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Node',
    name: 'myNode',
    version: 2,
    // ... v2 properties (can be completely different)
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    // v2 logic
  }
}
```

---

## 4. Version Routing Pattern

Check version inside `execute()` to share code between versions:

```typescript
async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
  const version = this.getNode().typeVersion;
  const items   = this.getInputData();
  const returnData: INodeExecutionData[] = [];

  for (let i = 0; i < items.length; i++) {
    const response = await this.helpers.httpRequest({ ... });

    // v1 output: flat structure
    // v2 output: nested structure with metadata
    const outputData = version === 1
      ? response.data
      : { data: response.data, meta: { source: 'myservice', version: 2 } };

    returnData.push({ json: outputData, pairedItem: { item: i } });
  }

  return [returnData];
}
```

---

## 5. Deprecating Old Versions

Show a notice in v1 nodes pointing users to upgrade:

```typescript
properties: [
  // At the top of v1 properties list
  {
    displayName: 'This version of the node is deprecated. Please upgrade to v2 for new features and fixes.',
    name: 'deprecationNotice',
    type: 'notice',
    default: '',
    displayOptions: {
      show: { '@version': [1] },
    },
  },
  // ... rest of v1 properties
]
```

> ⚠️ Never delete an old version from the `version` array or from the versioned class map — existing workflows will break. Always keep all historical versions functional.
