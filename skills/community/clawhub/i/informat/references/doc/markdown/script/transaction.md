# informat.transaction Database Transaction Operations

## Overview

Use `informat.transaction` to perform transaction-related operations

## defaultTransactionDefinition

Create a default transaction definition

```javascript
informat.transaction.defaultTransactionDefinition()
```

***Return Value***
Default transaction definition, type is [TransactionDefinition](/guide/script/transaction.md#transactiondefinition)

***

## currentTransactionStatus

Get the current transaction status

```js
informat.transaction.currentTransactionStatus()
```

***Return Value***

Current transaction status, type is [TransactionStatus](/guide/script/transaction.md#transactionstatus)

***

## getTransactionStatus

Get a transaction based on the given transaction definition (TransactionDefinition) and return its runtime status

```js
informat.transaction.getTransactionStatus(td)
```

| Parameter | Type                                                                          | Description |
|----|-----------------------------------------------------------------------------|------|
| td | [TransactionDefinition](/guide/script/transaction.md#transactiondefinition) | Transaction definition |

***Return Value***

Transaction propagation behavior, type is [TransactionStatus](/guide/script/transaction.md#transactionstatus)

## commit

Commit a transaction

```js
informat.transaction.commit(ts)
```

| Parameter | Type                | Description |
|----|-------------------|------|
| ts | TransactionStatus | Transaction status |

## rollback

Rollback a transaction

```js
informat.transaction.rollback(ts)
```

| Parameter | Type                | Description |
|----|-------------------|------|
| ts | TransactionStatus | Transaction status |

## TransactionDefinition

### setPropagationBehavior

Set transaction propagation behavior

```js
td.setPropagationBehavior(pb)
```

| Parameter | Type      | Description |
|----|---------|--------|
| pb | Integer | Transaction propagation behavior |

Transaction propagation behaviors are as follows:

| Propagation Behavior            | Value | Description |
|---------------------------|---|------------------------------------------------|
| PROPAGATION_REQUIRED      | 0 | If there is no current transaction, create a new one; if a transaction already exists, join it. This is the default propagation behavior. |
| PROPAGATION_SUPPORTS      | 1 | If a current transaction exists, join it; if there is no transaction, execute in non-transactional mode. |
| PROPAGATION_MANDATORY     | 2 | If a current transaction exists, join it; if there is no transaction, throw an exception. |
| PROPAGATION_REQUIRES_NEW  | 3 | Always create a new transaction regardless of whether a current transaction exists. The current transaction (if any) is suspended and resumed after the new transaction completes. |
| PROPAGATION_NOT_SUPPORTED | 4 | Execute in non-transactional mode. If a current transaction exists, suspend it and resume after execution. |
| PROPAGATION_NEVER         | 5 | Execute in non-transactional mode. If a current transaction exists, throw an exception. |
| PROPAGATION_NESTED        | 6 | If a current transaction exists, execute within a nested transaction; if there is no transaction, create a new one. Nested transactions can be rolled back independently. |

***

### setPropagationBehaviorName

Set transaction propagation behavior

```js
td.setPropagationBehaviorName(pbName)
```

Example:

```
td.setPropagationBehaviorName('PROPAGATION_REQUIRED')
```

### getPropagationBehavior

Get transaction propagation behavior

```js
td.getPropagationBehavior()
```

***Return Value***

Transaction propagation behavior, type is `Integer`



***

### setIsolationLevel

Set transaction isolation level

```js
td.setIsolationLevel(isolationLevel)
```

| Parameter        | Type      | Description |
|----------------|---------|------|
| isolationLevel | Integer | Isolation level |

Isolation levels are defined as follows:

| Isolation Level                | Value | Description |
|----------------------------|----|--------------------------|
| ISOLATION_DEFAULT          | -1 | Default isolation level, uses the default isolation level of the underlying data source |
| ISOLATION_READ_UNCOMMITTED | 0  | Read uncommitted data, allows dirty reads, non-repeatable reads, and phantom reads |
| ISOLATION_READ_COMMITTED   | 1  | Read committed data, prevents dirty reads but allows non-repeatable reads and phantom reads |
| ISOLATION_REPEATABLE_READ  | 2  | Repeatable read, prevents dirty reads and non-repeatable reads but allows phantom reads |
| ISOLATION_SERIALIZABLE     | 3  | Serializable, prevents dirty reads, non-repeatable reads, and phantom reads |

### setIsolationLevelName

Set transaction isolation level

```js
td.setIsolationLevelName(isolationLevelName)
```

Example:

```js
td.setIsolationLevelName('ISOLATION_READ_UNCOMMITTED')
```

***

### getIsolationLevel

Get transaction isolation level

```js
td.getIsolationLevel()
```

***Return Value***

Transaction isolation level, type is `Integer`

***

### setTimeout

Set transaction timeout

```js
td.setTimeout(seconds)
```

| Parameter | Type      | Description |
|---------|---------|------|
| seconds | Integer | Timeout in seconds |

Example:

```js
var td = informat.transaction.defaultTransactionDefinition()
td.setTimeout(30)
```

In this example, we create a default TransactionDefinition object and call the setTimeout method to set the transaction timeout to 30 seconds. This means that if the transaction is not completed within 30 seconds, the transaction manager will abort the transaction and perform a rollback.

***

### getTimeout

Get transaction timeout in seconds

```js
td.getTimeout()
```

***Return Value***
Transaction timeout, type is `Integer`

***

### setReadOnly

Set whether the transaction is read-only

```js
td.setReadOnly(readOnly)
```

| Parameter  | Type      | Description |
|----------|---------|------|
| readOnly | Boolean | Whether read-only |

Read-only transactions are typically used for query operations because they do not need to modify data. Setting a transaction as read-only may help performance, as some databases may optimize for read-only transactions.


***

### isReadOnly

Check if the transaction is read-only

```js
td.isReadOnly()
```

***Return Value***
Whether the transaction is read-only, type is `Boolean`

***

### setName

Set transaction name

```js
td.setName(name)
```

| Parameter | Type     | Description |
|------|--------|----|
| name | String | Name |

Transaction names can help developers easily identify and trace transactions in logs and monitoring tools.

### getName

Get transaction name

```js
td.getName()
```

***Return Value***
Transaction name, type is `String`

## TransactionStatus

### isNewTransaction

Check if this is a new transaction

```js
ts.isNewTransaction()
```

***Return Value***
Whether it is a new transaction, type is `Boolean`

### isRollbackOnly

Check if the transaction is rollback-only

```js
ts.isRollbackOnly()
```

***Return Value***
Whether the transaction is rollback-only, type is `Boolean`

### isCompleted

Check if the transaction is completed

```js
ts.isCompleted()
```

***Return Value***
Whether the transaction is completed, type is `Boolean`

### setRollbackOnly

Set the transaction to rollback-only

```js
ts.setRollbackOnly()
```

**A Complete Example**

```js
var ts = informat.transaction.currentTransactionStatus(); // Get current transaction status
informat.transaction.commit(ts); // Commit current transaction
//
var td = informat.transaction.defaultTransactionDefinition(); // Create default transaction definition
td.setPropagationBehaviorName('PROPAGATION_REQUIRES_NEW'); // Change propagation behavior to new transaction
var ts = informat.transaction.getTransactionStatus(td); // Get transaction status
try {
    informat.table.insert('task', {
        'name': 'From script'
    }); // Insert a data table record
    informat.transaction.commit(ts); // Commit transaction
} catch (e) {
    informat.transaction.rollback(ts); // Rollback transaction on exception
}
```

:::tip
Note: In automation, if you need to start a new transaction so that subsequent steps can execute within a transaction, you need to run the following commands:

let td=informat.transaction.defaultTransactionDefinition();
td.setPropagationBehaviorName('PROPAGATION_REQUIRES_NEW');
let ts=informat.transaction.getTransactionStatus(td);

After executing these three commands in a code snippet, subsequent automation steps will execute within a transaction.
:::

## registerSynchronization

Register a transaction synchronization callback

```javascript
informat.transaction.registerSynchronization(ts)
```

| Parameter | Type     | Description |
|------|--------|----|
| ts | TransactionSynchronization | Transaction synchronization callback object |


***TransactionSynchronization***
The transaction synchronization callback object contains the following configurable listener functions:

### beforeCommit
Type: Function
Trigger timing: Executed before the transaction is committed
Parameter: readOnly (Boolean) - Indicates whether the transaction is read-only

### beforeCompletion
Type: Function
Trigger timing: Executed before transaction completion (whether commit or rollback)

### afterCommit
Type: Function
Trigger timing: Executed after the transaction is successfully committed (only triggered on commit)

### afterCompletion
Type: Function
Trigger timing: Executed after transaction completion (whether commit or rollback)
Parameter: status (Integer) - Completion status (0=commit, 1=rollback)

***Example***
```js
// Create synchronization callback object
var sync = {};
// Configure callback functions
sync.beforeCommit = function(readOnly) {
    console.log("Transaction is about to commit, read-only mode:", readOnly);
};

sync.beforeCompletion = function() {
    console.log("Pre-completion processing");
};

sync.afterCommit = function() {
    console.log("Transaction has been successfully committed");
};

sync.afterCompletion = function(status) {
    console.log("Transaction completion status:", status === 0 ? "Committed" : "Rolled back");
};

// Register callback
informat.transaction.registerSynchronization(sync);
```
