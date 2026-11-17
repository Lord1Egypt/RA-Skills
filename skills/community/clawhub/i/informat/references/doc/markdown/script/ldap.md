# informat.ldap LDAP Operations

## Overview

Use the `informat.ldap` object to connect to an LDAP (Lightweight Directory Access Protocol) directory server and perform search operations.

## connect

Create an LDAP connection
Connect to an LDAP server with the specified information. An exception will be thrown if the connection fails or username/password verification fails. The `connect` method can be used to check whether a user's username and password are valid.
After a successful connection, you can use the returned [LdapConnection](/guide/script/ldap.md#ldapconnection)
to perform queries, modifications, and additions. Note that after operations are complete, you need to call the `close` method of [LdapConnection](/guide/script/ldap.md#ldapconnection) to close the connection.

```javascript
informat.ldap.connect(info)
```

| Parameter   | Type                                                              | Description           |
|------|-----------------------------------------------------------------|--------------|
| info | [LdapConnectionInfo](/guide/script/model.md#ldapconnectioninfo) | LDAP server connection information |

**Return Value**

Returns a [LdapConnection](/guide/script/ldap.md#ldapconnection) object

**Example**

```js
let connection = null
try {
    connection = informat.ldap.connect({
        providerURL: 'LDAP://1.13.173.190:389',
        securityPrincipal: 'user',
        securityCredentials: 'pwd'
    })

} catch (e) {
    //Failed to connect to LDAP server or authentication failed
    console.error('Connection failed:', e)
} finally {
    if (connection != null) {
        connection.close();
    }
}
```

## LdapConnection

### close

Close the LDAP connection

```javascript
connection.close()
```

### search

Search for entries that match the criteria
Returns entries under the base DN that satisfy the conditions specified by the filter.

```javascript
connection.search(basedn, filter, control)
```

| Parameter      | Type                  | Description                                       |
|---------|---------------------|------------------------------------------|
| basedn  | `String`            | Full path of the base node, e.g., `cn=users,dc=informat,dc=cn` |
| filter  | `String`            | Query condition                                     |
| control | `LdapSearchControl` | Search control                                     |

:::: tabs
::: tab Search Condition Syntax

- AND condition (& (...K1...) (...K2...))
- OR condition (| (...K1...) (...K2...))
- Nested conditions (|(& (...K1...) (...K2...))(& (...K3...) (...K4...)))

:::
::: tab Query Condition Syntax

- Equals: (attribute=abc) , e.g. (&(objectClass=user)(displayName=Foeckeler)
- Not equals: (!(attribute=abc)) , e.g. (!objectClass=group)
- Not null:    (attribute=*) , e.g. (mailNickName=*)
- Is null: (!(attribute=*)) , e.g. (!proxyAddresses=*)
- Greater than or equals: (attribute>=abc) , e.g. (mdbStorageQuota>=100000)
- Less than or equals: (attribute<=abc) , e.g. (mdbStorageQuota<=100000)
- Wildcard: (attribute=ab*), e.g. (name=yan*)

:::
::::

**Return Value**

Type is Array<[LdapSearchResult](/guide/script/model.md#ldapsearchresult)>

**Example**

```js
// Query 10 entries under cn=Users,dc=informat,dc=cn, returning only id, name, age attributes.
const result = connect.search('cn=Users,dc=informat,dc=cn', 'name=*', {
    searchScope: 'SUBTREE', // Search scope, default is SUBTREE. SUBTREE returns all matching entries, ONELEVEL returns entries at the same level, OBJECT returns only matching objects
    countLimit: 10, // Optional. Maximum number of entries to return
    returningAttributes: ['id', 'name', 'age'] // Optional. List of attributes to return
})
// Output all entry names and their attributes
result.forEach(r => {
    console.log(r.name);
    r.attributes.forEach(ra => {
        console.log(ra.id + " = " + ra.values[0])
    })
})
```

### list

Enumerate the names bound in a naming context, along with the class names of objects bound to them

```javascript
connection.list(name)
```

| Parameter   | Type       | Description |
|------|----------|----|
| name | `String` | Name |

**Return Value**

Type is Array<[LdapListResult](/guide/script/model.md#ldaplistresult)>
Returns the list of bound objects

### getAttributes

Query the attributes of a specified node

```javascript
connection.getAttributes(dn)
```

| Parameter | Type       | Description          |
|----|----------|-------------|
| dn | `String` | Path of the node whose attributes to query |

**Return Value**

Type is Array<[LdapSearchResultAttribute](/guide/script/model.md#ldapsearchresultattribute)>
Returns the attribute list of the node

### addAttribute

Add attributes to a specified node

```javascript
connection.addAttribute(dn, attributes)
```

| Parameter         | Type                                                                       | Description          |
|------------|--------------------------------------------------------------------------|-------------|
| dn         | `String`                                                                 | Path of the node to modify attributes for |
| attributes | Array<[LdapModifyAttribute](/guide/script/model.md#ldapmodifyattribute)> | Attribute list        |

### updateAttribute

Update attributes of a specified node

```javascript
connection.updateAttribute(dn, attributes)
```

| Parameter         | Type                                                                       | Description          |
|------------|--------------------------------------------------------------------------|-------------|
| dn         | `String`                                                                 | Path of the node to modify attributes for |
| attributes | Array<[LdapModifyAttribute](/guide/script/model.md#ldapmodifyattribute)> | Attribute list        |

### deleteAttribute

Delete attributes of a specified node

```javascript
connection.deleteAttribute(dn, attributes)
```

| Parameter         | Type                                                                       | Description          |
|------------|--------------------------------------------------------------------------|-------------|
| dn         | `String`                                                                 | Path of the node to modify attributes for |
| attributes | Array<[LdapModifyAttribute](/guide/script/model.md#ldapmodifyattribute)> | Attribute list        |

### decodeSID

Decode the SID of an account in a Windows AD domain

```javascript
connection.decodeSID(sidAttribute)
```

| Parameter           | Type       | Description     |
|--------------|----------|--------|
| sidAttribute | `Object` | SID attribute value |

**Return Value**

Type is `String`
Returns the decoded SID value

### createEntry

Create a new LDAP entry (subcontext).

Used for creating "new entries" such as OUs and users. Note this differs from `addAttribute`, which can only append attributes to entries that already exist.

```javascript
connection.createEntry(dn, attributes)
```

| Parameter  | Type                                                                     | Description                                                                                                                                                              |
|------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dn         | `String`                                                                 | The full distinguished name of the new entry, e.g. `OU=Engineering,dc=informat,dc=cn`                                                                                    |
| attributes | Array<[LdapModifyAttribute](/guide/script/model.md#ldapmodifyattribute)> | Initial attribute list of the new entry. Must include `objectClass`. Multiple values for the same attribute are expressed as multiple `LdapModifyAttribute` entries (one value per entry). |

**Return Value**

No return value. An exception is thrown if the parent node does not exist, the attributes are invalid, or the target entry already exists.

**Example**

```js
// Create an organizational unit OU=Engineering under dc=informat,dc=cn
connection.createEntry('OU=Engineering,dc=informat,dc=cn', [
    { id: 'objectClass', value: 'top' },
    { id: 'objectClass', value: 'organizationalUnit' },
    { id: 'ou', value: 'Engineering' }
])

// Create a user under OU=Engineering
connection.createEntry('CN=80818,OU=Engineering,dc=informat,dc=cn', [
    { id: 'objectClass', value: 'top' },
    { id: 'objectClass', value: 'person' },
    { id: 'objectClass', value: 'organizationalPerson' },
    { id: 'objectClass', value: 'user' },
    { id: 'cn', value: '80818' },
    { id: 'sAMAccountName', value: '80818' },
    { id: 'displayName', value: 'Lin Wenya' },
    { id: 'userAccountControl', value: '514' } // Create as disabled first, then set password and enable
])
```

### deleteEntry

Delete an LDAP entry (subcontext).

```javascript
connection.deleteEntry(dn)
```

| Parameter | Type     | Description                                |
|-----------|----------|--------------------------------------------|
| dn        | `String` | The full distinguished name of the entry to delete |

**Return Value**

No return value. If the entry still has child entries, AD will return an error (LDAP error code 66 - NotAllowedOnNonLeaf). You must recursively delete all child entries first.

**Example**

```js
// Delete an empty OU
connection.deleteEntry('OU=Deprecated,dc=informat,dc=cn')

// Delete a user
connection.deleteEntry('CN=80818,OU=Engineering,dc=informat,dc=cn')
```

### renameEntry

Rename or move an LDAP entry (corresponds to the LDAP ModifyDN operation).

- Changing the RDN only (e.g. `CN=80818` → `CN=80927`): the parent container stays the same — this is a "rename"
- Moving across containers (`oldDn` and `newDn` have different parent DNs): this is a "move"

```javascript
connection.renameEntry(oldDn, newDn)
```

| Parameter | Type     | Description                                  |
|-----------|----------|----------------------------------------------|
| oldDn     | `String` | The current full distinguished name of the entry |
| newDn     | `String` | The target full distinguished name of the entry  |

**Return Value**

No return value. An exception is thrown if `oldDn` does not exist, `newDn` is already taken, or the LDAP server forbids cross-container moves.

**Example**

```js
// Rename: a user's employee code changes (same department)
connection.renameEntry(
    'CN=80818,OU=Engineering,dc=informat,dc=cn',
    'CN=80927,OU=Engineering,dc=informat,dc=cn'
)

// Move: a user transfers to another department
connection.renameEntry(
    'CN=80818,OU=Engineering,dc=informat,dc=cn',
    'CN=80818,OU=Product,dc=informat,dc=cn'
)

// Department rename: rename an OU
connection.renameEntry(
    'OU=Engineering,dc=informat,dc=cn',
    'OU=R&D,dc=informat,dc=cn'
)
```
### addAttributeEncoded

Add an attribute to the specified entry, with the attribute's `value` first encoded as a byte stream using the given `encoding`.

Used for writing attributes that require specific byte encodings. The most typical scenario is Windows AD's `unicodePwd` (which requires a UTF-16LE byte stream with the password wrapped in ASCII double quotes).

```javascript
connection.addAttributeEncoded(dn, attributes, encoding)
```

| Parameter  | Type                                                                     | Description                                                                                                                                                                                            |
|------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dn         | `String`                                                                 | The distinguished name of the entry to modify                                                                                                                                                          |
| attributes | Array<[LdapModifyAttribute](/guide/script/model.md#ldapmodifyattribute)> | List of attributes whose `value` is a string                                                                                                                                                           |
| encoding   | `String`                                                                 | Charset name (e.g. `"UTF-16LE"`, `"UTF-8"`, `"GBK"`); must be a Java-supported `Charset` name. When `null` or an empty string is passed, falls back to the regular `addAttribute` behavior (string write). |

**Return Value**

No return value. Throws an exception if the entry does not exist, the encoding is unsupported, or the attribute is invalid.

**Example**

```js
// Add an attribute that needs UTF-16LE encoding to a user entry
connection.addAttributeEncoded('CN=80818,OU=Engineering,dc=informat,dc=cn', [
    { id: 'someBinaryAttr', value: 'some-value' }
], 'UTF-16LE')
```

### updateAttributeEncoded

Update an attribute on the specified entry (REPLACE semantics). The `value` is first encoded as a byte stream using the given `encoding` before being written.

The most common use case: **setting a Windows AD user's password via `unicodePwd`**.

```javascript
connection.updateAttributeEncoded(dn, attributes, encoding)
```

| Parameter  | Type                                                                     | Description                                                                                                                                                                                               |
|------------|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dn         | `String`                                                                 | The distinguished name of the entry to modify                                                                                                                                                             |
| attributes | Array<[LdapModifyAttribute](/guide/script/model.md#ldapmodifyattribute)> | List of attributes whose `value` is a string                                                                                                                                                              |
| encoding   | `String`                                                                 | Charset name (e.g. `"UTF-16LE"`, `"UTF-8"`, `"GBK"`); must be a Java-supported `Charset` name. When `null` or an empty string is passed, falls back to the regular `updateAttribute` behavior (string write). |

**Return Value**

No return value. Throws an exception if the entry does not exist, the encoding is unsupported, or the server refuses the modification (e.g. AD rejects setting a password over a plaintext LDAP channel).

**Example**

```js
// Set a Windows AD user's password (must be invoked over LDAPS on port 636)
const password = '<ad-password>'
connection.updateAttributeEncoded(
    'CN=80818,OU=Engineering,dc=informat,dc=cn',
    [{ id: 'unicodePwd', value: `"${password}"` }],   // password must be wrapped in ASCII double quotes
    'UTF-16LE'
)
```

::: tip
Writing `unicodePwd` to AD requires LDAPS (port 636). Over plaintext LDAP on port 389, AD will reject the operation with `WILL_NOT_PERFORM`.
:::

### deleteAttributeEncoded

Delete an attribute from the specified entry, matching by the value encoded with the given `encoding`.

```javascript
connection.deleteAttributeEncoded(dn, attributes, encoding)
```

| Parameter  | Type                                                                     | Description                                                                                                                                                                                                  |
|------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dn         | `String`                                                                 | The distinguished name of the entry to modify                                                                                                                                                                |
| attributes | Array<[LdapModifyAttribute](/guide/script/model.md#ldapmodifyattribute)> | List of attributes whose `value` is a string                                                                                                                                                                 |
| encoding   | `String`                                                                 | Charset name (e.g. `"UTF-16LE"`, `"UTF-8"`, `"GBK"`); must be a Java-supported `Charset` name. When `null` or an empty string is passed, falls back to the regular `deleteAttribute` behavior (string match). |

**Return Value**

No return value.

**Example**

```js
// Delete a value previously written with UTF-16LE encoding
connection.deleteAttributeEncoded('CN=80818,OU=Engineering,dc=informat,dc=cn', [
    { id: 'someBinaryAttr', value: 'some-value' }
], 'UTF-16LE')
```
